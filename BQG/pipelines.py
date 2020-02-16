# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-12 15:44:47
@LastEditors  : Even.Sand
@LastEditTime : 2020-02-16 23:28:51

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''

from twisted.enterprise import adbapi
from scrapy.exporters import JsonItemExporter
from xjLib.mssql import MySQLConnection as mysql
from xjLib.dBrouter import dbconf
import codecs
import json


class PipelineToTxt(object):

    def __init__(self):
        self.content_list = []
        self.file = {}

    def process_item(self, item, spider):
        bookname = item["书名"]
        self.file[bookname] = open(bookname + '.txt', 'w', encoding='utf-8')
        self.file[bookname].write("-----------------------%s-----------------------\n" % (bookname))

        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        list_sorted = sorted(self.content_list, key=lambda x: x['index'])
        for item in list_sorted:
            # 首先从items里取出数据
            _BOOKNAME = item['书名']
            _INDEX = item['index']
            _ZJNAME = item['章节名称']
            _ZJTEXT = item['章节正文']

            self.file[_BOOKNAME].write("----------%s----------%d----------%s----------\n" % (_BOOKNAME, _INDEX, _ZJNAME))
            self.file[_BOOKNAME].write(_ZJTEXT)
        self.file[_BOOKNAME].close()


class PipelineToJson:

    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('Items.json', 'w', encoding='utf-8')

    def open_spider(self, spider):
        # 可选实现，当spider被开启时，这个方法被调用。
        pass

    def process_item(self, item, spider):
        # 存储数据，将 Item 实例作为 json 数据写入到文件中
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        # 可选实现，当spider被关闭时，这个方法被调用
        self.file.close()


class PipelineToJsonExp:
    # 调用 scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        self.file = open('Items_exp.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class PipelineToSql(object):
    def __init__(self):
        self.connect = mysql('TXbook')

    def process_item(self, item, spider):
        _BOOKNAME = item['书名']
        Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)' % _BOOKNAME
        self.connect.execute(Csql)
        self.connect.commit()

        _INDEX = item['index']
        _ZJNAME = item['章节名称']
        _ZJTEXT = item['章节正文']

        _sql = 'Insert into %s (`BOOKNAME`,`INDEX`,`ZJNAME`,`ZJTEXT`) values (\'%s\',%d ,\'%s\',\'%s\')' % (_BOOKNAME, _BOOKNAME, _INDEX, _ZJNAME, _ZJTEXT)
        self.connect.insert(_sql)
        self.connect.commit()

        return item

    def close_spider(self, spider):
        # del self.connect
        self.connect.close()

    def handle_error(self, e):
        # log.err(e)
        print(e)


class PipelineToSqlTwisted(object):
    def __init__(self, DBname='TXbook'):
        # 指定擦做数据库的模块名和数据库参数参数
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbconf[DBname])
        self.Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)'

    def process_item(self, cursor, item, spider):
        _BOOKNAME = item['书名']
        cursor.execute(self.Csql, _BOOKNAME)

        # 指定操作方法和操作的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 指定异常处理方法
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
