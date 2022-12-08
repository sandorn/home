# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@==============================================================
@Descripttion : None
@Develop      : VSCode
@Author       : Even.Sand
@Contact      : sandorn@163.com
@Date         : 2020-02-14 20:38:57
FilePath     : /xjLib/xt_DAO/dbconf.PY
LastEditTime : 2020-08-24 13:56:46
@Github       : https://github.com/sandorn/home
#==============================================================

Navicat
sandorn@163.com
Sand@2808
'''

DB_CONFIG = {
    'TXbook': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'biqukan',
        'charset': 'utf8mb4'
    },
    'TXbx': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'bxflb',
        'charset': 'utf8mb4'
    },
    'TX_Root': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'root',
        'password': 'Sand2808',
        'db': 'bxflb',
        'charset': 'utf8mb4'
    },
    'db4': {
        'type': 'mysql',
        'host': 'db4free.net',
        'port': 3306,
        'user': 'sandorn',
        'password': 'eeM3sh4KPkp4sJ8A',
        'db': 'baoxianjihuashu',
        'charset': 'utf8mb4'
    },
    'redis': {
        'type': 'redis',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 4
    },
    'Jkdoc': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'Jkdoc',
        'charset': 'utf8mb4'
    },
    'dbtest': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'password': '123456',
        'db': 'dbtest',
        'charset': 'utf8mb4'
    }
}

# # 有优化空间

DB_CONFIG['default'] = DB_CONFIG['dbtest']


def make_connect_string(key, odbc=None):
    if key in DB_CONFIG:
        types = DB_CONFIG[key]['type']
    else:
        raise ('错误提示：检查数据库配置：' + key)

    if types == 'mysql':
        if odbc == 'mysqlclient':
            drver = 'mysql+mysqldb'
        elif odbc == 'pymysql':
            drver = 'mysql+pymysql'
        elif odbc == 'connector':
            drver = 'mysql+mysqlconnector'
        elif odbc == 'OurSQL':
            drver = 'mysql+oursql'
        else:
            drver = 'mysql'
        return f"{drver}://{DB_CONFIG[key]['user']}:{DB_CONFIG[key]['password']}@{DB_CONFIG[key]['host']}:{DB_CONFIG[key]['port']}/{DB_CONFIG[key]['db']}?charset={DB_CONFIG[key]['charset']}"

    if types == 'PostgreSQL':
        if odbc == 'psycopg2':
            drver = 'postgresql+psycopg2'
        elif odbc == 'pg8000':
            drver = 'postgresql+pg8000'
        else:
            drver = 'postgresql'
        return f"{drver}://{DB_CONFIG[key]['user']}:{DB_CONFIG[key]['password']}@{DB_CONFIG[key]['host']}:{DB_CONFIG[key]['port']}/{DB_CONFIG[key]['db']}?charset={DB_CONFIG[key]['charset']}"

    if types == 'Oracle':
        if odbc == 'cx_oracle':
            drver = 'oracle+cx_oracle'
        else:
            drver = 'oracle'
        return f"{drver}//{DB_CONFIG[key]['user']}:{DB_CONFIG[key]['password']}@{DB_CONFIG[key]['host']}:{DB_CONFIG[key]['port']}/{DB_CONFIG[key]['db']}?charset={DB_CONFIG[key]['charset']}"
        # cx_oracle:'oracle+cx_oracle://scott:tiger@tnsname'

    if types == 'SQLServer':
        if odbc == 'pyodbc':
            drver = 'mssql+pyodbc'
        else:
            drver = 'mssql+pymssql'
        return f"{drver}://{DB_CONFIG[key]['user']}:{DB_CONFIG[key]['password']}@{DB_CONFIG[key]['host']}:{DB_CONFIG[key]['port']}/{DB_CONFIG[key]['db']}?charset={DB_CONFIG[key]['charset']}"
        # pyodbc:'mssql+pyodbc://scott:tiger@mydsn'

    if types == 'SQLite':
        drver = 'sqlite'
        return f"{drver}:///{DB_CONFIG[key]['host']}"

    if types == 'access':
        drver = 'access+pyodbc'
        return f"{drver}://{DB_CONFIG[key]['host']}"

    if types == 'monetdb':
        if odbc == 'lite':
            drver = 'monetdb+lite'
        else:
            drver = 'monetdb'
        return f"{drver}:///{DB_CONFIG[key]['host']}"
