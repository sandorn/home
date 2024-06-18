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
import traceback
from datetime import datetime
from functools import wraps
from time import perf_counter

from xt_Thread import Singleton_Mixin

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
        pyfile = pyfile or traceback.extract_stack()[-2].filename
        self.level = level
        self.filename = pyfile + '-' + datetime.now().strftime('%Y%m%d') + '-' + _levelToName[level] + '.log'
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

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warn = self.logger.warning
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical

    def print(self, *args):
        commad = getattr(self.logger, _levelToName[self.level])
        [commad(item) for item in list(args)]


def __handle_result(result):
    if result is None:
        return ''
    elif isinstance(result, str):
        return result
    elif isinstance(result, tuple):
        return list(result)
    else:
        return str(result)


def log_wraps(func):
    @wraps(func)
    def wrapper(*args, **kw):
        # 处理结果

        logger = LogCls()
        dicc = {}
        dinp = {}
        varnames = func.__code__.co_varnames
        deft = func.__defaults__
        if deft is None:
            deft = ()

        for i in range(len(args)):
            dinp[varnames[i]] = str(args[i])
        for j in range(len(deft)):
            dinp[varnames[i + j + 1]] = str(deft[j])
        for i, j in kw.items():
            dinp[i] = str(j)

        try:
            result = func(*args, **kw)
        except Exception as e:
            result = 'err:' + str(e)
        finally:
            dretrun = __handle_result(result)
            dicc['run_input'] = dinp
            dicc['run_return'] = dretrun
            logger.print(dicc)

        return result

    return wrapper


def log_decorator(func):
    frame = inspect.currentframe().f_back
    func_line = frame.f_lineno
    logger = LogCls(pyfile=frame.f_code.co_filename)

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = re.sub(r'<([^<>]+)>', r'\<\1\>', str(args))  # 使用正则表达式替换<任意内容>为\<任意内容>
        kwargs_str = re.sub(r'<([^<>]+)>', r'\<\1\>', str(kwargs))
        logger.print(f'{func.__qualname__}:{func.__name__}:{func_line} |</> args: {args_str}, kwargs:{kwargs_str}</>')
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            result_str = re.sub(r'<([^<>]+)>', r'\<\1\>', str(result))
            end = perf_counter()
            duration = end - start
            logger.print(f'{func.__qualname__}:{func.__name__}:{func_line} |</> 返回结果：{result_str}, 耗时：{duration:4f}s</>')
            return result
        except Exception as e:
            logger.print('exception', f'{func.__qualname__}:{func.__name__}:{func_line} |</> 报错:{e}')

    return wrapper
