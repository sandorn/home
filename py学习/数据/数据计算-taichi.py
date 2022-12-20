# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-19 14:26:15
LastEditTime : 2022-12-20 20:27:40
FilePath     : /py学习/数据/数据计算-taichi.py
Github       : https://github.com/sandorn/home
==============================================================
Count the number of primes in range [1, n].
Count the number of primes below a given bound.
'''
import taichi as ti
from xt_Time import fn_timer

ti.init()  # arch=ti.gpu, kernel_profiler=True


@ti.func
def is_prime(n: int):
    result = True
    for k in range(2, int(n**0.5) + 1):
        if n % k == 0:
            result = False
            break
    return result


@ti.kernel
def count_primes(n: int) -> int:
    count = 0
    for k in range(2, n):
        if is_prime(k):
            count += 1

    return count


@fn_timer
def main(num):
    print(count_primes(num))


def is_prime2(n: int):
    result = True
    for k in range(2, int(n**0.5) + 1):
        if n % k == 0:
            result = False
            break
    return result


def count_primes2(n: int) -> int:
    count = 0
    for k in range(2, n):
        if is_prime2(k):
            count += 1

    return count


@fn_timer
def main2(num):
    print(count_primes2(num))


if __name__ == "__main__":
    import sys
    print(sys.path)
    main(2000000)
    main2(2000000)
