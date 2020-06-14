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
#LastEditTime : 2020-06-14 23:07:19
# author:      he.zhiming
'''

import logging
import logging.config
from datetime import datetime

style = {
    'standard':
    '[%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(filename)s->%(funcName)s:%(lineno)d]\t[%(levelname)s]\t[%(message)s]',
    'simple': '[%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
}

_levelToName = {
    50: 'critical',
    40: 'error',
    30: 'warning',
    20: 'info',
    10: 'debug',
    0: 'NOTSET',
}


def _make_filename(level=10):
    result = _levelToName.get(level)
    if result is not None:
        _level = result
    else:
        _level = level

    return datetime.today().strftime('%Y%m%d') + '-' + _level + '.log'


class log(object):
    def __init__(self, level=logging.DEBUG, logger=__name__):
        self.level = level
        self.filename = _make_filename(level=self.level)
        # #定义字典
        self.conf_dic = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': style['standard']
                },
                'simple': {
                    'format': style['standard']
                },
            },
            'filters': {},
            'handlers': {
                'console': {
                    'level': self.level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
                'default': {
                    'level': self.level,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    'filename': self.filename,
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'encoding': 'utf-8',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['default', 'console'],
                    'level': self.level,
                    'propagate': True,
                },
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
        # #定义字典完毕        logging.config.dictConfig(self.conf_dic)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)
        # 日志的5个级别对应以下的五个函数

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warn = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical

    def print(self, *args):
        commad = getattr(self.logger, _levelToName.get(self.level))
        [commad(item) for item in list(args)]

    @classmethod
    def setFormat(cls):
        logging.basicConfig(format=style['simple'])


if __name__ == "__main__":
    pass
