# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-03 23:35:58
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-06 15:49:27
变更requests为ahttp
'''
import os

from xjLib.ahttp import ahttpGetAll
from xjLib.mystr import Ex_Re_Sub, savefile, Ex_Replace, fn_timer
from xjLib.ls import get_download_url


def 结果处理(resps):
    text_list = []

    for resp in resps:
        index = resp.index
        response = resp.html

        _name = "".join(response.xpath('//h1/text()'))
        _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

        name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
        text = Ex_Replace(
            _showtext.strip("\n\r　  "),
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

    return text_list


texts = []


def callback(resp):
    if resp is None:
        return

    index = resp.index
    response = resp.html

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
    texts.append([index, name, '    ' + text])


@fn_timer
def main(url):
    bookname, urls = get_download_url(url)
    resps = ahttpGetAll(urls, pool=200)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    aftertexts = [[row[i] for i in range(1, 3)] for row in text_list]
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'main.txt', aftertexts, br='\n')


@fn_timer
def mainbycall(url):
    bookname, urls = get_download_url(url)
    ahttpGetAll(urls, pool=500, callback=callback)

    texts.sort(key=lambda x: x[0])  # #排序
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    # @重新梳理数据，剔除序号
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'mainbycall.txt', aftertexts, br='\n')


def multpool(urls):
    from multiprocessing import Pool
    p = Pool(5)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
    _ = [p.apply_async(main, args=(url,)) for url in urls]

    p.close()
    p.join()


if __name__ == '__main__':

    from xjLib.log import MyLog
    mylog = MyLog()
    # print = mylog.print
    mylog.setlevel('xjLib.ahttp', 30)

    # main('https://www.biqukan.com/38_38836/')
    # mainbycall('https://www.biqukan.com/2_2714/')

    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/73_73450/',
        'https://www.biqukan.com/76_76015/',
        'https://www.biqukan.com/75_75766/',
        'https://www.biqukan.com/2_2714/',
        'https://www.biqukan.com/61_61396/',
    ]
    multpool(urls)
    # '38_38836'  #2676KB，#@  6秒
    # "2_2714"    #武炼巅峰，#@  38秒
