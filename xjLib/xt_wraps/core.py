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

import asyncio
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast

T = TypeVar("T", bound=Callable[..., Any])


def decorate_sas(decorator_func: Callable) -> Callable:
    """
    使装饰器同时支持同步和异步函数的装饰器工厂 - 原始版本
    """

    @wraps(decorator_func)
    def wrapper(func: T) -> T:
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            return await decorator_func(func, *args, **kwargs)

        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            return decorator_func(func, *args, **kwargs)

        # 检查函数是否是异步的
        return (
            cast(T, async_wrapped)
            if asyncio.iscoroutinefunction(func)
            else cast(T, sync_wrapped)
        )
    return wrapper

def decorate_sync_async(
    decorator_func: Optional[Callable] = None, **decorator_kwargs
) -> Callable:
    """
    增强版装饰器工厂 - 同时支持同步和异步函数，支持可选参数和无参数装饰器模式

    特性:
    - 支持同步和异步函数的装饰
    - 支持带参数和不带参数的装饰器模式
    - 保留原函数的元数据
    - 可自定义同步和异步装饰逻辑

    Args:
        decorator_func: 装饰器函数，如果为None则返回一个接受装饰器函数的函数
        **decorator_kwargs: 传递给装饰器的额外参数

    Returns:
        装饰器函数
    """

    # 处理无参数装饰器模式 @decorate_sync_async
    if decorator_func is None:

        def decorator_wrapper(func: Callable) -> Callable:
            return decorate_sync_async(func, **decorator_kwargs)

        return decorator_wrapper

    @wraps(decorator_func)
    def decorator(func: T) -> T:
        # 定义异步包装函数
        @wraps(func)
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            # 如果装饰器函数接受func作为第一个参数
            if decorator_func.__code__.co_argcount > 0:
                return await decorator_func(func, *args, **kwargs)
            else:
                # 直接调用装饰后的函数
                decorated_func = decorator_func(**decorator_kwargs)
                if asyncio.iscoroutinefunction(decorated_func):
                    return await decorated_func(*args, **kwargs)
                else:
                    return decorated_func(*args, **kwargs)

        # 定义同步包装函数
        @wraps(func)
        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            # 如果装饰器函数接受func作为第一个参数
            if decorator_func.__code__.co_argcount > 0:
                return decorator_func(func, *args, **kwargs)
            else:
                # 直接调用装饰后的函数
                decorated_func = decorator_func(**decorator_kwargs)
                return decorated_func(*args, **kwargs)

        # 检查函数是否是异步的
        return (
            cast(T, async_wrapped)
            if asyncio.iscoroutinefunction(func)
            else cast(T, sync_wrapped)
        )

    return decorator
