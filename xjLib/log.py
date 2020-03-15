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
@LastEditors: Even.Sand
@LastEditTime: 2020-03-13 11:47:47
# author:      he.zhiming
'''

import logging
import logging.config
import os
from datetime import datetime

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s->%(funcName)s:%(lineno)d]' \
    '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字
simple_format = '[%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    CRITICAL: 'critical',
    ERROR: 'error',
    WARNING: 'warn',
    INFO: 'info',
    DEBUG: 'debug',
    NOTSET: 'NOTSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}


def _make_filename(filename='.log', log_level=10):
    result = _levelToName.get(log_level)
    if result is not None:
        _level = result
    else:
        _level = log_level

    date_str = datetime.today().strftime('%Y%m%d')
    pidstr = '-' or str(os.getpid())
    return ''.join((date_str, '-', pidstr, '-', _level, '', filename,))


class _logDic(object):
    def __init__(self, level=logging.DEBUG, logger=__name__):
        self.level = level
        self.log_name = _make_filename(log_level=self.level)
        # #定义字典
        self.DIC = {
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
                    'class': 'logging.StreamHandler',  # 打印到屏幕
                    'formatter': 'simple',
                },
                # 打印到文件的日志,收集DEBUG及以上的日志
                'default': {
                    'level': self.level,
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                    'formatter': 'standard',
                    'filename': self.log_name,  # 日志文件
                    'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                    'backupCount': 5,
                    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                },
            },
            'loggers': {
                # logging.getLogger(__name__)拿到的logger配置
                '': {
                    'handlers': ['default', 'console'],  # log数据既写入文件又打印到屏幕
                    'level': self.level,
                    'propagate': True,  # 向上（更高level的logger）传递
                },
                'def': {
                    'handlers': ['default'],
                    'level': self.level,
                    'propagate': True,
                },
                'con': {
                    'handlers': ['console'],
                    'level': self.level,
                    'propagate': True,
                },
            }
        }
        # #定义字典完毕
        logging.config.dictConfig(self.DIC)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)

    def p(self, *args):
        #listargs = (list(args))
        commad = getattr(self.logger, _levelToName.get(self.level))
        [commad(item)for item in list(args)]


def log(level=logging.DEBUG, logger=__name__):
    newlog = _logDic(level=level, logger=logger)
    return newlog


def logs():
    logging.basicConfig(level=logging.DEBUG, format=simple_format)
    # logging.basicConfig函数对日志的输出格式及方式做相关配置
