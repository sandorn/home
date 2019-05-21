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
@LastEditTime: 2019-05-18 11:22:20

python--threading多线程总结 - 苍松 - 博客园
http://www.cnblogs.com/tkqasn/p/5700281.html
threading.currentThread(): 返回当前的线程变量。
threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。
'''

import time
from queue import Queue
import threading
from xjLib.req import parse_url as parse_url
from bs4 import BeautifulSoup
from xjLib.req import savefile as writer
from xjLib.req import get_stime

SemaphoreNum = 25
Semaphore = threading.BoundedSemaphore(SemaphoreNum)  # 设置同时执行的线程数，其他等待执行
lock = threading.Lock()
urls = Queue()  # 存放章节链接
texts = []  # 将爬下来的小说都存在里面，做最后排序


def get_download_url(target):
    _response = parse_url(target)
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
            download_url = 'http://www.biqukan.com/' + child.find('a').get(
                'href')
            urls.put(download_url)
    return _bookname


class MyThread(threading.Thread):

    def __init__(self, sph, index, count):
        super(MyThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.count = count
        self.index = index
        self.sph = sph

    def run(self):  # 定义每个线程要运行的函数
        with self.sph:  # 同时并行线程数量
            # 以下为需要重复的单次函数操作
            target = urls.get()
            _texts = ''
            _response = parse_url(target)
            _name = _response.h1.get_text()  # 章节名
            _showtext = _response.select('.showtxt')[0]
            for text in _showtext.stripped_strings:
                _texts += text + '\n'

            with lock:
                texts.append([self.index, _name, _texts])
                print('下载进度{}%......\t'.format((self.count - threading.activeCount()) / self.count * 100), end='', flush=True)
                print('{}\tdone\twith\t{}\tat\t{}'.format(self.name, self.index, get_stime()), flush=True)
            urls.task_done()


def main_thread(target):
    _stime = time.time()
    bookname = get_download_url(target)
    thread_list = []
    print('threading-继承，开始下载：《' + bookname + '》', flush=True)
    count = urls.qsize()
    for index in range(count):
        res = MyThread(Semaphore, index, count)
        res.start()
        thread_list.append(res)

    for item in thread_list:
        item.join()  # join等待线程执行结束
    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)
    writer(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)),
          flush=True)


if __name__ == '__main__':
    main_thread('https://www.biqukan.com/2_2704/')
    # '65_65593'  #章节少，测试用
    # '2_2704'  #231万字  #6239kb, 132秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
