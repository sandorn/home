# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
FilePath     : /项目包/线程小成果/笔趣阁-threading-继承-5星.py
LastEditTime : 2022-11-12 15:29:44
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
from xt_File import savefile
from xt_Requests import get_parse
from xt_Thread.Custom import CustomThread
from xt_Ls_Bqg import get_download_url, get_contents
from xt_Time import fn_timer


@fn_timer
def main_thread(target):
    bookname, urls, _ = get_download_url(target)
    print('threading-继承，开始下载：《' + bookname + '》', flush=True)
    # 设置同时执行的线程数，其他等待执行
    _ = [CustomThread(get_contents, (index, urls[index])) for index in range(len(urls))]
    # 获取全部线程结果
    text_list = CustomThread.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + '.txt', text_list, br='\n')


if __name__ == '__main__':
    main_thread('https://www.biqukan8.cc/38_38163/')
    # '38_38836'    7秒
    # "2_2714"   #《武炼巅峰》1724万字,47839kb, #!72秒。无线程限制
