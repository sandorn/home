# !/usr/bin/env python3
"""
==============================================================
Description  : 日志工具模块 - 增强版，利用loguru内置功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-26 16:00:00
FilePath     : /CODE/xjlib/xt_wraps/log.py
Github       : https://github.com/sandorn/home

优化特性:
- 利用loguru的record对象直接获取调用信息，无需手动处理调用栈
- 大幅简化代码结构，提高可维护性
- 保持原有的所有功能和图标显示
- 支持callfrom参数扩展功能，可自定义调用位置显示
- 增强异常处理参数，与exc_wraps保持一致
- 添加日志上下文管理器，方便跟踪函数执行流程
- 支持动态调整日志级别，适应不同场景需求
- 优化日志格式和配置，提高可读性
==============================================================
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any


def log_wraps(
    func: Callable | None = None,
    log_args: bool = True,
    log_result: bool = True,
    re_raise: bool = False,
    default_return: Any = None
) -> Callable:
    """
    简化版日志装饰器 - 利用callfrom参数传递调用者信息
    
    这个装饰器可以为函数自动添加日志记录功能，包括：
    - 记录函数调用时的参数
    - 记录函数的返回值
    - 自动处理同步和异步函数
    - 支持异常处理和重新抛出
    
    Args:
        func: 被装饰的函数（装饰器语法糖参数）
        log_args: 是否记录函数参数，默认为True
        log_result: 是否记录函数返回值，默认为True
        re_raise: 是否重新抛出异常，默认为False
        default_return: 异常时的默认返回值，默认为None
        
    Returns:
        Callable: 装饰后的函数
        
    Example:
        >>> @log_wraps
        >>> def my_function(x, y):
        >>>     return x + y
        
        >>> @log_wraps(log_args=True, log_result=False)
        >>> async def async_function(data):
        >>>     return await process_data(data)
    """
    from xt_log import mylog
    from xt_wraps.exception import handle_exception

    def decorator(func: Callable) -> Callable:
        """实际的装饰器实现"""
        
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """同步函数包装器"""
            
            if log_args:
                mylog.debug(' Args: {} | Kwargs: {}', args, kwargs, callfrom=func)
            
            try:
                result: Any = func(*args, **kwargs)
                if log_result:
                    mylog.success(' Result: {} = {}', type(result).__name__, result, callfrom=func)
                return result
            except Exception as err:
                return handle_exception(
                    err, 
                    re_raise=re_raise, 
                    default_return=default_return, 
                    callfrom=func
                )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """异步函数包装器"""
            
            if log_args:
                mylog.debug(' Args: {} | Kwargs: {}', args, kwargs, callfrom=func)
            
            try:
                result: Any = await func(*args, **kwargs)
                if log_result:
                    mylog.success(' Result: {} = {}', type(result).__name__, result, callfrom=func)
                return result
            except Exception as err:
                return handle_exception(
                    err, 
                    re_raise=re_raise, 
                    default_return=default_return, 
                    callfrom=func
                )

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(func) if func else decorator

