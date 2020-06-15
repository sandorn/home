# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-05-30 14:25:16
#LastEditTime : 2020-06-15 12:58:30
# Github       : https://github.com/sandorn/home
# License      : (C)Copyright 2009-2020, NewSea
# ==============================================================

Python 类的__getattr__ __setattr__ __getitem__ __setitem__ - Vincen_shen - 博客园
https://www.cnblogs.com/vincenshen/articles/7107522.html
'''

import threading
from pysnooper import snoop
from xt_Log import log
log = log()
snooper = snoop(log.filename)
# print = log.debug


class Ex_Class_Method_Meta:

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
        return ' < ' + str(self.__class__.__name__) + ' >: ' + str(
            {attr: getattr(self, attr)
             for attr in self.__dict__})

    __str__ = __repr__
    '''
        # return  self.__setattribute__(attr)
        # self.__dict__[attr] = value
    '''


def Singleton_Warp_Func(cls):
    """单例装饰器"""
    _instance = {}

    def inner(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
            print(cls.__class__.__name__, id(cls))
            # output:type
        return _instance[cls]

    return inner


class Singleton_Warp_Class(object):
    '''
    类装饰器@SingletonWarp
    或Cls3 = SingletonWarp(Cls3)
    '''
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
        # print(self.__class__.__name__, id(self))

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class SingletonMeta(object):
    '''
    用于继承
    Python单例（Singleton）不完美解决方案之实例创建_A_baobo的专栏-CSDN博客
    https://blog.csdn.net/A_baobo/article/details/43970315
    '''
    _instances = {}
    _obj = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instances.get(cls):
            orig = super(SingletonMeta, cls)
            obj = orig.__new__(cls, *args, **kwargs)
            cls._instances[cls] = obj
            cls._obj[obj] = dict(init=False)
            setattr(cls, '__init__', cls.decorate_init(cls.__init__))
        return cls._instances[cls]

    @classmethod
    def decorate_init(cls, fun):
        def warp_init(*args, **kwargs):
            if not cls._obj.get(args[0], {}).get('init'):
                fun(*args, **kwargs)

        return warp_init

    def __init__(self):
        # print(self.__class__.__name__, id(self))
        pass


class Singleton(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # print(self.__class__.__name__, id(self))
        pass


def typeassert(**kwargs):
    # Descriptor for a type-checked attribute
    # @限制属性赋值的类型，因使用__dict__,与slots冲突
    class Typed:
        def __init__(self, name, expected_type):
            self.name = name
            self.expected_type = expected_type

        def __get__(self, instance, cls):
            if instance is None:
                return self
            else:
                return instance.__dict__[self.name]

        def __set__(self, instance, value):
            if not isinstance(value, self.expected_type):
                raise TypeError('Expected ' + str(self.expected_type))
            instance.__dict__[self.name] = value

        def __delete__(self, instance):
            del instance.__dict__[self.name]

    # Class decorator that applies it to selected attributes
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls, name, Typed(name, expected_type))
        return cls

    return decorate


def typed_property(name, expected_type):
    '''class属性生成器'''
    storage_name = '_' + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError('{} must be a {}'.format(name, expected_type))
        setattr(self, storage_name, value)

    return prop


def readonly(name):
    '''
    class属性生成器,用于隐藏真实属性名，真实属性名用name定义
    '''
    storage_name = name

    @property
    def prop(self):
        return getattr(self, storage_name)

    return prop


if __name__ == "__main__":
    obj = Singleton_Warp_Class()
    obj1 = Singleton_Warp_Class()
    obj2 = Singleton_Warp_Class()
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

    你真的了解__instancecheck__、__subclasscheck__、__subclasshook__三者的用法吗 - 古明地盆 - 博客园
    https://www.cnblogs.com/traditional/p/11731676.html

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
