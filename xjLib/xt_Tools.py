# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 18:42:56
#FilePath     : /xjLib/xt_Tools.py
#LastEditTime : 2020-06-05 22:07:44
#Github       : https://github.com/sandorn/home
#==============================================================

拒绝重复造轮子！python实用工具类及函数大推荐！ - 知乎
https://zhuanlan.zhihu.com/p/31644562
https://github.com/ShichaoMa
'''

import time
import traceback
import signal
from functools import wraps


class ExceptContext(object):
    """
    异常捕获上下文
        with ExceptContext(Exception, errback=lambda name, *args:print(name)):
            raise Exception("test. ..")
    """

    def __init__(self, exception=Exception, func_name=None, errback=lambda func_name, *args: traceback.print_exception(*args) is None, finalback=lambda got_err: got_err):
        """
        :param exception: 指定要监控的异常
        :param func_name: 可以选择提供当前所在函数的名称，回调函数会提交到函数，用于跟踪
        :param errback: 提供一个回调函数，如果发生了指定异常，就调用该函数，该函数的返回值为True时不会继续抛出异常
        :param finalback: finally要做的操作
        """
        self.errback = errback
        self.finalback = finalback
        self.exception = exception
        self.got_err = False
        self.func_name = func_name  # or _find_caller_name(is_func=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return_code = False
        if isinstance(exc_val, self.exception):
            self.got_err = True
            return_code = self.errback(self.func_name, exc_type, exc_val, exc_tb)
        self.finalback(self.got_err)
        return return_code


def timeout(timeout_time, default):
    """超时器，装饰函数并指定其超时时间"""

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


def call_later(callback, call_args=tuple(), immediately=True, interval=1):
    """
    应用场景：
    被装饰的方法需要大量调用，随后需要调用保存方法，但是因为被装饰的方法访问量很高，而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后，再调用保存方法。规定间隔内，无论调用多少次被装饰方法，保存方法只会
    调用一次，除非immediately=True
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


if __name__ == '__main__':
    pass
