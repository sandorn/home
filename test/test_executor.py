# !/usr/bin/env python
"""
==============================================================
Description  : 执行器装饰器测试文件
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 11:46:00
LastEditTime : 2025-09-01 11:46:30
FilePath     : /CODE/test/test_executor.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from xt_wraps.executor import executor_wraps


# 测试同步函数 - 正常执行
@executor_wraps
def sync_test_function():
    """测试同步函数的执行器装饰器"""
    print(f"同步函数在 {time.strftime('%H:%M:%S')} 开始执行")
    time.sleep(1)  # 模拟耗时操作
    print(f"同步函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "同步函数执行结果"

# 测试同步函数 - 带参数
@executor_wraps
def sync_test_with_params(a, b):
    """测试带参数的同步函数"""
    print(f"带参数的同步函数: {a} + {b}")
    time.sleep(0.5)
    return a + b

# 测试同步函数 - 后台执行
@executor_wraps(background=True)
def sync_background_function():
    """测试同步函数的后台执行"""
    print(f"后台同步函数在 {time.strftime('%H:%M:%S')} 开始执行")
    time.sleep(2)  # 模拟较长时间操作
    print(f"后台同步函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "后台同步函数执行结果"

# 测试同步函数 - 自定义执行器
custom_executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="CustomExecutor")
@executor_wraps(executor=custom_executor)
def sync_custom_executor():
    """测试使用自定义执行器的同步函数"""
    print(f"自定义执行器函数在 {time.strftime('%H:%M:%S')} 开始执行")
    time.sleep(0.8)
    print(f"自定义执行器函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "自定义执行器函数结果"

# 测试同步函数 - 会抛出异常
@executor_wraps
def sync_test_with_exception():
    """测试会抛出异常的同步函数"""
    print("测试同步函数异常")
    time.sleep(0.2)
    raise ValueError("同步函数测试异常")

# 测试异步函数 - 正常执行
@executor_wraps  # 测试别名
async def async_test_function():
    """测试异步函数的执行器装饰器"""
    print(f"异步函数在 {time.strftime('%H:%M:%S')} 开始执行")
    await asyncio.sleep(1)  # 模拟异步耗时操作
    print(f"异步函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "异步函数执行结果"

# 测试异步函数 - 带参数
@executor_wraps
async def async_test_with_params(a, b):
    """测试带参数的异步函数"""
    print(f"带参数的异步函数: {a} * {b}")
    await asyncio.sleep(0.5)
    return a * b

# 测试异步函数 - 后台执行
@executor_wraps(background=True)
async def async_background_function():
    """测试异步函数的后台执行"""
    print(f"后台异步函数在 {time.strftime('%H:%M:%S')} 开始执行")
    await asyncio.sleep(2)  # 模拟较长时间操作
    print(f"后台异步函数在 {time.strftime('%H:%M:%S')} 执行完成")
    return "后台异步函数执行结果"

# 测试异步函数 - 会抛出异常
@executor_wraps
async def async_test_with_exception():
    """测试会抛出异常的异步函数"""
    print("测试异步函数异常")
    await asyncio.sleep(0.2)
    raise ValueError("异步函数测试异常")

async def main():
    print("===== 测试run_on_executor装饰器 =====")
    
    # 1. 测试同步函数的正常执行
    print("\n1. 测试同步函数的正常执行:")
    result = await sync_test_function()
    print(f"同步函数结果: {result}")
    
    # 2. 测试同步函数带参数
    print("\n2. 测试同步函数带参数:")
    result = await sync_test_with_params(10, 20)
    print(f"带参数同步函数结果: {result}")
    
    # 3. 测试同步函数的后台执行
    print("\n3. 测试同步函数的后台执行:")
    task = sync_background_function()
    print("后台任务已提交，无需等待结果继续执行")
    # 等待一段时间，确保能看到后台任务的输出
    await asyncio.sleep(0.5)
    
    # 4. 测试使用自定义执行器的同步函数
    print("\n4. 测试使用自定义执行器的同步函数:")
    result = await sync_custom_executor()
    print(f"自定义执行器函数结果: {result}")
    
    # 5. 测试同步函数异常处理
    print("\n5. 测试同步函数异常处理:")
    try:
        await sync_test_with_exception()
    except ValueError as e:
        print(f"成功捕获同步函数异常: {e}")
    
    # 6. 测试异步函数的正常执行
    print("\n6. 测试异步函数的正常执行 (使用别名executor):")
    result = await async_test_function()
    print(f"异步函数结果: {result}")
    
    # 7. 测试异步函数带参数
    print("\n7. 测试异步函数带参数:")
    result = await async_test_with_params(10, 20)
    print(f"带参数异步函数结果: {result}")
    
    # 8. 测试异步函数的后台执行
    print("\n8. 测试异步函数的后台执行:")
    task = await async_background_function()
    print("后台任务已提交，无需等待结果继续执行")
    # 等待一段时间，确保能看到后台任务的输出
    await asyncio.sleep(0.5)
    print(f"async_background_function {task}")
    
    # 9. 测试异步函数异常处理
    print("\n9. 测试异步函数异常处理:")
    try:
        await async_test_with_exception()
    except ValueError as e:
        print(f"成功捕获异步函数异常: {e}")
    
    # 等待所有后台任务完成
    print("\n等待所有后台任务完成...")
    await asyncio.sleep(2)
    print("\n所有测试完成!")

if __name__ == "__main__":
    asyncio.run(main())