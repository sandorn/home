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
@LastEditTime: 2019-05-28 13:53:18
# author:      he.zhiming
'''

import logging
import os
from datetime import datetime
import logging.config

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
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
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


def _make_filename(filename='py.log', log_level=10):
    result = _levelToName.get(log_level)
    if result is not None:
        _level = result
    else:
        _level = log_level
    #_level = _levelToName[log_level]

    date_str = datetime.today().strftime('%Y%m%d')
    pidstr = str(os.getpid())
    return ''.join((date_str, '-', pidstr, '-', _level, '-', filename,))


class _class_log(object):
    # #封装后的logging
    def __init__(self, level=logging.DEBUG, logger=None):
        self.level = level
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(self.level)
        self.standard_format = logging.Formatter(standard_format)
        self.simple_format = logging.Formatter(simple_format)

        self.fhinit()
        self.chinit()

    def fhinit(self):
        self.log_name = _make_filename(log_level=self.level)
        self.fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        # fh.setLevel(level)
        # 定义handler的输出格式
        self.fh.setFormatter(self.standard_format)
        # 给logger添加handler
        self.logger.addHandler(self.fh)

    def chinit(self):
        self.ch = logging.StreamHandler()
        self.ch.setFormatter(self.simple_format)
        self.logger.addHandler(self.ch)

    def __del__(self):
        # self.logger.removeHandler(ch)
        # 关闭打开的文件
        self.fh.close()
        self.ch.close()


# @ 第二种方法
class _cls_log(object):
    # #封装后的logging
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
                    'formatter': 'simple'
                },
                # 打印到文件的日志,收集DEBUG及以上的日志
                'default': {
                    'level': self.level,
                    'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                    'formatter': 'standard',
                    'filename': self.log_name,  # 日志文件
                    'maxBytes': 1024 * 1024 * 5 * 10,  # 日志大小 50M
                    'backupCount': 5,
                    'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                },
            },
            'loggers': {
                # logging.getLogger(__name__)拿到的logger配置
                '': {
                    'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                    'level': self.level,
                    'propagate': True,  # 向上（更高level的logger）传递
                },
                'file': {
                    'handlers': ['default'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                    'level': self.level,
                    'propagate': True,  # 向上（更高level的logger）传递
                },
            },
        }
        # #定义字典完毕
        logging.config.dictConfig(self.DIC)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)


def log(level=logging.DEBUG):
    if level in [0, 10, 20, 30, 40, 50]:
        newlog = _class_log(level=level)
    else:
        newlog = _class_log()
    return newlog.logger


def logd(level=logging.DEBUG, logger=__name__):
    newlog = _cls_log(level=level, logger=logger)
    return newlog.logger  # 生成一个log实例


def logc():
    logging.basicConfig(level=logging.DEBUG, format=simple_format)

    # logging.basicConfig函数对日志的输出格式及方式做相关配置


def logf():
    filename = _make_filename(log_level=20)
    logging.basicConfig(level=logging.DEBUG,  # 日志级别
                        filename=filename,
                        filemode='a',  # 覆写w和追加a，默认追加
                        format=standard_format  # 日志格式
                        )
