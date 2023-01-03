# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
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
'''
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
# DeclarativeMeta  类;declarative_base类工厂
from xt_Class import item_Mixin
from xt_DAO.cfg import make_connect_string  # type: ignore


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


class Model_Method_Mixin(item_Mixin):
    '''解决下标取值赋值、打印显示、生成字段列表'''

    @classmethod
    def columns(cls):
        '''获取字段名列表'''
        cls._c = [col.name for col in cls.__table__.c]
        return cls._c

    @classmethod
    def _fields(cls):
        '''获取字段名列表, # 弃用'''
        return [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__") and attr not in [
            '_sa_class_manager',
            '_decl_class_registry',
            '_sa_instance_state',
            'metadata',
        ]]

    @classmethod
    def make_dict(cls, result):
        '''基于数据库模型转换记录为字典,使用: dbmode.make_dict(records)'''
        if isinstance(result, cls):
            return {key: getattr(result, key) for key in cls.columns()}

        elif isinstance(result, (list, tuple)) and isinstance(result[0], cls):
            return [{key: getattr(item, key) for key in cls.columns()} for item in result]

    def to_dict(self):
        '''单一记录record转字典,使用:record.to_dict()'''
        return self.make_dict(self)

    def __repr__(self):
        return self.__class__.__name__ + str({attr: getattr(self, attr) for attr in self.columns()})

    __str__ = __repr__


Base_Model = declarative_base(cls=Model_Method_Mixin)  # #生成SQLORM基类,混入继承Model_Method_Mixin
'''metadata = Base.metadata'''
'''定义table  引用方式: from xt_DAO.xt_chemyMeta import Base_Model'''

# 若有多个类指向同一张表，那么在后边的类需要把 extend_existing设为True，表示在已有列基础上进行扩展
# 或者换句话说，sqlalchemy 允许类是表的字集，如下：
# __table_args__ = {'extend_existing': True}
# 若表在同一个数据库服务（datebase）的不同数据库中（schema），可使用schema参数进一步指定数据库
# __table_args__ = {'schema': 'AiTestOps_database'}

# sqlalchemy 强制要求必须要有主键字段不然会报错，sqlalchemy在接收到查询结果后还会自己根据主键进行一次去重，因此不要随便设置非主键字段设为primary_key
# 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系，指定 person_id 映射到 person_id 字段; person_id 字段为整型，为主键，自动增长（其实整型主键默认就自动增长）


class parent_model_Mixin:
    '''定义所有数据库表对应的父类,用于混入继承,与Base_Model协同'''
    __abstract__ = True


def inherit_table_cls(target_table_name, table_model_cls, cid_class_dict=None):
    """从指定table_model_cls类继承,重新定义表名；
    target_table_name:目标表名,用于数据库和返回的类名；
    table_model_cls:包含字段信息的表model类,必须有__abstract__ = True,或混入继承
    table_model_cls 例子:
    class table_model(Base_Model):
        __tablename__ = _BOOKNAME
        extend_existing = True

        ID = Column(INTEGER(10), primary_key=True)
        BOOKNAME = Column(VARCHAR(255), nullable=False)
        INDEX = Column(INTEGER(10), nullable=False)
        ZJNAME = Column(VARCHAR(255), nullable=False)
        ZJTEXT = Column(TEXT, nullable=False)
        ZJHERF = Column(VARCHAR(255), nullable=False)
    """
    if cid_class_dict is None: cid_class_dict = {}
    if not isinstance(table_model_cls, DeclarativeMeta):
        raise TypeError('table_model_cls must be a DeclarativeMeta class')
    if not hasattr(table_model_cls, '__abstract__'):
        raise ValueError('table_model_cls must has __abstract__')

    if target_table_name not in cid_class_dict:
        cls = type(
            target_table_name,
            (table_model_cls, ),
            {
                '__table_args__': {
                    "extend_existing": True,  # 允许表已存在
                    # "__abstract__": True,  # 父类模式
                },
                '__tablename__': target_table_name,
            })
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


def getModel(source_table_name, engine, target_table_name=None):
    """读取源表的model类,或copy源表结构,创建新表
    根据engine连接数据库,读取表source_table_name,返回model类
    source_table_name:读取表名
    target_table_name:另存为表名,如为None则返回source_table_name
    engine:create_engine 对象,指定要操作的数据库连接
    """
    Base_Model.metadata.reflect(engine)
    source_table = Base_Model.metadata.tables[source_table_name]

    return_name = target_table_name or source_table_name
    target_kws = {
        '__table__': source_table,
        '__tablename__': return_name,
    }

    if target_table_name is not None:
        target_kws['__table__'].name = target_table_name

    return type(return_name, (Base_Model, ), target_kws)


def Data_Model_2_py(tablename, filename=None, key='default'):
    '''
    根据已有数据库生成模型
    sqlacodegen --tables users2 --outfile db.py mysql+pymysql://sandorn:123456@cdb-lfp74hz4.bj.tencentcdb.com:10014/bxflb?charset=utf
    '''
    import subprocess

    if filename is None:
        filename = tablename
    com_list = f'sqlacodegen --tables {tablename} --outfile {filename}_db.py {make_connect_string(key)}'

    subprocess.call(com_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    # Data_Model_2_py('uuu', 'd:/1.py', 'TXbook')  # 待测试
    from xt_DAO.xt_sqlalchemy import SqlConnection, get_engine
    engine, session = get_engine('TXbx')
    t = getModel('users2', engine)  # , 'users99')
    print(t)
    print(t.columns())
    sqlhelper = SqlConnection(t, 'TXbx')
    res = sqlhelper.select()
    print(res)
