# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-03-25 10:13:07
#FilePath     : /xjLib/xt_DAO/xt_sqlalchemy.py
#LastEditTime : 2020-06-16 17:22:32
# Github       : https://github.com/sandorn/home
# License      : (C)Copyright 2009-2020, NewSea
# ==============================================================
'''

from sqlalchemy import (TIMESTAMP, Column, DateTime, Enum, Integer, Numeric,
                        String, text, create_engine)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base, api
from sqlalchemy.orm import scoped_session, sessionmaker, validates

# 此处用.引用在其他地方可以操作，本文件不可以
from .dbconf import make_connect_string
from .xt_sqlbase import SqlBase, SqlMeta
from xt_Class import typed_property


class SqlConnection(SqlBase):

    # #限定参数类型
    baseclass = typed_property('baseclass', api.DeclarativeMeta)

    def __init__(self, baseclass, key='default'):
        self.baseclass = baseclass  # #定义基础数据类
        # #设置self.params参数
        self.params = {
            attr: getattr(baseclass, attr)
            for attr in baseclass._fields()
        }
        self.engine = create_engine(make_connect_string(key), echo=False)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        # #单线程 sessionmaker(bind=self.engine)
        self.baseclass.metadata.create_all(self.engine)

    def drop_db(self):
        self.baseclass.metadata.drop_all(self.engine)

    def insert(self, dict):
        """传入字段与值对应的字典"""
        item = self.baseclass(**dict)
        self.session.add(item)
        self.session.commit()

    def insert_all(self, dict_list):
        """传入字段与值对应的字典所构成的list"""
        item = [self.baseclass(**dict) for dict in dict_list]
        self.session.add_all(item)
        self.session.commit()

    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(
                        self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(self.baseclass)
            for condition in conditions:
                query = query.filter(condition)
            deleteNum = query.delete()
            self.session.commit()
        else:
            deleteNum = 0
        return 'deleteNum', deleteNum

    def update(self, conditions=None, value_dict=None):
        '''
        conditions的格式是个字典。类似self.params
        :param conditions:
        :param value_dict:也是个字典：{'ip':192.168.0.1}
        :return:
        '''
        if conditions and value_dict:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(
                        self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(self.baseclass)
            for condition in conditions:
                query = query.filter(condition)
            updatevalue = {}
            for key in list(value_dict.keys()):
                if self.params.get(key, None):
                    updatevalue[self.params.get(key,
                                                None)] = value_dict.get(key)
            updateNum = query.update(updatevalue)
            self.session.commit()
        else:
            updateNum = 0
        return {'updateNum': updateNum}

    def select(self, count=None, conditions=None, Columns=None):
        '''
        conditions:条件，where  格式是个字典。类似self.params
        :param Columns:选择的列名
        :param count:返回的记录数
        :return:处理后的list，内含dict(未选择列)，或tuple(选择列)
        '''
        if isinstance(Columns, (tuple, list)) and len(Columns) > 0:
            Columns_list = []
            for key in Columns:
                if self.params.get(key, None):
                    Columns_list.append(self.params.get(key))
            Columns = Columns_list
        else:
            Columns = [self.baseclass]
        query = self.session.query(*Columns)

        if isinstance(conditions, dict):
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(
                        self.params.get(key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        if len(conditions) > 0:
            for condition in conditions:
                query = query.filter(condition)

        if count:
            return query.limit(count).all()
        else:
            return query.all()

    def from_statement(self, sql, conditions=None):
        '''
        使用完全基于字符串的语句
        '''
        if sql:
            query = self.session.query(self.baseclass).from_statement(
                text(sql))
        if conditions:
            result = query.params(**conditions).all()
            self.session.commit()
        else:
            result = query.all()
            self.session.commit()

        return result

    def filter_by(self, conditions):
        '''
        filter_by用于查询简单的列名，不支持比较运算符,不需要额外指定类名。
        fitler_by使用的是"="。
        filter_by的参数是**kwargs，直接支持组合查询。
        仅支持[等于]、[and]，无需明示，在参数中以字典形式传入
        '''
        result = self.session.query(
            self.baseclass).filter_by(**conditions).all()
        return result

    def close(self):
        pass


def creat_sqlalchemy_db_class(tablename, filename=None, key='default'):
    '''
    根据已有数据库生成模型
    sqlacodegen --tables users2 --outfile db.py mysql+pymysql://sandorn:123456@cdb-lfp74hz4.bj.tencentcdb.com:10014/bxflb?charset=utf
    '''
    import subprocess

    if filename is None:
        filename = tablename
    com_list = f'sqlacodegen --tables {tablename} --outfile {filename}_db.py {make_connect_string(key)}'

    subprocess.call(com_list,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
