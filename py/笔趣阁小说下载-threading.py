# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 使用循环，反防爬虫
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 18:31:14
@LastEditTime: 2019-05-12 17:59:21

Python3网络爬虫快速入门实战解析（一小时入门 Python 3 网络爬虫） - u012662731的博客 - CSDN博客
https://blog.csdn.net/u012662731/article/details/78537432

爬虫笔记——第三方库Beautiful Soup4 使用总结 - 简书
https://www.jianshu.com/p/1ba25d35ff25

python requests用法总结 - lwli - 博客园
https://www.cnblogs.com/lilinwei340/p/6417689.html
'''
import queue
import threading
import time

import requests
from bs4 import BeautifulSoup
from retrying import retry

lock = threading.Lock()


def decorator_timer(method_to_decorate):
    from functools import wraps
    #为了保留被装饰函数的函数名和帮助文档信息,不理解
    @wraps(method_to_decorate)
    # 在内部定义了另外一个函数：一个封装器。
    # 这个函数将原始函数进行封装，所以你可以在它之前或者之后执行一些代码
    def wrapper(self, *args, **kwargs):
        # 放原函数执行前的一些代码
        #print('args:', args,'kwargs:', kwargs, flush=True)
        _stime = time.time()
        # 执行原始函数
        reslut = method_to_decorate(self, *args, **kwargs)
        msecs = round((time.time() - _stime) * 1000)
        print(
            'times out : {0} ms，now is: {1}\r'.format(msecs, time.time()),
            flush=True)
        #返回原程序的返回值
        return reslut

    #'wrapper'尚未执行，请求执行：
    return wrapper


class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'https://www.biqukan.com/62_62384/'
        self.names = queue.Queue()  #存放章节名
        self.urls = queue.Queue()  #存放章节链接
        self.bookname = ''  #书名
        self.texts = []  #将爬下来的小说都存在里面，做最后排序

        self.myhead = {
            'Accept':
                '*/*',
            'Accept-Encoding':
                'gzip,deflate,sdch, br',
            'Accept-Language':
                'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control':
                'max-age=0',
            'Connection':
                'close',
            #'Cache-Control':'no-cache', 'Connection':'close','keep-alive'
            'Proxy-Connection':
                'no-cache',
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
            'Host':
                'www.biqukan.com'
        }

    def parse_url(self, url):

        @retry(stop_max_attempt_number=10)
        def _parse_url(url):
            #print('此处计入装饰器' + '*' * 100, flush=True)
            header = self.myhead
            response = requests.get(url, headers=header, timeout=6)
            assert response.status_code == 200
            #print('此处获取url反馈:', url, flush=True)
            htmlTree = BeautifulSoup(response.text, 'html5lib')  # 'html.parser'
            return htmlTree.body

        html = _parse_url(url)
        return html

    def get_download_url(self):
        response = self.parse_url(self.target)
        self.bookname = response.find('h2').get_text()
        #搜索文档树,找出div标签中class为listmain的所有子标签
        _div = str(response.find_all('div', class_='listmain')[0])
        download_soup = BeautifulSoup(_div, features="html5lib")
        #开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
        begin_flag = False

        #遍历dl标签下所有子节点
        for child in download_soup.dl.children:

            #找到正文卷,使能标志位
            if child.string.strip() == '《' + self.bookname + '》正文卷':
                begin_flag = True

            #爬取链接并下载链接内容
            if begin_flag and child.name == 'dd':
                download_url = self.server + child.find('a').get('href')
                章节名 = child.find('a').get_text()
                self.urls.put(download_url)
                self.names.put(章节名)

    #@decorator_timer
    def get_contents(self, name, target, index):
        #lock.acquire()
        print('下载《{}》。。。。。。'.format(name), flush=True)
        #lock.release()

        texts = ''
        response = self.parse_url(target)
        _showtext = response.select('.showtxt')[0]

        for text in _showtext.stripped_strings:
            texts += text + '\n'

        #lock.acquire()
        self.texts.append([index, name, texts])
        print('下载《{}》完成。'.format(name), flush=True)
        #lock.release()

    def writer(self):
        '''
        函数说明:将爬取的文章内容写入文件
        '''
        print('《' + self.bookname + '》开始保存', flush=True)
        self.texts.sort()
        with open(self.bookname + '.txt', 'a', encoding='utf-8') as f:
            for i in self.texts:
                f.write(i[1] + '\n')
                f.write(i[2] + '\n')
        print('《' + self.bookname + '》保存完成，任务结束', flush=True)


def main_thread():
    index = 1  #用来排序
    threads = []  #线程池

    print('开始下载：《' + dl.bookname + '》', flush=True)
    while not dl.urls.empty():
        #dl.get_contents(new_name, new_url, index) # 单线程
        new_url = dl.urls.get()
        new_name = dl.names.get()
        pool = threading.Thread(
            target=dl.get_contents, args=(new_name, new_url, index))
        threads.append(pool)
        pool.start()
        index += 1
    for pool in threads:
        pool.join()  # join等待其他子线程执行结束

    print('\r《' + dl.bookname + '》完成下载', flush=True)


if __name__ == '__main__':
    _stime = time.time()
    global dl
    dl = downloader()
    dl.get_download_url()
    main_thread()
    dl.writer()
    print(
        '下载《{}》完成，用时:{} 秒。'.format(dl.bookname, round((time.time() - _stime))),
        flush=True)
