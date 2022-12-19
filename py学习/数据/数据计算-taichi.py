# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-19 14:26:15
LastEditTime : 2022-12-19 14:26:17
FilePath     : /py学习/数据/数据计算.py
Github       : https://github.com/sandorn/home
==============================================================
Count the number of primes in range [1, n].
Count the number of primes below a given bound.
'''
import taichi as ti
from xt_Time import fn_timer

ti.init()


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


if __name__ == "__main__":
    main(1000000)
    main(10000000)
