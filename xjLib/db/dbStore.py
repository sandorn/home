# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 01:37:18
@LastEditors: Even.Sand
@LastEditTime: 2020-04-01 18:50:44
'''


import sys
from dbRouter import db_conf


def make_db_connect_string(key):
    if db_conf[key]['type'] == 'mysql':
        db_conf_str_list[key] = f"mysql+mysqlconnector://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # mysqlclient:mysql+mysqldb
        # PyMySQL:mysql+pymysql
        # MySQL-connector-python:mysql+mysqlconnector
        # OurSQL:mysql+oursql

    elif db_conf[key]['type'] == 'PostgreSQL':
        db_conf_str_list[key] = f"postgresql://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # psycopg2:postgresql+psycopg2
        # pg8000:postgresql+pg8000

    elif db_conf[key]['type'] == 'Oracle':
        db_conf_str_list[key] = f"oracle://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # cx_oracle:'oracle+cx_oracle://scott:tiger@tnsname'

    elif db_conf[key]['type'] == 'SQLServer':
        db_conf_str_list[key] = f"mssql+pymssql://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        # pyodbc:'mssql+pyodbc://scott:tiger@mydsn'

    elif db_conf[key]['type'] == 'SQLite':
        db_conf_str_list[key] = f"sqlite:///{db_conf[key]['host']}"
        # engine = create_engine('sqlite:///C:\\path\\to\\foo.db')

    elif db_conf[key]['type'] == 'access':
        db_conf_str_list[key] = f"access+pyodbc://{db_conf[key]['host']}"
        # engine = create_engine("access+pyodbc://@your_dsn")

    elif db_conf[key]['type'] == 'monetdb':
        db_conf_str_list[key] = f"monetdb:///{db_conf[key]['host']}"
        # engine = create_engine('monetdb:///demo:', echo=True)
        # engine = create_engine('monetdb+lite:////tmp/monetdb_lite')


class classname(object):

    def __init__(self, connectType='orm', dbName='default', odbc='connector'):
        '''
        @description:
        @connectType:'dbapi';'orm';
        @return:
        '''
        self.connectType = connectType
        self.dbName = dbName
        self.odbc = odbc

    try:
        if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
            from db.MongoHelper import MongoHelper as SqlHelper
        elif DB_CONFIG['DB_CONNECT_TYPE'] == 'redis':
            from db.RedisHelper import RedisHelper as SqlHelper
        else:
            from db.SqlHelper import SqlHelper as SqlHelper
        self.db = SqlHelper()
        self.db.init_db()
    except Exception as e:
        raise "使用DB_CONNECT_STRING:%s--连接数据库失败" % DB_CONNECT_STRING
