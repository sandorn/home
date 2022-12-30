# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2022-12-30 11:00:25
FilePath     : /py学习/线程协程/使用Python爬取小说(多进程版).py
Github       : https://github.com/sandorn/home
==============================================================
'''
import random
import time
from multiprocessing import Process

from xt_File import savefile
from xt_Ls_Bqg import Str_Replace, clean_Content
from xt_Requests import MYHEAD, ReqResult, get


# 爬取一本小说
class ScrapyOne(object):

    def __init__(self, rootLink):
        super(ScrapyOne, self).__init__()
        self.rootLink = rootLink

    # 爬取每章的链接
    def scrapyLink(self):
        resp = get(self.rootLink, headers=MYHEAD)

        assert isinstance(resp, ReqResult)
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

    # 爬取一章的内容
    def scrapyText(self, index, url):
        resp = get(url)
        assert isinstance(resp, ReqResult)
        _xpath = (
            '//h1/text()',
            '//*[@id="content"]/text()',
        )

        _title, _showtext = resp.xpath(_xpath)
        title = Str_Replace("".join(_title), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
        content = clean_Content(_showtext)
        return [index, title, content]

    # 主函数
    def main(self):
        self.texts = []
        self.scrapyLink()
        for index, url in enumerate(self.urls):
            time.sleep(random.randint(1, 3))
            self.texts.append(self.scrapyText(index, url))
        savefile(f'{self.bookname}ScrapyProcess.txt', self.texts, br='\n')


class ScrapyProcess(Process):

    def __init__(self, typeLink):
        super(ScrapyProcess, self).__init__()
        self.typeLink = typeLink

    def run(self):
        one = ScrapyOne(self.typeLink)
        one.main()


if __name__ == "__main__":
    _str = 'http://www.biqugse.com/96703/'
    _process = ScrapyProcess(_str)
    _process.start()
