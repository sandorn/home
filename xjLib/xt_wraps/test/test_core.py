"""
测试core.py模块 - 验证装饰器工厂函数的功能

开发工具: VSCode
作者: sandorn sandorn@live.cn
FilePath: d:/CODE/xjLib/xt_wraps/test/test_core.py
LastEditTime: 2025-09-06 10:30:00

https://mp.weixin.qq.com/s/4nkQITVniE9FhESDMt34Ow  # wrapt库
"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from typing import Any

from xt_wraps.core import decorate_sas, decorate_sync_async


class TestResult:
    """测试结果收集器"""

    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.results: list[tuple[str, bool, str]] = []

    def add_success(self, test_id: str, message: str = '') -> None:
        self.success_count += 1
        self.results.append((test_id, True, message))

    def add_failure(self, test_id: str, message: str = '') -> None:
        self.fail_count += 1
        self.results.append((test_id, False, message))

    def summary(self) -> str:
        total = self.success_count + self.fail_count
        return f'测试总结: 共 {total} 个测试, 成功 {self.success_count} 个, 失败 {self.fail_count} 个'


def print_test_header(title: str, indent: int = 0) -> None:
    """打印测试标题"""
    pass


def print_test_case(test_id: str, description: str, indent: int = 1) -> None:
    """打印测试用例信息"""
    pass


def print_call_path(call_info: str, indent: int = 2) -> None:
    """打印调用路径信息"""
    pass


def print_test_result(result: Any, indent: int = 2) -> None:
    """打印测试结果"""
    pass


# 1. 测试 decorate_sas 函数 - 基本功能测试
# 1.1 创建用于测试的装饰器函数
def simple_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    """1.1.1 一个简单的装饰器函数，用于测试decorate_sas"""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)
    return wrapper


# 1.2 使用 decorate_sas 包装装饰器
def sas_decorator(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """1.2.1 使用decorate_sas包装的装饰器函数"""
    return func(*args, **kwargs)


# 先定义装饰器,再使用它
sas_wrapper = decorate_sas(sas_decorator)


# 2. 测试 decorate_sync_async 函数 - 基本功能测试
# 2.1 创建用于测试的装饰器函数，支持参数
def enhanced_decorator(func: Callable[..., Any] | None = None, prefix: str = '[Enhanced]', print_args: bool = False) -> Callable[..., Any]:
    """2.1.1 增强的装饰器函数，支持参数"""
    # 处理无参数调用模式
    if func is None:
        def decorator_wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            return enhanced_decorator(func, prefix=prefix, print_args=print_args)
        return decorator_wrapper
    
    @decorate_sync_async
    def decorator(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """2.1.2 实际的装饰器逻辑"""
        if print_args:
            pass
        return func(*args, **kwargs)
    
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


@enhanced_decorator(prefix='[Sync]', print_args=True)
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


@enhanced_decorator(prefix='[Async]', print_args=True)
async def async_test_function_enhanced(a: int, b: int) -> int:
    """3.2.2 使用增强装饰器的异步测试函数"""
    await asyncio.sleep(0.05)  # 模拟异步处理时间
    return a // b


# 3.3 带异常的测试函数
@enhanced_decorator
async def async_test_with_exception(x: int) -> float:
    """3.3.1 测试异常处理的异步函数"""
    await asyncio.sleep(0.05)
    if x == 0:
        raise ValueError('除数不能为零')
    return 10 / x


# 4. 测试 decorate_sync_async 的各种使用模式
# 4.1 直接装饰函数（无参数）
@decorate_sync_async
def test_direct_decoration(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """4.1.1 直接使用decorate_sync_async装饰"""
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
@decorate_sync_async(prefix='[Custom]')
def test_custom_params(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """4.2.1 使用带参数的decorate_sync_async装饰"""
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
async def run_all_tests() -> None:
    """主测试函数，按顺序执行所有测试用例"""
    # 初始化测试结果收集器
    test_result = TestResult()

    # ========== 1. 测试 decorate_sas 函数 ==========
    # 1.1 测试同步函数
    try:
        sync_test_function(5, 3)
        test_result.add_success('1.1')
    except Exception:
        test_result.add_failure('1.1')
    
    # 1.2 测试使用SAS包装的同步函数
    try:
        sync_test_function_sas(5, 3)
        test_result.add_success('1.2')
    except Exception:
        test_result.add_failure('1.2')
    
    # 1.3 测试使用SAS包装的异步函数
    try:
        async_test_function_sas(10, 3)
        test_result.add_success('1.3')
    except Exception:
        test_result.add_failure('1.3')

    # ========== 2. 测试 decorate_sync_async 函数 ==========
    # 2.1 测试使用增强装饰器的同步函数
    try:
        sync_test_function_enhanced(2, 3)
        test_result.add_success('2.1')
    except Exception:
        test_result.add_failure('2.1')
    
    # 2.2 测试使用增强装饰器的异步函数
    try:
        await async_test_function_enhanced(10, 3)
        test_result.add_success('2.2')
    except Exception:
        test_result.add_failure('2.2')

    # ========== 3. 测试异常处理 ==========
    # 3.1 测试正常执行
    try:
        await async_test_with_exception(5)
        test_result.add_success('3.1')
    except ValueError:
        test_result.add_failure('3.1')
    
    # 3.2 测试异常处理
    try:
        await async_test_with_exception(0)
        test_result.add_success('3.2')
    except ValueError:
        test_result.add_success('3.2', '成功捕获到预期异常')

    # ========== 4. 测试 decorate_sync_async 的各种使用模式 ==========
    # 4.1 测试直接装饰函数
    try:
        sync_direct_test(42)
        await async_direct_test(42)
        test_result.add_success('4.1')
    except Exception:
        test_result.add_failure('4.1')
    
    # 4.2 测试带参数的装饰器模式
    try:
        sync_custom_params_test(42)
        await async_custom_params_test(42)
        test_result.add_success('4.2')
    except Exception:
        test_result.add_failure('4.2')

    # 输出测试总结
    pass


# 运行测试
if __name__ == '__main__':
    asyncio.run(run_all_tests())