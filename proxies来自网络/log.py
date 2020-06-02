# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:51:00
@LastEditors: Even.Sand
@LastEditTime: 2020-04-17 18:22:16
'''
import logging
import sys
import settings


class Logger(object):

    def __init__(self):
        self._logger = logging.getLogger()  # 得到一个日志处理对象
        # 传参数，告诉它写入日志内容格式
        self.formatter = logging.Formatter(
            fmt=settings.LOG_FMT, datefmt=settings.LOG_DATEFMT)
        # 把要写入的日志加入句柄里面，到时候会输出到文件内保存
        self._logger.addHandler(self._get_file_handler(settings.LOG_FILENAME))
        # 把要写入的日志加入句柄里面，到时候会输出到控制台查看
        self._logger.addHandler(self._get_console_handler())
        # 设置写入日志级别
        self._logger.setLevel(settings.LOG_LEVEL)

    def _get_file_handler(self, filename):  # 设置一下要往那个文件里面写，和编码问题
        filehandler = logging.FileHandler(filename=filename, encoding="utf-8")
        filehandler.setFormatter(self.formatter)  # 日志格式
        return filehandler

    def _get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    @property
    def logger(self):
        return self._logger


if __name__ == '__main__':  # 下面的是用来测试这个模块
    logger = Logger()._logger
    logger.debug("1")
    logger.info("2")
    logger.warning("3")
    logger.error("4")
    logger.critical("5")
