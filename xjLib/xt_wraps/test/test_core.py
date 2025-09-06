"""
测试core.py模块 - 验证装饰器工厂函数的功能

开发工具: VS Code
作者: sandorn sandorn@live.cn
FilePath: d:/CODE/xjLib/xt_wraps/test/test_core.py
LastEditTime: 2025-09-06 10:30:00
"""

import asyncio
import time
from typing import Any, Callable

from xt_wraps.core import decorate_sas, decorate_sync_async


# 1. 测试 decorate_sas 函数 - 基本功能测试
# 1.1 创建用于测试的装饰器函数
def simple_decorator(func: Callable) -> Callable:
    """1.1.1 一个简单的装饰器函数，用于测试decorate_sas"""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"简单装饰器: 调用函数 {func.__name__}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"简单装饰器: 函数 {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    return wrapper


# 1.2 使用 decorate_sas 包装装饰器
def sas_decorator(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """1.2.1 使用decorate_sas包装的装饰器函数"""
    print(f"SAS装饰器: 调用函数 {func.__name__}")
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"SAS装饰器: 函数 {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
    return result

# 先定义装饰器，再使用它
sas_wrapper = decorate_sas(sas_decorator)


# 2. 测试 decorate_sync_async 函数 - 基本功能测试
# 2.1 创建用于测试的装饰器函数，支持参数
def enhanced_decorator(
    func: Callable = None,
    prefix: str = "[Enhanced]",
    print_args: bool = False
) -> Callable:
    """2.1.1 增强的装饰器函数，支持参数"""
    # 处理无参数调用模式
    if func is None:
        def decorator_wrapper(func: Callable) -> Callable:
            return enhanced_decorator(func, prefix=prefix, print_args=print_args)
        return decorator_wrapper
    
    @decorate_sync_async
    def decorator(func: Callable, *args: Any, **kwargs: Any) -> Any:
        """2.1.2 实际的装饰器逻辑"""
        print(f"{prefix} 调用函数 {func.__name__}")
        if print_args:
            print(f"{prefix} 参数: args={args}, kwargs={kwargs}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{prefix} 函数 {func.__name__} 执行时间: {end_time - start_time:.4f}秒")
        return result
    
    return decorator(func)


# 3. 定义测试函数
# 3.1 同步测试函数
@simple_decorator
def sync_test_function(a: int, b: int) -> int:
    """3.1.1 同步测试函数"""
    time.sleep(0.05)  # 模拟处理时间
    return a + b


@sas_wrapper
def sync_test_function_sas(a: int, b: int) -> int:
    """3.1.2 使用SAS包装的同步测试函数"""
    time.sleep(0.05)  # 模拟处理时间
    return a * b


@enhanced_decorator(prefix="[Sync]", print_args=True)
def sync_test_function_enhanced(a: int, b: int) -> int:
    """3.1.3 使用增强装饰器的同步测试函数"""
    time.sleep(0.05)  # 模拟处理时间
    return a ** b


# 3.2 异步测试函数
@sas_wrapper
def async_test_function_sas(a: int, b: int) -> int:
    """3.2.1 使用SAS包装的异步测试函数"""
    time.sleep(0.05)  # 模拟处理时间
    return a - b


@enhanced_decorator(prefix="[Async]", print_args=True)
async def async_test_function_enhanced(a: int, b: int) -> int:
    """3.2.2 使用增强装饰器的异步测试函数"""
    await asyncio.sleep(0.05)  # 模拟异步处理时间
    return a // b


# 3.3 带异常的测试函数
@enhanced_decorator
async def async_test_with_exception(x: int) -> None:
    """3.3.1 测试异常处理的异步函数"""
    await asyncio.sleep(0.05)
    if x == 0:
        raise ValueError("除数不能为零")
    return 10 / x


# 4. 测试 decorate_sync_async 的各种使用模式
# 4.1 直接装饰函数（无参数）
@decorate_sync_async
def test_direct_decoration(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """4.1.1 直接使用decorate_sync_async装饰"""
    print(f"直接装饰: 调用函数 {func.__name__}")
    return func(*args, **kwargs)


@test_direct_decoration
def sync_direct_test(a: int) -> int:
    """4.1.2 直接装饰的同步函数"""
    return a * 10


@test_direct_decoration
async def async_direct_test(a: int) -> int:
    """4.1.3 直接装饰的异步函数"""
    await asyncio.sleep(0.03)
    return a * 100


# 4.2 带参数的装饰器模式
@decorate_sync_async(prefix="[Custom]")
def test_custom_params(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """4.2.1 使用带参数的decorate_sync_async装饰"""
    prefix = kwargs.pop('prefix', '[Default]')
    print(f"{prefix} 自定义参数: 调用函数 {func.__name__}")
    return func(*args, **kwargs)


@test_custom_params
def sync_custom_params_test(a: int) -> int:
    """4.2.2 使用带参数装饰器的同步函数"""
    return a * 1000


@test_custom_params
async def async_custom_params_test(a: int) -> int:
    """4.2.3 使用带参数装饰器的异步函数"""
    await asyncio.sleep(0.03)
    return a * 10000


# 5. 主测试函数
async def run_all_tests():
    """主测试函数，按顺序执行所有测试用例"""
    print("===== 开始测试 core.py 装饰器工厂函数 ======")

    # ========== 1. 测试 decorate_sas 函数 ==========
    print("\n===== 1. 测试 decorate_sas 函数 ======")
    # 1.1 测试同步函数
    print("\n1.1 测试同步函数:")
    result1 = sync_test_function(5, 3)
    print(f"结果: {result1}")
    
    # 1.2 测试使用SAS包装的同步函数
    print("\n1.2 测试使用SAS包装的同步函数:")
    result2 = sync_test_function_sas(5, 3)
    print(f"结果: {result2}")
    
    # 1.3 测试使用SAS包装的异步函数
    print("\n1.3 测试使用SAS包装的异步函数:")
    result3 = async_test_function_sas(10, 3)
    print(f"结果: {result3}")

    # ========== 2. 测试 decorate_sync_async 函数 ==========
    print("\n===== 2. 测试 decorate_sync_async 函数 ======")
    # 2.1 测试使用增强装饰器的同步函数
    print("\n2.1 测试使用增强装饰器的同步函数:")
    result4 = sync_test_function_enhanced(2, 3)
    print(f"结果: {result4}")
    
    # 2.2 测试使用增强装饰器的异步函数
    print("\n2.2 测试使用增强装饰器的异步函数:")
    result5 = await async_test_function_enhanced(10, 3)
    print(f"结果: {result5}")

    # ========== 3. 测试异常处理 ==========
    print("\n===== 3. 测试异常处理 ======")
    # 3.1 测试正常执行
    print("\n3.1 测试正常执行:")
    try:
        result6 = await async_test_with_exception(5)
        print(f"结果: {result6}")
    except ValueError as e:
        print(f"捕获到异常: {e}")
    
    # 3.2 测试异常处理
    print("\n3.2 测试异常处理:")
    try:
        result7 = await async_test_with_exception(0)
        print(f"结果: {result7}")
    except ValueError as e:
        print(f"捕获到异常: {e}")

    # ========== 4. 测试 decorate_sync_async 的各种使用模式 ==========
    print("\n===== 4. 测试 decorate_sync_async 的各种使用模式 ======")
    # 4.1 测试直接装饰函数
    print("\n4.1 测试直接装饰函数:")
    result8 = sync_direct_test(42)
    print(f"同步结果: {result8}")
    
    result9 = await async_direct_test(42)
    print(f"异步结果: {result9}")
    
    # 4.2 测试带参数的装饰器模式
    print("\n4.2 测试带参数的装饰器模式:")
    result10 = sync_custom_params_test(42)
    print(f"同步结果: {result10}")
    
    result11 = await async_custom_params_test(42)
    print(f"异步结果: {result11}")

    print("\n===== 所有测试完成! =====")


# 运行测试
if __name__ == "__main__":
    asyncio.run(run_all_tests())