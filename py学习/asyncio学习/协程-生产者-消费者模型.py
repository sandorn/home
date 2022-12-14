# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:36:04
LastEditTime : 2022-12-14 23:13:02
FilePath     : /py学习/asyncio学习/协程-生产者-消费者模型.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def consumer():
    r = ''
    while True:
        n = yield r
        if not n: return
        print(f'[消费者] Consuming {n}...')
        r = str(n) + ' | 200 OK'


def produce(c, max=5):
    c.send(None)  # #启动
    n = 0
    # @不能使用forin循环，因为c.send()会阻塞，导致无法执行下一次循环
    while (n := n + 1) < max:
        print('[生产者] Producing %s...' % n)
        r = c.send(n)  # #发送指令，并获取返回
        print(f'[生产者] get 消费者 return: {r}')
    c.close()


c = consumer()
produce(c, 28)
