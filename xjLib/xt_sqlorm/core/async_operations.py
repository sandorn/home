# !/usr/bin/env python3
"""
==============================================================
Description  : 异步SQL ORM操作模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-23 10:15:00
LastEditTime : 2025-09-23 10:15:00
FilePath     : /CODE/xjlib/xt_sqlorm/core/async_operations.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 异步通用的ORM增删改查操作
- 异步条件查询、分页查询、批量操作
- 异步事务处理和错误处理
==============================================================
"""

from __future__ import annotations

import asyncio
from typing import Any

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from xt_database.untilsql import make_insert_sql, make_update_sql
from xt_sqlorm.core.async_connection import AsyncSqlConnection
from xt_wraps.exception import exc_wraps
from xt_wraps.log import log_wraps, mylog as loger


class AsyncOrmOperations[T]:
    """异步ORM操作基类

    提供异步通用的ORM增删改查操作
    """

    def __init__(self, data_model: type[T], db_conn: AsyncSqlConnection | None = None):
        """
        初始化异步ORM操作类

        Args:
            data_model: ORM模型类
            db_conn: 异步数据库连接对象，如果为None则创建新连接
        """
        self._data_model = data_model
        self.id = self._data_model.__name__
        self._db_conn = db_conn
        self._loop = None  # 延迟初始化

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

    @property
    def db(self) -> AsyncSqlConnection:
        """获取或创建异步数据库连接对象"""
        if not self._db_conn:
            self._db_conn = AsyncSqlConnection()
        return self._db_conn

    @log_wraps
    async def get_by_id(self, id_value: int, session: AsyncSession | None = None) -> T | None:
        """
        异步根据ID获取单条记录

        Args:
            id_value: ID值
            session: 异步数据库会话对象，如果为None则创建新会话

        Returns:
            查询到的模型对象，不存在则返回None
        """
        session = session or await self.db.create_session()
        try:
            result = await session.get(self._data_model, id_value)
            if result:
                loger.ok(f'根据ID {id_value}查询{self.id}: 找到')
            else:
                loger.warning(f'根据ID {id_value}查询{self.id}: 未找到')
            return result
        except Exception as e:
            loger.fail(f'异步查询ID失败: {e}')
            return None

    @log_wraps
    async def get_one(self, where_dict: dict[str, Any] | None = None, session: AsyncSession | None = None) -> T | None:
        """
        异步获取符合条件的单条记录

        Args:
            where_dict: 查询条件字典
            session: 异步数据库会话对象，如果为None则创建新会话

        Returns:
            查询到的模型对象，不存在则返回None
        """
        session = session or await self.db.create_session()
        try:
            query = session.query(self._data_model)
            if where_dict:
                query = query.filter_by(**where_dict)
            result = await query.first()
            if result:
                loger.ok(f'查询单个{self.id}，条件{where_dict}: 找到')
            else:
                loger.warning(f'查询单个{self.id}，条件{where_dict}: 未找到')
            return result
        except Exception as e:
            loger.fail(f'异步查询单条记录失败: {e}')
            return None

    @log_wraps(log_result=False)
    async def query(self, sql: str, params: dict[str, Any] | None = None, session: AsyncSession | None = None) -> list[Any] | int | None:
        """
        异步执行SQL查询

        Args:
            sql: SQL查询语句
            params: 查询参数字典（可选）
            session: 异步数据库会话对象，如果为None则创建新会话

        Returns:
            list[Any] | int | None: 查询结果行列表或受影响行数，失败返回None
        """
        # 确保sql是字符串类型
        if not isinstance(sql, str):
            raise TypeError(f'SQL must be a string, got {type(sql).__name__}')

        # 处理SQL中的占位符格式
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

        session = session or await self.db.create_session()
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
    async def insert(self, data: dict[str, Any], session: AsyncSession | None = None) -> int:
        """
        异步执行单条数据插入操作

        Args:
            data: 数据字典，字典的键为列名，值为要插入的数据
            session: 异步数据库会话对象，如果为None则创建新会话

        Returns:
            int: 插入操作受影响的行数
        """
        session = session or await self.db.create_session()
        try:
            # 创建模型实例
            instance = self._data_model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            loger.ok(f'成功插入{self.id}记录')
            return 1
        except Exception as e:
            await session.rollback()
            loger.fail(f'异步插入记录失败: {e}')
            return 0

    @log_wraps
    async def insert_many(self, data_list: list[dict[str, Any]], tablename: str | None = None) -> list[int]:
        """
        异步执行多条数据插入操作

        Args:
            data_list: 多条数据字典列表
            tablename: 表名（可选，默认从模型获取）

        Returns:
            list[int]: 插入操作受影响的行数列表
        """
        if isinstance(data_list, dict):
            data_list = [data_list]

        # 如果未指定表名，则从模型获取
        if not tablename:
            tablename = getattr(self._data_model, '__tablename__', None)
            if not tablename:
                raise ValueError('表名不能为空')

        # 生成参数化SQL和参数列表
        sql_params_list = [make_insert_sql(data_dict, tablename) for data_dict in data_list]
        coro = [self.query(sql, *params) if isinstance(sql, tuple) else self.query(sql, params) 
                for sql, params in sql_params_list]
        
        # 使用事件循环运行所有协程
        return self.db.run_until_all(coro)

    @log_wraps
    async def update(self, data: dict[str, Any], where_dict: dict[str, Any], tablename: str | None = None) -> int:
        """
        异步执行单条数据更新操作

        Args:
            data: 更新数据字典
            where_dict: 更新条件字典
            tablename: 表名（可选，默认从模型获取）

        Returns:
            int: 更新操作受影响的行数
        """
        # 如果未指定表名，则从模型获取
        if not tablename:
            tablename = getattr(self._data_model, '__tablename__', None)
            if not tablename:
                raise ValueError('表名不能为空')

        try:
            # 生成更新SQL
            sql_params = make_update_sql(data, where_dict, tablename)
            
            # 执行更新
            if isinstance(sql_params, tuple):
                sql, params = sql_params
                if isinstance(params, tuple):
                    params = {f'param_{i}': v for i, v in enumerate(params)}
                result = await self.query(sql, params)
            else:
                result = await self.query(sql_params, {**data, **where_dict})
            
            loger.ok(f'成功更新{self.id}记录，受影响行数: {result}')
            return result if result is not None else 0
        except Exception as e:
            loger.fail(f'异步更新记录失败: {e}')
            return 0

    @log_wraps
    async def update_many(self, data_list: list[dict[str, Any]], where_list: list[dict[str, Any]], tablename: str | None = None) -> list[int]:
        """
        异步执行多条数据更新操作

        Args:
            data_list: 多条更新数据字典列表
            where_list: 多条更新条件字典列表
            tablename: 表名（可选，默认从模型获取）

        Returns:
            list[int]: 更新操作受影响的行数列表
        """
        # 验证输入
        if len(data_list) != len(where_list):
            raise ValueError('data_list和where_list长度必须一致')

        # 如果未指定表名，则从模型获取
        if not tablename:
            tablename = getattr(self._data_model, '__tablename__', None)
            if not tablename:
                raise ValueError('表名不能为空')

        # 生成参数化SQL和参数列表
        sql_params_list = []
        for i, data_dict in enumerate(data_list):
            where_dict = where_list[i]
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
                coro_list.append(self.query(sql, params))
            else:
                sql = sql_params
                coro_list.append(self.query(sql, {**data_list[i], **where_list[i]}))

        loger.info(f'执行批量更新，记录数量: {len(data_list)}, 表名: {tablename}')
        return self.db.run_until_all(coro_list)

    @log_wraps
    async def add_all(self, dict_in_list: list[dict[str, Any]], session: AsyncSession | None = None) -> list[int]:
        """
        异步批量添加记录

        Args:
            dict_in_list: 要添加的字典列表
            session: 异步数据库会话对象，如果为None则创建新会话

        Returns:
            list[int]: 添加的记录数列表，每个元素表示对应添加操作的记录数
        """
        try:
            # 验证输入
            if not dict_in_list:
                loger.warning('添加记录为空')
                return [0]

            session = session or await self.db.create_session()
            try:
                items_list = [self._data_model(**d) for d in dict_in_list]
                session.add_all(items_list)
                await session.commit()
                loger.ok(f'批量添加成功，记录数: {len(items_list)}')
                return [len(items_list)]
            except SQLAlchemyError as e:
                await session.rollback()
                loger.fail(f'批量提交失败: {e}')
                return [-1]
        except Exception as e:
            loger.fail(f'执行批量添加失败: {e}')
            return [-1]

    @log_wraps
    async def delete(self, where_dict: dict[str, Any], session: AsyncSession | None = None) -> int:
        """
        异步删除符合条件的记录

        Args:
            where_dict: 删除条件字典
            session: 异步数据库会话对象，如果为None则创建新会话

        Returns:
            int: 删除操作受影响的行数
        """
        session = session or await self.db.create_session()
        try:
            query = session.query(self._data_model)
            if where_dict:
                query = query.filter_by(**where_dict)
            result = await session.delete(query)
            await session.commit()
            loger.ok(f'成功删除{self.id}记录，受影响行数: {result}')
            return result
        except Exception as e:
            await session.rollback()
            loger.fail(f'异步删除记录失败: {e}')
            return 0


__all__ = ['AsyncOrmOperations']