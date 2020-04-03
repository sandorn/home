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
@LastEditTime: 2020-04-02 00:20:40
'''


import threading
import time


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        time.sleep(0.001)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = cls(*args, **kwargs)
        return cls._instance


def task(arg):
    obj = Singleton.instance()
    print(obj)


def main0():
    for i in range(10):
        t = threading.Thread(target=task, args=[i, ])
        t.start()
    time.sleep(2)
    obj = Singleton.instance()
    print(obj)
    print('#' * 60)


class Singleton2(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = object.__new__(cls)
        return cls._instance


def task2(arg):
    obj = Singleton2()
    print(obj)


def main():
    obj1 = Singleton2()
    obj2 = Singleton2()
    print(obj1, obj2)

    for i in range(10):
        t = threading.Thread(target=task2, args=[i, ])
        t.start()


if __name__ == "__main__":
    main0()
    main()
