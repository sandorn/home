"""
==============================================================
Description  : 线程装饰器模块 - 提供函数线程化、并行化和线程安全装饰器
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-07 17:00:00
FilePath     : /CODE/xjLib/xt_thread/wraps.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- thread_safe：线程安全装饰器，确保函数在多线程环境中的安全调用
- thread_print：线程安全的打印函数
- run_in_thread：将函数在单独线程中执行的简洁装饰器
- thread_wraps：增强型线程装饰器，支持回调和线程配置
- ThreadWrapsManager：类风格的线程装饰器，支持结果收集和批量管理
- run_in_qtthread：将函数在QThread中执行的装饰器
- qthread_wraps：PyQt6线程装饰器，用于GUI应用程序
- parallelize_wraps：函数并行化装饰器，利用线程池提高处理效率

主要特性：
- 支持同步函数的异步执行
- 提供结果获取、异常处理和回调机制
- 支持守护线程设置和线程生命周期管理
- 与PyQt6框架无缝集成
- 简洁统一的API设计，易于使用
- 完整的类型注解支持
==============================================================
"""

from __future__ import annotations

import builtins
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Any, ClassVar, TypeVar

import wrapt
from xt_thread.qthread import QtThreadBase, QtThreadManager
from xt_thread.thread import ThreadBase, ThreadManager

# 类型定义
T = TypeVar('T')  # 泛型类型变量，用于表示任意类型
R = TypeVar('R')  # 泛型类型变量，用于表示返回值类型


def thread_safe[R](func: Callable[..., R]) -> Callable[..., R]:
    """线程安全装饰器，确保函数在多线程环境中的安全调用

    为函数或方法添加线程安全保护，使用锁机制防止并发访问导致的问题。
    支持内置函数、普通函数和类方法。

    Args:
        func: 需要进行线程安全处理的函数或方法

    Returns:
        线程安全的包装函数，保持原函数签名

    Example:
        >>> @thread_safe
        >>> def shared_resource_access():
        >>> # 访问共享资源的代码
        >>>     pass
    """
    # 为非内置函数提前初始化锁，避免每次调用检查
    if func.__module__ != builtins.__name__ and not hasattr(func, '__lock__'):
        func.__lock__ = threading.Lock()

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.__module__ == builtins.__name__:  # 内置函数使用临时锁
            with threading.Lock():
                return func(*args, **kwargs)
        else:  # 普通函数和类方法使用预初始化的锁
            with func.__lock__:
                return func(*args, **kwargs)

    return wrapper


thread_print = thread_safe(print)


# 线程执行装饰器
def run_in_thread[R](func: Callable[..., R]) -> Callable[..., ThreadBase]:
    """简洁的线程装饰器，将函数在单独线程中执行

    将任何函数转换为在独立线程中执行的版本，保持函数签名不变但返回线程对象。
    适用于快速线程化简单函数。

    Args:
        func: 需要在线程中执行的函数

    Returns:
        包装后的函数，调用时返回ThreadBase实例，可通过get_result()获取结果

    Example:
        >>> @run_in_thread
        >>> def long_running_task(param):
        >>> # 长时间运行的任务
        >>>     return result
        >>>
        >>> # 调用方式不变，但会在线程中执行
        >>> thread = long_running_task(param)
        >>> result = thread.get_result()  # 获取执行结果
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> ThreadBase:
        return ThreadManager.create_thread(func, *args, **kwargs)

    return wrapper


def thread_wraps(fn=None, daemon=False, max_retries=0):
    """增强型线程装饰器 - 将函数转换为在线程中执行的版本

    支持两种调用方式：直接装饰(@thread_wraps)和带参数装饰(@thread_wraps(daemon=True, max_retries=3))
    提供更丰富的配置选项，包括守护线程设置、回调函数和重试机制。

    Args:
        func: 被装饰的函数（当直接调用时）
        daemon: 是否设置为守护线程
        max_retries: 最大重试次数

    Returns:
        装饰后的函数，调用时返回线程实例，可通过get_result()方法获取执行结果

    Example:
        >>> # 1. 直接装饰函数
        >>> @thread_wraps
        >>> def long_running_task(x):
        >>> # 耗时操作
        >>>     return x * 2
        >>>
        >>> # 调用方式不变，但会在线程中执行
        >>> thread = long_running_task(10)
        >>> result = thread.get_result()  # 获取执行结果
        >>>
        >>> # 2. 带参数装饰
        >>> @thread_wraps(daemon=True, max_retries=3)
        >>> def critical_task(x):
        >>> # 关键任务，需要重试
        >>>     return x * 2
        >>>
        >>> # 调用方式不变
        >>> thread = critical_task(10)
        >>> result = thread.get_result()
    """

    # 处理两种调用方式：直接装饰(@thread_wraps)和带参数装饰(@thread_wraps())
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if max_retries > 0:
                    # 创建安全线程（带重试机制）
                    thread_instance = ThreadManager.create_safe_thread(
                        func,
                        *args,
                        max_retries=max_retries,
                        daemon=daemon,
                        **kwargs,
                    )
                else:
                    # 创建普通线程
                    thread_instance = ThreadManager.create_thread(func, *args, daemon=daemon, **kwargs)
                return thread_instance
            except Exception as e:
                thread_print(f'创建线程时发生错误: {e}')
                raise

        return wrapper

    # 如果带参数调用装饰器，则返回装饰器函数
    return decorator(fn) if fn is not None else decorator


class ThreadWrapsManager:
    """类风格的线程装饰器 - 提供更丰富的线程管理功能

    支持结果收集、批量管理和线程控制，适用于需要统一管理多个线程的场景。

    Example:
        >>> @ThreadWrapsManager
        >>> def process_data(x):
        >>> # 处理数据
        >>>     return x * 5
        >>>
        >>> # 创建并启动线程
        >>> thread = process_data(10)
        >>> # 获取单个结果
        >>> result = thread.get_result()
        >>> # 获取所有线程的结果
        >>> all_results = ThreadWrapsManager.getAllResult()
    """

    # 存储所有线程实例的字典
    _thread_dict: ClassVar[dict] = {}  # ✅ 标注为类变量
    _lock = threading.Lock()

    def __init__(self, func: Callable[..., T]):
        self.func = func

    def __call__(self, *args: Any, **kwargs: Any) -> ThreadBase:
        try:
            # 创建线程实例，使用ThreadManager的方法
            thread_instance = ThreadManager.create_thread(self.func, *args, **kwargs)

            # 保存线程引用，便于获取所有结果
            with self._lock:
                self._thread_dict[id(thread_instance)] = thread_instance
            # thread_print(f"函数 `{self.func.__name__}` 由 ThreadWrapsManager 启动")
            return thread_instance
        except Exception as e:
            thread_print(f'创建ThreadWrapsManager线程时发生错误: {e}')
            raise

    @classmethod
    def get_all_result(cls) -> dict[int, Any | None]:
        """获取所有由该装饰器创建的线程的结果

        Returns:
            字典，键为线程ID，值为线程执行结果
        """
        results: dict[int, Any | None] = {}  # 存储线程ID到结果的映射

        with cls._lock:
            # 创建线程引用的副本，避免在迭代过程中修改字典
            threads_copy = list(cls._thread_dict.items())  # 使用下划线开头，表示内部变量

        for thread_id, thread in threads_copy:
            try:
                # 等待线程完成并获取结果
                results[thread_id] = thread.get_result()
            except Exception as e:
                thread_print(f'获取线程结果时发生错误: {e}')
                results[thread_id] = None

        return results

    @classmethod
    def clear(cls) -> None:
        """清除所有线程引用，释放资源"""
        with cls._lock:
            cls._thread_dict.clear()
        thread_print('ThreadWrapsManager 已清除所有线程引用')


# PyQt6线程装饰器
def run_in_qtthread[R](func: Callable[..., R]) -> Callable[..., QtThreadBase]:
    """Qt线程装饰器，将函数在QThread中异步执行

    将任何函数转换为在独立QThread中执行的版本，保持函数签名不变但返回线程对象。
    适用于PyQt6应用程序中的后台任务。

    Args:
        func: 要在线程中执行的函数

    Returns:
        装饰后的函数，返回QtThreadBase实例

    Example:
        >>> @run_in_qtthread
        >>> def long_running_task(param):
        >>> # 长时间运行的任务
        >>>     time.sleep(2)
        >>>     return f"处理完成: {param}"
        >>>
        >>> # 调用方式不变，但会在QThread中执行
        >>> thread = long_running_task('数据')
        >>> # 可选：等待结果
        >>> result = thread.get_result(timeout=5)
        >>> print(result)  # 输出: 处理完成: 数据
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> QtThreadBase:
        try:
            return QtThreadManager.create_thread(func, *args, **kwargs)
        except Exception as e:
            thread_print(f'创建QtThread时发生错误: {e}')
            raise

    return wrapper


def qthread_wraps(fn=None, daemon=False, max_retries=0):
    """PyQt6线程装饰器 - 将函数转换为在QThread中执行的版本

    轻量级PyQt6线程装饰器，为函数添加QThread支持，适用于简单的PyQt应用场景。

    Args:
        func: 被装饰的函数

    Returns:
        装饰后的函数，调用时返回QtThreadBase实例，可通过get_result()方法获取执行结果

    Example:
        >>> @qthread_wraps
        >>> def pyqt_task(data):
        >>> # PyQt相关的耗时操作
        >>>     return processed_data
        >>>
        >>> # 调用方式不变，但会在QThread中执行
        >>> qt_thread = pyqt_task('input_data')
        >>> result = qt_thread.get_result()  # 获取执行结果
    """

    # 处理两种调用方式：直接装饰(@qthread_wraps)和带参数装饰(@qthread_wraps())
    def _decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            try:
                # 检查是否需要安全线程（带重试机制）
                if max_retries > 0:
                    # 创建安全线程（带重试机制）
                    return QtThreadManager.create_safe_thread(func, *args, max_retries=max_retries, retry_delay=kwargs.pop('retry_delay', 1.0), daemon=daemon, **kwargs)
                return QtThreadManager.create_thread(func, *args, daemon=daemon, **kwargs)
            except Exception as e:
                thread_print(f'创建线程时发生错误: {e}')
                raise

        return _wrapper

    # 如果带参数调用装饰器，则返回装饰器函数
    return _decorator(fn) if fn is not None else _decorator


@wrapt.decorator
def parallelize_wraps(func, instance, args, kwargs):
    """函数并行化装饰器 - 使用线程池并行执行函数

    适用于处理大量独立数据项的场景，可显著提高处理效率。
    自动管理线程池生命周期，保持输入顺序返回结果。

    Args:
        func: 被装饰的函数，应接收单个数据项作为参数
        instance: 实例方法的self参数
        args: 包含数据项的可迭代对象
        kwargs: 关键字参数

    Returns:
        函数执行结果的列表，保持原始输入顺序

    Example:
        >>> @parallelize_wraps
        >>> def process_item(item):
        >>> # 处理单个数据项
        >>>     return item * 2
        >>>
        >>> # 并行处理多个数据项
        >>> results = process_item([1, 2, 3, 4, 5])
        >>> # results 将是 [2, 4, 6, 8, 10]
    """
    try:
        max_workers = kwargs.pop('max_workers', None)  # 使用下划线开头，表示内部变量
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(func, *args, **kwargs))
        thread_print(f'并行处理完成，共处理 {len(results)} 个项目')
        return results
    except Exception as e:
        thread_print(f'并行处理时发生错误: {e}')
        raise


# 公共API导出
__all__ = [
    'ThreadWrapsManager',
    'parallelize_wraps',
    'qthread_wraps',
    'run_in_qtthread',
    'run_in_thread',
    'thread_print',
    'thread_safe',
    'thread_wraps',
]
