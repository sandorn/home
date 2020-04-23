# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-18 03:50:41
@LastEditors: Even.Sand
@LastEditTime: 2020-04-23 17:00:26

# !存在问题，主线程先结束，子线程后结束，未能取得返回值
# !意思源库join有问题
'''
import os
import vthread
from xjLib.mystr import Ex_Re_Sub, savefile, Ex_Replace
from xjLib.ls import get_download_url
from xjLib.req import parse_get

text_list = []
pool = vthread.pool(20)


@pool
def get_contents(index, target):
    print(index, target)
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
    text_list.append([index, name, '    ' + text])


if __name__ == "__main__":
    _name, urls = get_download_url('https://www.biqukan.com/38_38836/')

    _ = [get_contents(i, urls[i]) for i in range(len(urls))]

    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + _name + 'main.txt', text_list, br='\n')

    # '38_38836/'  #章节少，测试用
    # '65_65593/'  #章节少，测试用
    # "2_2714"   #《武炼巅峰》664万字
    # [武炼巅峰.txt]150W, 用时: 947.34 秒。
