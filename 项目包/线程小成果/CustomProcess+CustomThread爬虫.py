# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2024-06-15 19:54:18
FilePath     : /CODE/项目包/线程小成果/CustomProcess+CustomThread爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
from multiprocessing import Pool

from xt_File import savefile
from xt_Ls_Bqg import get_contents, get_download_url
from xt_Thread import CustomThread, Do_CustomProcess
from xt_Time import fn_timer


def get_in_one(target):
    bookname, urls, _ = get_download_url(target)
    # baseurl = '/'.join(target.split('/')[:-2])
    # urls = [baseurl + item for item in temp_urls]  # # 章节链接
    urls = urls[:100]
    _ = [CustomThread(get_contents, index, urls[index]) for index in range(len(urls))]
    text_list = CustomThread.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}&CustomProcess+CustomThread.txt', text_list, br='\n')


if __name__ == '__main__':
    # from memory_profiler import profile
    # from snoop import snoop
    url_list = ['https://www.bigee.cc/book/6909/']

    @fn_timer
    def main():
        for url in url_list:
            Do_CustomProcess(get_in_one, [url])

    main()

    @fn_timer
    def Pool_main():
        p = Pool(60)
        res_l = []
        for url in url_list:
            res = p.apply_async(get_in_one, args=(url,))  # 异步执行任务
            res_l.append(res)

        p.close()
        p.join()
        # res_list = [res.get() for res in res_l]
        # print(res_list)
        # 38s

    # Pool_main()
