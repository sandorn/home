# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-05-30 14:25:16
#LastEditTime : 2020-06-18 16:13:31
# Github       : https://github.com/sandorn/home
# License      : (C)Copyright 2009-2020, NewSea
# ==============================================================
'''
import abc
from threading import Lock

from pysnooper import snoop

from xt_Log import log

log = log()
snooper = snoop(log.filename)
# print = log.debug


class item_MixIn:
    '''下标obj[key]'''
    def __getitem__(self, attr):
        return getattr(self, attr)

    def __setitem__(self, attr, value):
        return setattr(self, attr, value)

    def __delitem__(self, attr):
        return delattr(self, attr)


class attr_MixIn:
    '''
    原点调用obj.key
    不可使用init
    '''
    def __getattr__(self, attr):
        return super().__getattribute__(attr)
        # return getattr(self, attr)

    def __setattr__(self, attr, value):
        return super().__setattr__(attr, value)
        # return setattr(self, attr, value)

    def __delattr__(self, attr, value):
        return delattr(self, attr)


class dict_MixIn:
    '''生成类字典'''
    def __init__(self):
        self.__dict__ = {
            key: getattr(self, key)
            for key in dir(self)
            if not key.startswith('__') and not callable(getattr(self, key))
        }


class iter_MixIn:
    '''
    # #迭代类，用于继承
    from collections import Iterable
    print(isinstance(a, Iterable))
    '''
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class repr_MixIn:
    '''用于打印显示'''
    def __repr__(self):
        tmp = str(self.__dict__).replace('{', '').replace('}', '')
        return self.__class__.__name__ + '(' + tmp + ')'

    __str__ = __repr__


@snooper
class Class_Meta(dict_MixIn, item_MixIn, attr_MixIn, iter_MixIn, repr_MixIn):
    '''metaclass=abc.ABCMeta'''
    pass


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
    类装饰器@Singleton_Warp_Class
    或Cls3 = Singleton_Warp_Class(Cls3)
    '''
    def __init__(self, cls=None):
        self._cls = cls
        self._instance = {}
        # print(self.__class__.__name__, id(self))

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class Singleton_Meta(object):
    '''
    用于继承
    Python单例（Singleton）不完美解决方案之实例创建_A_baobo的专栏-CSDN博客
    https://blog.csdn.net/A_baobo/article/details/43970315
    '''
    _instances = {}
    _obj = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instances.get(cls):
            orig = super()
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
    _instance_lock = Lock()

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
        # #限制赋值类型
        if not isinstance(value, expected_type):
            raise TypeError('{} must be a {}'.format(name, expected_type))
        setattr(self, storage_name, value)

    return prop


def readonly(name):
    '''
    class属性生成器,用于隐藏真实属性名，真实属性名用name定义
    @dataclass(init=False),不生成类__dict__,使用class_to_dict函数
    '''
    storage_name = name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        # #赋值：无操作，直接返回
        return

    return prop
