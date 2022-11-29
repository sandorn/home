# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-26 11:12:51
FilePath     : /py学习/gopup接口爬虫-test.py
LastEditTime : 2022-11-26 11:12:53
Github       : https://github.com/sandorn/home
==============================================================
TOKEN：7def31ce977366fa8aa78212402b7743

有了这个库，这些爬虫都不用亲自写了！
https://mp.weixin.qq.com/s/kw8vlwOJy8axAD2Hvl-SgQ

GoPUP 概况
http://doc.gopup.cn/#/README
'''
import gopup as gp

df_index = gp.realtime_boxoffice()
print(df_index)

df_index = gp.weibo_index(word="疫情", time_type="3month")
# print(df_index)

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 5))
plt.title("微博「疫情」热度走势图")
plt.xlabel("时间")
plt.ylabel("指数")
plt.plot(df_index.index, df_index['疫情'], '-', label="指数")
plt.legend()
plt.grid()
plt.show()
