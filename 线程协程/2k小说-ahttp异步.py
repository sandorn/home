# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
FilePath     : /线程协程/2k小说-ahttp异步.py
LastEditTime : 2022-10-22 16:01:48
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
import time
from xt_Ahttp import ahttpGet, ahttpGetAll
from xt_String import Ex_Re_Sub, Ex_Re_Repl
from xt_Time import get_time
from xt_File import savefile


def get_download_url(target):
    urls = []  # 存放章节链接
    response = ahttpGet(target).html

    _bookname = response.xpath('//h1/text()')[0]
    全部章节节点 = response.xpath('//html/body/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = target + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []


def callback(resp):
    if resp is None:
        return

    index = resp.index
    response = resp.html

    _name = "".join(response.xpath('//h2/text()'))
    _showtext = "".join(response.xpath('//*[@class="Text"]/text()'))

    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Re_Repl(
        _showtext.strip("\n\r　  \xa0"),
        {
            '    ': '\n',
            '\xa0': ' ',  # 表示空格  &nbsp;
            '\u3000': ' ',  # 全角空格
            '2k小说阅读网': ' ',  # 全角空格
        },
    )

    texts.append([index, name, '    ' + text])


def main(url):
    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_time()), flush=True)
    bookname, urls = get_download_url(url)

    print('AHTTP,开始下载：《' + bookname + '》', flush=True)
    ahttpGetAll(urls, pool=500, timeout=60, callback=callback)
    print('AHTTP，书籍《' + bookname + '》完成下载')

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + '.txt', aftertexts, br='\n')
    print('{} 结束，\t用时:{} 秒。'.format(get_time(), round(time.time() - _stime, 2)))


if __name__ == '__main__':
    url = 'https://www.fpzw.com/xiaoshuo/76/76783/'
    _stime = time.time()
    main(url)
