# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-02-29 23:00:26
@LastEditors: Even.Sand
@LastEditTime: 2020-03-18 02:04:19
https://blog.csdn.net/ksws0393238aa/article/details/20286405?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
'''

import os
import time
from threading import BoundedSemaphore, RLock, Thread, currentThread

from xjLib.mystr import Ex_Re_Sub, savefile, Ex_Replace
from xjLib.req import parse_get

lock = RLock()
texts = []  # 将爬下来的小说存列表list，做最后排序


class myThread(Thread):
    all_Thread = []

    def __init__(self, MaxSem, func, parameter):
        # 注意：一定要显式的调用父类的初始化函数。
        super(myThread, self).__init__()
        self.func = func  # func为想要调用的函数
        self.parameter = parameter
        # 添加一个标识符，指示线程是否在进行
        self.isRunning = True
        self.MaxSem = MaxSem
        myThread.all_Thread.append(self)

    def run(self):
        with self.MaxSem:  # 同时并行线程数量
            self.res = self.func(*self.parameter)

    def result(self):
        try:
            return self.res
        except Exception:
            return None

    def stop(self):
        # 结束线程的标识符
        self.isRunning = False


def get_contents(index, target):
    """以下为需要重复的单次函数操作"""
    response = parse_get(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  \xa0"),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            '\xa0': '',  # 表示空格  &nbsp;
            '\u3000': '',  # 全角空格
            'www.biqukan.com。': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            '笔趣看;': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '<br />': '',
            '\r\r': '\n',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        },
    )

    texts.append([index, name, '    ' + text])

    with lock:
        print(currentThread().name, '\tindex:', index, '\tdone。', flush=True)

    return [index, name, '    ' + text]


def get_download_url(target):
    urls = []  # 存放章节链接
    # response = etree.HTML(parse_get(target).content)
    resp = parse_get(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def main_thread(target):
    _stime = time.time()
    bookname, urls = get_download_url(target)
    print('threading-继承，开始下载：《' + bookname + '》', flush=True)

    # 设置同时执行的线程数，其他等待执行
    MaxSem = BoundedSemaphore(200)

    thread_list = []
    for index in range(len(urls)):
        res = myThread(MaxSem, get_contents, (index, urls[index]))
        res.start()
        thread_list.append(res)

    for item in thread_list:
        item.join()  # join等待线程执行结束
        # callback(item.result()) # 获取线程结果,并回调
    print('threading-继承，书籍《' + bookname + '》完成下载', flush=True)

    texts.sort(key=lambda x: x[0])
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + '.txt', aftertexts, br='\n')
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_thread('https://www.biqukan.com/2_2714/')
    # '38_38836'  #34秒
    # '10_10736'  #
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, #!77秒。无线程限制
    # '0_790'    #《元尊》328万字， 8988KB， 45秒钟
