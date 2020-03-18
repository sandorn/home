# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 23:35:58
@LastEditors: Even.Sand
@LastEditTime: 2020-03-18 02:39:25
变更requests为ahttp
'''
import os
import time

from xjLib.ahttp import ahttpGet, ahttpGetAll
from xjLib.mystr import Ex_Re_Sub, get_stime, savefile, Ex_Replace


def get_download_url(target):
    urls = []  # 存放章节链接
    resp = ahttpGet(target)
    # response = resp.html
    # 指定解析器
    response = resp.html

    _bookname = response.xpath('//h2/text()', first=True)[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []


def 结果处理(resps):
    for resp in resps:
        index = resp.index
        response = resp.html

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
        texts.append([index, name, '    ' + text])


def callback(resp):
    if resp is None: return

    index = resp.index
    response = resp.html

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
    print(str(index) + '\t号任务,has done。', flush=True)
    texts.append([index, name, '    ' + text])


def main(url):
    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)
    print('AHTTP,开始下载：《' + bookname + '》', flush=True)

    # 方法2：不回调，获取最终结果，自动排序
    resps = ahttpGetAll(urls, pool=200)
    print('小说爬取完成，开始整理数据\t time:{} 。'.format(get_stime()))

    结果处理(resps)
    print('AHTTP，书籍《' + bookname + '》数据整理完成，time:{}'.format(get_stime()), flush=True)

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    savefile(bookname + '.txt', aftertexts, br='\n')
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)


def mainbycall(url):
    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)
    print('AHTTP,开始下载：《' + bookname + '》', flush=True)

    # 方法1：使用回调，不排序
    ahttpGetAll(urls, pool=500, callback=callback)
    print('AHTTP，书籍《' + bookname + '》完成下载')

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + '.txt', aftertexts, br='\n')
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)))


if __name__ == '__main__':
    url = 'https://www.biqukan.com/2_2714/'
    _stime = time.time()
    mainbycall(url)
    # texts = []
    # main(url)

    # '76_76519'  #章节少，#@  4秒
    # '38_38836'  #2676KB，#@  9秒
    # '0_790'     #8977KB，#@  13秒
    # "10_10736"    #34712KB，#@  24秒
    # "2_2714"    #武炼巅峰，#@  36秒
