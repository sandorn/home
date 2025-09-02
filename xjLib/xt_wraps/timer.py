# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:56:45
LastEditTime : 2025-09-02 13:32:43
FilePath     : /CODE/xjLib/xt_wraps/timer.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
from functools import wraps
from time import perf_counter
from typing import Any, Callable

from xt_wraps.log import create_basemsg, mylog


def timer_wraps(fn: Callable = None):
    """耗时记录装饰器 - 同时支持同步和异步函数"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                mylog.debug(
                    f"{_basemsg} | Timer-Consuming <{perf_counter() - start_time:.4f} s>"
                )

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                mylog.debug(
                    f"{_basemsg} | Timer-Consuming <{perf_counter() - start_time:.4f} s>"
                )

        _basemsg = create_basemsg(func)
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator(fn) if fn else decorator


timer = timer_wraps


if __name__ == "__main__":

    @timer_wraps
    def test_function(*args):
        total = 0
        for i in range(1000000):
            total += i
        return total

    @timer_wraps
    async def async_test_function():
        """测试异步函数的计时装饰器"""
        await asyncio.sleep(0.1)  # 模拟异步处理时间
        # raise ValueError("异步函数执行失败")
        return "异步函数执行完成"

    async def main():
        result = test_function()
        print(f"1. 测试同步函数结果: {result}")
        result = await async_test_function()
        print(f"2. 测试异步函数结果: {result}")

    asyncio.run(main())