# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
FilePath     : /项目包/线程小成果/笔趣阁-ahttp异步--7星.py
LastEditTime : 2022-11-12 16:34:53
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Time import fn_timer
from xt_String import Str_Replace
from xt_Ls_Bqg import get_download_url, clean_Content, 结果处理
from xt_Thread import P_Map  ##, P_Sub
# T_Map, T_Sub, T_Pool, P_Map, P_Sub, P_Pool

texts = []


def callback_func(resp):
    if resp is None:
        return

    index = resp.index
    response = resp.element

    _name = "".join(response.xpath('//h1/text()'))
    name = Str_Replace(_name, [(' ', ' '), ('\xa0', ' ')])
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = clean_Content(_showtext)
    texts.append([index, name, content])


@fn_timer
def main(url):
    bookname, urls, _ = get_download_url(url)
    resps = ahttpGetAll(urls)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'main.txt', text_list, br='\n')


@fn_timer
def mainbycall(url):
    bookname, urls, _ = get_download_url(url)
    ahttpGetAll(urls, callback=callback_func)
    texts.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'mainbycall.txt', texts, br='\n')


@fn_timer
def multpool(urls):
    mypool = P_Map(main, urls)
    mypool.wait_completed()


@fn_timer
def multpoolback(urls):
    # !可能结果串进程
    mypool = P_Map(mainbycall, urls, MaxSem=7)
    mypool.wait_completed()


if __name__ == '__main__':
    url = 'https://www.biqukan8.cc/38_38163/'
    main(url)
    # mainbycall(url)

    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/2_2760/',
        'https://www.biqukan.com/2_2714/',
        'https://www.biqukan.com/73_73450/',
        'https://www.biqukan.com/76_76015/',
        'https://www.biqukan.com/75_75766/',
        'https://www.biqukan.com/46_46394/',
        'https://www.biqukan.com/61_61396/',
    ]
    # multpool(urls)
    # multpoolback(urls)

    # main                      mainbycall
    # '38_38836'    #@  2.97秒           4秒
    # '2_2760'      #@  4.23秒           8秒
    # "2_2714"      #@  19秒         25秒
    # multpool(urls)  #@  41.33秒
    # multpoolback(urls)  #@  35秒
