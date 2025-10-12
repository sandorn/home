#!/usr/bin/env python3
"""
异常处理模块 - 提供统一的异常处理机制

该模块提供一致的异常处理策略，用于处理线程和进程中的异常，
确保错误被适当记录并可选择重新抛出。
"""

from __future__ import annotations

import functools
import traceback
from collections.abc import Callable
from typing import Any, overload

from xtlog import mylog

# 类型别名
ExceptionTypes = tuple[type[Exception], ...]


def handle_exception(
    exc: BaseException | None = None,
    re_raise: bool = False,
    handler: Callable[..., Any] | None = None,
    default_return: Any | None = None,
    log_traceback: bool = True,
    custom_message: str | None = None,
) -> Any | None:
    """
    统一的异常处理函数，提供完整的异常捕获、记录和处理机制

    Args:
        exc: 异常对象
        re_raise: 是否重新抛出异常，默认False（不抛出异常）
        handler: 异常处理函数，默认None（不处理）
        default_return: 默认返回值
        log_traceback: 是否记录完整堆栈信息，默认True
        custom_message: 自定义错误提示信息，默认None

    Returns:
        Any: 如果re_raise=True，重新抛出异常；否则返回default_return

    Example:
        >>> # 基本使用
        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     # 记录异常但不中断程序
        ...     result = handle_exception(e, re_raise=False, default_return=0)
        >>> print(result)  # 输出: 0
    """

    # 构建错误信息
    error_type = type(exc).__name__
    error_msg = str(exc)

    # 统一的日志格式
    error_message = f'{custom_message} | except: {error_type}({error_msg})' if custom_message else f'except: {error_type}({error_msg})'
    mylog.error(error_message)

    # 调用异常处理函数
    if handler:
        handler(exc)

    # 如果需要,记录完整堆栈信息
    if log_traceback and exc is not None:  # 确保有异常对象
        # 显式传入异常的类型、值和追踪信息
        tb_str = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        mylog.error(f'traceback | {tb_str}')
    elif log_traceback:
        mylog.error('traceback | No exception traceback available (exc is None)')

    # 根据需要重新抛出异常
    if re_raise and exc is not None:
        raise exc

    return default_return if default_return is not None else f'except: {error_type}({error_msg})'


@overload
def safe_call(fn: Callable[..., Any]) -> Callable[..., Any]:
    pass


@overload
def safe_call(
    fn: None = None,
    re_raise: bool = False,
    handler: Callable[..., Any] | None = None,
    default_return: Any = None,
    log_traceback: bool = True,
    custom_message: str | None = None,
    exceptions: ExceptionTypes = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    pass


def safe_call(
    fn: Callable[..., Any] | None = None,
    re_raise: bool = False,
    handler: Callable[..., Any] | None = None,
    default_return: Any | None = None,
    log_traceback: bool = True,
    custom_message: str | None = None,
    exceptions: ExceptionTypes = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    异常处理装饰器，用于包装函数以统一捕获和处理异常

    Args:
        re_raise: 是否重新抛出异常，默认False（不抛出异常）
        handler: 异常处理函数，默认None（不处理）
        default_return: 不抛出异常时的默认返回值
        log_traceback: 是否记录完整堆栈信息，默认True
        custom_message: 自定义错误提示信息，默认None
        exceptions: 要捕获的异常类型元组，默认捕获所有Exception类型

    Returns:
        Callable: 装饰后的函数

    Example:
        >>> @safe_call(default_return=0)
        ... def divide(a, b):
        ...     return a / b
        >>> divide(10, 2)  # 正常调用
        5
        >>> divide(10, 0)  # 异常调用，返回默认值
        0
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                func_name = func.__name__
                # 添加函数名到自定义消息中
                message = f'{func_name} | {custom_message}' if custom_message else f'{func_name}'
                return handle_exception(
                    exc=e,
                    re_raise=re_raise,
                    handler=handler,
                    default_return=default_return,
                    log_traceback=log_traceback,
                    custom_message=message,
                )

        return wrapper

    return decorator if fn is None else decorator(fn)


__all__ = ['handle_exception', 'safe_call']
