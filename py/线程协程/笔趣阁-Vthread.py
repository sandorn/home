# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2019-05-18 03:50:41
#LastEditTime : 2020-04-28 17:50:24
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
# !存在问题，主线程先结束，子线程后结束
# !已修复
#==============================================================
'''

import os
from xjLib.CustomThread import my_pool
# from xjLib.xt_vthread import pool as my_pool
from xjLib.mystr import Ex_Re_Sub, savefile, Ex_Replace
from xjLib.ls import get_download_url
from xjLib.req import parse_get

# text_list = []
pool = my_pool(200)


def baidu():
    response = parse_get('http://www.baidu.com')
    print(response.status)


@pool
def get_contents(index, target):
    response = parse_get(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  \xa0"),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            # '\xa0': '',  # 表示空格  &nbsp;
            '\u3000': '',  # 全角空格
            'www.biqukan.com。': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            '笔趣看;': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '<br />': '',
            '\r\r': '\n',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        },
    )

    # text_list.append([index, name, '    ' + text])
    return [index, name, '    ' + text]


def main(url):
    _name, urls = get_download_url(url)
    _ = [get_contents(i, urls[i]) for i in range(len(urls))]
    text_list = pool.wait_completed()

    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + _name + 'main.txt', text_list, br='\n')


if __name__ == "__main__":

    # '38_38836/'  #用时: 10秒
    # '65_65593/'  #用时: 10秒
    # "2_2714"   #《武炼巅峰》664万字 用时: 77秒。
    urls = [
        'https://www.biqukan.com/38_38836/', 'https://www.biqukan.com/65_65593/'
    ]
    main(urls[0])
