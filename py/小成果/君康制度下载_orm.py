# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-28 19:10:26
#LastEditTime : 2020-05-11 15:21:13
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================

大幅度修改：
1.修改Session，保留cookies
2.修改post数据，将每页默认20项改为9999，不用循环获取；
3.找到公文分类标识  "typeId": "1"
4.get修改为允许跳转，直接获取网页信息
5.使用mysql存储下载进度，利用set去重;又改为list判断
6.xpath().get获取属性字符串，json.loads为包含字典的list
7.pandas.read_sql参数为db.conn，而不是db
8.完善sqlHelper.has_tables,判断数据库是否包含某个表
9.数据库存储公告内容
10.使用sqlalchemyorm方式
11.使用vthread.pool方式
'''
import json
import os

from xjLib.req import RequestsSession

import xjLib.db.xt_sqlalchemy
from xjLib.CustomThread import my_pool
from xjLib.mystr import random_20char

pool = my_pool(200)
Session = RequestsSession()


def get_download_url(connect, stop=None):
    # #登录，并保存cookies
    _ = Session.post(
        'http://oa.jklife.com/seeyon/main.do?method=login',
        data={
            'login_username': 'liuxinjun',
            'login_password': 'sand2808',
        })

    # #获取公文列表
    getlistdata = {
        "managerMethod": "findBulDatas",
        "method": "ajaxAction",
        "managerName": "bulDataManager",
        "rnd": random_20char(5),
        "arguments": json.dumps([{
            "pageSize": "9999",
            "pageNo": 1
        }])
    }
    # #"typeId": 区分类别，1为公告

    _itlist = Session.post(
        "http://oa.jklife.com/seeyon/ajax.do", data=getlistdata).json['list']

    # #利用set去重,填充数据库已有公文
    db_urls_list = [item[0] for item in connect.select(Columns=['URL'])]

    # #将未下载公文的编号进行保存
    _urls = []
    for item in _itlist:
        if item['id'] not in db_urls_list:
            _urls.append([item['title'].strip(), item['id']])
            db_urls_list.append(item['id'])

    return _urls


@pool
def down_content(connect, title, url):
    path = f'd:/1/{title}'.strip().rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)

    _res = Session.get(
        f'http://oa.jklife.com/seeyon/bulData.do?method=bulView&bulId={url}')

    print(_res.json)

    公告正文 = ''.join(
        _res.html.xpath('//div[@class="contentText"]//text()')).replace(
            'xa0', ' ').replace(' ', ' ').replace('%', '%%')

    # #写数据库
    connect.insert({
        'TITLE': title,
        'URL': url,
        'content': 公告正文,
    })

    # # 写html文件,二进制文件模式加b
    open(path + '/' + title + '.html', 'wb').write(_res.content)
    # #写txt文件
    open(
        path + '/' + title + '.txt', 'w',
        encoding='utf-8').write(title + '\n\n' + 公告正文)

    # #下载附件
    _附件下载 = _res.html.xpath('//div[@id="attFileDomain"]')[0].get('attsdata')
    # !关键get字符串str
    if _附件下载:
        for item in json.loads(_附件下载):  # 转dict
            formdata = {
                'method': 'download',
                'fileId': item['fileUrl'],
                'v': item['v'],
                'createDate': item['createdate'].split(' ')[0],
                'filename': item['filename'],
            }

            _res = Session.get(
                'http://oa.jklife.com/seeyon/fileDownload.do', params=formdata)

            open(path + '/' + item['filename'], 'wb').write(_res.content)

    print(f'《{title}》\t下载完成')
    return


def main():
    from sqlalchemy import Column, DateTime, String
    from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.sql import text
    Base = declarative_base()

    class Jkdoc(Base, xjLib.db.xt_sqlalchemy.model):
        __tablename__ = 'jkdoc'

        ID = Column(INTEGER(6), primary_key=True)
        TITLE = Column(String(255, 'utf8mb4_bin'), nullable=False)
        URL = Column(String(64, 'utf8mb4_bin'), nullable=False)
        content = Column(LONGTEXT)
        update_TIME = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    connect = xjLib.db.xt_sqlalchemy.SqlConnection(Jkdoc, 'Jkdoc')

    urls = get_download_url(connect)
    print(f'需要下载的公文数量为：{len(urls)}')
    _ = [down_content(connect, item[0], item[1]) for item in urls]
    pool.wait_completed()


if __name__ == '__main__':
    from xjLib.log import MyLog
    mylog = MyLog()
    print = mylog.print

    main()
