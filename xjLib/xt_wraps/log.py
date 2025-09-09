# !/usr/bin/env python
"""
==============================================================
Description  : 日志工具模块 - 提供统一的日志记录、格式化和函数装饰器功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-06 11:00:00
FilePath     : /CODE/xjLib/xt_wraps/log.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- LogCls：单例模式的日志配置类，支持文件和控制台日志输出
- create_basemsg：生成包含模块名、行号和函数名的日志基础信息
- log_wraps：日志记录装饰器，同时支持同步和异步函数，提供参数和返回值日志

主要特性：
- 统一的日志格式，包含时间戳、日志级别和消息内容
- 智能路径处理，提取有意义的模块名信息
- 日志文件自动轮转和保留策略
- 开发环境和生产环境差异化日志输出
- 异常捕获和处理机制，确保程序稳定性
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

# 常量定义 - 日志配置参数
IS_DEV = os.getenv("ENV", "dev").lower() == "dev"
DEFAULT_LOG_LEVEL = 10  # 默认日志级别（DEBUG）
LOG_FILE_ROTATION_SIZE = "512 MB"  # 日志文件轮转大小
LOG_FILE_RETENTION_DAYS = "180 days"  # 日志文件保留时间
MAX_MODULE_PARTS = 3  # 模块路径最多向上追溯的层数


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

        # 智能路径处理逻辑
        module_name = _process_file_path(filename)

        return f"{module_name}#{line_number}@{func_name}"
    except Exception:
        # 终极异常处理，确保函数不会失败
        func_name = getattr(original_func, "__name__", "unknown")
        return f"unknown#0@{func_name}"


def _process_file_path(file_path: str) -> str:
    """处理文件路径，提取有意义的模块名部分。

    Args:
        file_path: 文件的完整路径

    Returns:
        str: 处理后的模块名
    """
    # 规范化路径并处理可能的空值
    if not file_path:
        return "unknown_file"

    try:
        # 规范化路径并分割
        normalized_path = os.path.normpath(file_path)
        file_parts = normalized_path.split(os.sep)

        # 提取文件名（包含扩展名）
        filename = file_parts[-1] if file_parts else "unknown_file"

        # 尝试智能识别项目结构中的关键目录
        # 1. 查找项目根目录标识
        root_indicators = ["xjLib", "tests", "test", "src", "app", "main"]
        module_parts = []

        # 从后向前搜索，找到第一个根目录标识或合适的父目录
        for i in range(len(file_parts) - 2, -1, -1):
            part = file_parts[i]
            # 跳过隐藏目录和无效目录名
            if part.startswith(".") or not part:
                continue

            module_parts.insert(0, part)

            # 如果找到根目录标识，停止搜索
            if part.lower() in (indicator.lower() for indicator in root_indicators):
                break

            # 最多向上追溯指定层数的目录，避免路径过长
            if len(module_parts) >= MAX_MODULE_PARTS:
                break

        # 构建模块名
        if module_parts:
            # 添加模块路径部分和文件名
            return ".".join(module_parts + [filename])
        elif len(file_parts) >= 2:
            # 回退到原始逻辑：父目录.文件名
            parent_dir = file_parts[-2]
            return f"{parent_dir}.{filename}"
        else:
            # 如果路径部分不足，直接使用文件名
            return filename

    except Exception:
        # 异常情况下回退到基本文件名（不带扩展名）作为最后手段
        return os.path.splitext(os.path.basename(file_path))[0]


class LogCls(SingletonMixin):
    """日志配置类 - 采用单例模式确保全局日志配置一致性"""

    def __init__(self, level=DEFAULT_LOG_LEVEL, logger=logger):
        self.log = logger
        # 移除默认配置
        self.log.remove()

        # 文件日志（始终记录）
        log_file = f"XtLog-{datetime.now().strftime('%Y%m%d')}.log"
        self.log.add(
            log_file,
            rotation=LOG_FILE_ROTATION_SIZE,
            retention=LOG_FILE_RETENTION_DAYS,
            level=level,
            encoding="utf-8",
            format=standard_format,
        )

        # 控制台日志（仅开发环境）
        if IS_DEV:
            self.log.add(sys.stderr, level=level, format=standard_format)


# 全局日志实例
mylog = LogCls().log


def log_wraps(
    func: Callable = None,
    log_level: int = DEFAULT_LOG_LEVEL,
    log_args: bool = True,
    log_result: bool = True,
):
    """
    日志记录装饰器 - 同时支持同步和异步函数，提供参数、返回值记录和异常处理

    Args:
        func: 被装饰的函数，可选（支持直接装饰和带参数装饰两种方式）
        log_level: 日志级别，默认10(DEBUG)
        log_args: 是否记录函数参数，默认True
        log_result: 是否记录函数返回结果，默认True

    Returns:
        装饰后的函数，保持原函数签名和功能

    Example:
        >>> # 1. 直接装饰同步函数
        >>> @log_wraps
        >>> def add(x, y):
        >>>     return x + y
        >>>
        >>> # 2. 带参数装饰异步函数
        >>> @log_wraps(log_result=False)
        >>> async def process_data(data):
        >>>     await asyncio.sleep(1)
        >>>     return f"Processed: {data}"
        >>>
        >>> # 3. 完整参数设置
        >>> @log_wraps(log_level=20, log_args=True, log_result=True)
        >>> def complex_operation(param1, param2=None):
        >>>     # 函数实现
        >>>     return result
    """

    def decorator(func: Callable) -> Callable:
        # 生成基础日志信息，避免在每次函数调用时重新计算
        _basemsg = create_basemsg(func)

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """同步函数包装器 - 处理同步函数的日志记录和异常捕获"""
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
                # 使用统一的异常处理模块
                return handle_exception(
                    err=err,
                    context=_basemsg,
                    loger=mylog,
                    re_raise=False,
                    default_return=None,
                )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """异步函数包装器 - 处理异步函数的日志记录和异常捕获"""
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
                # 使用统一的异常处理模块
                return handle_exception(
                    err=err,
                    context=_basemsg,
                    loger=mylog,
                    re_raise=False,
                    default_return=None,
                )

        # 根据函数类型返回对应的包装函数
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    # 支持两种调用方式：@log_wraps 或 @log_wraps()
    return decorator(func) if func else decorator
