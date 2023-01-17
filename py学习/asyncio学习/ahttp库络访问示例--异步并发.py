# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-17 00:51:54
FilePath     : /CODE/py学习/asyncio学习/ahttp库络访问示例--异步并发.py
Github       : https://github.com/sandorn/home
==============================================================
https://blog.csdn.net/getcomputerstyle/article/details/103014896
python ahttp:简单、高效、异步requests请求模块
'''
import os

import ahttp
from xt_File import savefile
from xt_Ls_Bqg import clean_Content, get_biqugse_download_url
from xt_String import Str_Replace

sess = ahttp.Session()

bookname, urls, _ = get_biqugse_download_url('http://www.biqugse.com/96703/')
tasks = [sess.get(url) for url in urls]

resps = ahttp.run(tasks, order=True)  # 参数order=True顺序返回

text_list = []
_xpath = ('//h1/text()', '//*[@id="content"]/text()')
for index, item in enumerate(resps):
    _title = item.dom.xpath('//h1/text()')
    _showtext = item.dom.xpath('//*[@id="content"]/text()')
    title = Str_Replace("".join(_title), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
    content = clean_Content(_showtext)
    text_list.append([index, title, content])

files = os.path.split(__file__)[-1].split(".")[0]
savefile(f'{files}&{bookname}&ahttp.txt', text_list, br='\n')
# 38s
