# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-02-27 11:40:29
#FilePath     : /项目包/BQG.spider/BQG/spiders/spilerByset.py
#LastEditTime : 2020-07-15 10:16:03
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import os
import sys

_p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(_p)

import scrapy
from items import BqgItem
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from xt_DAO.xt_chemyMeta import Base_Model
from xt_DAO.xt_mysql import engine as mysql
from xt_Ls_Bqg import clean_Content
from xt_String import Str_Replace, align


def make_model(_BOOKNAME):
    # # 类工厂函数
    class table_model(Base_Model):
        # Base_Model 继承自from xt_DAO.xt_chemyMeta.Model_Method_Mixin
        __tablename__ = _BOOKNAME

        ID = Column(INTEGER(10), primary_key=True)
        BOOKNAME = Column(VARCHAR(255), nullable=False)
        INDEX = Column(INTEGER(10), nullable=False)
        ZJNAME = Column(VARCHAR(255), nullable=False)
        ZJTEXT = Column(TEXT, nullable=False)
        ZJHERF = Column(VARCHAR(255), nullable=False)

    return table_model


class Spider(scrapy.Spider):
    name = 'spilerByset'  # 设置name

    custom_settings = {
        #$ 使用数据库,判断重复入库
        'ITEM_PIPELINES': {
            'BQG.pipelines.PipelineToAiomysql': 20,
            # 'BQG.pipelines.PipelineToSqlalchemy': 20,
            # 'BQG.pipelines.PipelineToSqlTwisted': 30,
            # 'BQG.pipelines.PipelineToMysql': 40,
        },
    }

    start_urls = [
        'http://www.biqugse.com/96703/',
        # 'http://www.biqugse.com/96717/',
        # 'http://www.biqugse.com/2367/',
    ]

    # 编写爬取方法
    def start_requests(self):
        # 循环生成需要爬取的地址
        self.connect = mysql('TXbook')
        self.db = set()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)  # dont_filter=True 表示不过滤

    def parse(self, response):
        # #获取书籍名称
        _BOOKNAME = response.xpath('//meta[@property="og:title"]//@content').extract_first()
        if _BOOKNAME not in self.db:
            # 避免重复创建数据库
            Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,`ZJHERF` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)' % _BOOKNAME
            self.connect.execute(Csql)
            self.db.add(_BOOKNAME)

        _result = self.connect.get_all_from_db(_BOOKNAME)
        ZJHERF_list = [res[5] for res in _result]

        全部章节链接 = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        # titles = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()').extract()
        baseurl = '/'.join(response.url.split('/')[0:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接

        for index in range(len(urls)):
            if urls[index] not in ZJHERF_list:
                # @meta={}传递参数,给callback
                request = scrapy.Request(urls[index], meta={'index': index}, callback=self.parse_content)
                yield request
            else:
                # request = scrapy.Request(urls[index], meta={'index': index}, callback=self.parse_content)
                # yield request
                print(f'spilerByset-->《{align( _BOOKNAME, 16)}》\t{align(index, 6)}\t | 记录重复，剔除！！')
                pass

    def parse_content(self, response):
        item = BqgItem()
        item['BOOKNAME'] = response.xpath('//div[@class="con_top"]/a[2]/text()').extract_first()
        item['INDEX'] = response.meta['index']  # @接收meta={}传递的参数
        item['ZJNAME'] = response.xpath('//h1/text()').extract_first()
        item['ZJNAME'] = Str_Replace(item['ZJNAME'].strip('\r\n'), [(u'\u3000', u' '), (u'\xa0', u' '), (u'\u00a0', u' ')])
        _ZJTEXT = response.xpath('//*[@id="content"]/text()').extract()
        item['ZJTEXT'] = '\n'.join([st.strip("\r\n　  ") for st in _ZJTEXT])
        item['ZJTEXT'] = Str_Replace(clean_Content(item['ZJTEXT']), [('%', '%%'), ("'", "\\\'"), ('"', '\\\"')])
        item['ZJHERF'] = response.url
        yield item


if __name__ == '__main__':
    from xt_ScrapyRun import ScrapyRun

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, 'spilerByset')

###############################################################################
'''
方法1
       全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a').extract()


        for index in range(len(全部章节节点)):
            _ZJHERF = re.match('<a href="(.*?)">', 全部章节节点[index]).group(1)
            _ZJHERF = response.urljoin(_ZJHERF)
            _ZJNAME = re.match('<a href=".*?">(.*?)</a>', 全部章节节点[index]).group(1)

方法2：
        全部章节链接 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        全部章节名称 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/text()').extract()
        baseurl = '/'.join(response.url.split('/')[0:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接
'''
