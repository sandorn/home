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
@LastEditTime: 2020-02-27 16:56:26

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''

import MySQLdb
import numpy
import pandas

from twisted.enterprise import adbapi

from xjLib.dBrouter import dbconf
from xjLib.mystr import align, Ex_Re_Sub


class PipelineCheck(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        #_showtext = item['ZJTEXT']
        item['ZJTEXT'] = Ex_Re_Sub(
            item['ZJTEXT'],
            {
                '\'': '',
                ' ': ' ',
                '\xa0': ' ',
                '\x0a': '\n',
                # '\b;': '\n',
                '&nbsp;': ' ',
                'app2();': '',
                '笔趣看;': '',
                '\u3000': '',
                'chaptererror();': '',
                'readtype!=2&&(\'vipchapter\n(\';\n\n}': '',
                'm.biqukan.com': '',
                'wap.biqukan.com': '',
                'www.biqukan.com': '',
                'www.biqukan.com。': '',
                '百度搜索“笔趣看小说网”手机阅读:': '',
                '请记住本书首发域名:': '',
                '请记住本书首发域名：': '',
                '笔趣阁手机版阅读网址:': '',
                '笔趣阁手机版阅读网址：': '',
                '[]': '',
                '\r': '\n',
                '\n\n': '\n',
                '\n\n': '\n',
            }
        )
        item['ZJNAME'] = Ex_Re_Sub(
            item['ZJNAME'],
            {
                '\'': '',
                ' ': ' ',
                '\xa0': ' ',
                '\x0a': '\n',
            }
        )
        return item


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
        print('--《' + align(item['BOOKNAME'], 20, 'center') + '》\t' + align(item['ZJNAME'], 40) + '\t|记录入库')
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
        Insert into %s(`BOOKNAME`, `INDEX`, `ZJNAME`, `ZJTEXT`, `ZJHERF`) values('%s', %d, '%s', '%s', '%s')
        """ % (
            item['BOOKNAME'],
            item['BOOKNAME'],
            item['INDEX'],
            item['ZJNAME'],
            item['ZJTEXT'],
            item['ZJHERF'],
        )
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
            self.file[bookname] = open(bookname + '.txt', 'w', encoding='utf-8')
            self.file[bookname].write("-----------------------%s-----------------------\n" % (bookname))
        return item

    def close_spider(self, spider):
        self.connect = MySQLdb.connect(**dbconf['TXbook'])

        for bookname in self.file_dict:
            # 从MySQL里提数据
            sql = "SELECT * FROM %s;" % bookname
            # 读MySQL数据到DataFrame
            pDataFrame = pandas.read_sql(sql, self.connect)
            # 将DataFrame转换为list
            self.content_list[bookname] = numpy.array(pDataFrame).tolist()
            # 将list排序
            self.list_sorted[bookname] = sorted(self.content_list[bookname], key=lambda x: x[2])  # @'INDEX'

            for item in self.list_sorted[bookname]:
                self.file[item[1]].write("----------%s----------%d----------%s----------\n" % (item[1], item[2], item[3]))
                self.file[item[1]].write(item[4] + '\n')

            print('--《%s》文本TEXT文件存储完毕！！\t' % bookname)
            self.file[bookname].close()
        self.connect.close()
