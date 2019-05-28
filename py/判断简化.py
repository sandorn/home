# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-28 16:38:02
@LastEditors: Even.Sand
@LastEditTime: 2019-05-28 17:08:34
'''
a, b, c = 1, 2, 3

if a > b:
    c = a
else:
    c = b
print(c)
d = a if a > b else b
print(d)
aaa = 'abc'
bbb = aaa if aaa == 'abc' else 'cha'
print(bbb)
max_value = (a > b and a or b)  # 等同于a > b ? a : b
#max_value = a if a > b else b
print('max_value:', max_value)
e = [b, a][a > b]
print(e)
f = (a > b and [a] or [b])[0]
print(f)

lista = [12, 3, 4, 6, 7, 13, 21]
newList = [x for x in lista]
print(newList)
newList2 = [x for x in lista if x % 2 == 0]
print(newList2)

x = [1, 2, 3, 4]
y = [5, 6, 7, 8]
z = [a + b for a in x for b in y if a % 2 == 0 and b % 2 == 0]
print(z)
z2 = ['a + b:[{}][{}]'.format(a, b) for a in x for b in y]
print(z2)


mean_domain = '.--'.join(['127', '0', '0', '1'])
print(mean_domain)
