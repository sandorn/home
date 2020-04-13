# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@version:
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 01:37:18
@LastEditors: Even.Sand
@LastEditTime: 2020-04-13 10:02:10
'''


class SqlBase(object):
    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, dict=None):
        raise NotImplemented

    def insert_all(self, dict=None):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def update(self, conditions=None, value=None):
        raise NotImplemented

    def select(self, conditions=None, Columns=None, count=None, show=False):
        raise NotImplemented

    def from_statement(self, sql, conditions=None, show=False):
        raise NotImplemented

    def filter(self, conditions, show=False):
        raise NotImplemented

    def filter_by(self, conditions, show=False):
        raise NotImplemented

    def _result_refine(self, result):
        raise NotImplemented
