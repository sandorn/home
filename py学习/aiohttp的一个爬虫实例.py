# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-15 10:54:35
FilePath     : /CODE/py学习/asyncio学习/aiohttp的一个爬虫实例.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup


class AsnycGrab(object):

    def __init__(self, url_list, max_threads):
        self.urls = url_list
        self.results = {}
        self.max_threads = max_threads

    def __parse_results(self, url, html):
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title').get_text()
        except Exception as e:
            raise e

        if title:
            self.results[url] = title

    async def get_body(self, url):
        async with ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    html = await response.read()
                    return response.url, html

    async def get_results(self, url):
        url, html = await self.get_body(url)
        self.__parse_results(url, html)
        return 'Completed'

    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()
            try:
                task_status = await self.get_results(current_url)
            except Exception as e:
                logging.exception(f'Error for {current_url}', exc_info=True)

    def start_loop(self):
        que = asyncio.Queue()
        [que.put_nowait(url) for url in self.urls]
        loop = asyncio.get_event_loop()
        tasks = [self.handle_tasks(
            task_id,
            que,
        ) for task_id in range(self.max_threads)]
        loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()


if __name__ == '__main__':
    async_example = AsnycGrab(['http://www.baidu.com', 'https://www.sina.com.cn', 'https://www.163.com/', 'https://www.zhihu.com/'], 5)
    async_example.start_loop()
    print(async_example.results)
'''
————————————————
版权声明：本文为CSDN博主「天痕坤」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/kun1280437633/article/details/80685334
'''
