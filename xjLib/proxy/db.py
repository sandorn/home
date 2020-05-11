# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-30 08:58:40
#LastEditTime : 2020-05-11 12:30:02
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import xjLib.db.xt_sqlalchemy

import datetime
from sqlalchemy import Column, Integer, DateTime, Numeric, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from config import DEFAULT_SCORE
Base = declarative_base()


class Proxy(Base, xjLib.db.xt_sqlalchemy.model):
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


sqlhelper = xjLib.db.xt_sqlalchemy.SqlConnection(Proxy)

if __name__ == '__main__':
    from xjLib.log import MyLog
    log = MyLog()

    from xjLib.req import get_by_proxy
    from config import TEST_HTTP_HEADER
    import random
    # proxylist = sqlhelper.select(10)

    # proxy = random.choice(proxylist)
    proxy = ['123.163.97.79', 9999]
    res = get_by_proxy(TEST_HTTP_HEADER, proxy)
    print(res, res.text)
