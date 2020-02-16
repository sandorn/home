# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-12 15:44:47
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-16 12:05:17
'''

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BqgItem(scrapy.Item):
    书名 = scrapy.Field()
    index = scrapy.Field()
    章节名称 = scrapy.Field()
    章节正文 = scrapy.Field()
    pass

    def get_insert_sql(self):
        insert_sql = """
                    insert into %s (BOOKNAME, INDEX, ZJNAME, ZJTEXT)
                    VALUES (%s,%s, %d, %s, %s);
                """
        params = (self["书名"], self["书名"], self["index"], self["章节名称"], self["章节正文"])
        return insert_sql, params
