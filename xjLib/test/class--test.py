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
#LastEditTime : 2020-06-16 09:26:14
#Github       : https://github.com/sandorn/home
#==============================================================
8.9 创建新的类或实例属性_w3cschool
https://www.w3cschool.cn/youshq/ciy5nozt.html
Python3.7 dataclass使用指南 - apocelipes - 博客园
https://www.cnblogs.com/apocelipes/p/10284346.html

'''

from dataclasses import dataclass
from functools import partial

from pysnooper import snoop

from xt_Class import readonly, typeassert, typed_property
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


def example1():
    # String = partial(typed_property, expected_type=str)
    Integer = partial(typed_property, expected_type=int)

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


def example2():
    @typeassert(name=str, shares=int, price=float)
    class Stock:
        def __init__(self, name, shares, price):
            self.name = name
            self.shares = shares
            self.price = price

        def __repr__(self):
            return f"{self.__class__.__name__} [name={self.name},shares={self.shares},price={self.price}]"

    zsy = Stock('中国石油', 600987, 4.02)
    print(zsy)


def example3():
    class Stock_1:
        __slots__ = ('real_name', '_shares', '__price')
        name = readonly('real_name')
        shares = readonly('_shares')
        price = readonly('_Stock_1__price')

        def __init__(self, name, shares, price):
            self.real_name = name
            self._shares = shares
            self.__price = price

        def __repr__(self):
            return f"{self.__class__.__name__} [name={self.name},shares={self.shares},price={self.price}]"

    zsy = Stock_1('中国石油', 600987, 4.02)
    zsy._shares = 260987
    zsy._Stock_1__price = 48.32
    print(zsy)


def example4():
    @dataclass
    class Stock_D:
        name = readonly('real_name')
        shares = readonly('_shares')
        price = readonly('__price')
        real_name: str = ''
        _shares: int = 600987
        __price: float = 8.72

    zsy = Stock_D('中国石油', 600987, 4.02)
    zsy._shares = 260987
    zsy._Stock_D__price = 48.32
    print(zsy)


example1()
example2()
example3()
example4()
