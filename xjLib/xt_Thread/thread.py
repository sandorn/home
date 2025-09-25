# !/usr/bin/env python
"""
==============================================================
Description  : 线程管理工具模块 - 提供增强型线程基类、线程安全装饰器和线程管理器
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-06 14:00:00
FilePath     : /CODE/xjLib/xt_thread/thread.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- ThreadBase：增强型线程基类，提供结果获取、安全停止和资源清理功能
- SafeThread：安全线程类，提供异常捕获和重试机制
- ThreadManager：线程管理器，用于管理所有线程实例
- SingletonThread：单例线程类，确保同一目标函数只有一个线程实例
- run_in_thread：将函数在单独线程中执行的装饰器

主要特性：
- 线程安全的函数调用机制
- 完善的线程生命周期管理
- 异常捕获和重试机制
- 线程资源自动清理
- 支持上下文管理器的线程使用方式
- 单例模式确保线程唯一性
==============================================================
"""

from __future__ import annotations

import contextlib
import threading
import weakref
from collections.abc import Callable
from threading import Event, Thread
from typing import Any, ClassVar, TypeVar, cast

from xt_wraps.log import LogCls
from xt_wraps.singleton import SingletonMixin

log = LogCls()

# 类型定义
_T = TypeVar('_T')
_R = TypeVar('_R')


class ThreadBase(Thread):
    """
    增强型线程基类，提供结果获取、安全停止和资源清理功能

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数
    """

    def __init__(self, target: Callable[..., _T], *args: Any, daemon: bool = True, **kwargs: Any):
        # 提取回调函数
        self.callback = kwargs.pop('callback', None)
        super().__init__(
            target=target,
            name=target.__name__,
            args=args,
            daemon=daemon,
            kwargs=kwargs,
        )
        self._is_running = False
        self._result = None
        self._exception = None
        self._stop_event = Event()
        self._thread_started = False

    def __enter__(self) -> ThreadBase:
        """上下文管理器入口 - 自动启动线程"""
        if not self._thread_started:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口 - 自动停止线程"""
        if self.is_running():
            self.stop()
        return False  # 不抑制异常

    def start(self) -> None:
        """启动线程，确保线程只被启动一次"""
        if not self._thread_started:
            super().start()
            self._is_running = True
            self._thread_started = True

    def run(self) -> None:
        """执行目标函数并处理结果和回调"""
        self._is_running = True

        try:
            if not self._stop_event.is_set():
                self._result = self._target(*self._args, **self._kwargs)
                if callable(self.callback):
                    self._result = cast(_T, self.callback(self._result))
        except Exception as e:
            log.error(f'线程执行异常: {e}')
            self._exception = e
            self._result = None
        finally:
            self._is_running = False

    def get_result(self, timeout: float | None = None) -> Any:
        """获取线程执行结果，等待线程完成

        Args:
            timeout: 等待线程完成的最大时间（秒），None表示无限等待

        Returns:
            线程执行的结果，如果线程执行失败则返回None

        Raises:
            RuntimeError: 当线程未启动时抛出
        """
        if not self._thread_started:
            raise RuntimeError("Cannot get result from a thread that hasn't been started")

        try:
            self.join(timeout)
            return self._result
        except Exception as e:
            log.error(f'获取线程结果失败: {e}')
            return None

    def stop(self, timeout: float | None = None) -> bool:
        """安全停止线程

        Args:
            timeout: 等待线程停止的最大时间（秒），None表示无限等待

        Returns:
            bool: 线程是否成功停止
        """
        if self._is_running:
            self._is_running = False
            self._stop_event.set()

            if timeout is not None and self.is_alive():
                self.join(timeout)

            log(f'线程 {self.name} 已停止')
            return True
        return False

    def is_running(self) -> bool:
        """检查线程是否正在运行
        Returns:
            bool: True if thread is running, False otherwise

        Note:
            - is_alive(): 标准线程运行状态检查
            - isRunning(): 自定义扩展方法（如果存在）
        """
        try:
            # 检查自定义运行状态方法
            custom_running = self.isRunning() if hasattr(self, 'isRunning') else False
            # 结合标准线程状态检查
            return custom_running and self.is_alive()
        except RuntimeError:
            return False

    def __del__(self):
        """对象销毁时自动清理资源"""
        if hasattr(self, 'is_running') and hasattr(self, 'stop') and self.is_running():
            with contextlib.suppress(Exception):
                self.stop(timeout=1.0)


class SafeThread(ThreadBase):
    """
    安全线程类，提供异常捕获和重试机制

    适用于需要异常处理和重试的任务

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        max_retries: 最大重试次数，默认为0（不重试）
        **kwargs: 传递给目标函数的关键字参数

    Example:
        >>> def risky_task():
        >>> # 可能失败的任务
        >>>     if random.random() < 0.3:
        >>>         raise ValueError("随机失败")
        >>>     return "成功"
        >>>
        >>> thread = SafeThread(risky_task, max_retries=3)
        >>> thread.start()
    """

    def __init__(
        self,
        target: Callable,
        *args,
        max_retries: int = 0,
        daemon: bool = True,
        **kwargs: Any,
    ):
        super().__init__(target, *args, daemon=daemon, **kwargs)
        self.max_retries = max_retries
        self.retry_count = 0

    def run(self) -> None:
        self._is_running = True

        while self.retry_count <= self.max_retries and not self._stop_event.is_set():
            try:
                self._result = self._target(*self._args, **self._kwargs)
                if callable(self.callback):
                    self._result = cast(_T, self.callback(self._result))
                break  # 成功执行，退出循环
            except Exception as e:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    log(f'安全线程 {self.name} 执行失败，已达最大重试次数: {e}')
                    self._exception = e
                    break
                log(f'安全线程 {self.name} 第 {self.retry_count} 次重试: {e}')
                self._stop_event.wait(1)  # 等待一段时间后重试
            finally:
                self._is_running = False


class ThreadManager(SingletonMixin):
    """
    线程管理器，用于管理所有线程实例

    采用单例模式，确保全局只有一个线程管理器实例
    使用弱引用存储线程，避免内存泄漏
    """

    _threads: ClassVar[dict[int, weakref.ref]] = {}
    _lock = threading.RLock()

    def __init__(self):
        """初始化线程管理器"""
        super().__init__()

    @classmethod
    def create_thread(cls, target: Callable, *args, **kwargs) -> ThreadBase:
        """创建并启动线程，自动添加到管理器

        Args:
            target: 线程执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        Returns:
            ThreadBase: 创建的线程实例
        """
        thread = ThreadBase(target, *args, **kwargs)
        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

        thread.start()
        return thread

    @classmethod
    def create_safe_thread(cls, target: Callable, *args, **kwargs) -> SafeThread:
        """创建并启动安全线程，自动添加到管理器

        Args:
            target: 线程执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数，可包含max_retries

        Returns:
            SafeThread: 创建的安全线程实例
        """
        thread = SafeThread(target, *args, **kwargs)

        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

        thread.start()
        return thread

    @classmethod
    def add_thread(cls, thread: ThreadBase) -> None:
        """将已存在的线程添加到管理器

        Args:
            thread: 已创建的线程实例
        """
        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

    @classmethod
    def stop_all(cls, timeout: float | None = None) -> None:
        """停止所有管理的线程

        Args:
            timeout: 等待线程停止的最大时间（秒），None表示无限等待
        """
        with cls._lock:
            threads_to_stop = []
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None and thread.is_running():
                    threads_to_stop.append(thread)
                else:
                    del cls._threads[thread_id]

            for thread in threads_to_stop:
                thread.stop(timeout)

            cls._threads.clear()

    @classmethod
    def wait_all_completed(cls, timeout: float | None = None) -> dict[int, Any]:
        """等待所有线程完成并返回结果

        Args:
            timeout: 等待线程完成的最大时间（秒），None表示无限等待

        Returns:
            Dict[int, Any]: 线程ID到执行结果的映射
        """
        tmp_all_results = {}

        with cls._lock:
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None:
                    result = thread.get_result(timeout)
                    tmp_all_results[thread_id] = result
                else:
                    del cls._threads[thread_id]

        with cls._lock:
            cls._threads.clear()

        return tmp_all_results

    @classmethod
    def get_active_count(cls) -> int:
        """获取当前活动的线程数量

        Returns:
            int: 当前活动的线程数量
        """
        with cls._lock:
            # 清理已经结束的线程引用
            active_count = 0
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None and thread.is_alive():
                    active_count += 1
                else:
                    del cls._threads[thread_id]
            return active_count

    @classmethod
    def get_thread_by_id(cls, thread_id: int) -> ThreadBase | None:
        """根据ID获取线程实例

        Args:
            thread_id: 线程ID

        Returns:
            Optional[ThreadBase]: 对应的线程实例，如果不存在则返回None
        """
        with cls._lock:
            thread_ref = cls._threads.get(thread_id)
            return thread_ref() if thread_ref else None

    @classmethod
    def get_thread_by_name(cls, name: str) -> list[ThreadBase]:
        """根据名称获取线程实例列表

        Args:
            name: 线程名称

        Returns:
            List[ThreadBase]: 名称匹配的线程实例列表
        """
        result = []
        with cls._lock:
            for thread_ref in cls._threads.values():
                thread = thread_ref()
                if thread and thread.name == name:
                    result.append(thread)
        return result

    @classmethod
    def stop_thread(cls, thread_id: int, timeout: float | None = None) -> bool:
        """停止指定线程

        Args:
            thread_id: 线程ID
            timeout: 等待线程停止的最大时间（秒），None表示无限等待
        """
        thread = cls.get_thread_by_id(thread_id)
        if thread and thread.is_running():
            return thread.stop(timeout)
        return False


class SingletonThread(SingletonMixin, SafeThread):
    """
    单例线程类，确保同一目标函数只有一个线程实例

    特性:
    - 单例模式保证唯一性
    - 自动线程管理
    - 安全停止机制

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数，可包含max_retries
    """

    def __init__(self, target: Callable, *args, **kwargs):
        # 先调用SingletonMixin的初始化
        SingletonMixin.__init__(self)
        # 然后调用SafeThread的初始化
        SafeThread.__init__(self, target, *args, **kwargs)

        # 确保所有必要的属性都已初始化
        if not hasattr(self, '_thread_started'):
            self._thread_started = False
        if not hasattr(self, '_is_running'):
            self._is_running = True
        if not hasattr(self, '_stop_event'):
            self._stop_event = Event()

    def restart(self) -> None:
        """重启单例线程

        注意：这会创建一个新的线程实例，但由于单例模式，旧实例仍会被新实例替代
        """
        if self._thread_started and not self.is_alive():
            # 创建新的线程实例
            target = self._target
            args = self._args
            kwargs = self._kwargs
            # 从管理器中移除旧线程
            ThreadManager._threads.pop(id(self), None)
            # 创建新线程
            self = SafeThread(target, *args, **kwargs)
            # 添加到管理器
            ThreadManager.add_thread(self)
            # 启动新线程
            self.start()


class ComposedSingletonThread:
    """
    组合式单例线程类，确保同一目标函数只有一个线程实例

    使用组合而不是继承，避免多继承问题，提供更灵活的单例实现

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数，可包含max_retries
    """

    _instances: ClassVar[dict[tuple, ComposedSingletonThread]] = {}
    _lock = threading.RLock()

    def __new__(cls, target: Callable, *args, **kwargs):
        # 使用目标函数ID、参数和关键字参数作为单例键
        key = (id(target), args, frozenset(kwargs.items()))

        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)
                instance._thread = SafeThread(target, *args, **kwargs)
                instance._key = key
                cls._instances[key] = instance
            return cls._instances[key]

    def __init__(self, target: Callable, *args, **kwargs):
        # 防止重复初始化（因为__new__可能返回已存在的实例）
        if not hasattr(self, '_initialized'):
            self._initialized = True

    def start(self) -> None:
        """启动线程"""
        self._thread.start()

    def get_result(self, timeout: float | None = None) -> Any:
        """获取线程执行结果

        Args:
            timeout: 等待线程完成的最大时间（秒），None表示无限等待

        Returns:
            线程执行的结果，如果线程执行失败则返回None
        """
        return self._thread.get_result(timeout)

    def stop(self, timeout: float | None = None) -> bool:
        """停止线程

        Args:
            timeout: 等待线程停止的最大时间（秒），None表示无限等待

        Returns:
            bool: 线程是否成功停止
        """
        return self._thread.stop(timeout)

    def is_running(self) -> bool:
        """检查线程是否正在运行

        Returns:
            bool: 线程是否正在运行
        """
        return self._thread.is_running()

    def restart(self) -> None:
        """重启单例线程

        当线程已结束时，创建并启动一个新的线程实例
        """
        if self._thread._thread_started and not self._thread.is_alive():
            # 创建新的线程实例
            target = self._thread._target
            args = self._thread._args
            kwargs = self._thread._kwargs

            # 从管理器中移除旧线程
            ThreadManager._threads.pop(id(self._thread), None)

            # 创建新线程
            self._thread = SafeThread(target, *args, **kwargs)

            # 添加到管理器
            ThreadManager.add_thread(self._thread)

            # 启动新线程
            self._thread.start()

    def __getattr__(self, name):
        """委托所有未定义的属性到内部线程对象"""
        return getattr(self._thread, name)

    @classmethod
    def clear_instances(cls):
        """清除所有单例实例"""
        with cls._lock:
            cls._instances.clear()
