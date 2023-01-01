# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-30 00:55:53
LastEditTime : 2022-12-30 00:55:55
FilePath     : /py学习/PY编程模式/分发装饰器-multipledispatch -1.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from multipledispatch import dispatch


@dispatch()
def ddd(x:int, y:int):
    return x + y


@dispatch()
def ddd(x: object, y: object):
    return f"{x} + {y}"


print(ddd(1, 2))
print(ddd(1, 'hello'))
print(ddd('hello', 'world'))
