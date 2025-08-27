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
import functools
import os
import selectors
from asyncio import Future
from asyncio.coroutines import iscoroutinefunction
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from aiohttp import ClientSession
from xt_response import ACResponse

# 根据操作系统选择合适的事件循环策略
if os.name == 'nt':  # Windows系统
    class MyPolicy(asyncio.DefaultEventLoopPolicy):
        def new_event_loop(self):
            return asyncio.ProactorEventLoop()
else:  # 非Windows系统
    class MyPolicy(asyncio.DefaultEventLoopPolicy):
        def new_event_loop(self):
            selector = selectors.SelectSelector()
            return asyncio.SelectorEventLoop(selector)


asyncio.set_event_loop_policy(MyPolicy())


def future_decorator(func):
    """future装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Future:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.Future()
        result = func(*args, **kwargs)
        future.set_result(result)

        loop.close()  # 关闭事件循环
        return future
    return wrapper


def coroutine_decorator(func):
    """将普通函数包装为返回协程的装饰器"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return func if iscoroutinefunction(func) else wrapper


def async_inexecutor_decorator(func):
    """异步运行装饰器,装饰普通函数或async函数,运行并返回结果"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        async def main(*args, **kwargs):
            if iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                loop = asyncio.get_running_loop()
                result = await loop.run_in_executor(None, func, *args, **kwargs)
            return result

        return asyncio.run(main(*args, **kwargs))

    return wrapper


def async_run_decorator(func):
    """异步装饰器,装饰函数或async函数,直接运行,返回结果"""

    @wraps(func)
    def _wrapper(*args, **kwargs):
        @wraps(func)
        async def main(*args, **kwargs):
            task = coroutine_decorator(func)(*args, **kwargs)
            return await asyncio.gather(task, return_exceptions=True)

        return asyncio.run(main(*args, **kwargs))

    return _wrapper


class AioHttpCrawl:
    def __init__(self): ...

    def add_pool(self, func, args_list, callback=None):
        """添加函数(同步异步均可)及参数,异步运行，返回结果\n
        [(url,),{'index':index}] for index, url in enumerate(urls_list,1)]"""
        return asyncio.run(self.multi_fetch(func, args_list, callback=callback))

    async def multi_fetch(self, func, args_list, callback=None):
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

    args_list = [
        [("https://www.163.com",), {"index": 3}],
        [("https://www.126.com",), {"index": 2}],
        [("https://httpbin.org/get",), {"index": 4}],
    ]
    print(111111111, myaio.add_pool(get, args_list))
    # $装饰器##########################################################

    @async_inexecutor_decorator
    def get_html(url):
        return get(url)

    print(44444444444444, res := get_html("https://www.baidu.com"))

    @async_run_decorator
    def get_a_html(url):
        return get(url)

    print(5555555555555, res := get_a_html("https://www.baidu.com"))

    @async_run_decorator
    async def get_message(url):
        async with ClientSession() as session, session.get(url) as response:
            content = await response.content.read()
            return ACResponse(response, content, 0)

    print(6666666666666, res := get_message("https://httpbin.org/get"))

    # @coroutine_decorator
    def normal_function():
        return "Hello, I'm a normal function!"

    # 使用await调用被装饰后的普通函数
    async def main():
        # result = await normal_function()
        result = await coroutine_decorator(normal_function)()
        print(777777777777777, result)

    asyncio.run(main())

    # 使用future_decorator装饰器
    @future_decorator
    def add(a, b):
        return a + b

    # 调用被装饰的函数
    print(88888888888888, result_future := add(3, 5))


    # 获取异步Future对象的结果
    async def get_result(in_future):
        result = await in_future
        print("Result:", result)

    asyncio.run(get_result(add(3, 5)))
