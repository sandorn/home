# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-03-03 10:03:22
LastEditTime : 2025-08-22 10:16:33
FilePath     : /CODE/xjLib/xt_catch.py
Github       : https://github.com/sandorn/home
==============================================================

拒绝重复造轮子!python实用工具类及函数大推荐! - 知乎
https://zhuanlan.zhihu.com/p/31644562
https://github.com/ShichaoMa
"""

import time
import traceback
from functools import wraps
from types import TracebackType
from typing import Any, Callable, Optional, Type, TypeVar

from wrapt import decorator
from xt_log import create_basemsg

# 定义一个类型变量，表示任何可调用函数
F = TypeVar("F", bound=Callable[..., Any])


def call_later(callback, *call_args, immediately=True, interval=1):
    """
    应用场景：
    被装饰的方法需要大量调用，随后需要调用保存方法，但是因为被装饰的方法访问量很高，而保存方法开销很大
    所以设计在装饰方法持续调用一定间隔后，再调用保存方法。规定间隔内，无论调用多少次被装饰方法，保存方法只会
    调用一次,除非immediately=True
    :param callback: 随后需要调用的方法名
    :param call_args: 随后需要调用的方法所需要的参数
    :param immediately: 是否立即调用
    :param interval: 调用间隔
    :return:
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0] if args else None
            try:
                return func(*args, **kwargs)
            finally:
                if self is not None:
                    now = time.time()
                    last_call_time_key = f"_last_call_time_{callback}"
                    if immediately and not hasattr(self, last_call_time_key):
                        getattr(self, callback)(*call_args)
                        setattr(self, last_call_time_key, now)
                    elif now - getattr(self, last_call_time_key, 0) > interval:
                        getattr(self, callback)(*call_args)
                        setattr(self, last_call_time_key, now)

        return wrapper

    return decorate


class ExceptContext:
    def __init__(
        self,
        func_name: str = "",
        exception: Type[Exception] = Exception,
        errback: Optional[Callable[..., Any]] = None,
        finalback: Optional[Callable[..., Any]] = None,
    ):
        self.errback = errback or self.default_res_errback
        self.finalback = finalback or self.default_res_finalback
        self.exception = exception
        self.has_error = False
        self.func_name = func_name

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        if exc_val and isinstance(exc_val, self.exception):
            self.has_error = True
            return_code = self.errback(self.func_name, exc_type, exc_val, exc_tb)
        else:
            return_code = False
        self.finalback(self.has_error)
        return return_code

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @decorator
        def wrapper(
            func: Callable[..., Any],
            instance: Optional[Any],
            args: tuple[Any],
            kwargs: dict[Any, Any],
        ) -> Any:
            with self:
                return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def default_res_errback(
        func_name: str,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        print(f"ExceptContext Raise in Function[{func_name}]: {exc_val}, {exc_tb}")
        return True

    @staticmethod
    def default_res_finalback(has_error: bool) -> None:
        pass


def catch_wrapt(func):
    """异常处理装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            print(err_str := f"{create_basemsg(func)} | catch_wraps | Error:{err!r}")
            return err_str

    return wrapper


def try_except_wraps(
    max_retries=3,
    delay=0.2,
    step=0.1,
    sleep_fn=time.sleep,
    validate_fn=None,
    callback_fn=None,
    default_res=None,
) -> Callable[[F], F]:
    """
    函数执行出现异常时自动重试的简单装饰器
    :param f: function 执行的函数。
    :param max_retries: int 最多重试次数。
    :param delay: int/float 每次重试的延迟,单位秒。
    :param step: int/float 每次重试后延迟递增,单位秒。
    :param sleep_fn: 实现延迟的方法,默认为time.sleep_fn。
    在一些异步框架,如tornado中,使用time.sleep会导致阻塞,可以传入自定义的方法来实现延迟。
    自定义方法函数签名应与time.sleep相同,接收一个参数,为延迟执行的时间。
    可用于记录异常日志,中断重试等。
    如处理函数正常执行,并返回True,则表示告知重试装饰器异常已经处理,重试装饰器终止重试,并且不会抛出任何异常。
    如处理函数正常执行,没有返回值或返回除True以外的结果,则继续重试。
    如处理函数抛出异常,则终止重试,并将处理函数的异常抛出。
    :param validate_fn: 验证函数,用于验证执行结果,并确认是否继续重试。
    函数签名应接收一个参数,每次被装饰的函数完成且未抛出任何异常时,调用验证函数,将执行的结果传入。
    如验证函数正常执行,且返回False,则继续重试,即使被装饰的函数完成且未抛出任何异常。
    如验证函数正常执行,没有返回值或返回除False以外的结果,则终止重试,并将函数执行结果返回。
    如验证函数抛出异常,且异常属于被重试装饰器捕获的类型,则继续重试。
    如验证函数抛出异常,且异常不属于被重试装饰器捕获的类型,则将验证函数的异常抛出。
    :param callback_fn: 回调函数,处理结果。
    :param default_res: 默认值/默认值生成函数
    :return: 被装饰函数的执行结果。
    """

    @decorator
    def wrapper(wrapped, instance, args, kwargs):
        func_exc = ""
        err_str = default_res if default_res is not None else ""
        for index in range(max_retries):
            try:
                result = wrapped(*args, **kwargs)
                if callable(validate_fn) and validate_fn(result) is False:
                    continue
                return callback_fn(result) if callable(callback_fn) else result
            except Exception as ex:
                func_exc, _ = ex, traceback.format_exc()
                print(
                    err_str
                    := f"{create_basemsg(wrapped)} | try_except_wraps | Error: {func_exc!r}"
                )
                sleep_fn(delay + step * index)  # #延迟重试

        return default_res() if callable(default_res) else err_str

    return wrapper


if __name__ == "__main__":

    @catch_wrapt
    def example_function():
        raise ValueError("example_function异常")

    def add(a, b):
        with ExceptContext("add"):
            raise ValueError("add异常")

    @try_except_wraps()
    def retry_function():
        raise ValueError("retry_function异常")
        return 4

    print(1111111111, example_function())
    print(2222222222, add(123, 0))
    print(3333333333, retry_function())
