# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 使用multiprocess.pool多进程
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
#LastEditors  : Please set LastEditors
@Date: 2019-05-08 18:31:14
#LastEditTime : 2020-04-28 18:36:57
#!子进程没有执行完毕
'''

from xjLib.req import parse_get
from multiprocess import Pool, Queue
from xjLib.mystr import (Ex_Re_Sub, Ex_Replace, savefile)
import os


class downloader(object):

    def __init__(self, target):
        self.server = 'http://www.biqukan.com/'
        self.target = target
        self.urls = Queue()  # 存放章节链接
        self.bookname = ''  # 书名
        self.texts = []  # 将爬下来的小说都存在里面，做最后排序

    def get_download_url(self):
        response = parse_get(self.target).html
        self.bookname = response.xpath(
            '//meta[@property="og:title"]//@content')[0]
        全部章节节点 = response.xpath(
            '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

        for item in 全部章节节点:
            _ZJHERF = 'https://www.biqukan.com' + item
            self.urls.put(_ZJHERF)

    def get_contents(self, index, target):
        response = parse_get(target).html
        print(2222, index, target)

        _name = "".join(response.xpath('//h1/text()'))
        _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
        name = Ex_Re_Sub(_name, {' ': ' '})
        text = Ex_Replace(
            _showtext.strip("\n\r　  "),
            {
                '　　': '\n',
                ' ': ' ',
                '\', \'': '',
                # '\xa0': '',  # 表示空格  &nbsp;  dictionary key '\xa0' repeated with different values
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
        print(index, name)
        self.texts.append([index, name, '    ' + text])


def down(self):
    self.get_download_url()
    print('开始下载：《' + self.bookname + '》', flush=True)
    mypool = Pool(20)
    for index in range(self.urls.qsize()):
        target = self.urls.get()
        mypool.apply_async(self.get_contents, args=(index, target))
    mypool.close()
    mypool.join()

    self.texts.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + self.bookname + 'main.txt', self.texts, br='\n')


if __name__ == '__main__':
    myclient = downloader('https://www.biqukan.com/2_2714/')
    down(myclient)

    # '38_38836/'  #用时: 10秒
    # '65_65593/'  #用时: 10秒
    # "2_2714"   #《武炼巅峰》664万字 用时: 77秒。
