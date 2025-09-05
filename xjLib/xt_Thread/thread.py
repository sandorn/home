# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-29 11:40:57
FilePath     : /CODE/xjLib/xt_thread/thread.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import builtins
import threading
import weakref
from functools import wraps
from threading import Event, Lock, Thread
from time import sleep
from typing import Any, Callable, Dict, List, Optional

from wrapt import ObjectProxy
from xt_wraps import SingletonMixin


class ThreadSafeWraps(ObjectProxy):
    """线程安全装饰器（支持实例方法和静态方法）

    :param wrapped: 被装饰的可调用对象
    :example:
        @ThreadSafe
        def critical_func():
            ...
    """

    def __init__(self, wrapped: Callable[..., Any]) -> None:
        super().__init__(wrapped)

    def __call__(self, *args, **kwargs):
        if self.__wrapped__.__module__ == builtins.__name__:  # 判断内置函数
            with Lock():
                return self.__wrapped__(*args, **kwargs)
        else:
            if not hasattr(self, "__lock__"):
                self.__lock__ = Lock()
            with self.__lock__:
                return self.__wrapped__(*args, **kwargs)  # 普通函数和类方法
            
def thread_safe(func):
    """线程安全化，装饰函数和类方法"""
    if func.__module__ == builtins.__name__:  # 判断内置函数

        def wrapper(*args, **kwargs):
            with Lock():
                return func(*args, **kwargs)
    else:

        def wrapper(*args, **kwargs):
            if not hasattr(func, "__lock__"):
                func.__lock__ = Lock()
            with func.__lock__:
                return func(*args, **kwargs)  # 普通函数和类方法

    return wrapper

thread_print = thread_safe(print)

ThreadSafe = ThreadSafeWraps

class ThreadBase(Thread):
    """
    增强型线程基类，提供结果获取、安全停止和资源清理功能
    """

    def __init__(self, target: Callable, *args, **kwargs):
        super().__init__(
            target=target, name=target.__name__, args=args, kwargs=kwargs, daemon=True
        )
        self._is_running = True
        self._result = None
        self._exception = None
        self._stop_event = Event()
        self._thread_started = False

    def __enter__(self):
        """上下文管理器入口"""
        if not self._thread_started:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.is_running():
            self.stop()
        return False  # 不抑制异常

    def start(self) -> None:
        """启动线程"""
        if not self._thread_started:
            super().start()
            self._thread_started = True

    def get_result(self, timeout: Optional[float] = None) -> Any:
        """获取线程执行结果，等待线程完成"""
        if not self._thread_started:
            raise RuntimeError(
                "Cannot get result from a thread that hasn't been started"
            )

        try:
            self.join(timeout)
            return self._result
        except Exception as e:
            thread_print(f"获取线程结果失败: {e}")
            return None

    def stop(self, timeout: Optional[float] = None) -> bool:
        """安全停止线程"""
        if self._is_running:
            self._is_running = False
            self._stop_event.set()

            if timeout is not None and self.is_alive():
                self.join(timeout)

            thread_print(f"线程 {self.name} 已停止")
            return True
        return False

    def is_running(self) -> bool:
        """检查线程是否正在运行"""
        return self._is_running and self.is_alive()

    def run(self) -> None:
        """线程主执行方法"""
        try:
            if not self._stop_event.is_set():
                self._result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            thread_print(f"线程 {self.name} 执行失败: {e}")
            self._exception = e
            self._result = None
        finally:
            self._is_running = False

    def __del__(self):
        """对象销毁时自动清理资源"""
        if self.is_running():
            self.stop(timeout=1.0)


class SafeThread(ThreadBase):
    """
    安全线程类，提供异常捕获和重试机制

    适用于需要异常处理和重试的任务

    Usage:
        def risky_task():
            # 可能失败的任务
            if random.random() < 0.3:
                raise ValueError("随机失败")
            return "成功"

        thread = SafeThread(risky_task, max_retries=3)
        thread.start()
    """

    def __init__(self, target: Callable, *args, max_retries: int = 0, **kwargs):
        super().__init__(target, *args, **kwargs)
        self.max_retries = max_retries
        self.retry_count = 0

    def run(self) -> None:
        """重写run方法，添加重试机制"""
        while self.retry_count <= self.max_retries and not self._stop_event.is_set():
            try:
                self._result = self._target(*self._args, **self._kwargs)
                break  # 成功执行，退出循环
            except Exception as e:
                self.retry_count += 1
                if self.retry_count > self.max_retries:
                    thread_print(
                        f"安全线程 {self.name} 执行失败，已达最大重试次数: {e}"
                    )
                    self._exception = e
                    break
                else:
                    thread_print(
                        f"安全线程 {self.name} 第 {self.retry_count} 次重试: {e}"
                    )
                    sleep(1)  # 等待一段时间后重试
            finally:
                self._is_running = False


class ThreadManager(SingletonMixin):
    """
    线程管理器，用于管理所有线程实例
    """

    _threads: Dict[int, weakref.ref] = {}
    _lock = threading.RLock()
    def __init__(self): 
        """初始化线程管理器"""
        super().__init__()
        
    @classmethod
    def create_thread(cls, target: Callable, *args, **kwargs) -> ThreadBase:
        """创建并启动线程，自动添加到管理器"""
        thread = ThreadBase(target, *args, **kwargs)
        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

        thread.start()
        return thread

    @classmethod
    def create_safe_thread(cls, target: Callable, *args, **kwargs) -> SafeThread:
        """创建并启动安全线程，自动添加到管理器"""
        thread = SafeThread(target, *args, **kwargs)

        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

        thread.start()
        return thread

    @classmethod
    def add_thread(cls, thread: ThreadBase) -> None:
        """将已存在的线程添加到管理器"""
        with cls._lock:
            cls._threads[id(thread)] = weakref.ref(thread)

    @classmethod
    def stop_all(cls, timeout: Optional[float] = None) -> None:
        """停止所有管理的线程"""
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
    def wait_all_completed(cls, timeout: Optional[float] = None) -> Dict[int,Any]:
        """等待所有线程完成并返回结果"""
        _all_results = {}

        with cls._lock:
            for thread_id, thread_ref in list(cls._threads.items()):
                thread = thread_ref()
                if thread is not None:
                    result = thread.get_result(timeout)
                    _all_results[thread_id] = result
                else:
                    del cls._threads[thread_id]

        with cls._lock:
            cls._threads.clear()

        return _all_results

    @classmethod
    def get_active_count(cls) -> int:
        """获取当前活动的线程数量"""
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
    def get_thread_by_id(cls, thread_id: int) -> Optional[ThreadBase]:
        """根据ID获取线程实例"""
        with cls._lock:
            thread_ref = cls._threads.get(thread_id)
            return thread_ref() if thread_ref else None

    @classmethod
    def get_thread_by_name(cls, name: str) -> List[ThreadBase]:
        """根据名称获取线程实例列表"""
        result = []
        with cls._lock:
            for thread_ref in cls._threads.values():
                thread = thread_ref()
                if thread and thread.name == name:
                    result.append(thread)
        return result

    @classmethod
    def stop_thread(cls, thread_id: int, timeout: Optional[float] = None) -> bool:
        """停止指定线程"""
        thread = cls.get_thread_by_id(thread_id)
        if thread and thread.is_running():
            return thread.stop(timeout)
        return False


class SingletonThread(SingletonMixin, SafeThread):
    """
    单例线程类，确保同一目标函数只有一个线程实例

    Features:
    - 单例模式保证唯一性
    - 自动线程管理
    - 安全停止机制
    """

    def __init__(self, target: Callable, *args, **kwargs):
        # 先调用SingletonMixin的初始化
        SingletonMixin.__init__(self)
        # 然后调用SafeThread的初始化
        SafeThread.__init__(self, target, *args, **kwargs)

        # 确保所有必要的属性都已初始化
        if not hasattr(self, "_thread_started"):
            self._thread_started = False
        if not hasattr(self, "_is_running"):
            self._is_running = True
        if not hasattr(self, "_stop_event"):
            self._stop_event = Event()

    def start(self) -> None:
        """启动线程，但只允许启动一次"""
        if not self._thread_started:
            super().start()

    def restart(self) -> None:
        """重启单例线程"""
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


class SingletonThread2:
    """
    单例线程类，确保同一目标函数只有一个线程实例

    使用组合而不是继承，避免多继承问题
    """

    _instances = {}
    _lock = threading.RLock()

    def __new__(cls, target: Callable, *args, **kwargs):
        # 使用目标函数作为单例键
        key = (id(target), args, frozenset(kwargs.items()))

        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)
                instance._thread = SafeThread(target, *args, **kwargs)
                instance._key = key
                cls._instances[key] = instance
            return cls._instances[key]

    def __init__(self, target: Callable, *args, **kwargs):
        # 防止重复初始化
        if not hasattr(self, "_initialized"):
            self._initialized = True

    def start(self) -> None:
        """启动线程"""
        self._thread.start()

    def get_result(self, timeout: Optional[float] = None) -> Any:
        """获取线程执行结果"""
        return self._thread.get_result(timeout)

    def stop(self, timeout: Optional[float] = None) -> bool:
        """停止线程"""
        return self._thread.stop(timeout)

    def is_running(self) -> bool:
        """检查线程是否正在运行"""
        return self._thread.is_running()

    def restart(self) -> None:
        """重启单例线程"""
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

# 便捷函数
def run_in_thread(func: Callable) -> Callable:
    """
    装饰器，将函数在单独线程中执行

    Usage:
        @run_in_thread
        def long_running_task(param):
            # 长时间运行的任务
            return result

        # 调用方式不变，但会在线程中执行
        result = long_running_task(param)
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> ThreadBase:
        thread = ThreadManager.create_thread(func, *args, **kwargs)
        return thread

    return wrapper


# 示例用法
if __name__ == "__main__":
    # 示例函数
    def sample_task(seconds: int, task_id: int) -> str:
        """示例任务函数，模拟耗时操作"""
        thread_print(f"任务 {task_id} 开始，需要 {seconds} 秒")
        sleep(seconds)
        result = f"任务 {task_id} 完成"
        thread_print(result)
        return result

    # 测试线程管理
    thread_print("=== 测试线程管理 [DEBUG] ===")
    # 创建多个线程
    threads = []
    for i in range(3):
        thread = ThreadManager.create_thread(sample_task, 1, i)  # 减少等待时间
        threads.append(thread)

    thread_print(f"活动线程数: {ThreadManager.get_active_count()}")

    # 等待所有线程完成
    results = ThreadManager.wait_all_completed()
    thread_print(f"所有线程完成，结果: {results}")

    # 测试装饰器
    thread_print("\n=== 测试线程装饰器 ===")

    @run_in_thread
    def decorated_task(x: int) -> int:
        """被装饰的任务函数"""
        thread_print(f"装饰器任务开始: {x}")
        sleep(1)
        result = x * 2
        thread_print(f"装饰器任务完成: {result}")
        return result

    # 调用被装饰的函数
    thread = decorated_task(5)
    result = thread.get_result()
    thread_print(f"装饰器任务结果: {result}")

    # 测试单例线程
    thread_print("\n=== 测试单例线程 ===")

    def singleton_task():
        """单例任务函数"""
        thread_print("单例任务执行中")
        sleep(1)
        return "单例任务完成"

    # 创建单例线程
    thread1 = SingletonThread(singleton_task)
    thread2 = SingletonThread(singleton_task)

    thread_print(f"线程1和线程2是同一个实例: {thread1 is thread2}")

    # 确保线程已启动
    thread1.start()
    thread2.start()

    # 等待完成
    result1 = thread1.get_result()
    result2 = thread2.get_result()
    thread_print(f"线程1结果: {result1}, 线程2结果: {result2}")
    # 测试重启功能
    thread_print("\n=== 测试重启功能 ===")
    thread1.restart()
    result3 = thread1.get_result()
    thread_print(f"重启后结果: {result3}")
    # 测试上下文管理器
    thread_print("\n=== 测试上下文管理器 ===")

    def context_task():
        sleep(0.5)
        return "上下文任务完成"

    with ThreadBase(context_task) as thread:
        result = thread.get_result()
        thread_print(f"上下文管理器结果: {result}")
