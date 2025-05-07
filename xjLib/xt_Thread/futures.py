# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-08-21 14:27:52
FilePath     : /CODE/xjLib/xt_thread/futures.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import threading
from concurrent.futures import (
    ALL_COMPLETED,
    Future,
    ThreadPoolExecutor,
    as_completed,
    wait,
)
from os import cpu_count
from typing import Any, Callable, List, Optional


class EnhancedThreadPool:
    def __init__(
        self, max_workers: int = None, thread_name_prefix: str = "EnhancedThreadPool"
    ):
        """
        增强型线程池，提供任务结果收集和异常处理功能
        :param max_workers: 最大工作线程数，默认根据CPU核心数自动计算
        :param thread_name_prefix: 线程名前缀，用于调试和日志跟踪
        """
        self.executor = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix=thread_name_prefix
        )
        self.futures: List[Future] = []
        self.results: List[Any] = []
        self._lock = threading.Lock()
        self.task_count = 0
        self.exception_handler: Optional[Callable[[Exception], None]] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)

    def set_exception_handler(self, handler: Callable[[Exception], None]) -> None:
        """设置全局异常处理器"""
        self.exception_handler = handler

    def _task_wrapper(self, fn: Callable, *args, **kwargs):
        """任务包装器，用于收集结果和处理异常"""
        try:
            result = fn(*args, **kwargs)
            with self._lock:
                self.results.append(result)
            return result
        except Exception as e:
            if self.exception_handler:
                self.exception_handler(e)
            else:
                print(f"Task failed with exception: {e}")
            raise
    def submit_task(self, fn: Callable, *args, **kwargs) -> Future:
        """
        提交异步任务到线程池
        :param fn: 要执行的目标函数
        :return: Future对象用于跟踪任务状态
        """
        future = self.executor.submit(self._task_wrapper, fn, *args, **kwargs)
        with self._lock:
            self.futures.append(future)
            self.task_count += 1
        return future

    def wait_for_completion(self, timeout: float = None) -> bool:
        """等待所有任务完成"""
        _, not_done = wait(self.futures, timeout=timeout, return_when=ALL_COMPLETED)
        with self._lock:
            self.futures = list(not_done)
        return not not_done

    def get_results(self) -> List[Any]:
        """获取已完成任务的结果"""
        with self._lock:
            return self.results.copy()

    def shutdown(self, wait: bool = True):
        """关闭线程池"""
        self.executor.shutdown(wait=wait)


class ThreadPool(ThreadPoolExecutor):
    def __init__(self, io_bound: bool = True):
        """
        :param io_bound: 是否为I/O密集型任务，True则设置较多线程
        """
        base_count = cpu_count() or 4
        # I/O密集型任务设置较多线程，CPU密集型任务设置较少线程
        self.count = base_count * 4 if io_bound else base_count + 2
        super().__init__(max_workers=self.count)
        self._future_tasks: List[Future] = []

    def add_tasks(self, fn, *args_iter, callback=None):
        for item in zip(*args_iter):
            future = self.submit(fn, *item)
            if callback:
                future.add_done_callback(callback)
            self._future_tasks.append(future)

    def wait_completed(self):
        """获取结果,无序"""
        # self.shutdown(wait=True)
        if not self._future_tasks:
            return []
        # while not all([future.done() for future in self._future_tasks]):sleep(0.01);continue

        result_list = []
        for future in as_completed(self._future_tasks):
            try:
                result = future.result()
                result_list.append(result)
            except Exception as exc:
                # 处理异常，例如记录日志
                print(f"Task failed with exception: {exc}")

        self._future_tasks.clear()
        return result_list


class FnInPool:
    """将程序放到ThreadPoolExecutor中异步运行,返回结果"""

    def __init__(self, fn, *args, **kwargs):
        self.count = (cpu_count() or 4) * 4
        self.executor = ThreadPoolExecutor(max_workers=self.count)
        self.fn, self.args, self.kwargs = fn, args, kwargs
        self._map() if len(args) == 1 else self._run()

    def _run(self):
        future_list = [
            self.executor.submit(self.fn, *arg, **self.kwargs)
            for arg in zip(*self.args)
        ]
        self.result = [future.result() for future in as_completed(future_list)]

    def _map(self):
        result_iterator = self.executor.map(self.fn, *self.args, **self.kwargs)
        self.result = list(result_iterator)


if __name__ == "__main__":
    from xt_requests import get

    url_list = [
        "https://www.jd.com/",
        "https://xinghuo.xfyun.cn/desk",
        "http://www.163.com/",
    ]
    # res = FnInPool(get, url_list * 1)
    # print(111111, res.result)

    # POOL = ThreadPool()
    # POOL.add_tasks(get, url_list)
    # res = POOL.wait_completed()
    # print(222222, res)
    def test_fn(urls):
        thread_pool = EnhancedThreadPool()

        # 提交多个任务
        futures = []
        for url in urls:
            future = thread_pool.submit_task(get, url)
            futures.append(future)

        # 等待所有任务完成
        thread_pool.wait_for_completion()

        # 获取并打印结果
        results = thread_pool.get_results()
        for result in results:...
            # print(result)

        # 关闭线程池
        thread_pool.shutdown()
        return results

    res = test_fn(url_list*4)
    print(333333,len(res), res)
