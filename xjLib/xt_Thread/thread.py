# !/usr/bin/env python
"""
==============================================================
Description  : 线程管理工具模块 - 提供增强型线程基类、线程安全装饰器和线程管理器
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2025-09-06 14:00:00
Github       : https://github.com/sandorn/nsthread

本模块提供以下核心功能：
- ThreadBase：增强型线程基类,提供结果获取、安全停止和资源清理功能
- SafeThread：安全线程类,提供异常捕获和重试机制
- ThreadManager：线程管理器,用于管理所有线程实例
- SingletonThread：单例线程类,确保同一目标函数只有一个线程实例
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
from typing import Any, ClassVar

from xtlog import mylog

from .exception import safe_call
from .singleton import SingletonMixin


class ThreadBase(Thread):
    """增强型线程基类，提供结果获取、安全停止和资源清理功能

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        daemon: 是否为守护线程，默认为True
        **kwargs: 传递给目标函数的关键字参数，可包含callback回调函数

    Attributes:
        callback: 线程执行完成后的回调函数
        _is_running: 线程运行状态标志
        _result: 线程执行结果
        _exception: 线程执行过程中捕获的异常
        _stop_event: 用于安全停止线程的事件对象
        _thread_started: 线程是否已启动的标志
    """

    _target: Callable[..., Any]
    _args: tuple
    _kwargs: dict[str, Any]

    def __init__(
        self,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: tuple = (),
        kwargs: dict[str, Any] = {},
        *,
        daemon: bool | None = True,
        **thread_kwargs: Any,  # 接收线程自身的额外参数
    ):
        super().__init__(
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
        )
        self.callback = thread_kwargs.pop('callback', None)
        self._thread_kwargs = thread_kwargs
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
        """启动线程,确保线程只被启动一次"""
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
                    self._result = self.callback(self._result)
        except Exception as e:
            mylog.error('线程执行异常: {}', e)
            self._exception = e
            self._result = None
        finally:
            self._is_running = False

    def get_result(self, timeout: float | None = None) -> Any:
        """获取线程执行结果,等待线程完成

        Args:
            timeout: 等待线程完成的最大时间（秒）,None表示无限等待

        Returns:
            线程执行的结果,如果线程执行失败则返回None

        Raises:
            RuntimeError: 当线程未启动时抛出
        """
        if not self._thread_started:
            raise RuntimeError("Cannot get result from a thread that hasn't been started")

        try:
            self.join(timeout)
            return self._result
        except Exception as e:
            mylog.error('获取线程结果失败: {}', e)
            return None

    def stop(self, timeout: float | None = None) -> bool:
        """安全停止线程

        Args:
            timeout: 等待线程停止的最大时间（秒）,None表示无限等待

        Returns:
            bool: 线程是否成功停止
        """
        if not self._is_running:
            return False
        self._is_running = False
        self._stop_event.set()

        if timeout is not None and self.is_alive():
            self.join(timeout)

        mylog.info('线程 {} 已停止', self.name)
        return True

    def is_running(self) -> bool:
        """检查线程是否正在运行

        Returns:
            bool: 线程是否正在运行

        Note:
            - is_alive(): 标准线程运行状态检查
        """
        return self._is_running and self.is_alive()

    def __del__(self):
        """对象销毁时自动清理资源"""
        with contextlib.suppress(Exception):
            # 检查对象是否仍有必要的属性且线程正在运行
            if hasattr(self, 'is_running') and hasattr(self, 'stop'):
                # 使用try-except包装is_running()调用，因为它可能也会访问已经被清理的资源
                try:
                    is_running_flag = self.is_running()
                except Exception:
                    is_running_flag = False

                if is_running_flag:
                    with contextlib.suppress(Exception):
                        self.stop(timeout=1.0)


class SafeThread(ThreadBase):
    """安全线程类，提供异常捕获和重试机制

    适用于需要异常处理和重试的任务

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        max_retries: 最大重试次数，默认为0（不重试）
        retry_delay: 重试等待时间（秒），默认为1.0
        daemon: 是否为守护线程，默认为True
        **kwargs: 传递给目标函数的关键字参数

    Attributes:
        max_retries: 最大重试次数
        retry_count: 当前已重试次数
        retry_delay: 重试等待时间（秒）

    Example:
        >>> def risky_task():
        >>> # 可能失败的任务
        >>>     if random.random() < 0.3:
        >>>         raise ValueError("随机失败")
        >>>     return "成功"
        >>>
        >>> thread = SafeThread(risky_task, max_retries=3, retry_delay=0.5)
        >>> thread.start()
    """

    def __init__(
        self,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: tuple = (),
        kwargs: dict[str, Any] = {},
        *,
        daemon: bool | None = True,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        **thread_kwargs: Any,  # 接收线程自身的额外参数
    ):
        self.callback = thread_kwargs.pop('callback', None)

        super().__init__(
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
        )
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_count = 0

    @safe_call()
    def run(self) -> None:
        self._is_running = True

        while self.retry_count <= self.max_retries and not self._stop_event.is_set():
            try:
                self._result = self._target(*self._args, **self._kwargs)
                if callable(self.callback):
                    self._result = self.callback(self._result)
                break  # 成功执行,退出循环
            except Exception as e:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    mylog.error('安全线程 {} 执行失败,已达最大重试次数: {}', self.name, e)
                    self._exception = e
                    break
                mylog.info('安全线程 {} 第 {} 次重试: {}', self.name, self.retry_count, e)
                self._stop_event.wait(self.retry_delay)  # 使用指定的重试等待时间
            finally:
                self._is_running = False


class ThreadManager(SingletonMixin):
    """线程管理器，用于管理所有线程实例

    采用单例模式，确保全局只有一个线程管理器实例
    使用弱引用存储线程，避免内存泄漏

    Attributes:
        _threads: 存储线程弱引用的字典
        _lock: 线程安全锁
    """

    _threads: ClassVar[dict[int, weakref.ref]] = {}
    _lock = threading.RLock()

    def __init__(self):
        """初始化线程管理器"""
        super().__init__()

    @classmethod
    def create_thread(
        cls,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: tuple = (),
        kwargs: dict[str, Any] = {},
        *,
        daemon: bool | None = True,
        **thread_kwargs: Any,  # 接收线程自身的额外参数
    ) -> ThreadBase:
        """创建并启动线程,自动添加到管理器

        Args:
            target: 线程执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        Returns:
            ThreadBase: 创建的线程实例
        """
        thread = ThreadBase(
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
            **thread_kwargs,  # 传递线程自身的额外参数
        )
        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

        thread.start()
        return thread

    @classmethod
    def create_safe_thread(
        cls,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: tuple = (),
        kwargs: dict[str, Any] = {},
        *,
        daemon: bool | None = True,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        **thread_kwargs: Any,  # 接收线程自身的额外参数
    ) -> SafeThread:
        """创建并启动安全线程,自动添加到管理器

        Args:
            target: 线程执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数,可包含max_retries

        Returns:
            SafeThread: 创建的安全线程实例
        """
        thread = SafeThread(
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
            max_retries=max_retries,
            retry_delay=retry_delay,
            **thread_kwargs,  # 传递线程自身的额外参数
        )

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
            timeout: 等待线程停止的最大时间（秒）,None表示无限等待
        """
        try:
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
        except Exception as e:
            mylog.error('停止所有线程失败: {}', e)
            raise  # 重新抛出异常，让调用者知道操作失败

    @classmethod
    def wait_all_completed(cls, timeout: float | None = None) -> dict[int, Any]:
        """等待所有线程完成并返回结果

        Args:
            timeout: 等待线程完成的最大时间（秒）,None表示无限等待

        Returns:
            Dict[int, Any]: 线程ID到执行结果的映射
        """
        tmp_all_results = {}

        with cls._lock:
            for thread_id, thread_ref in list(cls._threads.items()):
                try:
                    thread = thread_ref()
                    if thread is not None:
                        result = thread.get_result(timeout)
                        tmp_all_results[thread_id] = result
                    else:
                        del cls._threads[thread_id]
                except Exception as e:
                    mylog.error('获取线程结果时发生错误: {}', e)
                    tmp_all_results[thread_id] = None

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
            ThreadBase | None: 对应的线程实例，如果不存在则返回None
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
            list[ThreadBase]: 名称匹配的线程实例列表
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

        Returns:
            bool: 线程是否成功停止
        """
        thread = cls.get_thread_by_id(thread_id)
        if thread and thread.is_running():
            return thread.stop(timeout)
        return False


class SingletonThread(SingletonMixin, SafeThread):
    """单例线程类，确保同一目标函数只有一个线程实例

    特性：
    - 单例模式保证唯一性
    - 自动线程管理
    - 安全停止机制

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数，可包含max_retries
    """

    def __init__(
        self,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: tuple = (),
        kwargs: dict[str, Any] = {},
        *,
        daemon: bool | None = True,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        **thread_kwargs: Any,  # 接收线程自身的额外参数
    ):
        # 先调用SingletonMixin的初始化
        SingletonMixin.__init__(self)
        # 然后调用SafeThread的初始化
        SafeThread.__init__(
            self,
            target=target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
            max_retries=max_retries,
            retry_delay=retry_delay,
            **thread_kwargs,  # 传递线程自身的额外参数
        )

        # 确保所有必要的属性都已初始化
        if not hasattr(self, '_thread_started'):
            self._thread_started = False
        if not hasattr(self, '_is_running'):
            self._is_running = False
        if not hasattr(self, '_stop_event'):
            self._stop_event = Event()

    def restart(self) -> None:
        """重启单例线程"""
        if self._thread_started and not self.is_alive():
            # 正确的实现方式：重置实例并创建新实例
            target = self._target
            args = self._args
            kwargs = self._kwargs

            # 从管理器中移除旧线程
            ThreadManager._threads.pop(id(self), None)

            # 重置单例实例
            self.reset_instance()

            # 创建并启动新实例
            new_instance = type(self)(target, *args, **kwargs)
            new_instance.start()


class ComposedSingletonThread:
    """组合式单例线程类，确保同一目标函数只有一个线程实例

    使用组合而不是继承，避免多继承问题，提供更灵活的单例实现

    Args:
        target: 线程执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数，可包含max_retries

    Attributes:
        _instances: 存储单例实例的字典
        _lock: 线程安全锁
        _key: 单例键
        _thread: 内部线程实例
    """

    _instances: ClassVar[dict[tuple, ComposedSingletonThread]] = {}
    _lock = threading.RLock()
    _key: tuple[int, tuple, frozenset] | None = None

    def __new__(
            cls,
            target: Callable[..., Any] | None = None,
            name: str | None = None,
            args: tuple = (),
            kwargs: dict[str, Any] = {},
            *,
            daemon: bool | None = True,
            max_retries: int = 0,
            retry_delay: float = 1.0,
            **thread_kwargs: Any,  # 接收线程自身的额外参数
    ):
        # 使用目标函数ID、参数和关键字参数作为单例键
        key = (id(target), args, frozenset(kwargs.items()))

        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)
                instance._thread = SafeThread(
                    target=target,
                    name=name,
                    args=args,
                    kwargs=kwargs,
                    daemon=daemon,
                    max_retries=max_retries,
                    retry_delay=retry_delay,
                    **thread_kwargs,  # 传递线程自身的额外参数
                )
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
            timeout: 等待线程完成的最大时间（秒）,None表示无限等待

        Returns:
            线程执行的结果,如果线程执行失败则返回None
        """
        return self._thread.get_result(timeout)

    def stop(self, timeout: float | None = None) -> bool:
        """停止线程

        Args:
            timeout: 等待线程停止的最大时间（秒）,None表示无限等待

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

        当线程已结束时,创建并启动一个新的线程实例
        """
        if self._thread._thread_started and not self._thread.is_alive():
            # 创建新的线程实例
            target = self._thread._target
            args = self._thread._args
            kwargs = self._thread._kwargs

            # 从管理器中移除旧线程
            ThreadManager._threads.pop(id(self._thread), None)

            # 创建新线程
            self._thread = SafeThread(target=target, args=args, kwargs=kwargs)

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


__all__ = ['ComposedSingletonThread', 'SafeThread', 'SingletonThread', 'ThreadBase', 'ThreadManager']