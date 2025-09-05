# !/usr/bin/env python
"""
测试修复后的log_wraps装饰器功能 - 确保异步函数返回值正确处理
"""

import asyncio
import time

from xt_wraps.log import log_wraps


# 测试同步函数
@log_wraps
def sync_function(x: int, y: int) -> int:
    """测试基本的同步函数"""
    time.sleep(0.1)  # 模拟耗时操作
    return x + y

@log_wraps()
def sync_function_no_result(x: int, y: int) -> int:
    """测试不记录结果的同步函数"""
    time.sleep(0.1)
    return x * y

@log_wraps(log_level=10, log_args=True, log_result=True)
def sync_function_with_error(x: int, y: int) -> float:
    """测试会抛出异常的同步函数"""
    time.sleep(0.1)
    return x / y  # 当y=0时会抛出异常

# 测试异步函数
@log_wraps(log_level=10, log_args=True, log_result=True)
async def async_function(x: int, y: int) -> int:
    """测试基本的异步函数"""
    await asyncio.sleep(0.1)  # 模拟异步耗时操作
    return x + y

@log_wraps
async def async_function_with_error(x: int, y: int) -> float:
    """测试会抛出异常的异步函数"""
    await asyncio.sleep(0.1)
    return x / y  # 当y=0时会抛出异常

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


# 主测试函数
async def main():
    print("====== 开始测试修复后的 log_wraps 装饰器 ======")
    result = test_function()
    print(f"1. 测试同步函数结果: {result}")
    res2 = await async_test_function(10, 2)
    print(f"2. 测试异步函数结果: {res2}")
    result = await async_test_function(10, 0)
    print(f"3. 测试异步函数结果: {result}")

    print("\n1. 测试同步函数:")
    try:
        # 测试正常同步函数
        result1 = sync_function(5, 3)
        print(f"sync_function 结果: {result1}")
        
        # 测试不记录结果的同步函数
        result2 = sync_function_no_result(5, 3)
        print(f"sync_function_no_result 结果: {result2}")
        
        # 测试同步函数异常 - 除零
        try:
            sync_function_with_error(10, 0)
        except ZeroDivisionError:
            print("sync_function_with_error: 预期的除零错误")
            
    except Exception as e:
        print(f"同步函数测试失败: {e}")
    
    print("\n2. 测试异步函数:")
    try:
        # 测试正常异步函数
        result4 = await async_function(7, 4)
        print(f"async_function 结果: {result4}")
        
        # 测试异步函数异常 - 除零
        try:
            await async_function_with_error(15, 0)
        except ZeroDivisionError:
            print("async_function_with_error: 预期的除零错误")
            
    except Exception as e:
        print(f"异步函数测试失败: {e}")
    
    print("\n====== 测试完成 ======")

if __name__ == "__main__":
    asyncio.run(main())