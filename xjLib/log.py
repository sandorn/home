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
#LastEditTime : 2020-05-30 18:11:25
# author:      he.zhiming
'''

import logging
import logging.config
import os
from datetime import datetime

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][%(name)s][%(filename)s->%(funcName)s:%(lineno)d]\t[%(levelname)s]\t[%(message)s]'  # 其中name为getlogger指定的名字
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


class _logger(object):
    def __init__(self, level=logging.DEBUG, logger=__name__):
        self.level = level
        self.log_name = _make_filename(log_level=self.level)
        # #定义字典
        self.conf_dic = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {'standard': {'format': standard_format}, 'simple': {'format': simple_format},},
            'filters': {},
            'handlers': {
                # 打印到终端的日志
                'console': {'level': self.level, 'class': 'logging.StreamHandler', 'formatter': 'simple',},  # 打印到屏幕
                # 打印到文件的日志,收集DEBUG及以上的日志
                'default': {'level': self.level, 'class': 'logging.handlers.RotatingFileHandler', 'formatter': 'standard', 'filename': self.log_name, 'maxBytes': 1024 * 1024 * 5, 'backupCount': 5, 'encoding': 'utf-8',},  # 保存到文件  # 日志文件  # 日志大小 5M  # 日志文件的编码，再也不用担心中文log乱码了
            },
            'loggers': {
                # logging.getLogger(__name__)拿到的logger配置
                '': {'handlers': ['default', 'console'], 'level': self.level, 'propagate': True,},  # log数据既写入文件又打印到屏幕  # 向上（更高level的logger）传递
                'default': {'handlers': ['default'], 'level': self.level, 'propagate': True,},
                'console': {'handlers': ['console'], 'level': self.level, 'propagate': True,},
            },
        }
        # #定义字典完毕
        logging.config.dictConfig(self.conf_dic)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)

    def print(self, *args):
        # listargs = (list(args))
        commad = getattr(self.logger, _levelToName.get(self.level))
        [commad(item) for item in list(args)]


def log(level=logging.DEBUG, logger=__name__):
    newlog = _logger(level=level, logger=logger)
    return newlog


def logs():
    logging.basicConfig(level=logging.DEBUG, format=simple_format)


class MyLog(object):
    def __init__(self, name=__name__, showlevel=logging.DEBUG, writelevel=logging.WARNING):  # 类MyLog的构造函数
        self.logger = logging.getLogger(name)  # 返回一个特定名字的日志
        self.logger.setLevel(showlevel)  # 对显示的日志信息设置一个阈值低于DEBUG级别的不显示
        logFile = _make_filename(log_level=writelevel)  # 日志文件名
        std_formatter = logging.Formatter(standard_format)
        smp_formatter = logging.Formatter(simple_format)
        '''日志显示到屏幕上并输出到日志文件内'''
        logHand = logging.FileHandler(logFile)  # 输出日志文件，文件名是logFile
        logHand.setFormatter(std_formatter)  # 为logHand以formatter设置格式
        logHand.setLevel(writelevel)  # 只有错误才被记录到logfile中

        logHandSt = logging.StreamHandler()  # class logging.StreamHandler(stream=None)
        # 返回StreamHandler类的实例，如果stream被确定，使用该stream作为日志输出，反之，使用
        # sys.stderr
        logHandSt.setFormatter(smp_formatter)  # 为logHandSt以formatter设置格式

        self.logger.addHandler(logHand)  # 添加特定的handler logHand到日志文件logger中
        self.logger.addHandler(logHandSt)  # 添加特定的handler logHandSt到日志文件logger中
        '''日志的5个级别对应以下的五个函数'''

    def debug(self, msg):
        self.logger.debug(msg)

    def print(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def setlevel(self, name, level):
        logging.getLogger(name).setLevel(level)


def decoLog(func):
    '''
    程序出错日志记录装饰器
    :param func: 当前执行的函数
    :return: 返回日志
    '''

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            log().print(err)

    return wrapper


if __name__ == "__main__":
    log = log()
    log.print(999)
    mylog = MyLog()
    mylog.print(888)
