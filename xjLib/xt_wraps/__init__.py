# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-28 10:53:57
LastEditTime : 2025-09-02 14:32:04
FilePath     : /CODE/xjLib/xt_wraps/__init__.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from xt_wraps.core import decorate_sync_async
from xt_wraps.executor import (
    executor_wraps,
    future_wraps,
    future_wraps_result,
    run_executor_wraps,
)
from xt_wraps.log import create_basemsg, log_wraps, mylog
from xt_wraps.retry import retry_wraps
from xt_wraps.timer import timer, timer_wraps

__all__ = [
    "retry_wraps",
    "log_wraps",
    "mylog",
    "create_basemsg",
    "timer_wraps",
    "timer",
    "decorate_sync_async",
    "executor_wraps",
    "run_executor_wraps",
    "future_wraps",
    "future_wraps_result",
]

if __name__ == "__main__":
    import asyncio

    @timer_wraps
    @log_wraps
    def test_function(*args):
        total = 0
        for i in range(1000000):
            total += i
        return total
        # raise ValueError("值太小")

    @timer_wraps
    @log_wraps
    @retry_wraps
    async def async_test_function(x, y):
        """一个可能失败的操作"""
        await asyncio.sleep(0.1)  # 模拟异步处理时间
        return x / y

    @log_wraps
    @timer_wraps
    @retry_wraps
    async def async_test_function2(*args):
        """一个可能失败的操作"""
        await asyncio.sleep(0.1)  # 模拟异步处理时间
        raise Exception("值太小")

    async def main():
        result = test_function()
        print(f"1. 测试同步函数结果: {result}")
        res2 = await async_test_function(10, 2)
        print(f"2. 测试异步函数结果: {res2}")
        res3 = await async_test_function(10, 0)
        print(f"3. 测试异步函数结果: {res3}")
        res4 = await async_test_function2(10, 0)
        print(f"4. 测试异步函数结果: {res4}")

    asyncio.run(main())
