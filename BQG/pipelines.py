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
#LastEditTime : 2020-06-04 11:24:47

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''

import MySQLdb
import numpy
import pandas
from twisted.enterprise import adbapi
from xt_DAO.dbconf import db_conf
from xt_String import align
from xt_Ls import arrangeContent


class PipelineCheck(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        item['ZJNAME'] = item['ZJNAME'].strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        item['ZJTEXT'] = arrangeContent(item['ZJTEXT'])
        return item


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
        if 'type' in db_conf['TXbook']:
            db_conf['TXbook'].pop('type')
        dbpool = adbapi.ConnectionPool("MySQLdb", **db_conf['TXbook'])
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
        # #当spider被关闭时，这个方法被调用
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
        self.connect = MySQLdb.connect(**db_conf['TXbook'])

        for bookname in self.file_dict:
            # 从MySQL里提数据
            sql = "SELECT * FROM %s;" % bookname
            # 读MySQL数据到DataFrame
            pDataFrame = pandas.read_sql(sql, self.connect)
            # 将DataFrame转换为list
            self.content_list[bookname] = numpy.array(pDataFrame).tolist()
            # @'INDEX'  将list排序
            # self.list_sorted[bookname] = sorted(self.content_list[bookname], key=lambda x: x[2])
            self.content_list[bookname].sort(key=lambda x: x[2])

            for item in self.list_sorted[bookname]:
                self.file[item[1]].write("----------%s----------%d----------%s----------\n" % (item[1], item[2], item[3]))
                self.file[item[1]].write(item[4] + '\n')

            print('--《%s》文本TEXT文件存储完毕！！\t' % bookname)
            self.file[bookname].close()
        self.connect.close()


if __name__ == '__main__':
    from xt_ScrapyRun import ScrapyRun
    import os

    # 获取当前脚本路径
    filepath = os.path.abspath(__file__)
    dirpath = os.path.dirname(filepath)
    ScrapyRun(dirpath, 'spiler')
