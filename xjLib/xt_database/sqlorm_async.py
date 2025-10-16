# !/usr/bin/env python
"""
==============================================================
Description  : 异步SQLAlchemy ORM数据库操作模块
Develop      : Python 3.9+
Author       : sandorn sandorn@live.cn
Date         : 2024-09-05 09:48:11
LastEditTime : 2025-09-18 20:00:00
FilePath     : D:/CODE/xjlib/xt_database/sqlorm_async.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 基于SQLAlchemy的异步数据库操作
- 支持查询、插入、更新和批量操作
- 采用单例模式确保数据库连接管理的高效性

主要特性:
- 异步非阻塞数据库访问
- 完整的事务支持和错误处理
- 灵活的参数化查询
- 自动连接池管理
==============================================================
"""

from __future__ import annotations

import asyncio
from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from xt_database.cfg import connect_str
from xt_database.sqlorm_meta import ErrorMetaClass, copy_db_model
from xt_database.untilsql import make_insert_sql, make_update_sql
from xt_wraps.log import log_wraps, mylog as loger
from xt_wraps.singleton import SingletonMeta


class AioMySqlOrm(ErrorMetaClass, metaclass=SingletonMeta):
    """异步MySQL ORM操作类 - 提供高效的异步数据库访问功能

    该类提供基于SQLAlchemy的异步数据库操作功能，支持单例模式，确保连接资源的高效管理。

    Args:
        db_key: 数据库配置键名，默认为'default'
        target_table_name: 目标表名（类型：str | None，可选）
        source_table_name: 源表名（类型：str | None，可选）

    Attributes:
        tablename: 目标表名
        engine: 同步数据库引擎
        Base: 数据库模型类
        async_engine: 异步数据库引擎
        async_session: 异步会话工厂
        loop: 事件循环

    Raises:
        Exception: 初始化数据库连接失败时抛出

    Example:
        >>> # 创建实例示例
        >>> aio_orm = AioMySqlOrm('TXbx', 'users2', 'users_model')
        >>> # 查询示例
        >>> results = aio_orm.query('SELECT * FROM users2 WHERE id = 1')
    """

    @log_wraps
    def __init__(self, db_key: str = 'default', target_table_name: str | None = None, source_table_name: str | None = None) -> None:
        """初始化数据库连接

        Args:
            db_key: 数据库配置键名，默认为'default'
            target_table_name: 目标表名
            source_table_name: 源表名

        Raises:
            Exception: 初始化数据库连接失败时抛出
        """
        self.tablename = target_table_name
        try:
            # 创建同步引擎用于模型复制
            self.engine = create_engine(connect_str(db_key))
            self.Base = copy_db_model(self.engine, target_table_name, source_table_name)

            # 创建异步引擎
            self.async_engine = create_async_engine(
                connect_str(key=db_key, odbc='aiomysql'),
                max_overflow=0,  # 超过连接池大小外最多创建的连接
                pool_size=5,  # 连接池大小
                pool_timeout=30,  # 池中没有线程最多等待的时间,否则报错
                pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                echo=__name__ == '__main__',  # 是否打印sql语句
                future=True,  # 使用异步模式
            )

            # 创建异步会话工厂
            self.async_session = async_sessionmaker(
                bind=self.async_engine,
                autoflush=True,  # 自动刷新
                class_=AsyncSession,  # 异步会话类
            )

            # 创建并设置事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            loger.info(f'成功初始化数据库连接，配置键: {db_key}')
        except Exception as e:
            loger.fail(f'初始化数据库连接失败: {e}')
            raise

    @log_wraps
    def run_until_loop(self, coro_list: list[Any]) -> list[Any]:
        """运行协程列表直到完成

        Args:
            coro_list: 协程对象列表

        Returns:
            List[Any]: 协程执行结果列表

        Raises:
            Exception: 运行协程失败时抛出
        """
        try:
            return self.loop.run_until_complete(asyncio.gather(*coro_list))
        except Exception as e:
            loger.fail(f'运行协程失败: {e}')
            raise

    @log_wraps(log_result=False)
    def query(self, sql_list: str | list[str], params: dict[str, Any] | None = None) -> list[Any]:
        """执行SQL查询

        Args:
            sql_list: SQL查询语句或语句列表
            params: 查询参数字典（可选）

        Returns:
            List[Any]: 查询结果列表

        Example:
            >>> # 单条查询
            >>> results = aio_orm.query('SELECT * FROM users WHERE id = :id', {'id': 1})
            >>> # 多条查询
            >>> results = aio_orm.query(['SELECT * FROM users', 'SELECT * FROM orders'])
        """
        try:
            # 确保sql_list是列表格式
            sql_list = [sql_list] if isinstance(sql_list, str) else sql_list

            # 创建协程列表
            coro_list = [self._query(_sql, params) for _sql in sql_list]

            loger.info(f'执行查询，语句数量: {len(sql_list)}')
            return self.run_until_loop(coro_list)
        except Exception as e:
            loger.fail(f'执行查询失败: {e}')
            raise

    @log_wraps(log_result=False)
    async def _query(self, sql: str, params: dict[str, Any] | None = None) -> list[Any] | int | None:
        """异步执行单个SQL查询

        Args:
            sql: SQL查询语句
            params: 查询参数字典（可选）

        Returns:
            List[Any] | int | None: 查询结果行列表或受影响行数，失败返回None
        """
        # 确保sql是字符串类型
        if not isinstance(sql, str):
            raise TypeError(f'SQL must be a string, got {type(sql).__name__}')

        # 处理SQL中的占位符格式
        # 将 %s 替换为 :param_0, :param_1 等，以匹配SQLAlchemy的命名参数格式
        # 只在没有冒号占位符的情况下进行替换
        if '%s' in sql and ':' not in sql:
            # 计算%s的数量
            count = sql.count('%s')
            new_sql = sql
            for i in range(count):
                # 确保不会重复替换已替换的部分
                placeholder = f':param_{i}'
                new_sql = new_sql.replace('%s', placeholder, 1)
            sql = new_sql

            # 调整参数格式
            if params is not None:
                if isinstance(params, tuple):
                    # 将元组参数转换为命名字典
                    params = {f'param_{i}': params[i] for i in range(len(params))}
                elif isinstance(params, dict) and all(k.startswith('col_') for k in params):
                    # 转换col_*格式参数为param_*格式
                    params = {f'param_{i}': params[f'col_{i}'] for i in range(count) if f'col_{i}' in params}

        async with self.async_session() as session:
            try:
                # 确保params是字典类型
                safe_params = params or {}

                result = await session.execute(text(sql), safe_params)
                await session.commit()

                # 根据结果类型返回不同格式数据
                if getattr(result, 'returns_rows', False):
                    # 返回元组列表
                    rows = result.fetchall()
                    # 转换为列表字典格式
                    return [dict(row._mapping) for row in rows]
                return getattr(result, 'rowcount', 0)
            except SQLAlchemyError as e:
                await session.rollback()
                loger.fail(f'执行SQL失败: {sql}, 参数: {params}, 错误: {e}')
                return None
            except Exception as e:
                await session.rollback()
                loger.fail(f'查询过程中发生未知错误: {e}')
                return None

    @log_wraps
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
            >>> # 插入单条数据
            >>> item = {'username': '张三', 'password': '123456', 'created_at': '2024-05-18'}
            >>> result = aio_orm.insert(item)
            >>> # 插入多条数据
            >>> data_list = [{'username': '张三', 'password': '123456'}, {'username': '李四', 'password': '654321'}]
            >>> results = aio_orm.insert(data_list)
        """
        tablename = tablename or self.tablename
        if not tablename:
            raise ValueError('表名不能为空，请在参数中指定或在实例化时设置')

        if isinstance(data_list, dict):
            data_list = [data_list]

        # 生成参数化SQL和参数列表
        sql_params_list = [make_insert_sql(data_dict, tablename) for data_dict in data_list]
        coro = [self._query(sql, *params) if isinstance(sql, tuple) else self._query(sql, params) for sql, params in sql_params_list]
        return self.run_until_loop(coro)

    @log_wraps
    def update(self, data_list: dict[str, Any] | list[dict[str, Any]], where_list: dict[str, Any] | list[dict[str, Any]] | None = None, tablename: str | None = None) -> list[int]:
        """执行数据更新操作

        Args:
            data_list: 单条或多条更新数据字典，字典的键为列名，值为要更新的数据
            where_list: 单条或多条更新条件字典，字典的键为列名，值为条件值
                        如果为None，则data_list中的每一条数据的主键将作为更新条件
            tablename: 表名（可选，默认使用实例化时指定的表名）

        Returns:
            list[int]: 更新操作受影响的行数列表

        Raises:
            ValueError: 当表名为空或data_list与where_list长度不匹配时抛出
            Exception: 当更新操作失败时抛出

        Example:
            >>> # 单条更新
            >>> data = {'username': '张三_update', 'password': '654321'}
            >>> where = {'id': 1}
            >>> result = aio_orm.update(data, where)
            >>> # 多条更新
            >>> data_list = [{'username': '张三_update'}, {'username': '李四_update'}]
            >>> where_list = [{'id': 1}, {'id': 2}]
            >>> results = aio_orm.update(data_list, where_list)
        """
        tablename = tablename or self.tablename
        if not tablename:
            raise ValueError('表名不能为空，请在参数中指定或在实例化时设置')

        # 确保data_list是列表格式
        if isinstance(data_list, dict):
            data_list = [data_list]
            where_list = [where_list] if isinstance(where_list, dict) else where_list
        else:
            if where_list is not None and not isinstance(where_list, list):
                raise ValueError('当data_list为列表时，where_list必须为列表或None')

        # 验证data_list和where_list长度匹配
        if where_list is not None and len(data_list) != len(where_list):
            raise ValueError(f'data_list和where_list长度必须一致: {len(data_list)} != {len(where_list)}')

        # 生成参数化SQL和参数列表
        sql_params_list = []
        for i, data_dict in enumerate(data_list):
            where_dict = where_list[i] if where_list else None
            try:
                sql_params = make_update_sql(data_dict, where_dict, tablename)
                sql_params_list.append(sql_params)
            except Exception as e:
                loger.warning(f'生成更新SQL失败: {e}')
                continue

        # 执行更新操作
        coro_list = []
        for sql_params in sql_params_list:
            if isinstance(sql_params, tuple):
                sql, params = sql_params
                if isinstance(params, tuple):
                    params = {f'param_{i}': v for i, v in enumerate(params)}
                coro_list.append(self._query(sql, params))
            else:
                sql = sql_params
                where_dict = where_list[i] if where_list else {}
                params = {**data_dict, **where_dict}
                coro_list.append(self._query(sql, params))

        loger.info(f'执行更新，记录数量: {len(data_list)}, 表名: {tablename}')
        return self.run_until_loop(coro_list)

    @log_wraps
    def add_all(self, dict_in_list: list[dict[str, Any]]) -> list[int]:
        """批量添加记录

        Args:
            dict_in_list: 要添加的字典列表

        Returns:
            list[int]: 添加的记录数列表，每个元素表示对应添加操作的记录数

        Example:
            >>> # 批量添加
            >>> records = [{'username': 'user1', 'email': 'user1@example.com'}, {'username': 'user2', 'email': 'user2@example.com'}]
            >>> count = aio_orm.add_all(records)
        """
        try:
            # 验证输入
            if not dict_in_list:
                loger.warning('添加记录为空')
                return [0]

            coro_list = [self._add_all(dict_in_list)]
            result = self.run_until_loop(coro_list)

            # 返回结果处理
            if result and result[0] is not None:
                loger.ok(f'批量添加成功，记录数: {result[0]}')
                return [result[0]]
            loger.fail('批量添加失败')
            return [-1]
        except Exception as e:
            loger.fail(f'执行批量添加失败: {e}')
            return [-1]

    @log_wraps
    async def _add_all(self, dict_in_list: list[dict[str, Any]]) -> int | None:
        """异步批量添加记录

        Args:
            dict_in_list: 要添加的字典列表

        Returns:
            int | None: 添加的记录数，失败返回None
        """
        try:
            items_list = [self.Base(**__d) for __d in dict_in_list]

            async with self.async_session() as session:
                try:
                    session.add_all(items_list)
                    await session.commit()
                    return len(items_list)
                except SQLAlchemyError as e:
                    await session.rollback()
                    loger.fail(f'批量提交失败: {e}')
                    return None
        except Exception as e:
            loger.fail(f'批量添加准备失败: {e}')
            return None


def create_aio_mysql_orm(db_key: str = 'default', target_table: str | None = None, source_table: str | None = None) -> AioMySqlOrm:
    """创建异步MySQL ORM实例的工厂函数

    Args:
        db_key: 数据库配置键名
        target_table: 目标表名
        source_table: 源表名

    Returns:
        AioMySqlOrm: 异步MySQL ORM实例
    """
    return AioMySqlOrm(db_key, target_table, source_table)


if __name__ == '__main__':
    """本模块功能测试与使用示例

    提供本模块的主要功能演示和使用方法，包括:
    1. 初始化数据库连接
    2. 执行查询操作
    3. 数据插入与更新
    """

    # 示例数据
    query_list = ['select * from users2 where id = 1', 'select * from users2']
    item1 = {
        'username': '刘新',
        'password': '234567',
        '手机': '13910118122',
        '代理人编码': '10005393',
        '会员级别': 'SSS',
        '会员到期日': '9999-12-31 00:00:00',
    }

    try:
        # 初始化数据库连接
        loger.start('初始化数据库连接')
        aio = create_aio_mysql_orm('TXbx', 'users2', 'users_model')
        loger.stop('初始化完成')

        # 插入示例
        loger.start('执行插入操作')
        insert_res = aio.insert(item1)
        loger.ok(f'插入结果: 受影响行数列表 = {insert_res}')

        # 更新示例
        loger.start('执行更新操作')
        update_data = {'username': '刘新_更新'}
        update_condition = {'username': '刘新'}
        update_res = aio.update(update_data, update_condition)
        loger.ok(f'更新结果: 受影响行数列表 = {update_res}')

        # 批量添加示例
        loger.start('执行批量添加操作')
        batch_items = [
            {
                'username': '测试用户1',
                'password': '123456',
                '手机': '13800138001',
                '代理人编码': '10005394',
                '会员级别': 'S',
                '会员到期日': '2025-12-31 00:00:00',
            },
            {
                'username': '测试用户2',
                'password': '654321',
                '手机': '13800138002',
                '代理人编码': '10005395',
                '会员级别': 'A',
                '会员到期日': '2025-12-31 00:00:00',
            },
        ]
        batch_add_res = aio.add_all(batch_items)
        loger.ok(f'批量添加结果: 记录数列表 = {batch_add_res}')

        # 查询示例
        loger.start('执行查询操作')
        res = aio.query(query_list[1])
        loger.ok(f'查询结果: {len(res[0]) if res and res[0] else 0} 条记录')

        # 批量更新示例
        loger.start('执行批量更新操作')
        multi_update_data = [
            {'会员级别': 'B'},
            {'会员级别': 'C'}
        ]
        multi_update_where = [
            {'username': '测试用户1'},
            {'username': '测试用户2'}
        ]
        multi_update_res = aio.update(multi_update_data, multi_update_where)
        loger.ok(f'批量更新结果: 受影响行数列表 = {multi_update_res}')
        
    except Exception as e:
        loger.fail(f'示例运行失败: {e}')
        raise
