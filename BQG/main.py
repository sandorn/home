# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-11 01:48:27
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-11 19:44:50
法拍网(三方网站)http://www.fapaiwang.cn，信息采集
'''

# 'http://www.fapaiwang.cn/show?cid=0&ext2=0&ext3=0&ext4=0&ext5=0&min_pr=250&max_pr=580&min_ar=&max_ar=&orderId=2&status=2&q='

import time
from queue import Queue
import threading
from xjLib.req import parse_get as parse_url
from xjLib.req import savefile as writer
from xjLib.req import get_stime
from pyquery import PyQuery

SemaphoreNum = 30
Semaphore = threading.BoundedSemaphore(SemaphoreNum)  # 设置同时执行的线程数，其他等待执行
lock = threading.Lock()
urls = Queue()  # 存放章节链接
texts = []  # 将爬下来的小说存列表list，做最后排序


def get_download_url(url):
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
            url = urls.get()
            _texts = ''
            _response = parse_url(url)
            soup = PyQuery(_response.content)
            _name = soup('h1').text()  # 章节名
            _showtext = soup('#content').text()  # '.showtxt'
            _texts = _showtext.replace('\n\n', '\n')

            with lock:
                texts.append([self.index, _name, _texts])
                # @ print('下载进度{}%......\n'.format((self.count - threading.activeCount()) / self.count * 100), end='', flush=True)
                print('下载进度\t' + str(round(((self.count - threading.activeCount()) / self.count * 100), 2)), '%\t......\n', end='', flush=True)
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
    texts.sort(key=lambda x: x[0])
    writer(bookname + '.txt', texts)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)),
          flush=True)


if __name__ == '__main__':
    #!from xjLib.log import log
    #! log = log()
    main_thread('https://www.biqukan.com/2_2704/')
    # '65_65593'  #章节少，测试用 4秒
    # '2_2704'  #231万字  #6239kb, 132秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
