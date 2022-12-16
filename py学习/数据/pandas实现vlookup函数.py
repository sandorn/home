# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-16 18:13:48
LastEditTime : 2022-12-16 18:13:51
FilePath     : /py学习/数据/pandas实现vlookup函数.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import pandas as pd

# 用pandas科学数据库生成二维excel
# 用pandas的merge函数来实现excel中VLOOKUP函数
# 填充空值函数fillna，不会改变原来的数据源
pd1 = pd.DataFrame({"姓名": ["张剑", "李峰", "王帅"], "成绩": [95, 98, 89]})
print(pd1)
# 生成的数据保存在excel中
pd1.to_excel("d:/3-0.xlsx")
print("******************************")
pd2 = pd.DataFrame({"姓名": ["张剑", "李红", "王帅"]})
print(pd2)
pd2.to_excel("d:/3-1.xlsx")
print("********************************")
# 用python实现，VLOOKUP函数的功能
df = pd.merge(pd2, pd1, on="姓名", how="left")
print(df)
df.to_excel("d:/3-3.xlsx")
# 填充空值
tc_df = df.fillna("NULL")
print(tc_df)
tc_df.to_excel("d:/3-4.xlsx")
pd1.to_excel("d:/3-0.xlsx")
print("******************************")
pd2 = pd.DataFrame({"姓名": ["张剑", "李红", "王帅"]})
print(pd2)
pd2.to_excel("d:/3-1.xlsx")
print("********************************")
# 用python实现，VLOOKUP函数的功能
df = pd.merge(pd2, pd1, on="姓名", how="left")
print(df)
df.to_excel("d:/3-3.xlsx")
# 填充空值
tc_df = df.fillna("NULL")
print(tc_df)
tc_df.to_excel("d:/3-4.xlsx")
