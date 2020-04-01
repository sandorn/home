# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 21:49:56
@LastEditors: Even.Sand
@LastEditTime: 2020-04-01 18:09:46
根据网络资料，写的threadpool
'''

import os

from xjLib.ahttp import ahttpGet
from xjLib.CustomThread import (SingletonThread, SingletonThread_Queue, CustomThread, Custom_Thread_Queue, WorkManager, thread_pool_maneger)
from xjLib.mystr import (Ex_Re_Sub, Ex_Replace, fn_timer, savefile)
from xjLib.req import parse_get
import threading
from queue import Queue
import time


def get_download_url(target):
    urls = []  # 存放章节链接
    # response = etree.HTML(parse_get(target).content)
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(lock, index, target):
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

    return [index, name, '    ' + text]


@fn_timer
def st(bookname, urls):
    _ = [SingletonThread(get_contents, (index, url)) for index, url in enumerate(urls)]
    texts = SingletonThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SingletonThread.txt', texts, br='\n')


@fn_timer
def sq(bookname, urls):
    queue = Queue()
    for index, url in enumerate(urls):
        SingletonThread_Queue(queue)
        queue.put([get_contents, index, url])

    # texts = SingletonThread_Queue.getAllResult()
    texts = SingletonThread_Queue.wait_completed()

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'SingletonThread_Queue.txt', texts, br='\n')


@fn_timer
def ct(bookname, args):
    _ = [CustomThread(get_contents, [index, url])for index, url in enumerate(urls)]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


@fn_timer
def cq(bookname, args):
    queue = Queue()
    for index, url in enumerate(urls):
        Custom_Thread_Queue(queue)
        queue.put([get_contents, index, url])

    # texts = Custom_Thread_Queue.getAllResult()
    texts = Custom_Thread_Queue.wait_completed()

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'Custom_Thread_Queue.txt', texts, br='\n')


@fn_timer
def wm(bookname, urls):
    mywork = WorkManager([[get_contents, index, url] for index, url in enumerate(urls)])  # 调用函数,参数:list内tupe,线程数量
    # texts = mywork.wait_allcomplete()
    texts = mywork.queue_join()

    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'WorkManager.txt', texts, br='\n')


@fn_timer
def tp(bookname, urls, MaxSem=99):
    '''
    tasks = []
    for index, url in enumerate(urls):
        task = [get_contents, index, url]
        tasks.append(task)
    mywork = thread_pool_maneger(tasks)
    '''
    mywork = thread_pool_maneger([[get_contents, index, url] for index, url in enumerate(urls)], MaxSem=MaxSem)
    texts = mywork.getAllResult()
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'thread_pool_maneger.txt', texts, br='\n')


if __name__ == "__main__":
    bookname, urls = get_download_url('http://www.biqukan.com/2_2714/')  # 38_38836  #2_2714
    tp(bookname, urls)
    for func in ['st', 'sq', 'ct', 'cq', 'wm', 'tp']:
        eval(func)(bookname, urls)
        # print('#' * 33, threading.active_count(), threading.enumerate())
        # locals()[func](bookname, urls)
        # globals()[func](bookname, urls)


'''
# 默认线程数量
[笔趣阁-自定义库CustomThread例子＆武炼巅峰SingletonThread.txt]保存完成	size：46.47 MB
Total time running with [SingletonThread]: 68.46 seconds
[笔趣阁-自定义库CustomThread例子＆武炼巅峰SingletonThread_Queue.txt]保存完成	size：46.47 MB
Total time running with [SingletonThread_Queue]: 75.63 seconds
[笔趣阁-自定义库CustomThread例子＆武炼巅峰CustomThread.txt]保存完成	size：46.47 MB
Total time running with [CustomThread]: 91.00 seconds
[笔趣阁-自定义库CustomThread例子＆武炼巅峰Custom_Thread_Queue.txt]保存完成	size：46.47 MB
Total time running with [Custom_Thread_Queue]: 67.19 seconds
[笔趣阁-自定义库CustomThread例子＆武炼巅峰WorkManager.txt]保存完成	size：46.47 MB
Total time running with [WorkManager]: 66.73 seconds
[笔趣阁-自定义库CustomThread例子＆武炼巅峰thread_pool_maneger.txt]保存完成	size：46.47 MB
Total time running with [thread_pool_maneger]: 130.96 seconds
'''
