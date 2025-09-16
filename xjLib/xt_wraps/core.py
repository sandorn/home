# !/usr/bin/env python
"""
==============================================================
Description  : 核心装饰器工具模块 - 提供同步/异步函数通用装饰器工厂
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 11:06:38
LastEditTime : 2025-09-06 10:00:00
FilePath     : /CODE/xjlib/xt_wraps/core.py
Github       : https://github.com/sandorn/home

本模块提供了两个核心装饰器工厂函数，用于创建同时支持同步和异步函数的装饰器：
- decorate_sas: 基础版本，适用于简单的装饰器创建需求
- decorate_sync_async: 增强版本，支持带参数/无参数模式、内置异常处理、执行效率优化

使用场景：
- 构建通用装饰器库，简化同步/异步代码的装饰器实现
- 统一处理函数执行前后的逻辑，如日志记录、性能统计、异常处理等
- 优化异步环境下同步函数的执行方式，避免阻塞事件循环
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from .exception import handle_exception
from .log import create_basemsg

T = TypeVar('T', bound=Callable[..., Any])


def decorate_sas(decorator_func: Callable) -> Callable:
    """
    使装饰器同时支持同步和异步函数的装饰器工厂 - 基础版本

    Args:
        decorator_func: 装饰器函数，接收被装饰函数及其参数作为输入

    Returns:
        Callable: 返回一个新的装饰器，该装饰器可以同时装饰同步和异步函数

    Example:
        >>> def my_decorator(func, *args, **kwargs):
        ...     print(f'执行前: {func.__name__}')
        ...     result = func(*args, **kwargs)
        ...     print(f'执行后: {func.__name__}')
        ...     return result
        >>> my_sas_decorator = decorate_sas(my_decorator)
        >>> @my_sas_decorator
        ... def sync_func(x, y):
        ...     return x + y
        >>> @my_sas_decorator
        ... async def async_func(x, y):
        ...     await asyncio.sleep(0.1)
        ...     return x * y
    """

    @wraps(decorator_func)
    def wrapper(func: T) -> T:
        async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
            return await decorator_func(func, *args, **kwargs)

        def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
            return decorator_func(func, *args, **kwargs)

        # 根据函数类型返回对应的包装函数
        return cast(T, async_wrapped) if asyncio.iscoroutinefunction(func) else cast(T, sync_wrapped)

    return wrapper


def create_async_wrapper[T](decorator_func: Callable, func: T, decorator_kwargs: dict) -> Callable:
    # T 是被装饰函数的类型参数
    """创建异步包装函数"""

    @wraps(func)
    async def async_wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            # 判断装饰器函数的调用方式
            if decorator_func.__code__.co_argcount > 0:
                return await decorator_func(func, *args, **kwargs)
            # 直接调用装饰后的函数
            decorated_func = decorator_func(**decorator_kwargs)
            if asyncio.iscoroutinefunction(decorated_func):
                return await decorated_func(*args, **kwargs)
            # 对于同步装饰后的函数，使用run_in_executor确保不阻塞事件循环
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: decorated_func(*args, **kwargs))
        except Exception as err:
            # 异常处理并返回None，保持与同步行为一致
            handle_exception(create_basemsg(func), err)
            return None

    return async_wrapped


def create_sync_wrapper[T](decorator_func: Callable, func: T, decorator_kwargs: dict) -> Callable:
    # T 是被装饰函数的类型参数
    """创建同步包装函数"""

    @wraps(func)
    def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            if decorator_func.__code__.co_argcount > 0:
                return decorator_func(func, *args, **kwargs)
            decorated_func = decorator_func(**decorator_kwargs)
            return decorated_func(*args, **kwargs)
        except Exception as err:
            # 异常处理并返回None
            handle_exception(create_basemsg(func), err)
            return None

    return sync_wrapped


def decorate_sync_async[T](decorator_func: T = None, **decorator_kwargs) -> T:
    """
    增强版装饰器工厂 - 同时支持同步和异步函数，支持可选参数和无参数装饰器模式

    特性:
    - 支持同步和异步函数的装饰
    - 支持带参数和不带参数的装饰器模式
    - 保留原函数的元数据（名称、文档、签名等）
    - 内置异常处理机制，统一处理执行过程中的异常
    - 优化异步环境下同步函数的执行，避免阻塞事件循环

    Args:
        decorator_func: 装饰器函数，如果为None则返回一个接受装饰器函数的函数
        **decorator_kwargs: 传递给装饰器的额外参数

    Returns:
        装饰器函数

    Example:
        # 示例1: 无参数装饰器模式
        >>> @decorate_sync_async
        ... def log_execution(func, *args, **kwargs):
        ...     print(f'执行函数: {func.__name__}')
        ...     result = func(*args, **kwargs)
        ...     print(f'函数 {func.__name__} 执行完毕')
        ...     return result
        >>> @log_execution
        ... def sync_task():
        ...     return '同步任务完成'
        >>> @log_execution
        ... async def async_task():
        ...     await asyncio.sleep(0.1)
        ...     return '异步任务完成'

        # 示例2: 带参数装饰器模式
        >>> def with_custom_message(message):
        ...     def decorator(func, *args, **kwargs):
        ...         print(f'{message}: {func.__name__}')
        ...         return func(*args, **kwargs)
        ...
        ...     return decorator
        >>> # 使用带参数的装饰器
        >>> @decorate_sync_async(with_custom_message, message='开始执行')
        ... def my_function():
        ...     return '函数执行结果'
    """
    # 处理无参数装饰器模式 @decorate_sync_async
    if decorator_func is None:

        def decorator_wrapper(func: Callable) -> Callable:
            return decorate_sync_async(func, **decorator_kwargs)

        return decorator_wrapper

    @wraps(decorator_func)
    def decorator(func: T) -> T:
        # 根据函数类型创建对应的包装函数
        wrapped = create_async_wrapper(decorator_func, func, decorator_kwargs) if asyncio.iscoroutinefunction(func) else create_sync_wrapper(decorator_func, func, decorator_kwargs)
        return cast(T, wrapped)

    return decorator
