# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-08 12:57:15
LastEditTime : 2023-02-10 14:46:45
FilePath     : /CODE/py学习/廖雪峰python教程/filter序列练习.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


def _not_divisible(n):
    return lambda x: x % n > 0


def primes():
    yield 2
    it = _odd_iter()  # 初始序列
    while True:
        n = next(it)  # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it)  # 构造新序列


def run(n):
    # 打印 n 以内的素数:
    for x in primes():
        if x < n:
            print(x)
        else:
            break


def is_palindrome(n):
    return str(n) == str(n)[::-1]


def filter_palindrome():
    # 请利用filter()筛选出回数：
    output = filter(is_palindrome, range(1, 1000))
    print('1~1000:', list(output))
    if list(filter(is_palindrome, range(1, 200))) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33, 44, 55, 66, 77, 88, 99, 101, 111, 121, 131, 141, 151, 161, 171, 181, 191]:
        print('测试成功!')
    else:
        print('测试失败!')


def sort_func():
    # 请用sorted()对上述列表分别按名字排序：
    L = [('Dob', 75), ('Adam', 70), ('Bart', 66), ('Lisa', 88)]

    def by_name(t):
        return t[0]

    L2 = sorted(L, key=by_name)
    print(111, L2)

    # 再按成绩从高到低排序：
    def by_score(t):
        return t[1]

    L2 = sorted(L, key=by_score)
    print(222, L2)

    print(333, sorted(L, key=lambda x: x[1], reverse=True))

    L.sort(key=lambda x: x[0])

    print(444, L)


def createCounter():
    x = 0

    def counter():
        nonlocal x  # nonlocal关键字用来在函数或其他作用域中使用外层(非全局)变量。
        x += 1
        return x

    return counter


def 闭包():
    counterA = createCounter()
    print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
    counterB = createCounter()
    if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
        print('测试通过!')
    else:
        print('测试失败!')


def create_counter(N):
    i = 0

    def counter():
        nonlocal i
        while True:
            i += 1
            if i > N: break
            yield i

    return counter


def 闭包2():
    gc = create_counter(5)()

    # while True:
    #     try:
    #         print(next(gc))
    #     except StopIteration as e:
    #         print('Generator return value:', e.value)
    #         break

    # for i in gc:
    #     print(i)

    print(list(gc))

    # if [next(gc) for _ in range(4)] == [1, 2, 3, 4]:
    #     print('测试通过!')
    # else:
    #     print('测试失败!')


if __name__ == '__main__':
    ...
    import unittest

    from xt_Tools import gpt

    class TestRun(unittest.TestCase):

        def test_run(self):
            self.assertIsNone(闭包2())

    # unittest.main()
    # run(50)
    # filter_palindrome()
    # sort_func()
    # 闭包()
    # 闭包2()
    print(gpt('python迭代习题'))
