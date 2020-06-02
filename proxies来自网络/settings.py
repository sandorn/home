# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:50:34
@LastEditors: Even.Sand
@LastEditTime: 2020-03-23 19:53:26
'''
import logging

MAX_SCORE = 50  # 代理ip初始分数

# 下面这一部分是log.py的内容，是用来控制日志文件的
LOG_LEVEL = logging.INFO  # 控制日志文件报错级别
'''
报错级别一共5种（从上到下级别依次递增）
logger.debug("")
logger.info("")
logger.warning("")
logger.error("")
logger.critical("")

如果设置报错级别为INFO，那么就不会报debug的错误
'''
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 日志内容格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 日志内容的时间部分格式（也就是”年-月-日 时:分:秒“）
LOG_FILENAME = 'log.log'  # 要把日志文件放在哪，就放在本目录下log.log文件

TEST_TIMEOUT = 20  # 这个是requess访问链接设置的超时时间

# 因为我把数据放入了mongodb数据库，所以这里配置的是mongodb数据库连接信息
MONGO_URL = 'mongodb:#127.0.0.1:27017'

'''
这几个是分别爬取几个网站上代理ip的具体爬虫路径
'''
SPIDERS = [

    'proxy_spiders.ip66Spider',
    'proxy_spiders.KuaidailiSpider',
    'proxy_spiders.ProxylistplusSpider',
    'proxy_spiders.XiciSpider'
]
# 这个是多长时间爬取一次代理ip来使用
RUN_SPIDERS_INTERVEL = 12
# 这个是最多开多少协程来判断ip是否可用
TEST_PROXIES_ASYNC_COUNT = 10
# 这个是多少时间更新一次数据库内ip信息，因为代理ip存活时间有限
TEST_PROXIES_INTERVAL = 2
