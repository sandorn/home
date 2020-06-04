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
@LastEditTime: 2019-05-10 16:55:14

Python3网络爬虫快速入门实战解析（一小时入门 Python 3 网络爬虫） - u012662731的博客 - CSDN博客
https://blog.csdn.net/u012662731/article/details/78537432

爬虫笔记——第三方库Beautiful Soup4 使用总结 - 简书
https://www.jianshu.com/p/1ba25d35ff25

python requests用法总结 - lwli - 博客园
https://www.cnblogs.com/lilinwei340/p/6417689.html
'''

import time
from functools import wraps

import requests
from bs4 import BeautifulSoup


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
        self.target = 'https://www.biqukan.com/14_14986/'
        self.names = []  #存放章节名
        self.urls = []  #存放章节链接
        self.nums = 0  #章节数
        self.bookname = ''  #书名
        self.text = {}

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
        tr = div_bf.find_all('h2')[0]
        self.bookname = tr.get_text()

        div = str(div_bf.find_all('div', class_='listmain')[0])
        a_bf = BeautifulSoup(div, features="html5lib")
        a = a_bf.find_all('a')
        self.nums = len(a[15:])  #剔除不必要的章节，并统计章节数
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    #@decorator_timer
    def get_contents(self, name, target):
        """
        函数说明:获取章节内容
        Parameters:target - 下载连接(string)
        Returns:texts - 章节内容(string)

        @description:将获取到的章节内容保存到字典
        @param{name:章节名,text:章节内容}
        """
        headers = {
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":
                "gzip, deflate, br",
            "Accept-Language":
                "zh-CN,zh;q=0.9",
            "Connection":
                "keep-alive",
            "Host":
                "www.biqukan.com",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        while True:
            response = requests.get(url=target, headers=headers)
            if response.status_code == requests.codes.ok:
                #print('get_contents:ok')
                break
            time.sleep(0.2)

        texts = ''
        html = response.text
        bf = BeautifulSoup(html, 'html5lib')
        tr = bf.select('.showtxt')[0]
        for text in tr.stripped_strings:
            texts += text + '\n'
        self.text[name] = texts

    def writer(self):
        """
        函数说明:将爬取的文章内容写入文件
        Parameters:
            name - 章节名称(string)
            path - 当前路径下,小说保存名称(string)
            text - 章节内容(string)
        """
        with open(self.bookname + '.txt', 'a', encoding='utf-8') as f:
            for k, v in self.text.items():
                f.write(str(k) + '\n' + str(v) + '\n')


if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()

    print('《' + dl.bookname + '》开始下载：')
    _stime = time.time()
    for i in range(dl.nums):
        if i > 3:
            break
        dl.get_contents(dl.names[i], dl.urls[i])
        print(
            "\r # Process: {0}{1},已经用时：{2}".format(
                "|" * i, '%.3f%%' % float(i / dl.nums),
                round((time.time() - _stime) * 1000)),
            end="",
            flush=True)
        time.sleep(0.1)
        # \033[2J 清屏  #\033[nA 是光标上移 n 行
    print('\r《' + dl.bookname + '》下载完成')

    print('《' + dl.bookname + '》开始保存')
    dl.writer()
    print('《' + dl.bookname + '》保存完成，任务结束')
