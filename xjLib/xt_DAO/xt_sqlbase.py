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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-08 20:43:34
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


class SqlMeta:
    # #扩展DB模型的方法
    # #作用：支持下标引用和赋值
    def __getitem__(self, attr):
        # return  self.__getattribute__(attr)
        return getattr(self, attr)

    def __setitem__(self, attr, value):
        # return  self.__getattribute__(attr)
        return setattr(self, attr, value)

    # #获取字段名列表
    @classmethod
    def getColumns(cls):
        ColumnsList = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__") and not attr == '_sa_class_manager' and not attr == '_decl_class_registry' and not attr == '_sa_instance_state' and not attr == 'metadata']
        return ColumnsList

    # #数据记录转字典
    @classmethod
    def ToDict(cls, result):
        if isinstance(result, cls):
            return {key: getattr(result, key) for key in cls.getColumns()}

        elif isinstance(result[0], cls):
            return [{key: getattr(item, key) for key in cls.getColumns()} for item in result]

    # #用于打印显示
    def __repr__(self):
        return str(self.__class__) + ' : ' + str({attr: getattr(self, attr) for attr in self.getColumns()})

    __str__ = __repr__
