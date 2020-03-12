# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-12 16:34:15
@LastEditors: Even.Sand
@LastEditTime: 2020-03-12 16:50:54
'''


import time

from lxml import etree
from multiprocess import Pool

from xjLib.ahttp import ahttpGet, ahttpGetAll
from xjLib.mystr import Ex_Re_Sub, get_stime, savefile


def get_download_url(target):
    urls = []  # 存放章节链接
    resp = ahttpGet(target)
    # response = resp.html
    # 指定解析器
    response = etree.HTML(resp.text)

    _bookname = response.xpath('//h2/text()', first=True)[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


texts = []


def 结果处理(resps):
    for resp in resps:
        index = resp.index
        response = etree.HTML(resp.text)

        _name = response.xpath('//h1/text()', first=True)[0]
        _showtext = "".join(response.xpath('//*[@id="content"]/text()', first=True))
        # '''
        name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })
        text = Ex_Re_Sub(
            _showtext,
            {
                '\'': '',
                ' ': ' ',
                '\xa0': ' ',
                # '\x0a': '\n', #!错误所在，可能导致\n\n查找不到
                '\b;': '\n',
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
            }
        )
        texts.append([index, name, '    ' + text])


def callback(future):
    resp = future
    if resp is None: return

    index = resp.index
    response = etree.HTML(resp.text)

    _name = response.xpath('//h1/text()', first=True)[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })
    text = Ex_Re_Sub(
        _showtext,
        {
            '\'': '',
            ' ': ' ',
            '\xa0': ' ',
            # '\x0a': '\n', #!错误所在，可能导致\n\n查找不到
            '\b;': '\n',
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
        }
    )

    texts.append([index, name, '    ' + text])


def main(url):
    _stime = time.time()
    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)
    print('AHTTP,开始下载：《' + bookname + '》', flush=True)

    # 方法2：不回调，获取最终结果，自动排序
    resps = ahttpGetAll(urls, pool=200)
    print('小说爬取完成，开始整理数据\t time:{} 。'.format(get_stime()))

    结果处理(resps)
    print('AHTTP，书籍《' + bookname + '》数据整理完成，time:{}'.format(get_stime()), flush=True)

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    savefile(bookname + '.txt', aftertexts, br='\n')
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)), flush=True)


def mainbycall(url):
    _stime = time.time()
    print('开始下载：《{}》\t{}\t获取下载链接......'.format(url, get_stime()), flush=True)
    bookname, urls = get_download_url(url)
    print('AHTTP,开始下载：《' + bookname + '》', flush=True)

    # 方法1：使用回调，不排序
    ahttpGetAll(urls, pool=100, callback=callback)
    print('AHTTP，书籍《' + bookname + '》完成下载')

    texts.sort(key=lambda x: x[0])  # #排序
    # @重新梳理数据，剔除序号
    aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    savefile(bookname + '.txt', aftertexts, br='\n')
    print('{} 结束，\t用时:{} 秒。'.format(get_stime(), round(time.time() - _stime, 2)))


if __name__ == '__main__':
    pool_result = []  # 进程池
    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/0_790/',
        'https://www.biqukan.com/10_10736/',
        'https://www.biqukan.com/2_2714/',
    ]
    mypool = Pool(20)  # !进程数
    for url in urls:
        result = mypool.apply_async(main, args=(url,))
        pool_result.append(result)
    mypool.close()  # 关闭进程池，表示不能在往进程池中添加进程
    mypool.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用

    #texts = []
    # main(url)
    # '76_76519'  #章节少，#@  4秒
    # '38_38836'  #2676KB，#@  9秒
    # '0_790'     #8977KB，#@  13秒
    # "10_10736"    #34712KB，#@  24秒
    # "2_2714"    #武炼巅峰，#@  36秒
