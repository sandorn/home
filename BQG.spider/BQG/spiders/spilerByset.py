# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:57
LastEditTime : 2024-06-14 14:57:38
FilePath     : /CODE/项目包/BQG.spider/BQG/spiders/spilerByset.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import os
import sys

import scrapy
from xt_database.sqlorm import SqlConnection
from xt_ls_bqg import clean_Content
from xt_str import Str_Replace, align

_p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(_p)

from items import BqgItem  # noqa: E402


class Spider(scrapy.Spider):
    name = "spilerByset"  # 设置name

    custom_settings = {
        "ITEM_PIPELINES": {
            "BQG.pipelines.Pipeline3Csv": 20,
            # "BQG.pipelines.PipelineToSqlTwisted": 50,  # 30s
            # "BQG.pipelines.PipelineToAioMySqlOrm": 80,  # 32s
            # "BQG.pipelines.PipelineToAiomySql": 100,  # 33s
            # "BQG.pipelines.PipelineToSqlalchemy": 200,  # 135s
            # "BQG.pipelines.PipelineToMysql": 300,  # 170s
        }
    }

    start_urls = ["https://www.bigee.cc/book/6909/"]
    baseurl = "https://www.bigee.cc/"

    def parse(self, response, **kwargs):
        # #获取书籍名称
        _bookname = response.xpath("//h1/text()").extract_first()
        _bookname = Str_Replace(
            "".join(_bookname.strip("\r\n")),
            [("\u3000", " "), ("\xa0", " "), ("\u00a0", " ")],
        )

        self.connect = SqlConnection("TXbook", _bookname, "dbtable")
        _result = self.connect.select()
        ZJHERF_list = [res[5] for res in _result]

        _tmp_urls = response.xpath(
            "//dl/span/preceding-sibling::dd[not(@class='more pc_none')]/a/@href",
        ).extract()
        全部章节链接 = _tmp_urls + response.xpath("//dl/span/dd/a/@href").extract()

        urls = [f"{self.baseurl}{item}" for item in 全部章节链接]  ## 章节链接

        for index in range(len(urls)):
            if urls[index] not in ZJHERF_list:
                yield scrapy.Request(
                    urls[index],
                    meta={"index": index, "name": _bookname},
                    callback=self.parse_content,
                )
            else:
                print(
                    f"spilerByset-->《{align( _bookname, 16)}》\t{align(index, 6)}\t | 记录重复，剔除！！"
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


if __name__ == "__main__":
    from xt_scrapyrun import ScrapyRun

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, "spilerByset")

###############################################################################
"""
方法1
       全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a').extract()

        for index in range(len(全部章节节点)):
            _ZJHERF = re.match('<a href="(.*?)">', 全部章节节点[index]).group(1)
            _ZJHERF = response.urljoin(_ZJHERF)
            _ZJNAME = re.match('<a href=".*?">(.*?)</a>', 全部章节节点[index]).group(1)

方法2
        全部章节链接 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        全部章节名称 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/text()').extract()
        baseurl = '/'.join(response.url.split('/')[0:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接
"""
