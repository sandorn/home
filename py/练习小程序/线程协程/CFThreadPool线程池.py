# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 00:20:05
@LastEditors: Even.Sand
@LastEditTime: 2020-03-01 18:51:07
'''

import threading
import time
from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块

from lxml import etree

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile
from xjLib.req import parse_get

lock = threading.Lock()
texts = []


def get_download_url(target):
    urls = []  # 存放章节链接
    response = etree.HTML(parse_get(target).content)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(index, target):
    response = etree.HTML(parse_get(target).content)
    _name = response.xpath('//h1/text()')[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    with lock:
        print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)
    return [index, _name, _showtext]


# 回调方式获取线程结果
def callback(future):
    index, _name, _showtext = future.result()  # 回调函数取得返回值
    name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })

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
        }
    )
    texts.append([index, name, text])


def main_Pool(target):
    _stime = time.time()
    urls = []  # 存放章节链接

    print('开始下载：《{}》\t{}\t获取下载链接......'.format(target, get_stime()), flush=True)
    bookname, urls = get_download_url(target)
    print('CFThreadPool,开始下载：《' + bookname + '》', flush=True)
    # 创建多进程队列, 回调方式
    with Pool(50) as p:
        _ = [
            p.submit(get_contents, i, urls[i]).add_done_callback(callback)for i in range(len(urls))
        ]

    print('\nCFThreadPool，书籍《' + bookname + '》完成下载', flush=True)
    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)


if __name__ == '__main__':
    main_Pool('https://www.biqukan.com/2_2714/')
    # '76_76519'  #章节少，测试用
    # "2_2714"   #《武炼巅峰》664万字,#!87.5秒

    '''
    # 返回值方式
    with Pool(50) as p:
        future_tasks = [p.submit(get_contents,  i, urls[i]) for i in range(len(urls))]

    from concurrent.futures import as_completed
    texts = []  # 将爬下来的小说都存在里面，做最后排序
    for obj in as_completed(future_tasks):
        if obj.done():
            try:
                texts.append(obj.result())
            except Exception as e:
                print("obj.result()error:", e)
    '''
