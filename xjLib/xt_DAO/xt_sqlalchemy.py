# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-03-25 10:13:07
#FilePath     : /xjLib/xt_DAO/xt_sqlalchemy.py
#LastEditTime : 2020-06-04 15:23:00
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''
import os
import sys

# #上级目录
this_path = os.path.dirname(__file__)
parent_path = os.path.dirname(this_path)
sys.path.append(parent_path)
# #项目工作目录
sys.path.append(os.getcwd())

import subprocess

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

from xt_DAO.dbconf import make_connect_string
from xt_DAO.xt_sqlbase import SqlBase, SqlMeta


class SqlConnection(SqlBase):
    # @sqlhelper = engine(DB_class, 'TXbx')
    def __init__(self, baseclass, key='default'):
        self.baseclass = baseclass  # #定义基础数据类
        # #设置self.params参数
        self.params = {attr: getattr(baseclass, attr) for attr in baseclass.getColumns()}
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
                    conditon_list.append(self.params.get(key) == conditions.get(key))
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
                    conditon_list.append(self.params.get(key) == conditions.get(key))
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
        '''
        使用完全基于字符串的语句
        '''
        if sql:
            query = self.session.query(self.baseclass).from_statement(text(sql))
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
        result = self.session.query(self.baseclass).filter_by(**conditions).all()
        return result

    def close(self):
        pass


def creat_sqlalchemy_db_class(tablename, filename=None, key='default'):
    '''
    根据已有数据库生成模型
    sqlacodegen --tables users2 --outfile db.py mysql+pymysql://sandorn:123456@cdb-lfp74hz4.bj.tencentcdb.com:10014/bxflb?charset=utf
    '''
    if filename is None:
        filename = tablename
    com_list = f'sqlacodegen --tables {tablename} --outfile {filename}_db.py {make_connect_string(key)}'
    subprocess.call(com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


if __name__ == '__main__':

    def main():
        from sqlalchemy.orm import validates
        from sqlalchemy import Column, DateTime, String, Enum  # Integer, Numeric, TIMESTAMP
        from sqlalchemy.dialects.mysql import INTEGER

        Base = declarative_base()  # 生成一个SQLORM基类
        '''metadata = Base.metadata'''

        class Users(Base, SqlMeta):
            # #多个父类，继承model的一些方法
            # #解决下标取值赋值、打印显示、生成字段列表
            __tablename__ = 'users2'

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

        sqlhelper = SqlConnection(Users, 'TXbx')
        print(Users)
        res = sqlhelper.select(10)
        print(res)
        user2 = [{'username': '刘澈', 'password': '234567', '手机': '17610786502', '代理人编码': '10005393', '会员级别': 'SSS', '会员到期日': '8888,12,31', }, {'username': '刘新军', '手机': '13910118122', }]

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
        res = sqlhelper.select(conditions={"username": "刘澈"}, Columns=['username', 'ID'])
        print(4444, res)
        res = sqlhelper.select(2, conditions={"username": "刘澈"}, Columns=['username', 'ID'])
        print(5555, res)
        res = sqlhelper.select(conditions={"username": "刘澈"}, count=1)
        print(6666, res)
        print(6666, res[0]['username'], res[0].username)
        res = sqlhelper.from_statement("SELECT username,ID FROM users2 where username=:username limit 4", {"username": "刘澈"})
        print(7777, sqlhelper.baseclass.ToDict(res))
        for item in res:
            print(8888, Users.ToDict(item))

    main()

'''
    fiter举例：
    query(User.name).filter(User.fullname==’Ed Jones’)
    query.filter(or_(User.name == ‘ed’, User.name == ‘wendy’))
    query.filter(and_(User.name == ‘ed’, User.fullname == ‘Ed Jones’))

    filters = {
        User.name == ‘fengyao’,
        User.age > 25
    }
    User.query.filter(*filters).first()

    #查询 user 表里面名字等于 Tom 的：
    db.session.query(User).filter(User.name == 'Tom').all()
    #查询 user 表里面名字等于 Tom 并且年龄等于 18：
    db.session.query(User).filter(User.name == 'Tom', User.age == 18).all()
    #也可以这样：
    db.session.query(User).filter(User.name == 'Tom'）.filter(User.age == 18).all()
    #如果想使用 and 拼接需要用以下方式：
    db.session.query(User).filter(and_(User.name == 'Tom', User.age == 18)).all()
    #以下的方式 and 后面的 User.age == 18 不会生效：
    db.session.query(User).filter(User.name == 'Tom' and User.age == 18).all()
    #查询 user 表里面名字等于 Tom 的或者年龄等于 18：
    db.session.query(User).filter(or_(User.name == 'Tom', User.age == 18)).all()
    #查询 user 表里面名字等于 Tom 的并且年龄大于 18
    db.session.query(User).filter(User.name == 'Tom', User.age > 18).all()
    #查询 name 中包含字母 a 的所有数据(模糊查询)
    db.session.query(User).filter(User.name.like('%{0}%'.format("a"))).all()

    常用的SQLAlchemy字段类型
    类型名	python中类型	说明
    Integer	int	普通整数，一般是32位
    SmallInteger	int	取值范围小的整数，一般是16位
    BigInteger	int或long	不限制精度的整数
    Float	float	浮点数
    Numeric(P，D)decimal.Decimal	定点数
        P：有效数字长度。范围是1~65。
        D是表示小数点后的位数。范围是0~30。MYSQL要求D<=P。

    VARCHAR	str
    String	str	变长字符串
    Text	str	变长字符串，对较长或不限长度的字符串做了优化
    Unicode	unicode	变长Unicode字符串
    UnicodeText	unicode	变长Unicode字符串，对较长或不限长度的字符串做了优化
    Boolean	bool	布尔值
    Date	datetime.date	时间
    Time	datetime.datetime	日期和时间
    LargeBinary	str	二进制文件
    TIMESTAMP  自动获取时间

    1. Integer：整型，映射到数据库中是int类型。
    2. Float：浮点类型，映射到数据库中是float类型。它占据的32位。
    3. Double：双精度浮点类型，映射到数据库中是double类型，占据64位。
    4. String：可变字符类型，映射到数据库中是varchar类型。
    5. Boolean：布尔类型，映射到数据库中的是tinyint类型。
    6. DECIMAL：定点类型。是专门为了解决浮点类型精度丢失的问题的。在存储钱相关的字段的时候建议大家都使用这个数据类型。并且这个类型使用的时候需要传递两个参数，第一个参数是用来标记这个字段总能能存储多少个数字，第二个参数表示小数点后有多少位。
    7. Enum：枚举类型。指定某个字段只能是枚举中指定的几个值，不能为其他值。在ORM模型中，使用Enum来作为枚举。
    8. Date：存储时间，只能存储年月日。映射到数据库中是date类型。在Python代码中，可以使用`datetime.date`来指定。
    9. DateTime：存储时间，可以存储年月日时分秒毫秒等。映射到数据库中也是datetime类型。在Python代码中，可以使用`datetime.datetime`来指定。
    10. Time：存储时间，可以存储时分秒。映射到数据库中也是time类型。在Python代码中，可以使用`datetime.time`来指定。
    11. Text：存储长字符串。一般可以存储6W多个字符。如果超出了这个范围，可以使用LONGTEXT类型。映射到数据库中就是text类型。
    12. LONGTEXT：长文本类型，映射到数据库中是longtext类型。

    常用的SQLAlchemy列选项
    选项名	说明
    primary_key	如果为True，代表表的主键
    unique	如果为True，代表这列不允许出现重复的值
    index	如果为True，为这列创建索引，提高查询效率
    nullable	如果为True，允许有空值，如果为False，不允许有空值
    default	为这列定义默认值

    常用的SQLAlchemy关系选项
    选项名	说明
    backref	在关系的另一模型中添加反向引用
    primaryjoin	明确指定两个模型之间使用的联结条件
    uselist	如果为False，不使用列表，而使用标量值
    order_by	指定关系中记录的排序方式
    secondary	指定多对多中记录的排序方式
    secondaryjoin	在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件

    one_or_none()和one()很像，除了在查询不到的时候。查询不到的时候one_or_none()会直接返回None，但是在找到多个值的时候和one()一样。

    query.scalar()援引自one()函数，查询成功之后会返回这一行的第一列参数

    https://www.jianshu.com/p/0ad18fdd7eed
    https://blog.csdn.net/q370835062/article/details/84974951
    http://www.pythontip.com/blog/post/12611/
'''
