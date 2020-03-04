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
@LastEditors: Even.Sand
@LastEditTime: 2020-03-04 20:34:00
变更requests为ahttp
'''

import time

from xjLib.ahttp import ahttpGet, ahttpGetAll

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile


def get_download_url(target):
    urls = []  # 存放章节链接
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//h2', first=True).text
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []


def 结果处理(resps):
    for item in resps:
        response = item.html
        _name = response.xpath('//h1', first=True).text
        _showtext = "".join(response.xpath('//*[@id="content"]', first=True).text)

        name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })
        text = Ex_Re_Sub(
            _showtext,
            {
                '\'': '',
                ' ': ' ',
                '\xa0': ' ',
                '\x0a': '\n',
                # '\b;': '\n',
                '&nbsp;': ' ',
                'app2();': '',
                '笔趣看;': '',
                '\u3000': '',
                'chaptererror();': '',
                'readtype!=2&&(\'vipchapter\n(\';\n\n}': '',
                'm.biqukan.com': '',
                'wap.biqukan.com': '',
                'www.biqukan.com': '',
                'www.biqukan.com。': '',
                '百度搜索“笔趣看小说网”手机阅读:': '',
                '请记住本书首发域名:': '',
                '请记住本书首发域名：': '',
                '笔趣阁手机版阅读网址:': '',
                '笔趣阁手机版阅读网址：': '',
                '[]': '',
                '\r': '\n',
                '\n\n': '\n',
                '\n\n': '\n',
            }
        )

        texts.append([name, text])


def callback(future):
    resps = future.result()  # 回调函数取得返回值
    if resps is None:
        return False

    response = resps.html

    _name = response.xpath('//h1', first=True).text
    _showtext = "".join(response.xpath('//*[@id="content"]', first=True).text)

    name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })
    text = Ex_Re_Sub(
        _showtext,
        {
            '\'': '',
            ' ': ' ',
            '\xa0': ' ',
            '\x0a': '\n',
            # '\b;': '\n',
            '&nbsp;': ' ',
            'app2();': '',
            '笔趣看;': '',
            '\u3000': '',
            'chaptererror();': '',
            'readtype!=2&&(\'vipchapter\n(\';\n\n}': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            'www.biqukan.com。': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        }
    )

    texts.append([name, text])


if __name__ == '__main__':
    url = 'https://www.biqukan.com/2_2714/'
    _stime = time.time()

    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)

    print('AHTTP,开始下载：《' + bookname + '》', flush=True)
    # 方法1：使用回调，不排序
    resps = ahttpGetAll(urls, pool=50, callback=callback)
    '''
    # 方法2：不回调，获取最终结果，自动排序
    resps = ahttpGetAll(urls, pool=100)
    结果处理(resps)
    '''
    print('AHTTP，书籍《' + bookname + '》完成下载', flush=True)

    savefile(bookname + '.txt', texts)
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)

    # '76_76519'  #章节少，测试用#!4.3秒
    # "2_2714"   #武炼巅峰,#!173.8秒
