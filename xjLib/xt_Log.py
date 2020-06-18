# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-28 09:23:00
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-18 15:27:42
# author:      he.zhiming
'''

import logging
import logging.config
from datetime import datetime

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(filename)s->%(funcName)s:%(lineno)d]\t[%(levelname)s]\t[%(message)s]'  # 其中name为getlogger指定的名字
simple_format = '[%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

_levelToName = {
    50: 'critical',
    40: 'error',
    30: 'warning',
    20: 'info',
    10: 'debug',
    0: 'NOTSET',
}


class log(object):
    def __init__(self, level=logging.DEBUG, logger=__name__):
        self.level = level
        self.filename = datetime.today().strftime(
            '%Y%m%d') + '-' + _levelToName.get(level) + '.log'
        # #定义字典
        self.conf_dic = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': standard_format
                },
                'simple': {
                    'format': simple_format
                },
            },
            'filters': {},
            'handlers': {
                # 打印到终端的日志
                'console': {
                    'level': self.level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },  # 打印到屏幕
                # 打印到文件的日志,收集DEBUG及以上的日志
                'default': {
                    'level': self.level,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'filename': self.filename,
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'encoding': 'utf-8',
                },  # 保存到文件  # 日志文件  # 日志大小 5M  # 日志文件的编码，再也不用担心中文log乱码了
            },
            'loggers': {
                # logging.getLogger(__name__)拿到的logger配置
                '': {
                    'handlers': ['default', 'console'],
                    'level': self.level,
                    'propagate': True,
                },  # log数据既写入文件又打印到屏幕  # 向上（更高level的logger）传递
                'default': {
                    'handlers': ['default'],
                    'level': self.level,
                    'propagate': True,
                },
                'console': {
                    'handlers': ['console'],
                    'level': self.level,
                    'propagate': True,
                },
            },
        }
        # #定义字典完毕
        logging.config.dictConfig(self.conf_dic)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warn = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical

    def print(self, *args):
        # listargs = (list(args))
        commad = getattr(self.logger, _levelToName.get(self.level))
        [commad(item) for item in list(args)]


if __name__ == "__main__":
    log = log()
    log.print(999)
