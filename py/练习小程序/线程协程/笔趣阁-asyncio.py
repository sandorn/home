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
@LastEditTime: 2020-03-01 17:30:54
顺讯，单独，速度慢
'''
import asyncio  # @协程，异步操作
import time

from lxml import etree

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile
from xjLib.req import parse_get

texts = []  # 将爬下来的小说都存在里面，做最后排序


def get_download_url(target):
    urls = []  # 存放章节链接
    response = etree.HTML(parse_get(target).content)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


@asyncio.coroutine  # 设为异步函数
def get_contents(index, target):
    # #async def get_contents(index, count):
    # #使用async关键字定义一个协程，协程是一种对象，不能直接运行，需要加入事件循环loop。
    response = etree.HTML(parse_get(target).content)
    _name = response.xpath('//h1/text()')[0]

    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)
    return index, _name, _showtext


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


def main_thread(target):
    _stime = time.time()
    bookname, urls = get_download_url(target)
    tasks = []
    print('asyncio，开始下载：《' + bookname + '》', flush=True)

    loop = asyncio.get_event_loop()  # @进入事件循环

    for index in range(len(urls)):
        res = get_contents(index, urls[index])
        task = asyncio.ensure_future(res)
        task.add_done_callback(callback)  # #绑定回调函数
        tasks.append(task)

    # loop.run_until_complete(asyncio.gather(*task))　　#将协同程序注册到事件循环中
    loop.run_until_complete(asyncio.wait(tasks))  # #将协同程序注册到事件循环中
    loop.close()

    print('asyncio，书籍《' + bookname + '》完成下载', flush=True)
    savefile(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_thread('https://www.biqukan.com/76_76519/')
    # '76_76519'  #章节少，测试用  22 秒
    # '2_2704'  #231万字  #6239kb, 下载《混在抗战》完成，用时:751.93秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
