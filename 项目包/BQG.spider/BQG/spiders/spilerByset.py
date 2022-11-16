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
from xt_DAO.xt_sqlalchemy import SqlConnection
from xt_Ls_Bqg import clean_Content
from xt_String import Ex_md5, Str_Replace, align


def make_model(_BOOKNAME):
    # # 类工厂函数
    class table_model(Base_Model):
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

    # allowed_domains = ['biqukan8.cc']  # 设定域名

    custom_settings = {
        #@ 使用数据库模式,通过数据库判断是否重复录入
        'ITEM_PIPELINES': {
            'BQG.pipelines.PipelineToAiomysql': 20,
            # 'BQG.pipelines.PipelineToSqlalchemy': 20,
            # 'BQG.pipelines.PipelineToSqlTwisted': 30,
            # 'BQG.pipelines.PipelineToSql': 40,
            # 'BQG.pipelines.PipelineCheck': 50,
            # 'BQG.pipelines.PipelineToTxt': 100,
            # 'BQG.pipelines.PipelineToJson': 200,
            # 'BQG.pipelines.PipelineToJsonExp': 250,
            # 'BQG.pipelines.PipelineToCsv': 300,
            # 'BQG.pipelines.Pipeline2Csv': 400
            # 'BQG.pipelines.PipelineMysql2Txt': 500,
        },
    }

    start_urls = [
        # 'http://www.biqugse.com/96703/',
        # 'http://www.biqugse.com/96717/',
        'http://www.biqugse.com/2367/',
    ]

    bookdb = set()
    zjurls = {}

    # 编写爬取方法
    def start_requests(self):
        # 循环生成需要爬取的地址
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)  # dont_filter=True 表示不过滤

    def parse(self, response):
        # #获取书籍名称
        _BOOKNAME = response.xpath('//meta[@property="og:title"]//@content').extract_first()
        self.bookdb.add(Ex_md5(_BOOKNAME))  # k相当于字典名称
        DBtable = make_model(_BOOKNAME)
        sqlhelper = SqlConnection(DBtable, 'TXbook')

        if _BOOKNAME not in self.zjurls:
            # 构建set字典，用于去重
            self.zjurls[_BOOKNAME] = set()
            res = sqlhelper.select(Columns=['ZJHERF'])
            pandasData = [r[0] for r in res]
            # set字典填充数据
            for _ZJHERF in pandasData:
                self.zjurls[_BOOKNAME].add(Ex_md5(_ZJHERF))
        全部章节链接 = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        # titles = response.xpath('//*[@id="list"]/dl/dt[2]/following-sibling::dd/a/text()').extract()
        baseurl = '/'.join(response.url.split('/')[0:-2])
        urls = [baseurl + item for item in 全部章节链接]  ## 章节链接

        for index in range(len(urls)):
            if Ex_md5(urls[index]) not in self.zjurls[_BOOKNAME]:
                self.zjurls[_BOOKNAME].add(Ex_md5(urls[index]))
                # @meta={}传递参数,给callback
                request = scrapy.Request(urls[index], meta={'index': index}, callback=self.parse_content)
                yield request
            else:
                print('spilerByset--《' + align(_BOOKNAME, 16, 'center') + '》\t' + align(index, 30) + '\t | 记录重复，剔除！！')
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
    # from xt_Log import mylog
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
