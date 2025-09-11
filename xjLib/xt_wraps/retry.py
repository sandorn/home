"""
==============================================================
Description  : 重试机制模块 - 提供函数执行失败自动重试功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 09:00:00
LastEditTime : 2025-09-06 11:30:00
FilePath     : /CODE/xjLib/xt_wraps/retry.py
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
from collections.abc import Callable
from functools import wraps
from typing import Any

from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random,
)

from .exception import handle_exception
from .log import create_basemsg


# 常量定义
DEFAULT_RETRY_ATTEMPTS = 3  # 默认最大尝试次数
DEFAULT_MIN_WAIT_TIME = 0.0  # 默认最小等待时间（秒）
DEFAULT_MAX_WAIT_TIME = 1.0  # 默认最大等待时间（秒）


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
        # HTTPError,  # HTTP错误（如404、500等）
        # TooManyRedirects,  # 重定向过多
        # # SSL/TLS相关异常
        # SSLError,  # SSL错误
        # SSLZeroReturnError,  # SSL连接被关闭
        # SSLWantReadError,  # SSL需要读取更多数据
        # SSLWantWriteError,  # SSL需要写入更多数据
        # SSLSyscallError,  # SSL系统调用错误
        # SSLEOFError,  # SSL EOF错误
        # # DNS相关异常
        # gaierror,  # 地址信息错误（DNS解析失败）
        # # 代理相关异常
        # ProxyError,  # 代理错误
        # # 请求库特定异常（如requests）
        # requests.exceptions.Timeout,
        # requests.exceptions.ConnectionError,
        # requests.exceptions.HTTPError,
        # requests.exceptions.ChunkedEncodingError,
        # requests.exceptions.ContentDecodingError,
        # # 异步HTTP客户端异常（如aiohttp）
        # aiohttp.ClientError,
        # aiohttp.ClientConnectionError,
        # aiohttp.ClientResponseError,
        # aiohttp.ClientPayloadError,
        # aiohttp.ServerTimeoutError,
        # aiohttp.ServerDisconnectedError,
        # # 其他可能的重试异常
        # BrokenPipeError,  # 管道破裂错误
        # TemporaryFailure,  # 临时故障（SMTP相关）
    )

    def __init__(self):
        self._basemsg = ''
        self._default_return = None

    def configure(self, basemsg: str, default_return: Any) -> None:
        """配置RetryHandler的基础消息和默认返回值

        Args:
            basemsg: 基础日志消息前缀
            default_return: 重试失败时的默认返回值
        """
        self._basemsg = basemsg
        self._default_return = default_return

    def err_back(self, retry_state: RetryCallState) -> Any:
        """所有重试失败后的回调函数 - 记录错误日志并返回默认值

        Args:
            retry_state: tenacity的重试状态对象

        Returns:
            配置的默认返回值
        """
        ex = retry_state.outcome.exception()
        handle_exception(ex, self._basemsg + f' | 共 {retry_state.attempt_number} 次失败')
        return self._default_return

    def before_back(self, retry_state: RetryCallState) -> None:
        """重试前的回调函数 - 记录即将进行的重试信息

        Args:
            retry_state: tenacity的重试状态对象
        """
        ex = retry_state.outcome.exception()
        handle_exception(ex, self._basemsg + f' | 第 {retry_state.attempt_number} 次失败')

    def should_retry(self, exception: Exception) -> bool:
        """判断给定异常是否应该触发重试

        Args:
            exception: 捕获的异常对象

        Returns:
            bool: 如果异常属于可重试类型，返回True；否则返回False
        """
        return any(isinstance(exception, exc_type) for exc_type in self.RETRY_EXCEPT)


def retry_wraps(
    fn: Callable[..., Any] = None,
    max_attempts: int = DEFAULT_RETRY_ATTEMPTS,
    min_wait: float = DEFAULT_MIN_WAIT_TIME,
    max_wait: float = DEFAULT_MAX_WAIT_TIME,
    retry_exceptions: tuple[type[Exception], ...] = RetryHandler.RETRY_EXCEPT,
    is_before_callback: bool = True,
    is_error_callback: bool = True,
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
        is_before_callback: 是否在重试前调用回调函数，默认为True
        is_error_callback: 是否在所有重试失败后调用回调函数，默认为True
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

    def decorator(func: Callable[..., Any]) -> Callable:
        #  创建RetryHandler实例,设置基础消息和默认返回
        retry_handler = RetryHandler()
        basemsg = create_basemsg(func)
        retry_handler.configure(basemsg, default_return)

        # 创建重试条件 - 只重试指定类型的异常
        # 注意：不再直接修改类变量RETRY_EXCEPT，而是使用局部参数retry_exceptions
        retry_condition = retry_if_exception_type(retry_exceptions)

        # 配置tenacity的retry装饰器
        retry_decorator = retry(
            reraise=True,  # 保持为True，让异常传播到我们的包装器
            stop=stop_after_attempt(max_attempts),
            wait=wait_random(min=min_wait, max=max_wait),
            retry=retry_condition,
            before_sleep=retry_handler.before_back if is_before_callback else None,
            retry_error_callback=retry_handler.err_back if is_error_callback else None,
        )

        # 同步函数包装器
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # 使用retry_decorator包装函数调用
                # #raise：可重试错误会重试足够次数，不重试错误只运行1次
                return retry_decorator(func)(*args, **kwargs)
            except Exception as e:
                # 不再使用RetryHandler.should_retry，而是直接检查当前装饰器配置的异常类型
                is_retry_exception = any(isinstance(e, exc_type) for exc_type in retry_exceptions)
                if is_retry_exception:  # 检查是否重试异常
                    return default_return  # 重试异常在所有重试失败后返回默认值
                elif silent_on_no_retry:  # 检查是否静默处理非重试异常
                    return default_return  # 非重试异常返回默认值
                else:
                    # raise  # 否则重新抛出异常
                    handle_exception(e, basemsg, re_raise=True)

        # 异步函数包装器
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                # 使用retry_decorator包装函数调用
                return await retry_decorator(func)(*args, **kwargs)
            except Exception as e:
                # 不再使用RetryHandler.should_retry，而是直接检查当前装饰器配置的异常类型
                is_retry_exception = any(isinstance(e, exc_type) for exc_type in retry_exceptions)
                if is_retry_exception:  # 检查是否重试异常
                    return default_return  # 重试异常在所有重试失败后返回默认值
                elif silent_on_no_retry:  # 检查是否静默处理非重试异常
                    return default_return  # 非重试异常返回默认值
                else:
                    # raise  # 否则重新抛出异常
                    handle_exception(e, basemsg, re_raise=True)

        # 根据函数类型返回相应的包装器
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator
