# !/usr/bin/env python
"""
==============================================================
Description  : 数据库配置模块 - 提供统一的数据库连接配置管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-14 16:00:00
FilePath     : /CODE/xjlib/xt_database/cfg.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- DB_CFG: 数据库连接配置枚举类，集中管理所有数据库连接信息
- Driver_Map: 数据库驱动映射枚举类，管理不同数据库类型的驱动配置
- connect_str: 生成数据库连接字符串的工具函数

主要特性:
- 集中式配置管理，便于统一维护和修改数据库连接信息
- 支持多种数据库类型(MySQL、PostgreSQL、Oracle等)
- 支持多种数据库驱动选择
- 统一的连接字符串生成机制
- 完整的类型注解，支持Python 3.10+现代语法规范
==============================================================
"""

from __future__ import annotations

from xt_enum import BaseEnum


class DB_CFG(BaseEnum):  # noqa
    """数据库配置枚举类，集中管理所有数据库连接配置"""

    TXbook = (
        {
            'type': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'user': 'sandorn',
            'password': '123456',
            'db': 'biqukan',
            'charset': 'utf8mb4',
        },
    )
    TXbx = (
        {
            'type': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'user': 'sandorn',
            'password': '123456',
            'db': 'bxflb',
            'charset': 'utf8mb4',
        },
    )
    redis = ({'type': 'redis', 'host': 'localhost', 'port': 6379, 'db': 4},)
    Jkdoc = (
        {
            'type': 'mysql',
            'host': 'localhost',
            'port': 3306,
            'user': 'sandorn',
            'password': '123456',
            'db': 'Jkdoc',
            'charset': 'utf8mb4',
        },
    )

    default = TXbx


class Driver_Map(BaseEnum):  # noqa
    """数据库驱动映射枚举类，管理不同数据库类型的驱动配置"""

    mysql = (
        {
            'OurSQL': 'mysql+oursql',
            'aiomysql': 'mysql+aiomysql',
            'connector': 'mysql+mysqlconnector',
            'mysqldb': 'mysql+mysqldb',
            'pymysql': 'mysql+pymysql',
            'mysql': 'mysql',
        },
    )
    PostgreSQL = (
        {
            'pg8000': 'postgresql+pg8000',
            'psycopg2': 'postgresql+psycopg2',
            'postgresql': 'postgresql+psycopg2',
        },
    )
    Oracle = ({'oracle': 'oracle', 'cx': 'oracle+cx_oracle'},)
    SQLServer = (
        {
            'pyodbc': 'mssql+pyodbc',
            'pymssql': 'mssql+pymssql',
            'sqlserver': 'mssql+pymssql',
        },
    )
    SQLite = ({'sqlite': 'sqlite'},)
    access = ({'access': 'access+pyodbc'},)
    monetdb = ({'monetdb': 'monetdb', 'lite': 'monetdb+lite'},)


def connect_str(key: str, odbc: str | None = None) -> str:
    """生成数据库连接字符串的工具函数

    Args:
        key: 数据库配置键名，对应DB_CFG中的配置项
        odbc: 可选，指定数据库驱动类型，默认使用配置中的数据库类型

    Returns:
        str: 格式化的数据库连接字符串

    Raises:
        ValueError: 当配置键不存在时抛出
        KeyError: 当配置中缺少必要字段时抛出

    Example:
        >>> # 1. 使用默认驱动
        >>> conn_str = connect_str('TXbook')
        >>> # 返回: mysql://sandorn:123456@localhost:3306/biqukan?charset=utf8mb4
        >>> # 2. 指定驱动
        >>> conn_str = connect_str('TXbook', 'connector')
        >>> # 返回: mysql+mysqlconnector://sandorn:123456@localhost:3306/biqukan?charset=utf8mb4
        >>> # 3. 使用默认配置
        >>> conn_str = connect_str('default')
        >>> # 返回: mysql://sandorn:123456@localhost:3306/bxflb?charset=utf8mb4
    """
    if not hasattr(DB_CFG, key):
        raise ValueError(f'错误提示:检查数据库配置:{key}')

    cfg = DB_CFG[key].value
    db_types = cfg['type']
    odbc = db_types if odbc is None else odbc

    # 构建连接字符串基础部分
    try:
        link_str = f'{cfg["user"]}:{cfg["password"]}@{cfg["host"]}:{cfg["port"]}/{cfg["db"]}?charset={cfg["charset"]}'
    except KeyError as e:
        raise KeyError(f'配置中缺少必要字段: {e}') from e

    # 获取驱动字符串
    try:
        tmp_map = Driver_Map[db_types].value
        drivers_str = tmp_map.get(odbc, tmp_map.get(db_types))
    except KeyError as e:
        raise KeyError(f'不支持的数据库类型: {db_types}') from e

    return f'{drivers_str}://{link_str}'


if __name__ == '__main__':
    """示例代码，展示connect_str函数的使用方式"""
    # 使用默认驱动
    print(connect_str('TXbook'))

    # 指定特定驱动
    connector2 = connect_str('TXbook', 'connector')
    print(connector2)

    # 使用默认配置
    print(connect_str('default'))
