# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2019-06-03 10:10:51
#FilePath     : \CODE\py\线程协程\笔趣阁-gevent.py
#LastEditTime : 2020-04-28 15:50:20
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import os

from gevent import monkey, pool, joinall, spawn
from xjLib.mystr import savefile
from xjLib.ls import get_download_url, get_contents


def main(target):
    bookname, urls = get_download_url(target)
    print('gevent，开始下载：《' + bookname + '》', flush=True)
    gpool = pool.Pool(300)
    task_list = [
        spawn(get_contents, None, index, urls[index])
        for index in range(len(urls))
    ]
    gpool.join()  # join等待线程执行结束

    texts = []
    for task in task_list:
        texts.append(task.value)  # task.get()

    print('gevent，书籍《' + bookname + '》完成下载', flush=True)
    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'forin.txt', textssord, br='\n')


if __name__ == '__main__':
    monkey.patch_socket()

    from xjLib.log import log
    mylog = log()

    main('https://www.biqukan.com/38_38836/')

    # '76_76519'  #章节少，测试用 20秒
    # '38_38836'  420.94 秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
