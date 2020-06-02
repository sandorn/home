# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-14 15:26:00
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-14 23:35:24
'''

from xjLib.mssql import MySQLConnection


def main():
    dbcon = MySQLConnection()
    # 使用execute方法执行SQL语句
    dbcon.cur.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取一条数据库。
    print("数据库版本：", dbcon.cur.fetchone())

    dbcon2 = MySQLConnection('db4', 'pmysql')
    # 使用execute方法执行SQL语句
    dbcon2.cur.execute("SELECT VERSION()")
    # 使用 fetchone() 方法获取一条数据库。
    print("数据库版本：", dbcon2.cur.fetchone())
    return


def resert():
    # 首先从items里取出数据
    _BOOKNAME = '测试用书名'
    _INDEX = 1
    _XUHAO = 1
    _ZJNAME = '第一章'
    _ZJTEXT = '这就是章节正文，这就是章节正文'
    try:
        _sql = 'Insert into xiashu(`BOOKNAME`,`INDEX`,`XUHAO`,`ZJNAME`,`ZJTEXT`) values (\'%s\',%d ,%d ,\'%s\',\'%s\')' % (_BOOKNAME, _INDEX, _XUHAO, _ZJNAME, _ZJTEXT)

        dbcon.worKon(_sql)
    except Exception as e:
        print("插入数据出错,错误原因%s" % e)
    return


if __name__ == '__main__':
    main()
