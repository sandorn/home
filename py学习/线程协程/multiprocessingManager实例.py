# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-01-02 13:43:33
LastEditTime : 2023-01-13 21:19:22
FilePath     : /CODE/py学习/线程协程/multiprocessingManager实例.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import multiprocessing


def func(ns, x, y):
    print(f"func 处理前： {ns}")
    x.append(1)
    y.append("a")
    ns.x = x  # 将可变对象也作为参数传入
    ns.y = y
    print(f"func 处理后： {ns}")


def main(ctx):
    manager = ctx.Manager()
    ns = manager.Namespace()  # 命名参数
    ns.x = []  # manager 内部包括可变对象
    ns.y = []

    print(f"main 处理前： {ns}")
    p = ctx.Process(target=func, args=(ns, ns.x, ns.y))
    p.start()
    p.join()
    print(f"main 处理后：{ns}")


if __name__ == '__main__':
    # windows 启动方式
    multiprocessing.set_start_method('spawn')
    # 获取上下文
    ctx = multiprocessing.get_context('spawn')
    main(ctx)
    print()
