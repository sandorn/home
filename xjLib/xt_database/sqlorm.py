# !/usr/bin/env python
"""
==============================================================
Description  : SQL ORM 数据库操作模块 - 提供基于SQLAlchemy的ORM数据库操作功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-07-22 09:23:24
LastEditTime : 2024-09-10 09:56:47
FilePath     : /CODE/xjlib/xt_database/sqlorm.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- SqlConnection类:基于SQLAlchemy的ORM数据库连接管理
- 完整的CRUD操作支持:查询、插入、更新、删除数据
- SQL语句执行能力:支持原生SQL查询和参数化查询
- Pandas集成:支持DataFrame与数据库之间的数据转换

主要特性:
- 单例模式设计:确保全局数据库连接一致性
- 上下文管理器支持:安全的事务处理
- 元数据访问:获取数据库结构信息
- 异常处理:保证数据库操作的稳定性
==============================================================
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TypeVar

import pandas
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from xt_database.cfg import connect_str
from xt_database.sqlorm_meta import ErrorMetaClass, copy_db_model
from xt_wraps.log import mylog as log
from xt_wraps.singleton import SingletonMeta

# 类型变量定义
T = TypeVar('T')


class SqlConnection(ErrorMetaClass, metaclass=SingletonMeta):
    """SQLAlchemy ORM数据库连接类 - 提供完整的ORM数据库操作功能

    基于SQLAlchemy实现的数据库操作类，支持单例模式，提供完整的CRUD操作、
    原生SQL执行、事务管理和Pandas数据处理功能。

    Args:
        conn_url: 数据库连接URL字符串
        table_name: 目标数据表名
        source_table: 源模型表名（用于模型复制）

    Attributes:
        engine: SQLAlchemy引擎对象
        tablename: 当前操作的表名
        Base: ORM模型基类
        pd_conn: Pandas数据库连接
        session: SQLAlchemy会话对象
        params: 表字段参数字典
        _query: 基础查询对象
        insp: SQLAlchemy检查器对象
        dbnames: 数据库名称列表
        log: 日志记录器
    """

    def __init__(self, conn_url: str, table_name: str | None = None, source_table: str | None = None, pool_size=5, pool_timeout=30, max_overflow=0, future=True, pool_recycle=-1) -> None:
        # 初始化日志
        self.log = log

        # 参数验证
        if not conn_url:
            self.log.error('❌ 数据库连接URL不能为空')
            raise ValueError('数据库连接URL不能为空')

        # 创建引擎
        self.engine = create_engine(
            conn_url,
            max_overflow=max_overflow,  # 超过连接池大小外最多创建的连接
            pool_size=pool_size,  # 连接池大小
            pool_timeout=pool_timeout,  # 池中没有线程最多等待的时间,否则报错
            pool_recycle=pool_recycle,  # 线程连接回收时间（重置）
            future=future,  # 使用异步模式
            echo=__name__ == '__main__',  # 是否打印sql语句
        )

        self.tablename = table_name  # 目标表名
        # 获取ORM基类,同时创建表
        self.Base = copy_db_model(self.engine, table_name, source_table)
        self.pd_conn = self.engine.connect()  # Pandas使用的连接,需要关闭

        # 创建会话
        self.session = sessionmaker(
            bind=self.engine,
            autoflush=True,  # 自动刷新
            # expire_on_commit=True,  # 提交后自动过期
            # class_=AsyncSession, # 异步会话类
        )()

        # 设置表参数字典
        self.params = {attr: getattr(self.Base, attr) for attr in self.Base.columns()}
        self._query = self.session.query(self.Base)  # 基础查询对象
        self.Base.query = self.session.query()  # 为模型添加query属性

        # 获取数据库元数据
        tmp_insp = sqlalchemy.inspect(self.engine)
        self.table_names = tmp_insp.get_schema_names()  # 获取数据库名列表

        self.log.info(f'✅ 成功初始化SqlConnection，表名: {table_name}')

    def __enter__(self):
        """上下文管理器入口 - 返回数据库会话"""
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """上下文管理器出口 - 处理事务提交和会话关闭

        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常回溯

        Returns:
            bool: 是否抑制异常
        """
        if exc_type:
            self.log.warning(f'⚠️ 事务执行失败，正在回滚: {exc_val}')
            self.session.rollback()
        else:
            self.log.debug('🔄 事务执行成功，正在提交')
            self.session.commit()

        self.session.close()
        self.log.debug('🔒 数据库会话已关闭')
        return not exc_type

    def close_connection(self):
        """手动关闭数据库连接"""
        if hasattr(self, 'session') and self.session.is_active:
            self.session.close()
        if hasattr(self, 'pd_conn') and not self.pd_conn.closed:
            self.pd_conn.close()
        self.log.info('数据库连接已手动关闭')

    @property
    def connection_status(self):
        """检查连接状态"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
                return {'status': 'active', 'engine': 'connected'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def drop_db(self, dbname: str | None = None) -> None:
        """删除指定的数据库表

        Args:
            dbname: 要删除的表名
        """
        if not dbname:
            self.log.warning('⚠️ 未提供要删除的表名')
            return

        try:
            drop_sql = f'DROP TABLE IF EXISTS {dbname}'
            self.session.execute(text(drop_sql))
            self.session.commit()
            self.log.info(f'🗑️ 成功删除表: {dbname}')
        except Exception as e:
            self.session.rollback()
            self.log.error(f'❌ 删除表 {dbname} 失败: {e!s}')
            raise

    def run_sql(self, sql: str, params: dict[str, Any] | None = None) -> list[tuple[Any, ...]] | int:
        """执行并提交单条SQL语句

        Args:
            sql: SQL语句字符串
            params: SQL参数, 例如 {':id_val': 10, ':name_val': 'hui'}

        Returns:
            执行SQL的结果 - 查询返回结果集，其他操作返回影响行数
        """
        self.log.debug(f'▶️ 执行SQL: {sql}, 参数: {params}')

        try:
            sql_text = text(sql)
            result = self.session.execute(sql_text, params or {})

            # 判断是否返回结果集
            if getattr(result, 'returns_rows', False):
                query_result = result.all()
                self.log.info(f'✅ SQL查询成功，返回 {len(query_result)} 条记录')
                return query_result

            # 非查询操作返回影响行数
            row_count = getattr(result, 'rowcount', 0)
            self.session.commit()
            self.log.info(f'✅ SQL执行成功，影响行数: {row_count}')
            return row_count
        except Exception as e:
            self.session.rollback()
            self.log.error(f'❌ SQL执行失败: {e!s}')
            raise

    def query(self, where_dict: dict[str, Any] | None = None) -> list[Any]:
        """根据条件查询数据

        Args:
            where_dict: 查询条件字典

        Returns:
            查询结果列表
        """
        where_dict = where_dict or {}
        self.log.debug(f'🔍 查询条件: {where_dict}')

        try:
            query = self._query.filter_by(**where_dict)
            result = query.all()
            self.log.info(f'✅ 查询成功，返回 {len(result)} 条记录')
            return result
        except Exception as e:
            self.log.error(f'❌ 查询失败: {e!s}')
            raise

    def advanced_query(self, filter_conditions=None, order_by=None, limit=None, offset=None, join_tables=None):
        """高级查询功能，支持复杂过滤、排序、分页和连接查询"""
        query = self._query

        # 处理连接查询
        if join_tables:
            for table, condition in join_tables:
                query = query.join(table, condition)

        # 处理过滤条件
        if filter_conditions:
            for condition in filter_conditions:
                query = query.filter(condition)

        # 处理排序
        if order_by:
            query = query.order_by(order_by)

        # 处理分页
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = query.all()
        self.log.info(f'高级查询成功，返回 {len(result)} 条记录')
        return result

    def insert(self, item_list: list[dict[str, Any]], **kwargs) -> int:
        """插入数据到数据库

        Args:
            item_list: 要插入的数据列表或单个数据字典
            **kwargs: 其他参数

        Returns:
            成功插入的记录数量
        """
        # 处理单个数据字典的情况
        items_to_insert = [item_list] if not isinstance(item_list, list) else item_list
        self.log.debug(f'➕ 准备插入 {len(items_to_insert)} 条记录')

        try:
            # 将字典转换为模型实例
            model_instances = [self.Base(**item_dict) for item_dict in items_to_insert]
            self.session.add_all(model_instances)
            self.session.commit()
            self.log.info(f'✅ 成功插入 {len(items_to_insert)} 条记录')
            return len(items_to_insert)
        except Exception as e:
            self.session.rollback()
            self.log.error(f'❌ 插入数据失败: {e!s}')
            return 0

    def update(self, params: dict[str, Any], where_dict: dict[str, Any]) -> int:
        """更新数据库中的数据

        Args:
            params: 要更新的字段和值的字典
            where_dict: 更新条件字典

        Returns:
            成功更新的记录数量
        """
        self.log.debug(f'🔄 更新条件: {where_dict}, 更新内容: {params}')

        try:
            query = self._query.filter_by(**where_dict)
            update_count = query.update(params)
            self.session.commit()
            self.log.info(f'✅ 成功更新 {update_count} 条记录')
            return update_count
        except Exception as e:
            self.session.rollback()
            self.log.error(f'❌ 更新数据失败: {e!s}')
            return 0

    def delete(self, where_dict: dict[str, Any]) -> int:
        """删除数据库中的数据

        Args:
            where_dict: 删除条件字典

        Returns:
            成功删除的记录数量
        """
        self.log.debug(f'🗑️ 删除条件: {where_dict}')

        try:
            query = self._query.filter_by(**where_dict)
            delete_count = query.delete()
            self.session.commit()
            self.log.info(f'✅ 成功删除 {delete_count} 条记录')
            return delete_count
        except Exception as e:
            self.session.rollback()
            self.log.error(f'❌ 删除数据失败: {e!s}')
            return 0

    def select(self, where_dict: dict[str, Any] | None = None, columns_list: Sequence[str] | None = None, raw_count: int | None = None) -> list[Any]:
        """高级查询方法，支持选择指定列和限制返回数量

        Args:
            where_dict: 查询条件字典
            columns_list: 要查询的列名列表
            raw_count: 限制返回的记录数量

        Returns:
            查询结果列表
        """
        # 构建查询列
        query_columns = [self.params.get(key) for key in columns_list] if isinstance(columns_list, Sequence) and len(columns_list) > 0 else [self.Base]

        self.log.debug(f'🔍 高级查询 - 列: {columns_list}, 条件: {where_dict}, 限制: {raw_count}')

        try:
            query = self.session.query(*query_columns)

            # 添加查询条件
            if where_dict is not None:
                query = query.filter_by(**where_dict)

            # 添加数量限制
            if raw_count is not None:
                query = query.limit(raw_count)

            result = query.all()
            self.log.info(f'✅ 高级查询成功，返回 {len(result)} 条记录')
            return result
        except Exception as e:
            self.log.error(f'❌ 高级查询失败: {e!s}')
            raise

    def from_statement(self, sql: str, where_dict: dict[str, Any] | None = None) -> list[Any]:
        """执行原生SQL语句查询

        Args:
            sql: 原生SQL查询语句
            where_dict: SQL参数字典

        Returns:
            查询结果列表
        """
        self.log.debug(f'▶️ 执行原生SQL: {sql}, 参数: {where_dict}')

        try:
            sql_text = text(sql)
            query = self._query.from_statement(sql_text)

            # 添加参数
            result = query.params(**where_dict).all() if where_dict else query.all()

            self.log.info(f'✅ 原生SQL查询成功，返回 {len(result)} 条记录')
            return result
        except Exception as e:
            self.log.error(f'❌ 原生SQL查询失败: {e!s}')
            raise

    def filter_by(self, where_dict: dict[str, Any], raw_count: int | None = None) -> list[Any]:
        """简单条件查询，仅支持等值和AND逻辑

        Args:
            where_dict: 查询条件字典
            raw_count: 限制返回的记录数量

        Returns:
            查询结果列表
        """
        self.log.debug(f'🔍 条件查询: {where_dict}, 限制: {raw_count}')

        try:
            query = self._query.filter_by(**where_dict)

            # 添加数量限制
            if raw_count is not None:
                query = query.limit(raw_count)

            result = query.all()
            self.log.info(f'✅ 条件查询成功，返回 {len(result)} 条记录')
            return result
        except Exception as e:
            self.log.error(f'❌ 条件查询失败: {e!s}')
            raise

    def pd_get_dict(self, table_name: str) -> list[dict[str, Any]] | bool:
        """使用Pandas读取表数据并返回字典列表

        Args:
            table_name: 要读取的表名

        Returns:
            数据字典列表，如果没有数据则返回False
        """
        self.log.debug(f'📊 使用Pandas读取表: {table_name}')

        try:
            result = pandas.read_sql_table(table_name, con=self.pd_conn)
            data_dict = result.to_dict(orient='records')

            if data_dict:
                self.log.info(f'✅ Pandas读取成功，返回 {len(data_dict)} 条记录')
                return data_dict

            self.log.warning(f'⚠️ 表 {table_name} 中没有数据')
            return False
        except Exception as e:
            self.log.error(f'❌ Pandas读取表 {table_name} 失败: {e!s}')
            raise

    def pd_get_list(self, table_name: str, columns: list[str]) -> list[list[Any]] | bool:
        """使用Pandas读取表指定列并返回去重后的列表

        Args:
            table_name: 要读取的表名
            columns: 要读取的列名列表

        Returns:
            列表数据，如果没有数据则返回False
        """
        self.log.debug(f'📊 使用Pandas读取表 {table_name} 的列: {columns}')

        try:
            result = pandas.read_sql_table(table_name, con=self.pd_conn)
            pd_list = result[columns].drop_duplicates().values.tolist()

            if pd_list:
                self.log.info(f'✅ Pandas列读取成功，返回 {len(pd_list)} 条去重记录')
                return pd_list

            self.log.warning(f'⚠️ 表 {table_name} 的列 {columns} 中没有数据')
            return False
        except Exception as e:
            self.log.error(f'❌ Pandas读取表 {table_name} 的列 {columns} 失败: {e!s}')
            raise


def create_sqlconnection(db_key: str = 'default', table_name: str | None = None, source_table: str | None = None) -> SqlConnection:
    """创建数据库连接的工厂函数

    提供一种便捷的方式创建SqlConnection实例，自动从配置中获取连接信息。

    Args:
        db_key: 数据库配置键名，对应DB_CFG中的配置项，默认为'default'
        table_name: 目标数据表名
        source_table: 源模型表名（用于模型复制）

    Returns:
        SqlConnection: 配置好的SqlConnection实例

    Raises:
        ValueError: 当配置键不存在或无效时抛出
    """
    log.info(f'▶️ 正在创建SqlConnection实例，配置键: {db_key}，表名: {table_name}')

    try:
        conn_url = connect_str(db_key)
        return SqlConnection(conn_url, table_name, source_table)
    except Exception as e:
        log.error(f'❌ 创建SqlConnection实例失败: {e!s}')
        raise


if __name__ == '__main__':
    """模块测试代码"""
    log.info('🚀 开始测试SqlConnection模块')

    # 测试数据
    query_list = ['select * from users2 where id = 1', 'select * from users2']
    item = [
        {
            'username': '刘新',
            'password': '234567',
            '手机': '13910118122',
            '代理人编码': '10005393',
            '会员级别': 'SSS',
            '会员到期日': '9999-12-31 00:00:00',
        }
    ]

    try:
        # 创建数据库连接
        ASO = create_sqlconnection('TXbx', 'users2', 'users_model')
        log.info('✅ 成功创建SqlConnection实例')

        # 测试查询功能
        res = ASO.query()
        log.info(f'📋 查询结果数量: {len(res)}')
        log.debug(f'📋 模型转换结果: {ASO.Base.make_dict(res)}')

        # 测试条件查询
        filtered_res = ASO.filter_by({'ID': 1})
        log.info(f'🔍 条件查询结果数量: {len(filtered_res)}')

        # 测试原生SQL查询
        raw_sql_res = ASO.from_statement('select * from users2', {'ID': 2})
        log.info(f'🔧 原生SQL查询结果数量: {len(raw_sql_res)}')

        # 以下代码可以根据需要取消注释进行测试
        # # 测试插入
        # insert_count = ASO.insert(item)
        # log.info(f'➕ 插入记录数量: {insert_count}')
        #
        # # 测试更新
        # update_count = ASO.update(value={"username": "刘澈"}, conds={"ID": 4})
        # log.info(f'🔄 更新记录数量: {update_count}')
        #
        # # 测试删除
        # delete_count = ASO.delete({"ID": 3})
        # log.info(f'🗑️ 删除记录数量: {delete_count}')

    except Exception as e:
        log.error(f'❌ 测试失败: {e!s}')
