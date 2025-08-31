# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 11:06:38
LastEditTime : 2025-08-29 18:56:44
FilePath     : /CODE/xjLib/xt_wraps/core.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import inspect
from functools import wraps
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T", bound=Callable[..., Any])


def decorate_sync_async(decorator_func: Callable) -> Callable:
    """
    使装饰器同时支持同步和异步函数的装饰器工厂
    """

    @wraps(decorator_func)
    def wrapper(func: T) -> T:
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            return await decorator_func(func, *args, **kwargs)

        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            return decorator_func(func, *args, **kwargs)

        # 检查函数是否是异步的
        if inspect.iscoroutinefunction(func):
            return cast(T, async_wrapped)
        else:
            return cast(T, sync_wrapped)
    return wrapper


def func_sync_async(func: T) -> T:
    """
    直接修饰函数的装饰器工厂，使其能够同时支持同步和异步函数的执行
    用于其他装饰器的最内层，处理同步/异步函数的执行逻辑
    """
    # 如果函数已经是异步的，直接返回
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            # 直接执行原始异步函数
            return await func(*args, **kwargs)
        return cast(T, async_wrapped)
    else:
        # 如果是同步函数，保持原样返回
        return func
