#！/usr/bin/env python
#-*-coding:utf-8-*-
'''
@Software:   VSCode
@File    :   db.py
@Time    :   2019/04/13 12:26:47
@Author  :   Even Sand
@Version :   1.0
@Contact :   sandorn@163.com
@License :   (C)Copyright 2019-2019, NewSea
@Desc    :   None
'''

import pymysql as mysql
#import MySQLdb as mysql    #同样有效，MySQLdb来自于mysqlclient/DB API
import pandas as pd


def db():
    conn = mysql.connect(
        host='db4free.net',
        port=3306,
        user='sandorn',
        passwd='eeM3sh4KPkp4sJ8A',
        db='baoxianjihuashu',
        charset='utf8mb4',
    )
    if conn:
        return conn


def cur(db_name):
    # 使用cursor()方法获取操作游标
    cursor = db_name.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取一条数据库。
    if cursor.fetchone() == ('8.0.15', ):
        cursor.close()
        return True
    else:
        cursor.close()
        return False
