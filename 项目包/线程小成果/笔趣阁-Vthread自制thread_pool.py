# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
LastEditTime : 2022-12-21 22:09:42
FilePath     : /项目包/线程小成果/笔趣阁-Vthread自制thread_pool.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from xt_Requests import get as get
from xt_Thread import thread_pool, thread_print

pool = thread_pool(200)


@pool
def get_contents(index, target):
    response = get(target)
    thread_print(f"正在获取第{index}页")
    return index, response


def main():
    for index in range(100):
        get_contents(index, "https://httpbin.org/get")
    text_list = pool.wait_completed()
    for item in text_list:
        print(item)


if __name__ == "__main__":

    main()
