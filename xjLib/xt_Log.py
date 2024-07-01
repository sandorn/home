# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-06-18 10:20:12
FilePath     : /CODE/xjLib/xt_Log.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import inspect
import logging
import logging.config
import re
from datetime import datetime
from functools import wraps
from time import perf_counter

from xt_Singleon import Singleton_Mixin

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


class LogCls(Singleton_Mixin):
    def __init__(self, level=logging.DEBUG, logger=__name__, pyfile=None):
        if pyfile is None:
            frame = inspect.currentframe().f_back
            _func_line = frame.f_lineno
            _pyfile = frame.f_code.co_filename.split('\\')[-1].split('.')[0]
        pyfile = pyfile or _pyfile

        self.level = level
        self.filename = f'{pyfile}＆{datetime.now().strftime('%Y%m%d')}-{_levelToName[level]}.log'

        # #定义字典
        self.conf_dic = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {'format': standard_format},
                'simple': {'format': simple_format},
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
        logging.config.dictConfig(self.conf_dic)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)

    def __getitem__(self, item):
        return getattr(self.logger, _levelToName[self.level])

    def __getattr__(self, item):
        return getattr(self.logger, _levelToName[self.level])

    def print(self, *args):
        "打印日志，未能取得调用者的文件名和行号"
        commad = getattr(self.logger, _levelToName[self.level])
        [commad(item) for item in list(args)]


def log_decorator(func):
    frame = inspect.currentframe().f_back
    func_line = frame.f_lineno
    _filename = frame.f_code.co_filename
    _pyfile = _filename.split('\\')[-1].split('.')[0]
    logger = LogCls(pyfile=_pyfile)

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = re.sub(r'<([^<>]+)>', r'\<\1\>', str(args))  # 使用正则表达式替换<任意内容>为\<任意内容>
        kwargs_str = re.sub(r'<([^<>]+)>', r'\<\1\>', str(kwargs))
        logger.debug(f'[{_filename}|{func.__module__}.{func.__name__}:{func_line}] </> args: {args_str}, kwargs:{kwargs_str}</>')
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            result_str = re.sub(r'<([^<>]+)>', r'\<\1\>', str(result))
            end = perf_counter()
            duration = end - start
            logger.debug(f'[{_filename}|{func.__module__}.{func.__name__}:{func_line}] </> 返回结果：{result_str}, 耗时：{duration:4f}s</>')
            return result
        except Exception as e:
            logger.debug('exception', f'[{_filename}|{func.__module__}.{func.__name__}:{func_line}] </> 报错:{e}</>')

    return wrapper


if __name__ == '__main__':

    @log_decorator
    def test2(a, b=1):
        return a / b

    test2(1)
