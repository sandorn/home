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

from __future__ import annotations

import asyncio
import functools
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from xt_thread.futures import TaskExecutor
from xt_wraps import LogCls

mylog = LogCls()


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

    def __init__(self, max_workers: int | None = None, io_bound: bool = True):
        """初始化异步HTTP爬取类

        参数:
            max_workers: 最大工作线程数，默认为None（根据任务类型自动设置）
            io_bound: 是否为I/O密集型任务，默认为True
        """
        self.max_workers = max_workers
        self.io_bound = io_bound

    def add_pool(
        self,
        func,
        iterables: list[tuple | list[tuple | list, dict]] | list[Any],
        callback=None,
    ):
        """添加函数(同步异步均可)及参数列表，异步运行

        参数:
            func: 要执行的函数（同步或异步函数均可）
            iterables: 可迭代对象，支持两种格式：
                1. 简单格式: 如 [1, 2, 3, 4]，每个元素作为fn的单个位置参数
                2. 复杂格式: 如 [[(1,),{'id':9001}], [(2,),{'id':9002}]]，每个元素是(位置参数元组, 关键字参数字典)
            callback: 可选，任务完成后的回调函数

        返回:
            任务执行结果列表
        """
        return asyncio.run(self.multi_fetch(func, iterables, callback=callback))

    async def multi_fetch(
        self,
        func: Callable,
        iterables: list[tuple | list[tuple | list, dict]] | list[Any],
        callback: Callable | None = None,
    ):
        """异步批量执行函数

        参数:
            func: 要执行的目标函数
            iterables: 可迭代对象，支持两种格式：
                1. 简单格式: 如 [1, 2, 3, 4]，每个元素作为fn的单个位置参数
                2. 复杂格式: 如 [[(1,),{'id':9001}], [(2,),{'id':9002}]]，每个元素是(位置参数元组, 关键字参数字典)
            callback: 可选，任务完成后的回调函数

        返回:
            所有任务的执行结果列表
        """
        if iterables is None and isinstance(iterables, tuple | list):
            return None
        loop = asyncio.get_running_loop()

        tasks = []
        with ThreadPoolExecutor(160) as executor:
            # 智能检测输入格式
            # 检查第一个元素是否为(元组, 字典)的格式
            if isinstance(first_item := iterables[0], tuple | list) and len(first_item) == 2 and isinstance(first_item[1], dict):
                # 复杂格式: [(args_tuple, kwargs_dict), ...]
                for arg_tuple, kwargs_dict in iterables:
                    partial_func = functools.partial(func, *arg_tuple, **kwargs_dict)
                    task = loop.run_in_executor(executor, partial_func)
                    if callback:
                        task.add_done_callback(callback)
                    tasks.append(task)
            else:
                # 简单格式: [item1, item2, ...]，每个item作为单个参数
                for item in iterables:
                    # 如果item本身就是元组，将其展开为位置参数；如单个参数则直接用item
                    partial_func = functools.partial(func, *item) if isinstance(item, tuple | list) else functools.partial(func, item)
                    task = loop.run_in_executor(executor, partial_func)
                    if callback:
                        task.add_done_callback(callback)
                    tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=True)

    def fetch_tasks(
        self,
        func: Callable,
        iterables: list[tuple | list[tuple | list, dict]] | list[Any],
        callback: Callable | None = None,
    ) -> list[Any]:
        """执行自定义任务列表

        使用TaskExecutor管理任务执行，支持并行处理多个HTTP请求或其他I/O任务。
        特别处理异步函数，避免嵌套事件循环问题。

        参数:
            func: 执行任务的函数（支持同步和异步函数）
            tasks_params: 任务参数列表，每个元素是(位置参数元组, 关键字参数字典)
            callback: 可选，任务完成后的回调函数

        返回:
            任务结果列表
        """
        # 检查func是否是异步函数
        import inspect

        if inspect.iscoroutinefunction(func):
            # 对于异步函数，使用asyncio.run直接执行
            async def run_async_tasks():
                tasks = []
                # 智能检测输入格式
                if iterables and isinstance(first_item := iterables[0], tuple | list) and len(first_item) == 2 and isinstance(first_item[1], dict):
                    # 复杂格式: [(args_tuple, kwargs_dict), ...]
                    for arg_tuple, kwargs_dict in iterables:
                        task = asyncio.create_task(func(*arg_tuple, **kwargs_dict))
                        if callback:
                            task.add_done_callback(callback)
                        tasks.append(task)
                else:
                    for item in iterables:
                        task = asyncio.create_task(func(*item)) if isinstance(item, tuple | list) else asyncio.create_task(func(item))
                        if callback:
                            task.add_done_callback(callback)
                        tasks.append(task)
                return await asyncio.gather(*tasks, return_exceptions=True)

        # 对于同步函数，使用TaskExecutor执行
        with TaskExecutor(io_bound=self.io_bound, max_workers=self.max_workers) as executor:
            executor.add_tasks(func, iterables, callback=callback)
            return executor.wait_completed()


if __name__ == '__main__':
    from xt_wraps import LogCls

    mylog = LogCls()

    urls = ['https://www.126.com', 'https://www.126.com', 'https://httpbin.org/post']
    task_params = []
    args_list = []

    for index, url in enumerate(urls):
        args_list.append([(url,), {'timeout': 10}])
        task_params.append([(url,), {'index': index, 'timeout': 10}])

    myaio = AioCrawl()
    from xt_requests import get

    mylog('示例11 结果:', myaio.add_pool(get, urls))
    mylog('示例12 结果:', myaio.add_pool(get, task_params))
    mylog('示例13 结果:', myaio.fetch_tasks(get, urls))
    mylog('示例14 结果:', myaio.fetch_tasks(get, args_list))

    from xt_ahttp import ahttpGet

    mylog('示例21 结果:', myaio.add_pool(ahttpGet, urls))
    mylog('示例23 结果:', myaio.fetch_tasks(ahttpGet, urls))
    mylog('示例24 结果:', myaio.fetch_tasks(ahttpGet, args_list))
