# !/usr/bin/env python
"""
==============================================================
Description  : 测试log_wraps装饰器功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-06 08:45:00
LastEditTime : 2025-09-06 08:45:00
FilePath     : /CODE/xjLib/xt_wraps/test/test_log_wraps.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import time

from xt_wraps.log import log_wraps

# 常量定义
TEST_SLEEP_TIME = 0.1  # 测试用的睡眠时间（秒）
TEST_DEBUG_LOG_LEVEL = 10  # 测试用的日志级别（DEBUG）


# 测试同步函数
@log_wraps
def sync_function(x: int, y: int) -> int:
    """1.1 测试基本的同步函数"""
    time.sleep(TEST_SLEEP_TIME)  # 模拟耗时操作
    return x + y

@log_wraps()
def sync_function_no_result(x: int, y: int) -> int:
    """1.2 测试不记录结果的同步函数"""
    time.sleep(TEST_SLEEP_TIME)
    return x * y

@log_wraps(log_level=TEST_DEBUG_LOG_LEVEL, log_args=True, log_result=True)
def sync_function_with_error(x: int, y: int) -> float:
    """1.3 测试会抛出异常的同步函数"""
    time.sleep(TEST_SLEEP_TIME)
    return x / y  # 当y=0时会抛出异常

# 测试异步函数
@log_wraps(log_level=TEST_DEBUG_LOG_LEVEL, log_args=True, log_result=True)
async def async_function(x: int, y: int) -> int:
    """2.1 测试基本的异步函数"""
    await asyncio.sleep(TEST_SLEEP_TIME)  # 模拟异步耗时操作
    return x + y

@log_wraps
async def async_function_with_error(x: int, y: int) -> float:
    """2.2 测试会抛出异常的异步函数"""
    await asyncio.sleep(TEST_SLEEP_TIME)
    return x / y  # 当y=0时会抛出异常

@log_wraps()
def test_function(*args):
    """3.1 测试性能消耗较大的同步函数"""
    total = 0
    for i in range(1000000):
        total += i
    return total


@log_wraps()
async def async_test_function(x, y):
    """3.2 测试性能消耗较大的异步函数"""
    await asyncio.sleep(TEST_SLEEP_TIME)  # 模拟异步处理时间
    return x / y


# 主测试函数
async def main():
    """主测试函数 - 按序号组织所有测试用例"""
    print("====== 开始测试修复后的 log_wraps 装饰器 ======")

    # 1. 基础性能测试
    print("\n1. 基础性能测试:")
    result = test_function()
    print(f"1.1 测试性能同步函数结果: {result}")

    # 2. 异步基础函数测试
    print("\n2. 异步基础函数测试:")
    res2 = await async_test_function(10, 2)
    print(f"2.1 测试正常异步函数结果: {res2}")

    # 3. 异常处理测试
    print("\n3. 异常处理测试:")
    try:
        await async_test_function(10, 0)
    except ZeroDivisionError:
        print("3.1 异步函数异常测试: 成功捕获除零错误")

    # 4. 同步函数详细测试
    print("\n4. 同步函数详细测试:")
    try:
        # 测试正常同步函数
        result1 = sync_function(5, 3)
        print(f"4.1 基本同步函数结果: {result1}")
        
        # 测试不记录结果的同步函数
        result2 = sync_function_no_result(5, 3)
        print(f"4.2 不记录结果同步函数结果: {result2}")
        
        # 测试同步函数异常 - 除零
        try:
            sync_function_with_error(10, 0)
        except ZeroDivisionError:
            print("4.3 同步函数异常测试: 成功捕获除零错误")
            
    except Exception as e:
        print(f"同步函数测试失败: {e}")

    # 5. 异步函数详细测试
    print("\n5. 异步函数详细测试:")
    try:
        # 测试正常异步函数
        result4 = await async_function(7, 4)
        print(f"5.1 基本异步函数结果: {result4}")

        # 测试异步函数异常 - 除零
        try:
            await async_function_with_error(15, 0)
        except ZeroDivisionError:
            print("5.2 异步函数异常测试: 成功捕获除零错误")

    except Exception as e:
        print(f"异步函数测试失败: {e}")

    print("\n====== 测试完成 ======")


if __name__ == "__main__":
    asyncio.run(main())