# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-18 13:07:41
FilePath     : /CODE/项目包/线程小成果/笔趣阁-asyncio.py
Github       : https://github.com/sandorn/home
==============================================================
顺讯，单独，速度慢
'''

import asyncio
import os

import aiohttp
from xt_File import savefile
from xt_Ls_Bqg import clean_Content
from xt_Response import htmlResponse
from xt_String import Str_Replace
from xt_Time import timeit


async def fetch(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(
            ssl=False)) as sess:
        async with sess.get(url) as response:
            content = await response.read()
    return htmlResponse(response, content)


async def get_down_url(url):
    urls = []
    resp = await fetch(url)
    _xpath = (
        "//h2/text()",
        "//dt[2]/following-sibling::dd/a/@href",
        "//dt[2]/following-sibling::dd/a/text()",
    )
    bookname, temp_urls, titles = resp.xpath(_xpath)

    bookname = bookname[0]
    baseurl = '/'.join(url.split('/')[:-2])
    urls = [baseurl + item for item in temp_urls]  # # 章节链接
    return bookname, urls, titles


texts = []  # 将爬下来的小说都存在里面，做最后排序


async def get_contents(index, url):
    resp = await fetch(url)
    title = resp.pyquery("h1").text()
    content = resp.pyquery("#content").text()

    title = Str_Replace("".join(title), [(u'\u3000', u' '), (u'\xa0', u' '),
                                         (u'\u00a0', u' ')])
    content = clean_Content(content)
    # return [index, title, content]
    texts.append([index, title, content])


@timeit
def main_thread(url):

    bookname, urls, _ = asyncio.run(get_down_url(url))

    tasks = [get_contents(index, url) for index, url in enumerate(urls)]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*tasks))

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}_asyncio.txt', texts, br='\n')


if __name__ == '__main__':
    main_thread('https://www.biqukan8.cc/0_288/')
