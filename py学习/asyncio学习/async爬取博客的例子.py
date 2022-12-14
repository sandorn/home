# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-12 15:21:22
@LastEditors: Even.Sand
@LastEditTime: 2020-03-20 18:12:34
异步爬虫: async/await 与 aiohttp的使用，以及例子_Python_Multiangle's Notepad-CSDN博客
https://blog.csdn.net/u014595019/article/details/52295642
'''
import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs


async def getPage(url, res_list):
    print(url)
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    # conn = aiohttp.ProxyConnector(proxy="http://127.0.0.1:8087")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            assert resp.status == 200
            res_list.append(await resp.text())


class parseListPage():
    def __init__(self, page_str):
        self.page_str = page_str

    def __enter__(self):
        page_str = self.page_str
        page = bs(page_str, 'lxml')
        # 获取文章链接
        articles = page.find_all('div', attrs={'class': 'article_title'})
        art_urls = []
        for a in articles:
            x = a.find('a')['href']
            art_urls.append('http://blog.csdn.net' + x)
        return art_urls

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


page_num = 5
page_url_base = 'http://blog.csdn.net/u014595019/article/list/'
page_urls = [page_url_base + str(i + 1) for i in range(page_num)]
loop = asyncio.get_event_loop()
ret_list = []
tasks = [getPage(host, ret_list) for host in page_urls]
loop.run_until_complete(asyncio.wait(tasks))

articles_url = []
for ret in ret_list:
    with parseListPage(ret) as tmp:
        articles_url += tmp
ret_list = []

tasks = [getPage(url, ret_list) for url in articles_url]
loop.run_until_complete(asyncio.wait(tasks))
