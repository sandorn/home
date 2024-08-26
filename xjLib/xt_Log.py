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

import logging
import re
from datetime import datetime
from functools import wraps
from inspect import currentframe
from logging.config import dictConfig
from time import perf_counter

from xt_singleon import SingletonMixin

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
    def __init__(self, level=10, logname=__name__, pyfile=None):
        pyfile = pyfile or "XtLog"
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
            "handlers": {
                "console": {
                    "level": self.level,
                    "class": "logging.StreamHandler",  # 打印到屏幕
                    "formatter": "simple",
                },
                "writelog": {
                    "level": self.level,
                    "class": "logging.handlers.RotatingFileHandler",  # 打印到文件
                    "formatter": "standard",
                    "filename": self.filename,
                    "maxBytes": 1024 * 1024 * 5,
                    "backupCount": 5,
                    "encoding": "utf-8",
                },  # 保存到文件  # 日志文件  # 日志大小 5M  # 日志文件的编码
            },
            "loggers": {
                # logging.getLogger(__name__)拿到的logger配置
                "": {
                    "handlers": ["writelog", "console"],
                    "level": self.level,
                    "propagate": False,  # 向上级-父Logger传递
                },  # log数据既写入文件又打印到屏幕
            },
        }

        dictConfig(self.conf_dic)
        self.logger = logging.getLogger(logname)

    def __getattr__(self, item):
        if item in logging._levelToName:
            return getattr(self.logger, item)
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{item}'"
        )

    def __call__(self, *args):
        return [
            getattr(self.logger, LevelDict[self.level])(item) for item in list(args)
        ]


def get_fn_fileinfo(callfn):
    _filename = _f_lineno = "None"
    if callfn:
        frame = callfn.f_back
        if frame:
            _f_lineno = frame.f_lineno
            _filename = frame.f_code.co_filename.split("\\")[-1].split(".")[0]
    return _filename, _f_lineno


def format_strings(obj):
    if isinstance(obj, (list, tuple, set)):
        return ", ".join(map(format_strings, obj))
    elif isinstance(obj, dict):
        return ", ".join(f"{k}: {format_strings(v)}" for k, v in obj.items())
    elif isinstance(obj, str):
        return re.sub(r"<([^<>]+)>", r"\<\1\>", obj)
    else:
        return str(obj)


def log_decorator(func):
    _filename, _f_lineno = get_fn_fileinfo(currentframe())
    logger = LogCls(pyfile="XtLog")

    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = format_strings(args)
        kwargs_str = format_strings(kwargs)
        base_log_msg = f"[{_filename}|fn:{func.__name__}@{_f_lineno}]"

        logger(f"{base_log_msg}|<参数：{args_str} | 关键字参数：{kwargs_str}>")
        duration = perf_counter()

        try:
            result = func(*args, **kwargs)
            result_str = format_strings(str(result))
            duration = perf_counter() - duration
            logger(f"{base_log_msg}|<返回结果：{result_str} >|<耗时：{duration:.4f}s>")
            return result
        except Exception as e:
            logger("exception", f"{base_log_msg}|<报错：{e}>")

    return wrapper


if __name__ == "__main__":

    @log_decorator
    def test2(a, b=1):
        return a / b

    test2(1)
