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
@LastEditTime: 2020-03-24 13:34:04
'''
from xjLib.ahttp import ahttpGet


import telnetlib
import requests

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Connection': 'keep-alive'}
# http://icanhazip.com     #返回当前的IP地址
# https://ip.cn/


def test_ip(ip, port):
    try:
        telnetlib.Telnet(ip, port, timeout=10)
        print(f"{ip}:{port}代理ip有效！")
        return True
    except BaseException:
        print(f"{ip}:{port}代理ip无效！")
        return False


ip = "122.55.250.242"
port = "8080"
proxy = {
    'http': f'http://{ip}:{port}',
    'https': f'https://{ip}:{port}',
}


def ceshi():
    p = requests.get('http://icanhazip.com', headers=head, proxies=proxy)
    print(p.text)


async def aaa():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.request('http://python.org', proxy=proxy['http'], verify_ssl=False) as sessReq:
            content = await sessReq.read()
            print(content)


def bbb():
    if test_ip(ip, port):
        p = ahttpGet('http://icanhazip.com', headers=head, proxy=proxy['http'])
        print(p.text)


if __name__ == '__main__':
    aaa()
