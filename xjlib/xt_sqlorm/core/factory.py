# !/usr/bin/env python
"""
==============================================================
Description  : SQL数据库工厂函数模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-22 10:40:00
LastEditTime : 2025-09-23 10:30:00
FilePath     : d:/CODE/xjlib/xt_sqlorm/db/factory.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- create_sqlconnection: 创建数据库连接对象的工厂函数
- create_orm_operations: 创建ORM操作对象的工厂函数
- reflect_table: 反射数据库中已存在的表并创建对应的模型类
- copy_table_model: 复制模型类
- create_async_sqlconnection: 创建异步数据库连接对象的工厂函数
- create_async_orm_operations: 创建异步ORM操作对象的工厂函数

本模块采用工厂模式设计，提供了统一的接口来创建和管理数据库连接及ORM操作对象，
支持灵活的配置选项和错误处理机制。
==============================================================
"""

from __future__ import annotations

import re
import subprocess  # noqa: S404
from typing import Any

from sqlalchemy import Table, inspect
from xt_database.cfg import connect_str
from xt_sqlorm.core.async_connection import AsyncSqlConnection
from xt_sqlorm.core.async_operations import AsyncOrmOperations
from xt_sqlorm.core.connection import SqlConnection
from xt_sqlorm.core.operations import OrmOperations
from xt_sqlorm.models.base import BaseModel
from xt_wraps.log import create_basemsg, log_wraps, mylog as log


@log_wraps
def create_sqlconnection(
    db_key: str = 'default',
    url: str | None = None,
    **kwargs: Any,
) -> SqlConnection:
    """
    创建数据库连接对象的工厂函数

    根据提供的配置参数创建并返回一个SqlConnection实例，支持从配置文件获取连接信息
    或直接指定连接URL。自动配置连接池参数并验证连接有效性。

    Args:
        db_key: 数据库配置键，用于从配置文件中获取连接信息，默认为'default'
        url: 数据库连接URL，格式为 "dialect+driver://username:password@host:port/database"。
            如果提供此参数，将优先使用此URL而非从配置文件获取
        echo: 是否打印SQL语句及其执行细节，默认为False
        pool_size: 连接池维护的固定连接数，默认为10
        max_overflow: 连接池允许的最大额外连接数，默认为20
        pool_timeout: 获取连接的超时时间（秒），默认为30
        pool_recycle: 连接自动回收的时间间隔（秒），默认为3600
        **conn_kwargs: 其他传递给SQLAlchemy create_engine的参数

    Returns:
        配置完成并已验证连接的SqlConnection实例

    Raises:
        ValueError: 当无法获取有效的数据库连接URL时
        SQLAlchemyError: 当创建数据库连接失败时
        Exception: 当连接测试失败或发生其他意外错误时
    """
    # 获取数据库连接URL
    if not url:
        url = connect_str(db_key)

    db_conn = SqlConnection(url=url, **kwargs)
    if db_conn.ping():
        return db_conn
    return None


@log_wraps
def create_orm_operations(
    source_model: type[BaseModel] | str,
    db_conn: SqlConnection | None = None,
    copy_name: str | None = None,
    **conn_kwargs: Any,
) -> OrmOperations[BaseModel]:
    """
    创建ORM操作对象的工厂函数

    根据提供的ORM模型类或表名创建对应的OrmOperations实例，支持直接提供数据库连接
    或自动创建新的连接。

    Args:
        source_model: ORM模型类或数据库表名
        db_conn: 数据库连接对象，如果为None且提供了conn_kwargs，则创建新连接
        copy_name: 如果要复制表结构，指定新表名
        **conn_kwargs: 如果没有提供db_conn，这些参数将传递给create_sqlconnection

    Returns:
        针对指定模型的OrmOperations实例

    Raises:
        ValueError: 当提供的数据模型类型无效时
        SQLAlchemyError: 当创建ORM操作失败时
        Exception: 当发生其他意外错误时
    """
    # 如果没有提供数据库连接，则创建一个新的
    if db_conn is None and conn_kwargs:
        db_conn = create_sqlconnection(**conn_kwargs)

    # 验证数据模型类型
    is_valid_type = (isinstance(source_model, type) and issubclass(source_model, BaseModel)) or isinstance(source_model, str)

    if not is_valid_type:
        error_msg = f'无效的数据模型类型: {type(source_model).__name__}'
        log.warning(f'{create_basemsg(create_orm_operations)} | {error_msg}')
        raise ValueError(error_msg)

    # 处理不同类型的数据模型
    if isinstance(source_model, str) and copy_name:
        model_class = copy_table_model(source_model, db_conn, copy_name)
    elif isinstance(source_model, str):
        model_class = reflect_table(source_model, db_conn)
    else:
        model_class = source_model
        # 使用 inspector.has_table() 检查表是否存在
        inspector = inspect(db_conn.engine)
        table_name = model_class.__tablename__

        if not inspector.has_table(table_name):
            model_class.__table__.create(bind=db_conn.engine, checkfirst=True)
            log.ok(f'{create_basemsg(create_orm_operations)} | 成功创建表: {table_name}')

    # 创建ORM操作实例
    orm_ops = OrmOperations(model_class, db_conn)
    # 修复日志记录，使用正确的属性名  类名：__name__ ，表名： __tablename__
    source_name = source_model if isinstance(source_model, str) else source_model.__tablename__
    log.ok(f'{create_basemsg(create_orm_operations)} | 创建ORM操作: {model_class.__name__} | 表: {model_class.__tablename__} | 源: {source_name}')

    return orm_ops


@log_wraps
def reflect_table(
    source_table_name: str,
    db_conn: SqlConnection | None = None,
    **conn_kwargs: Any,
) -> type[BaseModel]:
    """
    反射数据库中已存在的表并创建对应的模型类

    通过SQLAlchemy的反射机制，动态创建一个与数据库中现有表结构匹配的模型类。

    Args:
        source_table_name: 数据库中已存在的表名
        db_conn: 数据库连接对象，如果为None则创建新连接
        **conn_kwargs: 如果没有提供db_conn，这些参数将传递给create_sqlconnection

    Returns:
        与指定表结构匹配的模型类

    Raises:
        ValueError: 当表名不存在或连接无效时
        SQLAlchemyError: 当反射过程中发生SQL错误时
        Exception: 当发生其他意外错误时
    """
    # 确保有有效的数据库连接
    if db_conn is None:
        db_conn = create_sqlconnection(**conn_kwargs)

    # 检查源表是否存在
    inspector = inspect(db_conn.engine)
    if not inspector.has_table(source_table_name):
        raise ValueError(f'数据库中不存在源表: {source_table_name}')

    # 只反射指定的表以提高性能
    log.start(f'{create_basemsg(reflect_table)} | 正在反射数据库表: {source_table_name}')
    BaseModel.metadata.reflect(bind=db_conn.engine, only=[source_table_name])

    # 获取源表对象
    source_table_obj = BaseModel.metadata.tables[source_table_name]

    # 创建模型类，继承自BaseModel
    model_name = source_table_name.title().replace('_', '')
    table_model = type(
        model_name,
        (BaseModel,),
        {
            '__table__': source_table_obj,
            '__tablename__': source_table_name,  # 添加这一行
        },
    )
    log.ok(f'{create_basemsg(reflect_table)} | 成功反射表: {source_table_name}，创建模型类: {model_name}')

    return table_model


@log_wraps
def copy_table_model(
    source_table_name: str,
    db_conn: SqlConnection | None = None,
    new_table_name: str | None = None,
    table_args: dict[str, Any] | None = None,
    **conn_kwargs: Any,
) -> type[BaseModel]:
    """
    轻量级表复制，支持结构修改

    复制源表结构创建新表，并返回对应的模型类。

    Args:
        source_table_name: 源表名
        db_conn: 数据库连接对象，如果为None则创建新连接
        new_table_name: 新表名，必须提供
        table_args: 表参数，用于修改表结构
        **conn_kwargs: 如果没有提供db_conn，这些参数将传递给create_sqlconnection

    Returns:
        新表对应的模型类

    Raises:
        ValueError: 当参数无效或表不存在时
        SQLAlchemyError: 当表操作过程中发生SQL错误时
        Exception: 当发生其他意外错误时
    """
    if not new_table_name:
        raise ValueError('复制表时必须提供新表名')

    # 确保有有效的数据库连接
    if db_conn is None:
        db_conn = create_sqlconnection(**conn_kwargs)

    # 检查源表是否存在
    inspector = inspect(db_conn.engine)
    if not inspector.has_table(source_table_name):
        raise ValueError(f'数据库中不存在源表: {source_table_name}')

    # 加载原表结构
    old_table = Table(
        source_table_name,
        BaseModel.metadata,
        autoload_with=db_conn.engine,
        extend_existing=True,
    )

    # 创建新表（可修改结构）
    new_table = old_table.tometadata(
        BaseModel.metadata,
        name=new_table_name,
        schema=old_table.schema,
        **(table_args or {}),  # 支持传入额外参数（如列修改）
    )

    # 仅当表不存在时创建
    if not inspector.has_table(new_table_name):
        new_table.create(bind=db_conn.engine, checkfirst=True)
        log.ok(f'✅ {create_basemsg(copy_table_model)} | 成功创建表: {new_table_name}')
    else:
        log.warning(f'ℹ️ {create_basemsg(copy_table_model)} | 表已存在，跳过创建: {new_table_name}')

    # 创建模型类
    model_name = new_table_name.title().replace('_', '')
    table_model = type(model_name, (BaseModel,), {'__table__': new_table})
    table_model = type(
        model_name,
        (BaseModel,),
        {
            '__table__': new_table,
            '__tablename__': new_table_name,  # 添加这一行
        },
    )
    log.ok(f'{create_basemsg(copy_table_model)} | 成功复制表: {source_table_name} 为 {new_table_name}，创建模型类: {model_name}')

    return table_model


@log_wraps
def _validate_tablename(tablename: str) -> None:
    """验证表名的有效性，防止SQL注入和命令注入。"""
    # 只允许字母、数字、下划线，防止SQL注入和命令注入
    if not tablename or not isinstance(tablename, str) or not re.match(r'^[a-zA-Z0-9_]+$', tablename):
        raise ValueError(f'无效的表名: {tablename}，表名只能包含字母、数字和下划线')


@log_wraps
def _build_command_args(url: str, tablename: str, output_file: str, **kwargs: Any) -> list[str]:
    """构建sqlacodegen命令参数列表，确保参数安全性。"""
    # 构建命令参数列表
    cmd_args = ['sqlacodegen', url, '--tables', tablename, f'--outfile={output_file}']

    # 添加额外的sqlacodegen参数
    for key, value in kwargs.items():
        # 验证参数名，防止注入
        if not re.match(r'^[a-zA-Z0-9_-]+$', key):
            continue

        if value is True:
            cmd_args.append(f'--{key}')
        elif value is not False and value is not None:
            # 对值进行简单验证，防止注入
            safe_value = str(value).replace('\\', '').replace("'", '').replace('"', '')
            cmd_args.append(f'--{key}={safe_value}')

    return cmd_args


@log_wraps
def _execute_command(cmd_args: list[str], echo: bool = False) -> subprocess.CompletedProcess:
    """执行命令并返回结果，包含日志记录。"""
    if echo:
        # 打印命令时隐藏URL中的敏感信息
        safe_cmd = []
        for arg in cmd_args:
            if '://' in arg and ':' in arg.split('://')[1]:
                # 隐藏URL中的密码信息
                parts = arg.split('://')
                credentials_and_rest = parts[1].split('@')
                if len(credentials_and_rest) > 1:
                    credentials = credentials_and_rest[0].split(':')[0] + ':********'
                    safe_cmd.append(f'{parts[0]}://{credentials}@{credentials_and_rest[1]}')
                else:
                    safe_cmd.append(arg)
            else:
                safe_cmd.append(arg)
        log.info(f'{create_basemsg(_execute_command)} | 执行命令: {" ".join(safe_cmd)}')

    # 执行命令，不使用shell=True以提高安全性
    # 注意：我们已经通过_build_command_args函数对所有命令参数进行了安全验证
    return subprocess.run(cmd_args, capture_output=True, text=True, check=False)  # noqa: S603


@log_wraps
def db_to_model(
    tablename: str,
    db_key: str = 'default',
    url: str = '',
    output_file: str | None = None,
    echo: bool = False,
    **kwargs: Any,
) -> int:
    """
    使用sqlacodegen将数据库表转换为SQLAlchemy模型类文件

    调用外部sqlacodegen工具，根据数据库连接信息和表名生成对应的SQLAlchemy模型类
    代码文件，支持自定义输出路径和额外的sqlacodegen参数。

    Args:
        tablename: 要转换的数据库表名
        db_key: 数据库配置键，用于从配置文件中获取连接信息，默认为'default'
        url: 数据库连接URL，如果提供此参数，将优先使用此URL而非从配置文件获取
        output_file: 输出文件路径，默认为None（使用tablename_db.py）
        echo: 是否打印详细执行信息，默认为False
        **kwargs: 传递给sqlacodegen的额外参数，格式为key=value

    Returns:
        命令执行结果的返回码，0表示成功

    Raises:
        ValueError: 当表名无效或无法获取数据库连接URL时
        FileNotFoundError: 当sqlacodegen工具未安装时
        Exception: 当执行过程中发生其他错误时
    """
    try:
        # 输入验证
        _validate_tablename(tablename)

        # 获取数据库连接URL
        if not url:
            url = connect_str(db_key)
            log.start(f'{create_basemsg(db_to_model)} | 从配置获取连接信息，配置键: {db_key}')
        else:
            log.start(f'{create_basemsg(db_to_model)} | 使用自定义连接URL')

        # 确定输出文件路径
        if output_file is None:
            output_file = f'{tablename}_data_model.py'

        # 构建命令参数列表
        cmd_args = _build_command_args(url, tablename, output_file, **kwargs)

        # 执行命令
        result = _execute_command(cmd_args, echo)

        # 记录命令输出和结果
        if result.stdout and echo:
            log.info(f'{create_basemsg(db_to_model)} | 命令输出: {result.stdout.strip()}')

        if result.stderr:
            log.warning(f'{create_basemsg(db_to_model)} | 命令错误输出: {result.stderr.strip()}')

        if result.returncode == 0:
            log.ok(f'{create_basemsg(db_to_model)} | 成功生成模型文件: {output_file}')
        else:
            log.fail(f'{create_basemsg(db_to_model)} | 生成模型文件失败，返回码: {result.returncode}')

        return result.returncode

    except FileNotFoundError as e:
        error_msg = 'sqlacodegen工具未安装，请使用 pip install sqlacodegen 进行安装'
        log.error(f'{create_basemsg(db_to_model)} | {error_msg}')
        raise FileNotFoundError(error_msg) from e

    except Exception as err:
        error_msg = f'生成模型文件时发生错误: {err!s}'
        log.error(f'{create_basemsg(db_to_model)} | {error_msg}')
        raise Exception(error_msg) from err


@log_wraps
async def create_async_sqlconnection(
    db_key: str = 'default',
    url: str | None = None,
    echo: bool = False,
    pool_size: int = 10,
    max_overflow: int = 20,
    pool_timeout: int = 30,
    pool_recycle: int = 3600,
    **conn_kwargs: Any,
) -> AsyncSqlConnection:
    """
    创建异步数据库连接对象的工厂函数

    根据提供的配置参数创建并返回一个AsyncSqlConnection实例，支持从配置文件获取连接信息
    或直接指定连接URL。自动配置连接池参数并验证连接有效性。

    Args:
        db_key: 数据库配置键，用于从配置文件中获取连接信息，默认为'default'
        url: 数据库连接URL，格式为 "dialect+async_driver://username:password@host:port/database"。
            如果提供此参数，将优先使用此URL而非从配置文件获取
        echo: 是否打印SQL语句及其执行细节，默认为False
        pool_size: 连接池维护的固定连接数，默认为10
        max_overflow: 连接池允许的最大额外连接数，默认为20
        pool_timeout: 获取连接的超时时间（秒），默认为30
        pool_recycle: 连接自动回收的时间间隔（秒），默认为3600
        **conn_kwargs: 其他传递给SQLAlchemy create_async_engine的参数

    Returns:
        配置完成并已验证连接的AsyncSqlConnection实例

    Raises:
        ValueError: 当无法获取有效的数据库连接URL时
        SQLAlchemyError: 当创建数据库连接失败时
        Exception: 当连接测试失败或发生其他意外错误时
    """
    # 获取数据库连接URL
    if not url:
        url = connect_str(db_key)

    # 确保URL使用异步驱动
    if 'async' not in url and 'aiosqlite' not in url:
        # 转换为异步URL（简单实现，实际可能需要更复杂的逻辑）
        if 'sqlite:///' in url:
            url = url.replace('sqlite:///', 'sqlite+aiosqlite:///')
        elif 'mysql://' in url:
            url = url.replace('mysql://', 'mysql+aiomysql://')
        elif 'postgresql://' in url:
            url = url.replace('postgresql://', 'postgresql+asyncpg://')

    db_conn = AsyncSqlConnection(url=url, echo=echo, pool_size=pool_size, max_overflow=max_overflow, pool_timeout=pool_timeout, pool_recycle=pool_recycle, **conn_kwargs)
    await db_conn.initialize()
    if await db_conn.ping():
        return db_conn
    return None


@log_wraps
async def create_async_orm_operations(
    source_model: type[BaseModel] | str,
    db_conn: AsyncSqlConnection | None = None,
    copy_name: str | None = None,
    **conn_kwargs: Any,
) -> AsyncOrmOperations[BaseModel]:
    """
    创建异步ORM操作对象的工厂函数

    根据提供的ORM模型类或表名创建对应的AsyncOrmOperations实例，支持直接提供数据库连接
    或自动创建新的连接。

    Args:
        source_model: ORM模型类或数据库表名
        db_conn: 异步数据库连接对象，如果为None且提供了conn_kwargs，则创建新连接
        copy_name: 如果要复制表结构，指定新表名
        **conn_kwargs: 如果没有提供db_conn，这些参数将传递给create_async_sqlconnection

    Returns:
        针对指定模型的AsyncOrmOperations实例

    Raises:
        ValueError: 当提供的数据模型类型无效时
        SQLAlchemyError: 当创建ORM操作失败时
        Exception: 当发生其他意外错误时
    """
    # 如果没有提供数据库连接，则创建一个新的
    if db_conn is None and conn_kwargs:
        db_conn = await create_async_sqlconnection(**conn_kwargs)

    if db_conn is None:
        raise ValueError('无法创建或获取有效的数据库连接')

    # 验证数据模型类型
    is_valid_type = (isinstance(source_model, type) and issubclass(source_model, BaseModel)) or isinstance(source_model, str)

    if not is_valid_type:
        error_msg = f'无效的数据模型类型: {type(source_model).__name__}'
        log.warning(f'{create_basemsg(create_async_orm_operations)} | {error_msg}')
        raise ValueError(error_msg)

    # 处理不同类型的数据模型
    if isinstance(source_model, str):
        # 对于异步操作，我们需要特殊处理表反射
        # 这里简化实现，实际项目可能需要更复杂的异步反射逻辑
        model_class = await reflect_table_async(source_model, db_conn)
    else:
        model_class = source_model
        # 使用异步检查器检查表是否存在
        inspector = inspect(db_conn.engine.sync_engine)
        table_name = model_class.__tablename__
        if not inspector.has_table(table_name):
            # 异步创建表
            async with db_conn.engine.begin() as conn:
                await conn.run_sync(model_class.__table__.create, checkfirst=True)
            log.ok(f'{create_basemsg(create_async_orm_operations)} | 成功创建表: {table_name}')
        else:
            log.warning(f'{create_basemsg(create_async_orm_operations)} | 表已存在，跳过创建: {table_name}')

    # 创建异步ORM操作实例
    orm_ops = AsyncOrmOperations(model_class, db_conn)
    source_name = source_model if isinstance(source_model, str) else source_model.__tablename__
    log.ok(f'{create_basemsg(create_async_orm_operations)} | 创建异步ORM操作: {model_class.__name__} | 表: {model_class.__tablename__} | 源: {source_name}')

    return orm_ops


@log_wraps
async def reflect_table_async(
    source_table_name: str,
    db_conn: AsyncSqlConnection,
) -> type[BaseModel]:
    """
    异步反射数据库中已存在的表并创建对应的模型类

    通过SQLAlchemy的反射机制，动态创建一个与数据库中现有表结构匹配的模型类。

    Args:
        source_table_name: 数据库中已存在的表名
        db_conn: 异步数据库连接对象

    Returns:
        与指定表结构匹配的模型类

    Raises:
        ValueError: 当表名不存在或连接无效时
        SQLAlchemyError: 当反射过程中发生SQL错误时
        Exception: 当发生其他意外错误时
    """
    # 检查源表是否存在
    inspector = inspect(db_conn.engine.sync_engine)
    if not inspector.has_table(source_table_name):
        raise ValueError(f'数据库中不存在源表: {source_table_name}')

    log.start(f'{create_basemsg(reflect_table_async)} | 正在异步反射数据库表: {source_table_name}')

    # 使用同步引擎进行反射（简化实现）
    await db_conn.engine.run_sync(lambda engine: BaseModel.metadata.reflect(engine, only=[source_table_name]))

    # 获取源表对象
    source_table_obj = BaseModel.metadata.tables[source_table_name]

    # 创建模型类，继承自BaseModel
    model_name = source_table_name.title().replace('_', '')
    table_model = type(
        model_name,
        (BaseModel,),
        {
            '__table__': source_table_obj,
            '__tablename__': source_table_name,
        },
    )

    log.ok(f'{create_basemsg(reflect_table_async)} | 成功异步反射表: {source_table_name}，创建模型类: {model_name}')
    return table_model


if __name__ == '__main__':
    """模块主函数，用于演示和测试db_to_model功能。"""
    import argparse

    from xt_wraps.log import mylog as loger

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将数据库表转换为SQLAlchemy模型类文件')
    parser.add_argument('tablename', nargs='?', default='users2', help='要转换的数据库表名')
    parser.add_argument('--db-key', default='default', help='数据库配置键，默认为"default"')
    parser.add_argument('--output', default=None, help='输出文件路径，默认为tablename_db.py')
    parser.add_argument('--echo', action='store_true', help='打印详细执行信息')

    # 解析命令行参数
    args = parser.parse_args()

    # 如果没有提供表名，显示帮助信息
    if not args.tablename:
        loger.start('db_to_model工具使用帮助')
        loger.error('请提供有效的表名')
        loger.info('\n使用示例:')
        loger.info(f'  python {__file__} your_table_name')
        loger.info(f'  python {__file__} your_table_name --db-key=production')
        loger.info(f'  python {__file__} your_table_name --output=custom_model.py --echo')
        loger.info('\n注意：')
        loger.info('  1. 确保指定的表存在于数据库中')
        loger.info('  2. 确保已安装sqlacodegen: pip install sqlacodegen')
        loger.info('  3. 确保数据库配置正确')
        loger.stop()
        # 仍然需要显示标准的帮助信息
        parser.print_help()
    else:
        try:
            # 执行db_to_model函数
            result = db_to_model(args.tablename, db_key=args.db_key, output_file=args.output, echo=args.echo)

            # 根据结果显示相应信息
            if result == 0:
                loger.ok('模型文件已生成')
            else:
                loger.fail(f'生成模型文件时出错，返回码: {result}')
                loger.info('请检查表名是否正确，以及数据库连接是否正常')

        except Exception as e:
            loger.fail(f'错误：{e!s}')
            loger.info('请检查您的配置和参数是否正确')
