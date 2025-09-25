# !/usr/bin/env python3
"""
==============================================================
Description  : SQL ORM操作模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:30:00
LastEditTime : 2024-09-22 10:30:00
FilePath     : /code/xt_sqlorm/db/orm_operations.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- 通用的ORM增删改查操作
- 条件查询、分页查询、批量操作
- 事务处理和错误处理
==============================================================
"""

from __future__ import annotations

import contextlib
from collections.abc import Generator
from typing import Any, Literal

import pandas
import pandas as pd
from pydantic import BaseModel, ValidationError
from sqlalchemy import and_, func, or_, text
from sqlalchemy.orm import Query, Session
from xt_sqlorm.core.connection import SqlConnection
from xt_wraps.exception import handle_exception
from xt_wraps.log import create_basemsg, log_wraps
from xt_wraps.log import mylog as log


class OrmOperations[T]:
    """优化的ORM操作基类"""

    def __init__(self, data_model: type[T], db_conn: SqlConnection | None = None, validator_model: type[BaseModel] | None = None, cache_enabled: bool = True):
        """
        初始化ORM操作类

        Args:
            data_model: ORM模型类
            db_conn: 数据库连接对象
            validator_model: Pydantic验证模型
            cache_enabled: 是否启用查询缓存
        """
        self._data_model = data_model
        self.id = self._data_model.__name__
        self._db_conn = db_conn
        self._validator_model = validator_model
        self._cache_enabled = cache_enabled
        self._query_cache = {}

    @property
    def db(self) -> SqlConnection:
        """获取或创建数据库连接对象"""
        if not self._db_conn:
            self._db_conn = SqlConnection()
        return self._db_conn

    @log_wraps
    @contextlib.contextmanager
    def session_scope(self, session: Session | None = None) -> Generator[Session]:
        """事务上下文管理器"""
        external_session = session is not None
        current_session = session or self.db.session

        try:
            log.start(f'{self.id} | 事务开始')
            yield current_session
            if not external_session:
                current_session.commit()
                log.ok(f'{self.id} | 事务成功')
        except Exception as e:
            if not external_session:
                current_session.rollback()
            handle_exception(f'{self.id} | 事务失败，已回滚', e, re_raise=True)
        finally:
            if not external_session:
                current_session.close()
                log.stop(f'{self.id} | 事务会话关闭')

    def _validate_data(self, data_dict: dict[str, Any]) -> dict[str, Any]:
        """数据验证"""
        if self._validator_model:
            try:
                validated_data = self._validator_model(**data_dict)
                return validated_data.dict(exclude_unset=True)
            except ValidationError as e:
                log.fail(f'{self.id} | 数据验证失败: {e}')
                raise ValueError(f'数据验证失败: {e}') from e
        return data_dict

    @log_wraps
    def get_by_id(self, id_value: int, session: Session | None = None) -> T | None:
        """根据ID获取记录（带缓存）,基础CRUD操作"""
        if self._cache_enabled:
            cache_key = f'id_{id_value}'
            if cache_key in self._query_cache:
                return self._query_cache[cache_key]

        session = session or self.db.session
        result = session.get(self._data_model, id_value)

        if self._cache_enabled and result:
            self._query_cache[cache_key] = result

        return result

    @log_wraps
    def create(self, data_dict: dict[str, Any], session: Session | None = None) -> T:
        """创建记录（带验证）"""
        validated_data = self._validate_data(data_dict)

        with self.session_scope(session) as current_session:
            instance = self._data_model(**validated_data)
            current_session.add(instance)

            if self._cache_enabled:
                # 清除相关缓存
                self.clear_cache()

            return instance

    # 批量操作优化
    @log_wraps
    def bulk_create_optimized(self, data_list: list[dict[str, Any]], batch_size: int = 1000, session: Session | None = None) -> list[T]:
        """优化的批量创建"""
        instances = []

        with self.transaction_scope(session) as current_session:
            for i in range(0, len(data_list), batch_size):
                batch_data = data_list[i : i + batch_size]
                batch_instances = [self._data_model(**self._validate_data(data)) for data in batch_data]
                current_session.add_all(batch_instances)
                instances.extend(batch_instances)

                # 分批刷新，避免内存问题
                if i % batch_size == 0:
                    current_session.flush()

        if self._cache_enabled:
            self.clear_cache()

        return instances

    # 高级查询方法
    @log_wraps
    def advanced_query(self, filters: list[Any] | None = None, order_by: list[Any] | None = None, limit: int | None = None, offset: int | None = None, session: Session | None = None) -> Query:
        """构建高级查询"""
        session = session or self.db.session
        query = session.query(self._data_model)

        if filters:
            query = query.filter(*filters)
        if order_by:
            query = query.order_by(*order_by)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return query

    def clear_cache(self) -> None:
        """清空缓存"""
        self._query_cache.clear()

    # 统计和分析方法
    @log_wraps
    def get_field_stats(self, field_name: str, session: Session | None = None) -> dict[str, Any]:
        """获取字段统计信息"""
        session = session or self.db.session
        field = getattr(self._data_model, field_name)

        stats = session.query(func.count(field), func.min(field), func.max(field), func.avg(field)).scalar()

        return {'count': stats[0], 'min': stats[1], 'max': stats[2], 'avg': float(stats[3]) if stats[3] else 0}

    # 数据导出方法
    @log_wraps
    def export_to_dataframe(self, columns: list[str] | None = None, filters: list[Any] | None = None, session: Session | None = None) -> pd.DataFrame:
        """导出到Pandas DataFrame"""
        session = session or self.db.session

        if columns:
            query_columns = [getattr(self._data_model, col) for col in columns]
            query = session.query(*query_columns)
        else:
            query = session.query(self._data_model)

        if filters:
            query = query.filter(*filters)

        return pd.read_sql(query.statement, session.bind)

    @log_wraps
    def get_one(self, where_dict: dict[str, Any] | None = None, session: Session | None = None) -> T | None:
        """
        获取符合条件的单条记录

        Args:
            where_dict: 查询条件字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            查询到的模型对象，不存在则返回None
        """
        msg = create_basemsg(self.get_one)
        session = session or self.db.session
        query = session.query(self._data_model)
        if where_dict:
            query = query.filter_by(**where_dict)
        result = query.first()
        if result:
            log.ok(f'{msg} | 查询单个{self.id}，条件{where_dict}: 找到: {result}')
        else:
            log.warning(f'{msg} | 查询单个{self.id}，条件{where_dict}: 未找到')
        return result

    @log_wraps
    def get_all(self, where_dict: dict[str, Any] | None = None, session: Session | None = None) -> list[T]:
        """
        获取符合条件的所有记录

        Args:
            where_dict: 查询条件字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            查询到的模型对象列表
        """
        msg = create_basemsg(self.get_all)
        session = session or self.db.session
        query = session.query(self._data_model)
        if where_dict:
            query = query.filter_by(**where_dict)
        result = query.all()
        if result:
            log.ok(f'{msg} | 查询所有{self.id}，条件{where_dict}: 找到{len(result)}条记录')
        else:
            log.warning(f'{msg} | 查询所有{self.id}，条件{where_dict}: 未找到')
        return result

    @log_wraps
    def get_paginated(
        self, page: int = 1, page_size: int = 10, where_dict: dict[str, Any] | None = None, order_by: str | None = None, order_dir: Literal['asc', 'desc'] = 'asc', session: Session | None = None
    ) -> tuple[list[T], int]:
        """
        分页查询记录

        Args:
            page: 页码，从1开始
            page_size: 每页记录数
            where_dict: 查询条件字典
            order_by: 排序字段
            order_dir: 排序方向，'asc'或'desc'
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            (查询到的模型对象列表, 总记录数)
        """
        msg = create_basemsg(self.get_paginated)
        session = session or self.db.session
        # 构建查询
        query = session.query(self._data_model)
        if where_dict:
            query = query.filter_by(**where_dict)

        # 计算总记录数
        total_count = query.count()

        # 排序
        if order_by:
            order_field = getattr(self._data_model, order_by)
            query = query.order_by(order_field.desc()) if order_dir == 'desc' else query.order_by(order_field)

        # 分页
        offset = (page - 1) * page_size
        result = query.offset(offset).limit(page_size).all()
        if result:
            log.ok(f'{msg} | {self.id}分页查询: 页码={page}, 每页条数={page_size}, 总记录数={total_count}')
        else:
            log.warning(f'{msg} | {self.id}分页查询: 未找到')
        return result, total_count

    @log_wraps
    def update(self, instance: T, data_dict: dict[str, Any], session: Session | None = None) -> T:
        """
        更新现有记录

        Args:
            instance: 要更新的模型对象
            data_dict: 要更新的数据字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            更新后的模型对象
        """
        msg = create_basemsg(self.update)
        external_session = session is not None
        session = session or self.db.session

        # 更新字段
        for key, value in data_dict.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        # 如果没有传入会话，则提交（外部会话由调用者管理事务）
        if not external_session:
            self.db.commit()
        log.ok(f'{msg} | 更新{self.id} {instance.ID}: {data_dict}')
        return instance

    @log_wraps
    def update_by_id(self, id_value: int, data_dict: dict[str, Any], session: Session | None = None) -> T | None:
        """
        根据ID更新记录

        Args:
            id_value: ID值
            data_dict: 要更新的数据字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            更新后的模型对象，不存在则返回None
        """
        msg = create_basemsg(self.update_by_id)
        instance = self.get_by_id(id_value, session)
        if instance:
            return self.update(instance, data_dict, session)
        log.warning(f'{msg} | 根据ID {id_value}更新{self.id}失败: 记录不存在')
        return None

    @log_wraps
    def delete(self, instance: T, session: Session | None = None) -> bool:
        """
        删除记录

        Args:
            instance: 要删除的模型对象
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            删除成功返回True
        """
        msg = create_basemsg(self.delete)
        external_session = session is not None
        session = session or self.db.session

        session.delete(instance)

        # 如果没有传入会话，则提交（外部会话由调用者管理事务）
        if not external_session:
            self.db.commit()

        log.ok(f'{msg} | 删除{self.id} {instance.ID}')
        return True

    @log_wraps
    def delete_by_id(self, id_value: int, session: Session | None = None) -> bool:
        """
        根据ID删除记录

        Args:
            id_value: ID值
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            删除成功返回True，记录不存在返回False
        """
        msg = create_basemsg(self.delete_by_id)
        instance = self.get_by_id(id_value, session)
        if instance:
            return self.delete(instance, session)
        log.warning(f'{msg} | 删除{self.id}失败: ID {id_value}未找到')
        return False

    @log_wraps
    def bulk_create(self, data_list: list[dict[str, Any]], session: Session | None = None) -> list[T]:
        """
        批量创建记录

        Args:
            data_list: 记录数据字典列表
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            创建的模型对象列表
        """
        msg = create_basemsg(self.bulk_create)
        external_session = session is not None
        session = session or self.db.session

        # 创建模型对象列表
        instances = [self._data_model(**data) for data in data_list]

        # 批量添加
        session.add_all(instances)

        # 如果没有传入会话，则提交（外部会话由调用者管理事务）
        if not external_session:
            self.db.commit()

        log.ok(f'{msg} | 批量创建{len(instances)}条{self.id}记录')
        return instances

    @log_wraps
    def execute_raw_sql(self, sql: str, params: dict[str, Any] | None = None, session: Session | None = None) -> Any:
        """
        执行原生SQL语句

        Args:
            sql: SQL查询语句
            params: SQL参数绑定
            session: 数据库会话对象，如果为None则使用数据库连接的execute_sql方法

        Returns:
            查询结果
        """
        msg = create_basemsg(self.execute_raw_sql)
        if session:
            log.info(f'{msg} | 使用会话执行原生SQL: {sql}, 参数: {params}')
            return session.execute(text(sql), params or {})
        log.info(f'{msg} | 使用数据库连接执行原生SQL: {sql}, 参数: {params}')
        return self.db.execute_sql(sql, params)

    @log_wraps
    def count(self, where_dict: dict[str, Any] | None = None, session: Session | None = None) -> int:
        """
        统计符合条件的记录数

        Args:
            where_dict: 查询条件字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            记录数量
        """
        msg = create_basemsg(self.count)
        session = session or self.db.session
        query = session.query(func.count('*')).select_from(self._data_model)
        if where_dict:
            query = query.filter_by(**where_dict)
        count = query.scalar() or 0
        if count:
            log.ok(f'{msg} | 统计{self.id}数量，条件{where_dict}: {count}')
        else:
            log.warning(f'{msg} | 统计{self.id}数量，条件{where_dict}: 没找到')
        return count

    @log_wraps
    def from_statement(self, sql: str, where_dict: dict[str, Any] | None = None, session: Session | None = None) -> list[Any]:
        """
        执行原生SQL语句查询

        Args:
            sql: 原生SQL查询语句
            where_dict: SQL参数字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            查询结果列表
        """
        msg = create_basemsg(self.from_statement)
        session = session or self.db.session

        log.debug(f'▶️ 执行原生SQL: {sql}, 参数: {where_dict}')

        sql_text = text(sql)
        query = session.query(self._data_model).from_statement(sql_text)

        # 添加参数
        result = query.params(**where_dict).all() if where_dict else query.all()

        log.ok(f'{msg} | 原生SQL查询成功，返回 {len(result)} 条记录')
        return result

    @log_wraps
    def filter_by_conditions(self, conditions: list[dict[str, Any]], raw_count: int | None = None, session: Session | None = None) -> list[Any]:
        """
        多条件查询，支持复杂逻辑条件

        Args:
            conditions: 条件字典列表，每个字典表示一组AND条件
            raw_count: 限制返回的记录数量
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            查询结果列表
        """
        msg = create_basemsg(self.filter_by_conditions)
        session = session or self.db.session

        log.debug(f'🔍 多条件查询: {conditions}, 限制: {raw_count}')

        query = session.query(self._data_model)

        # 构建复杂条件
        if conditions:
            or_conditions = []
            for condition in conditions:
                and_conditions = []
                for key, value in condition.items():
                    and_conditions.append(getattr(self._data_model, key) == value)
                if and_conditions:
                    or_conditions.append(and_(*and_conditions))

            if or_conditions:
                query = query.filter(or_(*or_conditions))

        # 添加数量限制
        if raw_count is not None:
            query = query.limit(raw_count)

        result = query.all()
        log.ok(f'{msg} | 多条件查询成功，返回 {len(result)} 条记录')
        return result

    @log_wraps
    def pd_get_dict(self, session: Session | None = None) -> list[dict[str, Any]] | bool:
        """
        使用Pandas读取表数据并返回字典列表

        Args:
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            数据字典列表，如果没有数据则返回False
        """
        msg = create_basemsg(self.pd_get_dict)
        session = session or self.db.session

        log.debug(f'📊 使用Pandas读取表: {self._data_model.__tablename__}')

        try:
            result = pandas.read_sql_table(self._data_model.__tablename__, con=session.bind)
            data_dict = result.to_dict(orient='records')

            if data_dict:
                log.ok(f'{msg} | Pandas读取成功，返回 {len(data_dict)} 条记录')
                return data_dict

            log.warning(f'{msg} | 表 {self._data_model.__tablename__} 中没有数据')
            return False
        except Exception as e:
            log.error(f'{msg} | Pandas读取表 {self._data_model.__tablename__} 失败: {e!s}')
            raise

    @log_wraps
    def pd_get_list(self, columns: list[str], session: Session | None = None) -> list[list[Any]] | bool:
        """
        使用Pandas读取表指定列并返回去重后的列表

        Args:
            columns: 要读取的列名列表
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            列表数据，如果没有数据则返回False
        """
        msg = create_basemsg(self.pd_get_list)
        session = session or self.db.session

        log.debug(f'📊 使用Pandas读取表 {self._data_model.__tablename__} 的列: {columns}')

        try:
            result = pandas.read_sql_table(self._data_model.__tablename__, con=session.bind)
            pd_list = result[columns].drop_duplicates().values.tolist()

            if pd_list:
                log.ok(f'{msg} | Pandas列读取成功，返回 {len(pd_list)} 条去重记录')
                return pd_list

            log.warning(f'{msg} | 表 {self._data_model.__tablename__} 的列 {columns} 中没有数据')
            return False
        except Exception as e:
            log.error(f'{msg} | Pandas读取表 {self._data_model.__tablename__} 的列 {columns} 失败: {e!s}')
            raise

    @log_wraps
    def bulk_update(self, data_list: list[dict[str, Any]], where_key: str = 'ID', session: Session | None = None) -> int:
        """
        批量更新记录

        Args:
            data_list: 更新数据字典列表，每个字典必须包含where_key字段
            where_key: 用于定位记录的字段名，默认为'ID'
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            更新的记录数量
        """
        msg = create_basemsg(self.bulk_update)
        external_session = session is not None
        session = session or self.db.session

        updated_count = 0

        for data in data_list:
            if where_key in data:
                instance = self.get_by_id(data[where_key], session)
                if instance:
                    self.update(instance, data, session)
                    updated_count += 1

        # 如果没有传入会话，则提交（外部会话由调用者管理事务）
        if not external_session:
            self.db.commit()

        log.ok(f'{msg} | 批量更新{updated_count}条{self.id}记录')
        return updated_count

    @log_wraps
    def exists(self, where_dict: dict[str, Any] | None = None, session: Session | None = None) -> bool:
        """
        检查是否存在符合条件的记录

        Args:
            where_dict: 查询条件字典
            session: 数据库会话对象，如果为None则使用当前连接的会话

        Returns:
            存在返回True，否则返回False
        """
        msg = create_basemsg(self.exists)
        session = session or self.db.session

        query = session.query(self._data_model)
        if where_dict:
            query = query.filter_by(**where_dict)

        exists = session.query(query.exists()).scalar()

        if exists:
            log.ok(f'{msg} | 检查{self.id}存在，条件{where_dict}: 存在')
        else:
            log.warning(f'{msg} | 检查{self.id}存在，条件{where_dict}: 不存在')

        return exists
