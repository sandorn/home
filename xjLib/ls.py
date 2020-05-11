# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-01 10:29:33
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-11 17:39:45
临时库
'''

from xjLib.xt_ahttp import ahttpGet
from xjLib.mystr import (Ex_Re_Sub, Ex_Replace)
from xjLib.req import parse_get


def get_download_url(target):
    urls = []  # 存放章节链接
    response = ahttpGet(target).element
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_biqugeinfo_url(target):
    urls = []  # 存放章节链接
    response = ahttpGet(target).element
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//dl/dd/a/@href')

    for item in 全部章节节点:
        urls.append(target + item)
    return _bookname, urls


def get_contents(lock, index, target):
    response = parse_get(target).element

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    name = Ex_Re_Sub(_name, {' ': '', ' ': ''})
    text = Ex_Replace(
        _showtext.strip("\n\r　  "),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            # '\xa0': '',  # 表示空格  &nbsp;
            '\u3000': '',  # 全角空格
            '/&nbsp;': '',  # 全角空格
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
            '    ': '\n    ',
        },
    )

    return [index, name, '    ' + text]


def get_contents_byahttp(lock, index, target):
    response = ahttpGet(target).element

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  "),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            # '\xa0': '',  # 表示空格  &nbsp;
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


def map_get_contents_byahttp(args):
    print(args)
    [index, target] = args
    response = ahttpGet(target).element

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  "),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            # '\xa0': '',  # 表示空格  &nbsp;
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


if __name__ == "__main__":
    pass
