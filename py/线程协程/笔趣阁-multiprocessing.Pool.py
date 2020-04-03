# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 使用multiprocessing.pool多进程
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 18:31:14
@LastEditTime: 2020-04-02 09:17:31
努努书坊 - 小说在线阅读   https://www.kanunu8.com/
'''

import multiprocessing
import time
import os

from xjLib.mystr import (Ex_Re_Sub, Ex_Replace, fn_timer, savefile)
from xjLib.req import parse_get
from xjLib.ahttp import ahttpGet


def get_download_url(target):
    urls = []  # 存放章节链接
    # response = etree.HTML(parse_get(target).content)
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(lock, index, target):
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

    return [index, name, '    ' + text]


@fn_timer
def main_Pool(target):
    lock = multiprocessing.Manager().Lock()

    bookname, urls = get_download_url(target)

    print('multiprocessing.pool，开始下载：《' + bookname + '》', flush=True)
    mypool = multiprocessing.Pool(32)   # !进程数,不能超过61

    future_tasks = []
    for i in range(len(urls)):
        item = mypool.apply_async(get_contents, args=(lock, i, urls[i]))
        # mypool.apply_async(func=task,callback=_callba)
        future_tasks.append(item)
    mypool.close()  # 关闭进程池,不再接受请求
    mypool.join()  # 等待进程池中的事件执行完毕，回收进程池

    texts = []  # 将爬下来的小说都存在里面
    for task in future_tasks:
        res = task.get()  # join后获取进程返回值
        texts.append(res)

    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'multiprocessing.txt', texts, br='\n')


if __name__ == '__main__':
    main_Pool('https://www.biqukan.com/38_38836/')
    # 38_38836     34.84 seconds
    # 2_2714      215.40 seconds
