# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
FilePath     : /线程协程/笔趣阁-自定义库CustomThread优化.py
LastEditTime : 2022-04-13 11:18:12
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_File import savefile
from xt_Thread import CustomThread
from xt_Ls_Bqg import get_download_url, get_contents


def main(bookname, args):
    _ = [CustomThread(get_contents, index, url) for index, url in enumerate(urls)]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    texts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


if __name__ == "__main__":
    from xt_Log import log
    mylog = log()
    bookname, urls = get_download_url('http://www.biqukan.com/2_2760/')
    # # 38_38836  #2_2714  2_2760

    main(bookname, urls)
