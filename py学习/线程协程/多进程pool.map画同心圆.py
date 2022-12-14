# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
LastEditTime : 2022-12-14 21:13:38
FilePath     : /线程协程/多进程pool.map画同心圆.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import time
import turtle
from multiprocessing import Pool, Process


def cir(n, m):
    turtle.penup()
    turtle.goto(n)
    turtle.pendown()
    turtle.circle(m)
    time.sleep(1)


def runn(lis1, lis2):
    for n, m in zip(lis1, lis2):
        cir(n, m)


def main():
    nn = [(0, -200), (0, -150), (0, -100), (0, -50)]
    mm = [200, 150, 100, 50]
    for i in range(4):
        Process(target=runn, args=(nn, mm)).start()


def cir2(m):
    turtle.penup()
    turtle.goto(m[0])
    turtle.pendown()
    turtle.circle(m[1])
    time.sleep(1)


def main2():
    nn = [(0, -200), (0, -150), (0, -100), (0, -50)]
    mm = [200, 150, 100, 50]
    mn = [(x, y) for x, y in zip(nn, mm)]
    p = Pool(2)
    p.map(cir2, mn)


if __name__ == '__main__':
    main2()
