# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-02-15 21:04:51
FilePath     : /CODE/项目包/线程小成果/自定义库CustomThread.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_File import savefile
from xt_Ls_Bqg import get_download_url, get_contents
from xt_Thread import CustomThread
from xt_Time import fn_timer


@fn_timer
def main_thread(target):
    bookname, urls, _ = get_download_url(target)
    _ = [CustomThread(get_contents, index, urls[index]) for index in range(len(urls))]
    text_list = CustomThread.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&CustomThread.txt', text_list, br='\n')


if __name__ == '__main__':
    main_thread('https://www.biqukan8.cc/0_288/')
    # time: 18.47 sec|processtime: 35.41 sec
