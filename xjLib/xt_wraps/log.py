# !/usr/bin/env python
"""
+==============================================================
Description  : 日志工具模块
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 14:39:12
FilePath     : /CODE/xjLib/xt_log.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import os
import sys
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from loguru import logger

from .exception import handle_exception
from .singleton import SingletonMixin

IS_DEV = os.getenv("ENV", "dev").lower() == "dev"


standard_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
)


def create_basemsg(func: Callable) -> str:
    """生成日志基础信息，包括模块名、行号和函数名。

    Args:
        func: 要记录的函数对象

    Returns:
        str: 格式化的日志基础信息，格式为"模块名.文件名#行号@函数名"
    """
    # 获取原始函数（通过__wrapped__属性），处理可能的多层装饰器
    original_func = func
    while hasattr(original_func, "__wrapped__"):
        original_func = original_func.__wrapped__

    try:
        # 获取代码对象和相关信息
        code = getattr(original_func, "__code__")
        filename = code.co_filename
        line_number = code.co_firstlineno
        func_name = original_func.__name__

        # 将完整文件路径转换为通用的库.文件名格式
        try:
            # 规范化路径并分割
            file_parts = os.path.normpath(filename).split(os.sep)
            if len(file_parts) >= 2:
                # 获取父目录名和完整文件名（包括扩展名）
                parent_dir = file_parts[-2]
                full_filename = file_parts[-1]
                module_name = f"{parent_dir}.{full_filename}"
            else:
                # 如果路径部分不足，直接使用完整文件名
                module_name = file_parts[-1]
        except Exception:
            # 如果处理失败，回退到使用文件名（不带扩展名）
            module_name = os.path.splitext(os.path.basename(filename))[0]

        return f"{module_name}#{line_number}@{func_name}"
    except Exception:
        # 终极异常处理，确保函数不会失败
        return f"unknown#0@{getattr(original_func, '__name__', 'unknown')}"


class LogCls(SingletonMixin):
    def __init__(self, level=10, logger=logger):
        self.log = logger
        # 移除默认配置
        self.log.remove()

        # 文件日志（始终记录）
        log_file = f"XtLog-{datetime.now().strftime('%Y%m%d')}.log"
        self.log.add(
            log_file,
            rotation="512 MB",
            retention="180 days",
            level=level,
            encoding="utf-8",
            format=standard_format,
        )

        # 控制台日志（仅开发环境）
        if IS_DEV:
            self.log.add(sys.stderr, level=level, format=standard_format)


mylog = LogCls().log


def log_wraps(
    func: Callable = None,
    log_level: int = 10,
    log_args: bool = True,
    log_result: bool = True,
):
    """
    日志记录装饰器,做了except处理 - 同时支持同步和异步函数

    Args:
        func: 被装饰的函数，可选
        log_level: 日志级别，默认10(DEBUG)
        log_args: 是否记录函数参数，默认True
        log_result: 是否记录函数返回结果，默认True
    Returns:
        装饰后的函数
    """
    # 创建日志实例
    mylog = LogCls(log_level).log

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            if log_args:
                mylog.debug(f"{_basemsg} | Args: {args} | Kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                if log_result:
                    mylog.success(f"{_basemsg} | result: < {result} >")
                else:
                    mylog.success(f"{_basemsg} | successfully")
                return result
            except Exception as err:
                return handle_exception(err, _basemsg)

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            if log_args:
                mylog.debug(f"{_basemsg} | Args: {args} | Kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                if log_result:
                    mylog.success(f"{_basemsg} | result: < {result} >")
                else:
                    mylog.success(f"{_basemsg} | successfully")
                return result
            except Exception as err:
                return handle_exception(err, _basemsg)

        _basemsg = create_basemsg(func)
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(func) if func else decorator
