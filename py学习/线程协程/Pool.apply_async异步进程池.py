# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-13 20:30:56
FilePath     : /py学习/线程协程/Pool.apply_async异步进程池.py
Github       : https://github.com/sandorn/home
==============================================================
进程池和multiprocess.Pool模块 - 笨笨侠 - 博客园
https://www.cnblogs.com/huangjm263/p/8418200.html
'''

import os
from multiprocessing import Pool


def work(n):
    import random
    import time

    print(f'{n} | Parent Pid:{os.getppid()} | Pid: {os.getpid()} ')
    time.sleep(random.randint(0, 6))

    def f(x):
        return x * x

    return f(n)


if __name__ == '__main__':
    p = Pool(8)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
    res_l = []
    for i in range(30):
        res = p.apply_async(work, args=(i, ))  # 异步运行，根据进程池中有的进程数，每次最多3个子进程在异步执行
        # 返回结果之后，将结果放入列表，归还进程，之后再执行新的任务
        # 需要注意的是，进程池中的三个进程不会同时开启或者同时结束
        # 而是执行完一个就释放一个进程，这个进程就去接收新的任务。
        res_l.append(res)
    # 异步apply_async用法：如果使用异步提交的任务，主进程需要使用jion，等待进程池内任务都处理完，然后可以用get收集结果
    # 否则，主进程结束，进程池可能还没来得及执行，也就跟着一起结束了
    p.close()
    p.join()
    # 进程池关闭之后不再接收新的请求
    # 调用 join 之前，先调用 close 函数，否则会出错。
    # 执行完 close 后不会有新的进程加入到 pool,join 函数等待所有子进程结束
    for res in res_l:
        print(res.get())  #使用get来获取apply_aync的结果,如果是apply,则没有get方法,因为apply是同步执行,立刻获取结果,也根本无需get
