# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-29 09:51:29
#FilePath     : /xjLib/test/requests--test.py
#LastEditTime : 2020-07-01 10:21:46
#Github       : https://github.com/sandorn/home
#==============================================================
aiohttp笔记 - happy_codes - 博客园
https://www.cnblogs.com/haoabcd2010/p/10615364.html
'''
import asyncio
from threading import Thread

from aiohttp import ClientSession, ClientTimeout, TCPConnector

from xt_Head import MYHEAD
from xt_Response import ReqResult
from xt_Requests import TRETRY as RETRY

# from xt_Log import mylog
# print = mylog.warn

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

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        # self.event_loop.stop()

    async def fetch(self,
                    url,
                    index=None,
                    method='GET',
                    headers=MYHEAD,
                    timeout=TIMEOUT,
                    cookies=None,
                    data=None):

        self.response = self.content = None  # #存放结果
        # #初始化参数
        index = index if index else id(url)
        data = data if data and isinstance(data, dict) else {}
        timeout = ClientTimeout(timeout)

        @RETRY
        async def _fetch_run():
            tcpc = TCPConnector(ssl=False)  # 禁用证书验证
            async with ClientSession(headers=headers,
                                     timeout=timeout,
                                     cookies=cookies,
                                     connector=tcpc) as session:
                async with session.request(method, url, params=data,
                                           json=data) as self.response:
                    self.content = await self.response.read()
                    assert self.response.status in [200, 201, 302]
                    return self.response, self.content

        # #循环抓取
        try:
            await _fetch_run()
        except Exception as err:
            print(f'AioCrawl.fetch:{url}; Err:{repr(err)}')
        finally:
            # #返回结果,不管是否正确
            self.concurrent -= 1  # 并发数-1
            new_res = ReqResult(self.response, self.content, index)
            return new_res

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

    def add_task(self, task):
        """添加单个任务"""
        if not self.event_loop.is_running():
            raise 'event_loop is stop!'

        future = asyncio.run_coroutine_threadsafe(task, self.event_loop)
        self.future_list.append(future)
        self.concurrent += 1  # 并发数加 1

    def add_fetch_tasks(self, tasks):
        """添加任务,传入url+index列表"""
        if not self.event_loop.is_running():
            raise 'event_loop is stop!'

        for task in tasks:
            if isinstance(task, (list, tuple)):
                future = asyncio.run_coroutine_threadsafe(
                    self.fetch(*task), self.event_loop)
            else:
                future = asyncio.run_coroutine_threadsafe(
                    self.fetch(task), self.event_loop)
            self.future_list.append(future)
            self.concurrent += 1  # 并发数加 1


if __name__ == '__main__':
    a = AioCrawl()

    for _ in range(2):
        a.add_tasks(['https://www.baidu.com' for _ in range(2)])  # 模拟动态添加任务

    t = a.wait_completed()
    for i in t:
        print(i)

    for _ in range(2):
        a.add_tasks(['https://httpbin.org/get' for _ in range(2)])  # 模拟动态添加任务

    t1 = a.wait_completed()
    for i in t1:
        print(i)
