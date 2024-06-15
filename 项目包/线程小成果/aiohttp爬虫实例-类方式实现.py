# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-15 08:03:28
FilePath     : /CODE/项目包/线程小成果/aiohttp爬虫实例-类方式实现.py
Github       : https://github.com/sandorn/home
==============================================================
#@待完善
"""

import asyncio
import os

from aiohttp import ClientSession
from xt_File import savefile
from xt_Ls_Bqg import Str_Replace, clean_Content
from xt_Requests import Head, htmlResponse


class AsnycGrab:
    def __init__(self, url_list, max_threads=36):
        self.urls = url_list
        self.results = []
        self.max_threads = max_threads
        self.url = url_list[0]

    async def get_body(self, url, index=None):
        async with ClientSession() as session:
            async with session.get(url, headers=Head().randua, timeout=30) as response:
                if response.status == 200:
                    html = await response.read()
                    return htmlResponse(response, html, index)

    async def get_text(self, url, index=None):
        resp = await self.get_body(url, index)
        _xpath = ('//h1/text()', '//*[@id="chaptercontent"]/text()')
        _title, _showtext = resp.xpath(_xpath)
        title = Str_Replace(''.join(_title), [('\u3000', ' '), ('\xa0', ' '), ('\u00a0', ' ')])
        content = clean_Content(_showtext)
        self.results.append([index, title, content])
        return [index, title, content]

    async def handle_tasks(self, task_id, work_queue):
        index = 1
        while not work_queue.empty():
            current_url = await work_queue.get()
            self.task_status = await self.get_text(current_url, f'{index}|{task_id}')
            index += 1

    async def getlink(self, url):
        resp = await self.get_body(url)
        _xpath = [
            '//h1/text()',
            '//dt[1]/following-sibling::dd/a/@href',
            '//dt[1]/following-sibling::dd/a/text()',
        ]
        bookname, temp_urls, self.titles = resp.xpath(_xpath)
        self.bookname = bookname[0]
        baseurl = '/'.join(url.split('/')[:-2])
        self.zj_urls = [baseurl + item for item in temp_urls]
        return self.zj_urls

    def start_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.getlink(self.url))

        que = asyncio.Queue()
        [que.put_nowait(url) for url in self.zj_urls]
        tasks = [
            self.handle_tasks(
                task_id,
                que,
            )
            for task_id in range(self.max_threads)
        ]
        loop.run_until_complete(asyncio.wait(tasks))

        self.results.sort(key=lambda x: x[0])
        files = os.path.basename(__file__).split('.')[0]
        savefile(f'{files}&{self.bookname}AsnycGrab.txt', self.results, br='\n')


if __name__ == '__main__':
    url_list = [
        'https://www.bigee.cc/book/6909/',  # 11s
    ]
    async_example = AsnycGrab(url_list)
    async_example.start_loop()
