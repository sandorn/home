# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-01-21 14:01:29
LastEditTime : 2025-01-21 14:10:03
FilePath     : /CODE/项目包/自定义库futures异步-9星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

from xt_file import savefile
from xt_ls_bqg import get_contents, get_download_url
from xt_thread import EnhancedThreadPool
from xt_time import fn_timer


@fn_timer
def myEnhancedThreadPool(book_name, urls_list):
    thread_pool = EnhancedThreadPool(max_workers=200)
    texts = []
    # 提交多个任务
    futures = []
    for i, url in enumerate(urls_list):
        future = thread_pool.submit_task(get_contents, i, url)
        futures.append(future)

    # 等待所有任务完成
    thread_pool.wait_for_completion()

    # 获取结果
    results = thread_pool.get_results()
    for result in results:
        texts.append(result)

    # 关闭线程池
    thread_pool.shutdown()
    texts.sort(key=lambda x: x[0])
    # sorted(texts, key=lambda x: x[0])
    files = os.path.basename(__file__).split(".")[0]
    savefile(f"{files}&{book_name}AioHttpCrawl_pool.txt", texts, br="\n")


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    book_name, urls, _ = get_download_url(url)
    myEnhancedThreadPool(book_name, urls)  # | <Time-Consuming 77.5360s>
