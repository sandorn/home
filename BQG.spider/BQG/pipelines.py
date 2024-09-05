# !/usr/bin/env python
"""
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-12 15:44:47
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-07-08 20:53:26

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
"""

import codecs
import csv
import json

from scrapy.exporters import JsonItemExporter
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from twisted.enterprise import adbapi
from xt_database.cfg import DB_CFG
from xt_database.aiomysql import AioMysql
from xt_database.aiomysqlpool import AioSqlPool
from xt_database.asynsqlorm import AsynSqlOrm
from xt_database.mysql import DbEngine as mysql
from xt_database.sqlorm import SqlConnection
from xt_database.sqlorm_meta import Base_Model


def make_model(_BOOKNAME):
    # # 类工厂函数

    class table_model(Base_Model):
        # Base_Model 继承自from xt_DAO.xt_chemyMeta.Model_Method_Mixin
        __tablename__ = _BOOKNAME
        __table_args__ = {"extend_existing": True}

        ID = Column(INTEGER(10), primary_key=True)
        BOOKNAME = Column(VARCHAR(255), nullable=False)
        INDEX = Column(INTEGER(10), nullable=False)
        ZJNAME = Column(VARCHAR(255), nullable=False)
        ZJTEXT = Column(TEXT, nullable=False)
        ZJHERF = Column(VARCHAR(255), nullable=False)

        def __repr__(self):
            return (
                f"({self.ID},{self.BOOKNAME},{self.INDEX},{self.ZJNAME},{self.ZJHERF})"
            )

    return table_model


class PipelineToSqlTwisted:
    # https://blog.51cto.com/u_15127513/4786890
    @classmethod
    def from_settings(cls, settings):
        # #用于获取settings配置文件中的信息
        cfg = DB_CFG["TXbook"].value
        cfg.pop("type", None)
        dbpool = adbapi.ConnectionPool("MySQLdb", **cfg)
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(f"PipelineToSqlTwisted 异步insert异常 | {failure} | item:{item}")

    def do_insert(self, cursor, item):
        # 根据item构建sql语句并执行
        insert_sql = """
        Insert into %s(`BOOKNAME`, `INDEX`, `ZJNAME`, `ZJTEXT`, `ZJHERF`) values('%s', %d, '%s', '%s', '%s')
        """ % (
            item["BOOKNAME"],
            item["BOOKNAME"],
            item["INDEX"],
            item["ZJNAME"],
            item["ZJTEXT"],
            item["ZJHERF"],
        )
        cursor.execute(insert_sql)


class PipelineToAiomysqlpool:
    def __init__(self):
        self.sql_list = []

    def process_item(self, item, spider):
        self.sql_list.append(self.Create_Sql(item))
        return item

    def Create_Sql(self, item):
        return """
        Insert into %s(`BOOKNAME`, `INDEX`, `ZJNAME`, `ZJTEXT`, `ZJHERF`) values('%s', %d, '%s', '%s', '%s')
        """ % (
            item["BOOKNAME"],
            item["BOOKNAME"],
            item["INDEX"],
            item["ZJNAME"],
            item["ZJTEXT"],
            item["ZJHERF"],
        )

    def close_spider(self, spider):
        AioSqlPool("TXbook").executeall(self.sql_list)


class PipelineToAsynorm:
    def __init__(self):
        self.db = set()
        self.sqlconn = None

    def process_item(self, item, spider):
        self._BOOKNAME = item["BOOKNAME"]
        if self._BOOKNAME not in self.db:
            self.db.add(self._BOOKNAME)
            self.DBtable = make_model(self._BOOKNAME)
        if self.sqlconn is None:
            self.sqlconn = AsynSqlOrm(self.DBtable, "TXbook", self._BOOKNAME)

        self.sqlconn.insert(dict(item), autorun=False)

        return item

    def close_spider(self, spider):
        if self.sqlconn is not None:
            self.sqlconn.run_in_loop()
            del self.db


class PipelineToAiomysql:
    def __init__(self):
        self.sql_list = []
        self.AioMysql = None

    def process_item(self, item, spider):
        if self.AioMysql is None:
            self.AioMysql = AioMysql("TXbook", item["BOOKNAME"])
        self.AioMysql.insert(dict(item), autorun=False)
        return item

    def close_spider(self, spider):
        if self.AioMysql is not None:
            self.AioMysql.run_in_loop()


class PipelineToSqlalchemy:
    def __init__(self):
        self.db = set()

    def process_item(self, item, spider):
        _BOOKNAME = item["BOOKNAME"]
        if _BOOKNAME not in self.db:
            self.db.add(_BOOKNAME)
            DBtable = make_model(_BOOKNAME)
            self.sqlconn = SqlConnection(DBtable, "TXbook")

        self.sqlconn.insert(item)
        return item

    def close_spider(self, spider):
        del self.sqlconn
        del self.db


class PipelineToMysql:
    def __init__(self):
        self.conn = mysql("TXbook", "MySQLdb")
        self.db = set()

    def process_item(self, item, spider):
        _BOOKNAME = item["BOOKNAME"]
        if _BOOKNAME not in self.db:
            # 避免重复创建数据库
            Csql = f"Create Table If Not Exists {_BOOKNAME}(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,`ZJHERF` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)"
            self.conn.execute(Csql)
            self.db.add(_BOOKNAME)

        _result = self.conn.get_all_from_db(_BOOKNAME)
        assert isinstance(_result, (list, tuple))
        ZJHERF_list = [res[5] for res in _result]

        if item["ZJHERF"] in ZJHERF_list:
            self.conn.update(dict(item), {"ZJHERF": item["ZJHERF"]}, _BOOKNAME)
        else:
            self.conn.insert(dict(item), _BOOKNAME)
        return item

    def close_spider(self, spider):
        del self.conn
        del self.db


class PipelineToTxt:
    def __init__(self):
        self.content_list = []
        self.file = {}

    def process_item(self, item, spider):
        bookname = item["BOOKNAME"]
        self.file[bookname] = open(f"{bookname}.txt", "w", encoding="utf-8")
        self.file[bookname].write(
            f"-----------------------{bookname}-----------------------\n"
        )
        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        list_sorted = sorted(self.content_list, key=lambda x: x["INDEX"])
        for item in list_sorted:
            _BOOKNAME = item["BOOKNAME"]
            self.file[_BOOKNAME].write(
                f"----------{_BOOKNAME}----------{item['INDEX']}----------{item['ZJNAME']}----------\n"
            )
            self.file[_BOOKNAME].write(item["ZJTEXT"])

        for key in self.file.keys():
            self.file[key].close()


class PipelineToJson:
    def __init__(self):
        self.file = ""

    def process_item(self, item, spider):
        self.file = codecs.open(item["BOOKNAME"] + ".json", "a", encoding="utf-8")
        # 存储数据，将 Item 实例作为 json 数据写入到文件中
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class PipelineToJsonExp:
    # # 调用 scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open("Items_exp.json", "wb")
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(
            self.file, encoding="utf-8", ensure_ascii=False
        )
        self.exporter.start_exporting()  # 开启倒数

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class PipelineToCsv:
    def __init__(self):
        self.file = any

    def process_item(self, item, spider):
        self.file = codecs.open(item["BOOKNAME"] + ".csv", "a", encoding="utf-8")
        # 存储数据，将 Item 实例作为 json 数据写入到文件中
        res = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(res + "\n")
        return item

    def close_spider(self, spider):
        self.file.close()


class Pipeline2Csv:
    def __init__(self):
        self.file = ""
        self.writer = ""

    def process_item(self, item, spider):
        self.file = open(item["BOOKNAME"] + "_2.csv", "a", newline="")
        self.writer = csv.writer(self.file, dialect="excel")  # csv写法
        self.writer.writerow(
            [item["BOOKNAME"], item["INDEX"], item["ZJNAME"], item["ZJTEXT"]]
        )
        return item

    def close_spider(self, spider):
        self.file.close()
