# !/usr/bin/env python
"""
==============================================================
Description  : PyQt6线程增强模块 - 提供安全、可靠的Qt线程封装和管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-06 17:36:20
FilePath     : /CODE/xjLib/xt_thread/qthread.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- QtThreadBase：基于QThread的增强型线程基类，提供结果获取、安全停止和异常处理
- QtSafeThread：安全线程类，集成异常捕获和重试机制
- QtThreadManager：线程管理器，提供全局线程跟踪和批量操作
- SingletonQtThread：单例线程类，确保同一目标函数只有一个线程实例
- ComposedSingletonQtThread：组合式单例线程类，使用组合而非继承实现
- run_in_qtthread：装饰器，将函数在QThread中执行

主要特性：
- 提供完整的线程生命周期管理
- 支持异步结果获取和超时控制
- 内置异常处理和信号通知机制
- 上下文管理器支持，简化线程使用
- 线程安全的单例模式实现
- 批量线程创建、等待和停止功能
==============================================================
"""

from __future__ import annotations

import contextlib
import time
import weakref
from collections.abc import Callable
from typing import Any, ClassVar, TypeVar, cast

from PyQt6.QtCore import (
    QMutex,
    QMutexLocker,
    QThread,
    QWaitCondition,
    pyqtSignal,
)
from xt_wraps.singleton import SingletonMixin

# 类型定义
T = TypeVar('T')


class QtThreadBase(QThread):
    """
    基于QThread的增强型线程基类

    提供结果获取、安全停止、自动资源清理和异常处理功能

    Signals:
        finished_signal: 线程完成时发射，携带执行结果
        error_signal: 线程发生错误时发射，携带异常信息
    """

    finished_signal = pyqtSignal(object)  # 线程完成信号，携带结果
    error_signal = pyqtSignal(Exception)  # 错误信号，携带异常

    def __init__(self, target: Callable, *args, daemon: bool = True, **kwargs):
        """
        初始化线程

        Args:
            target: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数
        """
        self.callback = kwargs.pop('callback', None)
        super().__init__()
        # 设置线程名称
        self.setObjectName(target.__name__)
        # 设置守护线程
        self.daemon = daemon

        # 保存目标函数和参数
        self._target = target
        self._args = args
        self._kwargs = kwargs

        self._result = None
        self._exception = None
        self._is_running = False
        self._stop_requested = False
        self._thread_started = False
        self._mutex = QMutex()
        self._condition = QWaitCondition()
        # 连接信号
        self.finished.connect(self._on_finished)

    def _on_finished(self) -> None:
        """线程完成时的处理"""
        self.finished_signal.emit(self)

    def __enter__(self):
        """上下文管理器入口"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
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
        """线程主执行方法"""
        self._is_running = True

        try:
            if not self._stop_requested:
                self._result = self._target(*self._args, **self._kwargs)
                if callable(self.callback):
                    self._result = cast(T, self.callback(self._result))
        except Exception as e:
            self._exception = e
            self.error_signal.emit(e)
        finally:
            self._is_running = False

    def get_result(self, timeout: float | None = None) -> Any:
        """
        获取线程执行结果，等待线程完成

        Args:
            timeout: 超时时间（秒），None表示无限等待

        Returns:
            线程执行结果，如果超时或出错返回None
        """
        # 等待线程完成
        if self.isRunning() or self._is_running:
            if timeout is not None:
                wait_time = int(timeout * 1000)  # 转换为毫秒
                success = self.wait(wait_time)
            else:
                success = self.wait()
        else:
            success = True

        return self._result if success else None

    def stop(self, timeout: float | None = None) -> bool:
        """
        安全停止线程

        Args:
            timeout: 等待线程停止的超时时间（秒）

        Returns:
            bool: 是否成功停止线程
        """
        if self._is_running:
            self._stop_requested = True

            # 请求线程退出
            self.quit()

            # 等待线程实际停止
            if timeout is not None:
                wait_time = int(timeout * 1000)  # 转换为毫秒
                return self.wait(wait_time)
            return self.wait()

        return True

    def is_running(self) -> bool:
        """检查线程是否正在运行"""
        try:
            return self._is_running or (self.isRunning() if hasattr(self, 'isRunning') else False)
        except RuntimeError:
            # 处理Qt对象已被销毁的情况
            return False

    def get_exception(self) -> Exception | None:
        """获取线程执行过程中的异常"""
        return self._exception

    def __del__(self):
        """对象销毁时自动清理资源"""
        if hasattr(self, 'is_running') and hasattr(self, 'stop') and self.is_running():
            with contextlib.suppress(Exception):
                self.stop(timeout=1.0)


class QtSafeThread(QtThreadBase):
    """
    安全线程类，提供异常捕获和重试机制

    适用于需要异常处理和重试的任务，确保关键操作的可靠性

    Args:
        target: 要执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数
        max_retries: 最大重试次数，默认0（不重试）
        retry_delay: 重试间隔时间（秒），默认1.0

    Example:
        >>> def risky_task():
        >>> # 可能失败的任务
        >>>     if random.random() < 0.3:
        >>>         raise ValueError("随机失败")
        >>>     return "成功"
        >>>
        >>> thread = QtSafeThread(risky_task, max_retries=3)
        >>> thread.start()
        >>> result = thread.get_result()
    """

    def __init__(
        self,
        target: Callable,
        *args,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        daemon: bool = True,
        **kwargs,
    ):
        """
        初始化安全线程

        Args:
            target: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数
            max_retries: 最大重试次数，默认0（不重试）
            retry_delay: 重试间隔时间（秒），默认1.0
        """
        super().__init__(target, *args, daemon=daemon, **kwargs)
        self.max_retries = max_retries
        self.retry_count = 0
        self.retry_delay = retry_delay  # 重试延迟（秒）

    def run(self) -> None:
        """重写run方法，添加重试机制"""
        self._is_running = True

        try:
            while self.retry_count <= self.max_retries and not self._stop_requested:
                try:
                    self._result = self._target(*self._args, **self._kwargs)
                    if callable(self.callback):
                        self._result = cast(T, self.callback(self._result))
                    break  # 成功执行，退出循环
                except Exception as e:
                    self.retry_count += 1
                    if self.retry_count > self.max_retries:
                        self._exception = e
                        self.error_signal.emit(e)
                        break
                    time.sleep(self.retry_delay)
        finally:
            self._is_running = False


class QtThreadManager(SingletonMixin):
    """
    QThread 线程管理器，用于管理所有线程实例

    Features:
    - 全局线程跟踪
    - 批量停止和等待
    - 结果收集
    - 线程安全
    """

    _threads: ClassVar[dict[int, weakref.ref]] = {}
    _mutex = QMutex()

    def __init__(self):
        """初始化线程管理器"""
        super().__init__()

    @classmethod
    def create_thread(cls, target: Callable, *args, **kwargs) -> QtThreadBase:
        """
        创建并启动线程，自动添加到管理器

        Args:
            target: 要执行的函数
            *args: 函数参数
            *kwargs: 函数关键字参数

        Returns:
            创建的线程实例
        """
        tmp_thread = QtThreadBase(target, *args, **kwargs)

        with QMutexLocker(cls._mutex):
            cls._threads[id(tmp_thread)] = weakref.ref(tmp_thread)

        tmp_thread.start()
        return tmp_thread

    @classmethod
    def create_safe_thread(cls, target: Callable, *args, **kwargs) -> QtSafeThread:
        """
        创建并启动安全线程，自动添加到管理器

        Args:
            target: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数

        Returns:
            创建的安全线程实例
        """
        thread = QtSafeThread(target, *args, **kwargs)

        with QMutexLocker(cls._mutex):
            cls._threads[id(thread)] = weakref.ref(thread)

        thread.start()
        return thread

    @classmethod
    def add_thread(cls, thread: QtThreadBase | QtSafeThread) -> None:
        """
        将已存在的线程添加到管理器

        Args:
            thread: 要添加的线程实例
        """
        with QMutexLocker(cls._mutex):
            cls._threads[id(thread)] = weakref.ref(thread)

    @classmethod
    def stop_all(cls, timeout: float | None = None) -> None:
        """
        停止所有管理的线程

        Args:
            timeout: 等待每个线程停止的超时时间（秒）
        """
        with QMutexLocker(cls._mutex):
            threads_to_stop = []
            # 收集所有有效的线程引用
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None and thread.is_running():
                    threads_to_stop.append(thread)
                else:
                    # 清理无效引用
                    del cls._threads[thread_id]

            # 停止所有线程
            for thread in threads_to_stop:
                thread.stop(timeout)

            # 清理所有引用
            cls._threads.clear()

    @classmethod
    def wait_all_completed(cls, timeout: float | None = None) -> dict[int, Any]:
        """
        等待所有线程完成并返回结果

        Args:
            timeout: 等待所有线程完成的超时时间（秒）

        Returns:
            所有线程的结果字典，键为线程ID，值为结果
        """
        # 创建一个字典来存储所有线程的结果
        tmp_results = {}

        # 获取当前时间，用于计算超时
        start_time = time.time()

        # 复制当前所有的线程引用，以便在等待过程中不会丢失
        thread_list = []
        with QMutexLocker(cls._mutex):
            for thread_ref in cls._threads.values():
                thread = thread_ref()
                if thread is not None:
                    thread_list.append(thread)

        # 等待所有线程完成并直接从每个线程获取结果
        for thread in thread_list:
            # 等待线程完成，但不依赖get_result()方法
            while thread.is_running():
                # 检查是否超时
                if timeout is not None and time.time() - start_time > timeout:
                    break
                # 短暂休眠
                time.sleep(0.01)

            # 直接从线程实例获取结果
            thread_id = id(thread)
            tmp_results[thread_id] = thread._result

        # 清空并返回结果
        with QMutexLocker(cls._mutex):
            cls._threads.clear()

        return tmp_results

    @classmethod
    def get_active_count(cls) -> int:
        """
        获取当前活动的线程数量

        Returns:
            当前活动的线程数量
        """
        with QMutexLocker(cls._mutex):
            count = 0
            # 清理已经结束的线程引用
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None and thread.is_running():
                    count += 1
                else:
                    del cls._threads[thread_id]
            return count

    @classmethod
    def get_thread_by_id(cls, thread_id: int) -> QtThreadBase | None:
        """
        根据ID获取线程实例

        Args:
            thread_id: 线程ID

        Returns:
            线程实例，如果不存在返回None
        """
        with QMutexLocker(cls._mutex):
            thread_ref = cls._threads.get(thread_id)
            return thread_ref() if thread_ref else None

    @classmethod
    def get_thread_by_name(cls, name: str) -> list[QtThreadBase]:
        """
        根据名称获取线程实例列表

        Args:
            name: 线程名称

        Returns:
            匹配名称的线程实例列表
        """
        result = []
        with QMutexLocker(cls._mutex):
            for thread_ref in cls._threads.values():
                thread = thread_ref()
                if thread and thread.objectName() == name:
                    result.append(thread)
        return result

    @classmethod
    def stop_thread(cls, thread_id: int, timeout: float | None = None) -> bool:
        """
        停止指定线程

        Args:
            thread_id: 线程ID
            timeout: 等待线程停止的超时时间（秒）

        Returns:
            bool: 是否成功停止线程
        """
        thread = cls.get_thread_by_id(thread_id)
        if thread and thread.is_running():
            return thread.stop(timeout)
        return False


class SingletonQtThread(SingletonMixin, QtSafeThread):
    """
    单例线程类，使用继承方式实现，确保同一目标函数只有一个线程实例

    通过继承SingletonMixin和QtSafeThread实现单例模式，适用于需要简单实现单例线程的场景

    Args:
        target: 要执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数

    Features:
    - 单例模式保证唯一性
    - 自动线程管理
    - 安全停止机制
    - 异常捕获和重试功能

    Example:
        >>> def singleton_task(param):
        >>> # 单例任务函数
        >>>     time.sleep(1)
        >>>     return f"结果: {param}"
        >>>
        >>> thread1 = SingletonQtThread(singleton_task, '参数1')
        >>> thread2 = SingletonQtThread(singleton_task, '参数2')
        >>> print(thread1 is thread2)  # 输出: True
        >>> result = thread1.get_result()
    """

    def __init__(self, target: Callable, *args, **kwargs):
        """
        初始化单例线程

        Args:
            target: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数
        """
        # 让SingletonMixin来管理单例实例
        super().__init__(target, *args, **kwargs)

        # 确保所有必要的属性都已初始化
        if not hasattr(self, '_is_running'):
            self._is_running = False
        if not hasattr(self, '_stop_requested'):
            self._stop_requested = False
        if not hasattr(self, '_result'):
            self._result = None

        # 只在新实例创建时自动启动
        if not self.isRunning() and not self._is_running:
            self.start()

    def restart(self) -> None:
        """重启单例线程"""
        if self.isRunning() or self._is_running:
            # 先停止当前线程
            self.stop()

            # 重置状态
            self._is_running = False
            self._stop_requested = False
            # 不重置_result，保留最后一次执行的结果
            # self._result = None
            self._exception = None
            self.retry_count = 0

            # 重新启动
            self.start()


class ComposedSingletonQtThread(SingletonMixin):
    """
    组合式单例线程类，使用组合而非继承的方式实现单例线程

    通过内部持有QtSafeThread实例来实现线程功能，避免多继承问题，提供更灵活的单例实现

    Args:
        target: 要执行的目标函数
        *args: 传递给目标函数的位置参数
        **kwargs: 传递给目标函数的关键字参数

    Features:
    - 单例模式保证唯一性
    - 组合式设计避免多继承问题
    - 安全停止机制
    - 异常捕获和重试功能
    - 灵活的重启机制

    Example:
        >>> def singleton_task(param):
        >>> # 单例任务函数
        >>>     time.sleep(1)
        >>>     return f"结果: {param}"
        >>>
        >>> thread1 = ComposedSingletonQtThread(singleton_task, '参数1')
        >>> thread2 = ComposedSingletonQtThread(singleton_task, '参数2')
        >>> print(thread1 is thread2)  # 输出: True
        >>> result = thread1.get_result()
    """

    _instances: ClassVar[dict[Callable, Any]] = {}
    _mutex = QMutex()

    def __new__(cls, target: Callable, *args, **kwargs):
        """\创建或返回已存在的单例实例"""
        with QMutexLocker(cls._mutex):
            # 只使用target函数作为键，忽略args和kwargs
            if target not in cls._instances:
                cls._instances[target] = super().__new__(cls)
                # 初始化线程对象（仅在创建新实例时）
                cls._instances[target]._initialize(target, *args, **kwargs)
        return cls._instances[target]

    def _initialize(self, target: Callable, *args, **kwargs):
        """初始化线程实例的内部状态"""
        self._thread = QtSafeThread(target, *args, **kwargs)
        self._thread.finished_signal.connect(self._on_thread_finished)
        self._thread.error_signal.connect(self._on_thread_error)
        self._target = target

        # 自动启动线程
        self.start()

    def _on_thread_finished(self):
        """线程完成信号处理"""
        # 可以在这里添加自定义处理逻辑
        pass

    def _on_thread_error(self, exception):
        """线程错误信号处理"""
        # 可以在这里添加自定义错误处理逻辑
        pass

    def start(self) -> None:
        """启动内部线程"""
        if not self._thread.isRunning() and not self._thread._is_running:
            self._thread.start()

    def get_result(self, timeout: float | None = None) -> Any:
        """获取线程执行结果"""
        return self._thread.get_result(timeout)

    def stop(self, timeout: float | None = None) -> bool:
        """停止内部线程"""
        return self._thread.stop(timeout)

    def restart(self) -> None:
        """重启单例线程"""
        self.stop()
        # 创建新的线程实例
        self._thread = QtSafeThread(self._target, *self._thread._args, **self._thread._kwargs)
        self._thread.finished_signal.connect(self._on_thread_finished)
        self._thread.error_signal.connect(self._on_thread_error)
        self.start()

    def is_running(self) -> bool:
        """检查线程是否正在运行"""
        return self._thread.is_running()

    def __getattr__(self, name: str):
        """将未找到的属性委托给内部线程实例"""
        # 委托给内部线程对象
        return getattr(self._thread, name)

    @classmethod
    def clear_instances(cls) -> None:
        """清理所有单例实例，通常只在测试或特殊情况下使用"""
        with QMutexLocker(cls._mutex):
            for instance in cls._instances.values():
                if hasattr(instance, '_thread'):
                    instance.stop()
            cls._instances.clear()
