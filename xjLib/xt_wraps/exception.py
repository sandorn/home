# !/usr/bin/env python
"""
==============================================================
Description  : 异常处理模块 - 提供统一、可配置的异常处理和堆栈信息管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-05 17:32:29
LastEditTime : 2025-09-06 10:30:00
FilePath     : /CODE/xjLib/xt_wraps/exception.py
Github       : https://github.com/sandorn/home

本模块提供了两个核心功能：
- get_simplified_traceback: 获取精简的堆栈跟踪信息，支持自定义显示帧数、过滤库文件帧等
- handle_exception: 统一的异常处理函数，支持日志记录、堆栈简化、异常重抛等功能

使用场景：
- 简化调试过程中的异常信息分析
- 统一应用程序的异常处理逻辑
- 在不同环境中动态调整异常信息的详细程度
- 提供友好的错误反馈和日志记录
==============================================================
"""

import os
import traceback
from typing import Any, List

# 常量定义 - 异常处理配置参数
DEFAULT_MAX_FRAMES = 5  # 默认最大显示堆栈帧数
DEFAULT_SIMPLIFY_TRACEBACK = True  # 默认是否简化堆栈信息
DEFAULT_INCLUDE_LIBRARY_FRAMES = False  # 默认是否包含库文件堆栈帧
DEFAULT_SHOW_FULL_PATH = False  # 默认是否显示完整文件路径


def get_simplified_traceback(
    exc: Exception,
    max_frames: int = DEFAULT_MAX_FRAMES,
    include_library_frames: bool = DEFAULT_INCLUDE_LIBRARY_FRAMES,
    show_full_path: bool = DEFAULT_SHOW_FULL_PATH,
) -> str:
    """
    获取精简的堆栈跟踪信息，过滤不必要的信息，提高可读性

    Args:
        exc: 异常对象，必须包含__traceback__属性
        max_frames: 最大显示的堆栈帧数，默认5帧，可以根据需要调整
        include_library_frames: 是否包含库文件的堆栈帧，默认False（不包含）
        show_full_path: 是否显示完整文件路径，默认False（只显示文件名）

    Returns:
        str: 精简后的堆栈跟踪字符串，格式为"file:line in func | file:line in func..."

    Example:
        >>> try:
        ...     1/0
        ... except ZeroDivisionError as e:
        ...     tb = get_simplified_traceback(e)
        ...     print(tb)
        test_script.py:2 in <module>
    """
    # 获取堆栈信息
    tb = traceback.extract_tb(exc.__traceback__)

    # 处理堆栈帧
    simplified_frames: List[str] = []
    frame_count = 0

    for frame in reversed(tb):  # 从最新的帧开始处理
        filename = frame.filename

        # 过滤掉库文件的堆栈帧（如果不需要）
        if not include_library_frames:
            # 常见的库路径判断
            if any(
                path in filename.lower()
                for path in [
                    "site-packages",
                    "dist-packages",
                    "python\\lib",
                    "python3\\lib",
                ]
            ):
                continue

        # 限制显示的帧数
        if frame_count >= max_frames:
            simplified_frames.append("...")
            break

        # 格式化文件名
        if not show_full_path:
            filename = os.path.basename(filename)

        # 格式化行号和函数名
        frame_str = f"{filename}:{frame.lineno} in {frame.name}"
        simplified_frames.append(frame_str)
        frame_count += 1

    # 反转回正确的顺序（最旧到最新）
    simplified_frames.reverse()

    # 构建最终的堆栈信息
    stack_info = " | ".join(simplified_frames)
    return stack_info


def handle_exception(
    err: Exception,
    context: str,
    mylog: Any = None,
    re_raise: bool = False,
    default_return: Any = None,
    simplify_traceback: bool = DEFAULT_SIMPLIFY_TRACEBACK,
    max_frames: int = DEFAULT_MAX_FRAMES,
    include_library_frames: bool = DEFAULT_INCLUDE_LIBRARY_FRAMES,
    show_full_path: bool = DEFAULT_SHOW_FULL_PATH,
) -> Any:
    """
    统一的异常处理函数，提供完整的异常捕获、记录和处理机制

    Args:
        err: 异常对象
        context: 异常上下文信息，通常包含函数名、文件名等标识信息
        mylog: 日志记录器实例，如果为None则使用模块内的默认日志记录器
        re_raise: 是否重新抛出异常，默认False（不抛出，返回默认值）
        default_return: 不抛出异常时的默认返回值，默认为None
        simplify_traceback: 是否简化堆栈信息，默认True（简化）
        max_frames: 简化堆栈时显示的最大帧数，默认5帧
        include_library_frames: 是否包含库文件的堆栈帧，默认False（不包含）
        show_full_path: 是否显示完整文件路径，默认False（只显示文件名）

    Returns:
        Any: 如果re_raise=False，返回default_return；否则重新抛出异常

    Example:
        >>> # 基本使用
        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     # 记录异常但不中断程序
        ...     result = handle_exception(e, "除法计算出错", re_raise=False, default_return=0)
        >>> print(result)  # 输出: 0

        >>> # 带日志记录器和重新抛出异常
        >>> import logging
        >>> logger = logging.getLogger(__name__)
        >>> try:
        ...     10 / 0
        ... except Exception as e:
        ...     handle_exception(
        ...         e,
        ...         "critical_operation",
        ...         mylog=logger,
        ...         re_raise=True,
        ...         simplify_traceback=True,
        ...         max_frames=3
        ...     )
    """
    # 统一的日志格式
    log_msg = f"{context} | {type(err).__name__} | {str(err)}"

    # 如果没有提供日志记录器，使用标准错误输出
    if mylog is None:
        from .log import mylog as logger
        mylog = logger

    # 环境感知处理 - 开发环境显示更详细的堆栈信息
    if os.getenv("ENV", "dev").lower() == "dev":
        if simplify_traceback and hasattr(err, "__traceback__"):
            # 使用精简的堆栈信息
            stack_info = get_simplified_traceback(
                err,
                max_frames=max_frames,
                include_library_frames=include_library_frames,
                show_full_path=show_full_path,
            )
            mylog.error(f"{log_msg} | Stack: {stack_info}")
        else:
            # 使用完整的堆栈信息
            mylog.error(f"{log_msg} | Stack: {traceback.format_exc()}")
    else:
        # 生产环境仅记录必要信息
        mylog.error(log_msg)

    # 根据需要重新抛出异常
    if re_raise:
        error_message = f"{context} | {type(err).__name__} | {str(err)}"
        raise type(err)(error_message) from err
    else:
        return default_return
