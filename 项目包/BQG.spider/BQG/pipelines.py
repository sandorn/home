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
import MySQLdb
import numpy
import pandas
from xt_DAO.xt_mysql import engine as mysql
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
from xt_DAO.dbconf import db_conf
from xt_String import align
from xt_Ls_Bqg import arrangeContent
from scrapy.exceptions import DropItem
from copy import deepcopy


class PipelineCheck(object):
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        item['ZJNAME'] = item['ZJNAME'].strip('\r\n').replace(
            u'\u3000', u' ').replace(u'\xa0', u' ')
        if item['ZJNAME'] in self.names_seen:
            print("--《%s》%s|章节重复" % ((item['BOOKNAME'], item['ZJNAME'])))
            raise DropItem("PipelineCheck Duplicate item found: %s" % item)
        else:
            item['ZJTEXT'] = arrangeContent(item['ZJTEXT'])

            self.names_seen.add(item['ZJNAME'])
            return item

    def close_spider(self, spider):
        del self.names_seen


class PipelineToSqlTwisted(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.db = set()

    def open_spider(self, spider):
        # #当spider被开启时调用该方法。
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
        print(
            f"--《  {align(item['BOOKNAME'], 20, 'center')}  》\t {align(item['ZJNAME'], 40)} \t|记录入库"
        )
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(f'handle_error:{failure}\n item:{item}')

    def close_spider(self, spider):
        # #当spider被关闭时，这个方法被调用
        pass

    def do_insert(self, cursor, item):
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
        Insert into %s(`BOOKNAME`, `INDEX`, `ZJNAME`, `ZJTEXT`, `ZJHERF`) values('%s', %d, '%s', '%s', '%s')
        """ % (item['BOOKNAME'], item['BOOKNAME'], item['INDEX'],
               item['ZJNAME'], item['ZJTEXT'], item['ZJHERF'])
        cursor.execute(insert_sql)


class PipelineToTxt(object):
    def __init__(self):
        self.file_dict = set()
        self.content_list = {}
        self.file = {}
        self.list_sorted = {}

    def process_item(self, item, spider):
        bookname = item['BOOKNAME']
        if bookname not in self.file_dict:
            self.file_dict.add(bookname)
            self.file[bookname] = open(bookname + '.txt',
                                       'w',
                                       encoding='utf-8')
            self.file[bookname].write(
                "-----------------------%s-----------------------\n" %
                (bookname))
        return item

    def close_spider(self, spider):
        config = deepcopy(db_conf['TXbook'])
        if 'type' in config: config.pop('type')

        self.connect = MySQLdb.connect(**config)

        for bookname in self.file_dict:
            # 从MySQL里提数据
            sql = "SELECT * FROM %s;" % bookname
            # 读MySQL数据到DataFrame
            pDataFrame = pandas.read_sql(sql, self.connect)
            # 将DataFrame转换为list
            self.content_list[bookname] = numpy.array(pDataFrame).tolist()
            # @'INDEX'  将list排序
            self.list_sorted[bookname] = sorted(self.content_list[bookname],
                                                key=lambda x: x[2])
            self.content_list[bookname].sort(key=lambda x: x[2])

            for item in self.list_sorted[bookname]:
                self.file[item[1]].write(
                    "----------%s----------%d----------%s----------\n" %
                    (item[1], item[2], item[3]))
                self.file[item[1]].write(item[4] + '\n')

            print('--《%s》文本TEXT文件存储完毕！！\t' % bookname)
            self.file[bookname].close()
        self.connect.close()


class PipelineToSqlalchemy(object):
    def __init__(self):
        print(1111)
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
        return item

    def close_spider(self, spider):
        del self.connect


class PipelineToSql(object):
    def __init__(self):
        self.connect = mysql('TXbook')
        self.db = set()

    def process_item(self, item, spider):
        _BOOKNAME = item['BOOKNAME']
        _INDEX = item['INDEX']
        _ZJNAME = item['ZJNAME']
        _ZJTEXT = item['ZJTEXT']
        _sql_dict = {
            'BOOKNAME': _BOOKNAME,
            'INDEX': _INDEX,
            'ZJNAME': _ZJNAME,
            'ZJTEXT': _ZJTEXT
        }
        self.connect.insert(_sql_dict, _BOOKNAME)
        # self.connect.commit()
        return item

    def process_item0(self, item, spider):
        # !数据库查重，备份
        _BOOKNAME = item['BOOKNAME']
        if _BOOKNAME not in self.db:
            # 避免重复创建数据库
            Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)' % _BOOKNAME
            self.connect.execute(Csql)
            self.connect.commit()
            self.db.add(_BOOKNAME)

        _INDEX = item['INDEX']
        _ZJNAME = item['ZJNAME']
        _ZJTEXT = item['ZJTEXT']

        # 避免重复插入章节
        isnullSql = """
        SELECT 1  FROM %s WHERE ZJNAME='%s' LIMIT 1
        """ % (_BOOKNAME, _ZJNAME)
        ret = self.connect.query(isnullSql)
        if ret:
            print('书籍:' + _BOOKNAME + '|章节:' + _ZJNAME + '|已存在，更新数据')
            _sql = """
            UPDATE %s SET ZJTEXT = '%s' WHERE ZJNAME='%s'
            """ % (
                _BOOKNAME,
                _ZJTEXT,
                _ZJNAME,
            )
            self.connect.update(_sql)
            self.connect.commit()
        else:
            _sql = """
            Insert into %s (`BOOKNAME`,`INDEX`,`ZJNAME`,`ZJTEXT`) values ('%s',%d ,'%s','%s')
            """ % (_BOOKNAME, _BOOKNAME, _INDEX, _ZJNAME, _ZJTEXT)
            self.connect.insert(_sql)
            self.connect.commit()

        return item

    def close_spider(self, spider):
        del self.connect


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
        self.exporter = JsonItemExporter(self.file,
                                         encoding='utf-8',
                                         ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    # 将 Item 实例导出到 json 文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class PipelineToTxt(object):
    def __init__(self):
        self.content_list = []
        self.file = {}

    def process_item(self, item, spider):
        bookname = item['BOOKNAME']
        self.file[bookname] = open(bookname + '.txt', 'w', encoding='utf-8')
        self.file[bookname].write(
            "-----------------------%s-----------------------\n" % (bookname))

        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        list_sorted = sorted(self.content_list, key=lambda x: x['INDEX'])
        for item in list_sorted:
            # 首先从items里取出数据
            _BOOKNAME = item['BOOKNAME']
            _INDEX = item['INDEX']
            _ZJNAME = item['ZJNAME']
            _ZJTEXT = item['ZJTEXT']

            self.file[_BOOKNAME].write(
                "----------%s----------%d----------%s----------\n" %
                (_BOOKNAME, _INDEX, _ZJNAME))
            self.file[_BOOKNAME].write(_ZJTEXT)
        self.file[_BOOKNAME].close()


class PipelineToCsv(object):
    # 初始化时指定要操作的文件
    def __init__(self):
        self.file = codecs.open('Items.csv', 'w+')

    def process_item(self, item, spider):
        # writer = csv.writer(self.file)
        # writer.writerow((item['BOOKNAME'], item['INDEX'], item['ZJNAME'], item['ZJTEXT']))
        res = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(res + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()


class Pipeline2Csv(object):
    def __init__(self):
        # csv文件的位置,无需事先创建
        self.file = open('Items2.csv', 'w+', newline='')
        # csv写法
        self.writer = csv.writer(self.file, dialect="excel")

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        self.writer.writerow(
            [item['BOOKNAME'], item['INDEX'], item['ZJNAME'], item['ZJTEXT']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()


if __name__ == '__main__':
    from xt_ScrapyRun import ScrapyRun
    import os

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, 'spilerByset')
