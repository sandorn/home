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
https://blog.51cto.com/u_16213668/9806859
"""

from __future__ import annotations

from pydantic import BaseModel, constr
from sqlalchemy import INTEGER, Column, DateTime, Table, create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from xt_class import ItemMixin
from xt_database.cfg import connect_str


class User(BaseModel):
    """https://zhuanlan.zhihu.com/p/696103020"""

    id: int
    username: str
    password: constr(min_length=8)

    # @field_validator('password')
    # def validate_password(self, value):
    #     if not any(char.isdigit() for char in value):
    #         raise ValueError('Password must contain at least one digit')
    #     if not any(char.isalpha() for char in value):
    #         raise ValueError('Password must contain at least one letter')
    #     return value


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

    # conditions=None, Columns=None, count=None, show=False):
    def select(self, *args, **kwargs):
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
        return self.__class__.__name__ + str({key: getattr(self, key) for key in self.keys() if getattr(self, key) is not None})

    __repr__ = __str__

    @classmethod
    def columns(cls):
        """获取字段名列表"""
        cls._c = [col.name for col in cls.__table__.c if col.name != '_sa_instance_state']
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
        """
        if isinstance(result, cls):
            return {key: result[key] for key in cls.columns()}
        if isinstance(result, (tuple, list)) and len(result) and isinstance(result[0], cls):
            return [{key: res[key] for key in cls.columns()} for res in result]
        return result

    def to_dict(self, alias_dict: dict[str, str] | None = None, exclude_none: bool = False) -> dict[str, any]:
        """
        单一记录record转字典,使用:record.to_dict()

        Args:
            alias_dict: 字段别名字典，用于重命名字段
                示例: {"id": "user_id"} - 将id字段名替换为user_id
            exclude_none: 是否排除值为None的字段，默认为False

        Returns:
            转换后的字典，键为字段名(或别名)，值为字段值

        注：本方法使用self[key]访问字段值，替换了原有的getattr(item, key)方式
        """
        # 初始化别名字典（如果未提供）
        alias_dict = alias_dict or {}
        
        # 创建结果字典
        result_dict = {}
        
        # 遍历模型的所有列
        for column in self.__table__.columns:
            # 获取字段名和对应的值
            key = column.name
            value = self[key]
            
            # 如果需要排除None值且当前值为None，则跳过
            if exclude_none and value is None:
                continue
            
            # 获取别名（如果有），否则使用原字段名
            alias_name = alias_dict.get(key, key)
            
            # 添加到结果字典
            result_dict[alias_name] = value
        
        return result_dict


Base = declarative_base(cls=ModelExt)


class BaseModel(Base):
    """定义所有数据库表对应的父类,用于混入继承,与BaseModel协同"""

    __abstract__ = True  # 父类模式
    __extend_existing__ = True  # 允许表已存在


def copy_db_model(engine, new_table_name, old_table_name=None):
    """
    """
    inspector = inspect(engine)
    tableinpool = new_table_name in inspector.get_table_names()
    tablename = new_table_name if tableinpool else old_table_name
    # 表结构
    table_structure = {
        '__table__': Table(
            str(tablename),  # !判断从哪个表复制结构
            BaseModel.metadata,  # 绑定元数据
            extend_existing=True,  # 允许表已存在
            autoload_with=engine,  # 从引擎加载表结构
        ),
        '__tablename__': new_table_name,
    }

    if not tableinpool:   # 表不存在时，创建新表
        table_structure['__table__'].name = new_table_name
        Base.metadata.create_all(engine)
    return type(new_table_name, (BaseModel,), table_structure)
    # return Table(new_table_name, Base.metadata, autoload_with=engine) # 反射单个表


def db_to_model(tablename, key='default'):
    import subprocess  # noqa: S404

    com_list = f'sqlacodegen {connect_str(key)} --tables {tablename} --outfile={tablename}_db.py '
    return subprocess.call(com_list, shell=True)  # noqa: S602


def reflect(tablename, key='default'):
    "反射已经存在的表，返回表对象和会话对象"
    engine = create_engine(connect_str(key))
    # 反射数据库表
    BaseModel.metadata.reflect(bind=engine, only=[tablename])
    session = sessionmaker(bind=engine)()
    # 获取表对象
    # table_obj = BaseModel.metadata.tables[tablename]
    table_obj = Table(tablename, Base.metadata, autoload_with=engine)

    # 为映射到的数据模型添加方法(继承自 BaseModel-ModelExt)
    class TableModel(BaseModel):
        __table__ = table_obj

    return TableModel, session


if __name__ == '__main__':

    def ceshi(key='default'):
        from sqlalchemy import TEXT, VARCHAR, Column

        class TableModel(BaseModel, TimestampMixin, IdMixin):
            __tablename__ = 'books'
            BOOKNAME = Column(VARCHAR(255), nullable=False)
            INDEX = Column(INTEGER, nullable=False)
            ZJNAME = Column(VARCHAR(255), nullable=False)
            ZJTEXT = Column(TEXT, nullable=False)
            ZJHERF = Column(VARCHAR(255), nullable=False)

        engine = create_engine(connect_str(key))
        Base.metadata.create_all(bind=engine)

        print(1111, db := TableModel, db.__mro__)
        # print(1111,db := inherit_table_cls("NT", table_model), db.__mro__)
        print(2222, db.__tablename__, db, db.columns())
        print(3333, db.__abstract__, db.__tablename__, db.__extend_existing__, db.metadata)
        print(4444, res := db(ID=1, BOOKNAME='sqlorm_bookname'))
        print(5555, res2 := db(**{'ID': '2', 'BOOKNAME': 'sqlorm_bookname22'}))
        print(6666, res.to_dict())
        print(7777, db.make_dict(res2))

    def ceshi2(tablename, key='default'):
        table_model, sess = reflect(tablename, key)
        print(table_model.columns())
        print(table_model.keys())
        print(sess.query(table_model).all())

    # ceshi()
    ceshi2('users2')
    # db_to_model("users2")
