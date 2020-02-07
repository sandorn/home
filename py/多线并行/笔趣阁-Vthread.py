# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-18 03:50:41
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-07 17:56:58

# !存在问题，主线程先结束，子线程后结束，未能取得返回值
'''
from bs4 import BeautifulSoup
from xjLib.req import get_stime
from xjLib.req import session_url as parse_url
from xjLib.req import savefile as writer
import threading
import time
import vthread

mypool = vthread.pool(20)  # gqueue=1，分组
lock = threading.RLock()
texts = []

# help(mypool)


def get_download_url(target):
    _urls = []
    _response = parse_url(target)
    _response = BeautifulSoup(_response.text, features="html5lib")
    _bookname = _response.find('h2').get_text()
    # 搜索文档树,找出div标签中class为listmain的所有子标签
    _div = str(_response.find_all('div', class_='listmain')[0])
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
            _urls.append(download_url)
    return _bookname, _urls


@mypool
def get_contents(index, url):
    print('ID: {} url: {}'.format(index, url), flush=True)
    _texts = ''
    _response = parse_url(url)
    _response = BeautifulSoup(_response.text, features="html5lib")
    _name = _response.h1.get_text()  # 章节名
    _showtext = _response.select('.showtxt')[0]
    for text in _showtext.stripped_strings:
        _texts += text + '\n'

    print('ID：{} done [{}] at {}'.format(index, _name, get_stime()), flush=True)
    with lock:
        texts.append([index, _name, _texts])


if __name__ == "__main__":
    from xjLib.log import log
    log = log()
    start = time.time()
    _name, urls = get_download_url('https://www.biqukan.com/2_2704/')
    args = [(i, urls[i])for i in range(len(urls))]
    for item in args:
        get_contents(*item)

    writer(_name + '.txt', texts)
    end = time.time()
    print("threadPool cost all time: %s" % (end - start), flush=True)
    # '65_65593/'  #章节少，测试用
    # "2_2714"   #《武炼巅峰》664万字
    # [武炼巅峰.txt]150W, 用时: 947.34 秒。
