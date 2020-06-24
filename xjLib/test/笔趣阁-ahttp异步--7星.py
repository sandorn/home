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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-24 15:08:29
变更requests为ahttp
'''
import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, arrangeContent


def 结果处理(resps):
    _texts = []

    for resp in resps:
        if resp is None:
            continue
        index = resp.index
        response = resp.element

        _title = "".join(response.xpath('//h1/text()'))
        title = _title.strip('\r\n').replace(u'\u3000',
                                             u' ').replace(u'\xa0', u' ')
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
    title = _title.strip('\r\n').replace(u'\u3000',
                                         u' ').replace(u'\xa0', u' ')
    _showtext = response.xpath('//*[@id="content"]/text()')
    content = arrangeContent(_showtext)
    texts.append([index, title, content])


@fn_timer
def main(url):
    bookname, urls = get_download_url(url)
    resps = ahttpGetAll(urls, pool=200)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'main.txt', text_list, br='\n')


@fn_timer
def mainbycall(url):
    bookname, urls = get_download_url(url)
    resps = ahttpGetAll(urls, pool=200, callback=callback)
    texts.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'mainbycall.txt', texts, br='\n')


@fn_timer
def multpool(urls):
    from multiprocessing import Pool

    p = Pool(10)  # 进程池中创建多个进程,进程执行任务
    _ = [p.apply_async(main, args=(url, )) for url in urls]

    p.close()
    p.join()


if __name__ == '__main__':

    main('https://www.biqukan.com/2_2714/')
    # mainbycall('https://www.biqukan.com/38_38836/')

    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/73_73450/',
        'https://www.biqukan.com/76_76015/',
        'https://www.biqukan.com/75_75766/',
        'https://www.biqukan.com/2_2714/',
        'https://www.biqukan.com/46_46394/',
        'https://www.biqukan.com/61_61396/',
    ]
    # multpool(urls)

    # '38_38836'  #2676KB，#@  6秒
    # "2_2714"    #武炼巅峰，#@  38秒
