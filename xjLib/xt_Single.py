# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-23 17:41:52
#FilePath     : /xjLib/xt_Single.py
#LastEditTime : 2020-06-23 17:42:47
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
    可用类调用classmethod，可照写'''
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass


class Singleton_Base:
    '''
    单例模式基类，用于继承，多次init，
    可用类调用classmethod
    '''
    _instance = dict()
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instance.keys():
            with cls._lock:
                if cls not in cls._instance.keys():
                    cls._instance[cls] = super().__new__(cls)
                    # 需给出一个标志，从而__init__方法可以根据此标志避免重复初始化成员变量
                    cls._instance[cls]._intialed = False
        return cls._instance[cls]


class Singleton_Meta(type):
    '''
    单例模式元类，单次init，
    metaclass=Singleton_Meta，
    可用类调用classmethod
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
