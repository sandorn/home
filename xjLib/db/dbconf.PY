# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@version:
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 01:37:18
@LastEditors: Even.Sand
@LastEditTime: 2020-04-13 18:18:47
'''

db_conf = {
    'TXbook': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'passwd': '123456',
        'db': 'biqukan',
        'charset': 'utf8mb4',
    },
    'TXbx': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'passwd': '123456',  # 'password'
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
    'TX_Root': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'root',
        'passwd': 'Sand2808',
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
    'db4': {
        'type': 'mysql',
        'host': 'db4free.net',
        'port': 3306,
        'user': 'sandorn',
        'passwd': 'eeM3sh4KPkp4sJ8A',
        'db': 'baoxianjihuashu',
        'charset': 'utf8mb4',
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
        'passwd': '123456',
        'db': 'Jkdoc',
        'charset': 'utf8mb4',
    },
}
db_conf['default'] = db_conf['TXbx']


def make_connect_string(key, odbc=None):

    if key in db_conf:
        types = db_conf[key]['type']
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
        return f"{drver}://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"

    if types == 'PostgreSQL':
        if odbc == 'psycopg2':
            drver = 'postgresql+psycopg2'
        elif odbc == 'pg8000':
            drver = 'postgresql+pg8000'
        else:
            drver = 'postgresql'
        return f"{drver}://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"

    if types == 'Oracle':
        if odbc == 'cx_oracle':
            drver = 'oracle+cx_oracle'
        else:
            drver = 'oracle'
        return f"{drver}//{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # cx_oracle:'oracle+cx_oracle://scott:tiger@tnsname'

    if types == 'SQLServer':
        if odbc == 'pyodbc':
            drver = 'mssql+pyodbc'
        else:
            drver = 'mssql+pymssql'
        return f"{drver}://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # pyodbc:'mssql+pyodbc://scott:tiger@mydsn'

    if types == 'SQLite':
        drver = 'sqlite'
        return f"{drver}:///{db_conf[key]['host']}"

    if types == 'access':
        drver = 'access+pyodbc'
        return f"{drver}://{db_conf[key]['host']}"

    if types == 'monetdb':
        if odbc == 'lite':
            drver = 'monetdb+lite'
        else:
            drver = 'monetdb'
        return f"{drver}:///{db_conf[key]['host']}"
