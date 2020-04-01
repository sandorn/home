# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 20:42:26
@LastEditors: Even.Sand
@LastEditTime: 2020-03-25 20:47:46
'''


import time
import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        time.sleep(1)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance


def task(arg):
    obj = Singleton.instance()
    print(obj)


def main0():
    for i in range(10):
        t = threading.Thread(target=task, args=[i, ])
        t.start()
    time.sleep(20)
    obj = Singleton.instance()
    print(obj)


import threading


class Singleton2(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton2, "_instance"):
            with Singleton2._instance_lock:
                if not hasattr(Singleton2, "_instance"):
                    Singleton2._instance = object.__new__(cls)
        return Singleton2._instance


obj1 = Singleton2()
obj2 = Singleton2()
print(obj1, obj2)


def task2(arg):
    obj = Singleton2()
    print(obj)


for i in range(10):
    t = threading.Thread(target=task2, args=[i, ])
    t.start()
