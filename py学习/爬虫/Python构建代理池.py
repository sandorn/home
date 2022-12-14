# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-22 21:23:52
@LastEditors: Even.Sand
@LastEditTime: 2020-03-22 23:14:55
https://blog.csdn.net/qq_1290259791/article/details/80474616
'''

from fake_useragent import UserAgent
import requests
import threading
from pyquery import PyQuery as pq

IP_list = []
Target_url = 'https://ip.cn'     # 验证ip的地址


def getheaders():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers


def findip(type, pagenum):
    """
    :param type: ip类型
    :param pagenum: 页码
    :return:
    """
    list = {
        '1': 'http://www.xicidaili.com/nt/',  # 国内普通代理
        '2': 'http://www.xicidaili.com/nn/',  # 国内高匿代理
        '3': 'http://www.xicidaili.com/wn/',  # 国内https代理
        '4': 'http://www.xicidaili.com/wt/'  # 国外http代理
    }
    url = list[str(type)] + str(pagenum)  # 配置url
    headers = getheaders()
    html = requests.get(url=url, headers=headers, timeout=5).text
    doc = pq(html)
    all = doc('#ip_list tr')
    for i in all.items():
        sumtd = i.find('td').text()
        result = sumtd.split(' ')
        if len(result) > 1:
            get_ip = result[1] + ':' + result[2]
            is_ok = checkip(get_ip)
            if is_ok == True:
                print(get_ip)
                IP_list.append(get_ip)


def getip():  # 获取ip
    threads = []
    for type in range(4):  # 四种ip类型，每种类型取前三页
        for pagenum in range(3):
            t = threading.Thread(target=findip, args=(type + 1, pagenum + 1))
            threads.append(t)
    print('开始爬取代理ip')
    for s in threads:   # 使用多线程爬取
        s.start()
    for e in threads:
        s.join()
    print('爬取完成')


def checkip(ip):    # 检验ip的有效性
    headers = getheaders()  # 获取随机headers
    proxies = {'http': f'http://{ip}', 'https': f'http://{ip}'}  # 代理ip
    try:
        response = requests.get(url=Target_url, proxies=proxies, headers=headers, timeout=1).status_code
        if response == 200:
            return True
        else:
            return False
    except BaseException:
        return False


if __name__ == '__main__':
    getip()
    with open('result.txt', 'w') as f:
        for IP in IP_list:
            f.writelines(IP + '\n')
