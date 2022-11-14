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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-07-08 20:53:26

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''
import codecs
import csv
import json
from copy import deepcopy

import MySQLdb
import numpy
import pandas
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from xt_DAO.dbconf import db_conf
from xt_DAO.xt_mysql import engine as mysql
from xt_String import align


class PipelineToSqlTwisted(object):
    # https://blog.51cto.com/u_15127513/4786890
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.db = set()

    def open_spider(self, spider):
        pass

    @classmethod
    def from_settings(cls, settings):
        # #用于获取settings配置文件中的信息
        config = deepcopy(db_conf['TXbook'])
        if 'type' in config: config.pop('type')
        dbpool = adbapi.ConnectionPool("MySQLdb", **config)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        print(f"PipelineToSqlTwisted --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(f'PipelineToSqlTwisted 异步insert异常 | {failure} | item:{item}')

    def do_insert(self, cursor, item):
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
        Insert into %s(`BOOKNAME`, `INDEX`, `ZJNAME`, `ZJTEXT`, `ZJHERF`) values('%s', %d, '%s', '%s', '%s')
        """ % (item['BOOKNAME'], item['BOOKNAME'], item['INDEX'], item['ZJNAME'], item['ZJTEXT'], item['ZJHERF'])
        cursor.execute(insert_sql)


class PipelineToSqlalchemy(object):

    def __init__(self):
        self.connect = mysql('TXbook')

    def process_item(self, item, spider):
        _BOOKNAME = item['BOOKNAME']
        _INDEX = item['INDEX']
        _ZJNAME = item['ZJNAME']
        _ZJTEXT = item['ZJTEXT']
        _ZJHERF = item['ZJHERF']

        _sql_dict = {
            'BOOKNAME': _BOOKNAME,
            'INDEX': _INDEX,
            'ZJNAME': _ZJNAME,
            'ZJTEXT': _ZJTEXT,
            'ZJHERF': _ZJHERF,
        }
        self.connect.insert(_sql_dict, _BOOKNAME)
        print(f"PipelineToSqlalchemy --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        del self.connect


class PipelineMysql2Txt(object):

    def __init__(self):
        self.file_set = set()
        self.file = {}

    def process_item(self, item, spider):
        bookname = item['BOOKNAME']
        if bookname not in self.file_set:
            self.file_set.add(bookname)
            self.file[bookname] = open(bookname + '.txt', 'w', encoding='utf-8')
            self.file[bookname].write(f"-----------------------{bookname}-----------------------\n")
        print(f"PipelineMysql2Txt --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        config = deepcopy(db_conf['TXbook'])
        if 'type' in config: config.pop('type')

        self.connect = MySQLdb.connect(**config)

        for bookname in self.file_set:
            # 从MySQL里提数据
            sql_str = "SELECT * FROM %s;" % bookname
            pDataFrame = pandas.read_sql(sql_str, self.connect)  # 读MySQL数据到DataFrame
            content_list = numpy.array(pDataFrame).tolist()  # 将DataFrame转换为list
            content_list.sort(key=lambda x: x[2])  # @'INDEX'  将list排序

            for item in content_list:
                self.file[item[1]].write(f"----------{item[1]}----------{item[2]}----------{item[3]}----------\n{item[4]}\n")

            print(f'PipelineMysql2Txt--《{bookname}》文本TEXT文件存储完毕！！')
            self.file[bookname].close()
        self.connect.close()


class PipelineCheck(object):

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if item['ZJNAME'] in self.names_seen:
            print(f"PipelineCheck--《{item['BOOKNAME']}》--\t {item['ZJNAME']} \t | 记录重复，剔除！！")
            raise DropItem("PipelineCheck Duplicate item found: %s" % item)
        else:
            self.names_seen.add(item['ZJNAME'])
            return item

    def close_spider(self, spider):
        del self.names_seen


class PipelineToTxt:

    def __init__(self):
        self.content_list = []
        self.file = {}

    def process_item(self, item, spider):
        bookname = item['BOOKNAME']
        self.file[bookname] = open(bookname + '.txt', 'w', encoding='utf-8')
        self.file[bookname].write(f"-----------------------{bookname}-----------------------\n")
        print(f"PipelineToTxt --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        list_sorted = sorted(self.content_list, key=lambda x: x['INDEX'])
        for item in list_sorted:
            _BOOKNAME = item['BOOKNAME']
            self.file[_BOOKNAME].write(f"----------{_BOOKNAME}----------{item['INDEX']}----------{item['ZJNAME']}----------\n")
            self.file[_BOOKNAME].write(item['ZJTEXT'])

        for key in self.file.keys():
            self.file[key].close()


class PipelineToSql(object):

    def __init__(self):
        self.connect = mysql('TXbook')
        self.db = set()

    def process_item(self, item, spider):
        _BOOKNAME = item['BOOKNAME']
        if _BOOKNAME not in self.db:
            # 避免重复创建数据库
            Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,`ZJHERF` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)' % _BOOKNAME
            self.connect.worKon(Csql)
            self.db.add(_BOOKNAME)
        _BOOKNAME = item['BOOKNAME']
        _INDEX = item['INDEX']
        _ZJNAME = item['ZJNAME']
        _ZJTEXT = item['ZJTEXT']
        _ZJHERF = item['ZJHERF']

        _sql_dict = {
            'BOOKNAME': _BOOKNAME,
            'INDEX': _INDEX,
            'ZJNAME': _ZJNAME,
            'ZJTEXT': _ZJTEXT,
            'ZJHERF': _ZJHERF,
        }
        self.connect.insert(_sql_dict, _BOOKNAME)
        print(f"PipelineToSql --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        del self.connect


class PipelineToJson:

    def __init__(self):
        self.file = any

    def process_item(self, item, spider):
        self.file = codecs.open(item['BOOKNAME'] + '.json', 'a', encoding='utf-8')
        # 存储数据，将 Item 实例作为 json 数据写入到文件中
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        self.connect.insert(_sql_dict, _BOOKNAME)
        print(f"PipelineToJson --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        self.file.close()


class PipelineToJsonExp:
    # # 调用 scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.file = open('Items_exp.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()  # 开启倒数
        pass

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        print(f"PipelineToJsonExp --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class PipelineToCsv:

    def __init__(self):
        self.file = any

    def process_item(self, item, spider):
        self.file = codecs.open(item['BOOKNAME'] + '.csv', 'a', encoding='utf-8')
        # 存储数据，将 Item 实例作为 json 数据写入到文件中
        res = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(res + '\n')
        print(f"PipelineToCsv --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        self.file.close()


class Pipeline2Csv:

    def __init__(self):
        self.file = any
        self.writer = any

    def process_item(self, item, spider):
        self.file = open(item['BOOKNAME'] + '_2.csv', 'a', newline='')
        self.writer = csv.writer(self.file, dialect="excel")  # csv写法
        self.writer.writerow([item['BOOKNAME'], item['INDEX'], item['ZJNAME'], item['ZJTEXT']])
        print(f"Pipeline2Csv --《  {align(item['BOOKNAME'], 16, 'center')}  》\t INDEX:{item['INDEX']} \t {align(item['ZJNAME'], 30)} \t|记录入库")
        return item

    def close_spider(self, spider):
        self.file.close()


if __name__ == '__main__':
    import os

    from xt_ScrapyRun import ScrapyRun

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, 'spilerByset')
