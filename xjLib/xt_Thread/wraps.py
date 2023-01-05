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

from PyQt5.QtCore import QThread


def thread_safe(func=None, lock=Lock()):
    '''函数的线程安全化,需要lock'''

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorate(func) if func else decorate


class _MyThread(Thread):
    '''不单独使用,供线程装饰器调用'''

    def __init__(self, func, name, *args, **kwargs):
        super().__init__(target=func, name=name, args=args, kwargs=kwargs)
        self._running = True

    def run(self):
        self.callback = self._kwargs.pop('callback', None)
        self.Result = self._target(*self._args, **self._kwargs)
        self.Result = self.callback(self.Result) if callable(self.callback) else self.Result

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.join()
            return self.Result
        except Exception:
            return None

    def wait(self):
        '''等待线程执行完毕'''
        self.join()

    def stop(self):
        '''停止线程'''
        self._running = False


def Thread_wrap(func=None, *args, **kwargs):
    '''函数的线程装饰器,返回线程实例,有无括号都可以,\n
    getResult获取结果,类或实例getAllResult获取结果集合,\n
    可在调用被装饰函数添加daemon=True,callback等参数'''

    # 需要再次嵌套一层装饰器,才可以供下面运行时使用
    def wrapper(fun):

        def inner(*args, **kwargs):
            _mythr = _MyThread(
                fun,
                fun.__name__,
                *args,
                **kwargs,
            )
            _mythr.daemon = kwargs.pop('daemon', False)
            _mythr.start()
            print(f"{_mythr} start with thread_wrap...")
            return _mythr

        return inner

    # 如果func是可以调用的函数
    return wrapper(func, *args, **kwargs) if callable(func) else wrapper


def QThread_wrap(func=None, *args, **kwargs):
    '''函数的线程装饰器,返回线程实例,有无括号都可以,\n
    getResult获取结果,类或实例getAllResult获取结果集合,\n
    可在调用被装饰函数添加daemon=True,callback等参数'''

    # 需要再次嵌套一层装饰器,才可以供下面运行时使用
    def wrapper(fun):

        def inner(*args, **kwargs):
            _mythr = QThread()
            _mythr.daemon = kwargs.pop('daemon', True)
            _mythr.callback = kwargs.pop('callback', None)
            _mythr.setObjectName(fun.__name__)
            _mythr.join = _mythr.wait
            _mythr.run = fun
            print(f"{_mythr} | {fun.__name__} start with QThread_wrap...")
            _mythr.Result = _mythr.run(*args, **kwargs)
            _mythr.Result = _mythr.callback(_mythr.Result) if callable(_mythr.callback) else _mythr.Result
            # _mythr.join()  # 自动阻塞，等待结果
            return _mythr

        return inner

    # 如果func是可以调用的函数
    return wrapper(func, *args, **kwargs) if callable(func) else wrapper


class Thread_wrap_class:
    '''无特别用处，暂停使用
    函数的线程装饰器,无括号(),返回线程实例,
    getResult获取结果,类或实例getAllResult获取结果集合,
    可在调用被装饰函数添加daemon=True,callback等参数'''
    Result_dict = {}
    thread_dict = {}

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        kwargs['Result_dict'] = Thread_wrap_class.Result_dict
        _mythr = _MyThread(
            self.func,
            self.func.__name__,
            *args,
            **kwargs,
        )

        print(f"{_mythr} start with thread_wrap_class...")
        _mythr.daemon = kwargs.pop('daemon', False)
        _mythr.start()
        self.thread_dict[_mythr.ident] = _mythr
        return _mythr

    @classmethod
    def getAllResult(cls):
        '''获取全部结果,并清空'''
        for thr in cls.thread_dict.values():
            thr.join()
        res, cls.Result_dict = cls.Result_dict, {}
        return res


class Thread_wrap_simple:
    # 简单的线程装饰器,无括号(),返回线程实例,不返回结果
    def __init__(self, func):  # 接受函数
        self.func = func

    def __call__(self, *args, **kwargs):  # 接受任意参数
        print('函数调用CALL')
        _thr = Thread(target=self.func, args=args, kwargs=kwargs)
        _thr.start()
        _thr.join()
        return _thr


def create_mixin_class(name, cls, meta, **kwargs):
    '''type动态混入继承,实质是调整 bases'''
    return type(name, (cls, meta), kwargs)


thread_print = thread_safe(print)
print_lock = thread_safe(print)

if __name__ == "__main__":

    @Thread_wrap_simple
    def a(i):
        print('Thread_wrap_simple in func a : ', i, i * 2)
        return i * 2

    @Thread_wrap
    def b(i):
        print('Thread_wrap in func b : ', i, i * 5)
        return i * 5

    import time

    @QThread_wrap
    def c(i):
        time.sleep(2)
        print('QThread_wrap in func c : ', i, i * 11)
        return i * 11

    aa = a(8)
    bb = b(40)
    cc = c(3, callback=lambda x: x * 100)
    print('Result:', cc.Result)
    print('callback:', cc.callback)
    print('daemon:', cc.daemon)
    print('objectName:', cc.objectName())
    # print(thread_print.__name__)
