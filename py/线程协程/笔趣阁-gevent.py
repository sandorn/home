# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-03 10:10:51
@LastEditors: Even.Sand
@LastEditTime: 2020-03-12 10:20:48
'''
import time

from gevent import monkey, pool
from lxml import etree

from xjLib.mystr import Ex_Re_Sub, get_stime, savefile
from xjLib.req import parse_get

monkey.patch_socket()


texts = []  # 将爬下来的小说都存在里面，做最后排序


def get_download_url(target):
    urls = []  # 存放章节链接
    response = etree.HTML(parse_get(target).content)
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(index, target):

    response = etree.HTML(parse_get(target).content)
    _name = response.xpath('//h1/text()')[0]
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))

    print('{}\tdone\tat\t{}'.format(index, get_stime()), flush=True)

    name = Ex_Re_Sub(_name, {'\'': '', ' ': ' ', '\xa0': ' ', })

    text = Ex_Re_Sub(
        _showtext,
        {
            '\'': '',
            ' ': ' ',
            '\xa0': ' ',
            #'\x0a': '\n',
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
    texts.append([index, name, text])


def main_thread(target):
    _stime = time.time()
    bookname, urls = get_download_url(target)
    #WaitList = []
    print('gevent，开始下载：《' + bookname + '》', flush=True)
    gpool = pool.Pool(100)
    for index in range(len(urls)):
        gpool.spawn(get_contents, index, urls[index])
        # WaitList.append(res)

    gpool.join()  # join等待线程执行结束

    print('gevent，书籍《' + bookname + '》完成下载', flush=True)
    textssord = sorted(texts, key=lambda x: x[0])
    savefile(bookname + '.txt', textssord)
    print('下载《{}》完成，用时:{} 秒。'.format(bookname, round(time.time() - _stime, 2)),
          flush=True)


if __name__ == '__main__':
    main_thread('https://www.biqukan.com/76_76519/')
    # '76_76519'  #章节少，测试用 20秒
    # '2_2704'  420.94 秒
    # "2_2714"   #《武炼巅峰》664万字, 秒。
