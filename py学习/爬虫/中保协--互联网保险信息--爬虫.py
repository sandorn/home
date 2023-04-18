# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-04-18 17:25:59
FilePath     : /CODE/py学习/爬虫/中保协--互联网保险信息--爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_File import savefile
from xt_Requests import SessionClient
from xt_Thread import ThreadPoolSub

s = SessionClient()
head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Content-Length': 68,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'icid.iachina.cn',
    'Origin': 'http://icid.iachina.cn',
    'Referer': 'http://icid.iachina.cn/?columnid_url=201509301401',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_contents(target=None):
    res = s.get('http://icid.iachina.cn/')
    print(res, res.text)
    res = s.get('http://icid.iachina.cn/?columnid_url=201509301401')
    print(res, res.text)
    res = s.post('http://icid.iachina.cn/front/generalSearch.do', data={'keyword': '%25E6%25B7%25B1%25E5%259C%25B3%25E4%25B8%25AD%25E8%259E%258D'})
    print(res, res.text)
    response = res.element
    all_li = response.xpath('/ul')
    # #main > div.ge > ul > li:nth-child(1)  document.querySelector("#main > div.ge")
    print(all_li)
    for li in all_li:
        class_value = li.xpath('@class')[0]
        text_value = li.xpath('text()')[0]
        print(class_value, text_value)

    # _title = "".join(response.xpath('//h1/text()'))
    # title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
    # _showtext = response.xpath('//*[@id="content"]/text()')
    # return [index, title, content]


get_contents()

# mypool = ThreadPoolSub(
#     get_contents,
#     [[index + 1, url] for index, url in enumerate(urls)],
#     #  callback=_c_func
# )
# texts = mypool.wait_completed()
# texts.sort(key=lambda x: x[0])
# files = os.path.basename(__file__).split(".")[0]
# savefile(files + '?' + bookname + 'ThreadPoolSub.txt', texts, br='\n')
