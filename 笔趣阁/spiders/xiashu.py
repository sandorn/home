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
@LastEditTime: 2020-02-19 15:36:37
'''

import scrapy
from BQG.items import BqgItem


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
    # 扩展设置
    custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'BQG.pipelines.PipelineCheck': 10,
            'BQG.pipelines.PipelineSqlCheck': 50,
            'BQG.pipelines.PipelineToSql': 200,
            # 'BQG.pipelines.PipelineToSqlTwisted': 200,
            # 'BQG.pipelines.PipelineToJson': 300,
            # 'BQG.pipelines.PipelineToJsonExp': 300,
            # 'BQG.pipelines.PipelineToTxt': 300,
            # 'BQG.pipelines.PipelineToCsv': 300,
            # 'BQG.pipelines.Pipeline2Csv': 300
        },
    }
    # 填写爬取地址
    start_urls = [
        'https://www.biqukan.com/32_32061/',
    ]

    # 编写爬取方法
    def parse(self, response):
        self.书名 = response.xpath('//meta[@property="og:title"]//@content').extract_first()

        全部章节链接 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href').extract()
        #3):  #
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
