# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-12 15:45:36
@LastEditors: Even.Sand
@LastEditTime: 2020-03-18 02:51:11
'''
import re

import MySQLdb
import pandas
import redis
import scrapy

from BQG.items import BqgItem
from xjLib.dBrouter import dbconf
from xjLib.mystr import align, md5


class Spider(scrapy.Spider):
    name = 'spiler'  # 设置name
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
        'https://www.biqukan.com/2_2714/',
        # 'https://www.biqukan.com/76_76519/',
        # 'https://www.biqukan.com/38_38836/',
        # 'https://www.biqukan.com/0_790/',
    ]

    db = set()
    res_db = {}
    connect = MySQLdb.connect(**dbconf['TXbook'])

    def start_requests(self):
        # 循环生成需要爬取的地址
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # dont_filter=True 表示不过滤

    def parse(self, response):
        # 爬取方法
        _BOOKNAME = response.xpath('//meta[@property="og:title"]//@content').extract_first()

        self.res_key = md5(_BOOKNAME)  # k相当于字典名称

        if _BOOKNAME not in self.db:
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
                % _BOOKNAME
            )
            self.connect.cursor().execute(CreateDb_sql)
            self.connect.commit()
            self.db.add(_BOOKNAME)

        if _BOOKNAME not in self.res_db:
            # #构建redis字典，用于去重
            self.res_db[self.res_key] = redis.Redis(host='127.0.0.1', port=6379, db=4)

            # #redis字典初始化,删除全部key
            self.res_db[self.res_key].flushdb()
            sql = "SELECT ZJHERF FROM %s;" % _BOOKNAME  # 从MySQL里提数据
            pandasData = pandas.read_sql(sql, self.connect)  # 读MySQL数据

            # #redis字典填充数据
            for _ZJHREF in pandasData['ZJHERF']:
                self.res_db[self.res_key].hset(self.res_key, md5(_ZJHREF), 0)

        全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a').extract()

        for index in range(len(全部章节节点)):
            _ZJHREF = re.match('<a href="(.*?)">', 全部章节节点[index]).group(1)
            _ZJHREF = response.urljoin(_ZJHREF)

            _ZJNAME = re.match('<a href=".*?">(.*?)</a>', 全部章节节点[index]).group(1)

            if not self.res_db[self.res_key].hexists(self.res_key, md5(_ZJHREF)):
                self.res_db[self.res_key].hset(self.res_key, md5(_ZJHREF), 0)

                request = scrapy.Request(_ZJHREF, meta={'index': index}, callback=self.parse_content)
                yield request
            else:
                print('--《' + align(_BOOKNAME, 20, 'center') + '》\t' + align(_ZJNAME, 40) + '\t|记录重复入库！')
                pass

    def parse_content(self, response):
        item = BqgItem()
        item['BOOKNAME'] = response.xpath('//div[@class="p"]/a[2]/text()').extract_first()
        item['INDEX'] = response.meta['index']
        item['ZJNAME'] = response.xpath('//h1/text()').extract_first()
        item['ZJTEXT'] = "".join(response.xpath('//*[@id="content"]/text()').extract())
        item['ZJHERF'] = response.url
        yield item


if __name__ == '__main__':
    from xjLib.ScrapyRun import ScrapyRun
    import os
    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(os.path.dirname(filepath))
    ScrapyRun(dirpath, 'spiler')


'''
# #爬取之后，入库之前去重
    def start_requests(self):
        # 循环生成需要爬取的地址
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            # dont_filter=True 表示不过滤

    def parse(self, response):

        # 编写爬取方法
        # #获取书籍名称，判断是否需要创建数据库
        _BOOKNAME = response.xpath(
            '//meta[@property="og:title"]//@content'
        ).extract_first()

        if _BOOKNAME not in self.db:
            # #创建数据库,用于储存爬取到的数据
            CreateDb_sql = "
            Create Table If Not Exists %s(
            `ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
            `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `INDEX` int(10) NOT NULL,
            `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            PRIMARY KEY (`ID`) USING BTREE)
            " % _BOOKNAME
            self.connect.cursor().execute(CreateDb_sql)
            self.connect.commit()
            self.db.add(_BOOKNAME)

        全部章节节点 = response.xpath(
            '//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a'
        ).extract()
        for index in range(len(全部章节节点)):
            href = re.match('<a href="(.*?)">', 全部章节节点[index]).group(1)
            # _ZJNAME = re.match('<a href=".*?">(.*?)</a>', 全部章节节点[index]).group(1).replace('\xa0', ' ')

            real_url = response.urljoin(href)
            request = scrapy.Request(
                real_url, meta={'index': index}, callback=self.parse_content)
            yield request

    def parse_content(self, response):
        item = BqgItem()
        item['BOOKNAME'] = response.xpath(
            '//div[@class="p"]/a[2]/text()').extract_first()
        _BOOKNAME = item['BOOKNAME']

        self.res_dict = md5(_BOOKNAME)  # k相当于字典名称

        if _BOOKNAME not in self.res_db:
            # #构建redis字典，用于去重
            self.res_db[self.res_dict] = redis.Redis(host='127.0.0.1', port=6379, db=4)

            # #redis字典初始化,删除全部key
            self.res_db[self.res_dict].flushdb()
            sql = "SELECT ZJNAME FROM %s;" % _BOOKNAME   # 从MySQL里提数据
            pandasData = pandas.read_sql(sql, self.connect)  # 读MySQL数据

            # #redis字典填充数据
            for _ZJNAME in pandasData['ZJNAME']:
                self.res_db[self.res_dict].hset(self.res_dict, md5(_ZJNAME.replace(' ', '')), 0)

        item['INDEX'] = response.meta['index']
        item['ZJNAME'] = response.xpath(
            '//h1/text()').extract_first().replace('\xa0', ' ')  # '�0�2 '
        _ZJNAME = item['ZJNAME']

        if not self.res_db[self.res_dict].hexists(self.res_dict, md5(_ZJNAME.replace(' ', ''))):
            self.res_db[self.res_dict].hset(
                self.res_dict, md5(_ZJNAME.replace(' ', '')), 0)
            print('查重************' + _ZJNAME)
            item['ZJTEXT'] = "".join(response.xpath(
                '//*[@id="content"]/text()').extract())
            yield item
        else:
            print('--《' + align(_BOOKNAME, 20, 'center') + '》\t' + align(_ZJNAME, 40) + '\t|记录重复入库！')
            pass
'''
