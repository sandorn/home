# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-15 09:30:53
FilePath     : /CODE/py学习/asyncio学习/异步结合多进程-爬虫程序.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import asyncio
import time
from multiprocessing import Pool

import aiohttp
from lxml import etree

urls = [
    'https://www.sina.com.cn',
    'https://www.163.com',
    # 省略后面8个url...
]
htmls = []
titles = []


# sem = asyncio.Semaphore(10)  # 信号量，控制协程数，防止爬的过快
async def get_html(url):
    '''提交请求获取AAAI网页html'''
    async with aiohttp.ClientSession() as session:  # 获取session
        async with session.request('GET', url) as resp:  # 提出请求
            html = await resp.read()  # 直接获取到bytes
            htmls.append(html)
            print('异步获取%s下的html.' % url)


def loop_get_html():
    '''协程调用方，请求网页'''
    loop = asyncio.get_event_loop()  # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放到一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
    loop.close()  # 关闭事件循环


def multi_parse_html(html, cnt):
    '''使用多进程解析html'''
    title = etree.HTML(html).xpath('//title/text()')
    titles.append(''.join(title))
    print(f'第{cnt}个html完成解析－title:{"".join(title)}')


def parses():
    '''多进程调用总函数，解析html'''
    p = Pool(4)
    for index in range(len(htmls)):
        p.apply_async(multi_parse_html, args=(htmls[index], index))
    p.close()
    p.join()


if __name__ == '__main__':
    loop_get_html()  # 调用方
    parses()  # 解析html
