# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-22 15:34:30
#FilePath     : /xjLib/xt_Thread/wraps.py
#LastEditTime : 2020-06-23 17:49:43
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from functools import wraps
from threading import Lock, Thread


def thread_safe(lock):
    '''函数的线程安全化，需要lock'''
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''函数的线程安全化'''
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorate


def thread_wraps(daemon=False):
    '''
    函数的线程装饰器，返回线程，
    # @加括号()，可选参数daemon
    '''
    def decorate(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            thr = Thread(target=func,
                         args=args,
                         kwargs=kwargs,
                         name=f"func-{func.__name__}",
                         daemon=daemon)
            thr.start()
            print(f"{thr} start with thread_wraps...")

            return thr

        return _wrapper

    print('in run wraps')
    return decorate


def thread_wrap(func):
    '''
    函数的线程装饰器，返回线程，
    # @不加括号()，无参数
    '''
    def wrapper(*args, **kwargs):
        thr = Thread(target=func,
                     args=args,
                     kwargs=kwargs,
                     name=f"func-{func.__name__}",
                     daemon=False)
        thr.start()
        print(f"{thr} start with thread_wrap...")

        return thr

    return wrapper


class thread_wraps_class:
    '''
    函数的线程装饰器，返回thread线程实例，getResult获取结果,
    thread_wraps_class.getAllResult 获取结果集合
    # @加括号()，可选参数daemon
    '''
    Result_dict = {}
    thread_dict = {}

    class MyThread(Thread):
        def __init__(self, func, name='', *args, **kwargs):
            super().__init__(target=func, args=args, kwargs=kwargs)
            self.name = name

        def run(self):
            print(f"{self} start with thread_wraps_class...")
            self.Result = self._target(*self._args, **self._kwargs)
            thread_wraps_class.Result_dict[self.ident] = self.Result

        def getResult(self):
            """获取当前线程结果"""
            try:
                self.join()
                return self.Result
            except Exception:
                return None

    def __init__(self, daemon=False, **kwargs):
        self.daemon = daemon

    def __call__(self, func):
        @wraps(func)
        def decorate(*args, **kwargs):
            _mythr = self.MyThread(func, func.__name__, *args, **kwargs)
            _mythr.start()
            self.thread_dict[_mythr.ident] = _mythr
            return _mythr

        return decorate

    @classmethod
    def getAllResult(cls):
        for thr in cls.thread_dict.values():
            thr.join()
        return cls.Result_dict


class thread_wrap_class:
    '''
    函数的线程装饰器，返回thread线程实例，getResult获取结果,
    thread_wrap_class.getAllResult 获取结果集合
    # @不加括号()，无参数
    '''
    Result_dict = {}
    thread_dict = {}

    class MyThread(Thread):
        def __init__(self, func, name='', *args, **kwargs):
            super().__init__(target=func, args=args, kwargs=kwargs, name=name)

        def run(self):
            print(f"{self} start with thread_wrap_class...")
            self.Result = self._target(*self._args, **self._kwargs)
            thread_wrap_class.Result_dict[self.ident] = self.Result

        def getResult(self):
            """获取当前线程结果"""
            try:
                self.join()
                return self.Result
            except Exception:
                return None

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        _mythr = self.MyThread(self.func, self.func.__name__, *args, **kwargs)
        _mythr.start()
        self.thread_dict[_mythr.ident] = _mythr
        return _mythr

    @classmethod
    def getAllResult(cls):
        for thr in cls.thread_dict.values():
            thr.join()
        return cls.Result_dict


_thread_lock = Lock()
print = thread_safe(_thread_lock)(print)
