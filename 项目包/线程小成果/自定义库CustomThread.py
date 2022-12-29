# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2022-12-29 13:34:03
FilePath     : /项目包/线程小成果/自定义库CustomThread.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, get_contents
from xt_Thread.Custom import CustomThread
from xt_Time import fn_timer


@fn_timer
def main_thread(target):
    bookname, urls, _ = get_biqugse_download_url(target)
    print(f'CustomThread,开始下载:《{bookname}》', flush=True)
    _ = [CustomThread(get_contents, index, urls[index]) for index in range(len(urls))]
    text_list = CustomThread.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&CustomThread.txt', text_list, br='\n')


if __name__ == '__main__':
    main_thread('http://www.biqugse.com/96703/')
    # '38_38836'    7秒
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, #!72秒。无线程限制
