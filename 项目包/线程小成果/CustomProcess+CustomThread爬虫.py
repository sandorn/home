# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-03 12:52:03
LastEditTime : 2023-01-03 12:52:04
FilePath     : /项目包/线程小成果/CustomProcess+CustomThread爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import os
from multiprocessing import Pool

from xt_File import savefile
from xt_Requests import get
from xt_Response import ReqResult
from xt_String import Re_Sub, Str_Clean, Str_Replace, UNprintable_Chars
from xt_Thread import CustomThread, Do_CustomProcess


def clean_Content(in_str):
    clean_list = [
        "', '",
        '&nbsp;',
        ';[笔趣看  www.biqukan.com]',
        'www.biqukan.com。',
        'wap.biqukan.com',
        'www.biqukan.com',
        'm.biqukan.com',
        'n.biqukan.com',
        'www.biqukan8.cc。',
        'www.biqukan8.cc',
        'm.biqukan8.cc。',
        'm.biqukan8.cc',
        '百度搜索“笔趣看小说网”手机阅读:',
        '百度搜索“笔趣看小说网”手机阅读：',
        '请记住本书首发域名:',
        '请记住本书首发域名：',
        '笔趣阁手机版阅读网址:',
        '笔趣阁手机版阅读网址：',
        '关注公众号：书友大本营  关注即送现金、点币！',
        '<br />',
        ';[笔趣看  ]',
        '[笔趣看 ]',
        '<br />',
        '\t',
    ]
    clean_list += UNprintable_Chars
    sub_list = [
        (r'\(https:///[0-9]{0,4}_[0-9]{0,12}/[0-9]{0,16}.html\)', ''),
    ]
    repl_list = [
        (u'\u3000', '  '),
        (u'\xa0', ' '),
        (u'\u0009', ' '),
        (u'\u000B', ' '),
        (u'\u000C', ' '),
        (u'\u0020', ' '),
        (u'\u00a0', ' '),
        (u'\uFFFF', ' '),
        (u'\u000A', '\n'),
        (u'\u000D', '\n'),
        (u'\u2028', '\n'),
        (u'\u2029', '\n'),
        ('\r', '\n'),
        ('    ', '\n    '),
        ('\r\n', '\n'),
        ('\n\n', '\n'),
    ]

    if isinstance(in_str, (list, tuple)):
        in_str = '\n'.join([item.strip("\r\n　  ") for item in in_str])
    in_str = in_str.strip("\r\n ")

    in_str = Str_Clean(in_str, clean_list)
    in_str = Re_Sub(in_str, sub_list)
    in_str = Str_Replace(in_str, repl_list)
    return in_str


def get_biqugse_download_url(target):
    # print(f'get_biqugse_download_url | Parent Pid:{os.getppid()} | Pid: {os.getpid()}')
    resp = get(target)
    assert isinstance(resp, ReqResult)
    _xpath = (
        '//meta[@property="og:title"]//@content',
        '//dt[2]/following-sibling::dd/a/@href',
        '//dt[2]/following-sibling::dd/a/text()',
    )
    bookname, temp_urls, titles = resp.xpath(_xpath)
    bookname = bookname[0]
    baseurl = '/'.join(target.split('/')[:-2])
    urls = [baseurl + item for item in temp_urls]  # # 章节链接

    _ = [CustomThread(get_contents, index, urls[index]) for index in range(len(urls))]
    text_list = CustomThread.getAllResult()
    text_list.sort(key=lambda x: x[0])  # #排序
    # aftertexts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(f'{files}&{bookname}&CustomProcess+CustomThread.txt', text_list, br='\n')


def get_contents(index, target):
    # print(f'get_contents | Parent Pid:{os.getppid()} | Pid: {os.getpid()}')
    resp = get(target)
    assert isinstance(resp, ReqResult)
    _xpath = (
        '//h1/text()',
        '//*[@id="content"]/text()',
    )
    _title, _showtext = resp.xpath(_xpath)
    title = Str_Replace("".join(_title), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
    content = clean_Content(_showtext)
    return [index, title, content]


if __name__ == '__main__':
    url_list = [
        'http://www.biqugse.com/96703/',
        'http://www.biqugse.com/96704/',
        'http://www.biqugse.com/96705/',
        'http://www.biqugse.com/96706/',
        'http://www.biqugse.com/96707/',
        'http://www.biqugse.com/96708/',
    ]

    def main():
        for url in url_list:
            Do_CustomProcess(get_biqugse_download_url, [url])
        # 45s~82s

    # main()

    def Pool_main():
        p = Pool(6)  # 进程池中从无到有创建三个进程,以后一直是这三个进程在执行任务
        res_l = []
        for url in url_list:
            res = p.apply_async(get_biqugse_download_url, args=(url, ))  # 异步执行任务
            res_l.append(res)

        p.close()
        p.join()
        # res_list = [res.get() for res in res_l]
        # print(res_list)
        # 38s

    Pool_main()
