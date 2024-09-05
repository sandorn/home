# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-08-23 16:01:33
LastEditTime : 2024-09-05 16:48:30
FilePath     : /CODE/BQG.spider/BQG/spiders/xiashu.py
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
            "BQG.pipelines.Pipeline3Csv": 20,
            # "BQG.pipelines.Pipeline2Csv": 40,
            # "BQG.pipelines.PipelineToTxt": 100,
            # "BQG.pipelines.PipelineToJson": 200,
            # "BQG.pipelines.PipelineToJsonExp": 250,
            # "BQG.pipelines.PipelineToCsv": 300,
        }
    }

    start_urls = ["https://www.bigee.cc/book/6909/"]
    host_url = "https://www.bigee.cc/"

    def parse(self, response, **kwargs):
        _bookname = response.xpath("//h1/text()").extract_first()
        _bookname = Str_Replace(
            "".join(_bookname.strip("\r\n")),
            [("\u3000", " "), ("\xa0", " "), ("\u00a0", " ")],
        )

        全部章节链接 = response.xpath(
            "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/@href",
        ).extract()

        全部章节链接.extend(response.xpath("//dl/span/dd/a/@href").extract())

        urls = [f"{self.host_url}{item}" for item in 全部章节链接]  ## 章节链接
        for index in range(len(urls)):
            yield scrapy.Request(
                url=urls[index],
                meta={"name": _bookname, "index": index},
                callback=self.parse_content,
                dont_filter=True,
            )

    def parse_content(self, response):
        item = BqgItem()
        item["BOOKNAME"] = response.meta["name"]  # @接收meta={}传递的参数
        item["INDEX"] = response.meta["index"]  # @接收meta={}传递的参数
        item["ZJNAME"] = response.xpath("//h1/text()").extract_first()
        item["ZJTEXT"] = response.xpath("//*[@id='chaptercontent']/text()").extract()
        item["ZJTEXT"] = Str_Replace(
            clean_Content(item["ZJTEXT"]), [("%", "%%"), ("'", "\\'"), ('"', '\\"')]
        )
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
