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
from asyncio.coroutines import iscoroutine, iscoroutinefunction
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


def async_wrapper(func):
    '''异步装饰器,装饰普通函数,返回coroutine'''

    @wraps(func)
    async def _wrapper(*args, **kwargs):
        await asyncio.sleep(0.01)
        return func(*args, **kwargs)

    return func if iscoroutinefunction(func) else _wrapper


def fun_runin_async(func):
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

    def __init__(self):
        self.future_list = []
        self.result_list = []
        self.concurrent = 0  # 记录并发数

    #     self.event_loop = asyncio.new_event_loop()
    #     Thread(target=self.star_loop, name='AioCrawl.__init__', daemon=True).start()

    # def star_loop(self):
    #     self.event_loop.run_forever()

    # def close_loop(self):
    #     self.event_loop.stop()
    #     self.event_loop.close()

    # def close(self):
    #     self.close_loop()

    # def __del__(self):
    #     self.close_loop()

    async def _task_run(self, url, method='GET', index=None, *args, **kwargs):
        '''运行任务'''

        @TRETRY
        async def __fetch():
            async with TCPConnector(ssl=False) as Tconn, ClientSession(cookies=cookies, connector=Tconn) as session, session.request(method, url, raise_for_status=True, *args, **kwargs) as response:
                content = await response.read()
                return response, content

        try:
            kwargs.setdefault('headers', Headers().randomheaders)
            kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
            cookies = kwargs.pop("cookies", {})
            callback = kwargs.pop("callback", None)
            # import threading
            # print(f'Count:{threading.active_count()} | {threading.current_thread()}')
            response, content = await __fetch()
        except Exception as err:
            print(f'_task_run:{self} | RetryErr:{err!r}')
            return None
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
            self.concurrent += 1  # 并发数加 1

        return await asyncio.gather(*self.future_list)

    def add_tasks(self, url_list, method='GET', *args, **kwargs):
        _coroutine = self._issue_tasks(url_list, method=method, *args, **kwargs)
        return asyncio.run(_coroutine)

    def _get_result(self):
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

        return self._get_result()


if __name__ == '__main__':
    ...
    #$add_tasks#######################################################################
    a = AioCrawl()
    a.add_tasks(["https://httpbin.org/get"] * 3)
    print(a.wait_completed())
    a.add_tasks(["https://httpbin.org/post"] * 3, method='post')
    print(a.wait_completed())
    #$装饰器#######################################################################
    # from xt_Requests import get_wraps

    # @fun_runin_async
    # def get_html(url):
    #     return get_wraps(url)

    # res = get_html('https://httpbin.org/get')
    # print(res)

    # @fun_runin_async
    # async def get_a_html(url):
    #     return get_wraps(url)

    # res = get_a_html('https://httpbin.org/get')
    # print(res)

    # @fun_runin_async
    # async def get_message():
    #     async with ClientSession() as session, session.get('http://httpbin.org/headers') as response:
    #         return await response.text()

    # res = get_message()
    # print(res)
