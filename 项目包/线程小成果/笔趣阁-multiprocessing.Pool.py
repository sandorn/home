# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
FilePath     : /项目包/线程小成果/笔趣阁-multiprocessing.Pool.py
LastEditTime : 2022-11-12 17:15:14
Github       : https://github.com/sandorn/home
==============================================================
'''

from multiprocessing import Pool
import os

from xt_File import savefile
from xt_Time import fn_timer
from xt_Ls_Bqg import get_download_url, ahttp_get_contents


@fn_timer
def main_Pool(target):
    texts_list = []
    bookname, urls, _ = get_download_url(target)

    print('multiprocessing.pool,开始下载:《' + bookname + '》', flush=True)
    mypool = Pool(32)  # !进程数,不能超过61
    mypool.map_async(func=ahttp_get_contents, iterable=[(index, urls[index]) for index in range(len(urls))], callback=lambda res: texts_list.append(res))
    # mypool.apply_async(func=ahttp_get_contents,callback=_callback_func)
    mypool.close()  # 关闭进程池,不再接受请求
    mypool.join()  # 等待进程池中的事件执行完毕，回收进程池

    texts_list.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'multiprocessing.txt', texts_list, br='\n')


if __name__ == '__main__':
    main_Pool('https://www.biqukan8.cc/38_38163/')
    # 38_38836     34.84 seconds
    # 2_2714      215.40 seconds
