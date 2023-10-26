# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : 函数超时、函数默认值装饰、动态创建函数、重试装饰器2种、获取对象帮助
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 18:42:56
#FilePath     : /xjLib/xt_Tools.py
#LastEditTime : 2020-07-30 12:43:08
#Github       : https://github.com/sandorn/home
#==============================================================
拒绝重复造轮子!python实用工具类及函数大推荐! - 知乎
https://zhuanlan.zhihu.com/p/31644562
https://github.com/ShichaoMa
'''

import functools
import logging
import signal
import time
import traceback
from copy import deepcopy
from functools import reduce, wraps
from types import FunctionType
from typing import Any, Callable, Type


class ExceptContext:

    def __init__(
        self,
        exception: Type[Exception] = Exception,
        func_name: str = "",
        errback=None,
        finalback=None,
    ):
        """
        Initialize the ExceptContext object.
        :param exception: The type of exception to monitor.
        :param func_name: The name of the current function being traced.
        :param errback: A callback function to be called when the specified exception occurs.
        :param finalback: A final callback function to be executed after all processing is done.
        """
        if errback is None:
            errback = self.default_errback
        if finalback is None:
            finalback = self.default_finalback
        self.errback = errback
        self.finalback = finalback
        self.exception = exception
        self.has_error = False
        self.func_name = func_name

    def __enter__(self):
        """
        Enter the context block.
        :return: The ExceptContext object itself.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context block.
        :param exc_type: The type of the raised exception.
        :param exc_val: The value of the raised exception.
        :param exc_tb: The traceback of the raised exception.
        :return: True if the exception was handled; False otherwise.
        """
        if isinstance(exc_val, self.exception):
            self.has_error = True
            return_code = self.errback(self.func_name, exc_type, exc_val,
                                       exc_tb)
        else:
            return_code = False
        self.finalback(self.has_error)
        return return_code

    def __call__(self, func):
        """
        Use the ExceptContext object as a decorator.
        :param func: The function to be decorated.
        :return: The decorated function.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def default_errback(func_name, exc_type, exc_val, exc_tb):
        """
        The default callback function for handling exceptions.
        :param func_name: The name of the function where the exception occurred.
        :param exc_type: The type of the raised exception.
        :param exc_val: The value of the raised exception.
        :param exc_tb: The traceback of the raised exception.
        :return: True if the exception was handled; False otherwise.
        """
        logging.exception(f"Exception in {func_name}: {exc_val}")
        return True

    @staticmethod
    def default_finalback(has_error: bool):
        """
        The default callback function for final processing.
        :param has_error: Whether an exception occurred or not.
        """
        pass


def timeout0(timeout_time, default):
    """超时器,装饰函数并指定其超时时间"""

    class DecoratorTimeout(Exception):
        pass

    def timeout_function(func):

        def function(*args):

            def timeout_handler(signum, frame):
                raise DecoratorTimeout()

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout_time)
            try:
                result = func(*args)
            except DecoratorTimeout:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)
            return result

        return function

    return timeout_function


def timeout(timeout_time: int, default: Any):
    """超时装饰器，用于为被装饰的函数设置超时时间。

    Args:
        timeout_time (int): 超时时间，以秒为单位。
        default (Any): 默认返回值。

    Returns:
        Callable[..., Any]: 被装饰后的函数。
    """

    class DecoratorTimeout(Exception):
        pass

    def timeout_function(func: Callable[..., Any]) -> Callable[..., Any]:

        @functools.wraps(func)
        def function(*args, **kwargs) -> Any:

            def timeout_handler(signum, frame):
                raise DecoratorTimeout()

            old_handler = signal.signal(signal.SIGINT, timeout_handler)
            signal.alarm(timeout_time)

            with signal_timeout_cleanup(signal.SIGINT, old_handler):
                return func(*args, **kwargs)

        return function

    return timeout_function


class signal_timeout_cleanup:
    """Context manager to ensure a signal is set back to its original state."""

    def __init__(self, signum, handler):
        self.signum = signum
        self.handler = handler

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)
        signal.signal(self.signum, self.handler)


def call_later(callback, call_args=tuple(), immediately=True, interval=1):
    """
    应用场景：
    被装饰的方法需要大量调用,随后需要调用保存方法,但是因为被装饰的方法访问量很高,而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后,再调用保存方法。规定间隔内,无论调用多少次被装饰方法,保存方法只会
    调用一次,除非  immediately=True
    :param callback: 随后需要调用的方法名
    :param call_args: 随后需要调用的方法所需要的参数
    :param immediately: 是否立即调用
    :param interval: 调用间隔
    :return:
    """

    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return func(*args, **kwargs)
            finally:
                if immediately:
                    getattr(self, callback)(*call_args)
                else:
                    now = time.time()
                    if now - self.__dict__.get("last_call_time", 0) > interval:
                        getattr(self, callback)(*call_args)
                        self.__dict__["last_call_time"] = now

        return wrapper

    return decorate


def freshdefault(func):
    '''装饰函数,使可变对象可以作为默认值'''
    # 保存函数的默认值
    fdefaults = func.__defaults__
    # 保存函数注解
    ftypes = func.__annotations__

    def refresher(*args, **kwds):
        if fdefaults:
            # 恢复函数的默认值
            func.__defaults__ = deepcopy(fdefaults)
        if ftypes:
            # 恢复函数的注解
            for key in ftypes.keys():
                if key not in kwds.keys():
                    kwds[key] = deepcopy(ftypes[key])
        return func(*args, **kwds)

    return refresher


def _create_func(code_body, **kwargs):
    '''动态函数创建器'''
    kwargs.setdefault('globals', {})
    filename = kwargs.pop('filename', 'xt_Tools._create_func')
    exmethod = kwargs.pop('exmethod', 'exec')
    module_code = compile(code_body, filename, exmethod)
    return FunctionType(module_code.co_consts[0], **kwargs)

    # FunctionType(code, globals, name=None, argdefs=None, closure=None)


func_attr_name_list = [
    # #函数的内置属性
    '__closure__',
    '__code__',
    '__defaults__',
    '__dict__',
    '__doc__',
    '__globals__',
    '__name__',
]
func_code_name_list = [
    # #函数.__code__的内置属性
    'co_argcount',
    'co_cellvars',
    'co_code',
    'co_consts',
    'co_filename',
    'co_firstlineno',
    'co_flags',
    'co_freevars',
    'co_kwonlyargcount',
    'co_lnotab',
    'co_name',
    'co_names',
    'co_nlocals',
    'co_posonlyargcount',
    'co_stacksize',
    'co_varnames',
]


def catch_wraps(func, bool=False):
    '''捕捉异常的装饰器'''

    def wrapper(*args, **keyargs):
        try:
            return func(*args, **keyargs)
        except Exception as err:
            print(f'catch_wraps: [{func.__name__}]\tError: {err!r}')
            if bool: traceback.print_exc()
            return None

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__dict__.update(func.__dict__)
    return wrapper


def try_except_wraps(fn=None,
                     max_retries: int = 6,
                     delay: float = 0.2,
                     step: float = 0.1,
                     exceptions: (BaseException, tuple, list) = BaseException,
                     sleep=time.sleep,
                     process=lambda ex: True,
                     validate=None,
                     callback=None,
                     default=None):
    """
        函数执行出现异常时自动重试的简单装饰器
        :param f: function 执行的函数。
        :param max_retries: int 最多重试次数。
        :param delay: int/float 每次重试的延迟,单位秒。
        :param step: int/float 每次重试后延迟递增,单位秒。
        :param exceptions: BaseException/tuple/list 触发重试的异常类型,单个异常直接传入异常类型,多个异常以tuple或list传入。
        :param sleep: 实现延迟的方法,默认为time.sleep。
        在一些异步框架,如tornado中,使用time.sleep会导致阻塞,可以传入自定义的方法来实现延迟。
        自定义方法函数签名应与time.sleep相同,接收一个参数,为延迟执行的时间。
        :param process: 处理函数,函数签名应接收一个参数,每次出现异常时,会将异常对象传入。
        可用于记录异常日志,中断重试等。
        如处理函数正常执行,并返回True,则表示告知重试装饰器异常已经处理,重试装饰器终止重试,并且不会抛出任何异常。
        如处理函数正常执行,没有返回值或返回除True以外的结果,则继续重试。
        如处理函数抛出异常,则终止重试,并将处理函数的异常抛出。
        :param validate: 验证函数,用于验证执行结果,并确认是否继续重试。
        函数签名应接收一个参数,每次被装饰的函数完成且未抛出任何异常时,调用验证函数,将执行的结果传入。
        如验证函数正常执行,且返回False,则继续重试,即使被装饰的函数完成且未抛出任何异常。
        如验证函数正常执行,没有返回值或返回除False以外的结果,则终止重试,并将函数执行结果返回。
        如验证函数抛出异常,且异常属于被重试装饰器捕获的类型,则继续重试。
        如验证函数抛出异常,且异常不属于被重试装饰器捕获的类型,则将验证函数的异常抛出。
        :param callback: 回调函数,处理结果。
        :param default: 默认值/默认值生成函数
        :return: 被装饰函数的执行结果。
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            func_exc = None
            for index in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if callable(validate) and validate(result) is False:
                        continue
                    # #回调函数,处理结果
                    return callback(result) if callable(callback) else result
                except exceptions as ex:
                    func_exc, _ = ex, traceback.format_exc()
                    sleep(delay + step * index)  # #延迟重试
            # #重试次数使用完毕,结果错误,返回默认值
            print(f'try_except_wraps: [{func.__name__}]\tError: {func_exc!r}')
            if callable(process) and process(func_exc) is True:
                return default() if callable(default) else default

        return wrapper

    return decorator(fn) if callable(fn) else decorator


def retry_on_exception(func, max_retry=3):
    """Retry 3 times if the function throws an exception."""

    def wrapper(*args, **kwargs):
        for _ in range(max_retry):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                time.sleep(1)
        return None

    return wrapper


if __name__ == '__main__':

    def trys():

        @catch_wraps
        def simple():
            return 5 / 0

        @catch_wraps
        def readFile(filename):
            with open(filename, "r") as f:
                print(len(f.readlines()))

        def add(a, b):
            with ExceptContext():
                return (int(a) / int(b))

        @try_except_wraps
        def assertSumIsPositive(*args):
            print('222222,assertSumIsPositive')
            _sum = reduce(add, *args)
            assert _sum >= 0

        @try_except_wraps()
        def checkLen(**keyargs):
            print('333333,checkLen')
            if len(keyargs) < 3:
                raise ValueError('Number of key args should more than 3.')

        simple()
        readFile("UnexistFile.txt")
        print(add(1, 0))
        # assertSumIsPositive(1, 2, -3, -4)
        # checkLen(a=5, b=2)

    def fre():
        # 可变对象默认装饰器
        @freshdefault
        def extend_list(v, li=[]):
            li.append(v)
            # print(li)
            return li

        list1 = extend_list(10)
        list2 = extend_list(123, [])
        list3 = extend_list('a')
        print(list1)
        print(list2)
        print(list3)

        print(list1 is list3)

    def fu():
        # #函数创建器
        foo_func = _create_func('def foo():a=3;return 3')

        print(foo_func())

        for attr in func_attr_name_list:
            print(attr, ':', getattr(foo_func, attr))

        for attr in func_code_name_list:
            print(
                f'foo_func.__code__.{attr.ljust(33)}',
                ':',
                getattr(foo_func.__code__, attr),
            )
        print(_create_func.__dict__)

    trys()
    # fre()
    # fu()
