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
@LastEditTime: 2020-02-19 18:53:39
'''

import scrapy
from BQG.items import BqgItem
import MySQLdb
from xjLib.dBrouter import dbconf
import redis


class Spider(scrapy.Spider):
    '''
    name:scrapy唯一定位实例的属性，必须唯一
    allowed_domains：允许爬取的域名列表，不设置表示允许爬取所有
    start_urls：起始爬取列表
    start_requests：它就是从start_urls中读取链接，然后使用make_requests_from_url生成Request，这就意味我们可以在start_requests方法中根据我们自己的需求往start_urls中写入我们自定义的规律的链接。
    parse：回调函数，处理response并返回处理后的数据和需要跟进的url
    log：打印日志信息
    closed：关闭spider
    '''

    # 设置name
    name = 'spiler'
    # 设定域名
    allowed_domains = ['biqukan.com']
    # 扩展设置
    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'BQG.pipelines.PipelineCheck': 10,
            'BQG.pipelines.PipelineSqlCheck': 50,
            'BQG.pipelines.PipelineToSqlTwisted': 200
        },
    }
    # 填写爬取地址
    start_urls = [
        'https://www.biqukan.com/32_32061/',
    ]
    db = set()
    connect = MySQLdb.connect(**dbconf['TXbook'])
    cur = connect.cursor()
    redb = set()
    redis_db = {}
    redis_dict = {}

    # 编写爬取方法
    def parse(self, response):
        _BOOKNAME = response.xpath('//meta[@property="og:title"]//@content').extract_first()
        if _BOOKNAME not in self.db:
            # 避免重复创建数据库
            Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)' % _BOOKNAME
            self.cur.execute(Csql)
            self.connect.commit()
            self.db.add(_BOOKNAME)
            self.redis_db[_BOOKNAME] = redis.Redis(host='127.0.0.1', port=6379, db=4)
            self.redis_dict[_BOOKNAME] = "ZJNAME"  # k相当于字典名称
            # 删除全部key
            self.redis_db[_BOOKNAME].flushdb()
            sql = "SELECT ZJNAME FROM %s;" % _BOOKNAME  # 从MySQL里提数据
            pandasData = pandas.read_sql(sql, self.connect)  # 读MySQL数据

            for res in pandasData['ZJNAME']:
                self.redis_db[_BOOKNAME].hset(self.redis_dict[_BOOKNAME], res, 0)
            self.redb.add(_BOOKNAME)

        全部章节链接 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href').extract()

        for index in range(len(全部章节链接)):
            url = 'https://www.biqukan.com' + str(全部章节链接[index])
            yield scrapy.Request(url=url, meta={'index': index}, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        item = BqgItem()
        item['BOOKNAME'] = response.xpath('//div[@class="p"]/a[2]/text()').extract_first()
        item['INDEX'] = response.meta['index']
        item['ZJNAME'] = response.xpath('//h1/text()').extract_first()
        item['ZJTEXT'] = "".join(response.xpath('//*[@id="content"]/text()').extract())
        yield item

    def parse_detail(self, response):
        pass
