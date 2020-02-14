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
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-14 16:36:28
'''

import scrapy
from BQG.items import BqgItem
from pyquery import PyQuery


class XiashuSpider(scrapy.Spider):
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
    name = 'xiashu'
    # 设定域名
    allowed_domains = ['biqukan.com']
    # 填写爬取地址
    start_urls = ['https://www.biqukan.com/2_2704/']

    # 编写爬取方法
    def parse(self, response):
        self.书名 = response.xpath('//meta[@property="og:title"]//@content').extract()[0]
        全部章节链接 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href').extract()

        for index in range(10):  # range(len(全部章节链接)):
            url = 'https://www.biqukan.com' + str(全部章节链接[index])
            yield scrapy.Request(url=url, meta={'index': index}, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        torrent = BqgItem()
        torrent['书名'] = self.书名
        torrent['index'] = response.meta['index']
        torrent['章节名称'] = response.xpath('//h1/text()').extract()[0]
        _soup = PyQuery(response.text)
        _showtext = _soup('#content').text()  # '.showtxt'
        torrent['章节正文'] = _showtext.replace('[笔趣看\xa0\xa0www.biqukan.com]', '')
        yield torrent

    def parse_detail(self, response):
        pass


'''
# torrent['书名'] = response.xpath("//h2/text()").extract()
# torrent['书名'] = response.xpath('//div[@class="listmain"]/dl/dt[2]/text()').extract()
torrent['download_url'] = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
torrent['章节名称'] = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/text()').extract()
zjs = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd')
self.index = 0
for zj in zjs:  # 一级页面的总父级
    url = zj.xpath('//dd/a/@href').extract()
    print('https://www.biqukan.com' + str(url) + '\n')
    yield scrapy.Request('https://www.biqukan.com' + str(url), callback=self.parse_info, dont_filter=True)
# torrent['章节正文'] = response.xpath('//div[@id="content"]//text()').extract()
'''

'''
# 需要实例化ItemLoader， 注意第一个参数必须是实例化的对象...
atricleItemLoader = ItemLoader(item = articleDetailItem(), response=response)
# 调用xpath选择器，提取title信息
atricleItemLoader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
# 调用css选择器，提取praise_nums信息
atricleItemLoader.add_css('praise_nums', '.vote-post-up h10::text')
# 直接给字段赋值，尤其需要注意，不管赋值的数据是什么，都会自动转换成list类型
atricleItemLoader.add_value('url', response.url)

# 将提取好的数据load出来
articleInfo = atricleItemLoader.load_item()
# 三种方式填充的数据，均为List类型
'''
