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
import threading
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
    print(f'同步函数在 {time.strftime("%H:%M:%S")} 开始执行 - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_MEDIUM)  # 模拟耗时操作
    print(f'同步函数在 {time.strftime("%H:%M:%S")} 执行完成 - 线程: {threading.current_thread().name}')
    return '同步函数执行结果'


@executor_wraps
def sync_test_with_params(a, b):
    """1.2 测试带参数的同步函数"""
    print(f'带参数的同步函数: {a} + {b} - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_SHORT)
    return a + b


@executor_wraps(background=True)
def sync_background_function():
    """1.3 测试同步函数的后台执行"""
    print(f'后台同步函数在 {time.strftime("%H:%M:%S")} 开始执行 - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_LONG)  # 模拟较长时间操作
    print(f'后台同步函数在 {time.strftime("%H:%M:%S")} 执行完成 - 线程: {threading.current_thread().name}')
    return '后台同步函数执行结果'


# 自定义执行器
custom_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix='CustomExecutor')


@executor_wraps(executor=custom_executor)
def sync_custom_executor():
    """1.4 测试使用自定义执行器的同步函数"""
    print(f'自定义执行器函数在 {time.strftime("%H:%M:%S")} 开始执行 - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_MEDIUM)
    print(f'自定义执行器函数在 {time.strftime("%H:%M:%S")} 执行完成 - 线程: {threading.current_thread().name}')
    return '自定义执行器函数结果'


@executor_wraps
def sync_test_with_exception():
    """1.5 测试会抛出异常的同步函数"""
    print('测试同步函数异常')
    time.sleep(TEST_SLEEP_SHORT)
    raise ValueError('同步函数测试异常')


@executor_wraps
async def async_test_function():
    """1.6 测试异步函数的执行器装饰器"""
    print(f'异步函数在 {time.strftime("%H:%M:%S")} 开始执行')
    await asyncio.sleep(TEST_SLEEP_MEDIUM)  # 模拟异步耗时操作
    print(f'异步函数在 {time.strftime("%H:%M:%S")} 执行完成')
    return '异步函数执行结果'


@executor_wraps
async def async_test_with_params(a, b):
    """1.7 测试带参数的异步函数"""
    print(f'带参数的异步函数: {a} * {b}')
    await asyncio.sleep(TEST_SLEEP_SHORT)
    return a * b


@executor_wraps(background=True)
async def async_background_function():
    """1.8 测试异步函数的后台执行"""
    print(f'后台异步函数在 {time.strftime("%H:%M:%S")} 开始执行')
    await asyncio.sleep(TEST_SLEEP_LONG)  # 模拟较长时间操作
    print(f'后台异步函数在 {time.strftime("%H:%M:%S")} 执行完成')
    return '后台异步函数执行结果'


@executor_wraps
async def async_test_with_exception():
    """1.9 测试会抛出异常的异步函数"""
    print('测试异步函数异常')
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
    print(f'future_wraps函数执行: {a} + {b} - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_SHORT)
    return a + b


@future_wraps
def future_test_with_exception(a, b):
    """3.2 测试future_wraps装饰器的异常处理"""
    print(f'future_wraps异常函数执行: {a} / {b} - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_SHORT)
    return a / b  # 当b=0时会抛出异常


@future_wraps(executor=custom_executor)
def future_test_custom_executor(a, b):
    """3.3 测试future_wraps装饰器使用自定义执行器"""
    print(f'future_wraps自定义执行器函数: {a} - {b} - 线程: {threading.current_thread().name}')
    time.sleep(TEST_SLEEP_SHORT)
    return a - b


# 测试执行函数 - 使用连续序号便于查找和管理
async def run_all_tests():
    """主测试函数，按顺序执行所有测试用例"""
    print('===== 开始测试 xt_wraps.executor 模块 ======')

    # ========== 1. 测试 executor_wraps 装饰器 ==========
    print('\n===== 1. 测试 executor_wraps 装饰器 ======')

    # 1.1 测试同步函数的正常执行
    print('\n1.1 测试同步函数的正常执行:')
    result = await sync_test_function()
    print(f'同步函数结果: {result}')

    # 1.2 测试同步函数带参数
    print('\n1.2 测试同步函数带参数:')
    result = await sync_test_with_params(10, 20)
    print(f'带参数同步函数结果: {result}')

    # 1.3 测试同步函数的后台执行
    print('\n1.3 测试同步函数的后台执行:')
    future = sync_background_function()  # 这里不需要await
    print(f'后台任务已提交，返回的是Future对象: {isinstance(future, asyncio.Future)}')
    # 等待后台任务完成并获取结果
    result = await future  # 这里需要await来获取结果
    print(f'后台任务结果: {result}')

    # 1.4 测试使用自定义执行器的同步函数
    print('\n1.4 测试使用自定义执行器的同步函数:')
    result = await sync_custom_executor()
    print(f'自定义执行器函数结果: {result}')

    # 1.5 测试同步函数异常处理
    print('\n1.5 测试同步函数异常处理:')
    try:
        result = await sync_test_with_exception()
        print(f'异常函数结果: {result}')
    except ValueError as e:
        print(f'成功捕获同步函数异常: {e}')

    # 1.6 测试异步函数的正常执行
    print('\n1.6 测试异步函数的正常执行:')
    result = await async_test_function()
    print(f'异步函数结果: {result}')

    # 1.7 测试异步函数带参数
    print('\n1.7 测试异步函数带参数:')
    result = await async_test_with_params(10, 20)
    print(f'带参数异步函数结果: {result}')

    # 1.8 测试异步函数的后台执行
    print('\n1.8 测试异步函数的后台执行:')
    task = async_background_function()  # 这里不需要await
    print(f'后台任务已提交，返回的是Task对象: {isinstance(task, asyncio.Task)}')
    # 等待后台任务完成并获取结果
    result = await task  # 这里需要await来获取结果
    print(f'后台任务结果: {result}')

    # 1.9 测试异步函数异常处理
    print('\n1.9 测试异步函数异常处理:')
    try:
        result = await async_test_with_exception()
        print(f'异常函数结果: {result}')
    except ValueError as e:
        print(f'成功捕获异步函数异常: {e}')

    # ========== 2. 测试 run_executor_wraps 装饰器 ==========
    print('\n===== 2. 测试 run_executor_wraps 装饰器 ======')

    # 2.1 测试异步函数同步调用
    print('\n2.1 测试异步函数同步调用:')
    result = async_function_for_run_executor()
    print(f'异步函数同步调用结果: {result}')

    # 2.2 测试同步函数调用
    print('\n2.2 测试同步函数调用:')
    result = sync_function_for_run_executor()
    print(f'同步函数调用结果: {result}')

    # 2.3 测试带参数同步函数
    print('\n2.3 测试带参数同步函数:')
    result = sync_function_with_params(10, 5)
    print(f'带参数同步函数结果: {result}')

    # 2.4 测试异常处理
    print('\n2.4 测试异常处理:')
    try:
        result = sync_function_with_exception()
        print(f'异常函数结果: {result}')
    except ValueError as e:
        print(f'成功捕获异常: {e}')

    # ========== 3. 测试 future_wraps 装饰器 ==========
    print('\n===== 3. 测试 future_wraps 装饰器 ======')

    # 3.1 测试正常执行
    print('\n3.1 测试future_wraps正常执行:')
    future = future_test_function(10, 20)
    print(f'返回的是Future对象: {isinstance(future, asyncio.Future)}')
    result = await future
    print(f'Future结果: {result}')

    # 3.2 测试异常处理
    print('\n3.2 测试future_wraps异常处理:')
    future = future_test_with_exception(10, 0)  # 除以0会抛出异常
    try:
        result = await future
        print(f'异常函数结果: {result}')
    except ZeroDivisionError as e:
        print(f'成功捕获Future异常: {e}')

    # 3.3 测试自定义执行器
    print('\n3.3 测试future_wraps自定义执行器:')
    future = future_test_custom_executor(30, 10)
    result = await future
    print(f'自定义执行器Future结果: {result}')

    # ========== 4. 测试 future_wraps_result 函数 ==========
    print('\n===== 4. 测试 future_wraps_result 函数 ======')

    # 4.1 测试正常执行
    print('\n4.1 测试future_wraps_result正常执行:')
    future = future_test_function(50, 60)
    result = await future_wraps_result(future)
    print(f'future_wraps_result结果: {result}')

    # 4.2 测试异常处理
    print('\n4.2 测试future_wraps_result异常处理:')
    future = future_test_with_exception(100, 0)  # 除以0会抛出异常
    try:
        result = await future_wraps_result(future)
        print(f'异常函数结果: {result}')
    except ZeroDivisionError as e:
        print(f'成功捕获future_wraps_result异常: {e}')

    # ========== 5. 测试并发执行能力 ==========
    print('\n===== 5. 测试并发执行能力 ======')

    # 创建多个任务同时执行
    tasks = []
    for i in range(5):
        tasks.append(sync_test_with_params(i, i * 10))

    print(f'\n创建了 {len(tasks)} 个并发任务')
    results = await asyncio.gather(*tasks)

    print('所有任务完成，结果:')
    for i, result in enumerate(results):
        print(f'任务 {i}: {result}')

    # ========== 6. 测试混合执行（同步+异步+后台） ==========
    print('\n===== 6. 测试混合执行 ======')

    # 同时执行不同类型的任务
    sync_task = sync_test_function()
    async_task = async_test_function()
    background_task = sync_background_function()

    # 等待所有任务完成
    results = await asyncio.gather(sync_task, async_task, background_task, return_exceptions=True)

    print('混合执行结果:')
    print(f'同步任务结果: {results[0] if not isinstance(results[0], Exception) else f"异常: {results[0]}"}')
    print(f'异步任务结果: {results[1] if not isinstance(results[1], Exception) else f"异常: {results[1]}"}')

    # 特别处理后台任务结果 - 它可能仍然是Future对象
    if isinstance(results[2], asyncio.Future):
        if results[2].done():
            try:
                # 尝试获取Future的结果
                bg_result = results[2].result()
                print(f'后台任务结果: {bg_result}')
            except Exception as e:
                print(f'后台任务异常: {e}')
        else:
            # 如果Future仍在运行，我们可以选择等待它完成
            print(f'后台任务仍在运行中: {results[2]}')
            # 注意：如果需要确保后台任务完成，应该在这里添加 await，但这会阻塞测试直到它完成
    else:
        print(f'后台任务结果: {results[2] if not isinstance(results[2], Exception) else f"异常: {results[2]}"}')

    print('\n===== 所有测试完成! =====')
    # 关闭自定义执行器
    custom_executor.shutdown()


if __name__ == '__main__':
    asyncio.run(run_all_tests())
