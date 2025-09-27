"""
测试 timer_wraps 装饰器
"""

from __future__ import annotations

import asyncio
import time
from contextlib import suppress

from xt_wraps.timer import TimerWrapt, timer_wraps


# ========== 1. 基本功能测试 ==========
# 1.1 测试同步函数的计时装饰器
@timer_wraps
def sync_test_function():
    """测试同步函数的计时装饰器"""
    time.sleep(0.09)  # 模拟一些处理时间
    return '同步函数执行完成'


# 1.2 测试异步函数的计时装饰器
@timer_wraps
async def async_test_function():
    """测试异步函数的计时装饰器"""
    await asyncio.sleep(0.081)  # 模拟异步处理时间
    return '异步函数执行完成'


# ========== 2. 参数测试 ==========
# 2.1 测试带参数的同步函数计时
@timer_wraps
def sync_test_with_params(a, b):
    """测试带参数的同步函数计时"""
    time.sleep(0.05)  # 模拟处理时间
    return a + b


# 2.2 测试带参数的异步函数计时
@timer_wraps
async def async_test_with_params(a, b):
    """测试带参数的异步函数计时"""
    await asyncio.sleep(0.05)  # 模拟处理时间
    return a * b


# ========== 3. 异常处理测试 ==========
# 3.1 测试抛出异常的同步函数计时
@timer_wraps
def sync_test_with_exception():
    """测试抛出异常的同步函数计时"""
    time.sleep(0.05)  # 模拟处理时间
    raise ValueError('测试异常')


# 3.2 测试抛出异常的异步函数计时
@timer_wraps
async def async_test_with_exception():
    """测试抛出异常的异步函数计时"""
    await asyncio.sleep(0.05)  # 模拟处理时间
    raise ValueError('测试异步异常')


# ========== 4. TimerWrapt 类测试 ==========
# 4.1 测试 TimerWrapt 作为装饰器使用
@TimerWrapt
def timer_wrapt_decorator_test():
    """测试 TimerWrapt 作为装饰器使用"""
    time.sleep(0.05)
    return 'TimerWrapt 装饰器测试完成'


# 4.2 测试 TimerWrapt 作为上下文管理器使用
def timer_wrapt_context_test():
    """测试 TimerWrapt 作为上下文管理器使用"""
    with TimerWrapt('上下文管理器测试'):
        time.sleep(0.05)


# 4.3 测试 TimerWrapt 上下文管理器异常处理
def timer_wrapt_context_exception_test():
    """测试 TimerWrapt 上下文管理器异常处理"""
    try:
        with TimerWrapt('异常处理测试'):
            time.sleep(0.05)
            raise ValueError('测试异常')
    except ValueError:
        pass  # 预期异常，捕获后继续


# 4.4 测试 TimerWrapt 无参调用
def timer_wrapt_no_param_test():
    """测试 TimerWrapt 无参调用"""
    with TimerWrapt():
        time.sleep(0.05)


# ========== 5. 多装饰器组合测试 ==========
def test_multiple_decorators():
    """测试timer_wraps与其他装饰器的组合使用"""
    # 注意：这里仅作示例，实际使用时需要确保其他装饰器存在
    pass


# ========== 6. 边界情况测试 ==========
# 6.1 测试快速执行的函数
@timer_wraps
def fast_function_test():
    """测试快速执行的函数"""
    return sum(range(10000))


# 6.2 测试长时间运行的函数
@timer_wraps
async def long_running_function_test():
    """测试长时间运行的函数"""
    await asyncio.sleep(0.1)
    return '长时间运行函数完成'


# ========== 主测试函数 ==========
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
    with suppress(ValueError):
        sync_test_with_exception()

    # 3.2 测试抛出异常的异步函数
    with suppress(ValueError):
        await async_test_with_exception()

    # ========== 4. TimerWrapt 类测试 ==========
    # 4.1 测试 TimerWrapt 作为装饰器使用
    timer_wrapt_decorator_test()

    # 4.2 测试 TimerWrapt 作为上下文管理器使用
    timer_wrapt_context_test()

    # 4.3 测试 TimerWrapt 上下文管理器异常处理
    timer_wrapt_context_exception_test()

    # 4.4 测试 TimerWrapt 无参调用
    timer_wrapt_no_param_test()

    # ========== 5. 多装饰器组合测试 ==========
    test_multiple_decorators()

    # ========== 6. 边界情况测试 ==========
    # 6.1 测试快速执行的函数
    fast_function_test()

    # 6.2 测试长时间运行的函数
    await long_running_function_test()


if __name__ == '__main__':
    asyncio.run(run_all_tests())