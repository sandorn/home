# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-10 17:03:29
FilePath     : /xjLib/xt_Asyncio.py
Github       : https://github.com/sandorn/home
==============================================================
aiohttp笔记 - happy_codes - 博客园
https://www.cnblogs.com/haoabcd2010/p/10615364.html
'''
import asyncio
from asyncio.coroutines import iscoroutinefunction
from asyncio.proactor_events import _ProactorBasePipeTransport
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_Head import TIMEOUT, Head
from xt_Requests import TRETRY
from xt_Response import htmlResponse


def silence_event_loop_closed(func):
    '''解决event loop is closed问题'''

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


def future_wrapper(func):
    '''future装饰器'''

    @wraps(func)
    def __future(*args, **kwargs):
        future = asyncio.Future()
        result = func(*args, **kwargs)
        future.set_result(result)
        return future

    return __future


def async_wrapper(func):
    '''异步装饰器,装饰普通函数,返回coroutine'''

    @wraps(func)
    async def _wrapper(*args, **kwargs):
        await asyncio.sleep(0.01)
        return func(*args, **kwargs)

    return func if iscoroutinefunction(func) else _wrapper


def asyn_run_wrapper(func):
    '''异步装饰器,装饰函数和async函数,直接运行,返回结果'''

    @wraps(func)
    def _wrapper(*args, **kwargs):

        @wraps(func)
        async def __wrapper(*args, **kwargs):
            if iscoroutinefunction(func):
                return await asyncio.create_task(func(*args, **kwargs))
            else:
                return await asyncio.create_task(async_wrapper(func)(*args, **kwargs))

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper


class AioCrawl:

    def __init__(self, loop=None):
        self.future_list = []
        self.result_list = []
        self.loop = loop or asyncio.get_event_loop()

    def __del__(self):
        self.loop.close()

    async def _task_run(self, url, method='GET', index=None, *args, **kwargs):
        '''运行任务'''
        kwargs.setdefault('headers', Head().randua)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))
        cookies = kwargs.pop("cookies", {})
        callback = kwargs.pop("callback", None)

        @TRETRY
        async def __fetch():
            async with ClientSession(cookies=cookies, connector=TCPConnector(ssl=False)) as session, session.request(method, url, raise_for_status=True, *args, **kwargs) as response:
                content = await response.read()
                return response, content

        try:
            response, content = await __fetch()
        except Exception as err:
            print(f'AioCrawl_task_run:{self} | RetryErr:{err!r}')
            return err
        else:
            index = index or id(url)
            result = htmlResponse(response, content, index)
            if callback: result = callback(result)
            return result

    async def _issue_tasks(self, url_list, method='GET', *args, **kwargs):
        """分发任务"""
        callback = kwargs.pop("fu_callback", None)

        for index, url in enumerate(url_list, 1):
            if not isinstance(url, str): continue
            task = asyncio.create_task(self._task_run(url, method=method, index=index, *args, **kwargs))
            if callback: task.add_done_callback(callback)
            self.future_list.append(task)

        return await asyncio.gather(*self.future_list, return_exceptions=True)

    def add_tasks(self, url_list, method='GET', *args, **kwargs):
        '''添加网址列表,异步并发爬虫'''
        _coroutine = self._issue_tasks(url_list, method=method, *args, **kwargs)
        return asyncio.run(_coroutine)
        # self.loop.run_until_complete(_coroutine)  # 异常中断

    async def _func_run(self, func, *args, **kwargs):
        executor = ThreadPoolExecutor(32)
        args = list(zip(*args))
        for arg in args:
            task = self.loop.run_in_executor(executor, func, *arg, **kwargs)
            self.future_list.append(task)
        await asyncio.gather(*self.future_list)

    def add_func(self, func, *args, **kwargs):
        '''添加函数及参数,异步运行'''
        self.loop.run_until_complete(self._func_run(func, *args, **kwargs))

    def __get_result(self):
        for _ in range(len(self.future_list)):
            future = self.future_list.pop()
            res = future.result()
            self.result_list.append(res)

        res, self.result_list = self.result_list, []
        return res

    def wait_completed(self):
        while True:
            tmp = [fu._state for fu in self.future_list]
            if 'PENDING' in tmp: continue
            else: break

        return self.__get_result()


if __name__ == '__main__':
    ...
    #$add_tasks#######################################################################
    # bb = AioCrawl()
    # bb.add_tasks(["https://httpbin.org/get"] * 3)
    # print(bb.wait_completed())
    # bb.add_tasks(["https://httpbin.org/post"] * 3, method='post')
    # print(bb.wait_completed())
    #$add_func#######################################################################
    # from xt_Requests import get_wraps

    # bb = AioCrawl()
    # bb.add_func(get_wraps, ["https://httpbin.org/get"] * 3)
    # print(bb.wait_completed())
    # bb.add_tasks(["https://httpbin.org/post"] * 3, method='post')
    # print(bb.wait_completed())
    #$装饰器#######################################################################
    from xt_Requests import get_wraps

    @asyn_run_wrapper
    def get_html(url):
        return get_wraps(url)

    # print(111, get_html('https://httpbin.org/get'))

    @asyn_run_wrapper
    async def get_a_html(url):
        return get_wraps(url)

    print(222, get_a_html('https://httpbin.org/get'))

    @asyn_run_wrapper
    async def get_message():
        async with ClientSession() as session, session.get('http://httpbin.org/headers') as response:
            return await response.text()

    print(333, get_message())
