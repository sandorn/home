# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
FilePath     : /项目包/线程小成果/笔趣阁-自定义库CustomThread优化.py
LastEditTime : 2022-11-12 15:20:28
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_File import savefile
from xt_Thread import CustomThread
from xt_Ls_Bqg import get_download_url, get_contents
from xt_Time import fn_timer


@fn_timer
def main(bookname, args):
    _ = [CustomThread(get_contents, (index, url)) for index, url in enumerate(urls)]
    text_list = CustomThread.wait_completed()
    text_list.sort(key=lambda x: x[0])
    #& text_list = [[row[i] for i in range(1, 3)] for row in text_list]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', text_list, br='\n')


if __name__ == "__main__":
    bookname, urls, _ = get_download_url('https://www.biqukan8.cc/38_38163/')
    # # 38_38836  #2_2714  2_2760

    main(bookname, urls)
