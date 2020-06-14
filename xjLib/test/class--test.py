# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-12 16:05:58
#FilePath     : /xjLib/test/class--test.py
#LastEditTime : 2020-06-14 23:09:36
#Github       : https://github.com/sandorn/home
#==============================================================
8.9 创建新的类或实例属性_w3cschool
https://www.w3cschool.cn/youshq/ciy5nozt.html
Python3.7 dataclass使用指南 - apocelipes - 博客园
https://www.cnblogs.com/apocelipes/p/10284346.html

'''
from xt_Class import typed_property, typeassert, readonly, Singleton_Warp_Func, Singleton_Warp_Class
from dataclasses import dataclass
from functools import partial
from pysnooper import snoop
from xt_Log import log
log = log()
snooper = snoop(log.filename)
print = log.debug


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


def setparams(self, attr, value):
    # #设置参数，更新body_dict
    self.__setattr__(attr, value)

    if attr in self.body_dict.keys():
        self.body_dict[attr] = value


String = partial(typed_property, expected_type=str)
Integer = partial(typed_property, expected_type=int)


# Example use
class Person:
    name = typed_property('name', str)
    age = Integer('age')

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return "Person [name={}, age={}]".format(self.name, self.age)


a = Person('张三', 44)
a.name = '二狗子'
print(a)


# Example use
# @typeassert(name=str, shares=int, price=float)
class Stock:
    __slots__ = ('real_name', '_shares', '__price')
    name = readonly('real_name')
    shares = readonly('_shares')
    price = readonly('_Stock__price')

    def __init__(self, name, shares, price):
        self.real_name = name
        self._shares = shares
        self.__price = price

    def __repr__(self):
        return f"{self.__class__.__name__} [name={self.name},shares={self.shares},price={self.price}]"


zsy = Stock('中国石油', 600987, 4.02)
print(zsy)
zsy._shares = 260987
zsy._Stock__price = 48.32
print(zsy)
print(dir(zsy))
