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
@LastEditors: Even.Sand
@LastEditTime: 2020-03-23 15:00:51

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''


import codecs
import csv
import json

import MySQLdb
import pandas
import redis
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

from xjLib.dBrouter import dbconf
from xjLib.mssql import MySQLConnection as mysql
from xjLib.mystr import multiple_replace


class PipelineCheck(object):
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        if item['ZJNAME'] in self.names_seen:
            print("--《%s》%s|章节重复" % ((item['BOOKNAME'], item['ZJNAME'])))
            raise DropItem("PipelineCheck Duplicate item found: %s" % item)
        else:
            _showtext = item['ZJTEXT'].replace('[笔趣看\xa0\xa0www.biqukan.com]', '')
            item['ZJTEXT'] = multiple_replace(_showtext, {'\xa0': '', '&nbsp;': '', '\\b;': '', 'app2();': '', 'chaptererror();': '', '百度搜索“笔趣看小说网”手机阅读:m.biqukan.com': '', '请记住本书首发域名:www.biqukan.com。笔趣阁手机版阅读网址:wap.biqukan.com': '', '[笔趣看www.biqukan.com]': '', '\n\n': '\n', '\n\n': '\n', '请记住本书首发域名：www.biqukan.com。笔趣阁手机版阅读网址：wap.biqukan.com': '', '\u3000': '', 'readtype!=2&&(\'vipchapter\n(\';\n\n}': ''})

            self.names_seen.add(item['ZJNAME'])
            return item

    def close_spider(self, spider):
        del self.names_seen


class PipelineSqlCheck(object):
    def __init__(self):
        self.connect = MySQLdb.connect(**dbconf['TXbook'])
        self.cur = self.connect.cursor()
        self.db = set()
        self.redb = set()
        self.redis_db = {}
        self.redis_dict = {}

    def process_item(self, item, spider):
        _BOOKNAME = item['BOOKNAME']

        if _BOOKNAME not in self.db:
            # 避免重复创建数据库
            Csql = 'Create Table If Not Exists %s(`ID` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,  `BOOKNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `INDEX` int(10) NOT NULL,  `ZJNAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  `ZJTEXT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,  PRIMARY KEY (`ID`) USING BTREE)' % _BOOKNAME
            self.cur.execute(Csql)
            self.connect.commit()
            self.db.add(_BOOKNAME)

            self.redis_db[_BOOKNAME] = redis.Redis(host='127.0.0.1', port=6379, db=4)
            self.redis_dict[_BOOKNAME] = "ZJNAME"  # k相当于字典名称

            # 删除全部key
            self.redis_db[_BOOKNAME].flushdb()
            sql = "SELECT ZJNAME FROM %s;" % _BOOKNAME  # 从MySQL里提数据
            pandasData = pandas.read_sql(sql, self.connect)  # 读MySQL数据

            for res in pandasData['ZJNAME']:
                self.redis_db[_BOOKNAME].hset(self.redis_dict[_BOOKNAME], res, 0)
            self.redb.add(_BOOKNAME)

        _ZJNAME = item['ZJNAME']
        if self.redis_db[_BOOKNAME].hexists(self.redis_dict[_BOOKNAME], _ZJNAME):
            # item和key字段对比，存在就丢掉item;不存在则添加到字典，返回item
            print("--《%s》%s|记录已入库" % (_BOOKNAME, _ZJNAME))
            raise DropItem("PipelineSqlCheck Duplicate item found: %s" % item)
        else:
            self.redis_db[_BOOKNAME].hset(self.redis_dict[_BOOKNAME], _ZJNAME, 0)
            return item

    def open_spider(self, spider):
        # 可选实现，当spider被开启时，这个方法被调用。
        pass

    def close_spider(self, spider):
        del self.redis_dict
        del self.redis_db
        del self.redb
        del self.cur
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
        _sql = """
        Insert into %s (`BOOKNAME`,`INDEX`,`ZJNAME`,`ZJTEXT`) values ('%s',%d ,'%s','%s')
        """ % (_BOOKNAME, _BOOKNAME, _INDEX, _ZJNAME, _ZJTEXT)
        self.connect.insert(_sql)
        self.connect.commit()

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
            """ % (_BOOKNAME, _ZJTEXT, _ZJNAME,)
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


class PipelineToSqlTwisted(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.db = set()

    @classmethod
    def from_settings(cls, settings):
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbconf['TXbook'])
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def close_spider(self, spider):
        pass

    def do_insert(self, cursor, item):
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
        Insert into % s(`BOOKNAME`, `INDEX`, `ZJNAME`, `ZJTEXT`) values('%s', %d, '%s', '%s')
        """ % (item['BOOKNAME'], item['BOOKNAME'], item['INDEX'], item['ZJNAME'], item['ZJTEXT'])
        cursor.execute(insert_sql)

    def do_update(self, cursor, item):
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        update_sql = """
             UPDATE %s SET ZJTEXT = '%s' WHERE ZJNAME ='%s'
        """ % (item["BOOKNAME"], item['ZJTEXT'], item['ZJNAME'])
        cursor.execute(update_sql)


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


class PipelineToTxt(object):

    def __init__(self):
        self.content_list = []
        self.file = {}

    def process_item(self, item, spider):
        bookname = item['BOOKNAME']
        self.file[bookname] = open(bookname + '.txt', 'w', encoding='utf-8')
        self.file[bookname].write("-----------------------%s-----------------------\n" % (bookname))

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

            self.file[_BOOKNAME].write("----------%s----------%d----------%s----------\n" % (_BOOKNAME, _INDEX, _ZJNAME))
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
        self.writer.writerow([item['BOOKNAME'], item['INDEX'], item['ZJNAME'], item['ZJTEXT']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
