# -*- coding: utf-8 -*-
import scrapy


class XiashuSpider(scrapy.Spider):
    name = 'xiashu'
    allowed_domains = ['itjuzi.comwww.biqukan.com']
    start_urls = ['http://itjuzi.comwww.biqukan.com/']

    def parse(self, response):
        pass
