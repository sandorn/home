# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-04-01 10:29:33
#FilePath     : /xjLib/xt_Ls_Bqg.py
#LastEditTime : 2020-06-24 19:14:52
# Github       : https://github.com/sandorn/home
# ==============================================================
'''

from xt_Ahttp import ahttpGet
from xt_Requests import get
from xt_String import Ex_Re_Clean, Ex_Str_Replace, Ex_Re_Repl
from xt_Response import ReqResult


def clean_Content(string, repl_list=None):
    if repl_list is None:
        repl_list = [
            ("', '", ''),
            ('&nbsp;', ''),
            (r';\[笔趣看  www.biqukan.com\]', ''),
            (r'\(https://www.biqukan.com/[0-9]{1,4}_[0-9]{3,8}/[0-9]{3,14}.html\)',
             ''),
            ('www.biqukan.com。', ''),
            ('wap.biqukan.com', ''),
            ('www.biqukan.com', ''),
            ('m.biqukan.com', ''),
            ('n.biqukan.com', ''),
            ('百度搜索“笔趣看小说网”手机阅读:', ''),
            ('百度搜索“笔趣看小说网”手机阅读：', ''),
            ('请记住本书首发域名:', ''),
            ('请记住本书首发域名：', ''),
            ('笔趣阁手机版阅读网址:', ''),
            ('笔趣阁手机版阅读网址：', ''),
            (r';\[笔趣看  \]', ''),
            (r'\[笔趣看 \]', ''),
            ('<br />', '\n'),
            ('\r\r', '\n'),
            ('\r', '\n'),
            ('    ', '\n    '),
            ('\n\n\n', '\n'),
            ('\n\n', '\n'),
            ('\n\n', '\n'),
        ]

    if isinstance(string, (list, tuple)):
        string = '\n'.join([item.strip("\r\n　  ") for item in string])

    return Ex_Re_Repl(string, repl_list)


def arrangeContent(string):
    clean_list = [
        "', '", '&nbsp;', r';\[笔趣看  www.biqukan.com\]',
        r'\(https://www.biqukan.com/[0-9]{1,4}_[0-9]{3,8}/[0-9]{3,14}.html\)',
        'www.biqukan.com。', 'wap.biqukan.com', 'www.biqukan.com',
        'm.biqukan.com', 'n.biqukan.com', '百度搜索“笔趣看小说网”手机阅读:',
        '百度搜索“笔趣看小说网”手机阅读：', '请记住本书首发域名:', '请记住本书首发域名：', '笔趣阁手机版阅读网址:',
        '笔趣阁手机版阅读网址：', '<br />', r';\[笔趣看  \]', r'\[笔趣看 \]'
    ]
    repl_dict = [
        (r'<br />', '\n'),
        (r'\r\r', '\n'),
        (r'\r', '\n'),
        (r'    ', '\n    '),
        (r'\n\n\n', '\n'),
        (r'\n\n', '\n'),
        (r'\n\n', '\n'),
    ]
    if isinstance(string, (list, tuple)):
        string = '\n'.join([item.strip("\r\n　  ") for item in string])
    string = string.strip("\r\n　  ").replace(u'\u3000',
                                             u' ').replace(u'\xa0', u' ')
    string = Ex_Re_Clean(string, clean_list)
    string = Ex_Str_Replace(string, repl_dict)
    return string


def get_download_url(target):
    urls = []  # 存放章节链接
    res = get(target)
    assert isinstance(res, ReqResult)
    response = res.element

    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_title_url(target):
    _list = []
    _res = get(target)
    element = _res.element

    bookname = element.xpath('//meta[@property="og:title"]//@content')[0]

    全部章节节点 = element.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a')
    baseurl = '/'.join(target.split('/')[0:-2])
    for item in 全部章节节点:  # 遍历文章列表
        _href = item.xpath("@href")[0]  # 章节链接
        _text = item.xpath("string(.)").strip()  # 章节标题
        _list.append([_text, baseurl + _href])  # 获取遍历到的具体文章地址
    return bookname, _list


def get_biqugeinfo_url(target):
    urls = []  # 存放章节链接
    response = get(target).element
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//dl/dd/a/@href')

    for item in 全部章节节点:
        urls.append(target + item)
    return _bookname, urls


def get_contents(index, target):
    res = get(target)
    assert isinstance(res, ReqResult)
    t = res.elapsed.total_seconds()  # @运行时间
    print(f'SessionClient get<{target}> use total_seconds:{t}')

    response = res.element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000',
                                         u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    return [index, title, content]


def _get_contents_ahttp(index, target):
    response = ahttpGet(target).element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000',
                                         u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    return [index, title, content]


def map_get_contents(*args):
    index, target = args[0]  # 元组拆包
    return _get_contents_ahttp(index, target)


if __name__ == "__main__":
    url = 'https://www.biqukan.com/69_69034/458679741.html'
    res = get(url)
    response = res.element
    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000',
                                         u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')

    print(arrangeContent(_showtext), '*' * 88)
    print(clean_Content(_showtext), '*' * 88)
