# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 只有调试中有作用，run code 不起作用
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-10 12:37:45
@LastEditTime: 2019-05-10 12:39:16
'''

import time
for i in range(10):
    time.sleep(0.2)
    print("\r Loading... ".format(i) + str(i), end="")
