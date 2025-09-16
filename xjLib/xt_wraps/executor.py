#!/usr/bin/env python
"""
==============================================================
Description  : 异步执行器模块 - 提供异步执行同步函数和后台任务的功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-09-01 08:40:27
LastEditTime : 2025-09-11 16:40:00
FilePath     : /CODE/xjlib/xt_wraps/executor.py
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

from __future__ import annotations

import asyncio
from collections.abc import Callable
from concurrent.futures import Executor, ThreadPoolExecutor
from functools import partial, wraps
from typing import Any, TypeVar

from .exception import handle_exception
from .log import create_basemsg

R = TypeVar('R')
T = TypeVar('T', bound=Callable[..., Any])

# 常量定义
DEFAULT_EXECUTOR_MAX_WORKERS = 10  # 默认线程池最大工作线程数
DEFAULT_FUTURE_TIMEOUT = 30.0  # 默认Future超时时间（秒）

# 默认线程池执行器
_default_executor = ThreadPoolExecutor(max_workers=DEFAULT_EXECUTOR_MAX_WORKERS, thread_name_prefix='XtExecutor')


def _create_exception_handler(base_msg: str):
    """创建统一的异常处理回调函数"""

    def exception_handler(fut):
        if fut.exception():
            handle_exception(base_msg, fut.exception())

    return exception_handler


def run_on_executor(executor: Executor | None = None, background: bool = False):
    """
    异步装饰器
    - 支持同步函数使用 executor 加速
    - 异步函数和同步函数都可以使用 `await` 语法等待返回结果
    - 异步函数和同步函数都支持后台任务，无需等待
    Args:
        executor: 函数执行器, 装饰同步函数的时候使用
        background: 是否后台执行，默认False
    """

    def _run_on_executor(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if background:
                return asyncio.create_task(func(*args, **kwargs))
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # 确保在没有事件循环的线程中创建一个新的事件循环
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            task_func = partial(func, *args, **kwargs)  # 支持关键字参数
            return loop.run_in_executor(executor, task_func)

        # 根据函数类型选择包装器
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return _run_on_executor


class WrapperFactory:
    """包装器工厂类 - 集中管理各种包装器的创建逻辑"""

    @staticmethod
    def create_async_background_wrapper[R](func: Callable[..., R], base_msg: str) -> Callable[..., asyncio.Task[Any]]:
        """创建异步后台执行包装器"""

        @wraps(func)
        def async_background_wrapper[R](*args: Any, **kwargs: Any) -> asyncio.Task[R]:
            # R 是返回值类型参数，与外部保持一致
            async def task_wrapper():
                try:
                    return await func(*args, **kwargs)
                except Exception as err:
                    handle_exception(base_msg, err, re_raise=True)

            return asyncio.create_task(task_wrapper())

        return async_background_wrapper

    @staticmethod
    def create_async_wrapper[R](func: Callable[..., R], base_msg: str) -> Callable[..., Any]:
        """创建异步包装器"""

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as err:
                return handle_exception(base_msg, err, re_raise=True)

        return async_wrapper

    @staticmethod
    def create_sync_background_wrapper[R](func: Callable[..., R], base_msg: str, executor: ThreadPoolExecutor) -> Callable[..., asyncio.Future[R]]:
        """创建同步后台执行包装器"""

        @wraps(func)
        def sync_background_wrapper(*args: Any, **kwargs: Any) -> asyncio.Future[R]:
            loop = asyncio.get_event_loop()
            task_func = partial(func, *args, **kwargs)
            future = loop.run_in_executor(executor, task_func)
            future.add_done_callback(_create_exception_handler(base_msg))
            return future

        return sync_background_wrapper

    @staticmethod
    def create_sync_wrapper[R](func: Callable[..., R], base_msg: str, executor: ThreadPoolExecutor) -> Callable[..., R]:
        """创建同步包装器"""

        @wraps(func)
        async def sync_wrapper(*args: Any, **kwargs: Any) -> R:
            loop = asyncio.get_event_loop()
            task_func = partial(func, *args, **kwargs)
            try:
                return await loop.run_in_executor(executor, task_func)
            except Exception as err:
                return handle_exception(base_msg, err, re_raise=True)

        return sync_wrapper


class EventLoopManager:
    """事件循环管理类 - 统一处理事件循环的创建和获取逻辑"""

    @staticmethod
    def get_event_loop():
        """获取或创建事件循环"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 在新线程中创建并运行新的事件循环
                def run_in_new_loop(func, *args, **kwargs):
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        return new_loop.run_until_complete(func(*args, **kwargs))
                    finally:
                        new_loop.close()

                with ThreadPoolExecutor(max_workers=1) as executor:
                    return executor.submit(run_in_new_loop)
            return loop
        except RuntimeError:
            # 如果没有事件循环，创建一个新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop


class ExecutorDecorators:
    """执行器装饰器集合 - 提供各类执行器装饰器功能"""

    @staticmethod
    def executor_wraps(
        fn: Callable[..., Any] | None = None,
        *,
        background: bool = False,
        executor: ThreadPoolExecutor | None = None,
    ) -> Callable[..., Any]:
        """
        异步执行器装饰器 - 将同步函数转换为异步函数执行，或增强异步函数的执行能力

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
        """

        def decorator[R](func: Callable[..., R]) -> Callable[..., Any]:
            # R 是原函数返回值类型参数
            used_executor = executor or _default_executor
            base_msg = create_basemsg(func)

            match (asyncio.iscoroutinefunction(func), background):
                case (True, True):
                    return WrapperFactory.create_async_background_wrapper(func, base_msg)
                case (True, False):
                    return WrapperFactory.create_async_wrapper(func, base_msg)
                case (False, True):
                    return WrapperFactory.create_sync_background_wrapper(func, base_msg, used_executor)
                case _:
                    return WrapperFactory.create_sync_wrapper(func, base_msg, used_executor)
            # # 根据函数类型和执行模式选择合适的包装器
            # if asyncio.iscoroutinefunction(func):
            #     if background:
            #         return WrapperFactory.create_async_background_wrapper(func, base_msg)
            #     return WrapperFactory.create_async_wrapper(func, base_msg)

            # if background:
            #     return WrapperFactory.create_sync_background_wrapper(func, base_msg, used_executor)
            # return WrapperFactory.create_sync_wrapper(func, base_msg, used_executor)

        # 处理装饰器调用方式
        return decorator(fn) if fn else decorator

    @staticmethod
    def run_executor_wraps(fn: Callable[..., Any] | None = None) -> Callable[..., Any]:
        """
        同步运行异步函数装饰器 - 将异步函数转换为可直接调用的同步函数

        核心功能：
        - 自动适配异步和同步函数
        - 智能事件循环管理（处理循环已运行、未创建等情况）
        - 统一的异常处理机制

        Args:
            fn: 要装饰的函数（支持同步和异步函数），可选

        Returns:
            同步函数，可以直接调用而不需要await
        """

        def decorator[R](func: Callable[..., R]) -> Callable[..., R]:
            # R 是原函数返回值类型参数
            base_msg = create_basemsg(func)

            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> R:
                if asyncio.iscoroutinefunction(func):
                    try:
                        result = EventLoopManager.get_event_loop()
                        if isinstance(result, ThreadPoolExecutor._WorkItem):
                            # 如果是在线程池中运行，需要获取结果
                            return result.result()
                        # 否则直接运行协程
                        return result.run_until_complete(func(*args, **kwargs))
                    except Exception as err:
                        return handle_exception(base_msg, err)
                else:
                    try:
                        return func(*args, **kwargs)
                    except Exception as err:
                        return handle_exception(base_msg, err)

            return sync_wrapper

        # 处理装饰器调用方式
        return decorator(fn) if fn else decorator

    @staticmethod
    def future_wraps(
        fn: Callable[..., Any] | None = None,
        *,
        executor: ThreadPoolExecutor | None = None,
    ) -> Callable[..., Any]:
        """
        Future执行器装饰器 - 将同步函数包装成返回asyncio.Future对象的函数

        核心功能：
        - 将同步函数转换为返回Future的函数
        - 支持自定义线程池执行器
        - 自动异常捕获和处理

        Args:
            fn: 要装饰的同步函数，可选
            executor: 自定义线程池执行器，默认为None（使用默认执行器）

        Returns:
            装饰后的函数，返回asyncio.Future对象，可通过await获取结果
        """

        def decorator[R](func: Callable[..., R]) -> Callable[..., asyncio.Future[R]]:
            # R 是原函数返回值类型参数
            base_msg = create_basemsg(func)

            @wraps(func)
            def wrapper[R](*args: Any, **kwargs: Any) -> asyncio.Future[R]:
                # R 是原函数返回值类型参数
                try:
                    loop = asyncio.get_event_loop()
                    used_executor = executor or _default_executor
                    future = loop.run_in_executor(used_executor, lambda: func(*args, **kwargs))
                    future.add_done_callback(_create_exception_handler(base_msg))
                    return future
                except Exception as err:
                    # 创建一个已完成的future并设置异常
                    future = loop.create_future()
                    future.set_exception(err)
                    return future

            return wrapper

        return decorator(fn) if fn else decorator


# 导出装饰器函数
executor_wraps = ExecutorDecorators.executor_wraps
run_executor_wraps = ExecutorDecorators.run_executor_wraps
future_wraps = ExecutorDecorators.future_wraps


async def future_wraps_result[T](future: asyncio.Future[T]) -> T:
    """
    Future结果获取器 - 等待Future完成并返回结果，带超时处理和异常管理

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
    except TimeoutError as timerr:
        # 如果超时，取消任务并抛出异常
        if not future.done():
            future.cancel()
        return handle_exception(create_basemsg(_dummy_func_for_log), timerr, re_raise=True)
    except asyncio.CancelledError as cancerr:
        return handle_exception(create_basemsg(_dummy_func_for_log), cancerr, re_raise=True)
    except Exception as err:
        return handle_exception(create_basemsg(_dummy_func_for_log), err, re_raise=True)
