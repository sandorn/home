# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2023-02-07 09:13:56
LastEditTime : 2023-02-07 10:16:05
FilePath     : /CODE/py学习/廖雪峰python教程/迭代习题.py
Github       : https://github.com/sandorn/home
==============================================================
'''


def 迭代习题(func=None):

    def findMinAndMax_1(L):
        return (None, None) if L == [] else (min(L), max(L))

    def findMinAndMax(L):
        if L == []: return (None, None)
        __min = __max = L[0]  # 用第一个元素初始化
        for x in L:
            __max = __max if __max > x else x
            __min = __min if __min < x else x
        return __min, __max

    func = func or findMinAndMax

    if func([]) != (None, None):
        print('1测试失败!')
    elif func([7]) != (7, 7):
        print('2测试失败!')
    elif func([7, 1]) != (1, 7):
        print('3测试失败!')
    elif func([7, 1, 3, 9, 5]) != (1, 9):
        print('4测试失败!')
    else:
        print('测试成功!')


def 列表生成式():
    #  列表生成式
    L1 = ['Hello', 'World', 18, 'Apple', None]
    L2 = [s.lower() for s in L1 if isinstance(s, str)]
    print(L2)
    if L2 == ['hello', 'world', 'apple']:
        print('测试通过!')
    else:
        print('测试失败!')


def 斐波拉切数列(max):

    def fib(max):
        n, a, b = 0, 0, 1
        while n < max:
            yield b
            a, b = b, a + b
            n += 1
        return 'done'

    for i in fib(max):
        print(i)


def 生成器():

    def triangles():
        L = [1]
        while True:
            yield L
            L = [1] + [L[i] + L[i + 1] for i in range(len(L) - 1)] + [1]

    n = 0
    results = []
    for t in triangles():
        results.append(t)
        n += 1
        if n == 10: break

    for t in results:
        print(t)

    if results == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1], [1, 7, 21, 35, 35, 21, 7, 1], [1, 8, 28, 56, 70, 56, 28, 8, 1], [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]]:
        print('测试通过!')
    else:
        print('测试失败!')


def 递归(n):
    return 1 if n == 1 else n * 递归(n - 1)


def 尾递归优化(n):
    '''调用函数前，计算函数的参数'''

    def fact_iter(num, product):
        return product if num == 1 else fact_iter(num - 1, num * product)

    return fact_iter(n, 1)


def hanoi(n, x, y, z):
    if n == 1:
        print(x, '-->', z)
    else:
        hanoi(n - 1, x, z, y)  #将前n-1个盘子从x移动到y上
        print(x, '-->', z)  #将最底下的最后一个盘子从x移动到z上
        hanoi(n - 1, y, x, z)  #将y上的n-1个盘子移动到z上


def 递归汉诺塔_L(n):

    def fact(n, aa, bb, cc):

        if n == 1:
            cc.append(aa.pop())
            print(aa, 'a-->c', cc)
        else:
            fact(n - 1, aa, cc, bb)
            cc.append(aa.pop())
            print(aa, 'a-->c', cc)
            fact(n - 1, bb, aa, cc)
        return aa, bb, cc

    aL = list(range(1, n + 1))
    aL.reverse()
    bL, cL = [], []
    print(fact(n, aL, bL, cL))


def 递归汉诺塔_D(n):
    '''N>=3有问题'''

    def fact(n, L):
        # print(n, L)
        if n == 1:
            # print(hnDict)
            hnDict[L[2]].append(hnDict[L[0]].pop())
            print(hnDict[L[0]], f'{L[0]}-->{L[2]}', hnDict[L[2]])
        else:
            fact(n - 1, ['A', 'C', 'B'])
            hnDict[L[2]].append(hnDict[L[0]].pop())
            print(hnDict[L[0]], f'{L[0]}-->{L[2]}', hnDict[L[2]])
            fact(n - 1, ['B', 'A', 'C'])
        return hnDict

    hnDict = {}
    hnDict['A'] = list(range(1, n + 1))[::-1]
    hnDict['B'] = []
    hnDict['C'] = []
    print(fact(n, ['A', 'B', 'C']))


if __name__ == '__main__':
    ...
    # 迭代习题()
    # 列表生成式()
    # reduce 斐波拉切数列
    # from functools import reduce

    # d = map(f, [0, 0, 1, 1, 2])
    # print(d)
    # print(reduce(f, [0, 0, 1, 1, 2]))
    # 斐波拉切数列(9)
    # 生成器()
    # print(递归(5))
    # print(尾递归优化(5))
    # hanoi(3, 'X', 'Y', 'Z')
    # 递归汉诺塔_L(3)
    递归汉诺塔_D(3)
