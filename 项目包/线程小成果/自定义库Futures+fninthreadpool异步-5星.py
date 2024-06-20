# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-31 08:03:42
LastEditTime : 2024-06-20 17:17:56
FilePath     : /CODE/项目包/线程小成果/自定义库Futures+fninthreadpool异步-5星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_File import savefile
from xt_Ls_Bqg import clean_Content, get_contents, get_download_url
from xt_Requests import get
from xt_Response import htmlResponse
from xt_String import Str_Clean
from xt_Thread import FnInThreadPool, ThreadPool
from xt_Time import fn_timer


def new_get_contents(args):
    index, target = args
    resp = get(target)
    if not isinstance(resp, htmlResponse):
        return [0, resp, '']
    title = resp.pyquery('h1').text()
    content = resp.pyquery('#chaptercontent').text()
    title = ''.join(Str_Clean(''.join(title), ['\u3000', '\xa0', '\u00a0']))
    content = clean_Content(content).strip()
    return [index, title, content]


@fn_timer
def get_ThreadPool(bookname, urls, fn):
    mypool = ThreadPool()
    args = [[i, u] for i, u in enumerate(urls, start=1)]
    mypool.add_tasks(fn, args)
    texts = mypool.wait_completed()
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}get_contents.txt', texts, br='\n')


@fn_timer
def FnInPool(bookname, urls):
    indexes = list(range(len(urls)))
    texts = FnInThreadPool(get_contents, indexes, urls).result
    texts.sort(key=lambda x: x[0])
    files = os.path.basename(__file__).split('.')[0]
    savefile(f'{files}&{bookname}func_ThreadPool.txt', texts, br='\n')


if __name__ == '__main__':
    url_list = ['https://www.bigee.cc/book/6909/']
    bookname, urls, _ = get_download_url(url_list[0])
    get_ThreadPool(bookname, urls, new_get_contents)
    # FnInPool(bookname, urls)
