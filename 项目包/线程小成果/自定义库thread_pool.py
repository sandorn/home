# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-06-21 13:21:48
FilePath     : /CODE/项目包/线程小成果/自定义库thread_pool.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_File import savefile
from xt_Ls_Bqg import clean_Content, get_download_url
from xt_Requests import get as get
from xt_Response import htmlResponse
from xt_String import Str_Replace
from xt_Thread import thread_pool
from xt_Time import fn_timer

pool = thread_pool(200)


@pool
def get_contents(index, target):
    resp = get(target)

    assert isinstance(resp, htmlResponse)
    _title = resp.pyquery('h1').text()
    _showtext = resp.pyquery('#chaptercontent').text()

    title = Str_Replace(''.join(_title), [('\u3000', ' '), ('\xa0', ' '), ('\u00a0', ' ')])
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def main(target):
    bookname, urls, _ = get_download_url(target)
    for index, url in enumerate(urls):
        get_contents(index, url)
    text_list = pool.wait_completed()
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}&thread_pool.txt', text_list, br='\n')


if __name__ == '__main__':
    main('https://www.bigee.cc/book/6909/')  # |time: 76.25 sec|processtime: 45.08 sec
