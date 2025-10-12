"""
==============================================================
Description  : 线程池增强模块 - 提供多种线程池实现及异步任务处理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
LastEditTime : 2024-10-11 22:36:00
Github       : https://github.com/sandorn/nsthread

本模块提供以下核心功能：
- BaseThreadPool: 基础线程池实现,支持基本的任务提交和线程管理
- DynamicThreadRunner: 动态调整的线程池,可根据系统资源和任务队列自动扩展或收缩
- ThreadPoolManager: 全局线程池单例管理,适用于多模块共享线程池资源
- EnhancedThreadPool: 增强型线程池,提供任务结果收集和统一的异常处理机制
- AsyncThreadPool: 异步线程池,利用asyncio.loop实现异步任务执行和结果获取
- FutureThreadPool: 基于asyncio.run的线程池,侧重异步任务一次性执行

主要特性：
- 支持任务提交、结果收集和异常处理
- 动态调整线程数量,优化资源利用率
- 线程池单例管理,避免资源浪费
- 提供上下文管理器支持,确保资源正确释放
- 支持同步执行和异步结果获取
- 丰富的API接口,满足不同场景下的线程池使用需求
==============================================================
"""

from __future__ import annotations

import asyncio
import contextlib
import functools
import os
import queue
import time
from asyncio.tasks import ALL_COMPLETED, FIRST_COMPLETED
from collections.abc import Callable, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from queue import Queue
from threading import Lock, Semaphore, current_thread
from typing import Any, Self

import psutil

from .exception import handle_exception, safe_call
from .thread import SafeThread, ThreadBase, ThreadManager as ThreadInstanceManager

# 定义任务参数类型别名，支持两种格式：
# - 简单格式：单个参数值 (Any)
# - 复杂格式：包含位置参数元组和关键字参数字典的元组 ((args_tuple), {kwargs_dict})
TaskParams = Any | tuple[tuple[Any, ...], dict[str, Any]]


@dataclass
class PoolConfig:
    """线程池配置类"""

    max_workers: int = 0  # 0表示自动计算
    thread_name_prefix: str = 'ThreadPool'
    queue_size: int = 100
    min_workers: int = 2
    exception_handler: Callable[[Exception], None] | None = None
    monitor_interval: float = 2.0  # 监控间隔
    shutdown_timeout: float = 5.0  # 关闭超时时间


class BaseThreadRunner:
    """极简线程池实现

    提供最基础的线程池功能，使用信号量控制并发线程数量。
    适用于简单场景下的任务并发执行，不提供高级功能如结果收集和异常处理。
    """

    def __init__(self, max_workers: int = 10):
        """初始化线程池

        Args:
            max_workers: 最大工作线程数
        """
        self.max_workers = max_workers
        self._semaphore = Semaphore(max_workers)
        self._threads: list[ThreadBase] = []

    def submit(self, target: Callable, *args: Any, **kwargs: Any) -> ThreadBase:
        """提交任务到线程池

        Args:
            target: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        Returns:
            ThreadBase: 创建的线程对象

        Note:
            此方法会阻塞直到有可用的线程资源
        """
        # 等待信号量，确保不超过最大线程数
        self._semaphore.acquire()

        # 创建线程
        thread = ThreadBase(target=target, args=args, kwargs=kwargs)

        # 重写完成逻辑，确保线程结束后释放信号量
        original_run = thread.run

        def wrapped_run():
            try:
                original_run()
            finally:
                self._semaphore.release()

        thread.run = wrapped_run
        thread.start()
        self._threads.append(thread)

        return thread

    @property
    def active_threads(self) -> int:
        """获取当前活跃线程数

        Returns:
            int: 当前正在运行的线程数量

        Note:
            此实现直接统计活跃线程数，不依赖于Semaphore的内部属性
        """
        # 统计仍在运行的线程数量
        return sum(1 for thread in self._threads if thread.is_alive())

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池

        Args:
            wait: 是否等待所有线程完成执行

        Note:
            调用此方法后，线程池将不再接受新任务
        """
        if not wait:
            return

        for thread in self._threads:
            if thread.is_alive():
                thread.join()


class DynamicThreadRunner:
    """动态调整的线程池实现

    根据系统资源使用情况和任务队列状态自动调整工作线程数量,适用于负载波动较大的场景。
    支持自动扩缩容以适应不同的任务负载,同时提供资源监控和异常处理机制。

    参数:
        min_workers: 最小工作线程数（保持活跃）
        max_workers: 最大工作线程数（根据负载自动调整）
        queue_size: 任务队列最大容量

    使用示例:
        with DynamicThreadPool(min_workers=2, max_workers=20) as pool:
            for i in range(100):
                pool.submit(process_task, i)
    """

    def __init__(self, min_workers: int = 2, max_workers: int = 10, queue_size: int = 100, config: PoolConfig | None = None) -> None:
        """初始化动态调整的线程池

        Args:
            min_workers: 最小工作线程数（即使没有任务也保持活跃）
            max_workers: 最大工作线程数（根据负载自动调整）
            queue_size: 任务队列最大容量
        """
        self.config = config or PoolConfig()
        # 使用 self.config.max_workers 等
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.task_queue = Queue(maxsize=queue_size)
        self.workers = []
        self.is_running = True
        self.lock = Lock()

        # 启动监控线程，负责动态调整线程数
        self.monitor = SafeThread(target=self._monitor_resources)
        self.monitor.daemon = True  # 设置为守护线程,主程序结束时自动退出
        self.monitor.start()
        ThreadInstanceManager.add_thread(self.monitor)

        # 启动初始工作线程
        self._adjust_worker_count(min_workers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """上下文管理器退出时安全关闭线程池

        参数:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常追踪信息
        """
        self.shutdown(wait=True)

    @safe_call(re_raise=False)
    def _monitor_resources(self) -> None:
        """监控系统资源和任务队列,动态调整线程数

        每隔2秒检查一次系统CPU使用率和任务队列状态，根据以下策略调整线程数：
        - 当队列积压且CPU资源充足时增加线程
        - 当任务较少且线程数超过最小值时减少线程

        Exception Handling:
            捕获所有异常并通过handle_exception处理，确保监控线程不会意外终止
        """
        while self.is_running:
            try:
                cpu_percent = psutil.cpu_percent()
                queue_size = self.task_queue.qsize()
                current_workers = len(self.workers)

                with self.lock:
                    if queue_size > current_workers * 2 and cpu_percent < 80:
                        # 队列积压且CPU资源充足,增加线程
                        self._adjust_worker_count(min(current_workers + 2, self.max_workers))
                    elif queue_size < current_workers and current_workers > self.min_workers:
                        # 任务较少,减少线程
                        self._adjust_worker_count(max(current_workers - 1, self.min_workers))
            except Exception as exc:
                handle_exception(exc=exc, custom_message='DynamicThreadPool._monitor_resources')

            time.sleep(2)  # 监控间隔

    def _adjust_worker_count(self, target_count: int) -> None:
        """调整工作线程数量

        Args:
            target_count: 目标工作线程数量

        Operations:
            - 当目标数量大于当前数量时，创建并启动新的工作线程
            - 当目标数量小于当前数量时，向任务队列发送退出信号
        """
        with self.lock:
            current_count = len(self.workers)
            if target_count > current_count:
                # 增加工作线程
                for _ in range(target_count - current_count):
                    worker = SafeThread(target=self._worker_loop)
                    worker.daemon = True  # 设置为守护线程
                    worker.start()
                    ThreadInstanceManager.add_thread(worker)
                    self.workers.append(worker)
            elif target_count < current_count:
                # 标记多余的工作线程退出
                for _ in range(current_count - target_count):
                    self.task_queue.put(None)

    @safe_call(re_raise=False)
    def _worker_loop(self) -> None:
        """工作线程主循环

        持续从任务队列获取任务并执行，直到接收到退出信号或线程池关闭且队列为空。

        Task Processing Flow:
            1. 从队列获取任务(带1秒超时)
            2. 检查是否为退出信号(None)
            3. 执行任务并处理可能的异常
            4. 标记任务完成

        Exception Handling:
            - 捕获queue.Empty异常继续循环
            - 捕获任务执行异常并通过handle_exception处理
        """
        cur_thread = current_thread()
        while self.is_running or not self.task_queue.empty():
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:  # 退出信号
                    # 安全地移除线程，使用 contextlib.suppress 避免竞态条件
                    with self.lock, contextlib.suppress(ValueError):
                        self.workers.remove(cur_thread)
                    break

                func, args, kwargs = task
                try:
                    func(*args, **kwargs)
                except Exception as exc:
                    handle_exception(exc=exc, custom_message='DynamicThreadPool._worker_loop')
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """提交任务到线程池

        Args:
            func: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        Raises:
            RuntimeError: 当线程池已关闭时抛出

        Note:
            如果任务队列已满，此方法会阻塞直到队列有空间
        """
        if not self.is_running:
            raise RuntimeError('线程池已关闭')
        self.task_queue.put((func, args, kwargs))

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池

        Args:
            wait: 是否等待所有任务完成

        Operation Flow:
            1. 停止接受新任务
            2. 如果wait=True:
                - 等待队列处理完毕
                - 等待所有工作线程完成当前任务
                - 发送终止信号给工作线程
                - 等待工作线程终止
            3. 清空工作线程列表
        """
        self.is_running = False  # 先停止接受新任务
        if wait:
            # 等待队列处理完毕
            while not self.task_queue.empty():
                time.sleep(0.1)
            # 等待所有工作线程完成当前任务
            self.task_queue.join()
            # 发送终止信号给工作线程
            with self.lock:
                for _ in range(len(self.workers)):
                    self.task_queue.put(None)
                # 等待线程终止
                for worker in self.workers[:]:  # 使用副本避免迭代中修改
                    if worker.is_alive():
                        worker.join(1)  # 设置超时避免永久阻塞
        # 清空工作线程列表
        self.workers.clear()


class ThreadPoolManager:
    """全局线程池单例管理

    提供线程池实例的统一管理,避免重复创建线程池资源,适用于多模块共享线程池的场景。
    确保在整个应用程序生命周期内,相同配置的线程池只被创建一次。

    使用示例:
        with ThreadPoolManager.get_pool() as executor:
            future = executor.submit(task_function, args)

        # 或者直接提交任务
        future = ThreadPoolManager.get_pool().submit(task_function, args)
    """

    _instance: ThreadPoolExecutor | None = None
    _lock = Lock()

    @classmethod
    def get_pool(cls, max_workers: int | None = None, wait: bool = True) -> ThreadPoolExecutor:
        """获取线程池实例

        Args:
            max_workers: None-自动计算(IO密集型推荐),具体数值适用于CPU密集型任务
            wait: 关闭旧线程池时是否等待任务完成

        Returns:
            ThreadPoolExecutor: 线程池实例
        """
        with cls._lock:
            # 计算实际使用的max_workers值
            # 计算实际使用的max_workers值
            base_workers = os.cpu_count() or 4  # 默认以CPU核心数为基础
            target_max_workers = base_workers * 4 if max_workers is None else max_workers

            if not cls._instance or cls._instance._max_workers != target_max_workers:
                # 关闭旧的线程池（如果存在）
                if cls._instance:
                    cls.shutdown(wait)

                cls._instance = ThreadPoolExecutor(max_workers=target_max_workers)
            return cls._instance

    @classmethod
    def shutdown(cls, wait: bool = True) -> None:
        """安全关闭线程池

        Args:
            wait: 是否等待所有任务完成

        Exception Handling:
            捕获关闭过程中的异常并通过handle_exception处理，默认重新抛出异常
        """
        if cls._instance:
            try:
                cls._instance.shutdown(wait=wait)
            except Exception as exc:
                handle_exception(exc=exc, custom_message='ThreadPoolManager.shutdown', re_raise=True)
            finally:
                cls._instance = None


class EnhancedThreadPool:
    """增强型线程池，提供任务结果收集和异常处理功能

    扩展了标准ThreadPoolExecutor，支持任务结果自动收集、统一异常处理、批量任务提交等功能。
    适用于需要集中管理和监控多任务执行的场景。

    Args:
        max_workers: 最大工作线程数，None表示根据CPU核心数自动计算
        thread_name_prefix: 线程名前缀，用于调试和日志跟踪
        exception_handler: 自定义异常处理器函数
    """

    def __init__(
        self,
        max_workers: int = 0,
        thread_name_prefix: str = 'EnhancedThreadPool',
        exception_handler: Callable[[Exception], None] | None = None,
    ):
        """初始化增强型线程池

        Args:
            max_workers: 最大工作线程数，默认CPU核心数×4（适合IO密集型任务）
            thread_name_prefix: 线程名前缀，用于调试和日志跟踪
            exception_handler: 自定义异常处理器函数
        """
        base_workers = os.cpu_count() or 4  # 默认IO密集型配置
        max_workers = max_workers if max_workers > 0 else base_workers * 4

        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self._future_tasks: list[Future] = []
        self.results: list[Any] = []
        self.exception_handler = exception_handler

    def __enter__(self):
        """支持上下文管理器协议"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """自动关闭线程池，确保资源正确释放"""
        self.shutdown(wait=True)

    def _task_wrapper(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """任务包装器，用于收集结果和处理异常

        Args:
            fn: 要执行的目标函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            Any: 任务执行结果或异常处理结果
        """
        try:
            result = fn(*args, **kwargs)
            self.results.append({'state': 'success', 'result': result, 'err': None})
            return result
        except Exception as err:
            self.results.append({'state': 'error', 'result': None, 'err': err})
            return handle_exception(exc=err, handler=self.exception_handler, custom_message='EnhancedThreadPool._task_wrapper')

    def submit_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """提交单个任务到线程池执行

        Args:
            fn: 要执行的目标函数
            *args: 传递给函数的位置参数
            **kwargs: 传递给函数的关键字参数

        Returns:
            Future: Future对象用于跟踪任务状态和获取结果

        Raises:
            RuntimeError: 当线程池已关闭时尝试提交任务
        """
        future = self.executor.submit(self._task_wrapper, fn, *args, **kwargs)
        self._future_tasks.append(future)
        return future

    def submit_tasks(
        self,
        fn: Callable[..., Any],
        iterables: Sequence[TaskParams],
    ) -> list[Future]:
        """批量提交任务到线程池，支持智能参数格式检测

        Args:
            fn: 要执行的目标函数
            iterables: 任务参数的可迭代对象
                - 简单格式: [item1, item2, ...]
                - 复杂格式: [((args_tuple), {kwargs_dict}), ...]

        Returns:
            list[Future]: 提交的任务Future对象列表
        """
        futures = []
        if not iterables:
            return futures

        # 统一处理所有参数项
        for item in iterables:
            if isinstance(item, (tuple, list)) and len(item) == 2 and isinstance(item[1], dict):
                # 复杂格式: (args_tuple, kwargs_dict)
                arg_tuple, kwargs_dict = item
                future = self.submit_task(fn, *arg_tuple, **kwargs_dict)
            else:
                # 简单格式: 单个参数
                future = self.submit_task(fn, item)
            futures.append(future)

        return futures

    def wait_all_completed(self, timeout: float | None = None) -> list[Any]:
        """等待所有任务完成并获取结果

        Args:
            timeout: 超时时间（秒），None表示无限等待

        Returns:
            list[Any]: 已完成任务的结果列表
        """
        # 记录当前已有的结果数量
        current_results_count = len(self.results)

        # 如果没有待处理任务，直接返回所有结果并清空
        if not self._future_tasks:
            results = self.results.copy()
            self.results.clear()
            return results

        # 等待任务完成，根据timeout决定等待策略
        if timeout is None:
            # 无超时限制，等待所有任务完成
            _, not_done = wait(self._future_tasks, timeout=None, return_when=ALL_COMPLETED)
            self._future_tasks = list(not_done)  # 应该为空列表

            # 返回所有结果并清空列表
            results = self.results.copy()
            self.results.clear()
            return results

        # 有超时限制，等待一段时间后返回已完成的任务
        _, not_done = wait(self._future_tasks, timeout=timeout, return_when=FIRST_COMPLETED)
        self._future_tasks = list(not_done)

        # 只返回本次调用期间新增的结果
        new_results = self.results[current_results_count:].copy()
        # 从results列表中移除已返回的结果
        del self.results[:current_results_count]
        return new_results

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池并清理资源

        Args:
            wait: 是否等待所有任务完成后再关闭
        """
        try:
            self.executor.shutdown(wait=wait)
        except Exception as exc:
            handle_exception(exc=exc, custom_message='EnhancedThreadPool.shutdown', re_raise=True)


class AsyncThreadPool:
    """异步增强型线程池，支持同步和异步函数执行的统一接口。

    该类提供了一个功能强大的线程池实现，能够处理同步函数和异步函数的执行，
    支持任务提交、批量任务处理、回调函数、异步等待以及自动资源管理。
    适用于需要在多线程环境中混合执行同步和异步代码的场景。

    Args:
        max_workers: 线程池中的最大工作线程数，默认为 CPU 核心数的 4 倍
        thread_name_prefix: 线程名称前缀，用于调试
        exception_handler: 自定义异常处理函数，接收一个异常对象作为参数
        loop: 可选的事件循环对象，如果未提供则自动获取或创建

    Attributes:
        executor: 底层使用的 ThreadPoolExecutor 对象
        _future_tasks: 存储所有提交的异步任务的列表
        results: 存储所有任务执行结果的列表
        exception_handler: 异常处理函数
        _loop: 事件循环对象
        _shutting_down: 表示线程池是否正在关闭的标志
    """

    def __init__(
        self,
        max_workers: int = 0,
        thread_name_prefix: str = 'AsyncThreadPool',
        exception_handler: Callable[[Exception], None] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        """初始化异步增强型线程池

        Args:
            max_workers: 线程池中的最大工作线程数，默认为CPU核心数×4
            thread_name_prefix: 线程名称前缀，用于调试
            exception_handler: 自定义异常处理函数
            loop: 可选的事件循环对象
        """
        base_workers = os.cpu_count() or 4  # 默认IO密集型配置
        max_workers = max_workers if max_workers > 0 else base_workers * 4

        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self._future_tasks: list[asyncio.Future] = []
        self.results: list[Any] = []
        self.exception_handler = exception_handler
        self._loop = loop
        self._loop_lock = Lock()  # 添加线程锁保护事件循环创建
        self._shutting_down = False

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """获取或创建事件循环对象。

        线程安全地获取事件循环，如果不存在则创建新的。

        Returns:
            asyncio.AbstractEventLoop: 事件循环对象
        """
        if self._loop is None:
            # 使用锁确保线程安全
            with self._loop_lock:
                # 双重检查，避免重复创建
                if self._loop is None:
                    try:
                        self._loop = asyncio.get_running_loop()
                    except RuntimeError:
                        # 创建新的事件循环但不设置为当前线程的循环
                        self._loop = asyncio.new_event_loop()
        return self._loop

    def __enter__(self):
        """支持上下文管理器协议的入口方法。"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理器协议的退出方法，自动关闭线程池。

        Args:
            exc_type: 异常类型
            exc_val: 异常值
            exc_tb: 异常回溯
        """
        self.shutdown(wait=True)

    def _sync_wrapper(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """执行同步函数并处理异常

        Args:
            fn: 要执行的同步函数
            *args: 传递给函数的位置参数
            **kwargs: 传递给函数的关键字参数

        Returns:
            Any: 函数执行的结果，如果发生异常则返回None
        """
        try:
            result = fn(*args, **kwargs)
            self.results.append({'state': 'success', 'result': result, 'err': None})
            return result
        except Exception as err:
            self.results.append({'state': 'error', 'result': None, 'err': err})
            return handle_exception(exc=err, handler=self.exception_handler, custom_message='AsyncThreadPool._sync_wrapper')

    async def _async_wrapper(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """异步执行异步函数并处理异常

        Args:
            fn: 要执行的异步函数
            *args: 传递给函数的位置参数
            **kwargs: 传递给函数的关键字参数

        Returns:
            Any: 函数执行的结果，如果发生异常则返回None
        """
        try:
            result = await fn(*args, **kwargs)
            self.results.append({'state': 'success', 'result': result, 'err': None})
            return result
        except Exception as err:
            self.results.append({'state': 'error', 'result': None, 'err': err})
            return handle_exception(exc=err, handler=self.exception_handler, custom_message='AsyncThreadPool._async_wrapper')

    def _task_wrapper(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """统一的任务包装器，根据函数类型选择执行方式

        对于异步函数，创建新的事件循环并执行；对于同步函数，直接执行。
        自动处理执行过程中的异常。

        Args:
            fn: 要执行的函数（同步或异步）
            *args: 传递给函数的位置参数
            **kwargs: 传递给函数的关键字参数

        Returns:
            Any: 函数执行的结果，如果发生异常则返回None
        """
        if asyncio.iscoroutinefunction(fn):
            # 对于异步函数，创建新的事件循环
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(self._async_wrapper(fn, *args, **kwargs))
            except Exception as err:
                handle_exception(exc=err, handler=self.exception_handler, custom_message=f'AsyncThreadPool._task_wrapper: {fn.__name__}')
            finally:
                # 简单关闭循环
                try:
                    loop.close()
                except Exception as err:
                    handle_exception(
                        exc=err,
                        handler=self.exception_handler,
                        custom_message=f'AsyncThreadPool._task_wrapper: {fn.__name__}',
                        re_raise=False,
                    )
        else:
            # 对于同步函数，直接执行
            return self._sync_wrapper(fn, *args, **kwargs)

    def submit_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> asyncio.Future:
        """提交单个任务到线程池执行。

        Args:
            fn: 要执行的函数（同步或异步）
            *args: 传递给函数的位置参数
            **kwargs: 传递给函数的关键字参数

        Returns:
            asyncio.Future: 表示任务执行的 Future 对象

        Raises:
            RuntimeError: 当线程池正在关闭时
        """
        if self._shutting_down:
            raise RuntimeError('Cannot submit task to a pool that is shutting down')

        task_func = functools.partial(self._task_wrapper, fn, *args, **kwargs)
        future = self.loop.run_in_executor(self.executor, task_func)
        self._future_tasks.append(future)
        return future

    def submit_tasks(
        self,
        fn: Callable[..., Any],
        iterables: Sequence[TaskParams],
    ) -> list[asyncio.Future]:
        """批量提交任务到线程池。

        Args:
            fn: 要执行的目标函数
            iterables: 任务参数的可迭代对象
                - 简单格式: [item1, item2, ...]
                - 复杂格式: [((args_tuple), {kwargs_dict}), ...]

        Returns:
            list[Future]: 提交的任务Future对象列表
        """
        if self._shutting_down:
            raise RuntimeError('Cannot submit tasks to a pool that is shutting down')

        futures = []
        if not iterables:
            return futures

        # 统一处理所有参数项
        for item in iterables:
            if isinstance(item, (tuple, list)) and len(item) == 2 and isinstance(item[1], dict):
                # 复杂格式: (args_tuple, kwargs_dict)
                arg_tuple, kwargs_dict = item
                future = self.submit_task(fn, *arg_tuple, **kwargs_dict)
            else:
                # 简单格式: 单个参数
                future = self.submit_task(fn, item)
            futures.append(future)

        return futures

    def wait_all_completed(self, timeout: float | None = None) -> list[Any]:
        """等待所有提交的任务完成并获取结果

        Args:
            timeout: 等待超时时间（秒），None表示无限等待

        Returns:
            list[Any]: 所有已完成任务的结果列表
        """
        if not self._future_tasks:
            results = self.results.copy()
            self.results.clear()
            return results

        try:
            # 使用 asyncio.wait 来等待所有任务完成
            if self.loop.is_running():
                # 如果循环正在运行，使用线程安全的方式等待
                future = asyncio.run_coroutine_threadsafe(self._wait_all_completed_async(timeout), self.loop)
                return future.result(timeout=timeout)
            # 如果循环未运行，直接等待
            return self.loop.run_until_complete(self._wait_all_completed_async(timeout))
        except Exception:
            return []

    async def _wait_all_completed_async(self, timeout: float | None = None) -> list[Any]:
        """异步等待所有任务完成的内部方法

        Args:
            timeout: 等待超时时间（秒）

        Returns:
            list[Any]: 所有已完成任务的结果列表
        """
        if not self._future_tasks:
            results = self.results.copy()
            self.results.clear()
            return results

        try:
            if timeout is not None:
                # 使用 asyncio.wait 带超时
                _, pending = await asyncio.wait(self._future_tasks, timeout=timeout, return_when=asyncio.ALL_COMPLETED)
                # 只保留未完成的任务
                self._future_tasks = list(pending)
            else:
                # 无超时，等待所有任务完成
                await asyncio.gather(*self._future_tasks, return_exceptions=True)
                self._future_tasks.clear()

            results = self.results.copy()
            self.results.clear()
            return results
        except TimeoutError:
            return []

    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池并清理资源

        Args:
            wait: 是否等待所有任务完成后再关闭

        Raises:
            Exception: 当关闭线程池过程中出现严重错误时
        """
        if self._shutting_down:
            return

        self._shutting_down = True

        # 等待剩余任务完成
        if wait and self._future_tasks:
            try:
                # 使用 wait_all_completed 来等待
                self.wait_all_completed(timeout=5)
            except Exception as exc:
                handle_exception(exc=exc, custom_message='AsyncThreadPool.shutdown.wait')

        # 关闭线程池
        try:
            self.executor.shutdown(wait=wait)
        except Exception as exc:
            handle_exception(exc=exc, custom_message='AsyncThreadPool.shutdown', re_raise=True)
            # 额外清理：确保主循环被正确关闭（如果是我们创建的）

        if hasattr(self, '_loop') and self._loop and not self._loop.is_closed():
            with contextlib.suppress(Exception):
                # 如果循环不在运行，就关闭它
                if not self._loop.is_running():
                    self._loop.close()


class FutureThreadPool:
    """异步增强型线程池，使用 asyncio.run 作为最外层入口

    专注于一次性任务执行场景，提供简洁高效的API接口。
    自动管理异步和同步函数的执行，支持批量任务处理和结果收集。

    参数:
        max_workers: 线程池中的最大工作线程数，默认为 CPU 核心数的 4 倍
        thread_name_prefix: 线程名称前缀，用于调试
        exception_handler: 自定义异常处理函数
    """

    def __init__(
        self,
        max_workers: int = 0,
        thread_name_prefix: str = 'FutureThreadPool',
        exception_handler: Callable[[Exception], None] | None = None,
    ):
        """初始化FutureThreadPool线程池

        Args:
            max_workers: 线程池中的最大工作线程数，默认为CPU核心数×4
            thread_name_prefix: 线程名称前缀，用于调试
            exception_handler: 自定义异常处理函数
        """
        base_workers = os.cpu_count() or 4  # 默认IO密集型配置
        self.max_workers = max_workers if max_workers > 0 else base_workers * 4
        self.thread_name_prefix = thread_name_prefix
        self.exception_handler = exception_handler

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        return False

    async def _submit_task(self, fn: Callable[..., Any], *args, **kwargs) -> Any:
        """提交单个任务，自动检测函数类型并处理异常

        根据函数类型自动选择异步或同步执行路径，并统一处理异常

        Args:
            fn: 要执行的函数（同步或异步）
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            Any: 任务执行结果
        """
        if asyncio.iscoroutinefunction(fn):
            # 异步函数处理路径
            try:
                return await asyncio.create_task(fn(*args, **kwargs))
            except Exception as err:
                return handle_exception(exc=err, handler=self.exception_handler, custom_message=f'FutureThreadPool 异步任务执行失败: {fn.__name__}')
        else:
            # 同步函数处理路径
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix=self.thread_name_prefix) as executor:
                # 定义内部函数用于异常处理
                def sync_execute():
                    try:
                        return fn(*args, **kwargs)
                    except Exception as err:
                        return handle_exception(exc=err, handler=self.exception_handler, custom_message=f'FutureThreadPool 同步任务执行失败: {fn.__name__}')

                # 在线程池中执行同步函数
                return await loop.run_in_executor(executor, sync_execute)

    async def _submit_tasks(self, fn: Callable[..., Any], iterables: Sequence[TaskParams]) -> list[Any]:
        """批量提交任务

        Args:
            fn: 要执行的目标函数
            iterables: 任务参数的可迭代对象

        Returns:
            list[Any]: 所有任务的执行结果列表
        """
        tasks = []
        if not iterables:
            return tasks

        # 统一处理所有参数项
        for item in iterables:
            if isinstance(item, (tuple, list)) and len(item) == 2 and isinstance(item[1], dict):
                # 复杂格式: (args_tuple, kwargs_dict)
                arg_tuple, kwargs_dict = item
                task = self._submit_task(fn, *arg_tuple, **kwargs_dict)
            else:
                # 简单格式: 单个参数
                task = self._submit_task(fn, item)
            tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)

    def submit_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """同步提交单个任务

        使用asyncio.run作为最外层入口，自动管理事件循环生命周期

        Args:
            fn: 要执行的函数（同步或异步）
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            Any: 任务执行结果
        """
        return asyncio.run(self._submit_task(fn, *args, **kwargs))

    def submit_tasks(
        self,
        fn: Callable[..., Any],
        iterables: Sequence[TaskParams],
    ) -> list[Any]:
        """批量提交任务到线程池

        使用asyncio.run作为最外层入口，自动管理事件循环生命周期

        Args:
            fn: 要执行的目标函数
            iterables: 任务参数的可迭代对象

        Returns:
            list[Any]: 所有任务的执行结果列表
        """
        return asyncio.run(self._submit_tasks(fn, iterables))


__all__ = ['AsyncThreadPool', 'BaseThreadRunner', 'DynamicThreadRunner', 'EnhancedThreadPool', 'FutureThreadPool', 'ThreadPoolManager']
