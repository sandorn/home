'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-14 20:42:20
@LastEditors: Even.Sand
@LastEditTime: 2019-05-14 20:51:49
'''
import turtle
import time
from multiprocessing import Process, Pool


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
