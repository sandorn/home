# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-03 10:10:51
@LastEditors: Even.Sand
@LastEditTime: 2020-04-17 22:59:36
'''
import os

from gevent import monkey, pool
from xjLib.mystr import savefile
from xjLib.ls import get_download_url, get_contents

monkey.patch_socket()


def main(target):
    bookname, urls = get_download_url(target)
    print('gevent，开始下载：《' + bookname + '》', flush=True)
    gpool = pool.Pool(100)
    task_list = [
        gpool.spawn(get_contents, None, index, urls[index])
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
    from xjLib.log import log
    mylog = log()

    main('https://www.biqukan.com/38_38836/')

    # '76_76519'  #章节少，测试用 20秒
    # '38_38836'  420.94 秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
