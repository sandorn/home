# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-30 00:10:28
LastEditTime : 2022-12-30 00:10:29
FilePath     : /py学习/PY编程模式/分发装饰器singledispatch-1.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from functools import singledispatch


def check_type(func):

    def wrapper(*args):
        arg1, arg2 = args[:2]
        return '【错误】：参数类型不同，无法拼接!!' if type(arg1) != type(arg2) else func(*args)

    return wrapper


@singledispatch
def add(obj, new_obj):
    raise TypeError


@add.register(str)
@check_type
def _(obj, new_obj):
    obj += new_obj
    return obj


@add.register(list)
@check_type
def _(obj, new_obj):
    obj.extend(new_obj)
    return obj


@add.register(dict)
@check_type
def _(obj, new_obj):
    obj.update(new_obj)
    return obj


@add.register(tuple)
@check_type
def _(obj, new_obj):
    return (*obj, *new_obj)


print(add('hello', ', world'))
print(add([1, 2, 3], [4, 5, 6]))
print(add({'name': 'wangbm'}, {'age': 25}))
print(add(('apple', 'huawei'), ('vivo', 'oppo')))

# list 和 字符串 无法拼接
print(add([1, 2, 3], '4,5,6'))
