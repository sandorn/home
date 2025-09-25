# !/usr/bin/env python
"""
==============================================================
Description  : 计时工具模块 - 提供函数执行耗时自动记录功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:56:45
LastEditTime : 2025-09-11 14:30:00
FilePath     : /CODE/xjlib/xt_wraps/timer.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- timer_wraps：自动记录函数执行耗时的装饰器
- timer：timer_wraps的简写别名
- timeit：支持同步和异步函数的计时装饰器

主要特性：
- 同时支持同步和异步函数，自动识别函数类型
- 毫秒级精度的执行时间记录
- 集成异常处理机制
- 详细的日志输出
- 支持无参和有参调用方式
- 保留原始函数的元数据（名称、文档等）
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import Any

from xt_wraps.exception import handle_exception
from xt_wraps.log import create_basemsg, mylog


def timer_wraps(fn: Callable | None = None):
    """自动记录函数执行耗时的装饰器

    核心功能：
    - 自动记录函数的执行时间并输出调试日志
    - 同时支持同步和异步函数，自动识别函数类型
    - 集成异常处理机制，确保计时准确性
    - 保留原始函数的元数据（名称、文档字符串、参数签名等）

    参数说明：
    - fn: 可选，要装饰的函数，用于支持无参调用方式

    返回值：
    - 装饰后的函数，执行时会自动记录耗时

    示例用法：
        >>> # 方式1: 直接装饰同步函数
        >>> @timer_wraps
        >>> def calculate_sum(a, b):
        >>> # 执行一些计算
        >>>     return a + b
        >>> # 方式2: 带括号装饰异步函数
        >>> @timer_wraps()
        >>> async def fetch_data(url):
        >>> # 模拟网络请求延迟
        >>>     await asyncio.sleep(1)
        >>>     return f"Data from {url}"
        >>> # 方式3: 与其他装饰器组合使用
        >>> @log_wraps
        >>> @timer_wraps
        >>> def complex_operation(data):
        >>> # 执行复杂操作
        >>>     return processed_data
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            basemsg = create_basemsg(func)
            start_time = perf_counter()
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_exception(basemsg=basemsg, errinfo=err, re_raise=True)
            finally:
                mylog.info(f'{basemsg} | 执行耗时：{perf_counter() - start_time:.4f} 秒')

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            basemsg = create_basemsg(func)
            start_time = perf_counter()
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_exception(basemsg=basemsg, errinfo=err, re_raise=True)
            finally:
                mylog.info(f'{basemsg} | 执行耗时：{perf_counter() - start_time:.4f} 秒')

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator


timer = timer_wraps
