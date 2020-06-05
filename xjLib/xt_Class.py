# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-05-30 14:25:16
#LastEditTime : 2020-06-05 14:49:38
# Github       : https://github.com/sandorn/home
# License      : (C)Copyright 2009-2020, NewSea
# ==============================================================

Python 类的__getattr__ __setattr__ __getitem__ __setitem__ - Vincen_shen - 博客园
https://www.cnblogs.com/vincenshen/articles/7107522.html
'''

import threading


class meta:

    # #下标obj[key]
    def __getitem__(self, attr):
        return getattr(self, attr)

    # #下标obj[key]
    def __setitem__(self, attr, value):
        return setattr(self, attr, value)

    # #迭代
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    # #原点调用obj.key
    def __getattr__(self, attr):
        return getattr(self, attr)

    # #原点调用obj.key
    def __setattr__(self, attr, value):
        setattr(self, attr, value)

    # #用于打印显示
    def __repr__(self):
        return str(self.__class__) + ' : ' + str({attr: getattr(self, attr) for attr in self.__dict__})

    __str__ = __repr__

    '''
        # return  self.__setattribute__(attr)
        # self.__dict__[attr] = value
    '''


class data_EXmethod:
    '''data_EXmethod  数据扩展.原点引用方法'''

    def __init__(self, primitive):
        self.data = primitive

    def __getattr__(self, item):
        value = self.data.get(item, None)
        if isinstance(value, dict):
            value = data_EXmethod(value)
        return value

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __getitem__(self, item):
        # value = self.__getattribute__(item)
        value = None
        if type(self.data) in (list, tuple):
            value = self.data[item]

            if type(value) in (dict, list, tuple):
                value = data_EXmethod(value)

        elif isinstance(self.data, dict):
            value = self.__getattr__(item)

        return value


def flatten(nested):
    try:
        # 不要迭代类似字符串的对象：
        # if isinstance(variate,(list,tuple)):
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError

        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


def Singleton_warp(cls):
    """单例装饰器"""
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class Singleton(object):
    """单例类"""

    """实例化 obj = Singleton()"""
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = super().__new__(cls, *args, **kwargs)
        return Singleton._instance

    def __init__(self):
        pass


def setparams(self, attr, value):
    # #设置参数，更新body_dict
    self.__setattr__(attr, value)

    if attr in self.body_dict.keys():
        self.body_dict[attr] = value


class Foo:
    def get_A(self):
        print('获取(get)属性时执行===')

    def set_A(self, value):
        print('设置(set)属性时执行===')

    def del_A(self):
        print('删除(del)属性时执行===')
    A = property(get_A, set_A, del_A)

# # category


if __name__ == "__main__":
    def run_data_EXmethod():
        p = data_EXmethod({'name': 'boob', 'body': {'color': 'black', 'sex': '1'}, 'toys': [1, 2, 3, ], 'age': 100})
        print(p['toys'][1])
        p['toys'][1] = 99
        print(p['toys'][1])
        print(p.toys, p['toys'])  # # [1, 99, 3] [1, 99, 3]
        print(len(p))
        print(p['body'])
        print(p.body.color)
        print(p.name, p['name'])
        p.name = 'sand'
        print(p.name, p['name'])  # !  sand boob
        # p['name'] = 'newsea'
        # !TypeError: 'data_EXmethod' object does not support item assignment
        print(type(p), type(p.toys))

    run_data_EXmethod()
    f2 = Foo()
    f2.A  # '获取(get)属性时执行==='
    f2.A = '2'  # '设置(set)属性时执行==='
    del f2.A  # '删除(del)属性时执行==='
