# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-11-14 21:48:46
FilePath     : /项目包/BQG.spider/BQG/spiders/xiashu.py
LastEditTime : 2022-11-16 12:50:36
Github       : https://github.com/sandorn/home
==============================================================
'''

import os
import sys

# '***获取上级目录***'
_p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(_p)

import scrapy
from items import BqgItem
from xt_Ls_Bqg import clean_Content
from xt_String import Str_Replace


class XiashuSpider(scrapy.Spider):

    name = 'xiashu'  # 设置name

    # allowed_domains = ['biqukan8.cc']  # 设定域名

    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            # 'BQG.pipelines.PipelineToSqlalchemy': 20,
            # 'BQG.pipelines.PipelineToSqlTwisted': 30,
            # 'BQG.pipelines.PipelineToSql': 40,
            # 'BQG.pipelines.PipelineCheck': 50,
            # 'BQG.pipelines.PipelineToTxt': 100,
            # 'BQG.pipelines.PipelineToJson': 200,
            # 'BQG.pipelines.PipelineToJsonExp': 250,
            # 'BQG.pipelines.PipelineToCsv': 300,
            'BQG.pipelines.Pipeline2Csv': 400
            # 'BQG.pipelines.PipelineMysql2Txt': 500,
        },
    }

    start_urls = [
        'http://www.biqugse.com/96703/',
        'http://www.biqugse.com/96717/',
        'http://www.biqugse.com/2367/',
    ]

    # 编写爬取方法
    def parse(self, response):
        _BOOKNAME = response.xpath('//meta[@property="og:title"]//@content').extract_first()
        全部章节链接 = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        # titles = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()').extract()

        baseurl = '/'.join(response.url.split('/')[0:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接

        for index in range(len(urls)):
            # @meta={}传递参数,给callback
            yield scrapy.Request(url=urls[index], meta={'BOOKNAME': _BOOKNAME, 'index': index}, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        item = BqgItem()
        item['BOOKNAME'] = response.meta['BOOKNAME']  # @接收meta={}传递的参数
        item['INDEX'] = response.meta['index']  # @接收meta={}传递的参数
        item['ZJNAME'] = response.xpath('//h1/text()').extract_first()
        item['ZJNAME'] = Str_Replace(item['ZJNAME'].strip('\r\n'), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
        item['ZJTEXT'] = response.xpath('//*[@id="content"]/text()').extract()
        item['ZJTEXT'] = Str_Replace(clean_Content(item['ZJTEXT']), [('%', '%%'), ("'", "\\\'"), ('"', '\\\"')])
        item['ZJHERF'] = response.url
        yield item

    def parse_detail(self, response):
        pass


if __name__ == '__main__':
    from xt_ScrapyRun import ScrapyRun

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, 'xiashu')
