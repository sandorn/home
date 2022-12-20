# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-23 17:41:52
FilePath     : /xjLib/xt_Singleon.py
LastEditTime : 2020-12-08 12:30:49
#Github       : https://github.com/sandorn/home
#==============================================================
单例，与多线程无关
'''

from functools import wraps
from threading import Lock


class Singleton_Mixin:
    '''单例模式,可混入继承,可多次init,
    可用类调用classmethod,可照写
    # 可通过self._intialed判断,设定初始化次数
    '''
    _lock = Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)  # ! *args, **kwargs出错
                    # #__init__标志,可避免重复初始化
                    cls._instance._intialed = False
        return cls._instance

    def __del__(self):
        self.__class__._instance = None
        self.__class__._intialed = False


class Singleton_Base:
    '''
    单例模式基类,用于继承,可多次init,
    可用类调用 classmethod
    # 可通过self._intialed判断,设定初始化次数
    '''
    _instance = dict()
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    cls._instance[cls] = super().__new__(cls)  # ! *args, **kwargs出错
                    # #__init__标志,可避免重复初始化
                    cls._instance[cls]._intialed = False

        return cls._instance[cls]


def singleton_wrap_return_class(_cls):
    '''单例类装饰器,多次init,返回类,类属性及方法通用
    # 可通过self._intialed判断,设定初始化次数'''

    class class_wrapper(_cls):

        _lock = Lock()
        _instance = None

        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                with cls._lock:
                    if cls._instance is None:
                        cls._instance = super().__new__(cls)
                        cls._instance._intialed = False
            return cls._instance

        def __del__(self):
            self.__class__._instance = None
            self.__class__._intialed = False

    class_wrapper.__name__ = _cls.__name__  # 保留原类的名字
    return class_wrapper


def singleton_wrap(cls):
    '''单例装饰器,单次init,只能实例调用classmethod'''
    _instance = {}
    _lock = Lock()

    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            with _lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


class singleton_wrap_class:
    '''单例类装饰器,单次init,只能实例调用classmethod'''
    _lock = Lock()

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self._cls(*args, **kwargs)
        return self._instance


class Singleton_Meta(type):
    '''单例模式元类,metaclass=Singleton_Meta,
    # @单次init,可用类调用classmethod'''

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


if __name__ == "__main__":

    class sss:

        def __init__(self, string, age=12):
            self.name = string
            self.age = age

    class sample(sss, Singleton_Mixin):
        # # Singleton_Base
        pass

    @singleton_wrap_return_class
    class t():
        ...

    @singleton_wrap
    class tt:
        ...

    aa = sample('张三')
    print(aa.__dict__)
    bb = sample('李四', 28)
    bb.ages = 99
    cc = t()
    cc.a = 88
    dd = tt()
    ee = tt()
    ee.b = 987
    dd.a = 4444
    print(aa is bb, ee is dd, id(aa), id(bb), id(cc), id(dd), aa.__dict__, bb.__dict__, cc.__dict__, dd.__dict__)
    print(11111, sample.__mro__)
    print(22222, sample.__base__)
    print(33333, sample.__bases__)
    # sample.__bases__ += (Singleton_Base, )
    # print(44444, sample.__bases__)
    print(55555, sample.__mro__)
