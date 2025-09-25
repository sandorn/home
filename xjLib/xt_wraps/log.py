# !/usr/bin/env python
"""
==============================================================
Description  : 日志工具模块 - 提供统一的日志记录、格式化和函数装饰器功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-06 11:00:00
FilePath     : /CODE/xjlib/xt_wraps/log.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- LogCls:单例模式的日志配置类,支持文件和控制台日志输出
- create_basemsg:生成包含模块名、行号和函数名的日志基础信息
- log_wraps:日志记录装饰器,同时支持同步和异步函数,提供参数和返回值日志

主要特性:
- 统一的日志格式,包含时间戳、日志级别和消息内容
- 智能路径处理,提取有意义的模块名信息
- 日志文件自动轮转和保留策略
- 开发环境和生产环境差异化日志输出
- 异常捕获和处理机制,确保程序稳定性
==============================================================
"""

from __future__ import annotations

import asyncio
import os
import sys
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import Any

from loguru import logger
from xt_wraps.singleton import SingletonMixin

# 常量定义 - 日志配置参数
IS_DEV = os.getenv('ENV', 'dev').lower() == 'dev'
DEFAULT_LOG_LEVEL = 10  # 默认日志级别(DEBUG)
LOG_FILE_ROTATION_SIZE = '16 MB'  # 日志文件轮转大小
LOG_FILE_RETENTION_DAYS = '30 days'  # 日志文件保留时间
MAX_MODULE_PARTS = 3  # 模块路径最多向上追溯的层数

standard_format = '<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}'


def create_basemsg(func: Callable) -> str:
    """生成日志基础信息,包括模块名、行号和函数名。

    Args:
        func: 要记录的函数对象

    Returns:
        str: 格式化的日志基础信息,格式为"模块名.文件名#行号@函数名"
    """
    # 获取原始函数(处理可能的多层装饰器)
    original_func = func
    while hasattr(original_func, '__wrapped__'):
        original_func = original_func.__wrapped__

    try:
        # 获取代码对象和相关信息
        code = original_func.__code__
        filename = code.co_filename
        line_number = code.co_firstlineno
        func_name = original_func.__name__

        # 处理文件路径
        module_name = _process_file_path(filename)
        return f'{module_name}#{line_number}@{func_name}'
    except Exception:
        # 异常处理,确保函数不会失败
        func_name = getattr(original_func, '__name__', 'unknown')
        return f'unknown#0@{func_name}'


def _process_file_path(file_path: str) -> str:
    """处理文件路径,提取有意义的模块名部分。

    Args:
        file_path: 文件的完整路径

    Returns:
        str: 处理后的模块名
    """
    if not file_path:
        return 'unknown_file'

    try:
        # 规范化路径并分割
        normalized_path = os.path.normpath(file_path)
        file_parts = normalized_path.split(os.sep)
        filename = file_parts[-1] if file_parts else 'unknown_file'

        # 查找项目结构中的关键目录
        root_indicators = ['xjLib', 'tests', 'test', 'src', 'app', 'main']
        module_parts = []

        # 从后向前搜索,找到第一个根目录标识或合适的父目录
        for i in range(len(file_parts) - 2, -1, -1):
            part = file_parts[i]
            if part.startswith('.') or not part:
                continue

            module_parts.insert(0, part)

            # 如果找到根目录标识,停止搜索
            if part.lower() in (indicator.lower() for indicator in root_indicators):
                break

            # 最多向上追溯指定层数的目录
            if len(module_parts) >= MAX_MODULE_PARTS:
                break

        # 构建模块名
        if module_parts:
            return '.'.join([*module_parts, filename])
        if len(file_parts) >= 2:
            return f'{file_parts[-2]}.{filename}'
        return filename
    except Exception:
        return os.path.splitext(os.path.basename(file_path))[0]


class LogCls(SingletonMixin):
    """日志配置类 - 采用单例模式确保全局日志配置一致性
    特殊符号: ▶️ ✅ ❌ ⚠️  🚫 ⛔ ℹ️ ⏹️ 🚨 🚀
    - info() - 带ℹ️符号的INFO级别日志
    - start() - 带▶️符号的DEBUG级别日志
    - stop() - 带⏹️符号的DEBUG级别日志
    - ok() - 带✅符号的SUCCESS级别日志
    - warning() - 带⚠️符号的WARNING级别日志
    - fail() - 带❌符号的ERROR级别日志
    - forbidden() - 带⛔符号的CRITICAL级别日志
    """

    def __init__(self, level=DEFAULT_LOG_LEVEL, logger=logger):
        self.log = logger
        self.log.remove()
        # workspace_root = os.path.dirname(os.getcwd())
        workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 确保logs目录存在
        logs_dir = os.path.join(workspace_root, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, f'xt_{datetime.now().strftime("%Y%m%d")}.log')
        # 文件日志(始终记录)
        self.log.add(
            log_file,
            rotation=LOG_FILE_ROTATION_SIZE,
            retention=LOG_FILE_RETENTION_DAYS,
            level=level,
            encoding='utf-8',
            format=standard_format,
        )

        # 控制台日志(仅开发环境)
        if IS_DEV:
            self.log.add(sys.stderr, level=level, format=standard_format)

    def __call__(self, *args: Any, **kwargs: Any) -> list[None]:
        """支持实例直接调用，用于快速记录多个调试日志信息"""
        return [self.log.debug(arg, **kwargs) for arg in list(args)]

    def __getattr__(self, attr):
        try:
            return getattr(self.log, attr)
        except Exception as err:
            raise AttributeError(f"[{type(self).__name__}].[{attr}]: '{err}'") from err

    def info(self, message: str, **kwargs: Any) -> None:
        """记录带ℹ️ 符号的信息日志(INFO级别)"""
        self.log.info(f'ℹ️ {message}', **kwargs)

    def start(self, message: str, **kwargs: Any) -> None:
        """记录带▶️ 符号的开始日志(DEBUG级别)"""
        self.log.debug(f'▶️ {message}', **kwargs)

    def stop(self, message: str, **kwargs: Any) -> None:
        """记录带⏹️ 符号的停止日志(DEBUG级别)"""
        self.log.debug(f'⏹️ {message}', **kwargs)

    def ok(self, message: str, **kwargs: Any) -> None:
        """记录带✅ 符号的成功日志(SUCCESS级别)"""
        self.log.success(f'✅ {message}', **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """记录带⚠️ 符号的警告日志(WARNING级别)"""
        self.log.warning(f'⚠️ {message}', **kwargs)

    def warn(self, message: str, **kwargs: Any) -> None:
        """记录带⚠️ 符号的警告日志(WARNING级别)"""
        self.log.warning(f'⚠️ {message}', **kwargs)

    def fail(self, message: str, **kwargs: Any) -> None:
        """记录带❌ 符号的失败日志(ERROR级别)"""
        self.log.error(f'❌ {message}', **kwargs)

    def forbidden(self, message: str, **kwargs: Any) -> None:
        """记录带⛔ 符号的禁止日志(CRITICAL级别)"""
        self.log.critical(f'⛔ {message}', **kwargs)


# 全局日志实例
mylog = LogCls()


def log_wraps(
    func: Callable | None = None,
    log_args: bool = False,
    log_result: bool = False,
    re_raise: bool = False,
    default_return: Any = None,
    simplify_traceback: bool = False,
    max_frames: int = 5
) -> Callable:
    """
    增强版日志记录装饰器 - 提供更丰富的异常处理和日志配置选项

    Args:
        func: 被装饰的函数,可选(支持直接装饰和带参数装饰两种方式)
        log_args: 是否记录函数参数,默认为True
        log_result: 是否记录函数返回结果,默认为True
        re_raise: 是否重新抛出异常,默认为True
        default_return: 不重新抛出异常时的默认返回值,默认为None
        simplify_traceback: 是否简化堆栈信息,默认为True
        max_frames: 简化堆栈时显示的最大帧数,默认为5

    Returns:
        装饰后的函数,保持原函数签名和功能

    Example:
        >>> # 1. 增强版装饰器
        >>> @log_wraps(re_raise=False)
        >>> def critical_operation(data):
        >>>     # 关键操作,异常时不中断程序
        >>>     return process_data(data)
        >>>
        >>> # 2. 带详细堆栈信息的装饰器
        >>> @log_wraps(simplify_traceback=False, max_frames=10)
        >>> def debug_operation():
        >>>     # 调试时显示完整堆栈信息
        >>>     return complex_calculation()
    """
    from xt_wraps.exception import handle_exception

    def decorator(func: Callable) -> Callable:
        basemsg = create_basemsg(func)

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """同步函数包装器 - 增强版异常处理和日志记录"""
            if log_args:
                mylog.start(f'{basemsg} | Args: {args} | Kwargs: {kwargs}')
            
            try:
                result = func(*args, **kwargs)
                if log_result:
                    mylog.ok(f'{basemsg} | result: {type(result).__name__} = {result}')

                return result
            except Exception as err:
                # 使用统一的异常处理函数
                return handle_exception(
                    basemsg=basemsg,
                    errinfo=err,
                    re_raise=re_raise,
                    default_return=default_return,
                    simplify_traceback=simplify_traceback,
                    max_frames=max_frames
                )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """异步函数包装器 - 增强版异常处理和日志记录"""
            if log_args:
                mylog.start(f'{basemsg} | Args: {args} | Kwargs: {kwargs}')
            
            try:
                result = await func(*args, **kwargs)
                if log_result:
                    mylog.ok(f'{basemsg} | result: {type(result).__name__} = {result}')

                return result
            except Exception as err:
                # 使用统一的异常处理函数
                return handle_exception(
                    basemsg=basemsg,
                    errinfo=err,
                    re_raise=re_raise,
                    default_return=default_return,
                    simplify_traceback=simplify_traceback,
                    max_frames=max_frames
                )

        # 根据函数类型返回对应的包装函数
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    # 支持两种调用方式:@log_wraps_enhanced 或 @log_wraps_enhanced()
    return decorator(func) if func else decorator
