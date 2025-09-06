# !/usr/bin/env python
"""
==============================================================
Description  : 函数执行计时器工具模块 - 提供同步和异步函数执行时间监控
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:56:45
LastEditTime : 2025-09-06 12:30:00
FilePath     : /CODE/xjLib/xt_wraps/timer.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- timer_wraps：自动记录函数执行耗时的装饰器
- timer：timer_wraps的简写别名

主要特性：
- 同时支持同步和异步函数，自动识别函数类型
- 毫秒级精度的执行时间记录
- 集成异常处理机制
- 详细的日志输出
- 支持无参和有参调用方式
- 保留原始函数的元数据（名称、文档等）
==============================================================
"""

import asyncio
from functools import wraps
from time import perf_counter
from typing import Any, Callable

from .exception import handle_exception
from .log import create_basemsg, mylog


def timer_wraps(fn: Callable = None):
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
    # 支持两种装饰器调用方式
    # 方式1: @timer_wraps
    # 方式2: @timer_wraps()
    # 可用于同步函数和异步函数
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            try:
                return func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err, _basemsg, re_raise=True)
            finally:
                mylog.debug(
                    f"{_basemsg} | Timer-Consuming <{perf_counter() - start_time:.4f} s>"
                )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_exception(err, _basemsg, re_raise=True)
            finally:
                mylog.debug(
                    f"{_basemsg} | Timer-Consuming <{perf_counter() - start_time:.4f} s>"
                )

        _basemsg = create_basemsg(func)
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator

timer = timer_wraps
