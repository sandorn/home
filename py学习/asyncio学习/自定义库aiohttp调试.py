# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-02 18:44:15
@LastEditors: Even.Sand
@LastEditTime: 2020-03-03 18:26:10
'''
import asyncio
import time

import aiohttp
from lxml import etree

from xjLib.aiohttp import fetch
from xjLib.mystr import Ex_Re_Sub, get_stime, savefile


async def get_download_url(target, session):
    urls = []  # 存放章节链接
    status, html, redirected_url = await fetch(target, session)
    response = etree.HTML(html)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)

    return _bookname, urls


async def get_contents(index, target, session):
    status, html, redirected_url = await fetch(target, session)

    response = etree.HTML(html)
    _name = response.xpath('//h1/text()')[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)
    return index, _name, _showtext

texts = []


def callback(future):
    index, _name, _showtext = future.result()  # 回调函数取得返回值
    name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })

    text = Ex_Re_Sub(
        _showtext,
        {
            '\'': '',
            ' ': ' ',
            '\xa0': ' ',
            '\x0a': '\n',
            # '\b;': '\n',
            '&nbsp;': ' ',
            'app2();': '',
            '笔趣看;': '',
            '\u3000': '',
            'chaptererror();': '',
            'readtype!=2&&(\'vipchapter\n(\';\n\n}': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            'www.biqukan.com。': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        }
    )
    texts.append([index, name, text])


session = aiohttp.ClientSession()

_stime = time.time()
urls = [
    'https://www.biqukan.com/76_76572/',
    'https://www.biqukan.com/64_64345/',
]
tasks = []
loop = asyncio.get_event_loop()
for url in urls:
    task = loop.create_task(get_download_url(url, session))
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))


tasks2 = []
for index in range(len(tasks)):
    bookname, urls = tasks[index].result()
    for i in range(len(urls)):
        task = asyncio.ensure_future(get_contents(i, urls[i], session))
        task.add_done_callback(callback)
        tasks2.append(task)

loop.run_until_complete(asyncio.wait(tasks2))  # #将协同程序注册到事件循环中
loop.close()
del session
print('asyncio，书籍《' + bookname + '》完成下载', flush=True)

texts.sort(key=lambda x: x[0])
savefile(bookname + '.txt', texts)
print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)
