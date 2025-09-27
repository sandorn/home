# !/usr/bin/env python3
"""
==============================================================
Description  : 核心装饰器工具模块 - 提供同步/异步函数通用装饰器工厂
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 11:06:38
LastEditTime : 2025-09-06 10:00:00
FilePath     : /CODE/xjlib/xt_wraps/deco.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import lru_cache, wraps
from time import perf_counter, sleep

from xt_wraps.log import mylog


async def maybe_await(fn, *args, **kwargs):
    if fn is None:
        return None
    if asyncio.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return fn(*args, **kwargs)


def universal_decorator(
    before: Callable | None = None,
    after: Callable | None = None,
    exception: Callable | None = None,
) -> Callable:
    """
    通用装饰器工厂，支持同步/异步函数，支持前置、后置、异常钩子。
    支持 context 参数用于 before/after/exception 之间数据传递。
    """

    def _build_wrapper(func: Callable, is_async: bool):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            context = {}
            await maybe_await(before, func, args, kwargs, context)
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                await maybe_await(exception, func, args, kwargs, e, context)
                raise
            await maybe_await(after, func, args, kwargs, result, context)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            context = {}
            if before:
                before(func, args, kwargs, context)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if exception:
                    exception(func, args, kwargs, e, context)
                raise
            if after:
                after(func, args, kwargs, result, context)
            return result

        return async_wrapper if is_async else sync_wrapper

    def decorator(func: Callable) -> Callable:
        return _build_wrapper(func, asyncio.iscoroutinefunction(func))

    return decorator


# 计时装饰器
def before_timer(func, args, kwargs, context):
    context['start'] = perf_counter()


def after_timer(func, args, kwargs, result, context):
    start = context.get('start')
    end = perf_counter()
    mylog.info(f'{func.__name__} 执行耗时: {end - start:.4f}秒')


timer_wrapper = universal_decorator(before=before_timer, after=after_timer)


def before_log(func, args, kwargs, context):
    mylog.info(' args={}, kwargs={}', args, kwargs, callfrom=func)


def after_log(func, args, kwargs, result, context):
    mylog.info(f'result: {result}', callfrom=func)


def exception_log(func, args, kwargs, exc, context):
    mylog.error(f'exception: {exc!r}', callfrom=func)


log_wrapper = universal_decorator(
    before=before_log,
    after=after_log,
    exception=exception_log,
)


def before_retry(func, args, kwargs, context):
    context['retries'] = 0


def exception_retry(func, args, kwargs, exc, context):
    max_retries = context.get('max_retries', 3)
    delay = context.get('delay', 0.1)
    context['retries'] += 1
    if context['retries'] <= max_retries:
        mylog.warning(f" 第{context['retries']}次重试，异常: {exc!r}", callfrom=func)
        if delay:
            sleep(delay)
        context['retry'] = True
    else:
        context['retry'] = False


def retry_wrapper(max_retries=3, delay=0.1):
    """
    通用重试装饰器，支持同步/异步函数。
    :param max_retries: 最大重试次数
    :param delay: 每次重试间隔（秒）
    """
    def decorator(func):
        is_async = asyncio.iscoroutinefunction(func)

        def before(func, args, kwargs, context):
            context['max_retries'] = max_retries
            context['delay'] = delay
            context['retries'] = 0

        def exception(func, args, kwargs, exc, context):
            context['retries'] += 1
            if context['retries'] <= context['max_retries']:
                mylog.warning(f" 第{context['retries']}次重试，异常: {exc!r}", callfrom=func)
                if context['delay']:
                    sleep(context['delay'])
                context['retry'] = True
            else:
                context['retry'] = False

        base_decorator = universal_decorator(
            before=before,
            exception=exception,
        )

        if is_async:
            @wraps(func)
            async def async_retry_wrapper(*args, **kwargs):
                context = {}
                for _ in range(max_retries + 1):
                    try:
                        # 只传递 args/kwargs，context 只在装饰器内部流转
                        return await base_decorator(func)(*args, **kwargs)
                    except Exception:
                        if not context.get('retry'):
                            raise
                return None
            return async_retry_wrapper

        @wraps(func)
        def sync_retry_wrapper(*args, **kwargs):
            context = {}
            for _ in range(max_retries + 1):
                try:
                    return base_decorator(func)(*args, **kwargs)
                except Exception:
                    if not context.get('retry'):
                        raise
            return None
        return sync_retry_wrapper

    return decorator


def cache_wrapper(maxsize=128):
    """
    通用缓存装饰器，支持同步函数。
    :param maxsize: 缓存最大数量
    """
    def decorator(func):
        cached_func = lru_cache(maxsize=maxsize)(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return cached_func(*args, **kwargs)
        return wrapper
    return decorator


def type_check_wrapper(*types):
    """
    简单参数类型检查装饰器，仅支持同步函数。
    :param types: 期望的参数类型
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i, (a, t) in enumerate(zip(args, types, strict=False)):
                if not isinstance(a, t):
                    raise TypeError(f'参数 {i} 应为 {t.__name__}, 实际为 {type(a).__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 示例
@type_check_wrapper(int, int)
def add(x, y):
    return x + y


# 示例
@cache_wrapper(maxsize=32)
def fib(n):
    """斐波那契数列（带缓存）"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# retry_wrapper 装饰器示例
@retry_wrapper(max_retries=2, delay=0.2)
def retry_sync_demo(x):
    """同步重试示例"""
    if x < 0:
        raise ValueError('x must be >= 0')
    return x * 2


@retry_wrapper(max_retries=2, delay=0.2)
async def retry_async_demo(x):
    """异步重试示例"""
    if x < 0:
        raise ValueError('x must be >= 0')
    await asyncio.sleep(0.05)
    return x * 3


# 使用装饰器
@timer_wrapper
def sync_function(x: int, y: int) -> int:
    """同步函数"""
    sleep(0.1)
    return x + y


@timer_wrapper
async def async_function(x: int, y: int) -> int:
    """异步函数"""
    await asyncio.sleep(0.1)
    return x * y


@log_wrapper
def log_sync_demo(a, b):
    """同步日志示例"""
    return a - b


@log_wrapper
async def log_async_demo(a, b):
    """异步日志示例"""
    await asyncio.sleep(0.05)
    return a / b


async def main():
    """主测试函数"""
    
    print('=== 测试同步函数 ===')
    result1 = sync_function(3, 4)
    print(f'同步函数结果: {result1}')
    
    print('\n=== 测试异步函数 ===')
    result2 = await async_function(5, 6)
    print(f'异步函数结果: {result2}')

    print('\n=== 测试log_wrapper同步函数 ===')
    log_result1 = log_sync_demo(10, 3)
    print(f'log_wrapper同步结果: {log_result1}')

    print('\n=== 测试log_wrapper异步函数 ===')
    log_result2 = await log_async_demo(20, 5)
    print(f'log_wrapper异步结果: {log_result2}')

    print('\n=== 测试retry_wrapper同步函数 ===')
    try:
        print('retry_sync_demo(-1):')
        retry_sync_demo(-1)
    except Exception as e:
        print(f'retry_sync_demo异常: {e}')
    print(f'retry_sync_demo(5): {retry_sync_demo(5)}')

    print('\n=== 测试retry_wrapper异步函数 ===')
    try:
        print('retry_async_demo(-2):')
        await retry_async_demo(-2)
    except Exception as e:
        print(f'retry_async_demo异常: {e}')

    print(f'retry_async_demo(7): {await retry_async_demo(7)}')
    print('fib(100):', fib(100))
    print('add(3, 5):', add(3, 5))
    print('add("3", 5):', add('3', 5))  # 触发类型检查异常


if __name__ == '__main__':
    asyncio.run(main())