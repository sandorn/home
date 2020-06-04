# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2019-05-03 23:26:06
@LastEditors: Even.Sand
@LastEditTime: 2020-04-07 11:17:20
'''

import pymysql as mys

import pandas

from xjLib.db.dbRouter import db_conf
from xjLib.db.xt_mysql import engine

config = db_conf['TXbx']


class MysqlHelp:
    def __init__(self):

        self.port = config['port']
        self.charset = config['charset']
        self.user = config['user']
        self.host = config['host']
        self.passwd = config['passwd']
        self.db = config['db']

        self.conn = mys.connect(**config)
        #  使用cursor()获取操作游标
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.close()

    def ver(self):
        sql = "SELECT VERSION()"
        #  使用execute方法执行SQL语句
        self.cur.execute(sql)
        #  使用 fetchone() 方法获取一条数据库。
        版本号 = self.cur.fetchone()
        if 版本号:
            return 版本号[0]
        else:
            return False

    def workon(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            print('workon , ok')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False

    def getall(self, sql, args=[]):
        try:
            self.cur.execute(sql, args)
            print('getall , ok')
            data = self.cur.fetchall()
            return data
        except Exception as e:
            self.conn.rollback()
            print(e)
            return False

    def getable(self, sql):
        #  read_sql的两个参数: sql语句， 数据库连接
        sql = "select * from " + sql
        table = pandas.read_sql(sql, self.conn)
        if len(table):
            # print('getable , ok')
            return table
        else:
            return False


def main():
    myDb = MysqlHelp()
    print("ver:", myDb.ver())
    sql = " select * from users ;"
    data = myDb.getall(sql)
    print("data[0]:", data[0], "++++++++++data[1][1]:", data[1][1])
    table = myDb.getable("users")
    print("table.values[1][1]:", table.values[1][1])
    print("table[1:2]:", table[1:2])
    print("table.iloc[0]:", table.iloc[0])


def main9():
    with engine('TXbx', 'mysqlclient') as myDb:
        formname = "users"
        data = myDb.get_all_from_db(formname)
        print("data[0]:", data[0], "++++++++++data[1][1]:", data[1][1])
        table = myDb.get_pd_table("users")
        print("table.values[1][1]:", table.values[1][1])
        print("table[1:2]:", table[1:2])
        print("table.iloc[0]:", table.iloc[0])
        sql = " select * from users2 ;"
        dic = myDb.get_dict(sql)
        for d in dic:
            print(d)


if __name__ == '__main__':
    main9()
    '''
    myDb.workon(
        # "ALTER TABLE  users DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8mb4_0900_ai_ci"  # 设置默认编码
        #"ALTER TABLE  意外险分解 AUTO_INCREMENT=6"
        #" ALTER TABLE  users AUTO_INCREMENT=3201"  # 设定自增ID
        # "insert into users(username, password,手机) values('%s','%s','%s')" % ('gaogao', '1234567', '17610786502')
    )

    query = "INSERT INTO users(username, password,手机) values ('%s','%s','%s')"
    val = ('gaogao', '1234567', '17610786502')
    curs.execute(
        "insert into users(username, password,手机) values('%s','%s','%s')" %
        ('gaogao', '1234567', '17610786502'))
    db2.commit()
    sql = " select * from users; "
    # read_sql_query的两个参数: sql语句， 数据库连接

    df = pd.read_sql(sql, db2)
    print(df)
    print(type(df))
    '''
