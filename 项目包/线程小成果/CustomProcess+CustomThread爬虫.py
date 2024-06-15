# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2024-06-16 02:20:02
FilePath     : /CODE/项目包/线程小成果/CustomProcess+CustomThread爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
from multiprocessing import Pool

from xt_File import savefile
from xt_Ls_Bqg import get_contents, get_download_url
from xt_Thread import Do_CustomProcess
from xt_Time import fn_timer


@fn_timer
def Custom(url):
    bookname, urls, titles = Do_CustomProcess(get_download_url, [url])[0]
    res_list = Do_CustomProcess(get_contents, list(range(20)), urls[:20])
    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}&Do_CustomProcess.txt', res_list, br='\n')


@fn_timer
def Poolapply_async(url):
    bookname, urls, titles = Do_CustomProcess(get_download_url, [url])[0]

    p = Pool(32)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
    res_l = []

    for i, url in enumerate(urls[:20]):
        res = p.apply_async(get_contents, args=(i, url))  # 异步执行任务
        res_l.append(res)
    p.close()
    p.join()
    res_list = [res.get() for res in res_l]
    res_list.sort(key=lambda x: x[0])  # #排序
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}&Poolapply_async.txt', res_list, br='\n')


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    # Custom(url)
    Poolapply_async(url)
