# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-16 14:20:05
FilePath     : /CODE/项目包/线程小成果/进程+多线程爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
from multiprocessing import Process

from xt_File import savefile
from xt_Ls_Bqg import Str_Replace, clean_Content
from xt_Requests import Head, get, htmlResponse
from xt_Thread import CustomThread


# 爬取一本小说
class ScrapyOne():

    def __init__(self, rootLink):
        super().__init__()
        self.rootLink = rootLink
        self.texts = []
        self.start()

    # 主函数
    def start(self):
        self.scrapyLink()
        [CustomThread(self.scrapyText, index, url) for index, url in enumerate(self.urls)]
        CustomThread.wait_completed()
        self.texts.sort(key=lambda x: x[0])
        files = os.path.basename(__file__).split(".")[0]
        savefile(f'{files}&{self.bookname}ScrapyProcess.txt', self.texts, br='\n')

    # 爬取章节链接
    def scrapyLink(self):
        resp = get(self.rootLink, headers=Head().random)
        assert isinstance(resp, htmlResponse)
        _xpath = [
            '//meta[@property="og:title"]//@content',
            '//dt[2]/following-sibling::dd/a/@href',
            '//dt[2]/following-sibling::dd/a/text()',
        ]
        bookname, temp_urls, self.titles = resp.xpath(_xpath)

        self.bookname = bookname[0]
        baseurl = '/'.join(self.rootLink.split('/')[:-2])
        self.urls = [baseurl + item for item in temp_urls]  # # 章节链接
        return self.bookname, self.urls, self.titles

    # 爬取内容
    def scrapyText(self, index, url):
        resp = get(url)
        assert isinstance(resp, htmlResponse)
        _xpath = (
            '//h1/text()',
            '//*[@id="content"]/text()',
        )

        _title, _showtext = resp.xpath(_xpath)
        title = Str_Replace("".join(_title), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
        content = clean_Content(_showtext)
        self.texts.append([index, title, content])
        return [index, title, content]


class ScrapyProcess(Process):

    def __init__(self, link_list):
        super(ScrapyProcess, self).__init__()
        self.link_list = link_list
        self.start()

    def run(self):
        for link in self.link_list:
            ScrapyOne(link)


if __name__ == "__main__":
    url_list = [
        'http://www.biqugse.com/96703/',  # 18s
        # 'http://www.biqugse.com/96717/',
        # 'http://www.biqugse.com/76169/',
        # 'http://www.biqugse.com/82744/',
        # 'http://www.biqugse.com/96095/',
        # 'http://www.biqugse.com/92385/',
    ]
    ScrapyProcess(url_list)
