# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-30 14:25:16
#LastEditTime : 2020-05-30 15:44:30
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================

Python 类的__getattr__ __setattr__ __getitem__ __setitem__ - Vincen_shen - 博客园
https://www.cnblogs.com/vincenshen/articles/7107522.html


'''


class category:

    # #使用[下标]获取实例属性 如obj[key]，自调用__getitem__
    def __getitem__(self, attr):
        # return  self.__getattribute__(attr)
        return getattr(self, attr)

    # #使用[下标]获取实例属性 如obj[key]，自调用__setitem__
    def __setitem__(self, attr, value):
        # #self.__dict__[attr] = value
        return setattr(self, attr, value)

    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def __getattr__(self, attr):
        return getattr(self, attr)

    # #设置类实例属性 如obj.key = 'tom'，自调用__setattr__
    def __setattr__(self, attr, value):
        # #self.__dict__[attr] = value
        setattr(self, attr, value)

    # #用于打印显示
    def __repr__(self):
        return str(self.__class__) + ' : ' + str({attr: getattr(self, attr) for attr in self.__dict__})

    __str__ = __repr__
