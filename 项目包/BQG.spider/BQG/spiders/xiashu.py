# !/usr/bin/env python
"""
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2023-01-03 14:06:48
FilePath     : /项目包/BQG.spider/BQG/spiders/xiashu.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import sys

import scrapy
from xt_ls_bqg import clean_Content
from xt_str import Str_Replace

# '***获取上级目录***'
_p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(_p)

from items import BqgItem  # noqa: E402


class XiashuSpider(scrapy.Spider):
    name = "xiashu"  # 设置name

    custom_settings = {
        "ITEM_PIPELINES": {
            "BQG.pipelines.Pipeline2Csv": 40
            # 'BQG.pipelines.PipelineToTxt': 100,
            # 'BQG.pipelines.PipelineToJson': 200,
            # 'BQG.pipelines.PipelineToJsonExp': 250,
            # 'BQG.pipelines.PipelineToCsv': 300,
        }
    }

    start_urls = ["https://www.biquge11.cc/read/11159/"]

    # 编写爬取方法
    def parse(self, response):
        _bookname = response.xpath("//h1/text()").extract_first()
        全部章节链接 = response.xpath("//dt[1]/following-sibling::dd/a/@href").extract()
        print(999, _bookname, 全部章节链接)
        # titles = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()').extract()

        baseurl = "/".join(response.url.split("/")[:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接

        for index in range(len(urls)):
            # @meta={}传递参数,给callback
            yield scrapy.Request(url=urls[index], meta={"BOOKNAME": _bookname, "INDEX": index}, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        item = BqgItem()
        item["BOOKNAME"] = response.meta["BOOKNAME"]  # @接收meta={}传递的参数
        item["INDEX"] = response.meta["INDEX"]  # @接收meta={}传递的参数
        item["ZJNAME"] = response.xpath("//h1/text()").extract_first()
        item["ZJNAME"] = Str_Replace(item["ZJNAME"].strip("\r\n"), [("\u3000", " "), ("\xa0", " "), ("\u00a0", " ")])
        item["ZJTEXT"] = response.xpath('//*[@id="chaptercontent"]/text()').extract()
        item["ZJTEXT"] = Str_Replace(clean_Content(item["ZJTEXT"]), [("%", "%%"), ("'", "\\'"), ('"', '\\"')])
        item["ZJHERF"] = response.url
        yield item

    def parse_detail(self, response):
        pass


if __name__ == "__main__":
    from xt_scrapyrun import ScrapyRun

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, "xiashu")
