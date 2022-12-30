# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2022-12-29 12:54:53
FilePath     : /项目包/线程小成果/自定义库futures-.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, get_contents, 结果处理
from xt_Thread import ProcessPool, ThreadPool


def multpool_ahttp_All(url):
    bookname, urls, _ = get_biqugse_download_url(url)
    resps = ahttpGetAll(urls)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(f'{files}&{bookname}ahttp_All.txt', text_list, br='\n')


def multpool(urls):
    mypool = ProcessPool()
    mypool.add_map(multpool_ahttp_All, urls)
    mypool.wait_completed()


def thrtpool(url):
    mypool = ThreadPool()
    bookname, urls, _ = get_biqugse_download_url(url)
    args = [[index, url] for index, url in enumerate(urls)]
    mypool.add_sub(get_contents, args)
    text_list = mypool.wait_sub_completed()
    # text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&Thrtpool.txt', text_list, br='\n')


if __name__ == '__main__':
    url = 'http://www.biqugse.com/96703/'
    # multpool_ahttp_All(url)

    urls = [
        'http://www.biqugse.com/96703/',
        'http://www.biqugse.com/96717/',
        # 'http://www.biqugse.com/2367/',
        # 'http://www.biqugse.com/2367/',
    ]
    multpool(urls)
    # thrtpool(url)
