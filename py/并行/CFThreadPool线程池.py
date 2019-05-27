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
@LastEditTime: 2019-05-21 18:54:22
'''

import time

from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
import threading
from bs4 import BeautifulSoup
from xjLib.req import parse_url as parse_url
from xjLib.req import savefile as writer
from xjLib.req import get_stime

lock = threading.Lock()
texts = []


def get_download_url(url):
    urls_list = []
    _response = parse_url(url)
    soup = BeautifulSoup(_response.text, 'lxml')
    [s.extract() for s in soup(["script", "style"])]
    _bookname = soup.find('h2').get_text()
    # 搜索文档树,找出div标签中class为listmain的所有子标签
    _div = str(soup.find_all('div', class_='listmain')[0])
    download_soup = BeautifulSoup(_div, features="html5lib")

    # 开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
    begin_flag = False

    # 遍历 dl 标签下所有子节点
    for child in download_soup.dl.children:
        # 找到正文卷,使能标志位
        if child.string.strip() == '《' + _bookname + '》正文卷':
            begin_flag = True
        # 爬取链接并下载链接内容
        if begin_flag and child.name == 'dd':
            download_url = 'http://www.biqukan.com/' + child.find('a').get('href')
            urls_list.append(download_url)
    return _bookname, urls_list


def get_contents(index, url):
    _texts = ''
    _response = parse_url(url)
    soup = BeautifulSoup(_response.text, 'lxml')
    [s.extract() for s in soup(["script", "style"])]
    _name = soup.h1.get_text()  # 章节名
    _showtext = soup.select('.showtxt')[0]
    for text in _showtext.stripped_strings:
        _texts += text + '\n'
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
            #task_list = [p.submit(get_contents, urls.get()) for i in range(urls.qsize())]
            for i in range(len(urls))
        ]
    '''
    # 返回值方式
    with Pool(20) as p:
        future_tasks = [p.submit(get_contents,  i, urls[i]) for i in range(len(urls))]

    from concurrent.futures import as_completed
    texts = []  # 将爬下来的小说都存在里面，做最后排序
    for obj in as_completed(future_tasks):
        if obj.done():
            try:
                texts.append(obj.result())
            except Exception as e:
                print("obj.result()error:", e)
    '''
    print('\nCFThreadPool，书籍《' + bookname + '》完成下载', flush=True)
    writer(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_Pool('https://www.biqukan.com//2_2704/')
    # '65_65593'  #章节少，测试用
    # '2_2704'  #231万字  #6239kb,36秒钟
    # "2_2714"   #《武炼巅峰》664万字
    # [武炼巅峰.txt]150W, 用时: 947.34 秒。
