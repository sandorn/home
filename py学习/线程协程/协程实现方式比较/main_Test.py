# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-03-15 22:32:25
FilePath     : /CODE/py学习/线程协程/协程实现方式比较/main_Test.py
Github       : https://github.com/sandorn/home
==============================================================
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:55
LastEditTime : 2022-12-14 14:03:57
FilePath     : /线程协程/协程实现方式比较/main_Test.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import asyncio_Test
import gevent_Test
import matplotlib.pyplot as plt

asyncio_list = []
gevent_list = []

url = 'http://www.python.org'
for i in range(20):
    asyncio_list.append(asyncio_Test.f(i + 1, url))
    gevent_list.append(gevent_Test.f(i + 1, url))

plt.plot(asyncio_list, label='asyncio')
plt.plot(gevent_list, label='gevent')

plt.legend()
plt.savefig('d:/temp/1.png')
plt.show()
