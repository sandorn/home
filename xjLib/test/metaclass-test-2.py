# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-18 09:40:31
#FilePath     : /xjLib/test/meta_class--test-2.py
#LastEditTime : 2020-06-18 10:08:50
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


a = two()
print(dir(a))
""" output
ClassWithMeta1 is created by Meta1
BaseClass is created by Meta2
BaseClass is created by Meta1
Test is created by Meta2
Test is created by Meta1
[<class '__main__.Meta2'>, <class 'abc.ABCMeta'>, <class '__main__.Meta1'>]
"""
