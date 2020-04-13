# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-25 10:13:07
@LastEditors: Even.Sand
@LastEditTime: 2020-04-05 01:43:54
'''

import datetime

from sqlalchemy import (VARCHAR, Column, DateTime, Integer, Numeric,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from xjLib.db.dbRouter import db_conf


class ISqlHelper(object):
    params = {
        'ip': None,
        'port': None,
        'types': None,
        'protocol': None,
        'country': None,
        'area': None
    }

    def init_db(self):
        raise NotImplemented

    def drop_db(self):
        raise NotImplemented

    def insert(self, value=None):
        raise NotImplemented

    def delete(self, conditions=None):
        raise NotImplemented

    def update(self, conditions=None, value=None):
        raise NotImplemented

    def select(self, count=None, conditions=None):
        raise NotImplemented


BaseModel = declarative_base()


class Proxy(BaseModel):
    __tablename__ = 'proxys'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False, default=0)
    country = Column(VARCHAR(100), nullable=False)
    area = Column(VARCHAR(100), nullable=False)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=20)


def createClass(cls):

    class SqlHelper(ISqlHelper):
        params = {
            'ip': Proxy.ip,
            'port': Proxy.port,
            'types': Proxy.types,
            'protocol': Proxy.protocol,
            'country': Proxy.country,
            'area': Proxy.area,
            'score': Proxy.score
        }

        def __init__(self):
            if 'sqlite' in DB_CONFIG['DB_CONNECT_STRING']:
                connect_args = {'check_same_thread': False}
                self.engine = create_engine(
                    DB_CONFIG['DB_CONNECT_STRING'],
                    echo=False,
                    connect_args=connect_args)
            else:
                self.engine = create_engine(
                    DB_CONFIG['DB_CONNECT_STRING'], echo=False)
            DB_Session = sessionmaker(bind=self.engine)
            self.session = DB_Session()

        def init_db(self):
            BaseModel.metadata.create_all(self.engine)

        def drop_db(self):
            BaseModel.metadata.drop_all(self.engine)

        def insert(self, value):
            proxy = Proxy(
                ip=value['ip'],
                port=value['port'],
                types=value['types'],
                protocol=value['protocol'],
                country=value['country'],
                area=value['area'],
                speed=value['speed'])
            self.session.add(proxy)
            self.session.commit()

        def delete(self, conditions=None):
            if conditions:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key, None):
                        conditon_list.append(
                            self.params.get(key) == conditions.get(key))
                conditions = conditon_list
                query = self.session.query(Proxy)
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
                query = self.session.query(Proxy)
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

        def select(self, count=None, conditions=None):
            '''
            conditions的格式是个字典。类似self.params
            :param count:
            :param conditions:
            :return:
            '''
            if conditions:
                conditon_list = []
                for key in list(conditions.keys()):
                    if self.params.get(key, None):
                        conditon_list.append(
                            self.params.get(key) == conditions.get(key))
                conditions = conditon_list
            else:
                conditions = []

            query = self.session.query(Proxy.ip, Proxy.port, Proxy.score)
            if len(conditions) > 0 and count:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Proxy.score.desc(),
                                      Proxy.speed).limit(count).all()
            elif count:
                return query.order_by(Proxy.score.desc(),
                                      Proxy.speed).limit(count).all()
            elif len(conditions) > 0:
                for condition in conditions:
                    query = query.filter(condition)
                return query.order_by(Proxy.score.desc(), Proxy.speed).all()
            else:
                return query.order_by(Proxy.score.desc(), Proxy.speed).all()

        def close(self):
            pass

    return SqlHelper


if __name__ == '__main__':
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    proxy = {
        'ip': '192.168.1.1',
        'port': 80,
        'type': 0,
        'protocol': 0,
        'country': '中国',
        'area': '广州',
        'speed': 11.123,
        'types': ''
    }
    sqlhelper.insert(proxy)
    sqlhelper.update({'ip': '192.168.1.1', 'port': 80}, {'score': 10})
    print(sqlhelper.select(1))
