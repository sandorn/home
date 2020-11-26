# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-03-25 10:13:07
FilePath     : /xjLib/xt_DAO/xt_sqlalchemy.py
LastEditTime : 2020-11-04 13:33:59
# Github       : https://github.com/sandorn/home
# License      : (C)Copyright 2009-2020, NewSea
# ==============================================================
'''

from sqlalchemy import (TIMESTAMP, Column, DateTime, Enum, Integer, Numeric, String, create_engine, text)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import DeclarativeMeta  # 类;declarative_base类工厂
from sqlalchemy.orm import scoped_session, sessionmaker, validates

from xt_Class import typed_property
from .dbconf import make_connect_string
from .xt_chemyMeta import Orm_Meta


def get_engine(key='default', dbmodel=None):
    engine = create_engine(
        make_connect_string(key),
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
        echo=False  # echo参数为True时，会显示每条执行的SQL语句
    )
    session = sessionmaker(bind=engine)  # #单线程
    # #实现user.query.xxxx  # FROM tablename
    if dbmodel is not None: dbmodel.query = session.query_property()
    return engine, session


class SqlConnection(Orm_Meta):

    # #限定参数类型
    dbmodel = typed_property('dbmodel', DeclarativeMeta)

    def __init__(self, dbmodel, key='default'):
        self.dbmodel = dbmodel  # #orm基类
        # #设置self.params参数
        self.params = {attr: getattr(self.dbmodel, attr) for attr in self.dbmodel.columns()}
        self.engine = create_engine(
            make_connect_string(key),
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            echo=False  # echo参数为True时，会显示每条执行的SQL语句
        )
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.dbmodel.metadata.create_all(self.engine)

    def drop_db(self):
        """删除init传入的self.dbmodel"""
        drop_sql = "DROP TABLE if exists {}".format(self.dbmodel.__tablename__)
        self.session.execute(drop_sql)
        # self.dbmodel.__table__.drop(self.engine)# 未生效
        # self.dbmodel.metadata.drop_all(self.engine) # 未生效

    def insert(self, dict):
        """传入字段与值对应的字典"""
        item = self.dbmodel(**dict)
        self.session.add(item)
        self.session.commit()

    def insert_all(self, dict_list):
        """传入字段与值对应的字典所构成的list"""
        item = [self.dbmodel(**dict) for dict in dict_list]
        self.session.add_all(item)
        self.session.commit()

    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(self.dbmodel)
            for condition in conditions:
                query = query.filter(condition)
            deleteNum = query.delete()
            self.session.commit()
        else:
            deleteNum = 0
        return 'deleteNum', deleteNum

    def update(self, conditions=None, value_dict=None):
        '''
        conditions：字典。类似self.params
        value_dict:字典：{'ip':192.168.0.1}
        '''
        if conditions and value_dict:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(self.dbmodel)
            for condition in conditions:
                query = query.filter(condition)
            updatevalue = {}
            for key in list(value_dict.keys()):
                if self.params.get(key, None):
                    updatevalue[self.params.get(key, None)] = value_dict.get(key)
            updateNum = query.update(updatevalue)
            self.session.commit()
        else:
            updateNum = 0
        return updateNum

    def select(self, conditions=None, Columns=None, count=None):
        '''
        conditions:字典，条件 where。类似self.params
        Columns:选择的列名
        count:返回的记录数
        return:处理后的list，内含dict(未选择列)，或tuple(选择列)
        '''
        if isinstance(Columns, (tuple, list)) and len(Columns) > 0:
            Columns_list = []
            for key in Columns:
                if self.params.get(key, None):
                    Columns_list.append(self.params.get(key))
            Columns = Columns_list
        else:
            Columns = [self.dbmodel]

        query = self.session.query(*Columns)

        if isinstance(conditions, dict):
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
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
        '''使用完全基于字符串的语句'''
        if sql:
            query = self.session.query(self.dbmodel).from_statement(text(sql))
        if conditions:
            result = query.params(**conditions).all()
            self.session.commit()
        else:
            result = query.all()
            self.session.commit()

        return result

    def filter_by(self, kwargs, count=None):
        '''
        filter_by用于简单查询，不支持比较运算符,不需要额外指定类名。
        filter_by的参数直接支持组合查询。
        仅支持[等于]、[and]，无需明示，在参数中以字典形式传入
        '''
        query = self.session.query(self.dbmodel).filter_by(**kwargs)
        if count:
            return query.limit(count).all()
        else:
            return query.all()

    def close(self):
        pass
