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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-29 09:44:03
'''

import os
import time

from xt_Ahttp import ahttpGet, ahttpGetAll
from xt_Ls_Bqg import arrangeContent
from xt_File import savefile
from xt_Time import get_lite_time


def get_download_url(target):
    urls = []  # 存放章节链接
    resp = ahttpGet(target)
    # response = resp.html
    # 指定解析器
    response = resp.html

    _bookname = response.xpath('//h1/text()', first=True)[0]
    全部章节节点 = response.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.lingdianksw.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []


def callback(resp):

    index = resp.index
    response = resp.element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000',
                                         u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    texts.append([index, title, content])


def main(url):
    bookname, urls = get_download_url(url)
    print('AHTTP,开始下载：《' + bookname + '》', flush=True)

    resps = ahttpGetAll(urls, pool=200, callback=callback)

    texts.sort(key=lambda x: x[0])  # #排序
    # texts = [[row[i] for i in range(1, 3)] for row in texts]
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'mainbycall.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.lingdianksw.com/48/48443/'
    _stime = time.time()
    main(url)
'''
#'https://www.lingdianksw.com/48/48443/'  size: 19.01 MB   11 seconds
#'https://www.lingdianksw.com/0/404/'  size: 14.77 MB   11 seconds
#'https://www.lingdianksw.com/0/405/' size: 3266.95 KB    5seconds
'''
