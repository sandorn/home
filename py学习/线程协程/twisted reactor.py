# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-23 23:55:43
LastEditTime : 2023-01-24 00:02:24
FilePath     : /CODE/py学习/twisted reactor.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import threading
import time

from twisted.internet import reactor

reactor.suggestThreadPoolSize(30)


def tt(i, j):
    if i == 10: reactor.stop()
    # while 1:
    print(i, f'{threading.currentThread()}-------tt--------', j)
    time.sleep(0.01)


def gg(i, j):
    time.sleep(0.01)
    if i == 10:
        reactor.stop()
    print(i, f'{threading.currentThread()}-------gg--------', j)
    time.sleep(0.01)


for i in range(20):
    # reactor.callFromThread(gg, i, i)
    reactor.callInThread(tt, i, i)
print("I want to start")
reactor.run()
