# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-01-13 22:37:59
FilePath     : /CODE/py学习/线程协程/multiprocessing.Pool.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
from multiprocessing import Pool

from xt_File import savefile
from xt_Ls_Bqg import ahttp_get_contents, get_biqugse_download_url
from xt_Time import fn_timer


@fn_timer
def main_Pool(target):
    texts_list = []
    bookname, urls, _ = get_biqugse_download_url(target)

    print(f'multiprocessing.pool,开始下载:《{bookname}》', flush=True)
    mypool = Pool(32)  # !进程数,不能超过61
    mypool.map_async(func=ahttp_get_contents, iterable=[(index, urls[index]) for index in range(len(urls))], callback=lambda res: texts_list.append(res))
    # mypool.apply_async(func=ahttp_get_contents,callback=_callback_func)
    mypool.close()  # 关闭进程池,不再接受请求
    mypool.join()  # 等待进程池中的事件执行完毕，回收进程池

    texts_list.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}multiprocessing.txt', texts_list, br='\n')


if __name__ == '__main__':
    main_Pool('http://www.biqugse.com/96703/')
    # 38_38836     34.84 seconds
    # 2_2714      215.40 seconds
