# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 不使用循环，不反防爬虫,随机中断
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 18:31:14
@LastEditTime: 2019-05-09 17:28:44

Python3网络爬虫快速入门实战解析（一小时入门 Python 3 网络爬虫） - u012662731的博客 - CSDN博客
https://blog.csdn.net/u012662731/article/details/78537432

爬虫笔记——第三方库Beautiful Soup4 使用总结 - 简书
https://www.jianshu.com/p/1ba25d35ff25

python requests用法总结 - lwli - 博客园
https://www.cnblogs.com/lilinwei340/p/6417689.html
'''

from functools import wraps
import time

import requests
from bs4 import BeautifulSoup


def _timeout(method_to_decorate):
    #为了保留被装饰函数的函数名和帮助文档信息,不理解
    @wraps(method_to_decorate)
    # 在内部定义了另外一个函数：一个封装器。
    # 这个函数将原始函数进行封装，所以你可以在它之前或者之后执行一些代码
    def wrapper(self, *args, **kwargs):
        # 放一些你希望在真正函数执行前的一些代码
        print('args:', args)
        #print('kwargs:', kwargs)
        startTime = time.time()
        # 执行原始函数
        #有返回值的函数，前面需要添加return
        res = method_to_decorate(self, *args, **kwargs)
        endTime = time.time()
        msecs = (endTime - startTime) * 1000
        print("time is %d ms" % msecs)
        return res

    #在此刻，"wrapper"还没有被执行，我们返回了创建的封装函数
    #封装器包含了函数以及其前后执行的代码，其已经准备完毕
    return wrapper


class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.target = 'https://www.biqukan.com/14_14986/'
        self.names = []  #存放章节名
        self.urls = []  #存放章节链接
        self.nums = 0  #章节数
        self.bookname = ''  #书名

    def get_download_url(self):
        req = requests.get(url=self.target)
        print(req.status_code)
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

    @_timeout
    def get_contents(self, target):
        """
        函数说明:获取章节内容
        Parameters:target - 下载连接(string)
        Returns:texts - 章节内容(string)
        """
        req = requests.get(url=target)
        texts = ''
        html = req.text
        bf = BeautifulSoup(html, 'html5lib')
        tr = bf.select('.showtxt')[0]
        for text in tr.stripped_strings:
            texts += text + '\n'
        #texts = texts.replace('\xa0' * 8, '\n\n')
        return texts

    def writer(self, name, path, text):
        """
        函数说明:将爬取的文章内容写入文件
        Parameters:
            name - 章节名称(string)
            path - 当前路径下,小说保存名称(string)
            text - 章节内容(string)
        """
        #write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《' + dl.bookname + '》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], dl.bookname + '.txt',
                  dl.get_contents(dl.urls[i]))
        time.sleep(3)  # 等待3秒
        print("  已下载:%.3f%%" % float(i / dl.nums) + '\r')
    print('《' + dl.bookname + '》下载完成')
