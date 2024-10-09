# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 09:27:13
FilePath     : /CODE/xjLib/xt_Thread/decorator.py
Github       : https://github.com/sandorn/home
==============================================================
https://mp.weixin.qq.com/s/4nkQITVniE9FhESDMt34Ow  # wrapt库
"""

import builtins
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Thread

import wrapt
from PyQt6.QtCore import QThread


class ThreadSafe(wrapt.ObjectProxy):
    """线程安全化，可以装饰普通函数和内部函数"""

    def __init__(self, wrapped):
        super().__init__(wrapped)

    def __call__(self, *args, **kwargs):
        if self.__wrapped__.__module__ == builtins.__name__:  # 判断内置函数
            with Lock():
                return self.__wrapped__(*args, **kwargs)
        else:
            if not hasattr(self, "__lock__"):
                self.__lock__ = Lock()
            with self.__lock__:
                return self.__wrapped__(*args, **kwargs)  # 普通函数和类方法


def thread_safe(func):
    """线程安全化，装饰函数和类方法"""
    if func.__module__ == builtins.__name__:  # 判断内置函数

        def wrapper(*args, **kwargs):
            with Lock():
                return func(*args, **kwargs)
    else:

        def wrapper(*args, **kwargs):
            if not hasattr(func, "__lock__"):
                func.__lock__ = Lock()
            with func.__lock__:
                return func(*args, **kwargs)  # 普通函数和类方法

    return wrapper


@wrapt.decorator
def parallelize_decorator(func, instance, args, kwargs):
    """
    使用多个 CPU 核心并行化函数调用。
    """

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(func, *args, **kwargs))
    return results


class _ThreadSafeDecoratorBase(Thread):
    """不单独使用,供线程装饰器[ thread_decorator | ThreadDecoratorClass ]调用"""

    def __init__(self, func, name, *args, **kwargs):
        super().__init__(target=func, name=name, args=args, kwargs=kwargs)
        self._running = True
        self.callback = self._kwargs.pop("callback", None)
        self.Result = None

    def run(self):
        self.Result = self._target(*self._args, **self._kwargs)
        self.Result = (
            self.callback(self.Result) if callable(self.callback) else self.Result
        )

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.join()
            return self.Result
        except Exception:
            raise Exception
            # return None

    def wait(self):
        """等待线程执行完毕"""
        self.join()

    def stop(self):
        """停止线程"""
        self._running = False


def thread_decorator(func=None, *args, **kwargs):
    """
    函数的线程装饰器,返回线程实例,\n
    有无括号都可以,getResult获取结果,\n
    可在调用被装饰函数添加daemon=True,callback等参数
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            _mythr = _ThreadSafeDecoratorBase(func, func.__name__, *args, **kwargs)
            _mythr.daemon = kwargs.pop("daemon", False)
            thread_print(
                f"func '{func.__name__}' in Thread start with thread_decorator..."
            )
            _mythr.start()
            return _mythr

        return inner

    return wrapper(func, *args, **kwargs) if callable(func) else wrapper


def qthread_decorator(func, *args, **kwargs):
    """
    函数的线程装饰器,返回线程实例,无括号,\n
    通过 getResult 获取结果集合,\n
    可在调用被装饰函数添加daemon=True,callback 等参数
    """

    def inner(*args, **kwargs):
        def getResult():
            _mythr.wait()
            return _mythr.Result

        _mythr = QThread()
        _mythr.daemon = kwargs.pop("daemon", True)
        _mythr.callback = kwargs.pop("callback", None)
        _mythr.setObjectName(func.__name__)
        _mythr.join = _mythr.wait
        _mythr.run = func

        thread_print(
            f"func '{func.__name__}' in QThread start with qthread_decorator..."
        )
        setattr(_mythr, "Result", _mythr.run(*args, **kwargs))
        if callable(_mythr.callback):
            _mythr.Result = _mythr.callback(_mythr.Result)

        _mythr.getResult = getResult

        # _mythr.join()  # 自动阻塞，等待结果
        return _mythr

    return inner


class ThreadDecoratorClass:
    """无特别用处，暂停使用,thread_decorator 无差异
    函数的线程装饰器,无括号(),返回线程实例,
    getResult获取结果,getAllResult获取结果集合,
    可在调用被装饰函数添加daemon=True,callback等参数"""

    Result_dict = {}
    thread_dict = {}

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        kwargs["Result_dict"] = ThreadDecoratorClass.Result_dict

        _mythr = _ThreadSafeDecoratorBase(
            self.func, self.func.__name__, *args, **kwargs
        )
        _mythr.daemon = kwargs.pop("daemon", False)
        _mythr.start()
        print(
            f"func    `{self.func.__name__}` in Thread start with ThreadDecoratorClass..."
        )
        self.thread_dict[_mythr.ident] = _mythr
        return _mythr

    @classmethod
    def getAllResult(cls):
        """获取全部结果,并清空"""
        for thr in cls.thread_dict.values():
            thr.join()
        res, cls.Result_dict = cls.Result_dict, {}
        return res


def create_mixin_class(name, cls, meta, **kwargs):
    """type动态混入继承,实质是调整 bases"""
    return type(name, (cls, meta), kwargs)


thread_print = thread_safe(print)

if __name__ == "__main__":

    @qthread_decorator
    def b(i):
        return i * 5

    @qthread_decorator
    def c(i):
        print(9999999999999, "in c", i)
        return i * 11

    # bb = b(8)
    # thread_print(bb.Result)
    # thread_print(bb)

    # cc = c(3, callback=lambda x: x * 11)
    # thread_print("Result:", cc.getResult())
    # thread_print("callback:", cc.callback, "daemon:", cc.daemon, "objectName:", cc.objectName())

    @parallelize_decorator
    def parallel_task(x):
        return x**3

    # thread_print(parallel_task(list(range(10))))

    class MyClass:
        @thread_safe
        def samethod(self, message):
            print(f"MyClass func with message: {message}")

    my_instance = MyClass()

    for i in range(3):
        t = my_instance.samethod(f"Thread {i}")
    ThreadSafe(c)("ThreadSafe C")
    ThreadSafe(print)("ThreadSafe print")
