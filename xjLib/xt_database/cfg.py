# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-25 16:44:26
FilePath     : /CODE/xjLib/xt_database/cfg.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from xt_enum import BaseEnum


class DB_CFG(BaseEnum):
    TXbook = (
        {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "user": "sandorn",
            "password": "123456",
            "db": "biqukan",
            "charset": "utf8mb4",
        },
    )

    TXbx = (
        {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "user": "sandorn",
            "password": "123456",
            "db": "bxflb",
            "charset": "utf8mb4",
        },
    )
    redis = {"type": "redis", "host": "127.0.0.1", "port": 6379, "db": 4}
    Jkdoc = (
        {
            "type": "mysql",
            "host": "localhost",
            "port": 3306,
            "user": "sandorn",
            "password": "123456",
            "db": "Jkdoc",
            "charset": "utf8mb4",
        },
    )

    default = TXbx


class Driver_Map(BaseEnum):
    mysql = (
        {
            "OurSQL": "mysql+oursql",
            "aiomysql": "mysql+aiomysql",
            "connector": "mysql+mysqlconnector",
            "mysqldb": "mysql+mysqldb",
            "pymysql": "mysql+pymysql",
            "mysql": "mysql",
        },
    )
    PostgreSQL = (
        {
            "pg8000": "postgresql+pg8000",
            "psycopg2": "postgresql+psycopg2",
            "postgresql": "postgresql+psycopg2",
        },
    )
    Oracle = ({"oracle": "oracle", "cx": "oracle+cx_oracle"},)
    SQLServer = (
        {
            "pyodbc": "mssql+pyodbc",
            "pymssql": "mssql+pymssql",
            "sqlserver": "mssql+pymssql",
        },
    )
    SQLite = ({"sqlite": "sqlite"},)
    access = ({"access": "access+pyodbc"},)
    monetdb = ({"monetdb": "monetdb", "lite": "monetdb+lite"},)


def connect_str(key, odbc=None):
    if not hasattr(DB_CFG, key):
        raise ValueError(f"错误提示:检查数据库配置:{key}")
    cfg = DB_CFG[key].value
    db_types = cfg["type"]
    odbc = db_types if odbc is None else odbc

    link_str = f"{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['db']}?charset={cfg['charset']}"

    _tmp_map = Driver_Map[db_types].value
    drivers_str = _tmp_map.get(odbc, _tmp_map.get(db_types))
    return f"{drivers_str}://{link_str}"


if __name__ == "__main__":
    print(connect_str("TXbook"))

    connector2 = connect_str("TXbook", "connector")
    print(connector2)
