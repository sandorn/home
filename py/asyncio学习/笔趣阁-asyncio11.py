# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 12:37:21
@LastEditors: Even.Sand
@LastEditTime: 2020-03-03 23:13:32
'''


import asyncio  # @协程，异步操作
import aiohttp
import time
from xjLib.aiohttp import fetch
from lxml import etree

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile

texts = []  # 将爬下来的小说都存在里面，做最后排序
urlss = {}
default_headers = {
    'User-Agent': ('Mozilla/5.0 (compatible; MSIE 9.0; '
                   'Windows NT 6.1; Win64; x64; Trident/5.0)'),
}


async def get_download_url(targ):
    (url, session) = targ
    print(1111, url)
    urls = []  # 存放章节链接
    _, html, _ = await fetch(url, session)
    response = etree.HTML(html)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')
    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    print(_bookname, urls)
    urlss[_bookname] = urls
    return _bookname, urls


async def get_contents(targ):
    (index, url, session) = targ
    # #使用async关键字定义一个协程，协程是一种对象，不能直接运行，需要加入事件循环loop。
    _, html, _ = await fetch(url, session)
    response = etree.HTML(html)
    _name = response.xpath('//h1/text()')[0]

    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)

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


async def main_thread(url):
    _stime = time.time()
    session = aiohttp.ClientSession()
    loop = asyncio.get_event_loop()

    readed = await loop.run_in_executor(None, get_download_url, (url, session))
    return True
    '''
        tasks.append(asyncio.ensure_future(begin_download(sem, session, url, path, flag)))
        # 等待返回结果
        tasks_iter = asyncio.as_completed(tasks)
        # 创建一个进度条
        fk_task_iter = tqdm.tqdm(tasks_iter, total=len(FLAGS))
        for coroutine in fk_task_iter:
            # 获取结果
            res = await coroutine
            print(res, '下载完成')
        '''
    for k in urlss:
        for i in range(len(urlss[k])):
            v = urlss[k][i]
            # event_loop.call_soon_threadsafe(get_contents, i, v, session)
            await loop.run_in_executor(None, get_contents, (i, v, session))

    session.close()

    # print('asyncio，书籍《' + bookname + '》完成下载', flush=True)

    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)

if __name__ == '__main__':
    url_list = ['https://www.biqukan.com/76_76572/',
                'https://www.biqukan.com/64_64345/', ]

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(main_thread(url, loop)) for url in url_list]
    loop.run_until_complete(asyncio.wait(tasks))
