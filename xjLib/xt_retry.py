# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-16 09:24:31
LastEditTime : 2024-09-18 11:39:57
FilePath     : /CODE/xjLib/xt_retry.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from functools import partial, wraps
from time import perf_counter, sleep

from wrapt import ObjectProxy, decorator
from xt_log import LogCls, create_basemsg, log_decor


def retry_wraper(wrapped=None, max_retry=3, delay=0.1):
    """重试装饰器，有无括号都可以"""
    if wrapped is None:
        return partial(retry_wraper, max_retry=max_retry, delay=delay)

    @decorator
    def wrapper(wrapped, instance, args, kwargs):
        for retries in range(max_retry):
            try:
                return wrapped(*args, **kwargs)
            except Exception as err:
                print(f"| retry_wraper {retries}/{max_retry} times | <Error:{err!r}>")
                if retries + 1 >= max_retry:
                    print(f"| retry_wraper Exception | MaxRetryError | <Error:{err!r}>")
                    # raise  # 抛出异常以便外部捕获
                    return err
                sleep(delay)

    return wrapper(wrapped)


def retry_wrapper(wrapped=None, max_retry=3, delay=0.1):
    """重试装饰器，使用functools.wraps,有无括号都可以"""
    if wrapped is None:
        return partial(retry_wrapper, max_retry=max_retry, delay=delay)

    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        for retries in range(max_retry):
            try:
                return wrapped(*args, **kwargs)
            except Exception as err:
                print(
                    f"| retry_wrapper {retries + 1}/{max_retry} times | <Error:{err!r}>"
                )
                if retries + 1 == max_retry:
                    print(
                        f"| retry_wrapper Exception | MaxRetryError | <Error:{err!r}>"
                    )
                    raise  # 抛出异常以便外部捕获
                sleep(delay)

    return wrapper


def retry_log_wrapper(max_retry=3, interval=0.1):
    """
    可以处理异步函数
    自编函数重试装饰器,记录日志
    :param max_retry: 重试次数
    :param interval: 重试间隔时间
    """

    def out_wrapper(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def coroutine_wrapper(*args, **kwargs):
                logger = LogCls()
                base_log_msg = create_basemsg(func)
                logger(f"{base_log_msg} | <Args:{args!r}> | <Kwargs:{kwargs!r}>")
                duration = perf_counter()
                retries = 0
                while True:
                    try:
                        result = await func(*args, **kwargs)
                        logger(
                            f"{base_log_msg} | <Result:{result!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
                        )
                        return result
                    except Exception as err:
                        logger(
                            f"{base_log_msg} | retry_log_wrapper retry {retries}/{max_retry} times | <Error:{err!r}>"
                        )
                        retries += 1
                        if retries >= max_retry:
                            logger(
                                err_str
                                := f"{base_log_msg} | retry_log_wrapper Exception | MaxRetryError | <Raise:{err!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
                            )
                            return err_str
                        else:
                            await asyncio.sleep(interval)

            return coroutine_wrapper

        else:

            @wraps(func)
            def wrapper(*args, **kwargs):
                logger = LogCls()
                base_log_msg = create_basemsg(func)
                logger(f"{base_log_msg} | <Args:{args!r}> | <Kwargs:{kwargs!r}>")
                duration = perf_counter()
                retries = 0
                while True:
                    try:
                        result = func(*args, **kwargs)
                        logger(
                            f"{base_log_msg} | <Result:{result!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
                        )
                        return result
                    except Exception as err:
                        logger(
                            f"{base_log_msg} | retry_log_wrapper retry {retries}/{max_retry} times | <Error:{err!r}>"
                        )
                        retries += 1
                        if retries >= max_retry:
                            logger(
                                err_str
                                := f"{base_log_msg} | retry_log_wrapper Exception | MaxRetryError | <Raise:{err!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
                            )
                            return err_str
                        else:
                            sleep(interval)

            return wrapper

    return out_wrapper


class RetryLogWrapper(ObjectProxy):
    def __init__(self, wrapped, max_retry=3, interval=0.1):
        super().__init__(wrapped)
        self.max_retry = max_retry
        self.interval = interval
        self.logger = LogCls()
        self.base_log_msg = create_basemsg(wrapped)

    def __call__(self, *args, **kwargs):
        self.retries = 0
        self.logger(f"{self.base_log_msg} | <Args:{args!r}> | <Kwargs:{kwargs!r}>")
        duration = perf_counter()
        while self.retries < self.max_retry:
            try:
                result = self.__wrapped__(*args, **kwargs)
                self.used_time = perf_counter() - duration
                self.logger(
                    f"{self.base_log_msg} | <Result:{result!r}> | <Time-Consuming:{self.used_time:.4f}s>"
                )
                return result
            except Exception as err:
                self.used_time = perf_counter() - duration
                self.err = err
                self.logger(
                    f"{self.base_log_msg} | RetryLogWrapper retry {self.retries}/{self.max_retry} times | <Error:{err!r}>"
                )
                self.retries += 1
                sleep(self.interval)

        self.logger(
            err_str
            := f"{self.base_log_msg} | RetryLogWrapper Exception | MaxRetryError | <Raise:{self.err!r}> | <Time-Consuming:{self.used_time:.4f}s>"
        )
        return err_str


def retry_log_by_tenacity(wrapped=None, max_retry=3):
    """tenacity.retry重试装饰器,处理异常,记录日志,有无括号都可以"""
    if wrapped is None:
        return partial(retry_log_by_tenacity, max_retry=max_retry)

    @decorator
    def wrapper(wrapped, instance, args, kwargs):
        from tenacity import retry, stop_after_attempt, wait_random

        @retry(reraise=True, stop=stop_after_attempt(max_retry), wait=wait_random())
        def retry_function():
            return log_decor(wrapped)(*args, **kwargs)  # type: ignore

        duration = perf_counter()
        try:
            return retry_function()
        except Exception as err:
            used_time = perf_counter() - duration
            logger = LogCls()
            logger(
                err_str
                := f"{create_basemsg(wrapped)} | retry_log_by_tenacity Exception | MaxRetryError | <Raise:{err!r}> | <Time-Consuming:{used_time:.4f}s>"
            )
            return err_str

    return wrapper(wrapped)


if __name__ == "__main__":

    @retry_wraper
    @log_decor
    def test(*args):
        return 1 / 0
        raise ValueError("raise by test_func")

    @retry_log_wrapper()
    def test2(*args):
        raise ValueError("raise by test2_func")

    @retry_log_by_tenacity()
    def get_html(*args):
        raise ValueError("raise by get_html")
        import requests

        return requests.get("https://www.google.com")

    # print(test())
    print(test2())
    # print(get_html())
