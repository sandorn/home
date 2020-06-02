# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-16 22:58:44
@LastEditors: Even.Sand
@LastEditTime: 2020-03-16 23:00:02
'''
import random
from tenacity import retry


def verify_url(url):
    import requests

    try:
        requests.get(url, timeout=10)
        return True
    except requests.exceptions.ConnectTimeout:
        return False


def main():
    for _ in range(5):
        try:
            if verify_url('http://www.baidu.com'):
                return
            else:
                continue
        except KeyError:
            continue


if __name__ == '__main__':
    main()
