# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-21 00:07:57
FilePath     : /CODE/xjLib/xt_DAO/xt_sqlalchemy.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import pandas
import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import DeclarativeMeta
# , declarative_base 类工厂
from sqlalchemy.orm import scoped_session, sessionmaker
from xt_Class import typed_property
from xt_DAO.cfg import connect_str
from xt_DAO.xt_chemyMeta import Orm_Meta


def get_engine(key='default'):
    engine = create_engine(connect_str(key))
    # session = sessionmaker(bind=engine)()  # 单线程
    # scoped_session类似单例模式,每次调用都是同一个session
    session = scoped_session(sessionmaker(bind=engine))  # autocommit=True, autoflush=True

    return engine, session


class SqlConnection(Orm_Meta):

    # #限定参数类型
    dbmodel = typed_property('dbmodel', DeclarativeMeta)

    def __init__(self, Base, key='default', tablename=None):
        self.Base = Base  # orm基类
        self.tablename = tablename or self.Base.__tablename__
        # #设置self.params参数
        self.params = {attr: getattr(self.Base, attr) for attr in self.Base.columns()}
        # 创建引擎
        self.engine = create_engine(
            connect_str(key),
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间,否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            # echo=True,  # echo参数为True时,会显示每条执行的SQL语句
            # poolclass=NullPool, # 禁用池
        )
        self.conn = self.engine.connect()  # pd使用
        self.session = sessionmaker(bind=self.engine)()
        self.Base.metadata.create_all(self.engine)  # 创建表
        self.query = self.session.query(self.Base)
        # self.Base.query = self.session.query()
        # 获取数据库名列表
        self.insp = sqlalchemy.inspect(self.engine)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        return not exc_type

    def drop_db(self, dbmodel=None):
        """删除init传入的self.Base"""
        # self.Base.__table__.drop(self.engine)# 未生效
        # self.Base.metadata.drop_all(self.engine) # 未生效
        dbmodel = dbmodel or self.Base
        drop_sql = f"DROP TABLE if exists {dbmodel.__tablename__}"
        self.session.execute(drop_sql)

    def insert(self, item_dict):
        """传入字段与值对应的字典"""
        item = self.Base(**item_dict)
        self.session.add(item)
        try:
            return self.session.commit()
        except BaseException as e:
            self.session.rollback()
            return 0

    def insert_all(self, dict_list):
        """传入字段与值对应的字典所构成的list"""
        item = [self.Base(**dict1) for dict1 in dict_list]
        self.session.add_all(item)
        try:
            return self.session.commit()
        except BaseException as e:
            self.session.rollback()
            return 0

    def delete(self, conditions_dict):
        query = self.__条件筛选(conditions_dict)
        deleteNum = query.delete()
        try:
            self.session.commit()
            return deleteNum
        except BaseException as e:
            self.session.rollback()
            return 0

    def update(self, conditions_dict, value_dict):
        '''
        conditions_dict:条件字典;where
        value_dict:更新数据字典:{'字段':字段值}
        '''
        query = self.__条件筛选(conditions_dict)
        updatevalue = {self.params.get(key, None): value_dict.get(key) for key in list(value_dict.keys()) if self.params.get(key, None)}
        return query.update(updatevalue)

    # TODO unitled in `delete` and `update`
    def __条件筛选(self, conditions_dict):
        conditon_list = [self.params.get(key) == conditions_dict.get(key) for key in list(conditions_dict.keys()) if self.params.get(key, None)]
        result = self.query
        for condition in conditon_list:
            result = result.filter(condition)
        return result

    def select(self, conditions_dict=None, Columns_list=None, count=None):
        '''
        conditions:字典,条件 where。类似self.params
        Columns:选择的列名
        count:返回的记录数
        return:处理后的list,内含dict(未选择列),或tuple(选择列)
        '''
        if isinstance(Columns_list, (tuple, list)) and len(Columns_list) > 0:
            __Columns_list = [self.params.get(key) for key in Columns_list if self.params.get(key, None)]
        else:
            __Columns_list = [self.Base]

        query = self.session.query(*__Columns_list)

        if isinstance(conditions_dict, dict):
            conditon_list = [self.params.get(key) == conditions_dict.get(key) for key in list(conditions_dict.keys()) if self.params.get(key, None)]
            for __cond in conditon_list:
                query = query.filter(__cond)

        return query.limit(count).all() if count else query.all()

    def from_statement(self, sql, conditions_dict=None):
        '''使用完全基于字符串的语句'''
        query = self.query.from_statement(text(sql))
        return query.params(**conditions_dict).all() if conditions_dict else query.all()

    def filter_by(self, filter_kwargs, count=None):
        '''
        filter_by用于简单查询,不支持比较运算符,不需要额外指定类名。
        filter_by的参数直接支持组合查询。
        仅支持[等于]、[and],无需明示,在参数中以字典形式传入
        '''
        query = self.query.filter_by(**filter_kwargs)
        return query.limit(count).all() if count else query.all()

    def pd_get_dict(self, table_name):
        result = pandas.read_sql_table(table_name, con=self.conn)
        data_dict = result.to_dict(orient="records")
        return data_dict if len(data_dict) else False

    def pd_get_list(self, table_name, Columns):
        result = pandas.read_sql_table(table_name, con=self.conn)
        pd_list = result[Columns].drop_duplicates().values.tolist()
        return pd_list if len(pd_list) else False


def create_orm(key, source_table_name, target_table_name=None):
    from xt_DAO.xt_chemyMeta import getModel
    engine, _ = get_engine(key)
    _t = getModel(source_table_name, engine, target_table_name)  # #获取orm基类
    return SqlConnection(Base=_t, key=key, tablename=_t.__tablename__)


if __name__ == "__main__":
    # Data_Model_2_py('uuu', 'd:/1.py', 'TXbook')  # 待测试
    item1 = {'username': '刘新军', 'password': '234567', '手机': '13910118122', '代理人编码': '10005393', '会员级别': 'SSS', '会员到期日': '9999-12-31 00:00:00'}
    sqlhelper = create_orm('TXbx', 'users2')  #, 'user99')
    # res = sqlhelper.filter_by({'ID': 1})
    # print(res)
    # res = sqlhelper.select()
    # print(res)
    # resfrom_statement = sqlhelper.from_statement('select * from users2 where id=:id', {'id': 1})
    # print(resfrom_statement)
    # print(sqlhelper.Base.make_dict(resfrom_statement))
    # print(resfrom_statement[0].to_dict())
    # print(resfrom_statement[0].to_json())
    # updateNum = sqlhelper.update({'ID': 2}, {'username': '刘新军'})
    # print(updateNum)
    # insertNum = sqlhelper.insert(item1)
    # print(insertNum)
    # deleNum = sqlhelper.delete({'ID': 3})
    # print(deleNum)
    # res = sqlhelper.select({'username': '刘新军'}, ['ID', 'username'], 2)
    # print(res)
    '''
    https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
    http://sunnyingit.github.io/book/section_python/SQLalchemy-engine.html
    https://www.cnblogs.com/pycode/p/mysql-orm.html
    https://docs.sqlalchemy.org/en/20/orm/session_basics.html
    SQLAlchemy 中的 Session、sessionmaker、scoped_session - 长安223 - 博客园
    https://www.cnblogs.com/ChangAn223/p/11277468.htm
    # self.s_engine = create_engine(connect_str(self.key))
    # self.tbl = Table(self.table_name, MetaData(bind=self.s_engine), autoload=True)
    # insert_sql = tbl.insert().values({'name': 'test', 'age': 18})
    # update_sql = tbl.update().where(tbl.c.id == 1).values({'name': 'test', 'age': 18})
    # select_sql = tbl.select().where(tbl.c.id == 1)
    # delete_sql = tbl.delete().where(tbl.c.id == 1)
    https://www.cnblogs.com/panwenbin-logs/p/5731265.html#_label4
    ==============================================================
    '''
