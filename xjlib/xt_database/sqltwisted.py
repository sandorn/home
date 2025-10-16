# !/usr/bin/env python3
"""
==============================================================
Description  : Twisted异步数据库操作模块 - 提供基于Twisted框架的异步MySQL数据库操作功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-21 00:08:37
LastEditTime : 2024-09-05 16:43:28
FilePath     : /CODE/xjLib/xt_database/sqltwisted.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- SqlTwisted类:基于Twisted框架的异步MySQL数据库操作类
- 支持异步执行SQL查询、插入和更新操作
- 集成了结果回调和错误处理机制

主要特性:
- 基于Twisted的adbapi实现异步数据库操作
- 自动管理数据库连接池
- 支持自定义表名和数据库配置
- 提供统一的结果回调和错误处理
==============================================================
"""

from __future__ import annotations

from typing import Any

from twisted.enterprise import adbapi
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from xt_database.cfg import DB_CFG
from xt_wraps.log import LogCls

log = LogCls()


class SqlTwisted:
    """SqlTwisted - 基于Twisted框架的异步MySQL数据库操作类

    提供异步执行SQL查询、插入和更新操作的功能，自动管理数据库连接池
    并集成了结果回调和错误处理机制。

    Args:
        db_key: 数据库配置键名（类型：str，默认值：'default'）
        tablename: 默认数据表名（类型：str | None，默认值：None）

    Attributes:
        tablename: 默认数据表名
        dbpool: Twisted数据库连接池对象
        log: 日志实例

    Raises:
        ValueError: 当指定的数据库配置不存在时抛出

    Example:
        >>> # 创建数据库操作实例
        >>> db = SqlTwisted('TXbx', 'users2')
        >>> # 执行查询
        >>> db.perform_query('SELECT * FROM users2 LIMIT 10')
        >>> # 启动事件循环
        >>> reactor.run()
    """

    def __init__(self, host: str, port: int, user: str, password: str, db: str, charset: str = 'utf8mb4', autocommit: bool = True, tablename: str | None = None, **kwargs) -> None:
        """初始化SqlTwisted实例，创建数据库连接池

        Args:
            host: 数据库主机地址
            port: 数据库端口号
            user: 数据库用户名
            password: 数据库密码
            db: 数据库名称
            charset: 数据库字符集，默认为'utf8mb4'
            autocommit: 是否自动提交事务，默认为True
            tablename: 默认操作的表名
            **kwargs: 其他aiomysql.create_engine支持的参数

        Raises:
            ValueError: 当指定的数据库配置不存在时抛出
        """
        self.log = log
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
                raise ValueError(f'❌ 缺少必要的数据库连接参数: {name}')

        # 设置直接参数
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
        # 创建数据库连接池配置
        try:
            # 创建连接池
            self.dbpool = adbapi.ConnectionPool('pymysql', **self.cfg)  # MySQLdb | pymysql
            reactor.callWhenRunning(self.close)  # 注册关闭回调
        except Exception as err:
            self.log.error(f'❌ 创建数据库引擎失败: {err}')
            raise Exception(f'❌ create_engine error:{err}') from err

    def close(self) -> None:
        """关闭数据库连接池并停止reactor事件循环

        在reactor启动时自动注册，当事件循环结束时调用
        """
        try:
            self.dbpool.close()
            self.log.info('数据库连接池已关闭')
        except Exception as e:
            self.log.error(f'关闭数据库连接池失败: {e!s}')
        finally:
            reactor.stop()  # 终止reactor

    def perform_query(self, query: str) -> Deferred[list[dict[str, Any]]]:
        """异步执行SQL查询语句

        Args:
            query: SQL查询语句

        Returns:
            Deferred[List[Dict[str, Any]]]: 返回包含查询结果的Deferred对象
        """

        # 添加内部回调，但确保结果能够继续传递
        def internal_success(results):
            """内部成功回调，记录日志并返回结果"""
            self.log.info(f'【perform_query 查询成功】: 共{len(results)}条记录')
            return results

        def internal_failure(error):
            """内部失败回调，记录日志并传递错误"""
            self.log.error(f'【perform_query 查询失败】: {error!s}')
            return error

        self.log.info(f'开始执行SQL查询: {query}')
        try:
            defer = self.dbpool.runQuery(query)
            # 确保回调收到的结果不为None
            defer.addCallback(lambda results: results or [])
            defer.addCallbacks(internal_success, internal_failure)
            return defer
        except Exception as e:
            self.log.error(f'执行查询失败: {e!s}')
            raise

    def query(self, sql: str) -> Deferred[list[dict[str, Any]]]:
        """异步执行SQL查询并处理结果

        Args:
            sql: SQL查询语句

        Returns:
            Deferred[List[Dict[str, Any]]]: 返回包含查询结果的Deferred对象
        """
        self.log.info(f'开始执行SQL查询操作: {sql}')
        try:
            defer = self.dbpool.runInteraction(self._query, sql)
            defer.addBoth(self.handle_back, sql, 'query')
            return defer
        except Exception as e:
            self.log.error(f'执行查询操作失败: {e!s}')
            raise

    def insert(self, item: dict[str, Any], tablename: str | None = None) -> Deferred[int]:
        """异步插入数据到指定表

        Args:
            item: 要插入的数据字典
            tablename: 目标数据表名（可选，默认使用实例初始化时的表名）

        Returns:
            Deferred[int]: 返回包含受影响行数的Deferred对象
        """
        tablename = tablename or self.tablename
        self.log.info(f'开始执行数据插入操作，表名:{tablename}，数据项数:{len(item)}')
        try:
            defer = self.dbpool.runInteraction(self._insert, item, tablename)
            defer.addBoth(self.handle_back, item, 'insert')
            return defer
        except Exception as e:
            self.log.error(f'执行插入操作失败: {e!s}')
            raise

    def update(self, item: dict[str, Any], condition: dict[str, Any], tablename: str | None = None) -> Deferred[int]:
        """异步更新指定表中的数据

        Args:
            item: 要更新的数据字典
            condition: 更新条件字典
            tablename: 目标数据表名（可选，默认使用实例初始化时的表名）

        Returns:
            Deferred[int]: 返回包含受影响行数的Deferred对象
        """
        tablename = tablename or self.tablename
        self.log.info(f'开始执行数据更新操作，表名:{tablename}，条件:{condition}')
        try:
            defer = self.dbpool.runInteraction(self._update, item, condition, tablename)
            defer.addBoth(self.handle_back, item, 'update')
            return defer
        except Exception as e:
            self.log.error(f'执行更新操作失败: {e!s}')
            raise

    def handle_back(self, result: Any, item: str | dict[str, Any], *args: Any) -> Any:
        """统一处理异步操作的回调结果

        Args:
            result: 操作结果
            item: 原始操作的参数（SQL语句或数据字典）
            *args: 附加参数，通常包含操作类型

        Returns:
            Any: 原始操作结果
        """
        operation = args[0] if args else 'unknown'
        self.log.info(f'【SqlTwisted异步回调 [{operation}] 】: 操作完成')
        return result

    def _query(self, cursor: Any, sql: str) -> list[dict[str, Any]]:
        """执行SQL查询的内部方法

        Args:
            cursor: 数据库游标对象
            sql: SQL查询语句

        Returns:
            List[Dict[str, Any]]: 查询结果集
        """
        try:
            self.log.debug(f'执行SQL查询语句: {sql}')
            # 直接执行查询，不再转换SQL语句类型
            cursor.execute(sql)  # self.dbpool 自带cursor
            results = cursor.fetchall()
            return results or []  # 确保返回空列表而不是None
        except Exception as e:
            self.log.error(f'执行查询操作异常: {e!s}')
            return []

    def _insert(self, cursor: Any, item: dict[str, Any], tablename: str) -> int:
        """执行数据插入的内部方法

        Args:
            cursor: 数据库游标对象
            item: 要插入的数据字典
            tablename: 目标数据表名

        Returns:
            int: 影响的行数
        """
        try:
            # 修改SQL执行方式，避免SQL语句类型问题
            columns = ', '.join(item.keys())
            values = ', '.join([f'%({k})s' for k in item])
            sql = f'INSERT INTO {tablename} ({columns}) VALUES ({values})'
            self.log.debug(f'执行SQL插入语句: {sql}')
            # 使用参数化查询，避免类型问题
            return cursor.execute(sql, item)
        except Exception as e:
            self.log.error(f'执行插入操作异常: {e!s}')
            raise

    def _update(self, cursor: Any, item: dict[str, Any], condition: dict[str, Any], tablename: str) -> int:
        """执行数据更新的内部方法

        Args:
            cursor: 数据库游标对象
            item: 要更新的数据字典
            condition: 更新条件字典
            tablename: 目标数据表名

        Returns:
            int: 影响的行数
        """
        try:
            # 修改SQL执行方式，避免SQL语句类型问题
            set_clause = ', '.join([f'{k} = %({k})s' for k in item])
            where_clause = ' AND '.join([f'{k} = %({k}_cond)s' for k in condition])

            # 合并参数
            params = item.copy()
            for k, v in condition.items():
                params[f'{k}_cond'] = v

            sql = f'UPDATE {tablename} SET {set_clause} WHERE {where_clause}'
            self.log.debug(f'执行SQL更新语句: {sql}')
            # 使用参数化查询，避免类型问题
            return cursor.execute(sql, params)
        except Exception as e:
            self.log.error(f'执行更新操作异常: {e!s}')
            raise


def create_sqltwisted(db_key: str = 'default', tablename: str | None = None, **kwargs) -> SqlTwisted:
    """创建SqlTwisted实例的快捷工厂函数

    提供一种更便捷的方式创建SqlTwisted实例，自动处理数据库配置参数

    Args:
        db_key: 数据库配置键名，对应DB_CFG中的配置项，默认为'default'
        tablename: 默认操作的表名，可选

    Returns:
        SqlTwisted: 配置好的SqlTwisted实例

    Raises:
        ValueError:
            - 当db_key参数不是字符串类型时抛出
            - 当DB_CFG中不存在指定的配置键时抛出

    Example:
        >>> # 创建默认数据库连接
        >>> db = create_sqltwisted()
        >>> # 创建指定配置的数据库连接
        >>> db = create_sqltwisted('TXbx')
        >>> # 创建指定表名的数据库连接
        >>> db = create_sqltwisted('TXbx', 'users2')

    Notes:
        1. 使用DB_CFG中的配置创建连接池，避免硬编码数据库连接信息
        2. 创建过程中自动初始化连接池，可直接用于数据库操作
        3. 配置文件应包含host、port、user、password、db等必要信息
    """
    # 参数类型验证
    if not isinstance(db_key, str):
        raise ValueError(f'❌ 配置键非字符串类型: [{type(db_key).__name__}]')

    # 配置键存在性检查
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f'❌ DB_CFG数据库配置中 [{db_key}] 不存在')

    # 获取配置并创建连接池
    cfg = DB_CFG[db_key].value.copy()
    cfg.pop('type', None)  # 移除类型字段(如果存在)

    log.info(f'▶️ 正在创建SqlTwisted实例，配置键: {db_key}')

    # 创建并返回SqlTwisted实例
    return SqlTwisted(**cfg, tablename=tablename, **kwargs)


def run_tests() -> None:
    """运行SqlTwisted的测试用例

    测试用例按照以下顺序执行:
    1. 查询用户表数据
    2. 插入新用户记录
    3. 更新现有用户记录
    4. 再次查询验证操作结果
    """
    try:
        # 创建数据库操作实例
        log = LogCls()
        log.info('开始运行SqlTwisted测试用例')

        # 创建数据库操作实例 - 使用新的工厂函数
        SQ = create_sqltwisted('TXbx', 'users2')  # noqa: N806
        log.info('成功创建SqlTwisted实例，默认表名为: users2')

        # 准备测试数据
        test_user_id = 2  # 测试用的用户ID，避免影响实际数据
        update_item = {'username': '测试用户_已更新'}
        insert_item = {
            'username': '测试用户_新增',
            'password': 'test123456',
            '手机': '13800138000',
            '代理人编码': '10009999',
            '会员级别': 'A',
            '会员到期日': '2025-12-31 00:00:00',
        }

        # 测试查询功能
        def test_query() -> Deferred[list[dict[str, Any]]]:
            """测试查询功能并返回查询结果"""
            log.info('=== 开始测试查询功能 ===')
            sql = 'select * from users2 LIMIT 5'
            # 处理查询结果
            d = SQ.perform_query(sql)
            d.addCallback(lambda results: (log.info(f'查询返回结果: {len(results or [])}条记录，结果: {results or []}'), results)[1])

            # 使用另一种查询方法
            detail_sql = 'select * from users2 where ID = 3'
            d2 = SQ.query(detail_sql)
            d2.addCallback(lambda results: log.info(f'详细查询返回结果: {results or []}'))
            log.info('查询功能测试完成')
            return d  # 返回主要查询的Deferred对象

        # 测试插入功能
        def test_insert() -> None:
            """测试插入功能"""
            log.info('=== 开始测试插入功能 ===')
            try:
                d = SQ.insert(insert_item, 'users2')
                d.addCallback(lambda affected_rows: log.info(f'成功执行插入操作，影响行数: {affected_rows}，用户ID: {test_user_id}'))
                d.addErrback(lambda failure: log.warning(f'用户ID {test_user_id} 已存在，跳过插入操作') if 'Duplicate entry' in str(failure.value) else failure.raiseException())
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    log.warning(f'用户ID {test_user_id} 已存在，跳过插入操作')
                else:
                    raise

        # 测试更新功能
        def test_update() -> None:
            """测试更新功能"""
            log.info('=== 开始测试更新功能 ===')
            d = SQ.update(update_item, {'ID': test_user_id})
            d.addCallback(lambda affected_rows: log.info(f'成功执行更新操作，影响行数: {affected_rows}，用户ID: {test_user_id}'))
            d.addErrback(lambda failure: log.error(f'更新操作失败: {failure.value!s}'))

        # 测试组合操作
        def test_combination() -> None:
            """测试组合操作"""
            log.info('=== 开始测试组合操作 ===')

            # 先查询
            query_sql = f'select * from users2 where ID = {test_user_id}'

            def after_initial_query(results):
                log.info(f'初始查询结果: {results or []}')
                # 然后更新
                update_item2 = {'password': 'updated_password'}
                d = SQ.update(update_item2, {'ID': test_user_id})
                d.addCallback(lambda affected_rows: {'affected_rows': affected_rows, 'query_sql': query_sql})
                return d

            def after_update(result_dict):
                log.info(f'更新操作影响行数: {result_dict["affected_rows"]}')
                # 最后再次查询验证更新结果
                d = SQ.perform_query(result_dict['query_sql'])
                d.addCallback(lambda results: log.info(f'更新后查询结果: {results}'))
                return d

            # 链式调用
            d = SQ.perform_query(query_sql)
            d.addCallback(after_initial_query)
            d.addCallback(after_update)
            d.addErrback(lambda failure: log.error(f'组合操作失败: {failure.value!s}'))

            log.info('组合操作测试完成')

        # 按顺序执行测试
        query_deferred = test_query()  # 存储查询返回的Deferred对象
        # test_insert()
        # test_update()
        # test_combination()

        log.info('所有测试用例已提交执行，请查看日志获取详细结果')

        # query_deferred对象可以被外部使用，以获取查询结果
        # 示例1: 添加回调函数处理查询结果
        def process_query_results(results):
            """处理查询结果的示例函数"""
            log.info(f'[外部处理] 查询到{len(results)}条记录')
            # 在这里可以对结果进行任何处理，如数据转换、过滤等
            # 返回处理后的结果，可以继续链式调用
            return results

        # 添加回调函数到Deferred对象
        query_deferred.addCallback(process_query_results)

        # 示例2: 错误处理
        def handle_query_error(failure):
            """处理查询错误的示例函数"""
            log.error(f'[外部处理] 查询发生错误: {failure.value!s}')
            # 返回None或其他默认值，防止后续回调失败
            return []  # 返回空列表作为默认值

        # 添加错误处理回调
        query_deferred.addErrback(handle_query_error)

        # 示例3: 结果转换
        def transform_results(results):
            """转换查询结果格式的示例函数"""
            # 例如：将结果转换为字典列表格式
            transformed = []
            for row in results:
                # 假设每行数据的字段顺序是固定的
                if row and len(row) >= 6:
                    transformed.append({'id': row[0], 'username': row[1], 'phone': row[3], 'level': row[5]})
            log.info(f'[外部处理] 转换后的结果: {transformed}')
            return transformed

        # 链式添加结果转换回调
        query_deferred.addCallback(transform_results)

        # 启动事件循环
        reactor.run()

    except Exception as e:
        log = LogCls()
        log.error(f'测试执行失败: {e!s}')
        import traceback

        log.error(f'详细错误信息: {traceback.format_exc()}')


if __name__ == '__main__':
    """主程序入口，运行SqlTwisted测试用例"""
    run_tests()
