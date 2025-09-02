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
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from loguru import logger
from xt_singleon import SingletonMixin

IS_DEV = os.getenv("ENV", "dev").lower() == "dev"


standard_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
)

# 异常处理逻辑
def handle_exception(err: Exception, msg: str, default_return: Any = None) -> Any:
    if not IS_DEV:  # 开发环境
        mylog.error(
            f"{msg} | log_catch | {type(err).__name__} : {str(err)} | stack trace: {traceback.format_exc()}"
        )
    else:
        mylog.error(f"{msg} | log_catch | {type(err).__name__} : {str(err)}")

    # 返回默认值
    return default_return


def create_basemsg(func: Callable) -> str:
    # 获取原始函数（通过__wrapped__属性）
    original_func = getattr(func, "__wrapped__", func)
    # 递归获取最原始的函数
    while hasattr(original_func, "__wrapped__"):
        original_func = original_func.__wrapped__

    code = getattr(original_func, "__code__")
    _filename = code.co_filename
    _f_lineno = code.co_firstlineno
    return f"{_filename}#{_f_lineno}@{original_func.__name__}"


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

        # 环境判断
        IS_DEV = os.getenv("ENV", "dev").lower() == "dev"
        # 控制台日志（仅开发环境）
        if IS_DEV:
            self.log.add(sys.stderr, level=level, format=standard_format)


mylog = LogCls().log


def log_wraps(
    func: Callable = None,
    log_level: int = 10,
    log_args: bool = True,
    log_result: bool = True,
    default_return: Any = None,
):
    """
    日志记录装饰器,做了except处理 - 同时支持同步和异步函数

    Args:
        func: 被装饰的函数，可选
        log_level: 日志级别，默认10(DEBUG)
        log_args: 是否记录函数参数，默认True
        log_result: 是否记录函数返回结果，默认True
        default_return: 默认返回值，默认为None
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
                    mylog.success(f"{_basemsg} | result: <{result}>")
                else:
                    mylog.success(f"{_basemsg} | successfully")
                return result
            except Exception as err:
                return handle_exception(err, _basemsg, default_return)

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            if log_args:
                mylog.debug(f"{_basemsg} | Args: {args} | Kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                if log_result:
                    mylog.success(f"{_basemsg} | result: <{result}>")
                else:
                    mylog.success(f"{_basemsg} | successfully")
                return result
            except Exception as err:
                return handle_exception(err, _basemsg, default_return)

        _basemsg = create_basemsg(func)
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(func) if func else decorator


if __name__ == "__main__":
    import asyncio

    @log_wraps()
    def test_function(*args):
        total = 0
        for i in range(1000000):
            total += i
        return total

    @log_wraps()
    async def async_test_function(x, y):
        await asyncio.sleep(0.1)  # 模拟异步处理时间
        return x / y

    async def main():
        result = test_function()
        print(f"1. 测试同步函数结果: {result}")
        res2 = await async_test_function(10, 2)
        print(f"2. 测试异步函数结果: {res2}")
        result = await async_test_function(10, 0)
        print(f"3. 测试异步函数结果: {result}")

    asyncio.run(main())
