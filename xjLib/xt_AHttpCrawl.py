# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-08-21 09:34:40
FilePath     : /CODE/xjLib/xt_ahttpcrawl.py
Github       : https://github.com/sandorn/home
==============================================================
aiohttp笔记 - happy_codes - 博客园
https://www.cnblogs.com/haoabcd2010/p/10615364.html
"""

import asyncio
import selectors
from asyncio.coroutines import iscoroutinefunction
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps

import wrapt
from aiohttp import ClientSession
from xt_response import ACResponse


class MyPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        selector = selectors.SelectSelector()
        return asyncio.SelectorEventLoop(selector)


asyncio.set_event_loop_policy(MyPolicy())


@wrapt.decorator
def future_decorator(func, instance, args, kwargs):
    """future装饰器"""
    future = asyncio.Future()
    result = func(*args, **kwargs)
    future.set_result(result)
    return future


def coroutine_decorator(func):
    """尝试将普通函数包装为返回协程的装饰器（但注意这不是真正的异步）"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 注意：这里直接调用同步函数，不等待任何异步操作
        return func(*args, **kwargs)

    return func if iscoroutinefunction(func) else wrapper


def async_inexecutor_decorator(func):
    """异步运行装饰器,装饰普通函数或async函数,运行并返回结果"""

    @wrapt.decorator
    def _wrapper(func, instance, args, kwargs):
        async def __wrapper(*args, **kwargs):
            if iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, func, *args, **kwargs)
            return result

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper(func)


def async_run_decorator(func):
    """异步装饰器,装饰函数或async函数,直接运行,返回结果"""

    @wraps(func)
    def _wrapper(*args, **kwargs):
        @wraps(func)
        async def __wrapper(*args, **kwargs):
            task = coroutine_decorator(func)(*args, **kwargs)
            return await asyncio.gather(task, return_exceptions=True)

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper


class AioHttpCrawl:
    def __init__(self):
        self.future_list = []

    def add_pool(self, func, *args, callback=None, **kwargs):
        """添加函数(同步异步均可)及参数,异步运行，返回结果"""
        return asyncio.run(self._multi_fetch(func, *args, callback=callback, **kwargs))

    async def _multi_fetch(self, func, *args, callback=None, **kwargs):
        _loop = asyncio.get_running_loop()

        tasks = []
        with ThreadPoolExecutor(160) as executor:
            for arg in zip(*args):
                task = _loop.run_in_executor(executor, func, *arg, **kwargs)
                if callback:
                    task.add_done_callback(callback)
                tasks.append(task)

        self.future_list.extend(tasks)

        return await asyncio.gather(*tasks, return_exceptions=True)

    def wait_completed(self):
        if not self.future_list:
            return []
        # while not all([future.done() for future in self.future_list]):sleep(0.01);continue

        result_list = []
        for future in as_completed(self.future_list):
            try:
                result = future.result()
                result_list.append(result)
            except Exception as exc:
                # 处理异常，例如记录日志
                print(f"Task failed with exception: {exc}")

        self.future_list.clear()
        return result_list

    def reset(self):
        """重置线程池和future_list(慎用,可能导致正在运行的任务被取消)"""
        self.future_list.clear()


if __name__ == "__main__":
    ...
    # $add_tasks#######################################################
    myaio = AioHttpCrawl()
    url_list = [
        "https://www.163.com",
        "https://www.126.com",
        "https://www.bigee.cc/book/6909/2.html",
    ]
    # $add_func########################################################
    from xt_requests import get

    print(11111111111111111, myaio.add_pool(get, url_list * 1))

    # print(2222222222222222, myaio.add_pool(get, ["https://httpbin.org/get"] * 3))
    # print(3333333333333333, myaio.wait_completed())
    # $装饰器##########################################################

    @async_inexecutor_decorator
    def get_html(url):
        return get(url)

    # print(44444444444444, res := get_html("https://www.baidu.com"))

    @async_run_decorator
    async def get_a_html(url):
        return get(url)

    # print(5555555555555, res := get_a_html("https://www.baidu.com"))

    @async_run_decorator
    async def get_message(url):
        async with ClientSession() as session, session.get(url) as response:
            content = await response.content.read()
            return ACResponse(response, content, 0)

    # print(6666666666666, res := get_message("https://httpbin.org/get"))

    # print(
    #     77777777777777,
    #     myaio.add_pool(get_message, ["https://httpbin.org/get"] * 3),
    # )

    # print(888888888888, myaio._wait_completed())
