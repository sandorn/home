# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-13 11:34:00
@LastEditors: Even.Sand
@LastEditTime: 2020-03-13 11:53:43
'''

import multiprocessing
import time

from lxml import etree

from xjLib.ahttp import ahttpGet, ahttpGetAll
from xjLib.mystr import get_stime, savefile


def get_download_url(target):
    urls = []  # 存放章节链接
    resp = ahttpGet(target)
    # response = resp.html
    # 指定解析器
    response = etree.HTML(resp.text)

    _bookname = response.xpath('//h2/text()', first=True)[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(lock, index, target):
    _texts = ''
    resp = ahttpGet(target)
    # response = resp.html
    # 指定解析器
    response = etree.HTML(resp.text)

    _name = response.xpath('//h1/text()', first=True)[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    for text in _showtext.stripped_strings:
        _texts = text + '\n'

    with lock:
        print('{} done with {} at {}'.format(multiprocessing.current_process().name, index, get_stime()), flush=True)
    return [index, _name, _texts]


def main_Pool(target):
    _stime = time.time()
    # 父进程创建Queue\lock，传给个子进程：
    lock = multiprocessing.Manager().Lock()

    print('开始下载：《{}》\t{}\t获取下载链接......'.format(target, get_stime()), flush=True)
    bookname, urls = get_download_url(target)
    print('multiprocessing.pool，开始下载：《' + bookname + '》', flush=True)
    mypool = multiprocessing.Pool(25)  # !进程数
    # 创建多进程队列
    future_tasks = []
    for i in range(len(urls)):
        item = mypool.apply_async(get_contents, args=(lock, i, urls[i]))
        # pool.apply_async(func=task,callback=_callba)
        future_tasks.append(item)
    mypool.close()  # 关闭进程池,不再接受请求
    mypool.join()  # 等待进程池中的事件执行完毕，回收进程池

    texts = []  # 将爬下来的小说都存在里面
    for item in future_tasks:
        _text = item.get()  # join后获取进程返回值
        texts.append(_text)

    print('\n multiprocessing.pool，书籍《' + bookname + '》完成下载', flush=True)
    savefile(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_Pool('https://www.biqukan.com/65_65593/')
    # '65_65593'  #章节少，测试用 26秒
    # '2_2704'  #231万字  #6239kb, 420.94 秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
