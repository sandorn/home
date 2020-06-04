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
#LastEditTime : 2020-06-03 11:36:51
变更requests为ahttp
'''
import os

from xt_Ahttp import ahttpGetAll
from xt_String import Ex_Re_Sub, savefile, Ex_Str_Replace, fn_timer
from xt_Ls import get_download_url, arrangeContent


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
    resps = ahttpGetAll(urls, pool=200)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    aftertexts = [[row[i] for i in range(1, 3)] for row in text_list]
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'main.txt', aftertexts, br='\n')


@fn_timer
def mainbycall(url):
    bookname, urls = get_download_url(url)

    texts.sort(key=lambda x: x[0])  # #排序
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'mainbycall.txt', aftertexts, br='\n')


def multpool(urls):
    from multiprocessing import Pool

    p = Pool(10)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
    _ = [p.apply_async(main, args=(url,)) for url in urls]

    p.close()
    p.join()


if __name__ == '__main__':

    from xt_Log import MyLog

    mylog = MyLog()
    # print = mylog.print
    mylog.setlevel('xjLib.ahttp', 30)

    main('https://www.biqukan.com/38_38836/')
    # mainbycall('https://www.biqukan.com/38_38836/')

    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/73_73450/',
        'https://www.biqukan.com/76_76015/',
        'https://www.biqukan.com/75_75766/',
        # 'https://www.biqukan.com/2_2714/',
        'https://www.biqukan.com/61_61396/',
    ]
    # multpool(urls)
    # '38_38836'  #2676KB，#@  6秒
    # "2_2714"    #武炼巅峰，#@  38秒
