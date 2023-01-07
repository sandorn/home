# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-07 15:04:21
FilePath     : /项目包/线程小成果/进程+多线程爬虫.py
Github       : https://github.com/sandorn/home
==============================================================
'''

from multiprocessing import Process

from xt_File import savefile
from xt_Ls_Bqg import Str_Replace, clean_Content
from xt_Requests import Headers, get, htmlResponse
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
        r = CustomThread(target=self.scrapyLink)
        r.wait_completed()
        [CustomThread(self.scrapyText, index, url) for index, url in enumerate(self.urls)]
        CustomThread.wait_completed()
        self.texts.sort(key=lambda x: x[0])
        savefile(f'{self.bookname}ScrapyProcess.txt', self.texts, br='\n')

    # 爬取章节链接
    def scrapyLink(self):
        resp = get(self.rootLink, headers=Headers().randomheaders)
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

    def __init__(self, typeLink):
        super(ScrapyProcess, self).__init__()
        self.typeLink = typeLink
        self.start()

    def run(self):
        one = ScrapyOne(self.typeLink)


if __name__ == "__main__":
    ScrapyProcess('http://www.biqugse.com/96703/')
