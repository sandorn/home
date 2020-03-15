# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 17:04:07
@LastEditors: Even.Sand
@LastEditTime: 2020-03-13 13:43:14
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
    # async with是异步上下文管理器
    async with aiohttp.ClientSession() as session:  # 获取session
        async with session.request('GET', url) as resp:  # 提出请求
            html = await resp.read()  # 直接获取到bytes
            htmls.append(html)
            print('异步获取%s下的html.' % url)


def loop_get_html():
    '''协程调用方，请求网页'''
    loop = asyncio.get_event_loop()           # 获取事件循环
    tasks = [get_html(url) for url in urls]  # 把所有任务放到一个列表中
    loop.run_until_complete(asyncio.wait(tasks))  # 激活协程
    loop.close()  # 关闭事件循环


def multi_parse_html(html, cnt):
    '''使用多进程解析html'''
    title = etree.HTML(html).xpath('//title/text()')
    titles.append(''.join(title))
    print('第%d个html完成解析－title:%s' % (cnt, ''.join(title)))


def parses():
    '''多进程调用总函数，解析html'''
    p = Pool(4)
    for index in range(len(htmls)):
        p.apply_async(multi_parse_html, args=(htmls[index], index))
    p.close()
    p.join()


if __name__ == '__main__':
    start = time.time()
    loop_get_html()   # 调用方
    parses()  # 解析html
    print('总耗时：%.5f秒' % float(time.time() - start))
