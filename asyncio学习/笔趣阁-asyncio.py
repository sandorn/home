# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-12 14:52:44
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-30 02:41:33
顺讯，单独，速度慢
'''

import asyncio  # @协程，异步操作
import time
import os

import aiohttp

from xt_String import Ex_Re_Sub
from xt_File import savefile
from xt_Ls_Bqg import arrangeContent
from xt_Response import ReqResult


# TIMESOUT = 20  # (20, 9, 9, 9)
async def fetch(url):
    async with aiohttp.ClientSession() as sess:
        async with sess.get(url) as response:
            content = await response.read()
    return ReqResult(response, content)


async def get_download_url(url):
    urls = []  # 存放章节链接
    resp = await fetch(url)
    html = resp.element

    _bookname = html.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = html.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []  # 将爬下来的小说都存在里面，做最后排序


async def get_contents(*args):
    index, url = args
    resp = await fetch(url)
    html = resp.element
    _title = "".join(html.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000',
                                         u' ').replace(u'\xa0', u' ')
    _showtext = html.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)

    texts.append([index, title, content])


async def callback(future):
    index, _name, _showtext = await future.result()  # 回调函数取得返回值
    name = Ex_Re_Sub(_name, {
        '\'': '',
        ' ': ' ',
        '\xa0': ' ',
    })

    text = arrangeContent(_showtext)
    texts.append([index, name, text])


def main_thread(url):

    bookname, urls = asyncio.run(get_download_url(url))
    print(9999, bookname)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [
        asyncio.ensure_future(get_contents(index, url))
        for index, url in enumerate(urls)
    ]

    loop.run_until_complete(asyncio.wait(tasks))

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + '_asyncio.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.biqukan.com/38_38836/'

    main_thread(url)

    # '76_76519'  #章节少，165KB  3秒
    # '38_38836'  #3670.75KB，测试用  6秒
    # "2_2714"   #48.04 MB, 用时:64秒
