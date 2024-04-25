# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2022-12-29 13:46:12
FilePath     : /项目包/线程小成果/自定义库WorkManager.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_File import savefile
from xt_Ls_Bqg import get_download_url, get_contents
from xt_Thread import WorkManager
from xt_Time import fn_timer


@fn_timer
def manager(url):
    bookname, urls, _ = get_download_url(url)
    WM = WorkManager()
    WM.add_work_queue([[get_contents, index, url] for index, url in enumerate(urls)])
    text_list = WM.wait_completed()
    text_list.sort(key=lambda x: x[0])
    # files = os.path.split(__file__)[-1].split(".")[0]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&WorkManager.txt', text_list, br='\n')


if __name__ == "__main__":
    url = 'https://www.biqukan8.cc/0_288/'
    # main(url)
    manager(url)
