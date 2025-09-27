# !/usr/bin/env python3
"""
==============================================================
Description  : 增强型装饰器工具模块 - 提供同步/异步函数通用装饰器工厂
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-27 01:00:00
LastEditTime : 2025-09-27 01:00:00
FilePath     : /CODE/xjlib/xt_wraps/decos.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import asyncio
import random
import traceback
from collections.abc import Callable
from functools import wraps
from time import perf_counter, sleep
from typing import Any, TypeVar

from xt_wraps.log import mylog

# 类型别名
ExceptionTypes = tuple[type[Exception], ...]
T = TypeVar('T')


async def maybe_await(fn: Callable | None, *args: Any, **kwargs: Any) -> Any:
    """
    根据函数类型执行同步或异步调用
    
    Args:
        fn: 要执行的函数
        *args: 位置参数
        **kwargs: 关键字参数
        
    Returns:
        函数执行结果
    """
    if fn is None:
        return None
    if asyncio.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return fn(*args, **kwargs)


def decorator_factory(
    before: Callable | None = None,
    after: Callable | None = None,
    exception: Callable | None = None,
) -> Callable:
    """
    通用装饰器工厂，支持同步/异步函数，支持前置、后置、异常钩子
    
    Args:
        before: 前置钩子函数，签名为(func, args, kwargs, context)
        after: 后置钩子函数，签名为(func, args, kwargs, result, context)
        exception: 异常钩子函数，签名为(func, args, kwargs, exc, context)
        
    Returns:
        装饰器函数
    """
    def _build_wrapper(func: Callable, is_async: bool) -> Callable:
        """构建适合函数类型的包装器"""
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """异步函数包装器"""
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
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """同步函数包装器"""
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
        """实际的装饰器"""
        return _build_wrapper(func, asyncio.iscoroutinefunction(func))

    return decorator


def handle_exception(
    errinfo: Exception,
    re_raise: bool = False,
    default_return: Any = None,
    callfrom: Callable | None = None,
    log_traceback: bool = True,
    custom_message: str | None = None,
) -> Any:
    """
    统一的异常处理函数，提供完整的异常捕获、记录和处理机制

    Args:
        errinfo: 异常对象
        re_raise: 是否重新抛出异常，默认False（不抛出，返回默认值）
        default_return: 不抛出异常时的默认返回值，default_return为None时返回错误信息字符串
        callfrom: 调用来源函数，用于日志记录
        log_traceback: 是否记录完整堆栈信息，默认True
        custom_message: 自定义错误提示信息，默认None

    Returns:
        Any: 如果re_raise=True，重新抛出异常；否则返回default_return或错误信息字符串
    """
    # 构建错误信息
    error_type = type(errinfo).__name__
    error_msg = str(errinfo)

    # 统一的日志格式
    error_message = f'{error_type} | {error_msg}'
    if custom_message:
        error_message = f'{custom_message} | {error_message}'

    # 记录警告日志
    mylog.error(error_message, callfrom=callfrom)

    # 如果需要，记录完整堆栈信息
    if log_traceback:
        mylog.error(f'堆栈信息: {traceback.format_exc()}', callfrom=callfrom)

    # 根据需要重新抛出异常
    if re_raise:
        raise errinfo
    return error_message if default_return is None else default_return


# ==================== 基础装饰器 ====================

# 计时装饰器
def before_timer(func: Callable, args: tuple, kwargs: dict, context: dict) -> None:
    """计时装饰器前置钩子"""
    context['start'] = perf_counter()


def after_timer(func: Callable, args: tuple, kwargs: dict, result: Any, context: dict) -> None:
    """计时装饰器后置钩子"""
    start = context.get('start')
    end = perf_counter()
    mylog.info(f'{func.__name__} 执行耗时: {end - start:.4f}秒')


timer = decorator_factory(before=before_timer, after=after_timer)


# 日志装饰器
def before_log(func: Callable, args: tuple, kwargs: dict, context: dict) -> None:
    """日志装饰器前置钩子"""
    mylog.debug('调用函数 {}，参数: {}, 关键字参数: {}', func.__name__, args, kwargs, callfrom=func)


def after_log(func: Callable, args: tuple, kwargs: dict, result: Any, context: dict) -> None:
    """日志装饰器后置钩子"""
    mylog.success('函数 {} 执行成功，返回值: {}', func.__name__, result, callfrom=func)


def exception_log(func: Callable, args: tuple, kwargs: dict, exc: Exception, context: dict) -> None:
    """日志装饰器异常钩子"""
    mylog.error('函数 {} 执行时发生异常: {}', func.__name__, str(exc), callfrom=func)


log = decorator_factory(
    before=before_log,
    after=after_log,
    exception=exception_log,
)


# 重试装饰器
def retry(  # noqa
    max_attempts: int = 3,
    min_wait: float = 0.1,
    max_wait: float = 1.0,
    retry_exceptions: ExceptionTypes = (Exception,),
) -> Callable:
    """
    重试装饰器工厂函数
    
    Args:
        max_attempts: 最大尝试次数，默认为3次
        min_wait: 重试间隔的最小等待时间(秒)，默认为0.1秒
        max_wait: 重试间隔的最大等待时间(秒)，默认为1.0秒
        retry_exceptions: 需要重试的异常类型元组，默认为所有异常
        
    Returns:
        装饰器函数
    """
    def before_retry(func: Callable, args: tuple, kwargs: dict, context: dict) -> None:
        """重试装饰器前置钩子"""
        context['retries'] = 0
        context['max_attempts'] = max_attempts
        context['min_wait'] = min_wait
        context['max_wait'] = max_wait
        context['retry_exceptions'] = retry_exceptions

    def exception_retry(func: Callable, args: tuple, kwargs: dict, exc: Exception, context: dict) -> None:
        """重试装饰器异常钩子"""
        # 检查异常类型是否在重试列表中
        if not isinstance(exc, context['retry_exceptions']):
            context['retry'] = False
            return
            
        context['retries'] += 1
        if context['retries'] < context['max_attempts']:
            wait_time = random.uniform(context['min_wait'], context['max_wait'])
            mylog.warning(f'函数 {func.__name__} 第 {context["retries"]} 次尝试失败: {exc}，等待 {wait_time:.2f} 秒后重试')
            if asyncio.iscoroutinefunction(func):
                # 异步等待需要特殊处理，这里只记录，实际等待在包装器中进行
                context['wait_time'] = wait_time
            else:
                sleep(wait_time)
            context['retry'] = True
        else:
            mylog.error(f'函数 {func.__name__} 在 {max_attempts} 次尝试后仍然失败: {exc}')
            context['retry'] = False

    def decorator(func: Callable) -> Callable:  # noqa
        """实际的装饰器"""
        is_async = asyncio.iscoroutinefunction(func)
        base_decorator = decorator_factory(
            before=before_retry,
            exception=exception_retry,
        )
        
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """异步函数重试包装器"""
            context = {'retry': False, 'retries': 0}
            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        mylog.debug(f'函数 {func.__name__} 第 {attempt + 1} 次尝试')
                    # 使用基础装饰器处理单次调用
                    return await base_decorator(func)(*args, **kwargs)
                except retry_exceptions:
                    if not context.get('retry'):
                        raise
                    # 异步等待
                    await asyncio.sleep(context.get('wait_time', min_wait))
                except Exception:
                    # 非重试异常直接抛出
                    raise
            return None  # 不应该到达这里

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """同步函数重试包装器"""
            context = {'retry': False, 'retries': 0}
            for attempt in range(max_attempts):
                try:
                    if attempt > 0:
                        mylog.debug(f'函数 {func.__name__} 第 {attempt + 1} 次尝试')
                    # 使用基础装饰器处理单次调用
                    return base_decorator(func)(*args, **kwargs)
                except retry_exceptions:
                    if not context.get('retry'):
                        raise
                except Exception:
                    # 非重试异常直接抛出
                    raise
            return None  # 不应该到达这里

        return async_wrapper if is_async else sync_wrapper

    return decorator