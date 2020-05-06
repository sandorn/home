# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-29 17:54:13
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-01 18:36:32
2种方法简单爬取JS加载的动态数据_Python_Python3 爬虫实战 1:应对特殊字体,爬取猫眼电影实时排行榜-CSDN博客
https://blog.csdn.net/qq523176585/article/details/78693900
'''
# coding=utf-8
import requests
import json
from prettytable import PrettyTable

if __name__ == '__main__':

    url = 'https://data-gkcx.eol.cn/soudaxue/queryProvince.html'

    row = PrettyTable()
    row.field_names = ["地区", "年份", "考生类别", "批次", "分数线"]

    for i in range(1, 34):
        data = {
            "messtype": "json",
            "page": i,
            "size": 50,
            "callback": "jQuery1830426658582613074_1469201131959",
            "_": "1469201133189",
        }
        school_datas = requests.post(url, data=data)  # .json()
        print(school_datas)
        datas = school_datas["school"]
        for data in datas:
            row.add_row((data["province"], data["year"], data["bath"],
                         data["type"], data["score"]))

    print(row)
