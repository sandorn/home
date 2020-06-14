# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-08 20:30:34
#FilePath     : /xjLib/xt_DAO/test/sqlalchemy测试.py
#LastEditTime : 2020-06-14 00:54:04
#Github       : https://github.com/sandorn/home
#==============================================================
'''

from xt_DAO.xt_sqlalchemy import SqlConnection, SqlMeta, declarative_base, text, validates, Column, DateTime, String, Enum, Integer, Numeric, INTEGER, TIMESTAMP

Base = declarative_base()  # 生成一个SQLORM基类
'''metadata = Base.metadata'''


class Users(Base, SqlMeta):
    # #多个父类，继承SqlMeta的一些方法
    # #解决下标取值赋值、打印显示、生成字段列表
    __tablename__ = 'users2'

    ID = Column(INTEGER(6), primary_key=True)
    username = Column(String(24), nullable=False)
    password = Column(String(16), nullable=False, server_default='123456')
    手机 = Column(String(11), nullable=False)
    代理人编码 = Column(String(8))
    会员级别 = Column(Enum('SSS', 'SS', 'S', 'A', "\\\\'B", 'C'),
                  server_default='C')
    会员到期日 = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    登陆次数 = Column(INTEGER(2))
    备注 = Column(String(255))  # db.ForeignKey('roles.id') 外键

    @validates('手机')  # 对字段的校验
    def validate_手机(self, key, 手机):
        assert len(手机) == 11
        return 手机


sqlhelper = SqlConnection(Users, 'TXbx')
res = sqlhelper.select(10)
print(res)
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

sqlhelper.insert_all(user2)
sqlhelper.update({'手机': '17610786502'}, {'会员到期日': '7777,12,31'})
sqlhelper.update({'username': '刘澈'}, {'会员到期日': '9999,12,31'})
res = sqlhelper.filter_by({"username": "刘澈"})
print(1111, res)
res[0]['会员级别'] = 'A'
sqlhelper.session.commit()
print(res[0].getColumns())
for row in sqlhelper.select(conditions={"username": "刘澈"}):
    print(row.username, row.ID)
res = sqlhelper.select(conditions={"username": "刘澈"})
print(2222, res)
res = sqlhelper.select(conditions={"username": "刘澈"})
print(3333, res)
res = sqlhelper.select(conditions={"username": "刘澈"},
                       Columns=['username', 'ID'])
print(4444, res)
res = sqlhelper.select(2,
                       conditions={"username": "刘澈"},
                       Columns=['username', 'ID'])
print(5555, res)
res = sqlhelper.select(conditions={"username": "刘澈"}, count=1)
print(6666, res)
print(6666, res[0]['username'], res[0].username)
res = sqlhelper.from_statement(
    "SELECT username,ID FROM users2 where username=:username limit 4",
    {"username": "刘澈"})
print(7777, sqlhelper.baseclass.ToDict(res))
for item in res:
    print(8888, Users.ToDict(item))
