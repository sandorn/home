'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-14 20:29:31
@LastEditors: Even.Sand
@LastEditTime: 2019-05-14 20:29:31
'''
from multiprocessing import Process, Manager


def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()


if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    l = manager.list(range(10))

    p = Process(target=f, args=(d, l))
    p.start()
    p.join()

    print(d)
    print(l)
'''
---------------------
作者：DataCareer
来源：CSDN
原文：https://blog.csdn.net/wmsok/article/details/81187149
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
