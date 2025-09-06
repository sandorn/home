# !/usr/bin/env python
"""
测试retry_wraps装饰器功能 - 验证同步/异步函数的重试机制

开发工具: VS Code
作者: Trae AI
FilePath: d:/CODE/xjLib/xt_wraps/test/test_retry_wraps.py
LastEditTime: 2025-09-06 09:25:00
"""

import asyncio

from xt_wraps.retry import retry_wraps


# 基础成功函数测试
@retry_wraps()
def basic_sync_success():
    """1.1 基础成功的同步函数"""
    print("基础同步函数执行成功")
    return "同步成功结果"


@retry_wraps()
async def basic_async_success():
    """1.2 基础成功的异步函数"""
    print("基础异步函数执行成功")
    return "异步成功结果"


# 重试后成功的函数测试
@retry_wraps(max_attempts=4)
def retry_sync_success():
    """2.1 重试后成功的同步函数（前两次失败，第三次成功）"""
    # 记录尝试次数的闭包变量
    if not hasattr(retry_sync_success, "attempts"):
        retry_sync_success.attempts = 0
    retry_sync_success.attempts += 1
    print(f"同步函数尝试第 {retry_sync_success.attempts} 次")
    if retry_sync_success.attempts < 3:
        raise ValueError(f"故意失败第 {retry_sync_success.attempts} 次")
    return "同步函数最终成功"


@retry_wraps(max_attempts=4)
async def retry_async_success():
    """2.2 重试后成功的异步函数（前两次失败，第三次成功）"""
    # 记录尝试次数的闭包变量
    if not hasattr(retry_async_success, "attempts"):
        retry_async_success.attempts = 0
    retry_async_success.attempts += 1
    print(f"异步函数尝试第 {retry_async_success.attempts} 次")
    if retry_async_success.attempts < 3:
        raise ValueError(f"故意失败第 {retry_async_success.attempts} 次")
    return "异步函数最终成功"


# 始终失败的函数测试
@retry_wraps(max_attempts=2)
def always_fail_sync():
    """3.1 始终失败的同步函数（达到最大尝试次数后失败）"""
    print("同步函数执行失败")
    raise RuntimeError("同步函数始终失败")


@retry_wraps(max_attempts=2)
async def always_fail_async():
    """3.2 始终失败的异步函数（达到最大尝试次数后失败）"""
    print("异步函数执行失败")
    raise RuntimeError("异步函数始终失败")


# 异常类型筛选测试
@retry_wraps
def exception_filter_func(x, y):
    """4.1 异常类型筛选（对某些异常不重试）"""
    print(f"计算 {x} / {y}")
    if y == 0:
        raise ZeroDivisionError("除数不能为零")  # 不重试的异常
    if y == 1:
        raise ValueError("y不能为1")  # 重试的异常
    return x / y


# 默认返回值测试
@retry_wraps(default_return="999")
def default_sync_no_retry():
    """5.1 同步函数不重试默认返回值"""
    raise ValueError("测试异常")


@retry_wraps(default_return="888", max_attempts=3)
def default_sync_retry():
    """5.2 同步函数重试后默认返回值"""
    raise TimeoutError("超时错误")


@retry_wraps(default_return="777")
async def default_async_no_retry():
    """5.3 异步函数不重试默认返回值"""
    raise ValueError("异步测试异常")


@retry_wraps(default_return="666", max_attempts=3)
async def default_async_retry():
    """5.4 异步函数重试后默认返回值"""
    raise TimeoutError("异步超时错误")


async def run_all_tests():
    """主测试函数 - 按序号组织所有测试用例"""
    print("====== 开始测试 retry_wraps 装饰器 ======")
    
    # 1. 基础成功函数测试
    print("\n1. 基础成功函数测试:")
    sync_result = basic_sync_success()
    print(f"1.1 同步函数结果: {sync_result}")
    
    async_result = await basic_async_success()
    print(f"1.2 异步函数结果: {async_result}")
    
    # 2. 重试后成功的函数测试
    print("\n2. 重试后成功的函数测试:")
    sync_retry_result = retry_sync_success()
    print(f"2.1 同步函数重试后结果: {sync_retry_result}")
    
    async_retry_result = await retry_async_success()
    print(f"2.2 异步函数重试后结果: {async_retry_result}")
    
    # 3. 始终失败的函数测试 - 使用try-except捕获预期失败
    print("\n3. 始终失败的函数测试:")
    try:
        always_fail_sync()
    except Exception as e:
        print(f"3.1 同步函数预期失败: {type(e).__name__}")
    
    try:
        await always_fail_async()
    except Exception as e:
        print(f"3.2 异步函数预期失败: {type(e).__name__}")
    
    # 4. 异常类型筛选测试
    print("\n4. 异常类型筛选测试:")
    try:
        exception_filter_func(10, 0)  # 不重试的异常
    except Exception as e:
        print(f"4.1 除零异常(不重试): {type(e).__name__}")
    
    try:
        exception_filter_func(10, 1)  # 重试的异常
    except Exception as e:
        print(f"4.2 ValueError(重试后): {type(e).__name__}")
    
    # 正常情况不应抛出异常
    normal_result = exception_filter_func(10, 2)
    print(f"4.3 正常计算结果: {normal_result}")
    
    # 5. 默认返回值测试
    print("\n5. 默认返回值测试:")
    print(f"5.1 同步函数不重试默认值: {default_sync_no_retry()}")
    print(f"5.2 同步函数重试后默认值: {default_sync_retry()}")
    print(f"5.3 异步函数不重试默认值: {await default_async_no_retry()}")
    print(f"5.4 异步函数重试后默认值: {await default_async_retry()}")
    
    print("\n====== 测试完成 ======")


# 运行主测试函数
if __name__ == "__main__":
    asyncio.run(run_all_tests())
