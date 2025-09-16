"""
==============================================================
Description  : 线程池增强模块 - 提供多种线程池实现及异步任务处理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-08-21 14:27:52
FilePath     : /CODE/xjLib/xt_thread/futures.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能：
- BaseThreadPool: 基础线程池实现，支持基本的任务提交和线程管理
- DynamicThreadPool: 动态调整的线程池，可根据系统资源和任务队列自动扩展或收缩
- ThreadPoolManager: 全局线程池单例管理，适用于多模块共享线程池资源
- EnhancedThreadPool: 增强型线程池，提供任务结果收集和统一的异常处理机制
- TaskExecutor: 简化的任务执行器，自动根据任务类型优化线程数量
- AsyncFunction: 便捷的函数异步执行包装器，自动在线程池中运行函数

主要特性：
- 支持任务提交、结果收集和异常处理
- 动态调整线程数量，优化资源利用率
- 线程池单例管理，避免资源浪费
- 提供上下文管理器支持，确保资源正确释放
- 支持同步执行和异步结果获取
==============================================================
"""

from __future__ import annotations

import queue
import time
from collections.abc import Callable
from concurrent.futures import (
    ALL_COMPLETED,
    Future,
    ThreadPoolExecutor,
    as_completed,
    wait,
)
from os import cpu_count
from queue import Queue
from threading import Condition, Lock, RLock, current_thread
from typing import Any, TypeVar

import psutil
from xt_wraps import handle_exception

from .thread import SafeThread, ThreadBase
from .thread import ThreadManager as ThreadInstanceManager

T = TypeVar('T')
R = TypeVar('R')


class BaseThreadPool:
    """基础线程池实现

    提供基本的线程创建、任务提交和线程资源管理功能，适用于简单的并发任务场景。
    作为其他线程池实现的基类或独立使用的轻量级线程池。

    参数:
        max_workers: 最大工作线程数
        name_prefix: 线程名称前缀，用于调试和日志跟踪

    使用示例:
        pool = BaseThreadPool(max_workers=5)
        thread = pool.submit(task_function, arg1, arg2)
    """

    def __init__(self, max_workers: int = 10, name_prefix: str = 'BaseThreadPool'):
        self.max_workers = max_workers
        self.name_prefix = name_prefix
        self._active_threads = 0
        self._lock = RLock()
        self._condition = Condition(self._lock)

    def submit(self, target: Callable, *args, **kwargs) -> ThreadBase:
        """提交任务到线程池

        参数:
            target: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        返回:
            ThreadBase: 创建并启动的线程对象
        """
        with self._condition:
            # 等待有空闲线程
            while self._active_threads >= self.max_workers:
                self._condition.wait()

            # 增加活跃线程计数
            self._active_threads += 1

            # 创建线程并启动
            def execute_task():
                self._worker_wrapper(target, args, kwargs)

            thread = ThreadBase(target=execute_task)
            thread.name = f'{self.name_prefix}-{thread.name}'
            thread.start()
            return thread

    def _worker_wrapper(self, target: Callable, args: tuple, kwargs: dict):
        """工作线程包装器，负责跟踪线程完成情况"""
        try:
            target(*args, **kwargs)
        finally:
            with self._condition:
                self._active_threads -= 1
                self._condition.notify()

    @property
    def active_threads(self) -> int:
        """获取当前活跃的线程数"""
        with self._condition:
            return self._active_threads


class DynamicThreadPool:
    """动态调整的线程池实现

    根据系统资源使用情况和任务队列状态自动调整工作线程数量，适用于负载波动较大的场景。
    支持自动扩缩容以适应不同的任务负载，同时提供资源监控和异常处理机制。

    参数:
        min_workers: 最小工作线程数（保持活跃）
        max_workers: 最大工作线程数（根据负载自动调整）
        queue_size: 任务队列最大容量

    使用示例:
        with DynamicThreadPool(min_workers=2, max_workers=20) as pool:
            for i in range(100):
                pool.submit(process_task, i)
    """

    def __init__(self, min_workers: int = 2, max_workers: int = 10, queue_size: int = 100) -> None:
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.task_queue = Queue(maxsize=queue_size)
        self.workers = []
        self.is_running = True
        self.lock = Lock()

        # 启动监控线程
        self.monitor = SafeThread(target=self._monitor_resources)
        self.monitor.daemon = True  # 设置为守护线程，主程序结束时自动退出
        self.monitor.start()
        ThreadInstanceManager.add_thread(self.monitor)

        # 启动初始工作线程
        self._adjust_worker_count(min_workers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """安全关闭线程池"""
        self.shutdown(wait=True)

    def _monitor_resources(self):
        """监控系统资源和任务队列，动态调整线程数"""
        while self.is_running:
            try:
                cpu_percent = psutil.cpu_percent()
                queue_size = self.task_queue.qsize()
                current_workers = len(self.workers)

                with self.lock:
                    if queue_size > current_workers * 2 and cpu_percent < 80:
                        # 队列积压且CPU资源充足，增加线程
                        self._adjust_worker_count(min(current_workers + 2, self.max_workers))
                    elif queue_size < current_workers and current_workers > self.min_workers:
                        # 任务较少，减少线程
                        self._adjust_worker_count(max(current_workers - 1, self.min_workers))
            except Exception as err:
                handle_exception('DynamicThreadPool._monitor_resources', err)

            time.sleep(2)  # 监控间隔

    def _adjust_worker_count(self, target_count: int):
        """调整工作线程数量"""
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

    def _worker_loop(self):
        """工作线程主循环"""
        cur_thread = current_thread()
        while self.is_running or not self.task_queue.empty():
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:  # 退出信号
                    with self.lock:
                        # 安全地移除线程，先检查线程是否在列表中
                        if cur_thread in self.workers:
                            self.workers.remove(cur_thread)
                    break

                func, args, kwargs = task
                try:
                    func(*args, **kwargs)
                except Exception as err:
                    handle_exception('DynamicThreadPool._worker_loop', err)
                finally:
                    self.task_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """提交任务到线程池

        参数:
            func: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        异常:
            RuntimeError: 当线程池已关闭时抛出
        """
        if not self.is_running:
            raise RuntimeError('线程池已关闭')
        self.task_queue.put((func, args, kwargs))

    def shutdown(self, wait: bool = True):
        """关闭线程池

        参数:
            wait: 是否等待所有任务完成
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

    提供线程池实例的统一管理，避免重复创建线程池资源，适用于多模块共享线程池的场景。
    确保在整个应用程序生命周期内，相同配置的线程池只被创建一次。

    使用示例:
        with ThreadPoolManager.get_pool() as executor:
            future = executor.submit(task_function, args)

        # 或者直接提交任务
        future = ThreadPoolManager.get_pool().submit(task_function, args)
    """

    _instance: ThreadPoolExecutor | None = None
    _lock = Lock()

    @classmethod
    def get_pool(cls, max_workers: int | None = None) -> ThreadPoolExecutor:
        """获取线程池实例

        参数:
            max_workers: None-自动计算(IO密集型推荐)，具体数值适用于CPU密集型任务

        返回:
            ThreadPoolExecutor: 线程池实例
        """
        with cls._lock:
            # 计算实际使用的max_workers值
            base_workers = cpu_count() or 4
            target_max_workers = base_workers * 4 if max_workers is None else max_workers

            # 如果实例不存在或max_workers不同，则创建新实例
            if not cls._instance or cls._instance._max_workers != target_max_workers:
                # 关闭旧的线程池（如果存在）
                if cls._instance:
                    try:
                        cls._instance.shutdown(wait=False)
                    except Exception as err:
                        handle_exception('ThreadPoolManager.get_pool', err)
                cls._instance = ThreadPoolExecutor(max_workers=target_max_workers)
            return cls._instance

    @classmethod
    def shutdown(cls):
        """安全关闭线程池"""
        if cls._instance:
            try:
                cls._instance.shutdown(wait=True)
            except Exception as err:
                handle_exception('ThreadPoolManager.shutdown', err, re_raise=True)
            cls._instance = None


class EnhancedThreadPool[T, R]:
    """增强型线程池，提供任务结果收集和异常处理功能

    扩展了标准ThreadPoolExecutor，增加了任务结果收集、统一异常处理和任务管理功能。
    适用于需要集中管理和监控多任务执行的场景。

    参数:
        max_workers: 最大工作线程数，默认根据CPU核心数自动计算
        thread_name_prefix: 线程名前缀，用于调试和日志跟踪

    使用示例:
        with EnhancedThreadPool(max_workers=8) as pool:
            # 提交多个任务
            for i in range(10):
                pool.submit_task(process_data, i)

            # 等待所有任务完成
            pool.wait_for_completion()

            # 获取所有结果
            results = pool.get_results()
    """

    def __init__(self, max_workers: int | None = None, thread_name_prefix: str = 'EnhancedThreadPool'):
        base_workers = cpu_count() or 4
        max_workers = max_workers or base_workers * 4  # 默认IO密集型配置

        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self.futures: list[Future] = []
        self.results: list[R] = []
        self.task_count = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)

    def _task_wrapper(self, fn: Callable[[T], R], *args, **kwargs) -> R:
        """任务包装器，用于收集结果和处理异常"""
        try:
            result = fn(*args, **kwargs)
            self.results.append(result)
            return result
        except Exception as err:
            handle_exception('EnhancedThreadPool._task_wrapper', err, re_raise=True)

    def submit_task(self, fn: Callable[[T], R], *args: Any, **kwargs: Any) -> Future:
        """提交异步任务到线程池

        参数:
            fn: 要执行的目标函数
            *args: 传递给目标函数的位置参数
            **kwargs: 传递给目标函数的关键字参数

        返回:
            Future: Future对象用于跟踪任务状态和获取结果
        """
        future = self.executor.submit(self._task_wrapper, fn, *args, **kwargs)
        self.futures.append(future)
        self.task_count += 1
        return future

    def wait_for_completion(self, timeout: float | None = None) -> bool:
        """等待所有任务完成

        参数:
            timeout: 超时时间（秒），None表示无限等待

        返回:
            bool: 所有任务是否都已完成
        """
        if not self.futures:
            return True

        _, not_done = wait(self.futures, timeout=timeout, return_when=ALL_COMPLETED)
        self.futures = list(not_done)
        return not not_done

    def get_results(self) -> list[R]:
        """获取已完成任务的结果

        返回:
            List: 已完成任务的结果列表
        """
        return self.results.copy()

    def shutdown(self, wait: bool = True):
        """关闭线程池

        参数:
            wait: 是否等待所有任务完成
        """
        self.executor.shutdown(wait=wait)


class TaskExecutor(ThreadPoolExecutor):
    """简化的任务执行器

    简化了多任务提交和结果获取流程，自动根据任务类型优化线程数量。
    适用于批量处理数据和需要统一管理多任务结果的场景。

    参数:
        io_bound: 是否为I/O密集型任务，True则设置较多线程
        max_workers: 可选，手动指定最大工作线程数，优先级高于io_bound

    使用示例:
        def process_item(item):
            return item * 2

        with TaskExecutor(io_bound=True) as executor:
            executor.add_tasks(process_item, [1, 2, 3, 4, 5])
            results = executor.wait_completed()
    """

    def __init__(self, io_bound: bool = True, max_workers: int | None = None):
        """
        参数:
            io_bound: 是否为I/O密集型任务，True则设置较多线程
            max_workers: 可选，手动指定最大工作线程数，优先级高于io_bound
        """
        base_count = cpu_count() or 4
        # I/O密集型任务设置较多线程，CPU密集型任务设置较少线程
        if max_workers is None:
            self.count = base_count * 4 if io_bound else base_count + 2
        else:
            self.count = max_workers
        super().__init__(max_workers=self.count)
        self._future_tasks: list[Future] = []

    def add_task(
        self,
        fn: T,
        *args: Any,
        callback: Callable[..., Any] | None = None,
        **kwargs: Any,
    ):
        """添加任务到线程池

        参数:
            fn: 要执行的目标函数
            args: 位置参数
            kwargs: 关键字参数
        """
        future = self.submit(fn, *args, **kwargs)
        if callback:
            future.add_done_callback(callback)
        self._future_tasks.append(future)

    def add_tasks(
        self,
        fn: T,
        iterables: list[tuple | list[tuple | list, dict]] | list[Any],
        callback: Callable[..., Any] | None = None,
    ):
        """并行执行函数，每个元素作为独立任务提交

        参数:
            fn: 要执行的目标函数
            iterables: 可迭代对象，支持两种格式：
                1. 简单格式: 如 [1, 2, 3, 4]，每个元素作为fn的单个位置参数
                2. 复杂格式: 如 [[(1,),{'id':9001}], [(2,),{'id':9002}]]，每个元素是(位置参数元组, 关键字参数字典)
            callback: 可选，任务完成后的回调函数
        """
        if not iterables:
            return

        # 智能检测输入格式
        # 检查第一个元素是否为(元组, 字典)的格式
        first_item = iterables[0]
        if isinstance(first_item, tuple | list) and len(first_item) == 2 and isinstance(first_item[1], dict):
            # 复杂格式: [(args_tuple, kwargs_dict), ...]
            for arg_tuple, kwargs_dict in iterables:
                self.add_task(fn, *arg_tuple, callback=callback, **kwargs_dict)
        else:
            # 简单格式: [item1, item2, ...]，每个item作为单个参数
            for item in iterables:
                # 如果item本身就是元组，将其展开为位置参数
                if isinstance(item, tuple | list):
                    self.add_task(fn, *item, callback=callback)
                else:
                    # 否则作为单个位置参数
                    self.add_task(fn, item, callback=callback)

    def wait_completed(self):
        """等待所有任务完成并获取结果

        返回:
            List: 任务结果列表（无序）
        """
        if not self._future_tasks:
            return []

        result_list = []
        for future in as_completed(self._future_tasks):
            try:
                result = future.result()
                result_list.append(result)
            except Exception as err:
                handle_exception('TaskExecutor.wait_completed', err, re_raise=True)

        self._future_tasks.clear()
        return result_list


class AsyncFunction:
    """函数异步执行包装器

    提供简单的API，自动管理线程池创建和任务提交，适用于一次性多任务处理场景。
    简化了函数在线程池中的异步执行过程，自动处理线程池生命周期。

    参数:
        fn: 要执行的目标函数
        *args: 传递给目标函数的参数，单参数列表将使用map方法
        **kwargs: 传递给目标函数的关键字参数
        max_workers: 可选，指定线程池最大工作线程数

    使用示例:
        # 单参数列表 - 使用map
        result = AsyncFunction(process_item, [1, 2, 3, 4, 5]).result

        # 多参数列表 - 使用zip组合参数
        result = AsyncFunction(process_pair, [1, 2, 3], [4, 5, 6]).result

        # 指定线程数
        result = AsyncFunction(process_item, [1, 2, 3], max_workers=8).result
    """

    def __init__(self, fn, *args, max_workers: int | None = None, **kwargs):
        self.count = max_workers or (cpu_count() or 4) * 4
        self.executor = ThreadPoolExecutor(max_workers=self.count)
        self.fn, self.args, self.kwargs = fn, args, kwargs
        self.result = []

        try:
            if len(args) == 1 and isinstance(args[0], (list, tuple)):
                self._map()
            else:
                self._run()
        finally:
            self.executor.shutdown(wait=True)

    def _run(self):
        """处理多参数列表的情况"""
        future_list = [self.executor.submit(self.fn, *arg, **self.kwargs) for arg in zip(*self.args, strict=False)]
        self.result = [future.result() for future in as_completed(future_list)]

    def _map(self):
        """处理单参数列表的情况"""
        if self.kwargs:
            # 如果有kwargs，使用submit而不是map，因为map不支持kwargs
            def wrapper(arg):
                return self.fn(arg, **self.kwargs)

            future_list = [self.executor.submit(wrapper, arg) for arg in self.args[0]]
            self.result = [future.result() for future in as_completed(future_list)]
        else:
            # 没有kwargs时使用map
            result_iterator = self.executor.map(self.fn, *self.args)
            self.result = list(result_iterator)


# 保持向后兼容性
def ThreadPool(*args, **kwargs):  # noqa: N802
    """ThreadPool类的兼容层，已重命名为BaseThreadPool"""
    print('警告: ThreadPool类已重命名为BaseThreadPool，请更新代码')  # noqa: T201
    return BaseThreadPool(*args, **kwargs)


def PoolExecutor(*args, **kwargs):  # noqa: N802
    """PoolExecutor类的兼容层，已重命名为TaskExecutor"""
    print('警告: PoolExecutor类已重命名为TaskExecutor，请更新代码')  # noqa: T201
    return TaskExecutor(*args, **kwargs)


def FnInPool(*args, **kwargs):  # noqa: N802
    """FnInPool类的兼容层，已重命名为AsyncFunction"""
    print('警告: FnInPool类已重命名为AsyncFunction，请更新代码')  # noqa: T201
    return AsyncFunction(*args, **kwargs)
