# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-01 10:29:33
#FilePath     : /xjLib/xt_Ls_Bqg.py
#LastEditTime : 2020-06-05 23:16:08
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from xt_Ahttp import ahttpGet
from xt_Log import log
from xt_Requests import get
from xt_String import Ex_Re_Clean, Ex_Str_Replace


def arrangeContent(textlist):
    temp_list = ["', '", '&nbsp;', r';\[笔趣看  www.biqukan.com\]', r'\(https://www.biqukan.com/[0-9]{1,4}_[0-9]{3,8}/[0-9]{3,14}.html\)', 'www.biqukan.com。', 'wap.biqukan.com', 'www.biqukan.com', 'm.biqukan.com', 'n.biqukan.com', '百度搜索“笔趣看小说网”手机阅读:', '百度搜索“笔趣看小说网”手机阅读：', '请记住本书首发域名:', '请记住本书首发域名：', '笔趣阁手机版阅读网址:', '笔趣阁手机版阅读网址：', '<br />', r';\[笔趣看  \]', r'\[笔趣看 \]']
    adict = {
        '<br />': '\n',
        '\r\r': '\n',
        '\r': '\n',
        '    ': '\n    ',
        '\n\n\n': '\n',
        '\n\n': '\n',
        '\n\n': '\n',
    }
    oldtext = '\n'.join([item.strip("\r\n　  ") for item in textlist])
    newtext = oldtext.strip("\r\n　  ").replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    newtext = Ex_Re_Clean(newtext, temp_list)
    newtext = Ex_Str_Replace(newtext, adict)
    return newtext


def get_download_url(target):
    urls = []  # 存放章节链接
    response = ahttpGet(target).element
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_title_url(target):
    _list = []
    _res = ahttpGet(target)
    element = _res.element

    bookname = element.xpath('//meta[@property="og:title"]//@content')[0]

    全部章节节点 = element.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a')
    baseurl = '/'.join(target.split('/')[0:-2])
    for item in 全部章节节点:  # 遍历文章列表
        _href = item.xpath("@href")[0]  # 章节链接
        _text = item.xpath("string(.)").strip()  # 章节标题
        _list.append([_text, baseurl + _href])  # 获取遍历到的具体文章地址

    return bookname, _list


def get_biqugeinfo_url(target):
    urls = []  # 存放章节链接
    response = ahttpGet(target).element
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//dl/dd/a/@href')

    for item in 全部章节节点:
        urls.append(target + item)
    return _bookname, urls


def get_contents(index=None, target=None, lock=None):
    response = get(target).element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    return [index, title, content]


def get_contents_byahttp(index, target, lock):
    response = ahttpGet(target).element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    return [index, title, content]


def map_get_contents_byahttp(*args):
    index, target = args  # 元组拆包
    response = ahttpGet(target).element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    return [index, title, content]


if __name__ == "__main__":
    pass
