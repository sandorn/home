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
@LastEditTime : 2020-02-14 15:48:58

# Define your item pipelines here#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
'''


import re
from xjLib.string import cn2num  # 章节数字转换
import xjLib.mysql as mysql


class BqgPipeline(object):

    def __init__(self):
        self.content_list = []

        self.db = mysql.MysqlHelp()
        # 使用execute方法执行SQL语句
        self.db.cur.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取一条数据库。
        print("数据库版本：", self.db.cur.fetchone())

    def process_item(self, item, spider):
        bookname = item["书名"]
        self.file = open(bookname + '.txt', 'w', encoding='utf-8')
        self.file.write("-----------------------%s-----------------------\n" % (bookname))

        name = item['章节名称']
        chapter = re.findall(r"第(.*)章", name)
        item['序号'] = cn2num(chapter)
        self.content_list.append(item)
        return item

    def close_spider(self, spider):
        list_sorted = sorted(self.content_list, key=lambda x: x['序号'])
        for item in list_sorted:
            # 首先从items里取出数据
            _BOOKNAME = item['书名']
            _INDEX = item['index']
            _XUHAO = item['序号']
            _ZJNAME = item['章节名称']
            _ZJTEXT = self.multiple_replace(item['章节正文'], {'\xa0': '', '&nbsp;': '', '\\b;': '', 'app2();': '', 'chaptererror();': '', '百度搜索“笔趣看小说网”手机阅读：m.biqukan.com': '', '请记住本书首发域名：www.biqukan.com。笔趣阁手机版阅读网址：wap.biqukan.com': '', '[笔趣看www.biqukan.com]': '', '\n\n': '\n', '\n\n': '\n', '\n\n': '\n'}) + "\n"

            self.file.write("----------------%d----------------- %s--------------\n" % (_XUHAO, _ZJNAME))
            self.file.write(_ZJTEXT)

            try:
                _sql = 'Insert into xiashu(`BOOKNAME`,`INDEX`,`XUHAO`,`ZJNAME`,`ZJTEXT`) values (\'%s\',%d ,%d ,\'%s\',\'%s\')' % (_BOOKNAME, _INDEX, _XUHAO, _ZJNAME, _ZJTEXT)
                self.db.worKon(_sql)
            except Exception as e:
                print("插入数据出错,错误原因%s" % e)
            return item
        self.file.close()

    # 批量替换字符
    def multiple_replace(self, text, adict):
        rx = re.compile('|'.join(map(re.escape, adict)))

        def one_xlat(match):
            return adict[match.group(0)]
        return rx.sub(one_xlat, text)


'''
import json
import codecs
class 预留(object):
    # 实现方式1
    def __init__(self):
        self.file = codecs.open('items.json', 'wb', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)

    # 实现方式2
    def process_item(self, item, spider):
        with open('items.json', 'a') as f:
            json.dump(dict(item), f, ensure_ascii=False)
            f.write(',\n')
        return item



from xjLib import mysql as mysql

class BqgPipeline(object):
    def __init__(self):
        self.db = mysql.MysqlHelp("default")
        # 使用execute方法执行SQL语句
        self.db.cur.execute("SELECT VERSION()")
        # 使用 fetchone() 方法获取一条数据库。
        print("数据库版本：", self.db.cur.fetchone())

    def process_item(self, item, spider):
        params = [item['书名'], item['序号'], item['章节名称'], item['章节正文']]
        try:
            self.db.cur.execute(
                'insert into xiashu(BOOKNAME, INDEX, ZJNAME, ZJTEXT)values (%s,%s,%s,%s)', params)
            self.conn.commit()
        except Exception as e:
            print("插入数据出错,错误原因%s" % e)
        return item
'''
