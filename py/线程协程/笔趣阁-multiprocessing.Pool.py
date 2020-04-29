# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 使用multiprocessing.pool多进程
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
#LastEditors  : Please set LastEditors
@Date: 2019-05-08 18:31:14
#LastEditTime : 2020-04-29 18:08:58
努努书坊 - 小说在线阅读   https://www.kanunu8.com/
'''

from multiprocessing import Pool
import os

from xjLib.ahttp import ahttpGet
from xjLib.mystr import Ex_Re_Sub, Ex_Replace, fn_timer, savefile


def get_download_url(target):
    urls = []  # 存放章节链接
    # response = etree.HTML(parse_get(target).content)
    resp = ahttpGet(target)
    response = resp.html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath(
        '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(args):
    (index, target) = args
    response = ahttpGet(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  \xa0"),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            '\xa0': '',  # 表示空格  &nbsp;
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

    return [index, name, '    ' + text]


@fn_timer
def main_Pool(target):
    texts = []
    bookname, urls = get_download_url(target)

    print('multiprocessing.pool，开始下载：《' + bookname + '》', flush=True)
    mypool = Pool(32)  # !进程数,不能超过61
    mypool.map_async(
        func=get_contents,
        iterable=[(i, urls[i]) for i in range(len(urls))],
        callback=lambda res: texts.append(res))
    # mypool.apply_async(func=get_contents,callback=_callba)
    mypool.close()  # 关闭进程池,不再接受请求
    mypool.join()  # 等待进程池中的事件执行完毕，回收进程池

    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'multiprocessing.txt', texts, br='\n')


if __name__ == '__main__':
    main_Pool('https://www.biqukan.com/38_38836/')
    # main_Pool('https://www.biqukan.com/2_2714/')
    # 38_38836     34.84 seconds
    # 2_2714      215.40 seconds
    # 81840_81840703
