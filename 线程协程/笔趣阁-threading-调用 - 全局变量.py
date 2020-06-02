# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@LastEditTime: 2020-03-15 18:18:27
'''
import threading
import time
from queue import Queue

from bs4 import BeautifulSoup

from xjLib.mystr import get_stime, savefile
from xjLib.req import parse_get

lock = threading.RLock()
urls = Queue()  # 存放章节链接
总章节 = 0  # 小说章节数量
当前进度 = 0  # 已下载小说章节数
texts = []  # 将爬下来的小说都存在里面，做最后排序
SemaphoreNum = 30
semaphore = threading.BoundedSemaphore(SemaphoreNum)  # 设置同时执行的线程数，其他等待执行


def get_download_url(target):
    response = parse_get(target)
    _response = BeautifulSoup(response.content, 'lxml')
    [s.extract() for s in _response(["script", "style"])]
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
            urls.put(download_url)
    return _bookname


def get_contents(index):
    global 总章节, 当前进度
    with semaphore:
        target = urls.get()
        _texts = ''
        _response = parse_get(target)
        html_str = _response.content.decode('gbk', 'ignore')
        html_str = html_str.split('<body')[-1]
        html_str = '<body' + html_str

        _response = BeautifulSoup(html_str, 'lxml')
        [s.extract() for s in _response(["script", "style"])]
        _name = _response.h1.get_text()  # 章节名
        _showtext = _response.select('.showtxt')[0]
        for text in _showtext.stripped_strings:
            _texts += text + '\n'
        with lock:
            texts.append([index, _name, _texts])
            当前进度 += 1
            print('下载\t' + str(当前进度) + '/' + str(总章节) + '|\t进度\t' + str(round(当前进度 / 总章节 * 100, 2)) + '%\t|\tBy\t' + str(index) + '\t号线程\n', end='', flush=True)
        urls.task_done()  # 发出此队列完成信号


def main_thread(target):
    _stime = time.time()
    bookname = get_download_url(target)
    thread_list = []
    global 总章节
    print('threading-调用，开始下载：《' + bookname + '》', flush=True)
    总章节 = urls.qsize()
    for index in range(总章节):
        res = threading.Thread(target=get_contents, args=(index,))
        res.start()
        thread_list.append(res)

    for item in thread_list:
        item.join()  # join等待线程执行结束

    print('threading-调用，书籍《' + bookname + '》完成下载', flush=True)
    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_thread('https://www.biqukan.com/2_2714/')
    # '65_65593'  #章节少，测试用
    # '2_2704'  #231万字  #6239kb, 153秒
    # "0_790"   # 60秒。
    # "2_2714"   #《武炼巅峰》664万字, 秒。
