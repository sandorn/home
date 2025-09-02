# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 11:38:00
LastEditTime : 2025-09-01 11:40:11
FilePath     : /CODE/test/test_timer_wraps.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import time

from xt_wraps.timer import timer_wraps


# 测试同步函数
@timer_wraps()
def sync_test_function():
    """测试同步函数的计时装饰器"""
    time.sleep(0.09)  # 模拟一些处理时间
    return "同步函数执行完成"

# 测试异步函数
@timer_wraps
async def async_test_function():
    """测试异步函数的计时装饰器"""
    await asyncio.sleep(0.081)  # 模拟异步处理时间
    return "异步函数执行完成"

# 测试带参数的同步函数
@timer_wraps()
def sync_test_with_params(a, b):
    """测试带参数的同步函数计时"""
    time.sleep(0.15)
    return a + b

# 测试带参数的异步函数
@timer_wraps
async def async_test_with_params(a, b):
    """测试带参数的异步函数计时"""
    await asyncio.sleep(0.10)
    return a * b

# 测试会抛出异常的同步函数
@timer_wraps()
def sync_test_with_exception():
    """测试抛出异常的同步函数计时"""
    time.sleep(0.14)
    raise ValueError("测试异常")

# 测试会抛出异常的异步函数
@timer_wraps
async def async_test_with_exception():
    """测试抛出异常的异步函数计时"""
    await asyncio.sleep(0.11)
    raise ValueError("测试异步异常")
    return "异步异常函数执行完成"

async def main():
    print("===== 测试timer_wraps装饰器 =====")
    
    # 测试同步函数
    print("\n1. 测试同步函数:")
    result = sync_test_function()
    print(f"结果: {result}")
    
    # 测试异步函数
    print("\n2. 测试异步函数:")
    result = await async_test_function()
    print(f"结果: {result}")
    
    # 测试带参数的同步函数
    print("\n3. 测试带参数的同步函数:")
    result = sync_test_with_params(10, 20)
    print(f"结果: {result}")
    
    # 测试带参数的异步函数
    print("\n4. 测试带参数的异步函数:")
    result = await async_test_with_params(10, 20)
    print(f"结果: {result}")
    
    # 测试会抛出异常的同步函数
    print("\n5. 测试抛出异常的同步函数:")
    try:
        sync_test_with_exception()
    except ValueError as e:
        print(f"捕获到异常: {e}")
    
    # 测试会抛出异常的异步函数
    print("\n6. 测试抛出异常的异步函数:")
    try:
        res =  await async_test_with_exception()
        print(res)
    except ValueError as e:
        print(f"捕获到异常: {e}")

if __name__ == "__main__":
    asyncio.run(main())