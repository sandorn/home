# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-07-22 09:23:24
LastEditTime : 2024-09-05 09:56:47
FilePath     : /CODE/xjLib/xt_database/sqlorm.py
Github       : https://github.com/sandorn/home
==============================================================
"""

from typing import Optional, Sequence

import pandas
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from xt_database.cfg import connect_str
from xt_database.sqlorm_meta import ErrorMetaClass, copy_db_model
from xt_singleon import SingletonMetaCls


class SqlConnection(ErrorMetaClass, metaclass=SingletonMetaCls):
    # #限定参数类型
    # Base = xt_class.typed_property("Base", DeclarativeMeta)

    def __init__(
        self, db_key="default", target_table_name=None, source_table_name=None
    ):
        # 创建引擎
        self.engine = create_engine(
            connect_str(db_key),
            max_overflow=0,  # 超过连接池大小外最多创建的连接
            pool_size=5,  # 连接池大小
            pool_timeout=30,  # 池中没有线程最多等待的时间,否则报错
            pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
            echo=True if __name__ == "__main__" else False,
            # echo参数为True时,会显示每条执行的SQL语句
            future=True,  # 使用异步模式
            # poolclass=NullPool, # 禁用池
        )
        self.Base = copy_db_model(
            self.engine, target_table_name, source_table_name
        )  # #获取orm基类,同时创建表
        self.conn = self.engine.connect()  # pd使用
        self.session = sessionmaker(
            bind=self.engine,
            autoflush=True,  # 自动刷新
            # expire_on_commit=True,  # 提交后自动过期
            # class_=AsyncSession,
        )()  # 类直接生成实例
        self.tablename = target_table_name  #  self.Base.name
        # 设置self.params参数
        self.params = {attr: getattr(self.Base, attr) for attr in self.Base.columns()}
        self._query = self.session.query(self.Base)
        # self.Base.query = self.session.query()
        # 获取数据库名列表
        # self.insp = sqlalchemy.inspect(engine)

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        return not exc_type

    def drop_db(self, dbname=None):
        """删除init传入的self.Base"""
        # Base.__table__.drop(self.engine)# 未生效
        # Base.metadata.drop_all(self.engine) # 未生效
        drop_sql = f"DROP TABLE if exists {dbname}"
        self.session.execute(text(drop_sql))

    def run_sql(self, sql: str, *, params: Optional[dict] = None):
        """
        执行并提交单条sql
        Args:
            sql: sql语句
            params: sql参数, eg. {":id_val": 10, ":name_val": "hui"}
            query_one: 是否查询单条,默认False查询多条
            session: 数据库会话对象，如果为 None,则通过装饰器在方法内部开启新的事务
        Returns:
            执行sql的结果
        """
        _sql = text(sql)
        result = self.session.execute(_sql, params)
        return result.all() if result.returns_rows else result.rowcount

    def query(self, whrere_dict: Optional[dict] = None):
        whrere_dict = whrere_dict or {}
        query = self._query.filter_by(**whrere_dict)
        return query.all()

    def insert(self, item_list: list, **kwargs):
        item_in_list = [item_list] if not isinstance(item_list, list) else item_list
        items = [self.Base(**item_dict) for item_dict in item_in_list]
        self.session.add_all(items)
        try:
            self.session.commit()
            return len(items)
        except BaseException:
            self.session.rollback()
            return 0

    def update(self, params: dict, whrere_dict: dict):
        """
        whrere_dict:条件字典;where
        params:更新数据字典:{'字段':字段值}
        """
        query = self._query.filter_by(**whrere_dict)
        updatenum = query.update(params)
        try:
            self.session.commit()
            return updatenum
        except BaseException:
            self.session.rollback()
            return 0

    def delete(self, whrere_dict: dict):
        query = self._query.filter_by(**whrere_dict)
        deleteNum = query.delete()
        try:
            self.session.commit()
            return deleteNum
        except BaseException:
            self.session.rollback()
            return 0

    def select(
        self,
        whrere_dict: Optional[dict] = None,
        Columns_list: Optional[Sequence[str]] = None,
        countNum: Optional[int] = None,
    ):
        """
        whrere_dict:字典,条件 where。类似self.params
        Columns_list:选择的列名
        countNum:返回的记录数
        return:处理后的list,内含dict(未选择列),或tuple(选择列)
        """
        if isinstance(Columns_list, Sequence) and len(Columns_list) > 0:
            __Columns_list = [self.params.get(key) for key in Columns_list]
        else:
            __Columns_list = [self.Base]

        query = self.session.query(*__Columns_list)
        if whrere_dict is not None:
            query = query.filter_by(**whrere_dict)

        return query.limit(countNum).all() if countNum else query.all()

    def from_statement(self, sql, whrere_dict: Optional[dict] = None):
        """使用完全基于字符串的语句"""
        query = self._query.from_statement(text(sql))
        return query.params(**whrere_dict).all() if whrere_dict else query.all()

    def filter_by(self, whrere_dict: Optional[dict], countNum: Optional[int] = None):
        """
        filter_by用于简单查询,不支持比较运算符,不需要额外指定类名。
        filter_by的参数直接支持组合查询。
        仅支持[等于]、[and],无需明示,在参数中以字典形式传入
        """
        query = self._query.filter_by(**whrere_dict)
        return query.limit(countNum).all() if countNum else query.all()

    def pd_get_dict(self, table_name):
        result = pandas.read_sql_table(table_name, con=self.conn)
        data_dict = result.to_dict(orient="records")
        return data_dict if len(data_dict) else False

    def pd_get_list(self, table_name, Columns):
        result = pandas.read_sql_table(table_name, con=self.conn)
        pd_list = result[Columns].drop_duplicates().values.tolist()
        return pd_list if len(pd_list) else False


if __name__ == "__main__":
    query_list = ["select * from users2 where id = 1", "select * from users2"]
    item = [
        {
            "username": "刘新",
            "password": "234567",
            "手机": "13910118122",
            "代理人编码": "10005393",
            "会员级别": "SSS",
            "会员到期日": "9999-12-31 00:00:00",
        }
    ]

    # ASO = SqlConnection("TXbx", "users2", "users")
    ASO = SqlConnection("TXbook", "人道大圣", "dbtable")
    # res = ASO.insert(item)
    # print(1111, res)
    # res = ASO.update(value={"username": "刘澈"}, conds={"ID": 4})
    # print(2222, res)
    # res = ASO.run_sql(query_list[0])
    # print(3333, res)
    res = ASO.query()
    print(4444, res)
    # res = ASO.filter_by({"ID": 4})
    # print(5555, res)
    # resfrom_statement = ASO.from_statement(
    #     "select * from users2 where id=:id", {"id": 5}
    # )
    # print(6666, resfrom_statement)
    # print(ASO.Base.make_dict(resfrom_statement))
    # print(7777, resfrom_statement[0].to_dict(), ASO.Base.to_dict(resfrom_statement[0]))
    # deleNum = ASO.delete({"ID": 3})
    # print(8888, deleNum)
    # res = ASO.select({"username": "刘新军"}, ["ID", "username"], 0)
    # print(9999, res)
