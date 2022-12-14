# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-03 10:25:02
#FilePath     : /py学习/tqdm进度条三方库.py
#LastEditTime : 2020-07-03 10:28:18
#Github       : https://github.com/sandorn/home
#==============================================================
'''
from tqdm import trange, tqdm
from random import random, randint
from time import sleep
with trange(100) as t:
    for i in t:
        # Description will be displayed on the left
        t.set_description('下载速度 %i' % i)
        # Postfix will be displayed on the right,
        # formatted automatically based on argument's datatype
        t.set_postfix(loss=random(),
                      gen=randint(1, 999),
                      str='详细信息',
                      lst=[1, 2])
        sleep(0.01)

for i in tqdm(range(100), ncols=200):
    j = i * i
    sleep(0.01)
