# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:56
FilePath     : /项目包/BQG.spider/BQG/items.py
LastEditTime : 2022-11-19 00:48:52
Github       : https://github.com/sandorn/home
==============================================================
'''

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field
#from scrapy.loader.processors import MapCompose, TakeFirst


class BqgItem(Item):
    BOOKNAME = Field()  # output_processor=TakeFirst())
    INDEX = Field()
    ZJNAME = Field()  # output_processor=TakeFirst())
    ZJTEXT = Field()
    ZJHERF = Field()
    pass
