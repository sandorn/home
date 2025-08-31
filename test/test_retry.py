# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-08-31 12:45:45
LastEditTime : 2025-08-31 12:48:11
FilePath     : /CODE/test/test_retry.py
Github       : https://github.com/sandorn/home
==============================================================
"""
import asyncio

from xt_wraps.retry import retry_deco


# 测试同步函数 - 应该重试3次后失败
@retry_deco(max_attempts=3)
def test_sync_fail():
    print("调用同步失败函数...")
    raise RuntimeError("同步函数失败")
    return "这个不会返回"

# 测试同步函数 - 第2次成功
counter = 0
@retry_deco(max_attempts=3)
def test_sync_success_after_retry():
    global counter
    counter += 1
    print(f"调用同步函数 - 尝试 #{counter}")
    if counter < 2:
        raise RuntimeError(f"第{counter}次尝试失败")
    return f"第{counter}次尝试成功"

# 测试异步函数 - 应该重试3次后失败
@retry_deco(max_attempts=3)
async def test_async_fail():
    print("调用异步失败函数...")
    await asyncio.sleep(0.1)
    raise RuntimeError("异步函数失败")
    return "这个不会返回"

# 测试异步函数 - 第2次成功
async_counter = 0
@retry_deco(max_attempts=3)
async def test_async_success_after_retry():
    global async_counter
    async_counter += 1
    print(f"调用异步函数 - 尝试 #{async_counter}")
    await asyncio.sleep(0.1)
    if async_counter < 2:
        raise RuntimeError(f"第{async_counter}次尝试失败")
    return f"第{async_counter}次尝试成功"

async def main():
    print("=== 开始测试 retry_deco 装饰器 ===")
    
    # 测试同步函数 - 预期失败
    try:
        print("\n测试同步函数(预期失败):")
        result = test_sync_fail()
        print(f"意外成功: {result}")
    except Exception as e:
        print(f"预期的异常: {type(e).__name__}: {e}")
    
    # 测试同步函数 - 预期重试后成功
    try:
        print("\n测试同步函数(预期重试后成功):")
        result = test_sync_success_after_retry()
        print(f"成功结果: {result}")
    except Exception as e:
        print(f"意外的异常: {type(e).__name__}: {e}")
    
    # 测试异步函数 - 预期失败
    try:
        print("\n测试异步函数(预期失败):")
        result = await test_async_fail()
        print(f"意外成功: {result}")
    except Exception as e:
        print(f"预期的异常: {type(e).__name__}: {e}")
    
    # 测试异步函数 - 预期重试后成功
    try:
        print("\n测试异步函数(预期重试后成功):")
        result = await test_async_success_after_retry()
        print(f"成功结果: {result}")
    except Exception as e:
        print(f"意外的异常: {type(e).__name__}: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    asyncio.run(main())