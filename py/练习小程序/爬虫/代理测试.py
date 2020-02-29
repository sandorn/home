# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-02-29 18:03:52
@LastEditors: Even.Sand
@LastEditTime: 2020-02-29 18:13:12
'''


import telnetlib
import requests
# 代理IP地址（高匿）

# head 信息
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Connection': 'keep-alive'}
# http://icanhazip.com会返回当前的IP地址


def test_ip(ip, port):
    try:
        telnetlib.Telnet(ip, port, timeout=2)
        print("代理ip有效！")
        return True
    except BaseException:
        print("代理ip无效！")
        return False


proxy = {
    'https': 'https://121.237.149.133:3000',
}

test_ip("121.237.149.133", "3000")

p = requests.get('https://icanhazip.com', headers=head, proxies=proxy)
print(p.text)
