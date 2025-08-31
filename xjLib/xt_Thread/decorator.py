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

from __future__ import annotations

import asyncio
import builtins
from concurrent.futures import Executor, ThreadPoolExecutor
from functools import partial, wraps
from threading import Lock, Thread
from typing import Any, Callable

import wrapt
from PyQt6.QtCore import QThread


def run_on_executor(executor: Executor = None, background: bool = False):
    """
    异步装饰器
    - 支持同步函数使用 executor 加速
    - 异步函数和同步函数都可以使用 `await` 语法等待返回结果
    - 异步函数和同步函数都支持后台任务，无需等待
    Args:
        executor: 函数执行器, 装饰同步函数的时候使用
        background: 是否后台执行，默认False

    Returns:
    """

    def _run_on_executor(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if background:
                return asyncio.create_task(func(*args, **kwargs))
            else:
                return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            loop = asyncio.get_event_loop()
            task_func = partial(func, *args, **kwargs)    # 支持关键字参数
            return loop.run_in_executor(executor, task_func)

        # 异步函数判断
        wrapper_func = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return wrapper_func

    return _run_on_executor
    

class ThreadSafe(wrapt.ObjectProxy):
    """线程安全装饰器（支持实例方法和静态方法）

    :param wrapped: 被装饰的可调用对象
    :example:
        @ThreadSafe
        def critical_func():
            ...
    """

    def __init__(self, wrapped: Callable[..., Any]) -> None:
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

    def __init__(self, func, *args, **kwargs):
        super().__init__(target=func, name=func.__name__, args=args, kwargs=kwargs)
        self._running = True
        self.callback = self._kwargs.pop("callback", None)
        self._result = None

    def run(self):
        self._result = self._target(*self._args, **self._kwargs)
        self._result = (
            self.callback(self._result) if callable(self.callback) else self._result
        )

    @property
    def result(self):
        """获取当前线程结果"""
        return self.getResult()

    def getResult(self):
        """获取当前线程结果"""
        try:
            self.join()
            return self._result
        except Exception:
            raise Exception

    def wait(self):
        """等待线程执行完毕"""
        self.join()

    def stop(self):
        """停止线程"""
        self._running = False


def thread_decorator(
    func: Callable[..., Any] | None = None,
    *,
    daemon: bool = False,
    exception_handler: Callable[[Exception], Any] | None = None,
) -> Callable[..., Thread]:
    """增强型线程装饰器
    函数的线程装饰器,返回线程实例,\n
    有无括号都可以,getResult获取结果,\n
    可在调用被装饰函数添加daemon=True,callback等参数
    :param daemon: 是否设置为守护线程
    :param exception_handler: 自定义异常处理器
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Thread]:
        def wrapper(*args: Any, **kwargs: Any) -> Thread:
            _thread = _ThreadSafeDecoratorBase(
                fn, *args, **kwargs
            )
            _thread.daemon = kwargs.pop("daemon", False)
            _thread.start()
            print(f"func `{fn.__name__}` start with thread_decorator")
            return _thread

        return wrapper

    return decorator(func) if func else decorator

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
    """
    类似 thread_decorator 的线程装饰器
    函数的线程装饰器,无括号(),返回线程实例,
    getResult获取结果,getAllResult获取结果集合,
    可在调用被装饰函数添加daemon=True,callback等参数
    """

    thread_dict = {}

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        _mythr = _ThreadSafeDecoratorBase(
            self.func, *args, **kwargs
        )
        _mythr.daemon = kwargs.pop("daemon", False)
        _mythr.start()
        print(
            f"func `{self.func.__name__}` start with ThreadDecoratorClass"
        )
        self.thread_dict[_mythr.ident] = _mythr
        _mythr.getAllResult = self.getAllResult  # 绑定方法
        return _mythr

    @classmethod
    def getAllResult(cls):
        """获取全部结果，并清空缓存"""
        results = {}
        for thr in cls.thread_dict.values():
            thr.join()
            results[thr.ident] = thr.getResult()
        return results


def create_mixin_class(name, cls, meta, **kwargs):
    """type动态混入继承,实质是调整 bases"""
    return type(name, (cls, meta), kwargs)


thread_print = thread_safe(print)

if __name__ == "__main__":


    @ThreadDecoratorClass
    def b(i):
        return i * 5

    @thread_decorator
    def c(i):
        print(9999999999999, "in c", i)
        return i * 4

    bb = b(8)
    thread_print("Result:", bb.getResult())
    thread_print("Result2:", bb.result)
    thread_print(bb.getAllResult())

    cc = c(4, callback=lambda x: x * 11)
    thread_print("Result:", cc.getResult())
    thread_print("Result2:", cc.result)

    @parallelize_decorator
    def parallel_task(x):
        return x**3

    # thread_print(parallel_task(list(range(10))))

    class MyClass:
        @thread_safe
        def samethod(self, message):
            print(f"MyClass func with message: {message}")

    # my_instance = MyClass()

    # for i in range(3):
    #     t = my_instance.samethod(f"Thread {i}")
    # ThreadSafe(c)("ThreadSafe C")
    # ThreadSafe(print)("ThreadSafe print")

    
