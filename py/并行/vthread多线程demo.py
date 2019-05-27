# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-18 00:04:03
@LastEditors: Even.Sand
@LastEditTime: 2019-05-18 04:38:52

python 多线程函数库 vthread ，简而强大 - Python开发社区 | CTOLib码库
https://java.ctolib.com/cilame-vthread.html
'''
import time
import vthread
help(vthread)
pool_1 = vthread.pool(5, gqueue=1)  # 开5个伺服线程，组名为1
pool_2 = vthread.pool(2, gqueue=2)  # 开2个伺服线程，组名为2


@pool_1
def foolfunc1(num):
    time.sleep(1)
    print(f"foolstring1, foolnumb1:{num}")


@pool_2  # foolfunc2 和 foolfunc3 用gqueue=2的线程池
def foolfunc2(num):
    time.sleep(1)
    print(f"foolstring2, foolnumb2:{num}")


@pool_2  # foolfunc2 和 foolfunc3 用gqueue=2的线程池
def foolfunc3(num):
    time.sleep(1)
    print(f"foolstring3, foolnumb3:{num}")


for i in range(5):
    foolfunc1(i)
for i in range(3):
    foolfunc2(i)
for i in range(2):
    foolfunc3(i)
print(2222222222)
# 额外开启线程池组的话最好不要用gqueue=0
# 因为gqueue=0就是默认参数
