# !/usr/bin/env python3
"""
==============================================================
Description  : 重试机制模块 - 提供函数执行失败自动重试功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 09:00:00
LastEditTime : 2025-09-06 11:30:00
FilePath     : /CODE/xjlib/xt_wraps/retry.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- retry_wraps：函数重试装饰器，同时支持同步和异步函数
- RetryHandler：重试处理器，管理重试逻辑和异常处理
- 自动识别同步/异步函数，提供一致的重试体验
- 支持自定义重试次数、等待时间和异常类型

主要特性：
- 基于tenacity库实现的高效重试机制
- 自动适配同步和异步函数
- 可配置的重试策略和等待时间范围
- 自定义的异常类型筛选和处理
- 丰富的回调函数支持
- 异常静默处理和默认返回值机制
- 统一的异常日志记录
==============================================================
"""

from __future__ import annotations

import asyncio
import smtplib
import socket
import ssl
from collections.abc import Callable
from functools import wraps
from typing import Any

import aiohttp
import requests
import urllib3.exceptions
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random,
)
from xt_wraps.exception import handle_exception

# 导入需要使用的异常类型
gaierror = socket.gaierror  # DNS解析错误

# SSL相关异常
SSLError = ssl.SSLError
SSLZeroReturnError = ssl.SSLZeroReturnError
SSLWantReadError = ssl.SSLWantReadError
SSLWantWriteError = ssl.SSLWantWriteError
SSLSyscallError = ssl.SSLSyscallError
SSLEOFError = ssl.SSLEOFError

# HTTP相关异常
HTTPError = requests.exceptions.HTTPError
TooManyRedirects = requests.exceptions.TooManyRedirects
ProxyError = urllib3.exceptions.ProxyError

# 其他异常
TemporaryFailure = smtplib.SMTPServerDisconnected

# 常量定义
DEFAULT_RETRY_ATTEMPTS = 3  # 默认最大尝试次数
DEFAULT_MIN_WAIT_TIME = 0.0  # 默认最小等待时间（秒）
DEFAULT_MAX_WAIT_TIME = 1.0  # 默认最大等待时间（秒）
TIMEOUT = 30
RETRY_TIME = 3

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(),
)


class RetryHandler:
    """重试处理器 - 管理重试逻辑、异常处理和回调函数

    核心功能：
    - 维护可重试异常类型列表
    - 提供重试前和错误回调函数
    - 判断异常是否应该重试
    - 处理全局配置和状态管理
    """

    # 默认可重试异常类型
    RETRY_EXCEPT = (
        # 网络连接异常
        TimeoutError,  # 超时错误
        ConnectionError,  # 连接错误
        ConnectionRefusedError,  # 连接被拒绝
        ConnectionResetError,  # 连接被重置
        ConnectionAbortedError,  # 连接被中止
        # 操作系统级I/O异常
        OSError,  # 操作系统错误（包括许多网络错误）
        # HTTP相关异常（默认注释，可根据需要取消注释）
        HTTPError,  # HTTP错误（如404、500等）
        TooManyRedirects,  # 重定向过多
        # # SSL/TLS相关异常
        SSLError,  # SSL错误
        SSLZeroReturnError,  # SSL连接被关闭
        SSLWantReadError,  # SSL需要读取更多数据
        SSLWantWriteError,  # SSL需要写入更多数据
        SSLSyscallError,  # SSL系统调用错误
        SSLEOFError,  # SSL EOF错误
        # # DNS相关异常
        gaierror,  # 地址信息错误（DNS解析失败）
        # # 代理相关异常
        ProxyError,  # 代理错误
        # # 请求库特定异常（如requests）
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.ChunkedEncodingError,
        requests.exceptions.ContentDecodingError,
        # # 异步HTTP客户端异常（如aiohttp）
        aiohttp.ClientError,
        aiohttp.ClientConnectionError,
        aiohttp.ClientResponseError,
        aiohttp.ClientPayloadError,
        aiohttp.ServerTimeoutError,
        aiohttp.ServerDisconnectedError,
        # # 其他可能的重试异常
        BrokenPipeError,  # 管道破裂错误
        TemporaryFailure,  # 临时故障（SMTP相关）
    )

    def __init__(self) -> None:
        self._default_return: Any = None
        self._callfrom: Callable | None = None

    def configure(self, default_return: Any | None = None, callfrom: Callable | None = None) -> None:
        """配置RetryHandler的基础消息和默认返回值"""
        self._default_return = default_return
        self._callfrom = callfrom

    def err_back(self, retry_state: RetryCallState) -> Any:
        """最后一次重试失败时执行的回调函数 - 记录错误日志并返回默认值

        Args:
            retry_state: tenacity的重试状态对象

        Returns:
            配置的默认返回值
        """
        # 获取原始错误对象（若有异常）
        original_exception = retry_state.outcome.exception()
        return handle_exception(errinfo=original_exception, default_return=self._default_return, callfrom=self._callfrom)


def _create_retry_decorator(max_attempts: int, min_wait: float, max_wait: float, retry_exceptions: tuple[type[Exception], ...], retry_handler: RetryHandler, is_err_back: bool) -> Callable:
    """创建tenacity重试装饰器

    Args:
        max_attempts: 最大尝试次数
        min_wait: 最小等待时间
        max_wait: 最大等待时间
        retry_exceptions: 需要重试的异常类型元组
        retry_handler: 重试处理器实例
        is_err_back: 是否使用错误回调

    Returns:
        配置好的tenacity重试装饰器
    """
    retry_condition = retry_if_exception_type(retry_exceptions)

    return retry(
        reraise=True,
        stop=stop_after_attempt(max_attempts),
        wait=wait_random(min=min_wait, max=max_wait),
        retry=retry_condition,
        retry_error_callback=retry_handler.err_back if is_err_back else None,
    )


def _handle_exception(errinfo: Exception, retry_exceptions: tuple[type[Exception], ...], default_return: Any, silent_on_no_retry: bool, func: Callable) -> Any:
    """统一异常处理函数 - 处理同步和异步函数的异常

    Args:
        errinfo: 异常对象
        retry_exceptions: 需要重试的异常类型元组
        default_return: 默认返回值
        silent_on_no_retry: 是否静默处理非重试异常
        func: 原始函数

    Returns:
        处理结果
    """
    error_message = f'Retry Error: {type(errinfo).__name__} | {errinfo!s}'
    is_retry_exception = any(isinstance(errinfo, exc_type) for exc_type in retry_exceptions)

    if is_retry_exception or silent_on_no_retry:
        return error_message if default_return is None else default_return

    return handle_exception(errinfo=errinfo, re_raise=True, callfrom=func)


def retry_wraps(
    fn: Callable | None = None,
    max_attempts: int = DEFAULT_RETRY_ATTEMPTS,
    min_wait: float = DEFAULT_MIN_WAIT_TIME,
    max_wait: float = DEFAULT_MAX_WAIT_TIME,
    retry_exceptions: tuple[type[Exception], ...] = RetryHandler.RETRY_EXCEPT,
    is_err_back: bool = True,
    silent_on_no_retry: bool = True,
    default_return: Any = None,
) -> Callable:
    """重试装饰器 - 基于tenacity库，提供函数执行失败自动重试功能，支持同步和异步函数

    核心功能：
    - 自动识别并适配同步/异步函数
    - 可配置最大重试次数和等待时间范围
    - 可自定义重试的异常类型
    - 支持重试前后的回调函数
    - 提供异常静默处理和默认返回值机制
    - 统一的异常日志记录

    Args:
        fn: 要装饰的函数，可选（支持同步和异步函数）
        max_attempts: 最大尝试次数，默认为3次
        min_wait: 重试间隔的最小等待时间(秒)，默认为0.0秒
        max_wait: 重试间隔的最大等待时间(秒)，默认为1.0秒
        retry_exceptions: 需要重试的异常类型元组，默认为网络和I/O相关异常
        is_err_back: 是否在所有重试失败后调用回调函数，默认为True
        silent_on_no_retry: 遇到非重试异常时是否静默处理（不抛出错误），默认为True
        default_return: 重试失败或静默处理时的默认返回值，默认为None

    Returns:
        装饰后的函数，保持原函数签名和类型

    示例:
        # 基础用法 - 默认配置（3次重试，随机等待0-1秒）
        @retry_wraps
        def network_request(url):
            # 网络请求代码
            return response

        # 自定义重试次数和等待时间
        @retry_wraps(max_attempts=5, min_wait=0.5, max_wait=2.0)
        def unstable_operation():
            # 不稳定操作
            return result

        # 自定义重试异常类型
        @retry_wraps(retry_exceptions=(ConnectionError, TimeoutError))
        def specific_error_handling():
            # 只对特定异常重试
            return result

        # 异步函数使用
        @retry_wraps
        async def async_network_request(url):
            # 异步网络请求
            return response

        # 设置默认返回值
        @retry_wraps(default_return="默认值", silent_on_no_retry=True)
        def function_with_default():
            # 可能失败的函数
            return result
    """

    def decorator(func: Callable) -> Callable:
        # 创建RetryHandler实例,设置基础消息和默认返回
        retry_handler = RetryHandler()
        retry_handler.configure(default_return, func)

        # 创建tenacity的retry装饰器
        retry_decorator = _create_retry_decorator(max_attempts, min_wait, max_wait, retry_exceptions, retry_handler, is_err_back)

        # 同步函数包装器
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # 使用retry_decorator包装函数调用
                return retry_decorator(func)(*args, **kwargs)
            except Exception as errinfo:
                return _handle_exception(errinfo, retry_exceptions, default_return, silent_on_no_retry, func)

        # 异步函数包装器
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # 使用retry_decorator包装函数调用
                return await retry_decorator(func)(*args, **kwargs)
            except Exception as errinfo:
                return _handle_exception(errinfo, retry_exceptions, default_return, silent_on_no_retry, func)

        # 根据函数类型返回相应的包装器
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    if fn is None:
        return decorator
    return decorator(fn)
