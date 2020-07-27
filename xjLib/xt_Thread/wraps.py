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
#LastEditTime : 2020-07-24 13:35:18
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from functools import wraps
from threading import Lock, Thread


def thread_safe(lock=None):
    '''函数的线程安全化，需要lock'''
    lock = lock or Lock()

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''函数的线程安全化'''
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorate


class MyThread(Thread):
    '''供线程装饰器调用'''
    def __init__(self, func, name, *args, **kwargs):
        super().__init__(target=func, args=args, kwargs=kwargs, name=name)

    def run(self):
        self.callback = self._kwargs.pop('callback', None)
        self.Result_dict = self._kwargs.pop('results', None)
        self.Result = self._target(*self._args, **self._kwargs)

        if self.callback is not None and callable(self.callback):
            self.Result = self.callback(self.Result)
        if self.Result_dict is not None:
            self.Result_dict[self.ident] = self.Result

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.join()
            return self.Result
        except Exception:
            return None


def thread_wrap(func=None):
    '''函数的线程装饰器，返回线程，有无括号都可以，\n
    getResult获取结果，类或实例getAllResult获取结果集合，\n
    可在调用被装饰函数添加daemon=True,callback等参数'''

    # 需要再次嵌套一层装饰器，才可以供下面运行时使用
    def wrapper(fun):
        def inner(*args, **kwargs):
            daemon = kwargs.pop('daemon', False)

            _mythr = MyThread(
                fun,
                func.__name__,
                *args,
                **kwargs,
            )

            _mythr.setDaemon(daemon)  # #传递装饰器参数
            _mythr.start()

            print(f"{_mythr} start with thread_wrap...")
            return _mythr

        return inner

    # 判断func(参数)
    if func is None:
        return wrapper

    # 如果func是可以调用的函数
    elif callable(func):
        return wrapper(func)


class thread_wrap_class:
    '''函数的线程装饰器，无括号()，返回线程实例，\n
    getResult获取结果，类或实例getAllResult获取结果集合，\n
    可在调用被装饰函数添加daemon=True，callback等参数'''
    Result_dict = {}
    thread_dict = {}

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f"{self.func.__name__} start with thread_wrap_class...")
        self.daemon = kwargs.pop('daemon', False)

        _mythr = MyThread(
            self.func,
            self.func.__name__,
            *args,
            results=thread_wrap_class.Result_dict,
            **kwargs,
        )

        _mythr.setDaemon(self.daemon)  # #传递装饰器参数
        _mythr.getAllResult = self.getAllResult
        _mythr.start()
        self.thread_dict[_mythr.ident] = _mythr
        return _mythr

    @classmethod
    def getAllResult(cls):
        '''获取全部结果，并清空'''
        for thr in cls.thread_dict.values():
            thr.join()
        res, cls.Result_dict = cls.Result_dict, {}
        return res


print = thread_safe()(print)
