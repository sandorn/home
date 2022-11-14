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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-07-08 20:24:16
'''

import xlwt
from scrapy.exporters import JsonLinesItemExporter  # 默认显示的中文是阅读性较差的Unicode字符
from scrapy.exporters import BaseItemExporter

BOT_NAME = 'BQG'

SPIDER_MODULES = ['BQG.spiders']
NEWSPIDER_MODULE = 'BQG.spiders'

# 修改默认的输出编码方式
# 需要定义子类显示出原来的字符集（将父类的ensure_ascii属性设置为False即可）
#FEED_EXPORT_ENCODING = 'gb18030'
FEED_EXPORT_ENCODING = 'utf-8'

#LOG_FILE = './scrapy.log'
# CRITICAL - 严重错误(critical)
# ERROR - 一般错误(regular errors)
# WARNING - 警告信息(warning messages)
# INFO - 一般信息(informational messages)
# DEBUG - 调试信息(debugging messages)
LOG_LEVEL = 'ERROR'


class CustomJsonLinesItemExporter(JsonLinesItemExporter):

    def __init__(self, file, **kwargs):
        super(CustomJsonLinesItemExporter, self).__init__(file, encoding='utf-8', ensure_ascii=False, **kwargs)

    # 启用新定义的Exporter类\
    FEED_EXPORTERS = {
        'json': 'stockstar.settings.CustomJsonExporter',
    }


class ExcelExporter(BaseItemExporter):
    """
    导出为Excel，在执行命令中指定输出格式为excel
    e.g. scrapy crawl -t excel -o books.xls
    """

    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.wbook = xlwt.Workbook(encoding='utf-8')
        self.wsheet = self.wbook.add_sheet('scrapy')
        self._headers_not_written = True
        self.fields_to_export = list()
        self.row = 0

    def finish_exporting(self):
        self.wbook.save(self.file)

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        fields = self._get_serialized_fields(item)
        for col, v in enumerate(x for _, x in fields):
            print(self.row, col, str(v))
            self.wsheet.write(self.row, col, str(v))
        self.row += 1

    def _write_headers_and_set_fields_to_export(self, item):
        if not self.fields_to_export:
            if isinstance(item, dict):
                self.fields_to_export = list(item.keys())
            else:
                self.fields_to_export = list(item.fields.keys())
        for column, v in enumerate(self.fields_to_export):
            self.wsheet.write(self.row, column, v)
        self.row += 1

    # 启用新定义的Exporter类\
    FEED_EXPORTERS = {'excel': 'example.excel_exporter.ExcelExporter'}


ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.1
# 并发线程数量
CONCURRENT_REQUESTS = 100
# 超时时间为10s
DOWNLOAD_TIMEOUT = 10
# 禁用cookies
COOKIES_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'BQG.middlewares.RandomUserAgentMiddlware': 543,
    #将middlewares中定义RandomUserAgentMiddlware添加到这里;
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    #需要将scrapy默认的置为None不调用
}

##########################################################
'''
# PROXIES = [{'ip_port': '111.11.228.75:80', 'user_pass': ''}]

# 可在spider中扩展设置
custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'autospider.pipelines.DcdAppPipeline': 300,
        },
        # 设置log日志
        'LOG_LEVEL':'DEBUG',
        'LOG_FILE':'./././Log/dcdapp_log.log'
    }

# 或者
ITEM_PIPELINES = {
    'BQG.pipelines.PipelineCheck': 100,
    # 'BQG.pipelines.PipelineToSql': 200,
    # 'BQG.pipelines.PipelineToSqlTwisted': 200,
    # 'BQG.pipelines.PipelineToJson': 300,
    # 'BQG.pipelines.PipelineToJsonExp': 300,
    # 'BQG.pipelines.PipelineToTxt': 300,
    'BQG.pipelines.PipelineToCsv': 300,
    'BQG.pipelines.Pipeline2Csv': 300,
}

# 设置默认导出组件
FEED_EXPORTERS_BASE = {
    'json': 'scrapy.exporters.JsonItemExporter',
    'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
    'jl': 'scrapy.exporters.JsonLinesItemExporter',
    'csv': 'scrapy.exporters.CsvItemExporter',
    'xml': 'scrapy.exporters.XmlItemExporter',
    'marshal': 'scrapy.exporters.MarshalItemExporter',
    'pickle': 'scrapy.exporters.PickleItemExporter',
}

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

# Scrapy settings for BQG project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'BQG (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.25
#DOWNLOAD_DELAY = 3

# The download delay setting will honor only one of:
# 决定最大值
# 下面两个二选一，一个是针对域名设置并发，一个是针对IP设置并发
# CONCURRENT_REQUESTS_PER_IP = 10
# CONCURRENT_REQUESTS_PER_DOMAIN = 10

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'BQG.middlewares.BqgSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'BQG.middlewares.BqgDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'BQG.pipelines.BqgPipeline': 300,
#    'BQG.pipelines.BqgJsonPipeline': 300,
#    'BQG.pipelines.BqgSQLPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
