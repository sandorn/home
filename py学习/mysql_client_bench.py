# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 14:34:37
@LastEditors: Even.Sand
@LastEditTime: 2020-03-25 14:49:06
msyql_client_bench/mysql_client_bench.py at master · roger777luo/msyql_client_bench
https://github.com/roger777luo/msyql_client_bench/blob/master/mysql_client_bench.py
'''


import sys

import MySQLdb  # mysqlclient fork from MySQLdb, fastest implementation, as it is C based
import pymysql
import mysql.connector

cfg = {'user': 'sandorn', 'host': 'cdb-lfp74hz4.bj.tencentcdb.com', 'port': 10014, 'database': 'bxflb', 'password': '123456'}


def one_plus_one(conn):
    cur = conn.cursor()
    cur.execute("SELECT 1+1")
    x = cur.fetchall()[0][0]
    assert x == 2
    cur.close()


def simple_select(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM `费率表` limit 100")
    rs = cur.fetchall()
    #assert len(rs) == 100
    cur.close()


import timeit
import functools


def bench_one(client_name):
    connector = sys.argv[1]

    if connector == 'connector':
        con = mysql.connector.connect(**cfg)
    elif connector == 'pymysql':
        con = pymysql.connect(**cfg)
    elif connector == 'mysqlclient':
        cfg['db'] = cfg.pop('database')
        con = MySQLdb.connect(**cfg)
    else:
        sys.exit("connector, pymysql or mysqlclient")

    print("{}:{}".format(client_name, timeit.timeit(functools.partial(one_plus_one, con), number=10000)))


def bench_all():
    n = 10000

    # connector
    con = mysql.connector.connect(**cfg)
    print("{}:{}".format("connector", timeit.timeit(functools.partial(one_plus_one, con), number=n)))

    # pymysql
    con = mysql.connector.connect(**cfg)
    print("{}:{}".format("pymysql", timeit.timeit(functools.partial(one_plus_one, con), number=n)))

    # mysqlclient
    cfg['db'] = cfg.pop('database')
    con = MySQLdb.connect(**cfg)
    print("{}:{}".format("mysqlclient", timeit.timeit(functools.partial(one_plus_one, con), number=n)))


def bench_all2():
    n = 100

    # connector
    con = mysql.connector.connect(**cfg)
    print("{}:{}".format("connector", simple_select(con)))

    # pymysql
    con = mysql.connector.connect(**cfg)
    print("{}:{}".format("pymysql", simple_select(con)))

    # mysqlclient
    cfg['db'] = cfg.pop('database')
    con = MySQLdb.connect(**cfg)
    print("{}:{}".format("mysqlclient", simple_select(con)))


if __name__ == '__main__':
    # bench_all()
    bench_all2()
