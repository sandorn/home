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
@LastEditTime: 2020-03-05 12:30:12
获取元素
request-html支持CSS选择器和XPATH两种语法来选取HTML元素。首先先来看看CSS选择器语法，它需要使用HTML的find函数，该函数有5个参数，作用如下：
- selector，要用的CSS选择器；
- clean，布尔值，如果为真会忽略HTML中style和script标签造成的影响（原文是sanitize，大概这么理解）;
- containing，如果设置该属性，会返回包含该属性文本的标签；
- first，布尔值，如果为真会返回第一个元素，否则会返回满足条件的元素列表；
- _encoding，编码格式。
————————————————
版权声明：本文为CSDN博主「过了即是客」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u011054333/article/details/81055423
'''

import threading
import time
from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块

from requests_html import HTMLSession  # @新增，与requests配套html解析组件

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile

lock = threading.Lock()

session = HTMLSession()


def get_download_url(target):
    urls = []  # 存放章节链接
    response = session.get(target).html
    _bookname = response.xpath('//h2', first=True).text
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(index, target):
    response = session.get(target).html
    _name = response.xpath('//h1', first=True).text
    _showtext = "".join(response.xpath('//*[@id="content"]', first=True).text)
    with lock:
        print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)
    return [index, _name, _showtext]


texts = []

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


if __name__ == '__main__':
    url = 'https://www.biqukan.com/2_2714/'
    _stime = time.time()
    urls = []  # 存放章节链接

    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)
    print('CFThreadPool,开始下载：《' + bookname + '》', flush=True)

    # 创建多进程队列, 回调方式
    with Pool(100) as p:
        future_tasks = [
            p.submit(get_contents, i, urls[i]).add_done_callback(callback)for i in range(len(urls))
        ]

    '''
    # 返回值方式
    from concurrent.futures import as_completed
    for task in as_completed(future_tasks):
        if task.done():
            try:
                callback(task.result())
            except Exception as e:
                print("task.result()error:", e)
    '''

    print('\nCFThreadPool，书籍《' + bookname + '》完成下载', flush=True)
    texts.sort(key=lambda x: x[0])
    savefile(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)

    # '76_76519'  #章节少，测试用
    # "2_2714"   #《武炼巅峰,#!87.5秒
