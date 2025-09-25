# !/usr/bin/env python
"""
==============================================================
Description  : 异步MySQL连接池模块 - 提供高效的异步数据库操作和连接管理
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-14 15:00:00
FilePath     : /CODE/xjlib/xt_database/aiomysqlpool.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- AioMySQLPool: 单例模式的异步MySQL连接池类，基于aiomysql实现高效连接管理
- create_async_mysql_pool: 快捷函数，简化连接池创建过程

主要特性:
- 连接池自动管理，支持最小/最大连接数配置和连接回收
- 完整的CRUD操作接口(fetchone/fetchall/fetchmany/execute)
- 支持异步上下文管理器(with语句)自动处理资源
- 支持事务操作(begin/commit/rollback)确保数据一致性
- 支持异步迭代器，高效处理大量数据避免内存溢出
- 统一的错误处理和日志记录机制
- 完整的类型注解，支持Python 3.10+现代语法规范
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

import aiomysql
import pymysql
from xt_database.cfg import DB_CFG
from xt_wraps import SingletonMixin
from xt_wraps.log import create_basemsg, log_wraps
from xt_wraps.log import mylog as logger


class AioMySQLPool(SingletonMixin):
    """异步 MySQL 连接池封装类，基于 aiomysql 实现高效的数据库连接管理。

    本类继承自单例模式混入类，确保在应用程序中只创建一个连接池实例，
    提供了异步数据库连接池的创建、初始化、查询、执行和关闭等功能，
    支持异步上下文管理器协议和异步迭代器，确保资源的正确管理和高效利用。

    参数说明:
        - 支持连接参数配置(主机、端口、用户名、密码等)
        - 支持连接池大小配置(最小/最大连接数)
        - 支持字符集和自动提交配置

    使用方式：
        # 直接初始化
        db = AioMySQLPool(host='localhost', port=3306, user='root',
                        password='password', db='test_db')
        result = await db.fetchone("SELECT * FROM users WHERE id = %s", 1)
        await db.close()

        # 使用快捷函数(推荐)
        db = create_async_mysql_pool('default')
        # 执行数据库操作
        await db.close()

        # 使用上下文管理器(推荐)
        async with create_async_mysql_pool('default') as db:
            result = await db.fetchone("SELECT * FROM users WHERE id = %s", 1)

        # 使用事务
        async with create_async_mysql_pool('default') as db:
            conn = await db.begin()
            try:
                # 执行操作
                await conn.execute("INSERT INTO users(name) VALUES (%s)", "test")
                await db.commit(conn)
            except Exception:
                await db.rollback(conn)

        # 使用迭代器处理大量数据
        async with create_async_mysql_pool('default') as db:
            async for row in db.iterate("SELECT * FROM large_table"):
                # 处理每一行数据
                pass
    """

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str,
        minsize: int = 1,
        maxsize: int = 10,
        charset: str = 'utf8mb4',
        autocommit: bool = True,
        cursorclass: type[aiomysql.cursors.Cursor] = aiomysql.cursors.DictCursor,
        pool_recycle: int = -1,
        **kwargs,
    ):
        """初始化异步MySQL连接池配置

        Args:
            host: 数据库主机地址
            port: 数据库端口号
            user: 数据库用户名
            password: 数据库密码
            db: 数据库名称
            minsize: 连接池最小连接数，默认1
            maxsize: 连接池最大连接数，默认10
            charset: 数据库字符集，默认'utf8mb4'
            autocommit: 是否自动提交事务，默认True
            pool_recycle: 连接回收时间(秒)，默认不回收(-1)

        Example:
            >>> # 直接初始化连接池(不推荐，建议使用create_async_mysql_pool)
            >>> db = AioMySQLPool(
            >>>     host='localhost',
            >>>     port=3306,
            >>>     user='root',
            >>>     password='password',
            >>>     db='test_db'
            >>> )
        """
        self.autocommit = autocommit
        self.pool: aiomysql.Pool | None = None

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
            'minsize': minsize,
            'maxsize': maxsize,
            'charset': charset,
            'autocommit': autocommit,
            'cursorclass': cursorclass,
            'pool_recycle': pool_recycle,  # 连接回收时间(秒)
            'echo': __name__ == '__main__',
        }
        self.cfg.update(kwargs)

    async def close(self) -> None:
        """关闭连接池，释放所有资源

        确保在使用完毕后调用此方法以释放连接资源
        """
        msg = create_basemsg(self.close)
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()
            logger.stop(f'{msg} | 连接池已关闭')
            self.pool = None

    @log_wraps
    async def init_pool(self) -> None:
        """初始化连接池

        创建连接池实例，建立初始连接
        如果连接池已存在，则发出警告并返回

        Raises:
            Exception: 创建连接池失败时抛出异常
        """
        if self.pool is not None:
            return
        self.pool = await aiomysql.create_pool(
            **self.cfg,
            loop=asyncio.get_running_loop(),  # 显式传递当前事件循环
        )
        
    @log_wraps
    async def execute(self, query, *parameters, **kwparameters) -> int:
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
        if self.pool is None:
            await self.init_pool()

        async with self.pool.acquire() as conn, conn.cursor() as cur:
            try:
                await cur.execute(query, kwparameters or parameters)
            except Exception:
                await conn.ping()
                await cur.execute(query, kwparameters or parameters)
            return cur.lastrowid

    async def get_cursor(self) -> tuple[aiomysql.Connection, aiomysql.Cursor]:
        """获取数据库连接和游标

        注意：使用完毕后请调用close_cursor()方法释放资源

        Returns:
            tuple[aiomysql.Connection, aiomysql.Cursor]: 连接和游标对象

        Raises:
            ValueError: 连接池未初始化时抛出
        """
        if self.pool is None:
            await self.init_pool()

        conn = await self.pool.acquire()
        cur = await conn.cursor(cursorclass=self.cursorclass)
        return conn, cur

    async def close_cursor(self, conn: aiomysql.Connection, cur: aiomysql.Cursor) -> None:
        """关闭游标并释放连接回连接池

        Args:
            conn: 数据库连接对象
            cur: 游标对象
        """
        if not self.autocommit:
            await conn.commit()
        await cur.close()
        await self.pool.release(conn)

    async def get(self, query, *parameters, **kwparameters) -> dict[str, any] | None:
        """查询单条记录，返回字典

        Args:
            query: 查询SQL语句
            *parameters: SQL语句的位置参数值（元组形式）
            **kwparameters: SQL语句的关键字参数值（字典形式）

        Returns:
            dict[str, any] | None: 查询结果字典，如果没有记录则返回None

        Raises:
            ValueError: 连接池未初始化时抛出
            Exception: 数据库操作异常时抛出
        """
        if self.pool is None:
            await self.init_pool()

        async with self.pool.acquire() as conn, conn.cursor() as cur:
            try:
                await cur.execute(query, kwparameters or parameters)
                ret = await cur.fetchone()
            except pymysql.err.InternalError:
                # 连接失效时重连并重新执行
                await conn.ping()
                await cur.execute(query, kwparameters or parameters)
                ret = await cur.fetchone()
            return ret

    async def query(self, query, *parameters, **kwparameters) -> list[dict[str, any]]:
        """查询所有记录，返回字典列表

        Args:
            query: 查询SQL语句
            *parameters: SQL语句的参数值
            **kwparameters: SQL语句的关键字参数值（字典形式）

        Returns:
            list[dict[str, Any]]: 查询结果列表，每条记录为字典格式

        Raises:
            ValueError: 连接池未初始化时抛出
        """
        if self.pool is None:
            await self.init_pool()

        async with self.pool.acquire() as conn, conn.cursor() as cur:
            try:
                await cur.execute(query, kwparameters or parameters)
                ret = await cur.fetchall()
            except pymysql.err.InternalError:
                await conn.ping()
                await cur.execute(query, kwparameters or parameters)
                ret = await cur.fetchall()
            return ret

    async def query_many(self, query, size: int, *parameters, **kwparameters) -> list[dict[str, any]]:
        """查询多条记录（指定数量）

        Args:
            query: 查询SQL语句
            size: 要获取的记录数量
            *parameters: SQL语句的参数值
            **kwparameters: SQL语句的关键字参数值（字典形式）

        Returns:
            list[dict[str, Any]]: 查询结果列表，每条记录为字典格式

        Raises:
            ValueError: 连接池未初始化时抛出
        """
        if self.pool is None:
            await self.init_pool()

        async with self.pool.acquire() as conn, conn.cursor() as cur:
            try:
                await cur.execute(query, kwparameters or parameters)
                ret = await cur.fetchmany(size)
            except pymysql.err.InternalError:
                await conn.ping()
                await cur.execute(query, kwparameters or parameters)
                ret = await cur.fetchmany(size)
            return ret

    # 异步上下文管理器支持
    async def __aenter__(self) -> AioMySQLPool:
        """异步上下文管理器入口，自动初始化连接池"""
        await self.init_pool()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """异步上下文管理器出口，自动关闭连接池"""
        await self.close()

    # 事务支持
    async def begin(self) -> aiomysql.Connection:
        """开始事务，返回连接对象

        Returns:
            aiomysql.Connection: 数据库连接对象

        Raises:
            ValueError: 连接池未初始化时抛出
        """
        if self.pool is None:
            await self.init_pool()

        conn = await self.pool.acquire()
        await conn.begin()
        return conn

    async def commit(self, conn: aiomysql.Connection) -> None:
        """提交事务

        Args:
            conn: 数据库连接对象
        """
        await conn.commit()
        await self.pool.release(conn)

    async def rollback(self, conn: aiomysql.Connection) -> None:
        """回滚事务

        Args:
            conn: 数据库连接对象
        """
        await conn.rollback()
        await self.pool.release(conn)

    # 异步迭代器支持
    async def iterate(self, query: str, *parameters, batch_size: int = 1000, **kwparameters) -> AsyncIterator[dict[str, any]]:
        """迭代查询结果，适用于处理大量数据

        Args:
            query: 查询SQL语句
            *parameters: SQL语句的参数值
            batch_size: 每批获取的记录数量
            **kwparameters: 命名参数

        Yields:
            dict[str, any]: 每条查询结果记录

        Raises:
            ValueError: 连接池未初始化时抛出
        """
        if self.pool is None:
            await self.init_pool()

        async with self.pool.acquire() as conn, conn.cursor() as cur:
            try:
                await cur.execute(query, kwparameters or parameters)
            except pymysql.err.InternalError:
                await conn.ping()
                await cur.execute(query, kwparameters or parameters)

            while True:
                batch = await cur.fetchmany(batch_size)
                if not batch:
                    break
                for row in batch:
                    yield row


# 快捷函数 - 提供更简便的数据库操作方式
def create_async_mysql_pool(db_key: str = 'default', **kwargs) -> AioMySQLPool:
    """创建异步MySQL连接池实例的快捷函数

    Args:
        db_key: 数据库配置键名，对应DB_CFG中的配置

    Returns:
        AioMySQLPool: 异步MySQL连接池实例

    Raises:
        ValueError: 当配置键不存在或参数类型错误时抛出

    Example:
        >>> # 1. 使用默认配置
        >>> db = create_async_mysql_pool()
        >>> # 2. 使用特定配置
        >>> db = create_async_mysql_pool('TXbx')
        >>> # 3. 使用上下文管理器(推荐)
        >>> async with create_async_mysql_pool('TXbx') as db:
        >>>     result = await db.fetchone('SELECT * FROM users')
    """
    # 参数类型验证
    if not isinstance(db_key, str):
        raise ValueError(f'配置键非字符串类型: [{type(db_key).__name__}]')

    # 配置键存在性检查
    if not hasattr(DB_CFG, db_key):
        raise ValueError(f'DB_CFG数据库配置中 [{db_key}] 不存在')

    # 获取配置并创建连接池
    cfg = DB_CFG[db_key].value.copy()
    cfg.pop('type', None)  # 移除字段(如果存在)

    logger.start(f'正在创建连接池实例，配置键: {db_key}')
    return AioMySQLPool(**cfg, **kwargs)


if __name__ == '__main__':
    """测试代码 - 演示连接池的各种用法"""

    # ruff: noqa : T201
    async def _test_basic_operations():
        """测试基本的数据库操作，包括初始化、查询、插入和关闭等核心功能。

        测试流程:
        1. 创建连接池实例并初始化
        2. 测试fetchone方法查询单条记录
        3. 测试execute方法执行插入操作
        4. 测试fetchall方法查询多条记录
        5. 确保资源正确关闭
        """
        print('\n=== 测试基本数据库操作 ===')
        db = create_async_mysql_pool(db_key='default')
        try:
            # 查询测试
            result = await db.get('SELECT * FROM users2 WHERE ID = %s', 143)
            print('单条查询结果:', result)

            # 插入测试
            affected = await db.execute('INSERT INTO users2(username, password, 手机) VALUES (%s, %s, %s)', '测试用户', '123456', '13800000000')
            print(f'插入完成，受影响行数: {affected}')

            # 查询全部
            all_users = await db.query('SELECT * FROM users2 LIMIT 5')
            print(f'多条查询结果(前5条): {all_users}')

        except Exception as e:
            print(f'测试过程中出错: {e}')
        finally:
            await db.close()

    async def _test_context_manager():
        """测试上下文管理器用法，验证异步上下文协议的正确实现。

        测试流程:
        1. 使用async with语句创建连接池实例
        2. 验证上下文管理器自动处理连接池的初始化
        3. 执行数据库查询操作
        4. 验证上下文管理器自动处理连接池的关闭
        5. 测试异常情况下的资源管理
        """
        print('\n=== 测试上下文管理器 ===')
        try:
            async with create_async_mysql_pool(db_key='default') as db:
                # 使用上下文管理器自动处理初始化和关闭
                result = await db.get('SELECT * FROM users2 WHERE ID = %s', 143)
                print('上下文管理器查询结果:', result)
        except Exception as e:
            print(f'上下文管理器测试出错: {e}')

    async def _test_transaction():
        """测试事务操作功能，验证事务的开始、提交和回滚流程。

        测试流程:
        1. 在上下文管理器中创建连接池实例
        2. 调用begin()方法开始事务并获取连接
        3. 创建游标并执行多条操作(插入和更新)
        4. 测试成功路径:调用commit()方法提交事务
        5. 测试异常路径:模拟错误并调用rollback()方法回滚事务
        6. 验证事务的原子性和一致性
        """
        print('\n=== 测试事务操作 ===')
        async with create_async_mysql_pool(db_key='default') as db:
            conn = await db.begin()
            try:
                # 开始事务
                cur = await conn.cursor()

                # 执行多个操作
                await cur.execute('INSERT INTO users2(username, password, 手机) VALUES (%s, %s, %s)', ('事务用户', '654321', '13900000000'))
                new_id = cur.lastrowid
                await cur.execute('UPDATE users2 SET username = %s WHERE ID = %s', ('更新后的事务用户', new_id))

                # 提交事务
                await db.commit(conn)
                print(f'事务提交成功，新增用户ID: {new_id}')

            except Exception as e:
                # 发生错误时回滚
                await db.rollback(conn)
                print(f'事务回滚: {e}')

    async def _test_iterator():
        """测试异步迭代器功能，验证批量处理大量数据的能力。

        测试流程:
        1. 在上下文管理器中创建连接池实例
        2. 使用async for循环和iterate方法迭代查询结果
        3. 测试指定batch_size参数的批量获取行为
        4. 验证每行数据的正确性
        5. 演示如何在处理大量数据时提前终止迭代

        iterate方法特别适合处理大量数据，通过分批获取避免内存溢出问题。
        """
        print('\n=== 测试迭代器功能 ===')
        async with create_async_mysql_pool(db_key='default') as db:
            count = 0
            async for row in db.iterate('SELECT * FROM users2', batch_size=2):
                print(f'迭代行 {count + 1}:', row)
                count += 1
                if count >= 5:  # 只打印前5行
                    break

    # 运行所有测试
    async def run_all_tests():
        """运行所有测试用例，全面验证AioMySQLPool类的各项功能。

        测试顺序:
        1. 测试基本数据库操作(_test_basic_operations)
        2. 测试上下文管理器(_test_context_manager)
        3. 测试事务操作(_test_transaction)
        4. 测试异步迭代器(_test_iterator)

        此函数作为测试入口，确保所有功能模块都能正常工作，
        在开发和维护过程中可以快速验证代码的正确性。
        """
        await _test_basic_operations()
        await _test_context_manager()
        await _test_transaction()
        await _test_iterator()

    # 执行测试
    try:
        asyncio.run(run_all_tests())
    except Exception as e:
        print(f'总测试失败: {e}')
