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
@LastEditTime: 2020-03-15 19:10:02
'''
import threading
import time
from queue import Queue

from xjLib.ahttp import ahttpGet
from xjLib.mystr import Ex_Re_Sub, savefile
from xjLib.req import parse_get

lock = threading.RLock()
urls = Queue()  # 存放章节链接
texts = []  # 将爬下来的小说都存在里面，做最后排序
SemaphoreNum = 100
semaphore = threading.BoundedSemaphore(SemaphoreNum)  # 设置同时执行的线程数，其他等待执行


def get_download_url(target):
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.put(_ZJHERF)
    return _bookname


def get_contents(index):
    with semaphore:
        target = urls.get()
        response = parse_get(target).html
        _name = response.xpath('//h1/text()')[0]
        _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

        name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' '})
        text = Ex_Re_Sub(
            _showtext,
            {
                '\'': '',
                ' ': ' ',
                '\xa0': ' ',
                '\x0a': '\n',
                # '\b;': '\n',
                '&nbsp;': ' ',
                'app2();': '',
                '笔趣看;': '',
                '\u3000': '',
                'chaptererror();': '',
                'readtype!=2&&(\'vipchapter\n(\';\n\n}': '',
                'm.biqukan.com': '',
                'wap.biqukan.com': '',
                'www.biqukan.com': '',
                'www.biqukan.com。': '',
                '百度搜索“笔趣看小说网”手机阅读:': '',
                '请记住本书首发域名:': '',
                '请记住本书首发域名：': '',
                '笔趣阁手机版阅读网址:': '',
                '笔趣阁手机版阅读网址：': '',
                '[]': '',
                '\r': '\n',
                '\n\n': '\n',
                '\n\n': '\n',
            },
        )

        with lock:
            texts.append([index, name, text])
            print(threading.current_thread().name + '线程 #{} 号  has done。\n'.format(index), end='', flush=True)
        urls.task_done()  # 发出此队列完成信号


def main_thread(target):
    _stime = time.time()
    bookname = get_download_url(target)
    thread_list = []
    print('threading-调用，开始下载：《' + bookname + '》', flush=True)
    for index in range(urls.qsize()):
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
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, 250秒。100线程
    #!为什么调用明显慢于继承
