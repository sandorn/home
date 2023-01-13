# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 14:20:36
FilePath     : /项目包/线程小成果/笔趣阁-gevent.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

import gevent
from gevent import monkey, pool, spawn
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, get_contents
from xt_Time import timeit


@timeit
def main(target):
    bookname, urls, _ = get_biqugse_download_url(target)
    gpool = pool.Pool()
    task_list = [spawn(get_contents, index, url) for index, url in enumerate(urls)]
    gpool.join()  # join等待线程执行结束
    # gevent.joinall(task_list)

    texts = [task.get() for task in task_list]
    print(f'gevent,书籍《{bookname}》完成下载', flush=True)
    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}gevent.txt', texts, br='\n')


if __name__ == '__main__':
    monkey.patch_socket()
    # main('http://www.biqugse.com/96703/') # 4.56秒
    main('http://www.biqugse.com/28542/')  # 146秒
    # http://www.biqugse.com/75197/
