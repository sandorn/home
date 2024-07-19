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
from xt_database.xt_mysql import DbEngine as mysql
from xt_ls_bqg import clean_Content
from xt_str import Str_Replace, align

_p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(_p)

from items import BqgItem  # noqa: E402


class Spider(scrapy.Spider):
    name = "spilerByset"  # 设置name

    custom_settings = {
        "ITEM_PIPELINES": {
            "BQG.pipelines.Pipeline2Csv": 4
            # 'BQG.pipelines.PipelineToSqlTwisted': 10,  # 25s
            # 'BQG.pipelines.PipelineToAiomysqlpool': 20,  # 27s
            # 'BQG.pipelines.PipelineToAsynorm': 80,  # 32s
            # 'BQG.pipelines.PipelineToAiomysql': 100,  # 33s
            # 'BQG.pipelines.PipelineToSqlalchemy': 200,  # 135s
            # 'BQG.pipelines.PipelineToMysql': 300,  # 170s
        }
    }

    # ... 其他代码

    start_urls = ["https://www.biquge11.cc/read/11159/"]

    # 编写爬取方法
    def start_requests(self):
        # 循环生成需要爬取的地址
        self.connect = mysql("TXbook", "MySQLdb")
        self.db = set()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)  # dont_filter=True 表示不过滤

    def parse(self, response):
        # #获取书籍名称
        # _bookname = response.xpath('//meta[@property="og:title"]//@content').extract_first()
        _bookname = response.xpath("//h1/text()").extract_first()
        if _bookname not in self.db:
            # 避免重复创建数据库
            Csql = f"Create Table If Not Exists {_bookname}(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,`ZJHERF` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)"
            self.connect.execute(Csql)
            self.db.add(_bookname)

        _result = self.connect.get_all_from_db(_bookname)
        assert isinstance(_result, (list, tuple))
        ZJHERF_list = [res[5] for res in _result]

        # 全部章节链接 = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        # titles = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()').extract()
        全部章节链接 = response.xpath("//dt[1]/following-sibling::dd/a/@href").extract()
        print(999, _bookname, 全部章节链接)
        # https://www.biqukan8.cc
        baseurl = "/".join(response.url.split("/")[:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接
        for index in range(len(urls)):
            if urls[index] not in ZJHERF_list:
                yield scrapy.Request(urls[index], meta={"index": index, "name": _bookname}, callback=self.parse_content)
            else:
                print(f"spilerByset-->《{align( _bookname, 16)}》\t{align(index, 6)}\t | 记录重复，剔除！！")

    def parse_content(self, response):
        item = BqgItem()
        # item['BOOKNAME'] = response.xpath('//div[@class="con_top"]/a[2]/text()').extract_first()
        item["BOOKNAME"] = response.meta["name"]  # @接收meta={}传递的参数
        item["INDEX"] = response.meta["index"]  # @接收meta={}传递的参数
        item["ZJNAME"] = response.xpath("//h1/text()").extract_first()
        item["ZJNAME"] = Str_Replace(item["ZJNAME"].strip("\r\n"), [("\u3000", " "), ("\xa0", " "), ("\u00a0", " ")])
        _ZJTEXT = response.xpath('//*[@id="chaptercontent"]/text()').extract()
        item["ZJTEXT"] = "\n".join([st.strip("\r\n　  ") for st in _ZJTEXT])
        item["ZJTEXT"] = Str_Replace(clean_Content(item["ZJTEXT"]), [("%", "%%"), ("'", "\\'"), ('"', '\\"')])
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
