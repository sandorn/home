# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-18 09:40:31
#FilePath     : /xjLib/test/metaclass-test-2.py
#LastEditTime : 2020-07-13 17:18:36
#Github       : https://github.com/sandorn/home
#==============================================================
Python3元类的多重继承_miuric的博客-CSDN博客
https://blog.csdn.net/miuric/article/details/84349633
'''
from xt_MetaClass import generate_base
import abc


class Meta1(type):
    def __new__(cls, *args, **kwargs):
        clsname, bases, namespace = args

        print(clsname, "is created by", Meta1.__name__)
        return super().__new__(cls, *args, **kwargs)


class Meta2(type):
    def __new__(cls, *args, **kwargs):
        clsname, bases, namespace = args

        print(clsname, "is created by", Meta2.__name__)
        return super().__new__(cls, *args, **kwargs)


class ClassWithMeta1(metaclass=Meta1):
    pass


class ClassWithMeta2(metaclass=Meta2):
    pass


class Common:
    pass


class Test(generate_base(abc.ABC, ClassWithMeta1, Meta2, Common)):
    pass


class two(generate_base(ClassWithMeta1, ClassWithMeta2, Common)):
    pass


# a = two()
# print(dir(a))
""" output
ClassWithMeta1 is created by Meta1
BaseClass is created by Meta2
BaseClass is created by Meta1
Test is created by Meta2
Test is created by Meta1
[<class '__main__.Meta2'>, <class 'abc.ABCMeta'>, <class '__main__.Meta1'>]
"""


class Fruit():
    def func(self):
        print('水果')


class South():
    def func(self):
        super().func()
        print('南方')


class North():
    def func(self):
        super().func()
        print('北方')


class Big():
    def func(self):
        super().func()
        print('大的')


class Small():
    def func(self):
        super().func()
        print('小的')


class Apple(Small, North, Fruit):
    def func(self):
        print('苹果属于')
        super().func()


apple = Apple()
apple.func()
'''
苹果属于
水果
北方
小的
'''
