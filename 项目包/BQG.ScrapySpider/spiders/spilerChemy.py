# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-03 20:54:21
#FilePath     : /项目包/BQG.ScrapySpider/spiders/spilerChemy.py
#LastEditTime : 2020-06-04 14:03:12
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import os
import sys

# #上级目录
this_path = os.path.dirname(__file__)
parent_path = os.path.dirname(this_path)
sys.path.append(parent_path)
# #项目工作目录
sys.path.append(os.getcwd())


import re

import MySQLdb
import pandas
import scrapy

from items import BqgItem
from xt_DAO.dbconf import db_conf
from xt_String import align, md5


class Spider(scrapy.Spider):
    name = 'spilerChemy'  # 设置name，用于区分多个爬虫
    allowed_domains = ['biqukan.com']  # 设定域名
    # 扩展设置
    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'BQG.pipelines.PipelineCheck': 20,
            'BQG.pipelines.PipelineToSqlTwisted': 100,
            'BQG.pipelines.PipelineToTxt': 200
        }
    }

    start_urls = [
        # 填写爬取地址
        # 'https://www.biqukan.com/2_2714/',
        # 'https://www.biqukan.com/76_76519/',
        'https://www.biqukan.com/38_38836/',
    ]

    db = set()
    zjurls = {}
    if db_conf['TXbook'].get('type'):
        db_conf['TXbook'].pop('type')
    connect = MySQLdb.connect(**db_conf['TXbook'])

    def start_requests(self):
        # 循环生成需要爬取的地址
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # dont_filter=True 表示不过滤

    def parse(self, response):
        # #获取书籍名称，判断是否需要创建数据库
        _bookname = response.xpath('//meta[@property="og:title"]//@content').extract_first()

        self.res_key = md5(_bookname)  # k相当于字典名称

        if _bookname not in self.db:
            # #创建数据库,用于储存爬取到的数据
            CreateDb_sql = (
                '''
            Create Table If Not Exists %s(
            `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
            `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `INDEX` int(10) NOT NULL,
            `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `ZJHERF` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            PRIMARY KEY (`ID`) USING BTREE)
            '''
                % _bookname
            )
            self.connect.cursor().execute(CreateDb_sql)
            self.connect.commit()
            self.db.add(_bookname)

        if _bookname not in self.zjurls:
            # #构建set字典，用于去重
            self.zjurls[_bookname] = set()
            sql = "SELECT ZJHERF FROM %s;" % _bookname  # 从MySQL里提数据
            pandasData = pandas.read_sql(sql, self.connect)  # 读MySQL数据

            # #set字典填充数据
            for _zj_link in pandasData['ZJHERF']:
                self.zjurls[_bookname].add(md5(_zj_link))

        全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a').extract()

        for index in range(len(全部章节节点)):
            _zj_link = re.match('<a href="(.*?)">', 全部章节节点[index]).group(1)
            _zj_link = response.urljoin(_zj_link)

            _zj_title = re.match('<a href=".*?">(.*?)</a>', 全部章节节点[index]).group(1)

            if md5(_zj_link) not in self.zjurls[_bookname]:
                self.zjurls[_bookname].add(md5(_zj_link))
                request = scrapy.Request(_zj_link, meta={'index': index}, callback=self.parse_content)
                yield request
            else:
                print('--《' + align(_bookname, 20, 'center') + '》\t' + align(_zj_title, 40) + '\t|记录重复入库！')
                pass

    def parse_content(self, response):
        item = BqgItem()
        item['BOOKNAME'] = response.xpath('//div[@class="p"]/a[2]/text()').extract_first()
        item['INDEX'] = response.meta['index']
        item['ZJNAME'] = response.xpath('//h1/text()').extract_first()  # .replace('\xa0', ' ')  # '�0�2 '
        item['ZJTEXT'] = "".join(response.xpath('//*[@id="content"]/text()').extract())
        item['ZJHERF'] = response.url
        yield item


if __name__ == '__main__':
    from xt_ScrapyRun import ScrapyRun

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(os.path.dirname(filepath))
    ScrapyRun(dirpath, 'spilerChemy')
