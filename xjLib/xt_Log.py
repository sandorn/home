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
from logging.config import dictConfig
from time import perf_counter
from typing import Any

from wrapt import decorator
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


def obj_to_str(obj):
    """将对象转换为字符串, 递归处理,无用暂存"""
    if isinstance(obj, (list, tuple, set)):
        return ", ".join(map(obj_to_str, obj))
    elif isinstance(obj, dict):
        return ", ".join(f"{k}: {obj_to_str(v)}" for k, v in obj.items())
    elif isinstance(obj, str):
        return re.sub(r"<([^<>]+)>", r"\<\1\>", obj)
    else:
        return str(obj)


def create_basemsg(func):
    code = getattr(func, "__code__")
    _filename = code.co_filename
    _f_lineno = code.co_firstlineno
    return f"[{_filename}@{_f_lineno}|{func.__name__}]"


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
                    "maxBytes": 1024 * 1024 * 5 * 10,
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

    def __getattr__(self, attr):
        if attr in logging._levelToName:
            return getattr(self.logger, attr)
        raise AttributeError(f"Object[{type(self).__name__}] has no attribute '{attr}'")

    def __call__(self, *args, **kwargs) -> Any:
        return [
            getattr(self.logger, LevelDict[self.level])(arg, **kwargs)
            for arg in list(args)
        ]

    def print(self, *args, **kwargs):
        return [
            getattr(self.logger, LevelDict[self.level])(arg, **kwargs)
            for arg in list(args)
        ]


class Log_Catch_Wrapt(LogCls):
    "日志及异常装饰器，打印并记录函数的入参、出参、耗时、异常信息"

    def __init__(self, level=10, logname=__name__, pyfile=None):
        super().__init__(level=level, logname=logname, pyfile=pyfile)

    @decorator
    def __call__(self, wrapped, instance, args, kwargs):
        self.blm = create_basemsg(wrapped)
        self.print(f"{self.blm } | <Args:{args!r}> | <Kwargs:{kwargs!r}>")
        duration = perf_counter()
        try:
            result = wrapped(*args, **kwargs)
            self.print(
                f"{self.blm } | <Result:{result!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
            )
            return result
        except Exception as err:
            self.print(
                err_str := f"{self.blm} | Log_Catch_Wrapt Exception | <Raise:{err!r}>"
            )
            return err_str


@decorator
def log_catch_decor(func, instance, args, kwargs):
    """日志及异常装饰器，打印并记录函数的入参、出参、耗时、异常信息"""
    logger = LogCls()
    blm = create_basemsg(func)
    logger(f"{blm} | <Args:{args!r}> | <Kwargs:{kwargs!r}>")

    duration = perf_counter()
    try:
        result = func(*args, **kwargs)
        logger(
            f"{blm} | <Result:{result!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
        )
        return result
    except Exception as err:
        logger(err_str := f"{blm} | LCD Exception | <Raise:{err!r}>")
        return err_str


@decorator
def log_decor(func, instance, args, kwargs):
    """日志装饰器，打印并记录函数的入参、出参、耗时"""

    logger = LogCls()
    blm = create_basemsg(func)
    logger(f"{blm} | <Args:{args!r}> | <Kwargs:{kwargs!r}>")

    duration = perf_counter()
    result = func(*args, **kwargs)

    logger(
        f"{blm} | <Result:{result!r}> | <Time-Consuming:{perf_counter() - duration:.4f}s>"
    )
    return result


if __name__ == "__main__":

    @log_catch_decor  # log_decor
    def test1(*args):
        return 9 / 0

    @Log_Catch_Wrapt()
    def test2(*args):
        return 9 / 0

    # test1()
    test2()
