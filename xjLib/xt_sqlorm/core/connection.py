# !/usr/bin/env python3
"""
==============================================================
Description  : SQL数据库连接管理模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:25:00
LastEditTime : 2024-09-22 10:25:00
FilePath     : /CODE/xjlib/xt_sqlorm/core/connection.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- SqlConnection: 同步SQL数据库连接管理类
- 数据库连接池配置和管理
- 事务处理和会话管理
==============================================================
"""

from __future__ import annotations

import contextlib
from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Query, Session, scoped_session, sessionmaker
from xt_database.cfg import connect_str
from xt_wraps.exception import exc_wraps, handle_exception
from xt_wraps.log import log_wraps, mylog
from xt_wraps.singleton import SingletonMeta

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine, Result


class SqlConnection(metaclass=SingletonMeta):
    """SQL数据库连接管理类

    提供数据库连接、会话管理、事务处理等功能
    支持多种数据库类型和连接参数配置

    特性:
    - 单例模式设计
    - 上下文管理器支持
    - 连接池管理
    - 事务自动提交和回滚
    """

    @exc_wraps
    def __init__(
        self,
        db_key: str = 'default',
        url: str | None = None,
        **kwargs: Any,
    ) -> None:
        """初始化数据库连接

        Args:
            db_key: 数据库配置键，用于从配置文件中获取连接信息，默认为'default'
            url: 数据库连接URL，格式为 "dialect+driver://username:password@host:port/database"
            **kwargs: 其他参数
        """
        if not url:
            url = connect_str(db_key)

        engine_config, session_config, remaining_kwargs = self._extract_engine_config(kwargs)
        self._engine: Engine = create_engine(url=url, **engine_config, **remaining_kwargs)
        self._session_factory = sessionmaker(bind=self._engine, **session_config)

        # 线程安全的会话对象,手动管理生命周期:self._scoped_session.remove()
        self._scoped_session_factory = scoped_session(self._session_factory)
        # 不初始化 _session，让属性处理
        self._session: Session | None = None

        if self.ping():
            mylog.success(f'SqlConnection@__init__ | 数据库连接已初始化: {self}')

    def __str__(self) -> str:
        return f'SqlConnection({self._engine.url!s})'

    def __enter__(self) -> SqlConnection:
        """上下文管理器入口

        # 使用方式：
        with SqlConnection() as db:
            db.session.add(obj)
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """上下文管理器出口

        自动提交或回滚事务，并关闭会话
        """
        try:
            if exc_type is not None:
                self.rollback()
                mylog.warning(f'SqlConnection@__exit__ | 事务回滚，异常: {exc_type.__name__}')
            else:
                self.commit()
        finally:
            self.cleanup_session(exc_val)

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
            'query_cls': Query,
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
            mylog.warning(f'SqlConnection | 以下参数未被识别: {list(kwargs.keys())}')

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
    def datainfo(self) -> dict[str, Any]:
        """获取数据库详细信息"""
        with self._engine.connect() as conn:
            # 获取数据库版本等信息
            result = conn.execute(text('SELECT version()'))
            version = result.scalar()
            
            # 获取当前连接数
            result = conn.execute(text('SELECT COUNT(*) FROM information_schema.processlist'))
            connections = result.scalar()
            
            return {
                'version': version,
                'active_connections': connections,
                'url': str(self._engine.url),
                'pool_status': self.pool_status,
            }

    @property
    def engine(self) -> Engine:
        """获取数据库引擎对象"""
        if not hasattr(self, '_engine'):
            mylog.error('SqlConnection@engine | 数据库引擎未初始化')
            raise RuntimeError('数据库引擎未初始化')
        return self._engine

    @property
    def session(self) -> Session:
        """获取当前数据库会话对象

        如果会话不存在则创建新的安全会话
        """
        if self._session is None:
            self._session = self._scoped_session_factory()
            mylog.success('SqlConnection@session | 安全会话已创建')
        return self._session

    @exc_wraps
    def cleanup_session(self, exception=None):
        """清理当前会话,请求结束时调用"""
        if self._session is None:
            return

        self._session.close()
        self._scoped_session_factory.remove()
        self._session = None
        if exception:
            mylog.success(f'SqlConnection@cleanup_session | 会话已清理，异常: {exception}')
        else:
            mylog.success('SqlConnection@cleanup_session | 安全会话已清理')

    @exc_wraps
    def new_session(self) -> Session:
        """创建新的数据库会话"""
        return self._session_factory()

    @exc_wraps
    def commit(self) -> None:
        """提交当前事务"""
        self.session.commit()
        mylog.success('SqlConnection@commit | 事务已成功提交')

    @exc_wraps
    def rollback(self) -> None:
        """回滚当前事务"""
        self.session.rollback()
        mylog.success('SqlConnection@rollback | 事务已回滚')

    @log_wraps
    def execute_sql(self, sql: str, params: dict[str, Any] | None = None) -> Result:
        """执行原生SQL语句

        Args:
            sql: SQL查询语句
            params: SQL参数绑定，默认为None

        Returns:
            查询结果
        """
        # 修复默认参数问题
        if params is None:
            params = {}

        with self.engine.begin() as conn:  # 使用begin()明确事务
            return conn.execute(text(sql), params)  # 自动提交

    @log_wraps(default_return=False)
    def ping(self) -> bool:
        """测试数据库连接是否正常

        Returns:
            连接成功返回True，否则返回False
        """
        with self.engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return True

    @log_wraps
    @contextlib.contextmanager
    def session_scope(self) -> Generator[Session]:
        """事务上下文管理器

        使用示例:
            with db.session_scope() as session:
                # 执行数据库操作
                session.add(some_model)
                # 自动提交，异常时自动回滚
        """
        session = self.new_session()
        try:
            mylog.debug('SqlConnection@session_scope | 事务开始')
            yield session
            session.commit()
            mylog.success('SqlConnection@session_scope | 事务完成')
        except Exception as e:
            session.rollback()
            handle_exception(e, re_raise=True, callfrom=self.session_scope)
        finally:
            session.close()
            mylog.info('SqlConnection@session_scope | 事务会话关闭')

    @log_wraps
    def execute_many(self, sql: str, params_list: list[dict[str, Any]]) -> list[Any]:
        """同步批量执行SQL语句"""
        results = []
        with self.engine.begin() as conn:
            for params in params_list:
                result = conn.execute(text(sql), params)
                results.append(result)
        return results

    @exc_wraps
    def dispose(self) -> None:
        """释放数据库连接资源"""
        if not hasattr(self, '_engine'):
            mylog.warning('SqlConnection@dispose | 数据库引擎不存在，无需释放')
            return
        try:
            self.cleanup_session()
            self.engine.dispose()
            mylog.info('SqlConnection@dispose | 数据库引擎已释放')
        finally:
            # 使用元类提供的方法重置单例实例
            type(self).reset_instance()


__all__ = ['SqlConnection']


if __name__ == '__main__':
    db_conn = SqlConnection()
    mylog.info(db_conn.ping())
    # 测试同步执行SQL
    sql_result = db_conn.execute_sql('SELECT 1')
    mylog.info(f'同步执行SQL测试结果: {sql_result}')
    # 展示如何提取数据
    scalar_value = sql_result.scalar()
    mylog.info(f'从结果中提取单个值: {scalar_value}')

    # 执行一个返回多行数据的查询示例
    multi_result = db_conn.execute_sql('SELECT 1 AS id, 2 AS value UNION SELECT 3, 4')
    all_rows = multi_result.all()
    mylog.info(f'提取所有行数据: {all_rows}')

    # 以字典形式获取结果
    dict_rows = multi_result.mappings().all()
    mylog.info(f'以字典形式提取所有行数据: {dict_rows}')

    # 测试同步创建会话
    session = db_conn.new_session()

    with db_conn.session_scope():
        ...
    # 测试数据库信息获取
    db_info = db_conn.datainfo()
    mylog.info(f'数据库信息: {db_info}')
    
    # 测试连接池状态
    pool_status = db_conn.pool_status
    mylog.info(f'连接池状态: {pool_status}')
    db_conn.dispose()

