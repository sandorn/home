# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-01-13 18:42:56
FilePath     : /项目包/线程小成果/自定义库thread_pool.py
Github       : https://github.com/sandorn/home
==============================================================
'''

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
    _showtext = resp.pyquery('#content').text()

    title = Str_Replace("".join(_title), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
    content = clean_Content(_showtext)
    return [index, title, content]


@fn_timer
def main(target):
    bookname, urls, _ = get_download_url(target)
    for index, url in enumerate(urls):
        get_contents(index, url)
    text_list = pool.wait_completed()
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&thread_pool.txt', text_list, br='\n')


if __name__ == "__main__":

    main('https://www.biqukan8.cc/0_288/')
