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
@LastEditors: Even.Sand
@LastEditTime : 2020-02-16 12:05:17
'''

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.loader.processors import MapCompose, TakeFirst


class BqgItem(scrapy.Item):
    BOOKNAME = scrapy.Field()  # output_processor=TakeFirst())
    INDEX = scrapy.Field()
    ZJNAME = scrapy.Field()  # output_processor=TakeFirst())
    ZJTEXT = scrapy.Field()
    pass
