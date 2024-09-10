# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-07-24 08:59:42
LastEditTime : 2024-09-05 09:56:13
FilePath     : /CODE/xjLib/xt_database/sqlorm_meta.py
Github       : https://github.com/sandorn/home
==============================================================
sqlalchemy创建异步sqlite会话 sqlalchemy async_mob64ca140caeb2的技术博客_51CTO博客
https://blog.51cto.com/u_16213668/9806859
"""

from sqlalchemy import INTEGER, Column, DateTime, Table, create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from xt_class import ItemMixin
from xt_database.cfg import connect_str


class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class IdMixin:
    ID = Column(INTEGER, primary_key=True)


class ErrorMetaClass:
    def init_db(self, *args, **kwargs):
        raise NotImplementedError

    def drop_db(self, *args, **kwargs):
        raise NotImplementedError

    def insert(self, *args, **kwargs):
        raise NotImplementedError

    def insert_all(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def select(
        self, *args, **kwargs
    ):  # conditions=None, Columns=None, count=None, show=False):
        raise NotImplementedError

    def from_statement(self, *args, **kwargs):
        raise NotImplementedError

    def filter(self, *args, **kwargs):
        raise NotImplementedError

    def filter_by(self, *args, **kwargs):
        raise NotImplementedError

    def _result_refine(self, *args, **kwargs):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class ModelExt(ItemMixin):
    """SQLAlchemy Base ORM Model Ext,下标取值赋值、打印显示、生成字段列表"""

    def __str__(self):
        return self.__class__.__name__ + str(
            {
                key: getattr(self, key)
                for key in self.keys()
                if getattr(self, key) is not None
            }
        )

    __repr__ = __str__

    @classmethod
    def columns(cls):
        """获取字段名列表"""
        cls._c = [
            col.name for col in cls.__table__.c if col.name != "_sa_instance_state"
        ]
        return cls._c

    @classmethod
    def keys(cls):
        """获取字段名列表"""
        cls._c = cls.__table__.columns.keys()
        return cls._c

    @classmethod
    def make_dict(cls, result):
        """
        基于数据库模型转换记录为字典,使用: dbmode.make_dict(records)
        替换 getattr(item, key) 为 result[key]
        """
        if isinstance(result, cls):
            return {key: result[key] for key in cls.columns()}
        elif (
            isinstance(result, (tuple, list))
            and len(result)
            and isinstance(result[0], cls)
        ):
            return [{key: res[key] for key in cls.columns()} for res in result]
        return result

    def to_dict(self):
        """单一记录record转字典,使用:record.to_dict()"""
        return self.make_dict(self)

    def model_to_dict(self, alias_dict=None, exclude_none=True) -> dict:
        """
        数据库模型转成字典
        Args:
            alias_dict: 字段别名字典
                eg: {"id": "user_id"}, 把id名称替换成 user_id
            exclude_none: 默认排查None值
        Returns: dict
        替换 getattr(item, key) 为 result[key]
        """
        alias_dict = alias_dict or {}
        if exclude_none:
            return {
                alias_dict.get(c.name, c.name): self[c.name]
                for c in self.__table__.columns
                if self[c.name] is not None
            }
        else:
            return {
                alias_dict.get(c.name, c.name): self[c.name]
                for c in self.__table__.columns
            }


Base = Base_Model = declarative_base(cls=ModelExt)
metadata = Base.metadata  # 等价于：sqlalchemy.MetaData()


class ParentBaseModel(Base):
    """定义所有数据库表对应的父类,用于混入继承,与Base_Model协同"""

    __abstract__ = True  # 父类模式
    __extend_existing__ = True  # 允许表已存在


def inherit_table_cls(new_table_name, parent_table_cls):
    """
    从指定parent_table_cls类继承,重新定义表名；
    new_table_name:目标表名,用于数据库和返回的类名；
    parent_table_cls:包含字段信息的表model类,或混入继承
    #@不完善，与 get_db_model() 功能重复
    """

    table_structure = {
        "__tablename__": new_table_name,  # 表名
        "__abstract__": True,  # 非父类模式
        "__extend_existing__": True,  # 允许表已存在
        # "__table__": parent_table_cls.__table__,  # 表结构
    }

    return type(new_table_name, (parent_table_cls,), table_structure)


def copy_db_model(engine, new_table_name, old_table_name=None):
    """
    读取数据库表;或copy源表结构,创建新表;返回model类
    Base_Model.metadata.reflect(engine)
    source_table = Base_Model.metadata.tables[old_table_name]
    Base_Model.metadata.bind = engine
    self.insp = sqlalchemy.inspect(self.engine)
    sqlhelper.insp.get_schema_names()
    sqlhelper.insp.get_table_names(schema='bxflb')
    sqlhelper.insp.get_columns('users2', schema='bxflb')  # 表名，库名
    reflect 映射dash_base库下的表结构
    sqlhelper.Base.metadata.reflect(bind=sqlhelper.engine, schema='bxflb')
    print([i for i in sqlhelper.Base.metadata.tables.values()])
    # 反射单个表
     some_table = Table("some_table", metadata_obj, autoload_with=engine)
     # 覆盖原有属性或增加新属性
     mytable = Table('mytable', metadata_obj,
                    Column('id', Integer, primary_key=True),
                    Column('mydata', Unicode(50)),
                     autoload_with=some_engine)
     # 一次反射所有表
     metadata_obj = MetaData()
     metadata_obj.reflect(bind=engine)
     users_table = metadata_obj.tables['users']
     addresses_table = metadata_obj.tables['addresses']

     # 更底层的反射可以看 inspect
     # 如果我想在异步中使用反射，先使用同步engine得到反射后的metadata_obj对象，在将它传递给Base就可以了
     # 也可以这样
     import asyncio

     from sqlalchemy.ext.asyncio import create_async_engine
     from sqlalchemy.ext.asyncio import AsyncSession
     from sqlalchemy import inspect

     engine = create_async_engine(
     "postgresql+asyncpg://scott:tiger@localhost/test"
     )

     def use_inspector(conn):
         inspector = inspect(conn)
         # use the inspector
         print(inspector.get_view_names())
         # return any value to the caller
         return inspector.get_table_names()

     async def async_main():
         async with engine.connect() as conn:
             tables = await conn.run_sync(use_inspector)
    async with engine.begin() as conn:
         await conn.run_sync(Base.metadata.drop_all)
         await conn.run_sync(Base.metadata.create_all)
    -----------------------------------
    sqlalchemy创建异步sqlite会话 sqlalchemy async
    https://blog.51cto.com/u_16213668/9806859
    """
    inspector = inspect(engine)
    tableinpool = new_table_name in inspector.get_table_names()
    tablename = new_table_name if tableinpool else old_table_name
    # 表结构
    table_structure = {
        "__table__": Table(
            str(tablename),  # 判断从哪个表复制结构
            Base_Model.metadata,
            extend_existing=True,
            autoload_with=engine,
        ),
        "__tablename__": new_table_name,
    }

    if not tableinpool:
        table_structure["__table__"].name = new_table_name
        # @关键语句，决定是否创建新表
        Base.metadata.create_all(engine)  # 创建表
    return type(new_table_name, (Base_Model,), table_structure)
    # return Table(new_table_name, Base.metadata, autoload_with=engine) # 反射单个表


def db_to_model(tablename, key="default"):
    import subprocess

    com_list = f"sqlacodegen {connect_str(key)} --tables {tablename} --outfile={tablename}_db.py "
    return subprocess.call(com_list, shell=True)


def reflect(tablename, key="default"):
    "反射已经存在的表，返回表对象和会话对象"
    engine = create_engine(connect_str(key))
    # 反射数据库表
    Base_Model.metadata.reflect(bind=engine)  # , only=[tablename])
    session = sessionmaker(bind=engine)()
    # 获取表对象
    table_obj = Base_Model.metadata.tables[tablename]
    # table_obj = Table(tablename, Base_Model.metadata, autoload_with=engine)

    # 定义数据模型
    class NewTableModel(ParentBaseModel):
        __table__ = table_obj

    return NewTableModel, session


if __name__ == "__main__":

    def ceshi(key="default"):
        from sqlalchemy import TEXT, VARCHAR, Column

        class table_model(ParentBaseModel, TimestampMixin, IdMixin):
            __tablename__ = "books"
            BOOKNAME = Column(VARCHAR(255), nullable=False)
            INDEX = Column(INTEGER, nullable=False)
            ZJNAME = Column(VARCHAR(255), nullable=False)
            ZJTEXT = Column(TEXT, nullable=False)
            ZJHERF = Column(VARCHAR(255), nullable=False)

        engine = create_engine(connect_str(key))
        ParentBaseModel.metadata.create_all(bind=engine)

        print(1111, db := table_model, db.__mro__)
        # print(1111,db := inherit_table_cls("NT", table_model), db.__mro__)
        print(2222, db.__tablename__, db, db.columns())
        print(
            3333, db.__abstract__, db.__tablename__, db.__extend_existing__, db.metadata
        )
        print(4444, res := db(ID=1, BOOKNAME="sqlorm_bookname"))
        print(5555, res := db(**{"ID": "2", "BOOKNAME": "sqlorm_bookname22"}))
        print(6666, res.to_dict())
        print(7777, res.model_to_dict())

    def ceshi2(tablename, key="default"):
        table_model, sess = reflect(tablename, key)
        print(table_model.columns())
        print(table_model.keys())
        print(sess.query(table_model).all())

    # ceshi()
    # ceshi2("users2")
    # db_to_model("users2")
