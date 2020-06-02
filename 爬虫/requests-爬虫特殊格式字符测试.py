# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-22 15:00:12
@LastEditors: Even.Sand
@LastEditTime: 2020-02-26 11:38:43
'''


from xjLib.req import parse_get as parse_url
from lxml import etree

# 获取网页源代码


def get_page(url):
    response = parse_url(url=url)
    html = response.content.decode('gbk', "ignore")
    return html


def get_page0(url):
    response = parse_url(url=url)
    response.encoding = 'gbk'
    return response.text


def parse4data(html):
    #html = etree.HTML(html)
    zjname = html.xpath('//*[@id="wrapper"]/div[4]/div[2]/h1/text()')
    print(zjname)
    zjtext = html.xpath('//*[@id="content"]/text()')
    data = [zjname, zjtext]
    return data


if __name__ == '__main__':
    url = 'https://www.biqukan.com/0_790/70727308.html'
    html = get_page(url)
    data = parse4data(html)

    #print('||||||||' + data[0])
