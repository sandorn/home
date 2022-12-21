# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-20 23:29:50
LastEditTime : 2022-12-21 12:43:21
FilePath     : /py学习/爬虫/网页编码--2.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import chardet  # 字符集检测
from xt_Ahttp import ahttpGet
from xt_Requests import get


def automatic_detect(url):
    html = get(url)

    print(html)
    print(html.dom.xpath('//title/text()'))
    print(html.html.xpath('//title/text()'))
    print(html.element.xpath('//title/text()'))
    print(html.text)

    result = chardet.detect(html._content)
    encoding = result['encoding']
    _tent = html._content.decode(encoding, 'ignore')

    return encoding, _tent


def main():

    urls = ['http://www.baidu.com', 'http://www.163.com', 'http://dangdang.com', 'https://www.biqukan8.cc/38_38163/']
    for url in urls:
        end, _tent = automatic_detect(url)
        print(url, end)
        # print(_tent)


def main2():
    urls = ['http://www.baidu.com', 'http://www.163.com', 'http://dangdang.com', 'https://www.biqukan8.cc/38_38163/']
    for url in urls:
        res = ahttpGet(url)
        print(res)
        print(res.dom.xpath('//title/text()'))
        print(res.html.xpath('//title/text()'))
        print(res.element.xpath('//title/text()'))
        print(res.text)


if __name__ == '__main__':
    main()
