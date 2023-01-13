# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-13 12:55:33
LastEditTime : 2023-01-13 12:55:35
FilePath     : /py学习/爬虫/代理ip池.py
Github       : https://github.com/sandorn/home
==============================================================
'''
# 代理ip
"""
客户端和服务器之间通过网络进行通信。为什么客户端能够正确的找到服务器、服务器也能够
正确的找到客户端，涉及到网络中的IP地址。在同一个网络下IP地址是唯一的。
"""
"""
代理ip等于客户端和目标服务器之间的中间商。
我们通过中间商访问目标服务器，等于我们将需求告诉中间商，中间商根据需求访问目标服务器，
目标服务器的响应结果再一层一层的返回给我们。

代理IP池：包含了N个代理ip。
"""
import json

# 常见的代理IP提供商：极光爬虫代理、芝麻代理、蘑菇代理、西刺代理等。
import requests

# 请求API接口获取代理ip

API_url = 'http://d.jghttp.alicloudecs.com/getip?num=10&type=2&pro=&city=0&yys=0&port=1&time=4&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'}
resp = requests.get(url=API_url, headers=Headers)
print(resp.text)
# 对保存了代理IP的json数据序列化
ip_data_list = json.loads(resp.text)['data']
# for i in ip_data_list:
#     # 需要将代理ip拼接成：ip:port
#     ip_port = f'{i["ip"]}:{i["port"]}'
#     print(ip_port)
print("_________________华丽的分界线________________")
print(ip_data_list)
ip_port_list = [f'{i["ip"]}:{i["port"]}' for i in ip_data_list]
print("_________________华丽的分界线________________")
print(ip_port_list)

# 构造代理ip需要的字典
proxy = {
    # 表示将一个代理ip拼接上它应该走的协议
    'http': f'http://{ip_port_list[0]}',
    'https': f'http://{ip_port_list[0]}'
}
print(proxy)
URL = 'https://movie.douban.com/top250?start=0&filter='
resp = requests.get(url=URL, headers=Headers, proxies=proxy)
if resp.status_code == 200:
    print(resp.text)
else:
    print(resp.status_code)
