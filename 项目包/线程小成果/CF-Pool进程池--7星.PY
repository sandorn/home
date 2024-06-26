"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-06-26 15:32:10
FilePath     : /CODE/项目包/线程小成果/CF-Pool进程池--7星.PY
Github       : https://github.com/sandorn/home
==============================================================
python线程池ThreadPoolExecutor与进程池ProcessPoolExecutor - Harvard_Fly - 博客园
https://www.cnblogs.com/FG123/p/9704233.html
"""

import os

# from concurrent.futures import ProcessPoolExecutor as Pool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
from concurrent.futures import as_completed, wait

from xt_File import savefile
from xt_Ls_Bqg import get_contents, get_download_url
from xt_Time import fn_timer

texts = []


def callback_func(future):
    # 回调方式获取线程结果
    index, name, text = future.result()  # 回调函数取得返回值
    texts.append([index, name, text])


@fn_timer
def main_callback(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        _ = [pool.submit(get_contents, index, urls[index]).add_done_callback(callback_func) for index in range(len(urls))]

    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}add_done_callback.txt', texts, br='\n')


@fn_timer
def main_completed(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = [pool.submit(get_contents, index, urls[index]) for index in range(len(urls))]

    texts = [future.result() for future in as_completed(future_tasks)]

    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}main_as_completed.txt', textssord, br='\n')


@fn_timer
def main_wait(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = [pool.submit(get_contents, index, urls[index]) for index in range(len(urls))]
    # texts = []
    # result = wait(future_tasks)
    # done_set = result[0]
    # for future in done_set:
    #     resp = future.result()
    #     texts.append(resp)
    texts = [future.result() for future in wait(future_tasks)[0]]
    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}main_wait.txt', texts, br='\n')


@fn_timer
def main_map(max, bookname, urls):
    indexs = list(range(len(urls)))
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = pool.map(get_contents, indexs, urls)

    texts = list(future_tasks)
    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}main_map.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    bookname, urls, _ = get_download_url(url)
    urls = urls
    # main_map(60, bookname, urls)  # |time: 74.27 sec|processtime: 43.34 sec
    # main_wait(60, bookname, urls)  # |time: 72.38 sec|processtime: 39.00 sec
    main_completed(60, bookname, urls)  # |time: 71.88 sec|processtime: 40.38 sec
    # main_callback(60, bookname, urls)  # |time: 74.23 sec|processtime: 42.19 sec
