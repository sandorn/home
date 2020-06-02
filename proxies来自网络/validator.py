# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:53:32
@LastEditors: Even.Sand
@LastEditTime: 2020-03-24 09:00:46

# check ip
目标:检查代理IP速度,匿名程度以及支持的协议类型.
步骤:检查代理IP速度和匿名程度;

代理IP速度:就是从发送请求到获取响应的时间间隔
匿名程度检查:
对http://httpbin.org/get 或https://httpbin.org/get 发送请求
如果响应的origin 中有'，分割的两个IP就是透明代理IP
如果响应的headers 中包含Proxy-Connection 说明是匿名代理IP,否则就是高匿代理IP检查代理IP协议类型
如果http://httpbin.org/get 发送请求可以成功,说明支持http协议
如果https://httpbin.org/get 发送请求可以成功,说明支持https协议

'''
from xjLib.ahttp import ahttpGet
import telnetlib
from domain import Proxy
from log import logger
from settings import TEST_TIMEOUT
from header import get_requests_headers
import time
import requests
import sys
import json

sys.path.append("..")  # 这一部分就是告诉你你要导入的模块在什么位置（相对于本模块地址）
sys.path.append("../..")


def check_proxy(proxy):
    def test_ip(ip, port):
        try:
            telnetlib.Telnet(ip, port, timeout=10)
            print(f"{ip}:{port}代理ip有效！")
            return True
        except BaseException:
            print(f"{ip}:{port}代理ip无效！")
            return False

    if not test_ip(proxy.ip, proxy.port):
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
        return proxy

    proxies = {  # 分别对着一个代理ip，进行http尝试和https尝试
        'http': f'http://{proxy.ip}:{proxy.port}',
        'https': f'https://{proxy.ip}:{proxy.port}',
    }
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)
    # 0->http,1->https,2->http and https
    if http and https:  # 按之前的逻辑进行判断
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed

    print('httpbin_validator 59:', proxy.__dict__)
    return proxy


def __check_http_proxies(proxies, is_http=True):  # 检查代理可用不
    nick_type = -1
    speed = -1
    start = time.time()  # 这个是记录当前时间
    try:  # 加上try，防止requests没访问到程序直接中断
        if is_http:
            # 'http://icanhazip.com'
            # 'https://ip.cn'
            # 'http://httpbin.org/get'
            test_url = 'http://httpbin.org/get'
            response = ahttpGet(test_url, headers=get_requests_headers(), proxy=proxies['http'], timeout=TEST_TIMEOUT)
        else:
            test_url = 'https://httpbin.org/get'
            response = ahttpGet(test_url, headers=get_requests_headers(), proxy=proxies['https'], timeout=TEST_TIMEOUT)

        if (response is not None)and (response.status == 200):
            speed = round(time.time() - start)
            print('#' * 20, response.headers)
            origin = dic['origin']
            proxy_connection = dic['headers'].get('Proxy-Connection', None)
            # 这里用get的原因是，如果获取不到内容可以赋值为None，而不会报错
            if ',' in origin:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0
            return True, nick_type, speed
        else:
            return False, nick_type, speed
    except Exception as err:
        logger.exception(err)
        return False, nick_type, speed


if __name__ == '__main__':  # 程序测试
    proxy = Proxy('111.222.141.127', port='8118')
    print(check_proxy(proxy))
