# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-17 17:25:15
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

standard_format = "[%(asctime)s][%(threadName)s:%(thread)d]\t%(message)s"  # 其中name为getlogger指定的名字
simple_format = "[%(asctime)s]\t%(message)s"

_levelToName = {50: "critical", 40: "error", 30: "warning", 20: "info", 10: "debug", 0: "NOTSET"}


class LogCls(Singleton_Mixin):
    def __init__(self, level=logging.DEBUG, logger=__name__, pyfile=None):
        pyfile = pyfile or "MyLog"
        self.level = level
        self.filename = f'{pyfile}--{datetime.now().strftime('%Y%m%d')}.log'

        # #定义字典
        self.conf_dic = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"standard": {"format": standard_format}, "simple": {"format": simple_format}},
            "filters": {},
            "handlers": {
                # 打印到终端的日志
                "console": {"level": self.level, "class": "logging.StreamHandler", "formatter": "simple"},  # 打印到屏幕
                # 打印到文件的日志,收集DEBUG及以上的日志
                "writelog": {"level": self.level, "class": "logging.handlers.RotatingFileHandler", "formatter": "standard", "filename": self.filename, "maxBytes": 1024 * 1024 * 5, "backupCount": 5, "encoding": "utf-8"},  # 保存到文件  # 日志文件  # 日志大小 5M  # 日志文件的编码，再也不用担心中文log乱码了
            },
            "loggers": {
                # logging.getLogger(__name__)拿到的logger配置
                "": {"handlers": ["writelog", "console"], "level": self.level, "propagate": True},  # log数据既写入文件又打印到屏幕  # 向上（更高level的logger）传递
                "writelog": {"handlers": ["writelog"], "level": self.level, "propagate": True},
                "console": {"handlers": ["console"], "level": self.level, "propagate": True},
            },
        }
        logging.config.dictConfig(self.conf_dic)  # 导入上面定义的logging配置
        self.logger = logging.getLogger(logger)

    def __getitem__(self, item):
        return getattr(self.logger, _levelToName[self.level])

    def __getattr__(self, item):
        return getattr(self.logger, _levelToName[self.level])

    def print(self, *args):
        "打印日志"
        return [getattr(self.logger, _levelToName[self.level])(item) for item in list(args)]


def log_decorator(func):
    frame = inspect.currentframe().f_back
    _func_line = frame.f_lineno
    _filename = frame.f_code.co_filename.split("\\")[-1].split(".")[0]
    logger = LogCls(pyfile="MyLog")

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(args))  # 使用正则表达式替换<任意内容>为\<任意内容>
        kwargs_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(kwargs))
        logger.print(f"[{_filename}|fn:{func.__name__}@{_func_line}]|<args:{args_str} | kwargs:{kwargs_str}>")
        start = perf_counter()
        try:
            result = func(*args, **kwargs)
            result_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(result))
            duration = perf_counter() - start
            logger.print(f"[{_filename}|fn:{func.__name__}@{_func_line}]|<返回结果：{result_str} | 耗时：{duration:4f}s>")
            return result
        except Exception as e:
            logger.print("exception", f"[{_filename}|fn:{func.__name__}@{_func_line}]|<报错:{e}>")

    return wrapper


if __name__ == "__main__":

    @log_decorator
    def test2(a, b=1):
        return a / b

    test2(1)
