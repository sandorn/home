# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:56:45
LastEditTime : 2025-08-30 19:50:18
FilePath     : /CODE/xjLib/xt_wraps/timer.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import datetime
import time
from time import perf_counter
from typing import Any, Callable

from xt_wraps.core import decorate_sync_async, func_sync_async
from xt_wraps.log import LogCls, create_basemsg

mylog = LogCls().logger

class TimeContextManager:
    """上下文管理器计时器"""
    def __enter__(self):
        self.start = perf_counter()

    def __exit__(self, *args):
        print(
            f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | TimeContextManager | <Time-Consuming {perf_counter() - self.start:.4f} s>"
        )


def timer_wraps():
    """耗时记录装饰器"""

    @decorate_sync_async
    def decorator(func: Callable, *args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        _basemsg = create_basemsg(func)
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            mylog.debug(
                f"{_basemsg} | timer | <Time-Consuming {perf_counter() - start_time:.4f} s>"
            )

    return decorator


def timer_deco():
    """耗时记录装饰器 - 同时支持同步和异步函数的计时"""
    def decorator(func: Callable) -> Callable:
        # 定义一个函数，它接收func作为第一个参数，然后是调用参数
        # 这与decorate_sync_async的工作方式匹配
        @func_sync_async
        def timer_decorator(*args: Any, **kwargs: Any) -> Any:
            # 执行原始函数
            return func(*args, **kwargs)
        
        # 外部包装函数，负责计时和日志记录
        def outer_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            _basemsg = create_basemsg(func)
            try:
                # 调用装饰后的函数，传入原始函数和调用参数
                return timer_decorator(*args, **kwargs)
            finally:
                mylog.debug(
                    f"{_basemsg} | timer | <Time-Consuming {perf_counter() - start_time:.4f} s>"
                )
                
        # 保留原始函数的元数据
        outer_wrapper.__name__ = func.__name__
        outer_wrapper.__doc__ = func.__doc__
        outer_wrapper.__module__ = func.__module__
        
        return outer_wrapper
    
    return decorator


if __name__ == "__main__":
    import asyncio

    with TimeContextManager():
        time.sleep(0.01)
        print("with Timer......")

    @timer_deco()
    def risky_operation(x, y):
        """一个可能失败的操作"""
        time.sleep(0.01)
        # raise RuntimeError("x不能为负数")
        return x / y

    print(f"结果: {risky_operation(10, 2)}")

    @timer_deco()
    async def async_risky_operation(x, y):
        """一个可能失败的异步操作"""
        await asyncio.sleep(1)  # 模拟异步操作
        # raise RuntimeError("xx不能为负数")
        return x / y

    print(f"结果: {asyncio.run(async_risky_operation(144, 12))}")
