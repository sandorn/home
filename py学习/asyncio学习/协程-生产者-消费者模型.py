# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-29 10:18:13
#FilePath     : /asyncio学习/协程-生产者-消费者模型.py
#LastEditTime : 2020-06-29 10:20:58
#Github       : https://github.com/sandorn/home
#==============================================================
协程 - 廖雪峰的官方网站
https://www.liaoxuefeng.com/wiki/1016959663602400/1017968846697824
'''


def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print(f'[消费者] Consuming {n}...')
        r = '200 OK'


def produce(c, max=5):
    c.send(None)  # #启动
    n = 0
    while n < max:
        n = n + 1
        print('[生产者] Producing %s...' % n)
        r = c.send(n)  # #发送指令，并获取返回
        print(f'[生产者] get 消费者 return: {r}')
    c.close()


c = consumer()
produce(c, 8)
