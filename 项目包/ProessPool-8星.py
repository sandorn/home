# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-03 12:52:03
LastEditTime : 2025-05-16 11:28:25
FilePath     : /CODE/项目包/ProessPool-8星.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os

# from concurrent.futures import ProcessPoolExecutor as PExecutor
# ProcessPoolExecutor 丢包, 但是速度快
# ThreadPoolExecutor 不丢包, 但是速度慢
from concurrent.futures import ThreadPoolExecutor as PExecutor
from multiprocessing import Pool as ProcPool

from xt_bqg import get_contents, get_download_url
from xt_file import savefile
from xt_thread import Do_CustomProcess
from xt_time import fn_timer


def new_get_contents(args):
    return get_contents(*args)


@fn_timer
def cmpro(bookname, urls):
    res_list = Do_CustomProcess(
        new_get_contents, [(i, url) for i, url in enumerate(urls, 1)]
    )
    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.splitext(os.path.basename(__file__))[0]
    savefile(f"{files}&{bookname}&cmpro.txt", res_list, br="\n")


@fn_timer
def MPpool(bookname, urls):
    with ProcPool(60) as propool:
        res_list = propool.map(new_get_contents, enumerate(urls, 1))
        # task_list = [
        #     propool.apply_async(get_contents, args=(index, url))
        #     for index, url in enumerate(urls, 1)
        # ]
        # res_list = [res.get() for res in task_list]

    res_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f"{files}&{bookname}&MPpool.txt", res_list, br="\n")


@fn_timer
def PPoolExecutor(bookname, urls):
    with PExecutor(60) as executor:
        task_list = [
            executor.submit(get_contents, i, url) for i, url in enumerate(urls, 1)
        ]
        res_list = [task.result() for task in task_list]

    res_list.sort(key=lambda x: x[0])
    files = os.path.splitext(os.path.basename(__file__))[0]

    savefile(f"{files}&{bookname}&PPoolExecutor.txt", res_list, br="\n")


# 必须在模块顶层定义目标函数
def process_data(a, b, coefficient=1):
    return (a * b) * coefficient


if __name__ == "__main__":
    url = "https://www.bigee.cc/book/6909/"
    bookname, urls, _ = get_download_url(url)
    # cmpro(bookname, urls[0:10])  # |<perf_counter: s>
    # MPpool(bookname, urls[0:10])  # |<perf_counter: 55.4s>
    # PPoolExecutor(bookname, urls)  # |<perf_counter: 76s>

    def test():
        list_a = [i for i in range(100)]
        list_b = [i for i in range(100)]

        # 正确调用方式
        results = Do_CustomProcess(
            process_data,  # 目标函数
            list_a,  # 参数列表1
            list_b,  # 参数列表2
            coefficient=1,  # 函数参数
        )

        print(f"处理完成，共得到 {len(results)} 个结果")
        print("示例结果：", results)

    test()
