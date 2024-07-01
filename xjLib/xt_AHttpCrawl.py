# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-26 09:47:33
FilePath     : /CODE/xjLib/xt_Asyncio.py
Github       : https://github.com/sandorn/home
==============================================================
aiohttp笔记 - happy_codes - 博客园
https://www.cnblogs.com/haoabcd2010/p/10615364.html
"""

import asyncio
from asyncio.coroutines import iscoroutinefunction
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from tenacity import retry, stop_after_attempt, wait_random
from xt_Head import RETRY_TIME, TIMEOUT, Head
from xt_Log import log_decorator
from xt_Response import htmlResponse

TRETRY = retry(
    reraise=True,  # 保留最后一次错误
    stop=stop_after_attempt(RETRY_TIME),
    wait=wait_random(min=0, max=1),
)


def future_decorator(func):
    """future装饰器"""

    @wraps(func)
    def __future(*args, **kwargs):
        future = asyncio.Future()
        result = func(*args, **kwargs)
        future.set_result(result)
        return future

    return __future


def coroutine_decorator(func):
    """异步装饰器,装饰普通函数,返回coroutine"""

    @wraps(func)
    async def _wrapper(*args, **kwargs):
        await asyncio.sleep(0)

        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return _wrapper


def async_inexecutor_decorator(func):
    """异步运行装饰器,装饰普通函数或async函数,运行并返回结果"""

    @wraps(func)
    def _wrapper(*args, **kwargs):
        @wraps(func)
        async def __wrapper(*args, **kwargs):
            if iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, func, *args, **kwargs)
            return result

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper


def async_run_decorator(func):
    """异步装饰器,装饰函数或async函数,直接运行,返回结果"""

    @wraps(func)
    def _wrapper(*args, **kwargs):
        @wraps(func)
        async def __wrapper(*args, **kwargs):
            callback = kwargs.pop('fu_callback', None)

            if iscoroutinefunction(func):
                task = asyncio.create_task(func(*args, **kwargs))
                if callback:
                    task.add_done_callback(callback)
            else:
                task = asyncio.create_task(coroutine_decorator(func)(*args, **kwargs))
                if callback:
                    task.add_done_callback(callback)
            return await asyncio.gather(task, return_exceptions=True)

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper


class AioHttpCrawl:
    def __init__(self, loop=None):
        self.future_list = []
        self.loop = loop or asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def __enter__(self):
        return self

    def __del__(self):
        self.loop.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.loop.close()

    @log_decorator
    async def __add_tasks(self, session, url, method, index=None, *args, **kwargs):
        """运行任务"""
        kwargs.setdefault('headers', Head().randua)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))
        # cookies = kwargs.pop('cookies', {})
        callback = kwargs.pop('callback', None)
        index = index or id(url)

        @TRETRY
        async def __fetch(session):
            # async with ClientSession(cookies=cookies, connector=TCPConnector(ssl=False)) as session,session.request(method, url, raise_for_status=True, *args, **kwargs) as response:
            async with session.request(method, url, raise_for_status=True, *args, **kwargs) as response:
                content = await response.read()
                return response, content

        try:
            response, content = await __fetch(session)
            result = htmlResponse(response, content, index)
            return callback(result) if callable(callback) else result
        except Exception as err:
            print(f'AioCrawl_run_task:{self} | RetryErr:{err!r}')
            return [index, err, '']

    async def _add_tasks(self, url_list, method, *args, **kwargs):
        """分发任务"""
        callback = kwargs.pop('fu_callback', None)
        cookies = kwargs.pop('cookies', {})
        _session = ClientSession(cookies=cookies, connector=TCPConnector(ssl=False))

        for index, url in enumerate(url_list, 1):
            task = asyncio.create_task(self.__add_tasks(_session, url, method=method, index=index, *args, **kwargs))
            if callback:
                task.add_done_callback(callback)
            self.future_list.append(task)

        result = await asyncio.gather(*self.future_list, return_exceptions=True)
        await _session.close()

        return result

    def add_tasks(self, url_list, method='GET', *args, **kwargs):
        """添加网址列表,异步并发爬虫，返回结果列表，可用wait_completed取结果"""
        return self.loop.run_until_complete(self._add_tasks(url_list, method=method, *args, **kwargs))

    async def _add_pool(self, func, *args, **kwargs):
        callback = kwargs.pop('fu_callback', None)
        with ThreadPoolExecutor(32) as executor:
            for arg in list(zip(*args)):
                task = self.loop.run_in_executor(executor, func, *arg, **kwargs)
                if callback:
                    task.add_done_callback(callback)
                self.future_list.append(task)

        return await asyncio.gather(*self.future_list, return_exceptions=True)

    def add_pool(self, func, *args, **kwargs):
        """添加函数及参数,异步运行，可用wait_completed取结果"""
        return self.loop.run_until_complete(self._add_pool(func, *args, **kwargs))

    def wait_completed(self):
        if len(self.future_list) == 0:
            return []
        while any(fu._state == 'PENDING' for fu in self.future_list):
            continue
        result_list = [fu.result() for fu in self.future_list]
        self.future_list.clear()
        return result_list


if __name__ == '__main__':
    ...
    # $add_tasks#######################################################
    myaio = AioHttpCrawl()
    url_list = ['https://www.163.com', 'https://www.126.com', 'https://www.qq.com']
    # print(111111, myaio.add_tasks(url_list * 1))
    # print(111111, myaio.wait_completed())
    # print(222222, myaio.add_tasks(url_list * 1))
    # print(222222, myaio.wait_completed())
    # $add_func########################################################
    from xt_Requests import get

    print(333333, myaio.add_pool(get, ['https://httpbin.org/get'] * 3))
    # print(333333, myaio.wait_completed())

    # $装饰器##########################################################
    @async_inexecutor_decorator
    def get_html(url):
        return get(url)

    # print(444444, get_html('https://www.baidu.com'))

    @async_inexecutor_decorator
    async def get_a_html(url):
        return get(url)

    # print(555555, get_a_html('https://cn.bing.com/'))

    @async_inexecutor_decorator
    async def get_message():
        async with ClientSession() as session, session.get('https://httpbin.org/get') as response:
            return await response.text()

    # print(666666, get_message())
