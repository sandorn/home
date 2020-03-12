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
@LastEditTime: 2020-03-10 14:14:35
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
        'json': 'stockstar.settings.CustomJsonLinesItemExporter',
    }


class ExcelItemExporter(BaseItemExporter):
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
    FEED_EXPORTERS = {
        'excel': 'stockstar.settings.ExcelItemExporter',
    }


ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0.1
# 爬虫线程数量
CONCURRENT_REQUESTS = 64
# 禁用cookies
COOKIES_ENABLED = False

PROXIES = [
    {'ip_port': '111.11.228.75:80', 'user_pass': ''}
]
DOWNLOADER_MIDDLEWARES = {
    # 取消原有的useragent中间件
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'BQG.middlewares.RandomUserAgentMiddleware': 543,  # 使用fake-useragent库
}
RANDOM_UA_TYPE = 'random'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 指定客户端浏览器可以支持的web服务器返回内容压缩编码类型
    'Accept-Encoding': 'gzip, deflate, br',
    # 指定HTTP客户端浏览器用来展示返回信息所优先选择的语言。
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.6,en;q=0.4',
    # 浏览器可以接受的字符编码集
    'Accept-Charset': 'gb2312,utf-8;q=0.7,*;q=0.7',
    # 表示是否需要持久连接  'keep-alive','close'
    'Connection': 'close',
    # 显示此HTTP连接的Keep-Alive时间    'Keep-Alive': '300',
    # 请求的web服务器域名地址    'Host': 'www.baidu.com',
}


'''
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

#可在spider中扩展设置
custom_settings = {
        # 设置管道下载
        'ITEM_PIPELINES': {
            'autospider.pipelines.DcdAppPipeline': 300,
        },
        # 设置log日志
        'LOG_LEVEL':'DEBUG',
        'LOG_FILE':'./././Log/dcdapp_log.log'
    }
'''
# 设置默认导出组件
'''
FEED_EXPORTERS_BASE = {
    'json': 'scrapy.exporters.JsonItemExporter',
    'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
    'jl': 'scrapy.exporters.JsonLinesItemExporter',
    'csv': 'scrapy.exporters.CsvItemExporter',
    'xml': 'scrapy.exporters.XmlItemExporter',
    'marshal': 'scrapy.exporters.MarshalItemExporter',
    'pickle': 'scrapy.exporters.PickleItemExporter',
}
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
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

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
