# !/usr/bin/env python
"""
==============================================================
Description  : 异步执行器模块测试文件
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 11:46:00
LastEditTime : 2025-09-06 08:30:00
FilePath     : /CODE/xjLib/xt_wraps/test/test_executor.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from __future__ import annotations

import asyncio
import contextlib
import time
from concurrent.futures import ThreadPoolExecutor

from xt_wraps.executor import (
    executor_wraps,
    future_wraps,
    future_wraps_result,
    run_executor_wraps,
)

# 测试用常量
TEST_SLEEP_SHORT = 0.1  # 短时间睡眠（用于快速测试）
TEST_SLEEP_MEDIUM = 0.5  # 中等时间睡眠（用于稍长的测试）
TEST_SLEEP_LONG = 1.0  # 长时间睡眠（用于模拟实际网络延迟）


# 1. executor_wraps 相关测试函数 - 连续序号便于查找
@executor_wraps
def sync_test_function():
    """1.1 测试同步函数的执行器装饰器"""
    time.sleep(TEST_SLEEP_MEDIUM)  # 模拟耗时操作
    return '同步函数执行结果'


@executor_wraps
def sync_test_with_params(a, b):
    """1.2 测试带参数的同步函数"""
    time.sleep(TEST_SLEEP_SHORT)
    return a + b


@executor_wraps(background=True)
def sync_background_function():
    """1.3 测试同步函数的后台执行"""
    time.sleep(TEST_SLEEP_LONG)  # 模拟较长时间操作
    return '后台同步函数执行结果'


# 自定义执行器
custom_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix='CustomExecutor')


@executor_wraps(executor=custom_executor)
def sync_custom_executor():
    """1.4 测试使用自定义执行器的同步函数"""
    time.sleep(TEST_SLEEP_MEDIUM)
    return '自定义执行器函数结果'


@executor_wraps
def sync_test_with_exception():
    """1.5 测试会抛出异常的同步函数"""
    time.sleep(TEST_SLEEP_SHORT)
    raise ValueError('同步函数测试异常')


@executor_wraps
async def async_test_function():
    """1.6 测试异步函数的执行器装饰器"""
    await asyncio.sleep(TEST_SLEEP_MEDIUM)  # 模拟异步耗时操作
    return '异步函数执行结果'


@executor_wraps
async def async_test_with_params(a, b):
    """1.7 测试带参数的异步函数"""
    await asyncio.sleep(TEST_SLEEP_SHORT)
    return a * b


@executor_wraps(background=True)
async def async_background_function():
    """1.8 测试异步函数的后台执行"""
    await asyncio.sleep(TEST_SLEEP_LONG)  # 模拟较长时间操作
    return '后台异步函数执行结果'


@executor_wraps
async def async_test_with_exception():
    """1.9 测试会抛出异常的异步函数"""
    await asyncio.sleep(TEST_SLEEP_SHORT)
    raise ValueError('异步函数测试异常')


# 2. run_executor_wraps 相关测试函数 - 连续序号便于查找
@run_executor_wraps
async def async_function_for_run_executor():
    """2.1 测试run_executor_wraps装饰的异步函数"""
    await asyncio.sleep(TEST_SLEEP_MEDIUM)
    return '异步函数完成'


@run_executor_wraps
def sync_function_for_run_executor():
    """2.2 测试run_executor_wraps装饰的同步函数"""
    time.sleep(TEST_SLEEP_SHORT)
    return '同步函数完成'


@run_executor_wraps
def sync_function_with_params(a, b):
    """2.3 测试run_executor_wraps装饰的带参数同步函数"""
    time.sleep(TEST_SLEEP_SHORT)
    return a * b


@run_executor_wraps
def sync_function_with_exception():
    """2.4 测试run_executor_wraps装饰的异常处理"""
    time.sleep(TEST_SLEEP_SHORT)
    raise ValueError('run_executor_wraps测试异常')


# 3. future_wraps 相关测试函数 - 连续序号便于查找
@future_wraps
def future_test_function(a, b):
    """3.1 测试future_wraps装饰器"""
    time.sleep(TEST_SLEEP_SHORT)
    return a + b


@future_wraps
def future_test_with_exception(a, b):
    """3.2 测试future_wraps装饰器的异常处理"""
    time.sleep(TEST_SLEEP_SHORT)
    return a / b  # 当b=0时会抛出异常


@future_wraps(executor=custom_executor)
def future_test_custom_executor(a, b):
    """3.3 测试future_wraps装饰器使用自定义执行器"""
    time.sleep(TEST_SLEEP_SHORT)
    return a - b


# 测试执行函数 - 使用连续序号便于查找和管理
async def run_all_tests():
    """主测试函数，按顺序执行所有测试用例"""

    # ========== 1. 测试 executor_wraps 装饰器 ==========

    # 1.1 测试同步函数的正常执行
    await sync_test_function()

    # 1.2 测试同步函数带参数
    await sync_test_with_params(10, 20)

    # 1.3 测试同步函数的后台执行
    future = sync_background_function()  # 这里不需要await
    # 等待后台任务完成并获取结果
    await future  # 这里需要await来获取结果

    # 1.4 测试使用自定义执行器的同步函数
    await sync_custom_executor()

    # 1.5 测试同步函数异常处理
    with contextlib.suppress(ValueError):
        await sync_test_with_exception()

    # 1.6 测试异步函数的正常执行
    await async_test_function()

    # 1.7 测试异步函数带参数
    await async_test_with_params(10, 20)

    # 1.8 测试异步函数的后台执行
    task = async_background_function()  # 这里不需要await
    # 等待后台任务完成并获取结果
    await task  # 这里需要await来获取结果

    # 1.9 测试异步函数异常处理
    with contextlib.suppress(ValueError):
        await async_test_with_exception()

    # ========== 2. 测试 run_executor_wraps 装饰器 ==========

    # 2.1 测试异步函数同步调用
    async_function_for_run_executor()

    # 2.2 测试同步函数调用
    sync_function_for_run_executor()

    # 2.3 测试带参数同步函数
    sync_function_with_params(10, 5)

    # 2.4 测试异常处理
    with contextlib.suppress(ValueError):
        sync_function_with_exception()

    # ========== 3. 测试 future_wraps 装饰器 ==========

    # 3.1 测试正常执行
    future = future_test_function(10, 20)
    await future

    # 3.2 测试异常处理
    future = future_test_with_exception(10, 0)  # 除以0会抛出异常
    with contextlib.suppress(ZeroDivisionError):
        await future

    # 3.3 测试自定义执行器
    future = future_test_custom_executor(30, 10)
    await future

    # ========== 4. 测试 future_wraps_result 函数 ==========

    # 4.1 测试正常执行
    future = future_test_function(50, 60)
    await future_wraps_result(future)

    # 4.2 测试异常处理
    future = future_test_with_exception(100, 0)  # 除以0会抛出异常
    with contextlib.suppress(ZeroDivisionError):
        await future_wraps_result(future)

    # ========== 5. 测试并发执行能力 ==========

    # 创建多个任务同时执行
    tasks = []
    for i in range(5):
        tasks.append(sync_test_with_params(i, i * 10))

    results = await asyncio.gather(*tasks)

    for i, _result in enumerate(results):
        pass

    # ========== 6. 测试混合执行（同步+异步+后台） ==========

    # 同时执行不同类型的任务
    sync_task = sync_test_function()
    async_task = async_test_function()
    background_task = sync_background_function()

    # 等待所有任务完成
    results = await asyncio.gather(sync_task, async_task, background_task, return_exceptions=True)

    # 特别处理后台任务结果 - 它可能仍然是Future对象
    if isinstance(results[2], asyncio.Future):
        if results[2].done():
            try:
                # 尝试获取Future的结果
                results[2].result()
            except Exception:
                pass
        else:
            # 如果Future仍在运行，我们可以选择等待它完成
            pass
            # 注意：如果需要确保后台任务完成，应该在这里添加 await，但这会阻塞测试直到它完成

    # 关闭自定义执行器
    custom_executor.shutdown()


if __name__ == '__main__':
    asyncio.run(run_all_tests())
