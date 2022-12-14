# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
LastEditTime : 2022-12-14 18:57:19
FilePath     : /线程协程/笔趣阁-gevent.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from gevent import monkey, pool, spawn
from xt_File import savefile
from xt_Ls_Bqg import get_contents, get_download_url


def main(target):
    bookname, urls, _ = get_download_url(target)
    print('gevent，开始下载：《' + bookname + '》', flush=True)
    gpool = pool.Pool(300)
    task_list = [spawn(get_contents, (index, urls[index])) for index in range(len(urls))]
    gpool.join()  # join等待线程执行结束

    texts = []
    for task in task_list:
        texts.append(task.get())
        # texts.append(task.value)

    print('gevent，书籍《' + bookname + '》完成下载', flush=True)
    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'forin.txt', textssord, br='\n')


if __name__ == '__main__':
    monkey.patch_socket()

    # from xt_Log import mylog

    # mylog = log()

    main('https://www.biqukan8.cc/38_38836/')

    # '76_76519'  #章节少，测试用 20秒
    # '38_38836'  420.94 秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
