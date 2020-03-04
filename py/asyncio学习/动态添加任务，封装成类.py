# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-04 19:16:05
@LastEditors: Even.Sand
@LastEditTime: 2020-03-04 19:20:19
https://www.cnblogs.com/haoabcd2010/p/10615364.html
'''
import asyncio
import logging
import time
from threading import Thread
from aiohttp import ClientSession, ClientTimeout, TCPConnector


# 默认请求头
HEADERS = {
    'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


# 默认超时时间
TIMEOUT = 15


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


class AioCrawl:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # 启动事件循环
        self.event_loop = asyncio.new_event_loop()
        self.t = Thread(target=start_loop, args=(self.event_loop,))
        self.t.setDaemon(True)
        self.t.start()

        self.concurrent = 0  # 记录并发数

    async def fetch(self, url, method='GET', headers=None, timeout=TIMEOUT, cookies=None, data=None, proxy=None):
        """采集纤程
        :param url: str
        :param method: 'GET' or 'POST'
        :param headers: dict()
        :param timeout: int
        :param cookies:
        :param data: dict()
        :param proxy: str
        :return: (status, content)
        """

        method = 'POST' if method.upper() == 'POST' else 'GET'
        headers = headers if headers else HEADERS
        timeout = ClientTimeout(total=timeout)
        cookies = cookies if cookies else None
        data = data if data and isinstance(data, dict) else {}

        tcp_connector = TCPConnector(ssl=False)  # 禁用证书验证
        async with ClientSession(headers=headers, timeout=timeout, cookies=cookies, connector=tcp_connector) as session:
            try:
                if method == 'GET':
                    async with session.get(url, proxy=proxy) as response:
                        content = await response.read()
                        return response.status, content
                else:
                    async with session.post(url, data=data, proxy=proxy) as response:
                        content = await response.read()
                        return response.status, content
            except Exception as e:
                raise e

    def callback(self, future):
        """回调函数
        1.处理并转换成Result对象
        2.写数据库
        """
        msg = str(future.exception()) if future.exception() else 'success'
        code = 1 if msg == 'success' else 0
        status = future.result()[0] if code == 1 else None
        data = future.result()[1] if code == 1 else b''  # 空串

        data_len = len(data) if data else 0
        if code == 0 or (status is not None and status != 200):  # 打印小异常
            self.logger.warning('<url="{}", code={}, msg="{}", status={}, data(len):{}>'.format(
                future.url, code, msg, status, data_len))

        self.concurrent -= 1  # 并发数-1

        print(len(data))

    def add_tasks(self, tasks):
        """添加任务
        :param tasks: list <class Task>
        :return: future
        """
        for task in tasks:
            # asyncio.run_coroutine_threadsafe 接收一个协程对象和，事件循环对象
            future = asyncio.run_coroutine_threadsafe(self.fetch(task), self.event_loop)
            future.add_done_callback(self.callback)  # 给future对象添加回调函数
            self.concurrent += 1  # 并发数加 1


if __name__ == '__main__':
    a = AioCrawl()

    for _ in range(5):
        a.add_tasks(['https://www.baidu.com' for _ in range(2)])  # 模拟动态添加任务
        time.sleep(1)
