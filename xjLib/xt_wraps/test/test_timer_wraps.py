"""
测试timer_wraps装饰器功能 - 验证计时器装饰器的正确性

开发工具: VS Code
作者: sandorn sandorn@live.cn
FilePath: d:/CODE/xjlib/xt_wraps/test/test_timer_wraps.py
LastEditTime: 2025-09-06 10:00:00
"""

from __future__ import annotations

import asyncio
import contextlib
import time

from xt_wraps.timer import timer_wraps


# 1. 基本功能测试 - 连续序号便于查找
@timer_wraps()
def sync_test_function():
    """1.1 测试同步函数的计时装饰器"""
    time.sleep(0.09)  # 模拟一些处理时间
    return '同步函数执行完成'


@timer_wraps
async def async_test_function():
    """1.2 测试异步函数的计时装饰器"""
    await asyncio.sleep(0.081)  # 模拟异步处理时间
    return '异步函数执行完成'


# 2. 参数测试 - 连续序号便于查找
@timer_wraps()
def sync_test_with_params(a, b):
    """2.1 测试带参数的同步函数计时"""
    time.sleep(0.15)  # 模拟处理时间
    return a + b


@timer_wraps
async def async_test_with_params(a, b):
    """2.2 测试带参数的异步函数计时"""
    await asyncio.sleep(0.10)  # 模拟处理时间
    return a * b


# 3. 异常处理测试 - 连续序号便于查找
@timer_wraps()
def sync_test_with_exception():
    """3.1 测试抛出异常的同步函数计时"""
    time.sleep(0.14)  # 模拟处理时间
    raise ValueError('测试异常')


@timer_wraps
async def async_test_with_exception():
    """3.2 测试抛出异常的异步函数计时"""
    await asyncio.sleep(0.11)  # 模拟处理时间
    raise ValueError('测试异步异常')


# 4. 计算密集型测试 - 连续序号便于查找
@timer_wraps
async def async_test_compute_intensive():
    """4.1 测试计算密集型异步函数的计时"""
    await asyncio.sleep(0.11)  # 模拟处理时间
    total = 0
    for i in range(1000000):
        total += i
    return total


# 5. 多装饰器组合测试 - 连续序号便于查找
async def test_multiple_decorators():
    """5. 测试timer_wraps与其他装饰器的组合使用"""
    from xt_wraps import log_wraps, retry_wraps

    await asyncio.sleep(0.11)  # 模拟处理时间

    @timer_wraps
    @log_wraps
    def test_function():
        """5.1 同步函数多装饰器组合测试"""
        total = 0
        for i in range(1000000):
            total += i
        return total

    @timer_wraps
    @log_wraps
    @retry_wraps(default_return=-999)
    async def async_test_function_with_retry(x, y):
        """5.2 异步函数多装饰器组合测试(包含重试)"""
        await asyncio.sleep(0.20)  # 模拟异步处理时间
        return x / y

    # 执行测试
    test_function()

    await async_test_function_with_retry(10, 2)

    await async_test_function_with_retry(10, 0)


# 主测试函数 - 按序号组织测试用例
async def run_all_tests():
    """主测试函数，按顺序执行所有测试用例"""

    # ========== 1. 基本功能测试 ==========
    # 1.1 测试同步函数
    sync_test_function()

    # 1.2 测试异步函数
    await async_test_function()

    # ========== 2. 参数测试 ==========
    # 2.1 测试带参数的同步函数
    sync_test_with_params(10, 20)

    # 2.2 测试带参数的异步函数
    await async_test_with_params(10, 20)

    # ========== 3. 异常处理测试 ==========
    # 3.1 测试抛出异常的同步函数
    with contextlib.suppress(ValueError):
        sync_test_with_exception()

    # 3.2 测试抛出异常的异步函数
    with contextlib.suppress(ValueError):
        await async_test_with_exception()

    # ========== 4. 计算密集型测试 ==========
    # 4.1 测试计算密集型异步函数的计时
    await async_test_compute_intensive()


# 运行所有测试
if __name__ == '__main__':
    import asyncio

    async def main_tests():
        await run_all_tests()
        await test_multiple_decorators()

    asyncio.run(main_tests())
