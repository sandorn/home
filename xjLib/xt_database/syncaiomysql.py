# !/usr/bin/env python
"""
==============================================================
Description  : 同步异步MySQL工具模块 - 提供同步环境下调用异步MySQL操作的统一接口
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-29 23:35:00
LastEditTime : 2025-09-06 12:00:00
FilePath     : /CODE/xjlib/xt_database/syncaiomysql.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- SyncAioMySQL:同步环境下调用异步MySQL操作的数据库工具类
- create_async_mysql:创建异步MySQL连接实例的快捷函数
- 自动管理数据库连接池，高效处理并发请求
- 提供安全的参数化SQL语句构建，防止SQL注入
- 支持单条和批量数据操作（查询、插入、更新）

主要特性:
- 基于aiomysql的异步实现，提供同步调用接口，避免阻塞
- 支持多数据库配置切换，灵活适应不同环境
- 自动提交模式，简化事务处理流程
- 完整的类型注解，提升代码健壮性和开发体验
- 统一的异常处理和详细的错误日志记录
- 结果自动格式化，返回易用的字典列表结构
==============================================================
参考文档:
- https://www.yangyanxing.com/article/aiomysql_in_python.html
- https://blog.csdn.net/ydyang1126/article/details/78226701/
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import Coroutine
from typing import Any

from aiomysql import sa as aiosa
from xt_database.cfg import DB_CFG
from xt_database.untilsql import make_insert_sql, make_update_sql
from xt_wraps.log import create_basemsg, log_wraps
from xt_wraps.log import mylog as logger

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class SyncAioMySQL:
    """
    同步环境下调用异步MySQL操作的数据库工具类

    该类提供了在同步环境中调用异步MySQL操作的能力，解决了在不支持异步的项目中
    使用aiomysql的需求。主要适用于需要在同步代码中高效执行数据库操作的场景。

    核心功能:
    - 自动管理数据库连接池，提高连接复用率
    - 支持单条和批量SQL操作，高效处理数据
    - 提供参数化SQL构建，防止SQL注入
    - 支持结果格式化，便于数据处理
    - 完整的异常处理和日志记录

    典型应用场景:
    - 非异步Web框架中需要高效数据库操作
    - 数据处理脚本和ETL工具
    - 需要在同步代码中集成异步数据库操作的项目

    设计理念:
    - 采用同步接口封装异步实现，降低学习成本
    - 自动管理事件循环，简化使用流程
    - 支持并发执行多条SQL语句，提高效率
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
        pool_recycle: int = -1,
        tablename: str | None = None,
        **kwargs,
    ) -> None:
        """
        初始化SyncAioMySQL实例

        Args:
            host: 数据库主机地址
            port: 数据库端口号
            user: 数据库用户名
            password: 数据库密码
            db: 数据库名称
            charset: 数据库字符集，默认为'utf8mb4'
            autocommit: 是否自动提交事务，默认为True
            pool_recycle: 连接池回收时间，单位秒，-1表示不回收，默认为-1
            tablename: 默认操作的表名
            **kwargs: 其他aiomysql.create_engine支持的参数

        Notes:
            1. 自动创建或获取事件循环，确保异步操作能够正确执行
            2. 初始化时自动创建数据库引擎连接池
            3. 推荐在程序启动时创建实例，避免频繁创建连接池

        Example:
            >>> # 基本初始化
            >>> db = SyncAioMySQL('localhost', 3306, 'user', 'password', 'dbname')
            >>> # 带额外参数的初始化
            >>> db = SyncAioMySQL('localhost', 3306, 'user', 'password', 'dbname', autocommit=True, tablename='users')
        """
        self.tablename = tablename
        self.engine = None

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
                raise ValueError(f'缺少必要的数据库连接参数: {name}')

        # 设置直接参数
        self.cfg = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'db': db,
            'charset': charset,
            'autocommit': autocommit,
            'echo': __name__ == '__main__',
            'pool_recycle': pool_recycle,
        }
        self.cfg.update(kwargs)
        # 获取或创建事件循环
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        self.run_until_loop([self._create_engine()])

    def __del__(self) -> None:
        """
        显式关闭数据库连接和事件循环资源

        Notes:
            1. 优雅关闭数据库连接池，释放资源
            2. 安全关闭事件循环，避免资源泄漏
            3. 用户应该在不再需要数据库连接时主动调用此方法
        """
        # 首先关闭所有连接
        msg = create_basemsg(self.__del__)
        if hasattr(self, 'engine') and self.engine is not None:
            try:
                # 手动清理连接池中的所有连接
                if hasattr(self.engine, '_pool') and self.engine._pool is not None:
                    # 立即关闭所有连接，而不是等待它们自然超时
                    self.loop.run_until_complete(self.engine._pool.clear())
                    logger.stop(f'{msg} | 连接池已经清理')
            except Exception as e:
                logger.warning(f'{msg} | 清理连接池时发生异常: {e}')

            try:
                self.engine.close()
                if hasattr(self, 'loop') and self.loop is not None and not self.loop.is_closed():
                    self.loop.run_until_complete(self.engine.wait_closed())
                logger.stop(f'{msg} | 数据引擎已关闭')
            except Exception as e:
                logger.warning(f'{msg} | 关闭引擎时发生异常: {e}')
            finally:
                self.engine = None

        # 关闭事件循环
        if hasattr(self, 'loop') and self.loop is not None:
            try:
                if not self.loop.is_closed():
                    # 取消所有计划任务
                    for task in asyncio.all_tasks(self.loop):
                        task.cancel()
                    # 运行一次循环以处理取消操作
                    self.loop.run_until_complete(asyncio.sleep(0))
                    self.loop.close()
                    logger.stop(f'{msg} | 事件循环已关闭')
            except Exception as e:
                logger.warning(f'{msg} | 关闭事件循环时发生异常: {e}')
            finally:
                self.loop = None

    @log_wraps
    async def _create_engine(self) -> None:
        """
        创建数据库引擎连接池

        Raises:
            Exception: 当创建引擎失败时抛出

        Notes:
            1. 使用实例初始化时设置的参数创建连接池
            2. 在开发模式下启用SQL语句回显
            3. 创建失败时记录详细错误日志
        """
        self.engine = await aiosa.create_engine(**self.cfg)

    def run_until_loop(self, coro_list: list[Coroutine]) -> list[Any]:
        """
        在事件循环中运行协程列表，实现同步调用异步操作

        Args:
            coro_list: 协程对象列表，包含需要执行的异步操作

        Returns:
            List[Any]: 协程执行结果列表，与输入的协程列表顺序一一对应

        Notes:
            1. 使用asyncio.gather确保所有协程并发执行
            2. 设置return_exceptions=True使单个协程失败不会影响整体执行
            3. 采用事件循环的run_until_complete方法而非asyncio.run，避免重复创建事件循环

        Example:
            >>> # 运行单个协程
            >>> result = db.run_until_loop([db._create_engine()])
            >>> # 运行多个协程并发执行
            >>> results = db.run_until_loop([coro1, coro2, coro3])
        """
        # 确保并发 + 结果收集 + 异常可控
        tasks = [self.loop.create_task(coro) for coro in coro_list]
        return self.loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

    @log_wraps(log_result=False)
    def query(self, querys: str | list[str], *parameters, return_dict: bool = True, **kwparameters) -> list[Any]:
        """
        执行SQL查询操作，支持单条或多条SQL语句

        Args:
            querys: SQL查询语句或语句列表，可以是SELECT、INSERT、UPDATE、DELETE等任意SQL语句
            *parameters: 位置参数，用于参数化查询，提高安全性
            return_dict: 是否返回字典列表，默认为True，若设为False则返回原始元组列表
            **kwparameters: 命名参数，用于参数化查询，提高安全性

        Returns:
            List[Any]:
                - 当sql为单条语句时，返回查询结果或受影响的行数
                - 当sql为多条语句时，返回与语句列表长度相同的结果列表
                - 对于SELECT语句，结果默认为字典列表（return_dict=True），或原始元组列表（ return_dict=False）
                - 对于非SELECT语句，结果为受影响的行数

        Raises:
            Exception: 当SQL执行失败时抛出，包含详细的错误信息

        Example:
            >>> db = SyncAioMySQL('localhost', 3306, 'user', 'password', 'dbname')
            >>> # 单条查询，返回字典列表
            >>> result = db.query('SELECT * FROM users')
            >>> # 参数化查询
            >>> result = db.query('SELECT * FROM users WHERE id=:id', {'id': 1})
            >>> # 执行非SELECT语句
            >>> affected_rows = db.query('DELETE FROM users WHERE status=0')
            >>> # 获取原始结果
            >>> raw_result = db.query('SELECT * FROM users', return_dict=False)
            >>> # 多条查询
            >>> results = db.query(['SELECT * FROM users LIMIT 10', 'SELECT COUNT(*) FROM users'])
        """
        # 如果是多条SQL语句，批量执行
        if isinstance(querys, list):
            return self.run_until_loop([self._query(query, *parameters, return_dict=return_dict, **kwparameters) for query in querys])
        # 单条SQL语句执行
        return self.run_until_loop([self._query(querys, *parameters, return_dict=return_dict, **kwparameters)])[0]

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

    @log_wraps(log_result=False)
    async def _query(self, query: str, *parameters, return_dict: bool = True, **kwparameters) -> Any:
        """
        异步执行单条SQL查询（内部方法）

        Args:
            query: SQL查询语句
            params: SQL参数（可选），用于参数化查询

        Returns:
            Any:
                - 对于SELECT语句：返回查询结果（默认是格式化的字典列表，当cursorclass=aiomysql.cursors.Cursor时返回原始元组列表）
                - 对于非SELECT语句：返回受影响的行数

        Raises:
            Exception: 当查询执行失败时抛出，包含详细的错误信息、SQL语句和参数

        Notes:
            1. 内部方法，不建议直接调用，应使用query方法代替
            2. 自动从连接池获取连接并执行SQL
            3. 执行失败时记录详细的错误日志
        """
        if self.engine is None:
            self._create_engine()

        async with self.engine.acquire() as conn, conn._connection.cursor() as cursor:
            await cursor.execute(query, kwparameters or parameters)
            raw_res = await cursor.fetchall()
            if return_dict:
                return self._dict_result(cursor, raw_res)
            return raw_res

    def execute(self, query: str, *parameters, **kwparameters) -> int:
        """
        执行 INSERT/UPDATE/DELETE 等语句，返回受影响行数

        Args:
            query: SQL语句，可包含占位符
            *parameters: SQL语句的参数值
            **kwparameters: SQL语句的关键字参数值（字典形式）

        Returns:
            int: 受影响的行数
        """
        return self.run_until_loop([self._execute(query, *parameters, **kwparameters)])[0]

    @log_wraps
    async def _execute(self, query: str, *parameters, **kwparameters) -> int:
        """执行 INSERT/UPDATE/DELETE 等语句，返回受影响行数

        Args:
            query: SQL语句，可包含占位符
            *parameters: SQL语句的参数值
            **kwparameters: SQL语句的关键字参数值（字典形式）

        Returns:
            int: 受影响的行数

        Raises:
            ValueError: 连接池未初始化时抛出
            Exception: 执行SQL时发生错误
        """
        if self.engine is None:
            self._create_engine()

        async with self.engine.acquire() as conn, conn._connection.cursor() as cursor:
            result = await cursor.execute(query, kwparameters or parameters)
            await conn._connection.commit()
            return result

    def insert(self, data_list: dict[str, Any] | list[dict[str, Any]], tablename: str | None = None) -> list[int]:
        """执行数据插入操作

        Args:
            data_list: 单条或多条数据字典，字典的键为列名，值为要插入的数据
            tablename: 表名（可选，默认使用实例化时指定的表名）

        Returns:
            list[int]: 插入操作受影响的行数列表

        Raises:
            ValueError: 当表名为空时抛出
            Exception: 当插入操作失败时抛出

        Example:
            >>> db = SyncAioMySQL('localhost', 3306, 'user', 'password', 'dbname', tablename='users')
            >>> # 插入单条数据
            >>> item = {'username': '张三', 'password': '123456', 'created_at': '2024-05-18'}
            >>> result = db.insert(item)
            >>> # 插入多条数据
            >>> data_list = [{'username': '张三', 'password': '123456'}, {'username': '李四', 'password': '654321'}]
            >>> results = db.insert(data_list)
        """
        tablename = tablename or self.tablename
        if not tablename:
            raise ValueError('表名不能为空，请在参数中指定或在实例化时设置')

        if isinstance(data_list, dict):
            data_list = [data_list]

        # 生成参数化SQL和参数列表
        sql_params_list = [make_insert_sql(data_dict, tablename) for data_dict in data_list]
        coro = [self._execute(sql, *params) for sql, params in sql_params_list]
        return self.run_until_loop(coro)

    def update(
        self,
        data_list: dict[str, Any] | list[dict[str, Any]],
        where_list: dict[str, Any] | list[dict[str, Any]],
        tablename: str | None = None,
    ) -> list[int]:
        """执行数据更新操作

        Args:
            data_list: 单条或多条更新数据字典，字典的键为列名，值为要更新的数据
            where_list: 单条或多条WHERE条件字典，用于指定更新哪些记录
            tablename: 表名（可选，默认使用实例化时指定的表名）

        Returns:
            List[Any]: 更新结果列表，每个元素表示对应更新操作受影响的行数

        Raises:
            ValueError: 当表名为空或数据列表和条件列表长度不一致时抛出
            Exception: 当更新操作失败时抛出

        Example:
            >>> db = SyncAioMySQL('localhost', 3306, 'user', 'password', 'dbname', tablename='users')
            >>> # 更新单条数据
            >>> result = db.update({'username': '李四', 'status': 1}, {'id': 1})
            >>> # 更新多条数据
            >>> update_data = [{'username': '李四'}, {'username': '王五'}]
            >>> conditions = [{'id': 1}, {'id': 2}]
            >>> results = db.update(update_data, conditions)
            >>> # 复杂条件更新
            >>> result = db.update({'status': 0}, {'is_active': False, 'created_at__lt': '2023-01-01'})
        """
        tablename = tablename or self.tablename

        if not tablename:
            raise ValueError('表名不能为空，请在参数中指定或在实例化时设置')

        if isinstance(data_list, dict):
            data_list = [data_list]
            where_list = [where_list] if isinstance(where_list, dict) else where_list

        if len(data_list) != len(where_list):
            raise ValueError('数据列表和条件列表长度必须一致')

        # 生成参数化SQL和参数列表
        sql_params_list = [make_update_sql(data_dict, where_dict, tablename) for data_dict, where_dict in zip(data_list, where_list, strict=False)]
        coro = [self._execute(sql, *params) for sql, params in sql_params_list]
        return self.run_until_loop(coro)


# 快捷函数 - 提供更简便的数据库操作方式
def create_async_mysql(db_key: str = 'default', tablename: str | None = None, autocommit: bool = True, **kwargs) -> SyncAioMySQL:
    """创建异步MySQL连接实例的快捷函数

    Args:
        db_key: 数据库配置键名，用于从DB_CFG中获取对应的数据库配置，默认为'default'
        tablename: 默认表名，可选，用于指定默认操作的表

    Returns:
        SyncAioMySQL: 异步MySQL实例，已完成连接池初始化

    Raises:
        ValueError:
            - 当db_key参数不是字符串类型时抛出
            - 当DB_CFG中不存在指定的配置键时抛出

    Example:
        >>> # 创建默认数据库连接
        >>> db = create_async_mysql()
        >>> # 创建指定配置的数据库连接
        >>> db = create_async_mysql('test_db')
        >>> # 创建指定表名的数据库连接
        >>> db = create_async_mysql('test_db', 'users')

    Notes:
        1. 使用DB_CFG中的配置创建连接池，避免硬编码数据库连接信息
        2. 创建过程中自动初始化连接池，可直接用于数据库操作
        3. 配置文件应包含host、port、user、password、db等必要信息
    """
    # 参数类型验证
    if not isinstance(db_key, str):
        raise ValueError(f'配置键非字符串类型: [{type(db_key).__name__}]')

    # 配置键存在性检查
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f'DB_CFG数据库配置中 [{db_key}] 不存在')

    # 获取配置并创建连接池
    cfg = DB_CFG[db_key].value.copy()
    cfg.pop('type', None)  # 移除类型字段(如果存在)

    logger.start(f'正在创建连接池实例，配置键: {db_key}')

    return SyncAioMySQL(**cfg, autocommit=autocommit, tablename=tablename, **kwargs)


if __name__ == '__main__':
    # 测试代码 - 完整的数据库操作测试

    def run_test():
        """
        运行完整的数据库测试用例，验证SyncAioMySQL类的各项功能

        测试流程:
        1. 初始化数据库连接
        2. 测试查询操作（格式化结果和原始结果）
        3. 准备测试数据
        4. 测试插入操作
        5. 查询插入的数据进行验证
        6. 测试更新操作
        7. 验证更新结果
        8. 清理测试数据（可选）

        Notes:
            1. 本测试函数仅供开发和调试使用，实际运行需要有效的数据库配置
            2. 默认使用'TXbx'配置和'users2'表进行测试
            3. 测试过程中会创建实际数据，请在测试环境中运行
        """
        aio = None
        try:
            # 1. 初始化数据库连接
            aio = create_async_mysql('TXbx', 'users2')

            # 2. 测试查询操作 - 使用格式化结果
            logger.start('测试查询操作（格式化结果）...')
            query_sql = 'SELECT * FROM users2 LIMIT 5'
            results = aio.query(query_sql)  # 默认返回格式化后的字典列表
            logger.ok(f'查询结果数量: {len(results)}')
            if results:
                logger.ok(f'第一条记录（格式化后）: {results[0]}')
                # 可以直接通过列名访问数据
                if isinstance(results[0], dict):
                    logger.ok(f'格式化结果示例: ID={results[0].get("ID")}, username={results[0].get("username")}')

            # 测试查询操作 - 使用原始结果
            logger.start('测试查询操作（原始结果）...')
            raw_results = aio.query(query_sql, return_dict=False)
            if raw_results:
                logger.info(f'第一条原始记录: {raw_results[0]}')

            # 3. 准备测试数据
            test_item = {
                'username': '测试用户',
                'password': 'test123',
                '手机': '13800138000',
                '代理人编码': '10000012',
                '会员级别': 'A',
                '会员到期日': '2025-12-31 00:00:00',
            }

            # 4. 测试插入操作
            logger.start('测试插入操作...')
            insert_result = aio.insert(test_item)
            logger.ok(f'插入结果: {insert_result}')

            # 5. 查询插入的数据 - 使用格式化结果
            logger.start('查询刚插入的数据（格式化结果）...')
            new_data = aio.query("SELECT * FROM users2 WHERE `代理人编码`='10000012' LIMIT 1")
            logger.info(f'查询结果: {new_data}')

            inserted_id = None
            if new_data and isinstance(new_data, list) and len(new_data) > 0 and isinstance(new_data[0], dict):
                inserted_id = new_data[0].get('ID')
                logger.info(f'提取的ID: {inserted_id}, 类型: {type(inserted_id)}')

            if inserted_id:
                logger.info(f'获取到插入ID: {inserted_id}')

                try:
                    # 6. 测试更新操作
                    logger.start('测试更新操作...')
                    update_data = {'username': '更新用户', '会员级别': 'B'}
                    update_condition = {'ID': inserted_id}
                    update_result = aio.update(update_data, update_condition)
                    logger.ok(f'更新结果: {update_result}')

                    # 7. 验证更新结果
                    logger.start('验证更新结果...')
                    # 使用参数化查询避免SQL注入
                    updated_data = aio.query('SELECT * FROM users2 WHERE ID=%s', inserted_id)
                    if updated_data and isinstance(updated_data, list) and len(updated_data) > 0 and isinstance(updated_data[0], dict):
                        logger.info(f'更新后的数据: {updated_data[0]}')
                        logger.info(f'用户名已更新为: {updated_data[0].get("username")}, 会员级别已更新为: {updated_data[0].get("会员级别")}')
                except Exception as e:
                    logger.fail(f'处理更新操作时发生错误: {e}')
            else:
                logger.warning('未能获取到插入数据的ID')

            # 8. 清理测试数据
            logger.start('清理测试数据...')
            # 注意：在实际环境中请谨慎使用DELETE语句
            cleanup_sql = 'DELETE FROM users2 WHERE ID=%s'
            cleanup_result = aio.execute(cleanup_sql, inserted_id)
            logger.info(f'清理结果: {cleanup_result}')
        except Exception as e:
            logger.fail(f'测试过程中发生错误: {e}')
            import traceback

            traceback.print_exc()

        logger.ok('测试完成')

    run_test()
