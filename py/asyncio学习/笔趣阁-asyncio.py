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
@LastEditors: Even.Sand
@LastEditTime: 2020-03-03 23:37:02
顺讯，单独，速度慢
'''

import ahttp  # @增加异步http
import asyncio  # @协程，异步操作
import aiohttp
import time
from xjLib.aiohttp import fetch

from lxml import etree

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile
from xjLib.req import parse_get

texts = []  # 将爬下来的小说都存在里面，做最后排序
sess = ahttp.Session()


def get_download_url(url):
    urls = []  # 存放章节链接
    #response = etree.HTML(parse_get(url).content)
    response = sess.get(url).html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


async def get_contents(index, url, session):
    # #async def get_contents(index, count):
    # #使用async关键字定义一个协程，协程是一种对象，不能直接运行，需要加入事件循环loop。
    _, html, _ = await fetch(url, session)  # !阻塞了
    response = etree.HTML(html)
    _name = response.xpath('//h1/text()')[0]

    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)
    return index, _name, _showtext


async def callback(future):
    index, _name, _showtext = await future.result()  # 回调函数取得返回值
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


async def create_session():
    return aiohttp.ClientSession()


def main_thread(url):
    _stime = time.time()
    bookname, urls = get_download_url(url)
    tasks = []
    print('asyncio，开始下载：《' + bookname + '》', flush=True)

    session = asyncio.get_event_loop().run_until_complete(create_session())
    loop = asyncio.get_event_loop()  # @进入事件循环

    for index in range(len(urls)):
        res = get_contents(index, urls[index], session)
        task = asyncio.ensure_future(res)
        task.add_done_callback(callback)  # #绑定回调函数
        tasks.append(task)

    loop.run_until_complete(asyncio.gather(*tasks))  # 将协同程序注册到事件循环中
    loop.run_until_complete(session.close())
    loop.close()

    print('asyncio，书籍《' + bookname + '》完成下载', flush=True)

    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    url = 'https://www.biqukan.com/2_2704/'

    main_thread(url)
    # '76_76519'  #章节少，测试用  8秒
    # '2_2704'  #6239kb, 用时:751.93秒
    # "2_2714"   #6239kb, 用时:751.93秒
