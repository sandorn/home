# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-29 09:51:29
#FilePath     : /xjLib/xt_Asyncio.py
#LastEditTime : 2020-07-22 13:28:33
#Github       : https://github.com/sandorn/home
#==============================================================
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
from xt_Requests import TRETRY

TIMEOUT = 20
RETRY_TIME = 6  # 最大重试次数


class AioCrawl:
    def __init__(self):
        '''启动事件循环'''
        self.event_loop = asyncio.new_event_loop()
        self.thr = Thread(target=self.start_loop, args=(self.event_loop, ))
        self.thr.setDaemon(True)
        self.thr.start()

        self.future_list = []
        self.result_list = []
        self.concurrent = 0  # 记录并发数
        self.Timeout_exc = False

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        # self.event_loop.stop()

    async def fetch(self, url, index=None, **kwargs):
        @TRETRY
        async def _fetch_run():
            async with TCPConnector(ssl=False) as Tconn, ClientSession(cookies=cookies, connector=Tconn) as session, session.request(method, url, raise_for_status=True, **kwargs) as self.response:
                self.content = await self.response.read()
                return self.response, self.content

        # #初始化参数
        kwargs.setdefault('headers', MYHEAD)
        kwargs.setdefault('timeout', ClientTimeout(TIMEOUT))  # @超时
        kwargs.setdefault('verify_ssl', False)

        index = index or id(url)
        cookies = kwargs.pop('cookies', {})
        method = kwargs.pop('method', 'get')
        callback = kwargs.pop("callback", None)

        # #循环抓取
        try:
            await _fetch_run()
        except Exception as err:
            print(f'AioCrawl.fetch:{url}; Err:{err!r}')
            self.concurrent -= 1  # 并发数-1
            self.result = None
            return None
        else:
            # #返回正确结果
            self.concurrent -= 1  # 并发数-1
            self.result = ReqResult(self.response, self.content, index)
            if callback:  # 有回调则调用
                self.result = callback(self.result)
            return self.result

    def getAllResult(self):
        for _ in range(len(self.future_list)):
            future = self.future_list.pop()
            res = future.result()
            self.result_list.append(res)

        res, self.result_list = self.result_list, []
        return res

    def wait_completed(self):
        while True:
            tmp = [fu._state for fu in self.future_list]
            if 'PENDING' in tmp:
                continue
            else:
                break

        for _ in range(len(self.future_list)):
            future = self.future_list.pop()
            res = future.result()
            self.result_list.append(res)

        res, self.result_list = self.result_list, []
        return res

    def add_tasks(self, tasks):
        """添加纤程任务"""
        if not isinstance(tasks, (list, tuple)):
            raise Exception('传入非list或tuple')

        for task in tasks:
            if not (iscoroutine(task)): continue
            future = asyncio.run_coroutine_threadsafe(task, self.event_loop)
            self.future_list.append(future)
            self.concurrent += 1  # 并发数加 1

    def add_fetch_tasks(self, tasks, **kwargs):
        """添加任务,传入url+index列表"""
        if not isinstance(tasks, (list, tuple)):
            raise Exception('传入非list或tuple')

        for index, task in enumerate(tasks):
            if isinstance(task, (list, tuple)):
                '''list传入多个参数,拆解'''
                future = asyncio.run_coroutine_threadsafe(self.fetch(*task, **kwargs), self.event_loop)

            elif isinstance(task, str):
                '''单一字符串参数,识别为url,添加序号'''
                future = asyncio.run_coroutine_threadsafe(self.fetch(task, index + 1, **kwargs), self.event_loop)

            self.future_list.append(future)
            self.concurrent += 1  # 并发数加 1


def make_future(func):
    '''协程装饰器'''
    @wraps(func)
    def _make_future(*args, **kwargs):
        future = asyncio.Future()
        result = func(*args, **kwargs)
        future.set_result(result)
        return future

    return _make_future


if __name__ == '__main__':
    a = AioCrawl()

    for _ in range(2):
        a.add_fetch_tasks(['https://www.baidu.com' for _ in range(2)])  # 模拟动态添加任务

    t = a.wait_completed()
    for i in t:
        print(i)

    for _ in range(2):
        a.add_fetch_tasks(['https://httpbin.org/get' for _ in range(2)])  # 模拟动态添加任务

    t1 = a.wait_completed()
    for i in t1:
        print(i)
