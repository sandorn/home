# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-30 08:58:40
#LastEditTime : 2020-06-03 11:41:29
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

from xt_DAO.xt_sqlbase import SqlMeta
from xt_DAO.xt_sqlalchemy import SqlConnection

import datetime
from sqlalchemy import Column, Integer, DateTime, Numeric, VARCHAR
from config import DEFAULT_SCORE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Proxy(Base, SqlMeta):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False, default=0)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=DEFAULT_SCORE)
    '''
    ip(ip地址)
    port(端口)
    types(类型,0高匿名,1透明)，
    protocol(0 http,1 https),
    updatetime(更新时间)
    speed(连接速度)
    score(质量分数)
    '''


sqlhelper = SqlConnection(Proxy)

if __name__ == '__main__':
    from xt_Log import MyLog

    log = MyLog()

    from xt_Requests import parse_get
    from config import TEST_HTTP_HEADER

    # proxylist = sqlhelper.select(10)

    # proxy = random.choice(proxylist)
    proxy = ['123.163.97.79', 9999]
    res = parse_get(TEST_HTTP_HEADER, proxies=proxy)
    print(res, res.text)
