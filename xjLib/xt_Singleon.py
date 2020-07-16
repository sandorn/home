# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-23 17:41:52
#FilePath     : /xjLib/xt_Singleon.py
#LastEditTime : 2020-07-14 09:08:33
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from threading import Lock
from functools import wraps


def singleton_wrap(cls):
    '''单例装饰器，单次init，只能实例调用classmethod'''
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


class Singleton_Model:
    '''单例模式，可继承，多次init，
    可用类调用classmethod，可照写
    # 单次初始化，增加下列语句
    # if not self._intialed:
    #     self._intialed = True
    '''
    _lock = Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
                    # #__init__标志，可避免重复初始化
                    cls._instance._intialed = False
        return cls._instance

    def __init__(self):
        pass


class Singleton_Base:
    '''
    单例模式基类，用于继承，多次init，
    可用类调用classmethod
    # 单次初始化，增加下列语句
    # if not self._intialed:
    #     self._intialed = True
    '''
    _instance = dict()
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with cls._lock:
                if cls not in cls._instance:
                    cls._instance[cls] = super().__new__(cls)
                    # #__init__标志，可避免重复初始化
                    cls._instance[cls]._intialed = False

        return cls._instance[cls]


class Singleton_Meta(type):
    '''
    单例模式元类，metaclass=Singleton_Meta，
    # @单次init，可用类调用classmethod
    '''

    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class singleton_wrap_class(object):
    '''单例类装饰器，单次init，只能实例调用classmethod'''
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


def singleton_wrap_return_class(_cls):
    '''单例类装饰器，多次init，返回类，类属性及方法通用'''
    class class_wrapper(_cls):

        _instance = dict()
        _lock = Lock()

        def __new__(cls, *args, **kwargs):
            if cls not in cls._instance.keys():
                with cls._lock:
                    if cls not in cls._instance.keys():
                        cls._instance[cls] = super().__new__(cls)
                        # cls._instance[cls]._intialed = False
            return cls._instance[cls]

    class_wrapper.__name__ = _cls.__name__  # 保留原类的名字
    return class_wrapper


class Singleton_Mixin:
    '''混入方式继承单例，部分无效'''
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance


if __name__ == "__main__":

    class sss:
        def __init__(self, string, age=12):
            self.name = string
            self.age = age

    class sample(sss, Singleton_Mixin):
        pass

    aa = sample('张三')
    print(aa.__dict__)
    bb = sample('李四', 28)
    print(aa is bb, id(aa), id(bb))
    print(aa.__dict__, bb.__dict__)
    print(11111, sample.__mro__)
    print(22222, sample.__base__)
    print(33333, sample.__bases__)
    sample.__bases__ += (Singleton_Model, )
    print(44444, sample.__bases__)
    print(55555, sample.__mro__)