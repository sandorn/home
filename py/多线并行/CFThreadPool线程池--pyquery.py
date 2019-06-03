# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 00:20:05
@LastEditors: Even.Sand
@LastEditTime: 2019-06-03 13:05:13

使用beautifulsoup和pyquery爬小说 - 坚强的小蚂蚁 - 博客园
https://www.cnblogs.com/regit/p/8529222.html
'''

import time

from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
import threading
from pyquery import PyQuery
from xjLib.req import parse_get as parse_url
from xjLib.req import savefile as writer
from xjLib.req import get_stime

lock = threading.Lock()
texts = []


def get_download_url(url):
    urls_list = []
    _response = parse_url(url)
    soup = PyQuery(_response.content)
    _bookname = soup('h2').text()

    # 开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
    begin_flag = False
    # 遍历所有子节点    #item()遍历节点数组
    for child in soup('body > div.listmain > dl').children():
        # 找到正文卷,使能标志位
        if child.tag == 'dt' and child.text.strip() == '《' + _bookname + '》正文卷':
            begin_flag = True
        # 爬取链接并下载链接内容
        if begin_flag and child.tag == 'dd':
            _soup = PyQuery(child)
            download_url = 'http://www.biqukan.com' + _soup('a').attr('href')
            urls_list.append(download_url)
    return _bookname, urls_list


def get_contents(index, url):
    _texts = ''
    _response = parse_url(url)
    soup = PyQuery(_response.content)
    _name = soup('h1').text()  # 章节名
    _showtext = soup('#content').text()  # '.showtxt'
    _texts = _showtext.replace('\n\n', '\n')
    with lock:
        print('{}\tdone\twith\t{}\tat\t{}'.format(threading.currentThread().name, index, get_stime()), flush=True)
    return [index, _name, _texts]


# 回调方式获取线程结果
def clb(obj):
    try:
        res = obj.result()
        texts.append(res)
    except Exception as e:
        print("obj.result()error:", e, flush=True)


def main_Pool(target):
    _stime = time.time()
    urls = []  # 存放章节链接

    print('开始下载：《{}》\t{}\t获取下载链接......'.format(target, get_stime()), flush=True)
    bookname, urls = get_download_url(target)
    print('CFThreadPool,开始下载：《' + bookname + '》', flush=True)
    # 创建多进程队列, 回调方式
    with Pool(25) as p:
        _ = [
            p.submit(get_contents, i, urls[i]).add_done_callback(clb)
            # task_list = [p.submit(get_contents, urls.get()) for i in range(urls.qsize())]
            for i in range(len(urls))
        ]

    print('\nCFThreadPool，书籍《' + bookname + '》完成下载', flush=True)
    texts.sort()
    writer(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), time.time() - _stime), flush=True)


if __name__ == '__main__':
    from xjLib.log import log
    log = log()
    main_Pool('https://www.biqukan.com//65_65593/')
    # '65_65593'  #章节少，测试用  3秒钟
    # '2_2704'  #231万字  #6239kb,34秒钟
    # "2_2714"   #《武炼巅峰》664万字  用时: 266 秒。
