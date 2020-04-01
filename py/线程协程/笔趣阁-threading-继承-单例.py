# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 20:55:55
@LastEditors: Even.Sand
@LastEditTime: 2020-03-26 19:18:14

https://blog.csdn.net/ksws0393238aa/article/details/20286405?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
'''

import os
from threading import currentThread, enumerate
import time

from xjLib.ahttp import ahttpGet
from xjLib.CustomThread import SingletonThread
from xjLib.mystr import Ex_Re_Sub, Ex_Replace, savefile
from xjLib.req import parse_get

texts = []  # 将爬下来的小说存列表list，做最后排序


def get_contents(lock, index, target):
    """以下为需要重复的单次函数操作"""
    response = parse_get(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  \xa0"),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            '\xa0': '',  # 表示空格  &nbsp;
            '\u3000': '',  # 全角空格
            'www.biqukan.com。': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            '笔趣看;': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '<br />': '',
            '\r\r': '\n',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        },
    )

    texts.append([index, name, '    ' + text])

    with lock:
        print(currentThread().name, '\tindex:', index, '\tdone。', flush=True)

    return [index, name, '    ' + text]


def get_download_url(target):
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    urls = []  # 存放章节链接
    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def main_thread(target):
    bookname, urls = get_download_url(target)
    print('threading-继承，开始下载：《' + bookname + '》', flush=True)

    _ = [SingletonThread(get_contents, (index, urls[index]), 200) for index in range(len(urls))]

    # 循环等待线程数量，降低到2
    while True:
        thread_num = len(enumerate())
        # print("线程数量是%d" % thread_num)
        if thread_num <= 2:  # #单例多线程较一般多线程多一个
            break
        time.sleep(0.2)

    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + '.txt', texts, br='\n')


if __name__ == '__main__':
    main_thread('https://www.biqukan.com/2_2714/')
    # '38_38836'  #34秒
    # '10_10736'  #
    # "2_2714"   #
    # '0_790'    #
