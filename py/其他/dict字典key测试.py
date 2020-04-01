# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 10:38:06
@LastEditors: Even.Sand
@LastEditTime: 2020-03-25 12:18:21
'''


# dict字典key测试

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
        'passwd': '123456',
        # 'password': '123456',
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
    'STXbx': {
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
    'proxy': {
        'type': 'mysql',
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'passwd': '123456',
        'db': 'proxy',
        'charset': 'utf8mb4',
    },
}

for key in db_conf:
    if db_conf[key]['type'] == 'mysql':
        db_conf[key]['DB_CONNECT_STRING'] = f"mysql+mysqlconnector://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # mysqlclient:mysql+mysqldb
        # PyMySQL:mysql+pymysql
        # MySQL-connector-python:mysql+mysqlconnector
        # OurSQL:mysql+oursql

    elif db_conf[key]['type'] == 'PostgreSQL':
        db_conf[key]['DB_CONNECT_STRING'] = f"postgresql://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # psycopg2:postgresql+psycopg2
        # pg8000:postgresql+pg8000

    elif db_conf[key]['type'] == 'Oracle':
        db_conf[key]['DB_CONNECT_STRING'] = f"oracle://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # cx_oracle:'oracle+cx_oracle://scott:tiger@tnsname'

    elif db_conf[key]['type'] == 'SQLServer':
        db_conf[key]['DB_CONNECT_STRING'] = f"mssql+pymssql://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # pyodbc:'mssql+pyodbc://scott:tiger@mydsn'

    elif db_conf[key]['type'] == 'SQLite':
        db_conf[key]['DB_CONNECT_STRING'] = f"sqlite:///{db_conf[key]['host']}"
        #engine = create_engine('sqlite:///C:\\path\\to\\foo.db')

    elif db_conf[key]['type'] == 'access':
        db_conf[key]['DB_CONNECT_STRING'] = f"access+pyodbc://{db_conf[key]['host']}"
        #engine = create_engine("access+pyodbc://@your_dsn")

    elif db_conf[key]['type'] == 'monetdb':
        db_conf[key]['DB_CONNECT_STRING'] = f"monetdb:///{db_conf[key]['host']}"
        #engine = create_engine('monetdb:///demo:', echo=True)
        #engine = create_engine('monetdb+lite:////tmp/monetdb_lite')

for key in db_conf:
    print(key, db_conf[key])
