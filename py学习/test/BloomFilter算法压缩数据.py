# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion:
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-13 11:17:54
@LastEditors: Even.Sand
@LastEditTime: 2019-05-13 11:45:29
'''
# -*- coding: utf-8 -*-
# BloomFilter
from pybloom_live import BloomFilter

f = BloomFilter(capacity=1000, error_rate=0.001)  # capacity是容量, error_rate 是能容忍的误报率,超过误报率，抛出异常
print([f.add(x) for x in range(10)])  # [False, False, False, False, False, False, False, False, False, False]
print(all([(x in f) for x in range(10)]))  # True
print(10 in f)  # False
print(5 in f)  # True


f = BloomFilter(capacity=1000, error_rate=0.001)
print(f.capacity)  # 等于capacity
print('len(f):', len(f))
for i in range(0, f.capacity):
    f.add(i)
print('len(f):', len(f))
print((1.0 - (len(f) / float(f.capacity))) <= f.error_rate + 2e-18)  # True


from pybloom_live import ScalableBloomFilter

sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
count = 10000
for i in range(0, count):
    sbf.add(i)
print((1.0 - (len(sbf) / float(count))) <= sbf.error_rate + 2e-18)  # True
'''
---------------------
作者：周小董
来源：CSDN
原文：https://blog.csdn.net/xc_zhou/article/details/81349231
版权声明：本文为博主原创文章，转载请附上博文链接！
---------------------
作者：tenliu2099
来源：CSDN
原文：https://blog.csdn.net/tenliu2099/article/details/78298778
版权声明：本文为博主原创文章，转载请附上博文链接！'''
