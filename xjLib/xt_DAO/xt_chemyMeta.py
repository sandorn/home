# !/usr/bin/env python
"""
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-03-25 01:37:18
FilePath     : /xjLib/xt_DAO/xt_chemyMeta.py
LastEditTime : 2021-03-25 10:03:29
#Github       : https://github.com/sandorn/home
#==============================================================
"""

from sqlalchemy import Table
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base
from xt_Class import item_Mixin
from xt_DAO.cfg import connect_str


class Orm_Meta:
    def init_db(self):
        raise NotImplementedError

    def drop_db(self):
        raise NotImplementedError

    def insert(self, dict=None):
        raise NotImplementedError

    def insert_all(self, dict=None):
        raise NotImplementedError

    def delete(self, conditions=None):
        raise NotImplementedError

    def update(self, conditions=None, value=None):
        raise NotImplementedError

    def select(self, conditions=None, Columns=None, count=None, show=False):
        raise NotImplementedError

    def from_statement(self, sql, conditions=None, show=False):
        raise NotImplementedError

    def filter(self, conditions, show=False):
        raise NotImplementedError

    def filter_by(self, conditions, show=False):
        raise NotImplementedError

    def _result_refine(self, result):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class ModelExt(item_Mixin):
    """下标取值赋值、打印显示、生成字段列表"""

    @classmethod
    def columns(cls):
        """获取字段名列表"""
        cls._c = [col.name for col in cls.__table__.c]
        return cls._c

    @classmethod
    def keys(cls):
        """获取字段名列表"""
        cls._c = cls.__table__.columns.keys()
        return cls._c

    @classmethod
    def make_dict(cls, result):
        """基于数据库模型转换记录为字典,使用: dbmode.make_dict(records)"""
        if isinstance(result, cls):
            return {key: getattr(result, key) for key in cls.columns()}
        elif isinstance(result, (list, tuple)) and isinstance(result[0], cls):
            return [{key: getattr(item, key) for key in cls.columns()} for item in result]
        return result

    def to_dict(self):
        """单一记录record转字典,使用:record.to_dict()"""
        return self.make_dict(self)

    def to_json(self):
        fields = self.__dict__
        fields.pop('_sa_instance_state', None)
        return fields

    def __repr__(self):
        fields = self.__dict__
        if '_sa_instance_state' in fields:
            del fields['_sa_instance_state']
        return self.__class__.__name__ + str(dict(fields.items()))
        # return self.__class__.__name__ + str({attr: getattr(self, attr) for attr in self.columns()})

    __str__ = __repr__


Base_Model = declarative_base(cls=ModelExt)  # #生成SQLORM基类,混入继承ModelExt
"""
metadata = Base.metadata
定义table的基类,所有的表都要继承这个类,这个类的作用是将表映射到数据库中
sqlalchemy 强制要求必须要有主键字段不然会报错,sqlalchemy在接收到查询结果后还会自己根据主键进行一次去重,因此不要随便设置非主键字段设为primary_key
一般情况下,我们不需要自己定义主键,sqlalchemy会自动为我们创建一个主键,但是如果我们需要自己定义主键,那么就需要在定义表的时候指定主键,如下所示:id = Column(Integer, primary_key=True)
"""


class parent_model_Mixin:
    """定义所有数据库表对应的父类,用于混入继承,与Base_Model协同"""

    __abstract__ = True


def inherit_table_cls(target_table_name, table_model_cls, cid_class_dict=None):
    """
    从指定table_model_cls类继承,重新定义表名；
    target_table_name:目标表名,用于数据库和返回的类名；
    table_model_cls:包含字段信息的表model类,必须有__abstract__ = True,或混入继承
    table_model_cls 例子:
    class table_model(Base_Model):
        __tablename__ = _BOOKNAME
        __table_args__ = {
            "extend_existing": True,  # 允许表已存在
            "abstract": True,  # 父类模式
            'schema': 'AiTestOps_database',  # 表在同一个数据库服务(datebase)的不同数据库中(schema),可指定数据库
        }
        # __extend_existing__ = True  # 允许表已存在
        # __abstract__ = True,  # 父类模式

        ID = Column(INTEGER(10), primary_key=True)
        BOOKNAME = Column(VARCHAR(255), nullable=False)
        INDEX = Column(INTEGER(10), nullable=False)
        ZJNAME = Column(VARCHAR(255), nullable=False)
        ZJTEXT = Column(TEXT, nullable=False)
        ZJHERF = Column(VARCHAR(255), nullable=False)
    """
    if cid_class_dict is None:
        cid_class_dict = {}
    if not isinstance(table_model_cls, DeclarativeMeta):
        raise TypeError('table_model_cls must be DeclarativeMeta object')

    if target_table_name not in cid_class_dict:
        cls = type(
            target_table_name,
            (table_model_cls,),
            {
                '__table_args__': {
                    'extend_existing': True,  # 允许表已存在
                },
                '__tablename__': target_table_name,
                '__abstract__': True,  # 父类模式
            },
        )
        cid_class_dict[target_table_name] = cls

    return cid_class_dict[target_table_name]


def dictToObj(results, to_class):
    """将字典list或者字典转化为指定类的对象list或指定类的对象
    python 支持动态给对象添加属性,所以字典中存在而该类不存在的会直接添加到对应对象
    """
    if isinstance(results, list):
        objL = []
        for result in results:
            obj = to_class()
            for r in result.keys():
                obj.__setattr__(r, result[r])
            objL.append(obj)
        return objL
    else:
        try:
            obj = to_class()
            for r in results.keys():
                obj.__setattr__(r, results[r])
            return obj
        except Exception as e:
            print(e)
            return None


def getModel(engine, target_table_name, source_table_name=None):
    """读取数据库表;或copy源表结构,创建新表;返回model类"""
    # Base_Model.metadata.reflect(engine)
    # source_table = Base_Model.metadata.tables[source_table_name]
    # Base_Model.metadata.bind = engine
    # self.insp = sqlalchemy.inspect(self.engine)
    # sqlhelper.insp.get_schema_names()
    # sqlhelper.insp.get_table_names(schema='bxflb')
    # sqlhelper.insp.get_columns('users2', schema='bxflb')  # 表名，库名
    # reflect 映射dash_base库下的表结构
    # sqlhelper.Base.metadata.reflect(bind=sqlhelper.engine, schema='bxflb')
    # print([i for i in sqlhelper.Base.metadata.tables.values()])

    # 表结构
    target_kws = {
        '__table__': Table(
            target_table_name if source_table_name is None else source_table_name,  # #判断是否从source_table_name复制表结构
            Base_Model.metadata,
            extend_existing=True,
            autoload_with=engine,
        ),
        '__tablename__': target_table_name,
    }
    target_kws['__table__'].name = target_table_name  # @关键语句，决定是否创建新表

    Base_Model.metadata.create_all(engine)  # 创建表
    return type(target_table_name, (Base_Model,), target_kws)


def Data_Model_2_py(tablename, key='default'):
    """
    根据已有数据库生成模型
    sqlacodegen --tables users2 --outfile db.py mysql+pymysql://sandorn:123456@cdb-lfp74hz4.bj.tencentcdb.com:10014/bxflb?charset=utf
    """
    import subprocess

    com_list = f'sqlacodegen --tables {tablename} --outfile {tablename}_db.py {connect_str(key)}'
    subprocess.call(com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
