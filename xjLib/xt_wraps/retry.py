# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-09-16 09:24:31
LastEditTime : 2025-08-29 09:18:49
FilePath     : /CODE/xjLib/xt_decorators/retry.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import random
import time
from typing import Any, Callable, Tuple, Type

from tenacity import (
    AsyncRetrying,
    RetryCallState,
    retry,
    retry_always,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random,
)
from xt_wraps import LogCls, create_basemsg, decorate_sync_async, func_sync_async

mylog = LogCls().logger

class RetryRaise:
    # 不重试异常
    NO_RETRY_EXCEPT = (ValueError, ZeroDivisionError)
    _basemsg :str= ""

    @classmethod
    def _raise(cls, retry_state: RetryCallState) -> str:
        ex = retry_state.outcome.exception()
        mylog.error(f"{cls._basemsg} | RetryRaise | 共 {retry_state.attempt_number} 次尝试失败，最后错误是: {retry_state.outcome.exception() if ex else '无'}")


    @classmethod
    def _before_sleep(cls, retry_state: RetryCallState, *args, **kwargs) -> None:
        mylog.error(
            f"{cls._basemsg} | RetryRaise | 第 {retry_state.attempt_number} 次尝试失败, 捕获到异常: {retry_state.outcome.exception()}"
        )


def retry_wraps(
    max_attempts: int = 3,
    min_wait: float = 0,
    max_wait: float = 1,
    is_not_retry_exceptions: bool = True,
    not_retry_exceptions: Tuple[Type[Exception], ...] = RetryRaise.NO_RETRY_EXCEPT,
    is_before_sleep: bool = True,
    before_sleep: Callable[[Any], None] | None = RetryRaise._before_sleep,
    is_error_callback: bool = True,
    retry_error_callback: Callable[[Any], Any] | None = RetryRaise._raise,
) -> Callable:
    """
    重试装饰器 - 同时支持同步和异步函数的重试逻辑
    使用decorate_sync_async处理函数的同步/异步执行

    Args:
        max_attempts: 最大尝试次数
        min_wait: 最小等待时间(秒)
        max_wait: 最大等待时间(秒)
        is_not_retry_exceptions: 是否不重试指定异常
        not_retry_exceptions: 不重试的异常类型元组
        is_before_sleep: 是否在每次重试前调用before_sleep
        before_sleep: 每次重试前调用的函数
        is_error_callback: 是否在重试失败时调用retry_error_callback
        retry_error_callback: 重试失败时调用的函数
    """
    @decorate_sync_async
    def wrapper(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        # 确定重试条件
        retry_condition = (
            retry_if_not_exception_type(not_retry_exceptions)
            if is_not_retry_exceptions
            else retry_always
        )
        RetryRaise._basemsg = create_basemsg(func)

        # 检查函数是否是异步的
        is_async = asyncio.iscoroutinefunction(func)

        if is_async:
            # 对于异步函数，使用异步重试
            async def async_retry_func():
                async for attempt in AsyncRetrying(
                    reraise=True,
                    stop=stop_after_attempt(max_attempts),
                    wait=wait_random(min=min_wait, max=max_wait),
                    retry=retry_condition,
                    before_sleep=before_sleep if is_before_sleep else None,
                    retry_error_callback=retry_error_callback
                    if is_error_callback
                    else None,
                ):
                    with attempt:
                        return await func(*args, **kwargs)

            return async_retry_func()

        else:
            # 对于同步函数，使用同步重试
            @retry(
                reraise=True,
                stop=stop_after_attempt(max_attempts),
                wait=wait_random(min=min_wait, max=max_wait),
                retry=retry_condition,
                before_sleep=before_sleep if is_before_sleep else None,
                retry_error_callback=retry_error_callback
                if is_error_callback
                else None,
            )
            def sync_retry_func():
                return func(*args, **kwargs)

            return sync_retry_func()

    return wrapper


def retry_deco(
    func: Callable[..., Any] | None = None,
    max_attempts=3,
    base_delay=1,
    max_delay=60,
    allowed_exceptions=(Exception,),
    retry_condition=None,
):
    """增强版重试装饰器，支持同步和异步函数的重试逻辑"""

    def decorator(func):
        # 创建一个内部函数来处理同步和异步执行
        @func_sync_async
        def retry_decorator(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            # 自定义条件检查
            if retry_condition and not retry_condition(result):
                return result
            return result

        # 创建一个外部包装器来处理重试逻辑
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            while retries < max_attempts:
                try:
                    return retry_decorator(*args, **kwargs)
                except allowed_exceptions:
                    retries += 1
                    if retries == max_attempts:
                        raise
                    # 指数退避+随机抖动
                    sleep_time = min(base_delay * (2 ** (retries - 1)), max_delay)
                    sleep_time *= 0.5 + random.random()  # 添加150%以内的随机因子
                    time.sleep(sleep_time)
                except Exception:
                    # 非预期异常立即抛出
                    raise
            return None

        # 保留原函数的元数据
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper

    return decorator(func) if func else decorator

if __name__ == "__main__":

    @retry_deco
    def test(*args):
        raise RuntimeError("raise by test_func")
        # raise ValueError("raise by test_func")
        return "同步函数成功"

    print(1111111,test())

    # 同步函数示例
    @retry_deco()
    def sync_function():
        raise Exception("同步随机失败")
        return "同步函数成功"
    
    print(222222, sync_function())

    # 异步函数示例
    @retry_deco()
    async def async_function():
        raise Exception("异步随机失败")
        return "异步函数成功"

    import asyncio

    print(3333333, asyncio.run(async_function()))
