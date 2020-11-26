# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-08 20:30:34
FilePath     : /xjLib/test/sqlalchemy测试.py
LastEditTime : 2020-11-05 14:22:56
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from sqlalchemy import Table

from xt_DAO.xt_chemyMeta import (Base_Model, inherit_table_cls, parent_model_Mixin)
from xt_DAO.xt_sqlalchemy import (INTEGER, TIMESTAMP, Column, DateTime, Enum, Integer, Numeric, SqlConnection, String, text, validates)


class Users(Base_Model):
    __tablename__ = 'users2'

    ID = Column(INTEGER(6), primary_key=True, autoincrement=True)
    username = Column(String(24), nullable=False)
    password = Column(String(16), nullable=False, server_default='123456')
    手机 = Column(String(11), nullable=False)
    代理人编码 = Column(String(8))
    会员级别 = Column(Enum('SSS', 'SS', 'S', 'A', "\\\\'B", 'C'), server_default='C')
    会员到期日 = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    登陆次数 = Column(INTEGER(2))
    备注 = Column(String(255))  # db.ForeignKey('roles.id') 外键

    @validates('手机')  # 对字段的校验
    def validate_手机(self, key, 手机):
        assert len(手机) == 11
        return 手机


class Users_two(Base_Model):
    __table__ = Table(
        'users2',
        Base_Model.metadata,
        Column('ID', INTEGER(6), primary_key=True),
        Column('username', String(24), nullable=False),
        Column('password', String(16), nullable=False, server_default='123456'),
        Column('手机', String(11), nullable=False),
        Column('代理人编码', String(8)),
        Column('会员级别', Enum('SSS', 'SS', 'S', 'A', "\\\\'B", 'C'), server_default='C'),
        Column('会员到期日', DateTime, server_default=text("CURRENT_TIMESTAMP")),
        Column('登陆次数', INTEGER(2)),
        Column('备注', String(255)),
        extend_existing=True,
    )

    @validates('手机')  # 对字段的校验
    def validate_手机(self, key, 手机):
        assert len(手机) == 11
        return 手机


def sqlalchemy测试():
    print(repr(Users))
    print(Users.columns())
    print(Users._c)
    sqlhelper = SqlConnection(Users, 'TXbx')
    # sqlhelper = SqlConnection(Users_two, 'TXbx')

    user2 = [{
        'username': '刘澈',
        'password': '234567',
        '手机': '17610786502',
        '代理人编码': '10005393',
        '会员级别': 'SSS',
        '会员到期日': '8888,12,31',
    }, {
        'username': '刘新军',
        '手机': '13910118122',
    }]

    # sqlhelper.insert_all(user2)
    # sqlhelper.update({'手机': '17610786502'}, {'会员到期日': '7777,12,31'})
    # sqlhelper.update({'username': '刘澈'}, {'会员到期日': '9999,12,31'})
    res = sqlhelper.filter_by({"username": "刘澈"})
    print(1111, res)

    res[0]['会员级别'] = 'A'
    sqlhelper.session.commit()

    # for row in sqlhelper.select(conditions={"username": "刘澈"}):
    #     print(row.username, row.ID)
    # res = sqlhelper.select(conditions={"username": "刘澈"})
    # print(2222, res)
    # res = sqlhelper.select(conditions={"username": "刘澈"})
    # print(3333, res)

    # res = sqlhelper.select(Columns=['username'])
    # print(3434, type(res), type(res[0]), res)
    # res = [r[0] for r in res]
    # print(4444, type(res), type(res[0]), res)
    # for a in res:
    #     print(a)
    # res = sqlhelper.select(count=2, conditions={"username": "刘澈"}, Columns=['username', 'ID'])
    # print(5555, res)
    # res = sqlhelper.select(conditions={"username": "刘澈"}, count=1)
    # print(6666, res)
    # res = sqlhelper.select({"username": "刘澈"})
    # print(7878, res)
    # print(6767, res[0]['username'], res[0].username)
    # res = sqlhelper.from_statement("SELECT username,ID FROM users2 where username=:username limit 4", {"username": "刘澈"})
    # for item in res:
    #     print(7878, item, item.username, item['password'])
    #     print(8888, Users.make_dict(item) or Users_two.make_dict(item))
    #     print(9999, item.to_dict())


class tab(Base_Model, parent_model_Mixin):
    ID = Column(INTEGER(6), primary_key=True)
    username = Column(String(24), nullable=False)
    password = Column(String(16), nullable=False, server_default='123456')
    手机 = Column(String(11), nullable=False)
    代理人编码 = Column(String(8))
    会员级别 = Column(Enum('SSS', 'SS', 'S', 'A', "\\\\'B", 'C'), server_default='C')
    会员到期日 = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    登陆次数 = Column(INTEGER(2))
    备注 = Column(String(255))  # db.ForeignKey('roles.id') 外键

    @validates('手机')  # 对字段的校验
    def validate_手机(self, key, 手机):
        assert len(手机) == 11
        return 手机


def ceshi2():
    cls = inherit_table_cls('users', tab)
    print(cls, str(cls), repr(cls))
    # print(cls, type(cls), cls.__class__)
    # print(cls.__tablename__, cls.__mro__)
    sqlhelper = SqlConnection(cls, 'TXbx')
    res = sqlhelper.select()
    print(2222, res)
    cls2 = inherit_table_cls('users2', tab)
    sqlhelper = SqlConnection(cls2, 'TXbx')
    res = sqlhelper.select()
    print(3333, res)


sqlalchemy测试()
ceshi2()
