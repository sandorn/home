# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-26 19:25:25
@LastEditors: Even.Sand
@LastEditTime: 2020-03-26 19:30:35
'''


import threading


def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func


class Singleton(object):
    instance = None
    glnum = 0

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        :type kwargs: object
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, num):
        self.a = num + 5
        Singleton.glnum += 10

    def printf(self):
        print(self.a)


a = Singleton(3)
print(id(a), a.a, id(a.a), a.glnum, id(a.glnum))
b = Singleton(4)
print(id(b), b.a, id(b.a), b.glnum, id(b.glnum))

print(id(a), a.a, id(a.a), a.glnum, id(a.glnum))
# !此行55输出与53输出完全一样！！
