# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-12 09:52:18
@LastEditTime: 2019-05-19 00:00:15
'''
# 下载第七天
# https://www.kanunu8.com
import requests
from bs4 import BeautifulSoup
import threading
import re
import time
t1 = time.time()
# print(t1)
url = "https://www.kanunu8.com/book4/10500/"
dat = requests.get(url)
dat.encoding = "gbk"
data = dat.text
soup = BeautifulSoup(data, "html.parser")
a = []
# print(a)
pool = []  # 方便最后聚合
zz = []  # 将爬下来的小说都存在里面，做最后排序


def task(a, zj):

    r = requests.get("https://www.kanunu8.com/book4/10500/" +
                     i[1]).content.decode(
                         "gbk", errors="ignore")
    so = BeautifulSoup(r, "html.parser")
    b = so.h2.string
    c = so.p.get_text()
    c1 = "\n    ".join(c.split())
    zz.append([zj, c1, b])


for s in soup.select("tbody tr td a"):
    a.append([s.get_text(), s.get("href")])
del a[0]
zj = 1  # 用来排序
for i in a:
    print("开始下载", i[0])
    t = threading.Thread(target=task, args=(i[1], zj))
    pool.append(t)
    t.start()
    zj += 1
for t in pool:
    t.join()
print(time.time() - t1)
print('下载完成')
zz.sort()
with open('1.txt', 'w') as f:
    for i in zz:
        f.write(i[2] + '\n')
        f.write(i[1] + '\n')
'''
---------------------
作者：haha13l4
来源：CSDN
原文：https://blog.csdn.net/haha13l4/article/details/89596635
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
