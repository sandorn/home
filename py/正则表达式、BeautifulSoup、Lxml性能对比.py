# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion:
九. 正则表达式、BeautifulSoup、Lxml性能对比 - 实例 - 简书
https://www.jianshu.com/p/d0541ecfa5b4
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-10 13:13:55
@LastEditTime: 2019-05-10 13:32:04
'''
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import time


##正则表达式
def re_info(r):
    ids = re.findall("<h2>(.*?)</h2>", r.text, re.S)
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', r.text,
                          re.S)
    #print('re_info:', ids, contents)
    return [ids, contents]


##BeautifulSoup
def bs4_info(r):
    soup = BeautifulSoup(r.text, "lxml")
    infos = soup.select("div.article")
    for info in infos:
        id = info.select("h2")[0].text.strip()
        content = info.select("div.content")[0].text.strip()
        #print('bs4_info:', id, content)
        return [id, content]


#lxml
def lxml_info(r):
    html = etree.HTML(r.text)
    infos = html.xpath(
        '//div[starts-with(@class,"article block untagged mb15")]')
    for info in infos:
        id = info.xpath('div[1]//h2/text()')[0]
        content = info.xpath('a[1]/div/span/text()')[0].strip()
        #print('lxml_info:', id, content)
        return [id, content]


if __name__ == "__main__":
    url_list = [
        "https://www.qiushibaike.com/text/page/{}/".format(i)
        for i in range(1, 14)
    ]
    hds = {
        'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3294.6 Safari/537.36'
    }
    for name, get_info in [('re', re_info), ('bs4', bs4_info),
                           ('lxml', lxml_info)]:
        start = time.time()
        for url in url_list:
            r = requests.get(url, headers=hds)
            get_info(r)
        stop = time.time()
        print(name, stop - start, flush=True)
