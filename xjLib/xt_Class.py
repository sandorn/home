# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-05-30 14:25:16
#LastEditTime : 2020-06-09 13:19:32
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


'''
python中以双下划线的是一些系统定义得名称，让python以更优雅得语法实行一些操作，本质上还是一些函数和变量，与其他函数和变量无二。
比如x.__add__(y) 等价于 x+y
有一些很常见，有一些可能比较偏，在这里罗列一下，做个笔记，备忘。
x.__contains__(y) 等价于 y in x, 在list,str, dict,set等容器中有这个函数
__base__, __bases__, __mro__, 关于类继承和函数查找路径的。
class.__subclasses__(), 返回子类列表
x.__call__(...) == x(...)
x.__cmp__(y) == cmp(x,y)
x.__getattribute__('name') == x.name == getattr(x, 'name'),  比__getattr__更早调用
x.__hash__() == hash(x)
x.__sizeof__(), x在内存中的字节数, x为class得话， 就应该是x.__basicsize__
x.__delattr__('name') == del x.name
__dictoffset__ attribute tells you the offset to where you find the pointer to the __dict__ object in any instance object that has one. It is in bytes.
__flags__, 返回一串数字，用来判断该类型能否被序列化（if it's a heap type), __flags__ & 512
S.__format__, 有些类有用
x.__getitem__(y) == x[y], 相应还有__setitem__, 某些不可修改类型如set，str没有__setitem__
x.__getslice__(i, j) == x[i:j], 有个疑问，x='123456789', x[::2],是咋实现得
__subclasscheck__(), check if a class is subclass
__instancecheck__(), check if an object is an instance
__itemsize__, These fields allow calculating the size in bytes of instances of the type. 0是可变长度， 非0则是固定长度
x.__mod__(y) == x%y, x.__rmod__(y) == y%x
x.__module__ , x所属模块
x.__mul__(y) == x*y,  x.__rmul__(y) == y*x

__reduce__, __reduce_ex__ , for pickle

__slots__ 使用之后类变成静态一样，没有了__dict__, 实例也不可新添加属性

__getattr__ 在一般的查找属性查找不到之后会调用此函数

__setattr__ 取代一般的赋值操作，如果有此函数会调用此函数， 如想调用正常赋值途径用 object.__setattr__(self, name, value)

__delattr__ 同__setattr__, 在del obj.name有意义时会调用
'''
