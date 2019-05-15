# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 使用multiprocess.pool多进程
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 18:31:14
@LastEditTime: 2019-05-15 23:17:17
努努书坊 - 小说在线阅读   https://www.kanunu8.com/

Python3网络爬虫快速入门实战解析（一小时入门 Python 3 网络爬虫） - u012662731的博客 - CSDN博客
https://blog.csdn.net/u012662731/article/details/78537432

爬虫笔记——第三方库Beautiful Soup4 使用总结 - 简书
https://www.jianshu.com/p/1ba25d35ff25

python requests用法总结 - lwli - 博客园
https://www.cnblogs.com/lilinwei340/p/6417689.html
'''

import time
from queue import Queue
from multiprocess import Pool
from bs4 import BeautifulSoup


class downloader(object):

    def __init__(self, target):
        self.server = 'http://www.biqukan.com/'
        self.target = target
        self.names = Queue()  # 存放章节名
        self.urls = Queue()  # 存放章节链接
        self.bookname = ''  # 书名
        self.texts = []  # 将爬下来的小说都存在里面，做最后排序

        self.myhead = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch, br',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'close',
            # Cache-Control':'no-cache','keep-alive'
            # Connection':'close','keep-alive'
            'Proxy-Connection': 'no-cache',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
            'Host': 'www.biqukan.com',
        }

    def parse_url(self, url):
        from retrying import retry
        import requests
        from bs4 import BeautifulSoup

        @retry(stop_max_attempt_number=10)
        def _parse_url(url):
            # //print('此处计入装饰器:', url ,'*' * 40, flush=True)
            header = self.myhead
            response = requests.get(url, headers=header, timeout=6)
            assert response.status_code == 200
            # //print('此处获取url反馈:', url, flush=True)
            htmlTree = BeautifulSoup(response.text, 'html5lib')
            return htmlTree.body

        htmlTree = _parse_url(url)
        return htmlTree

    def get_download_url(self):
        _response = self.parse_url(self.target)
        self.bookname = _response.find('h2').get_text()
        # 搜索文档树,找出div标签中class为listmain的所有子标签
        _div = str(_response.find_all('div', class_='listmain')[0])
        download_soup = BeautifulSoup(_div, features="html5lib")

        # 开始记录内容标志位,只要正文卷下面的链接,最新章节列表链接剔除
        begin_flag = False

        # 遍历 dl 标签下所有子节点
        for child in download_soup.dl.children:
            # 找到正文卷,使能标志位
            if child.string.strip() == '《' + self.bookname + '》正文卷':
                begin_flag = True
            # 爬取链接并下载链接内容
            if begin_flag and child.name == 'dd':
                download_url = self.server + child.find('a').get('href')
                章节名 = child.find('a').get_text()
                self.urls.put(download_url)
                self.names.put(章节名)

    def get_contents(self, index, target):
        import os
        print('下载《{}》,PID:{}......'.format(target, os.getpid()), flush=True)

        texts = ''
        _response = self.parse_url(target)
        _name = _response.h1.get_text()  #章节名
        _showtext = _response.select('.showtxt')[0]
        for text in _showtext.stripped_strings:
            texts += text + '\n'

        print('下载《{}》PID:{}完成!!!!!!'.format(_name, os.getpid()), flush=True)
        return [index, _name, texts]

    def writer(self):
        # @函数说明:将爬取的文章内容写入文件
        print('《' + self.bookname + '》开始保存', flush=True)

        self.texts.sort()
        with open(self.bookname + '.txt', 'a', encoding='utf-8') as f:
            for i in self.texts:
                f.write(i[1] + '\n' + i[2] + '\n')

        print('《' + self.bookname + '》保存完成，任务结束', flush=True)


def main_Pool():
    index = 1  # 用来排序
    pool_result = []  # 线程池

    print('开始下载：《' + myclient.bookname + '》', flush=True)
    mypool = Pool(20)  #!进程数
    while not myclient.urls.empty():
        target = myclient.urls.get()
        result = mypool.apply_async(myclient.get_contents, args=(index, target))
        pool_result.append(result)
        index += 1

    mypool.close()  # 关闭进程池，表示不能在往进程池中添加进程
    mypool.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用

    for res in pool_result:
        myclient.texts.append(res.get())

    # @join后获取进程返回值
    # res.wait()  # 等待进程函数执行完毕
    # res.ready():  # 进程函数是否已经启动了
    # res.successful():  # 进程函数是否执行成功

    print('\r《' + myclient.bookname + '》完成下载', flush=True)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    _stime = time.time()
    global myclient
    myclient = downloader('https://www.biqukan.com/65_65593/')
    myclient.get_download_url()
    main_Pool()
    myclient.writer()
    print('下载《{}》完成，用时:{} 秒。'.format(myclient.bookname,
                                     round((time.time() - _stime))),
          flush=True)
