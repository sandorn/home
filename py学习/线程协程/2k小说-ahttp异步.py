# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-10-27 15:54:47
FilePath     : /CODE/py学习/线程协程/2k小说-ahttp异步.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
import time

from xt_Ahttp import ahttpGet, ahttpGetAll
from xt_File import savefile
from xt_String import Str_Clean, Str_Replace
from xt_Time import get_time


def get_download_url(target):
    urls = []  # 存放章节链接
    response = ahttpGet(target).html

    _bookname = response.xpath('//h1/text()')[0]
    全部章节节点 = response.xpath('//html/body/dl/dt[2]/following-sibling::dd/a/@href')

    urls.extend(target + item for item in 全部章节节点)
    return _bookname, urls


texts = []


def callback(resp):
    if resp is None:
        return

    index = resp.index
    response = resp.html

    _name = "".join(response.xpath('//h2/text()'))
    _showtext = "".join(response.xpath('//*[@class="Text"]/text()'))

    name = Str_Replace(_name, [[' ', ' '], ['\xa0', ' ']])
    text = Str_Clean(
        _showtext.strip("\n\r　  \xa0"),
        [
            '    ',
            '\xa0',
            '\u3000',
            '2k小说阅读网',
        ],
    )

    texts.append([index, name, f'    {text}'])


def main(url):
    print(f'开始下载：《{url}》\t{get_time()}\t获取下载链接......', flush=True)
    bookname, urls = get_download_url(url)

    print(f'AHTTP,开始下载：《{bookname}》', flush=True)
    ahttpGetAll(urls, pool=500, timeout=60, callback=callback)
    print(f'AHTTP，书籍《{bookname}》完成下载')

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}＆{bookname}.txt', aftertexts, br='\n')
    print(f'{get_time()} 结束，\t用时:{round(time.time() - _stime, 2)} 秒。')


if __name__ == '__main__':
    url = 'https://www.fpzw.com/xiaoshuo/76/76783/'
    _stime = time.time()
    main(url)
