# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 18:42:56
#LastEditTime : 2020-06-03 19:02:05
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
拒绝重复造轮子！python实用工具类及函数大推荐！ - 知乎
https://zhuanlan.zhihu.com/p/31644562
https://github.com/ShichaoMa
'''
import re
import time
import traceback
import signal
from functools import reduce, wraps


class ExceptContext(object):
    """
    异常捕获上下文
    eg:
    def test():
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


def duplicate(iterable, keep=lambda x: x, key=lambda x: x, reverse=False):
    """
    保序去重
    :param iterable:
    :param keep: 去重的同时要对element做的操作
    :param key: 使用哪一部分去重
    :param reverse: 是否反向去重
    :return:
    """
    result = list()
    duplicator = list()
    if reverse:
        iterable = reversed(iterable)
    for i in iterable:
        keep_field = keep(i)
        key_words = key(i)
        if key_words not in duplicator:
            result.append(keep_field)
            duplicator.append(key_words)
    return list(reversed(result)) if reverse else result


def chain_all(iterobj):
    """
    连接多个序列或字典
    :param iter:
    :return:
    """
    iterobj = list(iterobj)
    if not iterobj:
        return []
    if isinstance(iterobj[0], dict):
        result = {}
        for i in iterobj:
            result.update(i)
    else:
        result = reduce(lambda x, y: list(x) + list(y), iterobj)
    return result


def format_html_string(html):
    """
    格式化html, 去掉多余的字符，类，script等。
    :param html:
    :return:
    """
    trims = [(r'\n', ''), (r'\t', ''), (r'\r', ''), (r'  ', ''), (r'\u2018', "'"), (r'\u2019', "'"), (r'\ufeff', ''), (r'\u2022', ":"), (r"<([a-z][a-z0-9]*)\ [^>]*>", '<\g<1>>'), (r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', ''), (r"</?a.*?>", '')]
    return reduce(lambda string, replacement: re.sub(replacement[0], replacement[1], string), trims, html)


def retry_wrapper(retry_times, exception=Exception, error_handler=None, interval=0.1):
    """
    函数重试装饰器
    :param retry_times: 重试次数
    :param exception: 需要重试的异常
    :param error_handler: 出错时的回调函数
    :param interval: 重试间隔时间
    :return:
    """

    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    count += 1
                    if error_handler:
                        result = error_handler(func.__name__, count, e, *args, **kwargs)
                        if result:
                            count -= 1
                    if count >= retry_times:
                        raise
                    time.sleep(interval)

        return wrapper

    return out_wrapper


def timeout(timeout_time, default):
    """
    超时器，装饰函数并指定其超时时间
    Decorate a method so it is required to execute in a given time period,
    or return a default value.
    :param timeout_time:
    :param default:
    :return:
    """

    class DecoratorTimeout(Exception):
        pass

    def timeout_function(f):
        def f2(*args):
            def timeout_handler(signum, frame):
                raise DecoratorTimeout()

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            # triger alarm in timeout_time seconds
            signal.alarm(timeout_time)
            try:
                retval = f(*args)
            except DecoratorTimeout:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler)
            signal.alarm(0)
            return retval

        return f2

    return timeout_function


def groupby(it, key):
    """
    自实现groupby，itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    :return: 字典对象
    """
    groups = dict()
    for item in it:
        groups.setdefault(key(item), []).append(item)
    return groups


def thread_safe(lock):
    """
    对指定函数进行线程安全包装，需要提供锁
    :param lock: 锁
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return wrapper

    return decorate


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
    li = [3, 7, 6, 1, 9, 4, 6, 3, 1, 7, 2, 3, 8]
    print(duplicate(li))
    print(chain_all([[1, 2], [1, 2]]))
