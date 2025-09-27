# !/usr/bin/env python3
"""
装饰器工具模块

整合了wrapper.py和deco.py的优点，提供灵活、高效、强壮的装饰器实现
"""

from __future__ import annotations

import asyncio
import contextlib
import functools
import random
import time
from collections.abc import Callable, Generator
from typing import Any, ParamSpec, TypeVar

from xt_wraps.log import mylog

# 类型定义
P = ParamSpec('P')
T = TypeVar('T')
ExceptionTypes = tuple[type[Exception], ...]


def _calculate_wait_time(min_wait: float, max_wait: float) -> float:
    """计算等待时间"""
    # 使用系统时间作为随机种子，避免密码学警告
    import time as time_module

    seed = int(time_module.time() * 1000) % 1000000
    local_random = random.Random(seed)  # noqa: S311

    return local_random.uniform(min_wait, max_wait)


def _get_random_value() -> float:
    """获取随机值"""
    # 使用系统时间作为随机种子，避免密码学警告
    import time as time_module

    seed = int(time_module.time() * 1000) % 1000000
    local_random = random.Random(seed)  # noqa: S311

    return local_random.random()


def _handle_retry_attempt(func_name: str, attempt: int, max_attempts: int, exception: Exception, wait_time: float, log_retry: bool, is_async: bool) -> Generator[Any]:
    """处理重试尝试"""
    if log_retry:
        mylog.warning(f'函数 {func_name} 第 {attempt + 1} 次执行失败，{wait_time:.2f}秒后重试: {exception}')

    # 等待
    if is_async:
        yield from asyncio.sleep(wait_time)
    else:
        time.sleep(wait_time)
        yield


def _handle_final_failure(func_name: str, max_attempts: int, exception: Exception, log_retry: bool) -> None:
    """处理最终失败"""
    if log_retry:
        mylog.error(f'函数 {func_name} 重试 {max_attempts} 次后仍然失败: {exception}')
    raise exception


def _create_async_wrapper(func: Callable, before_hook: Callable | None, after_hook: Callable | None, exception_hook: Callable | None) -> Callable:
    """创建异步包装器"""

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        """异步包装器"""
        try:
            # 执行前钩子
            if before_hook:
                before_hook(func, *args, **kwargs)

            # 执行函数
            result = await func(*args, **kwargs)

            # 执行后钩子
            if after_hook:
                after_hook(func, result, *args, **kwargs)

            return result
        except Exception as e:
            # 异常处理钩子
            if exception_hook:
                exception_hook(func, e, *args, **kwargs)
            raise

    return async_wrapper


def _create_sync_wrapper(func: Callable, before_hook: Callable | None, after_hook: Callable | None, exception_hook: Callable | None) -> Callable:
    """创建同步包装器"""

    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
        """同步包装器"""
        try:
            # 执行前钩子
            if before_hook:
                before_hook(func, *args, **kwargs)

            # 执行函数
            result = func(*args, **kwargs)

            # 执行后钩子
            if after_hook:
                after_hook(func, result, *args, **kwargs)

            return result
        except Exception as e:
            # 异常处理钩子
            if exception_hook:
                exception_hook(func, e, *args, **kwargs)
            raise

    return sync_wrapper


def universal_decorator(
    before_hook: Callable | None = None,
    after_hook: Callable | None = None,
    exception_hook: Callable | None = None,
) -> Callable:
    """
    通用装饰器工厂函数，支持同步和异步函数

    Args:
        before_hook: 函数执行前的钩子函数
        after_hook: 函数执行后的钩子函数
        exception_hook: 异常处理钩子函数

    Returns:
        通用装饰器
    """

    def decorator(func: Callable) -> Callable:
        """通用装饰器"""
        is_async = asyncio.iscoroutinefunction(func)

        if is_async:
            return _create_async_wrapper(func, before_hook, after_hook, exception_hook)
        return _create_sync_wrapper(func, before_hook, after_hook, exception_hook)

    return decorator


# 计时装饰器
def timer_wrapper(func: Callable) -> Callable:
    """
    计时装饰器，记录函数执行时间

    Args:
        func: 被装饰的函数

    Returns:
        包装后的函数
    """

    def before_hook(func: Callable, *args: Any, **kwargs: Any) -> None:
        """执行前记录开始时间"""
        mylog.info(f'开始执行函数: {func.__name__}')

    def after_hook(func: Callable, result: Any, *args: Any, **kwargs: Any) -> None:
        """执行后记录结束时间"""
        mylog.info(f'函数 {func.__name__} 执行完成')

    @universal_decorator(before_hook=before_hook, after_hook=after_hook)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """计时包装器"""
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            mylog.info(f'函数 {func.__name__} 执行耗时: {execution_time:.4f}秒')

    return wrapper


# 日志装饰器
def log_wrapper(func: Callable) -> Callable:
    """
    日志装饰器，记录函数调用和返回结果

    Args:
        func: 被装饰的函数

    Returns:
        包装后的函数
    """

    def before_hook(func: Callable, *args: Any, **kwargs: Any) -> None:
        """执行前记录参数"""
        mylog.debug(f'调用函数: {func.__name__}, 参数: args={args}, kwargs={kwargs}')

    def after_hook(func: Callable, result: Any, *args: Any, **kwargs: Any) -> None:
        """执行后记录结果"""
        mylog.debug(f'函数 {func.__name__} 返回结果: {result}')

    def exception_hook(func: Callable, exception: Exception, *args: Any, **kwargs: Any) -> None:
        """异常处理记录"""
        mylog.error(f'函数 {func.__name__} 执行异常: {exception}')

    return universal_decorator(before_hook=before_hook, after_hook=after_hook, exception_hook=exception_hook)(func)


# 重试装饰器工厂函数
def retry_wrapper(
    max_attempts: int = 3,
    min_wait: float = 0.0,
    max_wait: float = 1.0,
    exceptions: ExceptionTypes = (Exception,),
    log_retry: bool = True,
) -> Callable:
    """
    创建重试装饰器

    Args:
        max_attempts: 最大重试次数
        min_wait: 最小等待时间（秒）
        max_wait: 最大等待时间（秒）
        exceptions: 需要重试的异常类型
        log_retry: 是否记录重试信息

    Returns:
        重试装饰器
    """

    def decorator(func: Callable) -> Callable:
        """重试装饰器"""
        is_async = asyncio.iscoroutinefunction(func)

        @universal_decorator
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """重试包装器"""
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        # 计算等待时间
                        wait_time = _calculate_wait_time(min_wait, max_wait)
                        _handle_retry_attempt(func.__name__, attempt, max_attempts, e, wait_time, log_retry, is_async)
                    else:
                        # 最后一次尝试失败
                        _handle_final_failure(func.__name__, max_attempts, last_exception, log_retry)

            return None

        return wrapper

    return decorator


# 缓存装饰器
def cache_wrapper(ttl: int = 300) -> Callable:
    """
    创建缓存装饰器

    Args:
        ttl: 缓存生存时间（秒）

    Returns:
        缓存装饰器
    """

    def decorator(func: Callable) -> Callable:
        """缓存装饰器"""
        cache: dict = {}

        @universal_decorator
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """缓存包装器"""
            # 生成缓存键
            cache_key = (args, tuple(sorted(kwargs.items())))

            # 检查缓存
            if cache_key in cache:
                cached_value, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl:
                    mylog.debug(f'函数 {func.__name__} 命中缓存')
                    return cached_value

            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            mylog.debug(f'函数 {func.__name__} 缓存结果')

            return result

        return wrapper

    return decorator


# 测试函数
def main() -> None:
    """测试函数"""

    @timer_wrapper
    def sync_function(x: int) -> int:
        """同步测试函数"""
        time.sleep(0.1)
        return x * 2

    @timer_wrapper
    async def async_function(x: int) -> int:
        """异步测试函数"""
        await asyncio.sleep(0.1)
        return x * 3

    @retry_wrapper(max_attempts=3, min_wait=0.1, max_wait=0.5)
    def unstable_function(x: int) -> int:
        """不稳定的函数"""
        if _get_random_value() < 0.7:
            raise ValueError('随机错误')
        return x * 2

    # 测试同步函数
    sync_function(5)

    # 测试异步函数
    asyncio.run(async_function(5))

    # 测试重试函数
    with contextlib.suppress(Exception):
        unstable_function(10)


if __name__ == '__main__':
    main()
