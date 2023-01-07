# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================

Description  :  Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-09 16:23:50
LastEditTime : 2022-12-09 16:23:50
FilePath     : /xjLib/xt_Ext_Asyncio.py
Github       : https://github.com/sandorn/home
==============================================================
aiohttp笔记 - happy_codes - 博客园
https://www.cnblogs.com/haoabcd2010/p/10615364.html
'''
import asyncio
from asyncio.coroutines import iscoroutine
from functools import wraps
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from xt_Head import Headers
from xt_Requests import TRETRY
from xt_Response import htmlResponse

# 默认超时时间
TIMEOUT = 20


def future_wrapper(func):
    '''future装饰器'''

    @wraps(func)
    def __future(*args, **kwargs):
        future = asyncio.Future()
        result = func(*args, **kwargs)
        future.set_result(result)
        return future

    return __future


def asyncio_wrapper(func):
    '''异步装饰器,可装饰async函数和普通函数,,但是不能装饰协程'''

    @wraps(func)
    def _wrapper(*args, **kwargs):

        async def __wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if iscoroutine(result):
                result = await asyncio.create_task(func(*args, **kwargs))
            return result

        return asyncio.run(__wrapper(*args, **kwargs))

    return _wrapper


class AioCrawl:

    def __init__(self):
        # 启动事件循环
        self.event_loop = asyncio.new_event_loop()
        self.thr = Thread(
            target=self.start_loop,
            daemon=True,
        )
        self.thr.start()

        self.future_list = []
        self.result_list = []
        self.concurrent = 0  # 记录并发数

    def __del__(self):
        self.close_loop()

    def start_loop(self):
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_forever()

    def close_loop(self):
        self.event_loop.stop()
        self.event_loop.close()

    def close(self):
        self.close_loop()

    def stop(self):
        self.close_loop()

    async def _fetch(self, url, method='GET', *args, **kwargs):

        @TRETRY
        async def _fetch_run():
            async with TCPConnector(ssl=False) as Tconn, ClientSession(cookies=cookies, connector=Tconn) as session, session.request(method, url, raise_for_status=True, *args, **kwargs) as response:
                content = await response.read()
                return response, content

        try:
            kwargs.setdefault('headers', Headers().randomheaders)
            kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
            cookies = kwargs.pop("cookies", {})
            callback = kwargs.pop("callback", None)
            response, content = await _fetch_run()
        except Exception as err:
            print(f'AioCrawl_fetch:{url} | RetryErr:{err!r}')
            return None
        else:
            # #返回结果,不管是否正确
            result = htmlResponse(response, content)
            if callback: result = callback(result)
            return result

    def add_fetch_tasks(self, url_list, *args, **kwargs):
        """添加任务
        :param url_list: list <class url>
        :return: future
        """
        callback = kwargs.pop("future_callback", None)
        method = kwargs.pop("method", 'GET')

        for url in url_list:
            # asyncio.run_coroutine_threadsafe:接收协程对象、事件循环对象
            if not isinstance(url, str): continue
            future = asyncio.run_coroutine_threadsafe(self._fetch(url, method=method, *args, **kwargs), self.event_loop)
            self.future_list.append(future)
            if callback: future.add_done_callback(callback)  # 给future对象添加回调函数
            self.concurrent += 1  # 并发数加 1

    def add_tasks(self, tasks, callback=None):
        """添加纤程任务"""
        if not isinstance(tasks, (list, tuple)): raise TypeError('传入非list或tuple')
        for task in tasks:
            print(11111111111, type(task))
            if not iscoroutine(task): continue
            future = asyncio.run_coroutine_threadsafe(task, self.event_loop)
            self.future_list.append(future)
            if callback: future.add_done_callback(callback)  # 给future对象添加回调函数
            self.concurrent += 1  # 并发数加 1

    def getAllResult(self):
        for _ in range(len(self.future_list)):
            future = self.future_list.pop()
            res = future.result()
            self.result_list.append(res)
            self.concurrent -= 1  # 并发数-1

        res, self.result_list = self.result_list, []
        return res

    def wait_completed(self):
        while True:
            tmp = [fu._state for fu in self.future_list]
            if 'PENDING' in tmp: continue
            else: break

        return self.getAllResult()


if __name__ == '__main__':
    #########################################################################
    # a = AioCrawl()
    # for _ in range(3):
    #     a.add_fetch_tasks(["https://httpbin.org/get"])  # 模拟动态添加任务
    # print(222222222222222, a.getAllResult())
    #########################################################################
    # from xt_Ahttp import asynctask_run, get  # $配合ahttp使用

    # b = AioCrawl()
    # tasks = [asynctask_run(get('https://httpbin.org/get')) for _ in range(2)]
    # b.add_tasks(tasks)  # 模拟动态添加任务

    # res = b.getAllResult()
    # for item in res:
    #     print(item)
    #########################################################################
    # from xt_Requests import get

    # b = AioCrawl()

    # async def test(url):
    #     return get(url)

    # b.add_tasks([test('https://httpbin.org/get') for _ in range(2)])  # 模拟动态添加任务

    # res = b.getAllResult()
    # for item in res:
    #     print(item)

    #########################################################################
    from xt_Requests import get

    @asyncio_wrapper
    def get_html(url):
        return get(url)

    res = get_html('https://httpbin.org/get')
    print(res)

    @asyncio_wrapper
    async def get_message():
        async with ClientSession() as session:
            async with session.get('http://httpbin.org/headers') as response:
                return await response.text()

    res = get_message()
    print(res)
