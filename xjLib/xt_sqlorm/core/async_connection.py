# !/usr/bin/env python3
"""
==============================================================
Description  : 异步SQL数据库连接管理模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-23 10:00:00
LastEditTime : 2025-09-23 11:00:00
FilePath     : /CODE/xjlib/xt_sqlorm/core/async_connection.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- AsyncSqlConnection: 异步SQL数据库连接管理类
- 异步数据库连接池配置和管理
- 异步事务处理和会话管理
==============================================================
"""

from __future__ import annotations

import asyncio
import contextlib
from typing import TYPE_CHECKING, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine
from xt_database.cfg import connect_str
from xt_wraps.exception import exc_wraps, handle_exception
from xt_wraps.log import log_wraps
from xt_wraps.log import mylog as loger
from xt_wraps.singleton import SingletonMeta

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncResult


class AsyncSqlConnection(metaclass=SingletonMeta):
    """异步SQL数据库连接管理类

    提供异步数据库连接、会话管理、事务处理等功能
    支持多种数据库类型和连接参数配置

    特性:
    - 单例模式设计
    - 异步上下文管理器支持
    - 连接池管理
    - 异步事务自动提交和回滚
    """
    @exc_wraps
    def __init__(
        self,
        db_key: str = 'default',
        url: str | None = None,
        **kwargs: Any,
    ) -> None:
        """初始化异步数据库连接

        Args:
            db_key: 数据库配置键，用于从配置文件中获取连接信息，默认为'default'
            url: 数据库连接URL，格式为 "dialect+driver://username:password@host:port/database"
            **kwargs: 其他参数
        """
        if not url:
            url = connect_str(key=db_key, odbc='aiomysql')

        engine_config, session_config, remaining_kwargs = self._extract_engine_config(kwargs)
        self._engine: AsyncEngine = create_async_engine(url=url, **engine_config, **remaining_kwargs)
        self.async_session_factory = async_sessionmaker(bind=self._engine, **session_config)

        # 线程安全的会话对象,手动管理生命周期:self._scoped_session.remove()
        self._scoped_session_factory = async_scoped_session(self.async_session_factory, scopefunc=asyncio.current_task)

        # 不主动创建事件循环，让调用方管理
        self._loop = None  # 延迟初始化
        self._session: AsyncSession | None = None

        if self.ping():
            loger.ok(f'AsyncSqlConnection@__init__ | 数据库连接已初始化: {self}')

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """获取事件循环（延迟初始化）"""
        if self._loop is None:
            try:
                self._loop = asyncio.get_running_loop()
            except RuntimeError:
                # 如果没有运行中的事件循环，创建新的
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
        return self._loop

    @exc_wraps
    def loop_run(self, coro_list: list[Any]) -> list[Any]:
        """
        运行协程列表直到完成

        Args:
            coro_list: 协程对象列表

        Returns:
            list[Any]: 协程执行结果列表
        """
        return self.loop.run_until_complete(asyncio.gather(*coro_list))

    def __str__(self) -> str:
        return f'AsyncSqlConnection({self.engine.url!s})'
        
    async def __aenter__(self) -> AsyncSqlConnection:
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """异步上下文管理器退出

        自动提交或回滚事务，并关闭会话
        """
        try:
            if exc_type is not None:
                await self.rollback_async()
                loger.warn(f'AsyncSqlConnection@__aexit__ | 事务回滚，异常: {exc_type.__name__}')
            else:
                await self.commit_async()
        finally:
            await self.cleanup_session_async(exc_val)

    def _extract_engine_config(self, kwargs: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        """提取引擎配置参数"""
        # 定义默认值
        engine_defaults = {
            'pool_size': 5,
            'max_overflow': 10,
            'pool_timeout': 30,
            'pool_recycle': -1,
            'pool_pre_ping': False,
            'echo': False,
            'echo_pool': False,
            'hide_parameters': False,
            'future': True,
            'connect_args': {},
            'execution_options': {},
        }

        session_defaults = {
            'autocommit': False,
            'autoflush': True,
            'expire_on_commit': True,
            'twophase': False,
            'info': None,
        }

        # 安全提取配置（处理None和类型验证）
        engine_config = {}
        session_config = {}

        for key, default in engine_defaults.items():
            value = kwargs.pop(key, default)
            if value is not None:  # 只有非None值才覆盖默认值
                engine_config[key] = value

        for key, default in session_defaults.items():
            value = kwargs.pop(key, default)
            if value is not None:
                session_config[key] = value

        # 记录未使用的参数
        if kwargs:
            loger.warning(f'AsyncSqlConnection | 以下参数未被识别: {list(kwargs.keys())}')

        return engine_config, session_config, kwargs

    @property
    def pool_status(self) -> dict[str, Any]:
        """获取连接池状态信息"""
        if not hasattr(self, '_engine'):
            return {}
        
        return {
            'pool_size': self._engine.pool.size(),
            'dialect': self._engine.dialect.name,
            'checkedout': self._engine.pool.checkedout(),
            'checkedin': self._engine.pool.checkedin(),
            'overflow': self._engine.pool.overflow(),
            'timeout': self._engine.pool.timeout(),
        }
    
    @exc_wraps
    async def datainfo_async(self) -> dict[str, Any]:
        """获取数据库详细信息"""
        async with self._engine.connect() as conn:
            # 获取数据库版本等信息
            result = await conn.execute(text('SELECT version()'))
            version = result.scalar()
            
            # 获取当前连接数
            result = await conn.execute(text('SELECT COUNT(*) FROM information_schema.processlist'))
            connections = result.scalar()
            
            return {
                'version': version,
                'active_connections': connections,
                'url': str(self._engine.url),
                'pool_status': self.pool_status,
            }

    def datainfo(self) -> dict[str, Any]:
        """获取数据库详细信息"""
        return self.loop_run([self.datainfo_async()])

    @property
    def engine(self) -> AsyncEngine:
        """获取数据库引擎对象"""
        if not hasattr(self, '_engine'):
            loger.fail('AsyncSqlConnection@engine | 数据库引擎未初始化')
            raise RuntimeError('数据库引擎未初始化')
        return self._engine

    @property
    def session(self) -> AsyncSession:
        """获取当前数据库会话对象

        如果会话不存在则创建新的安全会话
        """
        if self._session is None:
            self._session = self._scoped_session_factory()
            loger.ok('AsyncSqlConnection@session | 安全会话已创建')
        return self._session

    @exc_wraps
    async def cleanup_session_async(self, exception=None):
        """异步清理当前会话,请求结束时调用"""
        if self._session is None:
            return

        await self._session.close()
        self._scoped_session_factory.remove()
        self._session = None
        if exception:
            loger.ok(f'AsyncSqlConnection@cleanup_session_async | 会话已清理，异常: {exception}')
        else:
            loger.ok('AsyncSqlConnection@cleanup_session_async | 安全会话已清理')

    def cleanup_session(self, exception=None):
        """同步清理当前会话，请求结束时调用

        Args:
            exception: 可选的异常信息
        """
        return self.loop_run([self.cleanup_session_async(exception)])

    @exc_wraps
    def new_session(self) -> AsyncSession:
        """创建新的数据库会话

        Returns:
            AsyncSession: 数据库会话对象
        """
        session = self.async_session_factory()
        loger.ok('AsyncSqlConnection@new_session | 会话已创建')
        return session

    @exc_wraps
    async def commit_async(self) -> None:
        """异步提交当前事务"""
        await self.session.commit()
        loger.ok('AsyncSqlConnection@commit_async | 事务已成功提交')

    def commit(self) -> None:
        """同步提交当前事务"""
        return self.loop_run([self.commit_async()])

    @exc_wraps
    async def rollback_async(self) -> None:
        """异步回滚当前事务"""
        await self.session.rollback()  
        loger.ok('AsyncSqlConnection@rollback_async | 事务已回滚')

    def rollback(self) -> None:
        """同步回滚当前事务"""
        return self.loop_run([self.rollback_async()])

    @log_wraps
    async def execute_sql_async(self, sql: str, params: dict[str, Any] | None = None) -> AsyncResult:
        """
        异步执行原生SQL语句

        Args:
            sql: SQL查询语句
            params: SQL参数绑定，默认为None

        Returns:
            查询结果
        """
        # 修复默认参数问题
        if params is None:
            params = {}

        async with self.engine.begin() as conn:  # 使用begin()明确事务
            return await conn.execute(text(sql), params)  # 自动提交

    def execute_sql(self, sql: str, params: dict[str, Any] | None = None) -> Any:
        """同步执行原生SQL语句

        Args:
            sql: SQL查询语句
            params: SQL参数绑定，默认为None

        Returns:
            查询结果(CursorResult对象)
            
        示例用法:
            # 获取所有结果
            result = db.execute_sql('SELECT * FROM users')
            rows = result.all()
            
            # 获取第一行结果
            row = result.first()
            
            # 获取单个值
            count = result.scalar()
            
            # 以字典形式获取所有结果
            dict_rows = result.mappings().all()
        """
        return self.loop_run([self.execute_sql_async(sql, params)])[0]

    @log_wraps(default_return=False)
    async def ping_async(self) -> bool:
        """异步测试数据库连接是否正常

        Returns:
            连接成功返回True，否则返回False
        """
        async with self._engine.connect() as conn:
            await conn.execute(text('SELECT 1'))
        return True

    def ping(self) -> bool:
        """测试数据库连接是否正常

        Returns:
            连接成功返回True，否则返回False
        """
        return self.loop_run([self.ping_async()])[0]

    @log_wraps
    @contextlib.asynccontextmanager
    async def session_scope_async(self):
        """异步事务上下文管理器

        使用示例:
            async with db.session_scope_async() as session:
                # 执行数据库操作
                session.add(some_model)
                # 自动提交，异常时自动回滚
        """
        session = self.new_session()
        try:
            loger.start('AsyncSqlConnection@session_scope_async | 事务开始')
            yield session
            await session.commit()
            loger.ok('AsyncSqlConnection@session_scope_async | 事务完成')
        except Exception as e:
            await session.rollback()
            handle_exception('AsyncSqlConnection@session_scope_async | 事务失败，已回滚', e, re_raise=True)
        finally:
            await session.close()
            loger.stop('AsyncSqlConnection@session_scope_async | 事务会话关闭')

    @log_wraps
    @contextlib.contextmanager
    def session_scope(self):
        """同步事务上下文管理器

        使用示例:
            with db.session_scope() as session:
                # 执行数据库操作
                session.add(some_model)
                # 自动提交，异常时自动回滚
        """
        session = self.new_session()
        try:
            loger.start('AsyncSqlConnection@session_scope | 事务开始')
            yield session
            self.loop_run([session.commit()])
            loger.ok('AsyncSqlConnection@session_scope | 事务完成')
        except Exception as e:
            self.loop_run([session.rollback()])
            handle_exception('AsyncSqlConnection.transaction | 事务失败，已回滚', e, re_raise=True)
        finally:
            self.loop_run([session.close()])
            loger.stop('AsyncSqlConnection@session_scope | 事务会话关闭')
    
    @log_wraps
    async def execute_many_async(self, sql: str, params_list: list[dict[str, Any]]) -> list[Any]:
        """异步批量执行SQL语句"""
        results = []
        async with self.engine.begin() as conn:
            for params in params_list:
                result = await conn.execute(text(sql), params)
                results.append(result)
        return results

    def execute_many(self, sql: str, params_list: list[dict[str, Any]]) -> list[Any]:
        """同步批量执行SQL语句"""
        return self.loop_run([self.execute_many_async(sql, params_list)])[0]

    @exc_wraps
    async def dispose_async(self) -> None:
        """异步释放数据库连接资源"""
        if not hasattr(self, '_engine'):
            loger.warn('AsyncSqlConnection@dispose_async | 数据库引擎不存在，无需释放')
            return
        try:
            await self.cleanup_session_async()
            await self.engine.dispose()
            loger.stop('AsyncSqlConnection@dispose_async | 数据库引擎已释放')
        finally:
            # 清理事件循环
            if hasattr(self, '_loop') and self._loop:
                if not self._loop.is_running():
                    self._loop.close()
                self._loop = None
            # 使用元类提供的方法重置单例实例
            type(self).reset_instance()

    def dispose(self) -> None:
        """同步释放数据库连接资源"""
        return self.loop_run([self.dispose_async()])


__all__ = ['AsyncSqlConnection']


if __name__ == '__main__':
    db_conn = AsyncSqlConnection()
    loger(db_conn.ping())

    # 测试同步执行SQL
    sql_result = db_conn.execute_sql('SELECT 1')
    loger(f'同步执行SQL测试结果: {sql_result}')
    # 展示如何提取数据
    scalar_value = sql_result.scalar()
    loger(f'从结果中提取单个值: {scalar_value}')
    
    # 执行一个返回多行数据的查询示例
    multi_result = db_conn.execute_sql('SELECT 1 AS id, 2 AS value UNION SELECT 3, 4')
    all_rows = multi_result.all()
    loger(f'提取所有行数据: {all_rows}')
    
    # 以字典形式获取结果
    dict_rows = multi_result.mappings().all()
    loger(f'以字典形式提取所有行数据: {dict_rows}')
    # 测试同步创建会话
    session = db_conn.new_session()

    # 测试同步事务上下文管理器
    with db_conn.session_scope():
        ...

    # 测试异步释放连接资源
    db_conn.dispose()

    # 测试数据库信息获取
    db_info = db_conn.datainfo()
    loger(f'数据库信息: {db_info}')
    
    # 测试连接池状态
    pool_status = db_conn.pool_status
    loger(f'连接池状态: {pool_status}')
    # 测试异步事务上下文管理器
    async def test_session_scope_async():
        try:
            async with db_conn.session_scope_async():
                ...
        except Exception as e:
            loger(f'异步事务上下文管理器测试失败: {e!s}')

    # 测试释放连接资源
    async def test_dispose():
        try:
            await db_conn.dispose_async()
        except Exception as e:
            loger(f'异步释放连接资源测试失败: {e!s}')

    # 运行异步测试
    db_conn.loop_run([test_session_scope_async(), test_dispose()])
