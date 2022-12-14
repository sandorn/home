'''
@Descripttion:
进程池和multiprocess.Pool模块 - 笨笨侠 - 博客园
https://www.cnblogs.com/huangjm263/p/8418200.html
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-12 14:38:19
@LastEditors: Even.Sand
@LastEditTime: 2019-05-12 14:46:55
'''
import os
import time
import random
from multiprocess import Pool
from multiprocess import Process


def func(i):
    i += 1


if __name__ == '__main__':
    p = Pool(5)  # 创建了5个进程
    start = time.time()
    p.map(func, range(100))
    p.close()  # 是不允许再向进程池中添加任务
    p.join()
    print(time.time() - start)  # 0.35544490814208984
    start = time.time()
    l = []
    for i in range(100):
        p = Process(target=func, args=(i,))  # 创建了一百个进程
        p.start()
        l.append(p)
    [i.join() for i in l]
    print(time.time() - start)  #  101.00088691711426
