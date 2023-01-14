# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:36:04
LastEditTime : 2022-12-14 22:42:13
FilePath     : /py学习/asyncio学习/零点看书网-ahttp异步.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import ahttpGet, ahttpGetAll
from xt_File import savefile
from xt_Ls_Bqg import clean_Content
from xt_Response import htmlResponse


def get_download_url(target):
    resp = ahttpGet(target)
    response = resp.html

    _bookname = response.xpath('//h1/text()', first=True)[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    urls = [f'https://www.lingdianksw.com{item}' for item in 全部章节节点]
    return _bookname, urls


texts = []


def callback(resp):
    if not isinstance(resp, htmlResponse):
        texts.append([resp.index, resp.result])
        print(1111111111111111111, resp.index, resp.result)
        return

    index = resp.index
    response = resp.element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = clean_Content(_showtext)
    texts.append([index, title, content])


def main(url):
    bookname, urls = get_download_url(url)
    print(f'AHTTP,开始下载：《{bookname}》', flush=True)

    resps = ahttpGetAll(urls, callback=callback)

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}＆{bookname}mainbycall.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.lingdianksw.com/0/405/'
    main(url)
'''
#'https://www.lingdianksw8.com/0/368/'  size: 1.01 MB   15 seconds
#'https://www.lingdianksw.com/48/48443/'  size: 30.84 MB   42 seconds
#'https://www.lingdianksw.com/0/404/'  size: 14.78 MB   27 seconds
#'https://www.lingdianksw.com/0/405/' size: 3267.95 KB  10 seconds
'''
