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

import time
from functools import wraps
from time import perf_counter

from wrapt import decorator
from xt_log import LogCls, create_basemsg, log_decor


def retry(max_retry=3, delay=0.1):
    """重试装饰器"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for index in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    print(f"| retry {index}/{max_retry} times | <Error:{err!r}>")
                    if index + 1 == max_retry:
                        print(f"| retry | Exception | MaxRetryError | <Error:{err!r}>")
                        return err
                    else:
                        time.sleep(delay)

        return wrapper

    return decorator


def retry_log_wrapper(max_retry=3, exception=Exception, interval=0.1):
    """
    自编函数重试装饰器,记录日志
    :param max_retry: 重试次数
    :param exception: 需要重试的异常
    :param interval: 重试间隔时间
    :return:
    """

    def out_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = LogCls()
            base_log_msg = create_basemsg(func)
            logger(f"{base_log_msg} | <Args:{args!r}> | <Kwargs:{kwargs!r}>")
            duration = perf_counter()
            index = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    logger(
                        f"{base_log_msg} | <Result:{result!r}> | <Used time:{perf_counter() - duration:.4f}s>"
                    )
                    return result
                except exception as err:
                    logger(
                        f"{base_log_msg} | RLW retry {index}/{max_retry} times | <Error:{err!r}>"
                    )
                    index += 1
                    if index >= max_retry:
                        logger(
                            err_str
                            := f"{base_log_msg} | RLW Exception | MaxRetryError | <Raise:{err!r}> | <Used time:{perf_counter() - duration:.4f}s>"
                        )
                        return err_str
                    else:
                        time.sleep(interval)

        return wrapper

    return out_wrapper


def retry_log_by_tenacity(max_retry=3):
    """tenacity.retry重试装饰器,处理异常,记录日志,括号调用"""

    @decorator
    def wrapper(wrapped, instance, args, kwargs):
        from tenacity import retry, stop_after_attempt, wait_random

        @retry(reraise=True, stop=stop_after_attempt(max_retry), wait=wait_random())
        def retry_function():
            return log_decor(wrapped)(*args, **kwargs)  # type: ignore

        duration = perf_counter()
        try:
            result = retry_function()
            return result
        except Exception as err:
            logger = LogCls()
            logger(
                err_str
                := f"{create_basemsg(wrapped)} | RLCD Exception | MaxRetryError | <Raise:{err!r}> | <Used time:{perf_counter() - duration:.4f}s>"
            )
            return err_str

    return wrapper


if __name__ == "__main__":

    @retry()
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

    print(test())
    # print(test2())
    # print(get_html())
