# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:51:21
@LastEditors: Even.Sand
@LastEditTime: 2020-03-24 12:06:13
'''

from fake_useragent import UserAgent


def get_requests_headers():  # 这个方法就是随机获取一个请求头
    headers = {  # 除了user-Agent变一下，其他大多都不用变
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip,deflate,sdch',
        # 'Content-Encoding': 'gzip,deflate,compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
        'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
        'Connection': 'close',
    }
    return headers


if __name__ == '__main__':  # 模块检查
    print(get_requests_headers())
