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

from xt_Requests import get

TIMEOUT = 20


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
        # self.Timeout_exc = False

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        # self.event_loop.stop()

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
            if not iscoroutine(task): continue
            future = asyncio.run_coroutine_threadsafe(task, self.event_loop)
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
    b = AioCrawl()

    for _ in range(2):
        a.add_tasks([get('https://www.baidu.com') for _ in range(2)])  # 模拟动态添加任务

    res = a.getAllResult()
    for item in res:
        print(item)

    for _ in range(2):
        b.add_tasks([get('https://httpbin.org/get') for _ in range(2)])  # 模拟动态添加任务

    res_b = b.getAllResult()
    for i in res_b:
        print(i)
