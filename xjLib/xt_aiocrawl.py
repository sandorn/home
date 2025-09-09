# !/usr/bin/env python
"""
==============================================================
Description  : 异步HTTP爬虫工具 - 提供高效的异步HTTP请求和任务管理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2025-09-08 16:48:00
FilePath     : /CODE/xjLib/xt_aiocrawl.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Tuple

from xt_thread.futures import TaskExecutor


class MyPolicy(asyncio.DefaultEventLoopPolicy):
    """自定义事件循环策略类 - 配置异步IO事件循环类型"""
    def new_event_loop(self):
        # return asyncio.ProactorEventLoop()
        return asyncio.SelectorEventLoop()


asyncio.set_event_loop_policy(MyPolicy())


class AioCrawl:
    """异步类 - 使用TaskExecutor实现高效的任务管理

    提供简洁的API接口，支持批量，自动管理线程池和任务执行。
    结合了异步IO和多线程技术，适用于大规模网络爬虫和数据采集场景。

    参数:
        max_workers: 最大工作线程数，默认为None（根据任务类型自动设置）
        io_bound: 是否为I/O密集型任务，默认为True
    """

    def __init__(self, max_workers: Optional[int] = None, io_bound: bool = True):
        """初始化异步HTTP爬取类

        参数:
            max_workers: 最大工作线程数，默认为None（根据任务类型自动设置）
            io_bound: 是否为I/O密集型任务，默认为True
        """
        self.max_workers = max_workers
        self.io_bound = io_bound

    def add_pool(self, func, args_list, callback=None):
        """添加函数(同步异步均可)及参数列表，异步运行

        参数:
            func: 要执行的函数（同步或异步函数均可）
            args_list: 参数列表，每个元素为[(位置参数元组), {关键字参数字典}]
            callback: 可选，任务完成后的回调函数

        返回:
            任务执行结果列表
        """
        return asyncio.run(self.multi_fetch(func, args_list, callback=callback))

    async def multi_fetch(
        self,
        func: Callable,
        args_list: List[Tuple[Tuple, Dict]],
        callback: Optional[Callable] = None,
    ):
        """异步批量执行函数

        参数:
            func: 要执行的目标函数
            args_list: 参数列表，每个元素为(位置参数元组, 关键字参数字典)
            callback: 可选，任务完成后的回调函数

        返回:
            所有任务的执行结果列表
        """
        _loop = asyncio.get_running_loop()

        tasks = []
        with ThreadPoolExecutor(160) as executor:
            for arg, kwargs in args_list:
                partial_func = functools.partial(func, *arg, **kwargs)
                task = _loop.run_in_executor(executor, partial_func)
                if callback:
                    task.add_done_callback(callback)
                tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)

    def fetch_tasks(
        self,
        func: Callable,
        tasks_params: List[Tuple[Tuple, Dict]],
        callback: Optional[Callable] = None,
    ) -> List[Any]:
        """执行自定义任务列表

        使用TaskExecutor管理任务执行，支持并行处理多个HTTP请求或其他I/O任务。

        参数:
            func: 执行任务的函数
            tasks_params: 任务参数列表，每个元素是(位置参数元组, 关键字参数字典)
            callback: 可选，任务完成后的回调函数

        返回:
            任务结果列表
        """
        # 使用TaskExecutor执行任务
        with TaskExecutor(io_bound=self.io_bound, max_workers=self.max_workers) as executor:
            # 直接使用submit方法添加任务，这样更直接且避免参数传递问题
            executor.add_tasks(func, tasks_params, callback=callback)
            # 等待所有任务完成并获取结果
            results = executor.wait_completed()
        return results


if __name__ == "__main__":
    from xt_ahttp import ahttpGet
    from xt_requests import get
    urls = ["https://www.163.com", "https://www.126.com", "https://httpbin.org/get"]
    task_params = []
    args_list = []

    for index,url in enumerate(urls):
        args_list.append([(url,), {"timeout": 10}])
        task_params.append([(url,), {"index": index, "timeout": 10}])

    myaio = AioCrawl()
    results_0 = myaio.add_pool(ahttpGet, args_list)
    print("示例1 结果:", results_0)

    print(2222222222222222, task_params)

    results_2 = myaio.fetch_tasks(get, task_params)
    print(f"示例2 结果: {results_2}")
