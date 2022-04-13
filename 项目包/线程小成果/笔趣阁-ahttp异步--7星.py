# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 23:35:58
LastEditors  : Please set LastEditors
LastEditTime : 2021-03-19 11:14:31
变更requests为ahttp
'''
import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, arrangeContent
from xt_Thread import P_Map  ##, P_Sub
# T_Map, T_Sub, T_Pool, P_Map, P_Sub, P_Pool


def 结果处理(resps):
    _texts = []

    for resp in resps:
        if resp is None:
            continue
        index = resp.index
        response = resp.element

        _title = "".join(response.xpath('//h1/text()'))
        title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        _showtext = response.xpath('//*[@id="content"]/text()')
        content = arrangeContent(_showtext)
        _texts.append([index, title, content])

    return _texts


texts = []


def callback(resp):
    if resp is None:
        return

    index = resp.index
    response = resp.element

    _title = "".join(response.xpath('//h1/text()'))
    title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    texts.append([index, title, content])


@fn_timer
def main(url):
    bookname, urls = get_download_url(url)
    resps = ahttpGetAll(urls)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'main.txt', text_list, br='\n')


@fn_timer
def mainbycall(url):
    bookname, urls = get_download_url(url)
    ahttpGetAll(urls, callback=callback)
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
    url = 'https://www.biqukan.com/38_38836/'
    # main(url)
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
