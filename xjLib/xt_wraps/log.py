# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 14:39:12
FilePath     : /CODE/xjLib/xt_log.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import sys
from datetime import datetime
from typing import Any, Callable

from loguru import logger
from xt_singleon import SingletonMixin
from xt_wraps.core import decorate_sync_async

standard_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
)


def create_basemsg(func: Callable) -> str:
    code = getattr(func, "__code__")
    _filename = code.co_filename
    _f_lineno = code.co_firstlineno
    return f"{_filename}#{_f_lineno}@{func.__name__}"


class LogCls(SingletonMixin):
    def __init__(self, level=10):
        self.logger = logger
        # 环境判断
        IS_DEV = os.getenv("ENV", "dev").lower() == "dev"
        self.logger.remove()  # 移除默认配置
        # 文件日志（始终记录）
        self.logger.add(
            f"XtLog-{datetime.now().strftime('%Y%m%d')}.log",
            rotation="512 MB",
            retention="180 days",
            level=level,
            encoding="utf-8",
            format=standard_format,
        )

        # 控制台日志（仅开发环境）
        if IS_DEV:
            self.logger.add(sys.stderr, level=level, format=standard_format)


def log_wraps(log_level: int = 10, log_args: bool = True, log_result: bool = True):
    """
    日志记录装饰器

    Args:
        level: 日志级别
        log_args: 是否记录参数
        log_result: 是否记录结果
    """
    mylog = LogCls(log_level).logger

    @decorate_sync_async
    def wrapper(func: Callable, *args: Any, **kwargs: Any) -> Any:
        # 记录函数开始
        _basemsg = create_basemsg(func)

        if log_args:
            mylog.debug(f"{_basemsg} | Args: {args} | Kwargs: {kwargs}")

        # 执行函数
        try:
            result = func(*args, **kwargs)
            if log_result:
                mylog.success(f"{_basemsg} | returned: {result}")
            else:
                mylog.success(f"{_basemsg} | successfully")
            return result
        except Exception as err:
            mylog.error(f"{_basemsg} | error: {err!r}")
            raise
    return wrapper


if __name__ == "__main__":
    @log_wraps()
    def test1(*args):
        return 9 / 3

    @log_wraps()
    def test2(*args):
        return 9 / 2

    test1()
    test2()

    @log_wraps()
    def risky_operation(x, y):
        """一个可能失败的操作"""
        if x < 0:
            raise ValueError("x不能为负数")
        return x / y

    # 使用
    result = risky_operation(10, 0)
    # print(f"结果: {result}")
