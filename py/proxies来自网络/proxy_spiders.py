# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:46:53
@LastEditors: Even.Sand
@LastEditTime: 2020-03-24 13:30:49

目标: 实现可以指定不同URL列表,分组的XPATH和详情的XPATH,从不同页面上提取代理的IP,端口号和区域的通用爬虫;
步骤:
1.定义一个BaseSpider类, 继承object
2.提供三个类成员变量:
    urls:代理IP网址的URL的列表
    group_ xpath:分组XPATH,获取包含代理IP信息标签列表的XPATH
    detail. xpath:组内XPATH,获取代理IP详情的信息XPATH,格式为: {'ip':'xx', 'pot':'xx','area':'xx'}
3.提供初始方法，传入爬虫URL列表,分组XPATH,详情(组内)XPATH4.对外提供-个获取代理IP的方法，遍历URL列表,获取URL
    根据发送请求,获取页面数据
    解析页面,提取数据,封装为Proxy对象
    返回Proxy对象列表
'''


import sys

from domain import Proxy
from header import get_requests_headers
from xjLib.ahttp import ahttpGet

sys.path.append("..")  # 提供要导入的模块路径，之前博客讲过怎么使用
sys.path.append("../..")


class BaseSpider(object):  # 定义一个最基础的爬虫，后面爬取专门网站的爬虫继承这个基础爬虫
    urls = []
    group_xpath = ''  # 因为我们用的lxml模块解析页面，所以要传入分组xpath和细节xpath
    detail_xpath = {}  # 这个细节xpath就是ip在页面的位置，端口在页面的位置等等

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls: self.urls = urls
        if group_xpath: self.group_xpath = group_xpath
        if detail_xpath: self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        return ahttpGet(url, headers=get_requests_headers())

    def get_first_list(self, li=[]):
        if len(li) != 0:
            return li[0]
        else:
            return ''

    def get_proxies_from_page(self, page):
        element = page.html
        trs = element.xpath(self.group_xpath)
        # print(trs)
        for tr in trs:
            # tr.xpath(self.detail_xpath['ip'])因为这一部分返回的是一个列表，而且如果我们直接写
            # tr.xpath(self.detail_xpath['ip'])[0],如果这个列表为空，他就会报错导致程序异常终止
            ip = self.get_first_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            # print(proxy.__dict__)  # 这个dict函数就是把对象转化成字典类型输出，python内部函数
            yield proxy  # 函数有了这个关键字，函数就是一个生成器函数。

    def get_proxies(self):
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxy = self.get_proxies_from_page(page)
            yield from proxy


class XiciSpider(BaseSpider):
    urls = {'https://www.xicidaili.com/nn/{}'.format(i) for i in range(1, 4)}
    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()'
    }


class ProxylistplusSpider(BaseSpider):
    urls = {'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 4)}
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>5]'
    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()'
    }


class KuaidailiSpider(BaseSpider):
    urls = {'https://www.kuaidaili.com/free/inha/{}'.format(i) for i in range(1, 4)}
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()'

    }


class ip66Spider(BaseSpider):
    urls = {'http://www.66ip.cn/{}.html'.format(i) for i in range(1, 4)}
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }


if __name__ == '__main__':
    pass
    spider = XiciSpider()
    #spider = ProxylistplusSpider()
    #spider = KuaidailiSpider()
    #pider = ip66Spider()
    for proxy in spider.get_proxies():
        print(proxy)
