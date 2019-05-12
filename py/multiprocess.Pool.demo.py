# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-12 13:55:08
@LastEditors: Even.Sand
@LastEditTime: 2019-05-12 14:11:41
'''

import multiprocess
#import sys, os, time


def do(n):
    #获取当前线程的名字
    print("worker ", n)
    return


if __name__ == '__main__':
    numList = []
    for i in range(4):
        p = multiprocess.Process(target=do, args=(i,))
        numList.append(p)
        p.start()
        p.join()
        print("Process end.")
'''
---------------------
作者：徐为波
来源：CSDN
原文：https://blog.csdn.net/xwbk12/article/details/77624248
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
