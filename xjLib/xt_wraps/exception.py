# !/usr/bin/env python
"""
==============================================================
Description  : 异常处理模块 - 提供统一且可配置的异常处理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-05 17:32:29
LastEditTime : 2025-09-05 18:22:15
FilePath     : /CODE/xjLib/xt_wraps/exception.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import traceback
from typing import Any, List


def get_simplified_traceback(
    exc: Exception,
    max_frames: int = 5,
    include_library_frames: bool = False,
    full_path: bool = False,
) -> str:
    """
    获取精简的堆栈跟踪信息

    Args:
        exc: 异常对象
        max_frames: 最大显示的堆栈帧数，默认5
        include_library_frames: 是否包含库文件的堆栈帧，默认False
        full_path: 是否显示完整文件路径，默认False（只显示文件名）

    Returns:
        精简后的堆栈跟踪字符串
    """
    # 获取堆栈信息
    tb = traceback.extract_tb(exc.__traceback__)

    # 处理堆栈帧
    simplified_frames: List[str] = []
    frame_count = 0

    for frame in reversed(tb):  # 从最新的帧开始
        filename = frame.filename

        # 过滤掉库文件的堆栈帧（如果需要）
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
        if not full_path:
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
    simplify_traceback: bool = True,
    max_frames: int = 5,
    include_library_frames: bool = False,
    full_path: bool = False,
) -> Any:
    """
    统一的异常处理函数

    Args:
        err: 异常对象
        context: 异常上下文信息
        re_raise: 是否重新抛出异常，默认False
        default_return: 不抛出异常时的默认返回值
        simplify_traceback: 是否简化堆栈信息，默认True
        max_frames: 简化堆栈时显示的最大帧数，默认5
        include_library_frames: 是否包含库文件的堆栈帧，默认False
        full_path: 是否显示完整文件路径，默认False（只显示文件名）

    Returns:
        默认返回值或重新抛出异常
    """
    # 统一的日志格式
    log_msg = f"{context} | Exception: {type(err).__name__} | {str(err)}"

    if mylog is None:
        from .log import mylog as logger

        mylog = logger
    # 环境感知处理
    if os.getenv("ENV", "dev").lower() == "dev":
        if simplify_traceback and hasattr(err, "__traceback__"):
            # 使用精简的堆栈信息
            stack_info = get_simplified_traceback(
                err,
                max_frames=max_frames,
                include_library_frames=include_library_frames,
                full_path=full_path,
            )
            mylog.error(f"{log_msg} | Stack: {stack_info}")
        else:
            # 使用完整的堆栈信息
            mylog.error(f"{log_msg} | Stack: {traceback.format_exc()}")
    else:
        mylog.error(log_msg)

    # 根据需要重新抛出异常
    if re_raise:
        error_message = f"{context} | {type(err).__name__} | {str(err)}"
        raise Exception(error_message) from err
    else:
        return default_return


# 配置项 - 可以在应用初始化时设置
exception_config = {
    "default_simplify_traceback": True,
    "default_max_frames": 5,
    "include_library_frames": False,
    "show_full_path": False,
}
