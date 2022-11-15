# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-04-01 10:29:33
FilePath     : /xjLib/xt_Ls_Bqg.py
LastEditTime : 2021-04-14 19:36:16
# Github       : https://github.com/sandorn/home
# ==============================================================
'''

from xt_Ahttp import ahttpGet
from xt_Requests import get
from xt_String import Str_Replace, Str_Clean, Re_Sub
from xt_Response import ReqResult


def clean_Content(in_str):
    clean_list = [
        "', '",
        '&nbsp;',
        ';[笔趣看  www.biqukan.com]',
        'www.biqukan.com。',
        'wap.biqukan.com',
        'www.biqukan.com',
        'm.biqukan.com',
        'n.biqukan.com',
        'www.biqukan8.cc。',
        'www.biqukan8.cc',
        'm.biqukan8.cc。',
        'm.biqukan8.cc',
        '百度搜索“笔趣看小说网”手机阅读:',
        '百度搜索“笔趣看小说网”手机阅读：',
        '请记住本书首发域名:',
        '请记住本书首发域名：',
        '笔趣阁手机版阅读网址:',
        '笔趣阁手机版阅读网址：',
        '关注公众号：书友大本营  关注即送现金、点币！',
        '<br />',
        ';[笔趣看  ]',
        '[笔趣看 ]',
        '<br />',
        '\t',
    ]
    sub_list = [
        (r'\(https:///[0-9]{0,4}_[0-9]{0,12}/[0-9]{0,16}.html\)', ''),
    ]
    repl_list = [
        (u'\u3000', ' '),
        (u'\xa0', ' '),
        (u'\u00a0', ' '),
        ('\r', '\n'),
        ('    ', '\n    '),
        ('\r\n', '\n'),
        ('\n\n', '\n'),
    ]

    if isinstance(in_str, (list, tuple)):
        in_str = '\n'.join([item.strip("\r\n　  ") for item in in_str])
    in_str = in_str.strip("\r\n ")

    in_str = Str_Clean(in_str, clean_list)
    in_str = Re_Sub(in_str, sub_list)
    in_str = Str_Replace(in_str, repl_list)
    return in_str


def 结果处理(resps):
    """传入的是爬虫数据包的集合"""
    _texts = []

    for resp in resps:
        if resp is None:
            continue
        index = resp.index
        response = resp.element if resp.element is not None else resp.html

        _title = "".join(response.xpath('//h1/text()'))
        title = Str_Replace(_title, [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
        _showtext = response.xpath('//*[@id="content"]/text()')
        content = clean_Content(_showtext)
        _texts.append([index, title, content])

    return _texts


def get_download_url(target):
    res = get(target)
    assert isinstance(res, ReqResult)
    response = res.element
    bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    temp_urls = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')
    titles = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/text()')
    baseurl = '/'.join(target.split('/')[0:-2])
    urls = [baseurl + item for item in temp_urls]  ## 章节链接
    return bookname, urls, titles
    ## https://chuangshi.qq.com/bk/ds/43345375.html
    ## /html/body/div[3]/div[3]/div[1]/div[1]/a/b  #书名
    ## body > div.wrap > div.mainbox > div.main1 > div.title > a > b
    ## /html/body/div[3]/div[3]/div[1]/div[4]/ul/li[2]/a/@href  #目录
    ## //ul[@class="block_ul"/li/a/@href  # 章节
    ## /html/body/div[3]/div[4]/div/div[1]/ul/li[2]/a/b/text() #章节标题
    ## /html/body/div[1]/div[4]/div[2]/div/div[2]/div/div/div[@class="bookreadercontent"] #正文内容


def get_biqugse_download_url(target):
    res = get(target)
    assert isinstance(res, ReqResult)
    response = res.element
    bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    temp_urls = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/@href')
    titles = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()')
    baseurl = '/'.join(target.split('/')[0:-2])
    urls = [baseurl + item for item in temp_urls]  ## 章节链接
    return bookname, urls, titles


def get_contents(args, func=get):
    (index, target) = args
    res = func(target)
    assert isinstance(res, ReqResult)
    response = res.element

    _title = "".join(response.xpath('//h1/text()'))
    title = Str_Replace(_title, [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = clean_Content(_showtext)
    return [index, title, content]


def map_get_contents(args):
    return get_contents(args)


def ahttp_get_contents(args):
    return get_contents(args, ahttpGet)


def map_get_contents_ahttp(args):
    return ahttp_get_contents(args)


if __name__ == "__main__":
    url = 'https://www.biqukan.com/69_69034/458679741.html'
    res = ahttpGet(url)
    response = res.element
    _title = "".join(response.xpath('//h1/text()'))
    title = Str_Replace(_title, [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
    _showtext = response.xpath('//*[@id="content"]/text()')
    print(title, '\n', '*' * 88)

    print(clean_Content(_showtext), '\n', '*' * 88)
