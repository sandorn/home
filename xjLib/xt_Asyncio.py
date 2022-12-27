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
from xt_Head import MYHEAD
from xt_Response import ReqResult

# 默认超时时间
TIMEOUT = 20


def make_future(func):
    '''协程装饰器'''

    @wraps(func)
    def _make_future(*args, **kwargs):
        future = asyncio.Future()
        result = func(*args, **kwargs)
        future.set_result(result)
        return future

    return _make_future


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

    def start_loop(self):
        asyncio.set_event_loop(self.event_loop)
        self.event_loop.run_forever()
        # self.event_loop.stop()

    async def fetch(self, url, method='GET', headers=None, timeout=TIMEOUT, cookies=None, data=None, proxy=None):
        """采集纤程
        :param url: str
        :param method: 'GET' or 'POST'
        :param headers: dict()
        :param timeout: int
        :param cookies:
        :param data: dict()
        :param proxy: str
        :return: ReqResult(response, content)
        """

        method = 'POST' if method.upper() == 'POST' else 'GET'
        headers = headers or MYHEAD
        timeout = ClientTimeout(total=timeout)
        cookies = cookies or None
        data = data if data and isinstance(data, dict) else {}

        tcp_connector = TCPConnector(ssl=False)  # 禁用证书验证
        async with ClientSession(headers=headers, timeout=timeout, cookies=cookies, connector=tcp_connector) as session:
            try:
                if method == 'GET':
                    async with session.get(url, proxy=proxy) as response:
                        content = await response.read()
                        return ReqResult(response, content)
                else:
                    async with session.post(url, data=data, proxy=proxy) as response:
                        content = await response.read()
                        return ReqResult(response, content)
            except Exception as e:
                raise e

    def add_fetch_tasks(self, url_list, callback=None):
        """添加任务
        :param url_list: list <class url>
        :return: future
        """
        for url in url_list:
            # asyncio.run_coroutine_threadsafe  # #接收一个协程对象和，事件循环对象
            future = asyncio.run_coroutine_threadsafe(self.fetch(url), self.event_loop)
            self.future_list.append(future)
            if callback: future.add_done_callback(callback)  # 给future对象添加回调函数
            self.concurrent += 1  # 并发数加 1

    def add_tasks(self, tasks, callback=None):
        """添加纤程任务"""
        if not isinstance(tasks, (list, tuple)): raise TypeError('传入非list或tuple')

        for task in tasks:
            if not iscoroutine(task): continue
            future = asyncio.run_coroutine_threadsafe(task, self.event_loop)
            self.future_list.append(future)
            if callback: future.add_done_callback(callback)  # 给future对象添加回调函数

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

    from xt_Requests import get

    b = AioCrawl()

    async def test():
        return get('https://www.baidu.com')

    b.add_tasks([test() for _ in range(2)])  # 模拟动态添加任务

    res = b.getAllResult()
    for item in res:
        print(item)

#########################################################################
# a = AioCrawl()

# for _ in range(5):
#     a.add_fetch_tasks(['https://www.sina.com.cn' for _ in range(2)])  # 模拟动态添加任务

# print(222222222222222, a.getAllResult())
#########################################################################
# from xt_Ahttp import Async_run, get  # $配合ahttp使用

# b = AioCrawl()
# asynctasks = []
# for _ in range(2):
#     task = get('https://www.baidu.com')
#     asynctasks.append(task)
# tasks = [Async_run(task) for task in asynctasks]

# b.add_tasks(tasks)  # 模拟动态添加任务

# res = b.getAllResult()
# for item in res:
#     print(item)
#########################################################################
# from xt_Requests import get

# b = AioCrawl()

# async def test():
#     return get('https://www.baidu.com')

# b.add_tasks([test() for _ in range(2)])  # 模拟动态添加任务

# res = b.getAllResult()
# for item in res:
#     print(item)

#########################################################################
# from xt_Requests import get

# @make_future
# def gethtml(url):
#     return get(url)

# res = gethtml('https://www.baidu.com')
# print(res.result())
