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
@LastEditTime: 2019-05-10 17:51:36

Python3网络爬虫快速入门实战解析（一小时入门 Python 3 网络爬虫） - u012662731的博客 - CSDN博客
https://blog.csdn.net/u012662731/article/details/78537432

爬虫笔记——第三方库Beautiful Soup4 使用总结 - 简书
https://www.jianshu.com/p/1ba25d35ff25

python requests用法总结 - lwli - 博客园
https://www.cnblogs.com/lilinwei340/p/6417689.html
'''

import random
import threading
import time
from functools import wraps

import requests
from bs4 import BeautifulSoup

lock = threading.Lock()


def decorator_timer(method_to_decorate):
    #为了保留被装饰函数的函数名和帮助文档信息,不理解
    @wraps(method_to_decorate)
    # 在内部定义了另外一个函数：一个封装器。
    # 这个函数将原始函数进行封装，所以你可以在它之前或者之后执行一些代码
    def wrapper(self, *args, **kwargs):
        # 放原函数执行前的一些代码
        #print('args:', args,'kwargs:', kwargs)
        _stime = time.time()
        # 执行原始函数
        reslut = method_to_decorate(self, *args, **kwargs)
        msecs = round((time.time() - _stime) * 1000)
        print("times out : {0} ms，now is: {1}\r".format(msecs, time.time()),)
        #返回原程序的返回值
        return reslut

    #"wrapper"尚未执行，请求执行：
    return wrapper


class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'https://www.biqukan.com/0_243/'
        self.names = []  #存放章节名
        self.urls = []  #存放章节链接
        self.nums = 0  #章节数
        self.bookname = ''  #书名
        self.text = {}  #书籍内容，章节名:内容
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get_download_url(self):
        while True:
            req = requests.get(url=self.target)
            if req.status_code == requests.codes.ok:
                print('获取小说章节下载地址:ok')
                break
            time.sleep(0.2)

        html = req.text
        #'html5lib','html.parser','lxml','html_parser')
        div_bf = BeautifulSoup(html, 'html5lib')
        self.bookname = div_bf.find_all('h2')[0].get_text()

        div = str(div_bf.find_all('div', class_='listmain')[0])
        a_bf = BeautifulSoup(div, features="html5lib")
        a = a_bf.find_all('a')
        self.nums = len(a[0:])  #剔除不必要的章节，并统计章节数
        for each in a[0:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    #@decorator_timer
    def get_contents(self, name, target):
        """
        函数说明:获取章节内容,将获取到的章节内容保存到字典
        Parameters:
        target - 下载连接(string)
        Returns:texts - 章节内容(string)
        self.text = {name:章节名,text:章节内容}
        """
        _stime = time.time()
        header = {}

        header['User-Agent'] = random.choice(self.user_agent_list)
        header.update({
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":
                "gzip, deflate, br",
            "Accept-Language":
                "zh-CN,zh;q=0.9",
            "Connection":
                "keep-alive",
            "Host":
                "www.biqukan.com"
        })
        while True:
            response = requests.get(url=target, headers=header, timeout=2)
            if response.status_code == requests.codes.ok:
                #print('get_contents:ok')
                break
            time.sleep(0.2)
            lock.acquire()
            print("重试下载：{},网址：{}".format(name, target), flush=True)
            lock.release()

        texts = ''
        html = response.text
        bf = BeautifulSoup(html, 'html5lib')
        tr = bf.select('.showtxt')[0]
        for text in tr.stripped_strings:
            texts += text + '\n'

        lock.acquire()
        self.text[name] = texts
        print(
            "下载《{}》完成，用时:{}。".format(name, round(
                (time.time() - _stime) * 1000)),
            flush=True)
        lock.release()

    def writer(self):
        """
        函数说明:将爬取的文章内容写入文件
        """
        print('《' + self.bookname + '》开始保存')
        with open(self.bookname + '.txt', 'a', encoding='utf-8') as f:
            for i in range(len(self.names)):
                f.write(self.names[i] + '\n' + self.text[self.names[i]] + '\n')
        print('《' + self.bookname + '》保存完成，任务结束')


def main_thread():
    print('开始下载：《' + dl.bookname + '》')
    threads = []  #演示多线程爬取
    for i in range(dl.nums):
        #dl.get_contents(dl.names[i], dl.urls[i]) # 单线程
        pool = threading.Thread(
            target=dl.get_contents, args=(dl.names[i], dl.urls[i]))
        threads.append(pool)
        pool.start()
    for pool in threads:
        pool.join()  # join等待其他子线程执行结束
    print('\r《' + dl.bookname + '》完成下载')


def main_Pool():
    '''
    @description:库错误提示
    '''
    print('开始下载：《' + dl.bookname + '》')
    from multiprocess.pool import Pool
    pool = Pool(6)
    for i in range(dl.nums):
        pool.apply_async(func=dl.get_contents, args=(dl.names[i], dl.urls[i]))
    #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    pool.close()
    pool.join()  # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
    print('\r《' + dl.bookname + '》完成下载')


if __name__ == "__main__":
    global dl
    dl = downloader()
    dl.get_download_url()
    # 选择多线程
    main_thread()
    #main_Pool()

    dl.writer()
