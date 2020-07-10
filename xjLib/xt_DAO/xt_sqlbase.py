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
#LastEditTime : 2020-07-08 20:22:59
'''
from xt_Class import item_MixIn


class Sql_Base(object):
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
        print('in select')
        raise NotImplemented

    def from_statement(self, sql, conditions=None, show=False):
        print('in from_statement')
        raise NotImplemented

    def filter(self, conditions, show=False):
        raise NotImplemented

    def filter_by(self, conditions, show=False):
        raise NotImplemented

    def _result_refine(self, result):
        raise NotImplemented

    def close(self):
        raise NotImplemented


class Sql_Meta(item_MixIn):
    '''解决下标取值赋值、打印显示、生成字段列表'''
    @classmethod
    def columns(cls):
        '''获取字段名列表'''
        cls._columns = [col.name for col in cls.__table__.columns]
        return cls._columns

    # #获取字段名列表
    @classmethod
    def _fields(cls):
        '''获取字段名列表，弃用'''
        listtmp = [
            attr for attr in dir(cls) if not callable(getattr(cls, attr))
            and not attr.startswith("__") and attr not in [
                '_sa_class_manager', '_decl_class_registry',
                '_sa_instance_state', 'metadata'
            ]
        ]
        return listtmp

    @classmethod
    def make_dict(cls, result):
        '''基于数据库模型转换记录为字典,使用: dbmode.get_dict(records)'''
        if isinstance(result, cls):
            return {key: getattr(result, key) for key in cls.columns()}

        elif isinstance(result, (list, tuple)) and isinstance(result[0], cls):
            return [{key: getattr(item, key)
                     for key in cls.columns()} for item in result]

    def to_dict(self):
        '''单一记录record转字典,使用:record.to_dict()'''
        return self.get_dict(self)

    def __repr__(self):
        return self.__class__.__name__ + str(
            {attr: getattr(self, attr)
             for attr in self.columns()})

    __str__ = __repr__
