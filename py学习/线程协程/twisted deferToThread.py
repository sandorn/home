# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-24 00:25:06
LastEditTime : 2023-01-24 21:02:59
FilePath     : /CODE/py学习/twisted deferToThread.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import functools
import threading
import time

from twisted.internet import defer, reactor
from twisted.internet.threads import deferToThread


# 耗时操作 这是一个同步阻塞函数
def mySleep(timeout):
    time.sleep(timeout / 10)
    print(threading.current_thread(), "耗时操作结束了")
    # 返回值相当于加进了callback里
    return 3


def say(result):
    print(threading.current_thread(), "耗时操作结束了, 并把它返回的结果给我了", result)


# 用functools.partial包装一下, 传递参数进去
cb = functools.partial(mySleep, 3)
d = deferToThread(cb)
d.addCallback(say)

print("你还没有结束我就执行了, 哈哈")

# reactor.callWhenRunning(cb)
reactor.run()
