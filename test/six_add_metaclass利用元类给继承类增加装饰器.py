# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-24 14:31:02
FilePath     : /xjLib/test/six_add_metaclass利用元类给继承类增加装饰器.py
LastEditTime : 2021-03-19 11:57:24
#Github       : https://github.com/sandorn/home
#==============================================================
python3利用元类批量给所有继承类增加装饰器_这天鹅肉有毒-CSDN博客_python 给类的所有函数增加装饰器
https://blog.csdn.net/weixin_43485502/article/details/91510311
'''

import six
import types
import inspect
from functools import wraps
from collections import OrderedDict


def xx(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        print('9999', '执行了decorator')
        res = func(*args, **kwargs)
        print('8888', '执行完毕')
        if res:
            return res

    return wrap


class Meta(type):
    @classmethod
    def options(cls, bases, attrs):
        new_attrs = OrderedDict()
        # 循环自己的所有属性
        for key, value in attrs.items():
            # 对各种类型的方法进行分别处理
            if hasattr(value, '__func__') or isinstance(value, types.FunctionType):
                if isinstance(value, staticmethod):
                    new_attrs[key] = staticmethod(cls.func(value.__func__))
                elif isinstance(value, classmethod):
                    new_attrs[key] = classmethod(cls.func(value.__func__))
                elif isinstance(value, property):
                    new_attrs[key] = property(fget=cls.func(value.fget), fset=cls.func(value.fset), fdel=cls.func(value.fdel), doc=value.__doc__)
                elif not key.startswith('__'):
                    new_attrs[key] = cls.func(value)
                continue
            new_attrs[key] = value

        # 循环所有继承类
        for base in bases:
            for key, value in base.__dict__.items():
                if key not in new_attrs:
                    if hasattr(value, '__func__') or isinstance(value, types.FunctionType):
                        if isinstance(value, staticmethod):
                            new_attrs[key] = staticmethod(cls.func(value.__func__))
                        elif isinstance(value, classmethod):
                            new_attrs[key] = classmethod(xx(value.__func__))
                        elif isinstance(value, property):
                            new_attrs[key] = property(fget=cls.func(value.fget), fset=cls.func(value.fset), fdel=cls.func(value.fdel), doc=value.__doc__)
                        elif not key.startswith('__'):
                            new_attrs[key] = xx(value)
                        continue
                    new_attrs[key] = value

        return new_attrs

    def __new__(cls, name, bases, attrs):
        """
        name:类名,
        bases:类所继承的父类
        attrs:类所有的属性
        """
        cls.func = attrs.get('meta_decoator')
        assert inspect.isfunction(cls.func), ('传入的meta装饰器不正确')
        # 在类生成的时候做一些手脚
        new_attrs = cls.options(bases, attrs)
        return super().__new__(cls, name, bases, new_attrs)


class obj(object):
    def __init__(self):
        print('obj.__init__')

    @classmethod
    def one(cls):
        print('obj.one')


@six.add_metaclass(Meta)
class obj1(obj):
    # 只要继承类中有meta_decoator属性,这个属性的方法就会自动装饰下面所有的方法
    # 包括类属性,实例属性,property属性,静态属性
    meta_decoator = xx
    aa = 1

    @classmethod
    def three(cls):
        print('obj1.three')

    @staticmethod
    def four():
        print('obj1.four')

    def two(self):
        print(self.pro)
        print('obj1.two')

    @property
    def pro(self):
        return self.aa


b = obj1()
print(dir(b))
b.one()
b.two()

a = obj1
a.four()
a.three()
