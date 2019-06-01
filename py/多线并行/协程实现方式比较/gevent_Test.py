# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-22 11:19:05
@LastEditors: Even.Sand
@LastEditTime: 2019-05-22 11:19:05
'''
import gevent
from gevent import monkey
import time
import requests
monkey.patch_socket()


def request_f(Target_url):
    res_text = requests.get(Target_url).text


def f(Times, Target_url):
    st = time.time()
    WaitList = [gevent.spawn(request_f, Target_url)] * Times
    gevent.joinall(WaitList)
    et = time.time()
    return et - st
