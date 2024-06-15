# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-15 20:39:57
FilePath     : /CODE/项目包/线程小成果/Process+CustomThread爬虫类实现.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
from multiprocessing import Process

from xt_File import savefile
from xt_Ls_Bqg import Str_Replace, clean_Content
from xt_Requests import Head, get, htmlResponse
from xt_Thread import CustomThread


# 爬取一本小说
class ScrapyOne:
    def __init__(self, rootLink):
        super().__init__()
        self.rootLink = rootLink
        self.texts = []
        self.start()

    # 主函数
    def start(self):
        self.scrapyLink()
        urls = self.urls[:20]
        [CustomThread(self.scrapyText, index, url) for index, url in enumerate(urls)]
        CustomThread.wait_completed()
        self.texts.sort(key=lambda x: x[0])
        files = os.path.basename(__file__).split('.')[0]
        savefile(f'{files}&{self.bookname}ScrapyProcess.txt', self.texts, br='\n')

    # 爬取章节链接
    def scrapyLink(self):
        resp = get(self.rootLink, headers=Head().ua)
        assert isinstance(resp, htmlResponse)
        _xpath = [
            '//h1/text()',
            "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/@href",
            '//dl/span/dd/a/@href',
        ]
        bookname, temp_urls, temp_urls2 = resp.xpath(_xpath)

        self.bookname = bookname[0]
        temp_urls += temp_urls2
        baseurl = '/'.join(self.rootLink.split('/')[:-3])
        self.urls = [baseurl + item for item in temp_urls]  # # 章节链接
        return self.bookname, self.urls, ''

    # 爬取内容
    def scrapyText(self, index, url):
        resp = get(url)
        assert isinstance(resp, htmlResponse)
        _xpath = (
            '//h1/text()',
            '//*[@id="chaptercontent"]/text()',
        )

        _title, _showtext = resp.xpath(_xpath)
        title = Str_Replace(''.join(_title), [('\u3000', ' '), ('\xa0', ' '), ('\u00a0', ' ')])
        content = clean_Content(_showtext)
        self.texts.append([index, title, content])
        return [index, title, content]


class ScrapyProcess(Process):
    def __init__(self, link_list):
        super().__init__()
        self.link_list = link_list
        self.start()

    def run(self):
        for link in self.link_list:
            ScrapyOne(link)


if __name__ == '__main__':
    url_list = ['https://www.bigee.cc/book/6909/']
    ScrapyProcess(url_list)
