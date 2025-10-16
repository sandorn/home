# !/usr/bin/env python3
"""
==============================================================
Description  : MySQL数据库操作模块 - 提供同步MySQL数据库连接和操作功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-09-10 16:30:00
FilePath     : /CODE/xjlib/xt_database/mysql.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- DbEngine类:MySQL数据库连接引擎，支持多种数据库驱动
- create_mysql_engine:创建MySQL连接实例的快捷函数
- 支持SQL执行、查询、插入、更新等基本操作
- 支持上下文管理器(with语句)使用方式
- 支持字典类型游标结果返回

主要特性:
- 支持两种初始化方式：直接参数方式和配置方式
- 配置从DB_CFG统一管理，支持多数据库配置切换
- 支持pymysql和MySQLdb两种驱动
- 自动提交模式，减少事务管理复杂性
- 完善的异常处理和日志记录
- 类型注解支持，提高代码可读性和IDE提示
==============================================================
"""

from __future__ import annotations

from typing import Any

import MySQLdb
import pymysql
from xt_database.cfg import DB_CFG
from xt_database.untilsql import make_insert_sql, make_update_sql
from xt_wraps.log import create_basemsg, log_wraps, mylog as logger


class DbEngine:
    """MySQL数据库连接引擎类，提供数据库连接和基本操作功能

    该类提供了同步MySQL数据库连接和操作的能力，主要适用于需要在同步代码中
    执行数据库操作的场景。支持多种数据库驱动和上下文管理器模式。

    Args:
        host: 数据库主机地址（直接参数方式）
        port: 数据库端口号（直接参数方式）
        user: 数据库用户名（直接参数方式）
        password: 数据库密码（直接参数方式）
        db: 数据库名称（直接参数方式）
        charset: 数据库字符集，默认为'utf8mb4'
        autocommit: 是否自动提交事务，默认为True
        tablename: 默认操作的表名，可选
        odbc: 数据库驱动类型，可选'pymysql'或'MySQLdb'，默认为'pymysql'

    Attributes:
        conn: 数据库连接对象
        cur: 数据库游标对象
        DictCursor: 字典类型游标类
        odbc: 数据库驱动类型
        tablename: 默认操作的表名
        cfg: 数据库连接配置字典
        charset: 数据库字符集

    Raises:
        ValueError: 当缺少必要的数据库连接参数时抛出
        Exception: 当数据库连接失败时抛出

    Example:
        >>> # 使用直接参数方式
        >>> db = DbEngine(
        >>>     host='localhost',
        >>>     port=3306,
        >>>     user='sandorn',
        >>>     password='123456',
        >>>     db='test_db'
        >>> )
    """

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str,
        charset: str = 'utf8mb4',
        autocommit: bool = True,
        tablename: str | None = None,
        odbc: str = 'pymysql',
        **kwargs: Any,
    ) -> None:
        """初始化DbEngine实例

        Args:
            host: 数据库主机地址（直接参数方式）
            port: 数据库端口号（直接参数方式）
            user: 数据库用户名（直接参数方式）
            password: 数据库密码（直接参数方式）
            db: 数据库名称（直接参数方式）
            charset: 数据库字符集，默认为'utf8mb4'
            autocommit: 是否自动提交事务，默认为True
            tablename: 默认操作的表名，可选
            odbc: 数据库驱动类型，可选'pymysql'或'MySQLdb'，默认为'pymysql'
            **kwargs: 其他数据库连接参数，会被合并到cfg中

        Notes:
            1. 连接成功后自动创建游标对象
            2. 支持pymysql和MySQLdb两种驱动
            3. 所有连接参数都是必需的
        """

        self.odbc: str = odbc
        self.tablename: str | None = tablename
        # 验证必要参数
        required_params = [
            (host, 'host'),
            (port, 'port'),
            (user, 'user'),
            (password, 'password'),
            (db, 'db'),
        ]
        for param, name in required_params:
            if param is None:
                raise ValueError(f'❌ 缺少必要的数据库连接参数: {name}')

        # 直接构建配置字典
        self.cfg = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'db': db,
            'charset': charset,
            'autocommit': autocommit,
        }
        self.cfg.update(kwargs)

        # 根据驱动类型创建连接
        if self.odbc == 'pymysql':
            self.conn = pymysql.connect(**self.cfg)
            self.DictCursor = pymysql.cursors.DictCursor
        else:  # MySQLdb驱动
            self.conn = MySQLdb.connect(**self.cfg)
            self.DictCursor = MySQLdb.cursors.DictCursor

        # 创建游标对象
        if hasattr(self, 'conn') and self.conn:
            self.cur = self.conn.cursor()

    def __enter__(self) -> DbEngine:
        """支持上下文管理器的入口方法"""
        logger.start(f'进入数据库上下文: {self.odbc}')
        return self

    def __exit__(self, exc_type: type[Exception] | None, exc_val: Exception | None, exc_tb: Any) -> bool:
        """支持上下文管理器的退出方法，自动关闭连接

        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常追踪信息
        """
        logger.stop(f'退出数据库上下文: {self.odbc}')

        # 如果发生异常，记录异常信息
        if exc_tb is not None:
            logger.fail(f'数据库操作异常: exc_type={exc_type}, exc_val={exc_val}')
            return False  # 不抑制异常

        return True

    def __del__(self) -> None:
        """对象销毁时自动关闭连接"""
        self.close()

    def __repr__(self) -> str:
        """返回对象的描述信息"""
        return f'MySQL数据库连接引擎，驱动类型: [{self.odbc}]；当前配置: {self.cfg}'

    __str__ = __repr__

    def close(self) -> None:
        """关闭数据库连接和游标"""
        try:
            if hasattr(self, 'cur') and self.cur:
                self.cur.close()
                logger.stop(f'游标已关闭: {self.odbc}')

            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
                logger.stop(f'数据库连接已关闭: {self.odbc}')

        except Exception as e:
            logger.fail(f'关闭数据库连接失败: {e}')

    @log_wraps
    def execute(self, sql: str, args: list[Any] | None = None) -> int:
        """执行SQL语句

        Args:
            sql: SQL语句
            args: SQL参数列表，默认为None

        Returns:
            int: 受影响的记录数量
        """
        self.cur.execute(sql, args)
        return self.cur.rowcount

    @log_wraps
    def query(self, sql: str, args: list[Any] | None = None, return_dict: bool = True) -> list[tuple[Any]] | None:
        """执行查询操作

        Args:
            sql: SQL查询语句
            args: SQL参数列表，默认为None

        Returns:
            Optional[list[tuple[Any]]]: 查询结果列表，如果查询失败返回None
        """
        self.cur.execute(sql, args)
        results = self.cur.fetchall()
        if return_dict:
            return self._dict_result(self.cur, results)
        return results

    @log_wraps
    def has_table(self, table_name: str) -> bool:
        """判断数据库是否包含指定表

        Args:
            table_name: 表名

        Returns:
            bool: 是否存在该表
        """
        self.cur.execute('show tables')
        tablerows = self.cur.fetchall()
        return any(rows[0] == table_name for rows in tablerows)

    @log_wraps
    def get_version(self) -> str | None:
        """获取数据库版本号

        Returns:
            Optional[str]: 数据库版本号，如果获取失败返回None
        """
        self.cur.execute('SELECT VERSION()')
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_all(self, table_name: str, args: list[Any] | None = None) -> list[tuple[Any]] | None:
        """获取表中所有记录

        Args:
            table_name: 表名
            args: SQL参数列表，默认为None

        Returns:
            Optional[list[tuple[Any]]]: 查询结果列表，如果查询失败返回None
        """
        sql = f'SELECT * FROM `{table_name}`'
        return self.query(sql, args)

    def _handle_error(self, prefix: str, error: Exception, sql: str) -> bool:
        """错误处理方法

        Args:
            prefix: 错误信息前缀
            error: 异常对象
            sql: 相关的SQL语句

        Returns:
            bool: 始终返回False表示操作失败
        """
        msg = create_basemsg(self._handle_error)
        try:
            if hasattr(self, 'conn'):
                self.conn.rollback()
        except Exception as rollback_err:
            logger.fail(f'{msg} | 事务回滚失败: {rollback_err}')

        # 记录错误日志，SQL语句过长时截断
        safe_sql = (sql[:200] + '...') if len(sql) > 200 else sql
        logger.fail(f'{msg} | {prefix} | {error}\nSQL: {safe_sql}')
        return False

    @log_wraps
    def _dict_result(self, cursor: Any, result: list[tuple]) -> list[dict[str, Any]]:
        """
        格式化查询结果为字典列表，使结果更易于使用

        Args:
            cursor: 数据库游标对象，用于获取列名信息
            result: 查询结果的原始元组列表，每行数据以元组形式存储

        Returns:
            List[Dict[str, Any]]: 格式化后的字典列表，每个字典的键为列名，值为对应的数据

        Notes:
            1. 自动处理嵌套结构的情况，确保数据格式一致性
            2. 只转换与列名数量匹配的行数据，避免数据格式错误
            3. 当结果为空时，返回空列表

        Example:
            >>> # 假设cursor是一个包含'name'和'age'列的游标对象
            >>> raw_result = [(1, '张三', 25), (2, '李四', 30)]
            >>> # 格式化结果类似: [{'id': 1, 'name': '张三', 'age': 25}, {'id': 2, 'name': '李四', 'age': 30}]
        """
        if not result:
            return []
        # 获取列名
        column_names = [desc[0] for desc in cursor.description]
        # 将元组列表转换为字典列表
        formatted_result = []
        for row in result:
            # 处理嵌套结构的情况
            if isinstance(row, (list, tuple)) and len(row) == 1 and isinstance(row[0], (list, tuple)):
                row = row[0]

            # 确保row是可迭代的，并且长度与列名匹配
            if isinstance(row, (list, tuple)) and len(row) == len(column_names):
                formatted_row = {column_names[i]: row[i] for i in range(len(column_names))}
                formatted_result.append(formatted_row)
        return formatted_result

    def insert_many(self, data_list: list[dict[str, Any]] | tuple[dict[str, Any]], table_name: str) -> int | None:
        """批量插入数据

        Args:
            data_list: 数据列表，每个元素为字典
            table_name: 表名

        Raises:
            TypeError: 当data_list不是列表或元组时
        """
        if not isinstance(data_list, (list, tuple)):
            raise TypeError('data_list must be list or tuple type')

        if not data_list:
            return None
        row_count = 0
        for item in data_list:
            row_count += self.insert(item, table_name)
        return row_count

    @log_wraps
    def insert(self, data: dict[str, Any], table_name: str) -> int | None:
        """插入单条数据

        Args:
            data: 数据字典
            table_name: 表名

        Returns:
            int | None: 受影响的记录数量，如果插入失败返回None

        Raises:
            ValueError: 当data不是字典时
        """
        if not isinstance(data, dict):
            raise ValueError('data must be dict type')

        sql_result = make_insert_sql(data, table_name)
        # 处理可能的元组返回值
        if isinstance(sql_result, tuple):
            sql, params = sql_result
            self.cur.execute(sql, params)
        else:
            self.cur.execute(sql_result)
        return self.cur.rowcount

    @log_wraps
    def update(self, new_data: dict[str, Any], condition: dict[str, Any], table_name: str) -> int | None:
        """更新数据

        Args:
            new_data: 新数据字典
            condition: 条件字典
            table_name: 表名

        Returns:
            int | None: 受影响的记录数量，如果更新失败返回None

        Raises:
            ValueError: 当new_data不是字典时
        """
        if not isinstance(new_data, dict):
            raise ValueError('new_data must be dict type')

        sql_result = make_update_sql(new_data, condition, table_name)
        # 处理可能的元组返回值
        if isinstance(sql_result, tuple):
            sql, params = sql_result
            self.cur.execute(sql, params)
            return self.cur.rowcount
        self.cur.execute(sql_result)
        return self.cur.rowcount

    @log_wraps
    def query_dict(self, sql: str) -> list[dict[str, Any]] | bool:
        """执行查询并返回字典类型结果

        Args:
            sql: SQL查询语句

        Returns:
            Union[list[dict[str, Any]], bool]: 查询结果列表(字典形式)，如果查询失败返回False
        """
        # 创建字典类型游标
        if self.DictCursor is None:
            cursor_dict = self.conn.cursor(dictionary=True)  # mysql-connector 驱动
        elif isinstance(self.DictCursor, int):
            cursor_dict = self.conn.cursor(self.DictCursor)  # 其他驱动
        else:
            cursor_dict = self.conn.cursor(self.DictCursor)

        cursor_dict.execute(sql)
        results = cursor_dict.fetchall()
        cursor_dict.close()  # 关闭字典游标
        return results if results else []


def create_mysql_engine(db_key: str = 'default', tablename: str | None = None, autocommit: bool = True, odbc: str = 'pymysql', **kwargs) -> DbEngine:
    """快捷函数 - 提供更简便的数据库操作方式
    创建MySQL连接实例的快捷函数 - 使用配置方式初始化
    该函数根据提供的数据库配置键名(db_key)，从DB_CFG配置中获取数据库连接参数，
    并使用这些参数初始化一个DbEngine实例。支持指定默认操作的表名、是否自动提交事务
    以及使用的数据库驱动类型。

    Args:
        db_key: 数据库配置键名，用于从DB_CFG中获取对应的数据库配置，默认为'default'
        tablename: 默认操作的表名，可选
        autocommit: 是否自动提交事务，默认为True
        odbc: 数据库驱动类型，可选'pymysql'或'MySQLdb'，默认为'pymysql'

    Returns:
        DbEngine: MySQL连接实例，已完成连接初始化

    Raises:
        ValueError:
            - 当db_key参数不是字符串类型时抛出
            - 当DB_CFG中不存在指定的配置键时抛出

    Example:
        >>> # 使用配置方式（推荐）
        >>> db = create_mysql_engine()  # 使用默认配置
        >>> db = create_mysql_engine('test_db')  # 使用指定配置
        >>> db = create_mysql_engine('test_db', 'users', False, 'MySQLdb')  # 指定配置、表名、事务设置和驱动
    """
    if not isinstance(db_key, str):
        raise ValueError(f'配置键非字符串类型: [{type(db_key).__name__}]')

    # 配置键存在性检查
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f'配置 [{db_key}] 不存在 ')

    # 获取配置并创建连接池
    cfg = DB_CFG[db_key].value.copy()
    cfg.pop('type', None)  # 移除类型字段(如果存在)

    return DbEngine(**cfg, autocommit=autocommit, tablename=tablename, odbc=odbc, **kwargs)


# ruff:noqa:S608
class TestMySQLEngine:
    """MySQL数据库引擎测试类"""

    def __init__(self):
        """初始化测试类"""
        self.test_db = None  # 测试数据库实例
        self.test_table = 'test_mysql_engine'
        self.test_data = [
            {'name': '张三', 'age': 28, 'email': 'zhangsan@example.com'},
            {'name': '李四', 'age': 32, 'email': 'lisi@example.com'},
            {'name': '王五', 'age': 45, 'email': 'wangwu@example.com'},
        ]

    def setup(self):
        """设置测试环境"""
        logger.info('\n===================== 开始设置测试环境 =====================')
        # 使用配置方式创建数据库连接
        self.test_db = create_mysql_engine('default')
        logger.ok('成功创建数据库连接')

        # 创建测试表
        self._create_test_table()
        logger.ok('成功创建测试表')
        logger.info('===================== 测试环境设置完成 =====================\n')

    def teardown(self):
        """清理测试环境"""
        logger.info('\n===================== 开始清理测试环境 =====================')
        try:
            # 删除测试表
            if self.test_db and self._has_test_table():
                sql = f'DROP TABLE IF EXISTS `{self.test_table}`'
                self.test_db.execute(sql)
                logger.ok(f'成功删除测试表: {self.test_table}')
        except Exception as e:
            logger.fail(f'清理测试环境失败: {e}')
        logger.info('===================== 测试环境清理完成 =====================\n')

    def _create_test_table(self):
        """创建测试表"""
        # 先删除可能存在的表
        sql = f'DROP TABLE IF EXISTS `{self.test_table}`'
        self.test_db.execute(sql)

        # 创建新表
        sql = f"""
        CREATE TABLE `{self.test_table}` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `name` VARCHAR(50) NOT NULL,
            `age` INT NOT NULL,
            `email` VARCHAR(100) NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.test_db.execute(sql)

    def _has_test_table(self):
        """检查测试表是否存在"""
        return self.test_db.has_table(self.test_table)

    def test_direct_params_initialization(self):
        """测试直接参数方式初始化"""
        logger.info('\n===== 测试直接参数方式初始化 =====')
        try:
            # 从配置中获取参数
            from xt_database.cfg import DB_CFG

            cfg = DB_CFG.default.value.copy()

            # 使用直接参数方式创建连接
            db = DbEngine(host=cfg['host'], port=cfg['port'], user=cfg['user'], password=cfg['password'], db=cfg['db'])

            # 验证连接
            version = db.get_version()
            logger.ok(f'直接参数方式初始化成功，数据库版本: {version}')

            # 关闭连接
            return True
        except Exception as e:
            logger.fail(f'直接参数方式初始化失败: {e}')
            return False

    def test_config_initialization(self):
        """测试配置方式初始化"""
        logger.info('\n===== 测试配置方式初始化 =====')
        try:
            # 使用配置方式创建连接
            db = create_mysql_engine('default')

            # 验证连接
            version = db.get_version()
            logger.ok(f'配置方式初始化成功，数据库版本: {version}')

            return True
        except Exception as e:
            logger.fail(f'配置方式初始化失败: {e}')
            return False

    def test_execute_sql(self):
        """测试执行SQL语句"""
        logger.info('\n===== 测试执行SQL语句 =====')
        try:
            # 执行简单的SQL语句
            sql = 'SELECT 1 + 1 AS result'
            row_count = self.test_db.execute(sql)
            logger.ok(f'SQL执行成功，影响行数: {row_count}')

            # 验证结果
            result = self.test_db.query(sql)
            if result and result[0]['result'] == 2:
                logger.ok(f'SQL执行结果验证成功: {result}')
                return True
            logger.fail(f'SQL执行结果验证失败: {result}')
            return False
        except Exception as e:
            logger.fail(f'执行SQL语句失败: {e}')
            return False

    def test_query(self):
        """测试查询操作"""
        logger.info('\n===== 测试查询操作 =====')
        try:
            # 插入测试数据
            for data in self.test_data:
                self.test_db.insert(data, self.test_table)

            # 执行查询
            sql = f'SELECT * FROM `{self.test_table}`'
            results = self.test_db.query(sql)

            if results and len(results) == len(self.test_data):
                logger.ok(f'查询成功，返回 {len(results)} 条记录')
                logger.debug(f'查询结果示例: {results[0]}')
                return True
            logger.fail(f'查询失败，返回 {len(results) if results else 0} 条记录')
            return False
        except Exception as e:
            logger.fail(f'查询操作失败: {e}')
            return False

    def test_insert_single(self):
        """测试插入单条数据"""
        logger.info('\n===== 测试插入单条数据 =====')
        try:
            # 插入单条数据
            data = {'name': '赵六', 'age': 36, 'email': 'zhaoliu@example.com'}
            row_count = self.test_db.insert(data, self.test_table)

            if row_count == 1:
                logger.ok(f'插入单条数据成功，影响行数: {row_count}')

                # 验证插入结果
                sql = f"SELECT * FROM `{self.test_table}` WHERE name = '赵六'"
                results = self.test_db.query(sql)
                if results and len(results) == 1:
                    logger.ok('插入结果验证成功')
                    return True
                logger.fail('插入结果验证失败')
                return False
            logger.fail(f'插入单条数据失败，影响行数: {row_count}')
            return False
        except Exception as e:
            logger.fail(f'插入单条数据失败: {e}')
            return False

    def test_insert_many(self):
        """测试批量插入数据"""
        logger.info('\n===== 测试批量插入数据 =====')
        try:
            # 批量插入数据
            batch_data = [{'name': '孙七', 'age': 29, 'email': 'sunqi@example.com'}, {'name': '周八', 'age': 42, 'email': 'zhouba@example.com'}]
            row_count = self.test_db.insert_many(batch_data, self.test_table)

            if row_count == len(batch_data):
                logger.ok(f'批量插入数据成功，影响行数: {row_count}')

                # 验证插入结果
                sql = f"SELECT * FROM `{self.test_table}` WHERE name IN ('孙七', '周八')"
                results = self.test_db.query(sql)
                if results and len(results) == len(batch_data):
                    logger.ok('批量插入结果验证成功')
                    return True
                logger.fail('批量插入结果验证失败')
                return False
            logger.fail(f'批量插入数据失败，影响行数: {row_count}')
            return False
        except Exception as e:
            logger.fail(f'批量插入数据失败: {e}')
            return False

    def test_update(self):
        """测试更新数据"""
        logger.info('\n===== 测试更新数据 =====')
        try:
            # 更新数据
            new_data = {'age': 30, 'email': 'zhangsan_new@example.com'}
            condition = {'name': '张三'}
            row_count = self.test_db.update(new_data, condition, self.test_table)

            if row_count >= 1:
                logger.ok(f'更新数据成功，影响行数: {row_count}')

                # 验证更新结果
                sql = f"SELECT * FROM `{self.test_table}` WHERE name = '张三'"
                results = self.test_db.query(sql)
                if results and results[0]['age'] == 30 and results[0]['email'] == 'zhangsan_new@example.com':
                    logger.ok('更新结果验证成功')
                    return True
                logger.fail('更新结果验证失败')
                return False
            logger.fail(f'更新数据失败，影响行数: {row_count}')
            return False
        except Exception as e:
            logger.fail(f'更新数据失败: {e}')
            return False

    def test_get_all(self):
        """测试获取表中所有记录"""
        logger.info('\n===== 测试获取表中所有记录 =====')
        try:
            # 获取所有记录
            results = self.test_db.get_all(self.test_table)

            if results:
                logger.ok(f'获取表中所有记录成功，返回 {len(results)} 条记录')
                logger.debug(f'记录示例: {results[0]}')
                return True
            logger.fail(f'获取表中所有记录失败，返回 {len(results) if results else 0} 条记录')
            return False
        except Exception as e:
            logger.fail(f'获取表中所有记录失败: {e}')
            return False

    def test_has_table(self):
        """测试检查表是否存在"""
        logger.info('\n===== 测试检查表是否存在 =====')
        try:
            # 检查测试表是否存在
            exists = self.test_db.has_table(self.test_table)

            if exists:
                logger.ok(f'检查表存在成功，表 {self.test_table} 存在')
                return True
            logger.fail(f'检查表存在失败，表 {self.test_table} 不存在')
            return False
        except Exception as e:
            logger.fail(f'检查表是否存在失败: {e}')
            return False

    def test_get_version(self):
        """测试获取数据库版本"""
        logger.info('\n===== 测试获取数据库版本 =====')
        try:
            # 获取数据库版本
            version = self.test_db.get_version()

            if version:
                logger.ok(f'获取数据库版本成功: {version}')
                return True
            logger.fail('获取数据库版本失败')
            return False
        except Exception as e:
            logger.fail(f'获取数据库版本失败: {e}')
            return False

    def test_context_manager(self):
        """测试上下文管理器方式"""
        logger.info('\n===== 测试上下文管理器方式 =====')
        try:
            # 使用上下文管理器
            with create_mysql_engine('default') as db_ctx:
                # 执行操作
                version = db_ctx.get_version()
                logger.ok(f'上下文管理器方式获取版本: {version}')

                # 执行查询
                sql = f'SELECT COUNT(*) AS count FROM `{self.test_table}`'
                result = db_ctx.query(sql)
                logger.ok(f'上下文管理器方式执行查询成功，表记录数: {result[0]["count"]}')

            logger.ok('上下文管理器方式测试成功')
            return True
        except Exception as e:
            logger.fail(f'上下文管理器方式测试失败: {e}')
            return False

    def test_error_handling(self):
        """测试错误处理"""
        logger.info('\n===== 测试错误处理 =====')
        try:
            # 执行错误的SQL语句
            invalid_sql = 'SELECT * FROM non_existent_table'
            result = self.test_db.query(invalid_sql)

            # 正常情况下，这里应该返回None或False
            if result is None or result is False:
                logger.ok('错误处理测试成功，正确处理了无效的SQL语句')
                return True
            logger.fail('错误处理测试失败，未能正确处理无效的SQL语句')
            return False
        except Exception as e:
            logger.fail(f'错误处理测试失败: {e}')
            return False

    def run_all_tests(self):
        """运行所有测试"""
        logger.info('\n' + '-' * 60 + '\n' + '                    MySQL数据库引擎全面测试\n' + '-' * 60)

        # 测试结果统计
        tests_run = 0
        tests_passed = 0

        try:
            # 设置测试环境
            self.setup()

            # 定义测试方法列表
            test_methods = [
                self.test_config_initialization,
                self.test_direct_params_initialization,
                self.test_execute_sql,
                self.test_query,
                self.test_insert_single,
                self.test_insert_many,
                self.test_update,
                self.test_get_all,
                self.test_has_table,
                self.test_get_version,
                self.test_context_manager,
                self.test_error_handling,
            ]

            # 运行每个测试方法
            for test_method in test_methods:
                tests_run += 1
                method_name = test_method.__name__
                logger.info(f'\n[{tests_run}/{len(test_methods)}] 运行测试: {method_name}')

                if test_method():
                    tests_passed += 1
                    logger.ok(f'测试通过: {method_name}')
                else:
                    logger.fail(f'测试失败: {method_name}')

            # 输出测试结果摘要
            logger.info(
                '\n'
                + '-' * 60
                + '\n'
                + '                    测试结果摘要\n'
                + f'                    总测试数: {tests_run}\n'
                + f'                    通过测试数: {tests_passed}\n'
                + f'                    失败测试数: {tests_run - tests_passed}\n'
                + f'                    通过率: {(tests_passed / tests_run * 100):.2f}%\n'
                + '-' * 60
            )

        finally:
            # 清理测试环境
            self.teardown()

        # 返回测试是否全部通过
        return tests_run == tests_passed


if __name__ == '__main__':
    """运行MySQL数据库引擎测试"""
    test_runner = TestMySQLEngine()
    all_passed = test_runner.run_all_tests()
    # 测试配置方式连接（推荐使用）
    default_db = create_mysql_engine()
    logger.ok(f'默认配置数据库版本: {default_db.get_version()}')
