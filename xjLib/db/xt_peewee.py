# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-06 23:19:45
#LastEditTime : 2020-04-28 18:56:38
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
#!未完成
'''

import os
from peewee import Model  # peewee提供的基础类，一个Model就对应一个数据库
from peewee import MySQLDatabase  # peewee支持 MySQLDatabase PostgresqlDatabase SqliteDatabase 等数据库
from peewee import BooleanField  # 几种常见的数据类型，还有PrimaryField自己可以看看用法
from peewee import CharField
from peewee import FloatField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import TextField
from xjLib.db.dbRouter import db_conf
from xjLib.db.dbStore import ISqlHelper


class engine(ISqlHelper):

    def __init__(self, baseclass, key='default'):
        self.baseclass = baseclass  # 父类定义表格类
        self._set_params()  # 设置self.params参数
        connstr = f"mysql+mysqlconnector://{db_conf[key]['user']}:{db_conf[key]['passwd']}@{db_conf[key]['host']}:{db_conf[key]['port']}/{db_conf[key]['db']}?charset={db_conf[key]['charset']}"
        self.engine = create_engine(connstr, echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()
        self.init_db()

    def _set_params(self):
        # #eval(f'self.baseclass.{attr}')
        '''
        self.params = {
            attr: getattr(self.baseclass, attr)
            for attr in dir(self.baseclass)
            if not callable(getattr(self.baseclass, attr))
            and not attr.startswith("__") and not attr ==
            '_decl_class_registry' and not attr == '_sa_class_manager'
            and not attr == '_sa_instance_state' and not attr == 'metadata'
        }
        '''
        self.params = {
            attr: getattr(self.baseclass, attr)
            for attr in self.baseclass.__dict__
            if not callable(getattr(self.baseclass, attr)) and
            not attr.startswith("__") and not attr == '_sa_class_manager'
        }

    def init_db(self):
        database.connect()
        database.create_tables([self.baseclass])

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

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
        return ('deleteNum', deleteNum)

    def update(self, conditions=None, value=None):
        '''
        conditions的格式是个字典。类似self.params
        :param conditions:
        :param value:也是个字典：{'ip':192.168.0.1}
        :return:
        '''
        if conditions and value:
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
            for key in list(value.keys()):
                if self.params.get(key, None):
                    updatevalue[self.params.get(key, None)] = value.get(key)
            updateNum = query.update(updatevalue)
            self.session.commit()
        else:
            updateNum = 0
        return {'updateNum': updateNum}

    def select(self, conditions=None, Columns=None, count=None, show=False):
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
            if show:
                return self._result_refine(query.limit(count).all())
            else:
                return query.limit(count).all()
        else:
            if show:
                return self._result_refine(query.all())
            else:
                return query.all()

    def from_statement(self, sql, conditions=None, show=False):
        '''
        使用完全基于字符串的语句
        @param {type}
        @return:
        '''
        if sql:
            query = self.session.query(self.baseclass).from_statement(text(sql))
        if conditions:
            result = query.params(**conditions).all()
            self.session.commit()
        else:
            result = query.all()
            self.session.commit()
        if show:
            return self._result_refine(result)
        else:
            return result

    def filter(self, conditions, show=False):
        '''
        #!未完善，暂不使用
        filter中，语法更加贴近于，类似于，Python的语法。
        比filter_by的功能更强大，且更复杂的查询的语法，
        and()，or()等多个条件的查询，只支持filter
        语法： column == expression
        传入参数的写法，要用：类名.列名 两个等号 去判断
        引用列名时，需要通过 类名.属性名 的方式。
        '''
        result = self.session.query(self.baseclass).filter(**conditions).all()
        if show:
            return self._result_refine(result)
        else:
            return result

    def filter_by(self, conditions, show=False):
        '''
        filter_by用于查询简单的列名，不支持比较运算符,不需要额外指定类名。
        fitler_by使用的是"="。
        filter_by的参数是**kwargs，直接支持组合查询。
        仅支持[等于]、[and]，无需明示，在参数中以字典形式传入
        '''
        result = self.session.query(
            self.baseclass).filter_by(**conditions).all()
        if show:
            return self._result_refine(result)
        else:
            return result

    def _result_refine(self, result):
        '''
        @description: 处理结果
        @param {type}:输入self.baseclass对象,或self.baseclass对象组成的list,或tuple组成的tuple
        @return:dict  或 list内含dict or list
        '''
        if isinstance(result, self.baseclass):
            return {key: getattr(result, key) for key in self.params.keys()}
        '''
        if isinstance(result, (tuple, list)):
            return  [{
                key: getattr(item, key)
                for key in self.params.keys()
            } for item in result if isinstance(item, self.baseclass)]
        '''
        res_list = []
        if isinstance(result, (tuple, list)):
            for item in result:
                if isinstance(item, self.baseclass):
                    # #list内多个self.baseclass对象
                    res_list.append(
                        {key: getattr(item, key) for key in self.params.keys()})
                elif isinstance(item, tuple):
                    # #设置了字段的select
                    res_list.append([*item])
            return res_list

    def close(self):
        pass

    def f(self, conditions, show=False):
        result = self.session.query(self.baseclass).filter(
            self.baseclass.username.like(conditions)).all()
        if show:
            return self._result_refine(result)
        else:
            return result


if __name__ == '__main__':

    from peewee import *
    from peewee import MySQLDatabase
    # 创建一个peewee数据库实例
    database = MySQLDatabase(
        'bxflb', **{
            'charset': 'utf8',
            'sql_mode': 'PIPES_AS_CONCAT',
            'use_unicode': True,
            'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
            'port': 10014,
            'user': 'sandorn',
            'password': '123456'
        })

    class UnknownField(object):

        def __init__(self, *_, **__):
            pass

    # 模型定义 - 标准“模式”是定义一个基础模型类，它指定要使用哪个数据库。
    # 然后任何子类将自动地使用正确的存储。
    class BaseModel(Model):
        u"""
        基础类
        可以在此处制定一些大家都需要的列，
        然后每个继承的子类（表）中都会有这么固定的几列
        """

        class Meta:
            database = database

    # 这个User模型以声明式指定其字段（或列）
    class Users2(BaseModel):
        id = AutoField()
        password = CharField()
        username = CharField()
        手机 = CharField(null=True)
        代理人编码 = CharField(null=True)
        会员级别 = CharField(constraints=[SQL("DEFAULT 'C'")], null=True)
        会员到期日 = DateTimeField(
            constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
        登陆次数 = CharField(null=True)
        备注 = IntegerField(null=True)

        class Meta:
            table_name = 'users2'
            u"""
            db_table指定表名，
            order_by 指定表中数据的排序顺序,
            indexes是为表中数据添加索引，加快后续的查询
            其中我指定对学生姓名和学号之间建立索引，两个一块查会有速度优势，
            后边的True表明，这两个数据组合必须是unique的
            db_table = 'student'
            order_by = (
                'student_ID',
                'student',
            )
            indexes = ((('student', 'student_ID'), True), )
            """

    database.connect()
    database.create_tables([
        Users2,
    ])
    for i in range(10):
        Users2(
            username='王五' + str(i), password=50,
            手机='1333333333' + str(i)).save()
'''
备注
# !根据已有数据库生成模型
#!python -m pwiz -e mysql -H cdb-lfp74hz4.bj.tencentcdb.com -p 10014 -u sandorn -P 123456  bxflb > db.py
留存，待完善，暂不进行了

使用 SQLObject 连接数据库与 Python
https://www.ibm.com/developerworks/cn/opensource/os-pythonsqlo/

Python：轻量级 ORM 框架 peewee 用法详解之——增删改查 - 丹枫无迹 - 博客园
https://www.cnblogs.com/gl1573/p/10380793.html

Peewee的使用_网络_qq123aa2006的博客-CSDN博客
https://blog.csdn.net/qq123aa2006/article/details/89276571

Peewee中文文档【二】：快速开始_数据库_package com.amos-CSDN博客
https://blog.csdn.net/amoscn/article/details/74529133

Peewee中文文档【三】：应用实例_数据库_package com.amos-CSDN博客
https://blog.csdn.net/amoscn/article/details/74530284

Python折腾数据库（一）peewee - 简书
https://www.jianshu.com/p/84e667320ab3

Python：轻量级 ORM 框架 peewee 用法详解_Python_guliang21的专栏-CSDN博客
https://blog.csdn.net/guliang21/article/details/87486355


'''
