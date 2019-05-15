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
@LastEditTime: 2019-05-15 21:38:05

python--threading多线程总结 - 苍松 - 博客园
http://www.cnblogs.com/tkqasn/p/5700281.html
threading.currentThread(): 返回当前的线程变量。
threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
threading.activeCount(): 返回正在运行的线程数量，与len(threading.enumerate())有相同的结果。
'''

import logging
import sys
import time
from queue import Queue
import threading

import requests
from bs4 import BeautifulSoup
from retrying import retry

lock = threading.Lock()
urls = Queue()  # 存放章节链接
indexs = Queue()  # 存放线程编号
texts = []  # 将爬下来的小说都存在里面，做最后排序

myhead = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch, br',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',  #' no-cache','keep-alive'
    'Connection': 'close',  # keep-alive'
    'Proxy-Connection': 'no-cache',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Host': 'www.biqukan.com',
}


def parse_url(url):

    @retry(stop_max_attempt_number=10)
    def _parse_url(url):
        # print('此处计入装饰器:', url ,'*' * 40, flush=True)
        header = myhead
        response = requests.get(url, headers=header, timeout=11)
        assert response.status_code == 200
        # print('此处获取url反馈:', url, flush=True)
        htmlTree = BeautifulSoup(response.text, 'html5lib')
        return htmlTree.body

    htmlTree = _parse_url(url)
    return htmlTree


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


def writer():
    # @函数说明:将爬取的文章内容写入文件
    print('《' + bookname + '》开始保存......', end='', flush=True)
    texts.sort()
    with open(bookname + '.txt', 'a', encoding='utf-8') as f:
        for i in texts:
            f.write(i[1] + '\n' + i[2] + '\n')
    print('《' + bookname + '》保存完成，任务结束！！！', flush=True)


# 方法二：从Thread继承，并重写run()
class MyThread(threading.Thread):

    def __init__(self, target=None, sph=None, index=None):
        super(MyThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.index = index
        self.sph = sph

    def run(self):  # 定义每个线程要运行的函数
        with self.sph:  # 同时并行指定的线程数量，执行完毕一个则死掉一个线程
            #以下为需要重复的单次函数操作
            self.sph.acquire()  # 计数器 -1
            target = urls.get()
            lock.acquire()
            print('队列剩余:{}，活动线程:{}'.format(urls.qsize(),
                                           threading.active_count()),
                  flush=True)
            print('ID：[%s]启动,下载《%s》......' % (self.name, target), flush=True)
            lock.release()

            _texts = ''
            _response = parse_url(target)
            _name = _response.h1.get_text()  #章节名
            _showtext = _response.select('.showtxt')[0]
            for text in _showtext.stripped_strings:
                _texts += text + '\n'

            lock.acquire()
            texts.append([self.index, _name, _texts])
            print('ID：[{}]结束,下载《{}》完成！！！'.format(self.name, _name), flush=True)
            lock.release()
            urls.task_done()  #发出此队列完成信号
            self.sph.release()  # 计数 +1.


def main_thread():
    index = 1  # 用来排序
    thread_list = []
    sph = threading.BoundedSemaphore(10)  # 设置同时执行的线程数，其他等待执行
    #threading.BoundedSemaphore(6)
    print('threading-继承，开始下载：《' + bookname + '》', flush=True)
    for i in range(urls.qsize()):
        time.sleep(0.1)
        res = MyThread(sph=sph, index=index)
        res.start()
        thread_list.append(res)
        index += 1

    for item in thread_list:
        item.join()  # join等待线程执行结束
    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    _stime = time.time()
    global bookname
    bookname = get_download_url('https://www.biqukan.com/31_31765/')
    main_thread()
    writer()
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round((time.time() - _stime))),
          flush=True)
