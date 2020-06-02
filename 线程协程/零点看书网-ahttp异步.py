# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-22 20:46:01
@LastEditors: Even.Sand
@LastEditTime: 2020-03-22 21:05:05
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

    _bookname = response.xpath('//h1/text()', first=True)[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.lingdianksw.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []


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
    #print(resp.task, 'index:', index, ',has done。', flush=True)
    texts.append([index, name, '    ' + text])


def main(url):
    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)
    print('AHTTP,开始下载：《' + bookname + '》', flush=True)

    ahttpGetAll(urls, pool=500, timeout=60, callback=callback)
    print('AHTTP，书籍《' + bookname + '》完成下载。time：' + get_stime())

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + '.txt', aftertexts, br='\n')
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)))


if __name__ == '__main__':
    url = 'https://www.lingdianksw.com/48/48443/'
    _stime = time.time()
    main(url)

'''
#'https://www.lingdianksw.com/48/48443/'  #76.489 seconds
'''
