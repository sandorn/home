# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-02 11:15:02
@LastEditors: Even.Sand
@LastEditTime: 2020-03-02 13:52:09
'''

import threading
import time
from xjLib.CustomThread import CustomThread

from lxml import etree
from xjLib.mystr import Ex_Re_Sub, get_stime, savefile
from xjLib.req import parse_get


def get_content(lock, index, target):
    """默认传入lock，以下为需要重复的单次函数操作"""
    response = etree.HTML(parse_get(target).content)
    _name = response.xpath('//h1/text()')[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    time.sleep(2)
    with lock:
        print('{}\tdone\tat\t{}'.format(index, get_stime()))
    return [index, _name, _showtext]


def get_download_url(target):
    urls = []  # 存放章节链接
    response = etree.HTML(parse_get(target).content)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []  # 将爬下来的小说存列表list，做最后排序


def callback(future):
    index, _name, _showtext = future  # 回调函数取得返回值
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


if __name__ == '__main__':
    # #from xjLib.log import log
    # #log = log()

    url = 'https://www.biqukan.com/2_2714/'
    _stime = time.time()
    bookname, urls = get_download_url(url)

    print('threading-继承，开始下载：《' + bookname + '》', flush=True)

    # threadingSum = threading.Semaphore(50)  # 同步线程数
    for index in range(len(urls)):
        # 创建多线程
        TASKS = CustomThread(get_content, (index, urls[index]))
        # , threadingSum
    for thread in TASKS.all_Thread:
        thread.join()  # join等待线程执行结束
        callback(thread.getResult())  # 线程结果执行回调函数

    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)
    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)

    # '65_65593'  #章节少134万字，3573kb,, 22秒
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, #!80秒,未限制线程数量
