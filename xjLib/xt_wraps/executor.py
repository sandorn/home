#!/usr/bin/env python
"""
==============================================================
Description  : 异步执行器模块 - 提供异步执行同步函数和后台任务的功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 08:40:27
LastEditTime : 2025-09-06 11:45:00
FilePath     : /CODE/xjLib/xt_wraps/executor.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- executor_wraps：异步执行同步函数，支持后台执行模式
- run_executor_wraps：同步运行异步函数，无需await
- future_wraps：将同步函数包装为返回Future对象的函数
- future_wraps_result：等待Future完成并返回结果，含超时处理

主要特性：
- 自动识别并适配同步和异步函数
- 支持后台执行模式，不阻塞主程序流程
- 统一的异常处理机制
- 支持自定义线程池执行器
- 提供超时控制和Future结果处理
- 完整的类型提示支持
==============================================================
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, Callable, Optional, TypeVar

from .exception import handle_exception
from .log import create_basemsg

# 类型变量
T = TypeVar("T")
R = TypeVar("R")

# 常量定义
DEFAULT_EXECUTOR_MAX_WORKERS = 10  # 默认线程池最大工作线程数
DEFAULT_FUTURE_TIMEOUT = 30.0  # 默认Future超时时间（秒）

# 默认线程池执行器
_default_executor = ThreadPoolExecutor(
    max_workers=DEFAULT_EXECUTOR_MAX_WORKERS, thread_name_prefix="XtExecutor"
)


def executor_wraps(
    fn: Optional[Callable[..., Any]] = None,
    *,
    background: bool = False,
    executor: Optional[ThreadPoolExecutor] = None,
) -> Callable[..., Any]:
    """异步执行器装饰器 - 将同步函数转换为异步函数执行，或增强异步函数的执行能力

    核心功能：
    - 自动识别并适配同步/异步函数
    - 支持后台执行模式，不阻塞主程序流程
    - 统一的异常处理机制
    - 支持自定义线程池执行器

    Args:
        fn: 要装饰的函数，可选（支持同步和异步函数）
        background: 是否在后台执行，默认为False
                    - False: 返回协程对象，需要await等待执行完成
                    - True: 返回Future/Task对象，立即返回不阻塞
        executor: 自定义线程池执行器，默认为None（使用默认执行器）

    Returns:
        装饰后的函数，根据参数和原函数类型返回不同对象：
        - 当background=False时：返回协程对象，需要await
        - 当background=True时：返回Future/Task对象，可后续await获取结果

    示例:
        # 装饰同步函数
        @executor_wraps
        def sync_function():
            time.sleep(1)
            return "完成"

        # 后台执行同步函数
        @executor_wraps(background=True)
        def background_task():
            time.sleep(5)
            return "后台任务完成"

        # 使用自定义执行器
        custom_executor = ThreadPoolExecutor(max_workers=3)
        @executor_wraps(executor=custom_executor)
        def custom_task():
            time.sleep(1)
            return "自定义执行器任务完成"

        # 在异步环境中使用
        async def main():
            # 普通模式 - 等待完成
            result = await sync_function()

            # 后台模式 - 立即返回，稍后获取结果
            future = background_task()
            # ... 做其他事情 ...
            result = await future  # 稍后获取结果
    """

    def decorator(func: Callable[..., R]) -> Callable[..., Any]:
        used_executor = executor or _default_executor
        base_msg = create_basemsg(func)

        if asyncio.iscoroutinefunction(func):
            if background:
                # 后台执行模式 - 返回普通函数，直接返回Task对象
                @wraps(func)
                def async_background_wrapper(
                    *args: Any, **kwargs: Any
                ) -> asyncio.Task[Any]:
                    # 后台执行异步函数，捕获并记录异常
                    async def task_wrapper():
                        try:
                            return await func(*args, **kwargs)
                        except Exception as err:
                            handle_exception(err, base_msg, re_raise=True)
                            # 重新抛出异常，让任务知道它失败了

                    # 直接返回创建的任务对象，不使用async函数包装
                    return asyncio.create_task(task_wrapper())

                return async_background_wrapper
            else:
                # 非后台模式 - 返回异步函数
                @wraps(func)
                async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                    # 非后台模式下捕获并处理异常
                    try:
                        return await func(*args, **kwargs)
                    except Exception as err:
                        return handle_exception(err, base_msg, re_raise=True)

                return async_wrapper
        else:
            if background:
                # 后台执行模式 - 返回普通函数，直接返回Future对象
                @wraps(func)
                def sync_background_wrapper(
                    *args: Any, **kwargs: Any
                ) -> asyncio.Future:
                    loop = asyncio.get_event_loop()
                    task_func = partial(func, *args, **kwargs)

                    # 同步函数后台执行直接返回future
                    future = loop.run_in_executor(used_executor, task_func)

                    # 添加回调来处理异常（如果有）
                    def exception_handler(fut):
                        if fut.exception():
                            handle_exception(fut.exception(), base_msg, re_raise=True)

                    future.add_done_callback(exception_handler)
                    return future  # 直接返回future

                return sync_background_wrapper
            else:
                # 非后台模式 - 返回异步函数
                @wraps(func)
                async def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                    loop = asyncio.get_event_loop()
                    task_func = partial(func, *args, **kwargs)

                    # 非后台模式下等待执行完成
                    try:
                        return await loop.run_in_executor(used_executor, task_func)
                    except Exception as err:
                        return handle_exception(err, base_msg, re_raise=True)

                return sync_wrapper

    # 处理装饰器调用方式
    return decorator(fn) if fn else decorator


def run_executor_wraps(fn: Optional[Callable[..., Any]] = None) -> Callable[..., Any]:
    """同步运行异步函数装饰器 - 将异步函数转换为可直接调用的同步函数

    核心功能：
    - 自动适配异步和同步函数
    - 智能事件循环管理（处理循环已运行、未创建等情况）
    - 统一的异常处理机制

    Args:
        fn: 要装饰的函数（支持同步和异步函数），可选

    Returns:
        同步函数，可以直接调用而不需要await

    示例:
        # 装饰异步函数，使其可同步调用
        @run_executor_wraps
        async def async_function():
            await asyncio.sleep(1)
            return "异步函数完成"

        # 直接调用，无需await
        result = async_function()  # 同步获取结果

        # 也可以装饰同步函数（保持功能不变但增加异常处理）
        @run_executor_wraps
        def sync_function():
            time.sleep(1)
            return "同步函数完成"
    """

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        base_msg = create_basemsg(func)

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> R:
            if asyncio.iscoroutinefunction(func):
                try:
                    # 尝试获取当前事件循环
                    loop = asyncio.get_event_loop()
                    # 如果事件循环正在运行，我们需要在线程池中创建新的事件循环
                    if loop.is_running():
                        # 在新线程中创建并运行新的事件循环
                        def run_in_new_loop():
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            try:
                                return new_loop.run_until_complete(
                                    func(*args, **kwargs)
                                )
                            finally:
                                new_loop.close()

                        # 使用线程池执行器来运行新的事件循环
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            return executor.submit(run_in_new_loop).result()
                    else:
                        # 使用当前事件循环
                        return loop.run_until_complete(func(*args, **kwargs))
                except RuntimeError:
                    # 如果没有事件循环，创建一个新的事件循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        return loop.run_until_complete(func(*args, **kwargs))
                    finally:
                        loop.close()
                except Exception as err:
                    return handle_exception(err, base_msg)
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    return handle_exception(err, base_msg)

        return sync_wrapper

    # 处理装饰器调用方式
    return decorator(fn) if fn else decorator


def future_wraps(
    fn: Optional[Callable[..., Any]] = None,
    *,
    executor: Optional[ThreadPoolExecutor] = None,
) -> Callable[..., Any]:
    """Future执行器装饰器 - 将同步函数包装成返回asyncio.Future对象的函数

    核心功能：
    - 将同步函数转换为返回Future的函数
    - 支持自定义线程池执行器
    - 自动异常捕获和处理

    Args:
        fn: 要装饰的同步函数，可选
        executor: 自定义线程池执行器，默认为None（使用默认执行器）

    Returns:
        装饰后的函数，返回asyncio.Future对象，可通过await获取结果

    示例:
        # 装饰同步函数为返回Future的函数
        @future_wraps
        def calculate_sum(a, b):
            time.sleep(1)
            return a + b

        # 使用方式
        future = calculate_sum(10, 20)  # 立即返回Future对象
        result = await future  # 等待并获取结果

        # 使用自定义执行器
        custom_executor = ThreadPoolExecutor(max_workers=2)
        @future_wraps(executor=custom_executor)
        def complex_calculation(x, y):
            time.sleep(1)
            return x * y
    """

    def decorator(func: Callable[..., R]) -> Callable[..., asyncio.Future[R]]:
        base_msg = create_basemsg(func)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> asyncio.Future[R]:
            try:
                loop = asyncio.get_event_loop()
                used_executor = executor or _default_executor
                future = loop.run_in_executor(
                    used_executor, lambda: func(*args, **kwargs)
                )

                # 添加回调来处理异常（如果有）
                def exception_handler(fut):
                    if fut.exception():
                        handle_exception(fut.exception(), base_msg)

                future.add_done_callback(exception_handler)
                return future
            except Exception as err:
                # 创建一个已完成的future并设置异常
                future = loop.create_future()
                future.set_exception(err)
                return future

        return wrapper

    return decorator(fn) if fn else decorator


async def future_wraps_result(future: asyncio.Future[T]) -> T:
    """Future结果获取器 - 等待Future完成并返回结果，带超时处理和异常管理

    核心功能：
    - 等待Future完成并获取结果
    - 自动超时处理，避免永久阻塞
    - 统一的异常处理机制
    - 自动取消超时的Future

    Args:
        future: 要等待的Future对象

    Returns:
        Future完成后的结果

    Raises:
        asyncio.TimeoutError: 当Future在DEFAULT_FUTURE_TIMEOUT(30秒)内未完成时
        asyncio.CancelledError: 当Future被取消时
        其他可能的异常: 由Future执行过程中抛出的原始异常

    示例:
        # 假设已有一个Future对象
        future = some_async_operation()

        try:
            # 等待Future完成并获取结果
            result = await future_wraps_result(future)
            print(f"结果: {result}")
        except asyncio.TimeoutError:
            print("操作超时")
        except Exception as e:
            print(f"发生错误: {e}")
    """

    # 为future_wraps_result创建一个假的可调用对象用于日志
    def _dummy_func_for_log(): ...

    try:
        # 添加超时机制，避免永久等待
        return await asyncio.wait_for(future, timeout=DEFAULT_FUTURE_TIMEOUT)
    except asyncio.TimeoutError as timerr:
        # 如果超时，取消任务并抛出异常
        if not future.done():
            future.cancel()
        return handle_exception(
            timerr, create_basemsg(_dummy_func_for_log), re_raise=True
        )
    except asyncio.CancelledError as cancerr:
        return handle_exception(
            cancerr, create_basemsg(_dummy_func_for_log), re_raise=True
        )
    except Exception as err:
        return handle_exception(err, create_basemsg(_dummy_func_for_log), re_raise=True)
