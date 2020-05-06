# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-31 12:12:40
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-06 15:11:54
'''

import os

from xjLib.mystr import savefile
from xjLib.CustomThread import CustomThread
from xjLib.mystr import Ex_Re_Sub, Ex_Replace
from xjLib.req import RequestsSession
Session = RequestsSession()


def get_download_url(target):
    urls = []  # 存放章节链接
    response = Session.get(target).html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(lock, index, target):
    response = Session.get(target)
    print(response)
    response = Session.get(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  "),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            # '\xa0': '',  # 表示空格  &nbsp;  dictionary key '\xa0' repeated with different values
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


def main(bookname, args):
    _ = [
        CustomThread(get_contents, [index, url])
        for index, url in enumerate(urls)
    ]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


if __name__ == "__main__":
    bookname, urls = get_download_url(
        'http://www.biqukan.com/38_38836/')  # 38_38836  #2_2714

    main(bookname, urls)
