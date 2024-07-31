# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2024-07-18 14:39:12
FilePath     : /CODE/xjLib/xt_log.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import inspect
import logging
import logging.config
import re
from datetime import datetime
from functools import wraps

from xt_singleon import SingletonMixin
from xt_time import fn_timer

standard_format = "[%(asctime)s][%(threadName)s:%(thread)d]\t%(message)s"
simple_format = "[%(asctime)s]\t%(message)s"

LevelDict = {
    50: "critical",
    40: "error",
    30: "warning",
    20: "info",
    10: "debug",
    0: "notset",
}


class LogCls(SingletonMixin):
    def __init__(self, level=logging.DEBUG, logger=__name__, pyfile=None):
        pyfile = pyfile or "MyLog"
        self.level = level
        self.filename = f'{pyfile}--{datetime.now().strftime('%Y%m%d')}.log'
        # 定义的logging配置字典
        self.conf_dic = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {"format": standard_format},
                "simple": {"format": simple_format},
            },
            "filters": {},
            "handlers": {
                # 打印到终端的日志
                "console": {
                    "level": self.level,
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                },  # 打印到屏幕
                # 打印到文件的日志,收集DEBUG及以上的日志
                "writelog": {
                    "level": self.level,
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "standard",
                    "filename": self.filename,
                    "maxBytes": 1024 * 1024 * 5,
                    "backupCount": 5,
                    "encoding": "utf-8",
                },  # 保存到文件  # 日志文件  # 日志大小 5M  # 日志文件的编码，再也不用担心中文log乱码了
            },
            "loggers": {
                # logging.getLogger(__name__)拿到的logger配置
                "": {
                    "handlers": ["writelog", "console"],
                    "level": self.level,
                    "propagate": True,
                },  # log数据既写入文件又打印到屏幕  # 向上（更高level的logger）传递
                "writelog": {
                    "handlers": ["writelog"],
                    "level": self.level,
                    "propagate": True,
                },
                "console": {
                    "handlers": ["console"],
                    "level": self.level,
                    "propagate": True,
                },
            },
        }
        logging.config.dictConfig(self.conf_dic)
        self.logger = logging.getLogger(logger)

    def __getitem__(self, item):
        return getattr(self.logger, LevelDict[self.level])

    def __getattr__(self, item):
        return getattr(self.logger, LevelDict[self.level])

    def print(self, *args):
        return [
            getattr(self.logger, LevelDict[self.level])(item) for item in list(args)
        ]

    def __call__(self, *args, level=None):
        if level is None:
            level = self.level
        return [getattr(self.logger, LevelDict[level])(item) for item in list(args)]


def get_fn_fileinfo(callfn):
    # callfn = inspect.currentframe()
    _filename = _f_lineno = "None"
    if callfn is not None:
        frame = callfn.f_back
        if frame is not None:
            _f_lineno = frame.f_lineno
            _filename = frame.f_code.co_filename.split("\\")[-1].split(".")[0]
    return _filename, _f_lineno


def format_args_and_keywords(args, kwargs):
    args_str = kwargs_str = ""

    if args:
        args_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(args))
    if kwargs:
        kwargs_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(kwargs))

    return args_str, kwargs_str


def log_decorator(func):
    _filename, _f_lineno = get_fn_fileinfo(inspect.currentframe())
    logger = LogCls(pyfile="MyLog")

    @fn_timer
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = kwargs_str = format_args_and_keywords(args, kwargs)

        logger(
            f"[{_filename}|fn:{func.__name__}@{_f_lineno}]|<参数：{args_str} | 关键字参数：{kwargs_str}>"
        )
        try:
            result = func(*args, **kwargs)
            result_str = re.sub(r"<([^<>]+)>", r"\<\1\>", str(result))
            logger(
                f"[{_filename}|fn:{func.__name__}@{_f_lineno}]|<返回结果：{result_str} >"
            )
            return result
        except Exception as e:
            logger(
                "exception", f"[{_filename}|fn:{func.__name__}@{_f_lineno}]|<报错：{e}>"
            )

    return wrapper


if __name__ == "__main__":

    @log_decorator
    def test2(a, b=1):
        return a / b

    test2(1)
