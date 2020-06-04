# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-04-02 12:27:12
#LastEditTime : 2020-04-29 11:23:56
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================

大幅度修改：
1.修改Session，保留cookies
2.修改post数据，将每页默认20项改为9999，不用循环获取；
3.找到公文分类标识  "typeId": "1"
4.get修改为允许跳转，直接获取网页信息
5.使用mysql存储下载进度，利用set去重
6.xpath().get获取属性字符串，json.loads为包含字典的list
7.pandas.read_sql参数为db.conn，而不是db
8.完善sqlHelper.has_tables,判断数据库是否包含某个表
9.数据库存储公告内容
'''
import json
import os
from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
from threading import Lock

import pandas
import requests

from xjLib.db.xt_mysql import engine
from xjLib.mystr import random_20char, toMysqlDateTime
from xjLib.req import sResponse

mutexA = Lock()


def login():
    Session = requests.session()
    Session.get('http://oa.jklife.com/')

    payload = {
        'login_username': 'liuxinjun',
        'login_password': 'sand2808',
    }
    response = Session.post(
        'http://oa.jklife.com/seeyon/main.do?method=login',
        data=payload,
        allow_redirects=True)
    if response.status_code == 200:
        return Session


def get_download_url(Session, stop=None):
    connect = engine('Jkdoc')
    db_set = set()
    if not connect.has_tables('jkdoc'):
        # #创建数据库,用于储存爬取到的数据
        creat_sql = '''
            CREATE TABLE `jkdoc` (
                `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
                `TITLE` varchar(255) COLLATE utf8mb4_bin NOT NULL,
                `URL` varchar(255) COLLATE utf8mb4_bin NOT NULL,
                `content` LONGTEXT COLLATE utf8mb4_bin,
                `update_TIME` datetime NOT NULL,
                PRIMARY KEY (`ID`)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
        '''
        connect.cur.execute(creat_sql)
        connect.conn.commit()

    def _run():
        payload = {
            "managerMethod": "findBulDatas",
            "method": "ajaxAction",
            "managerName": "bulDataManager",
            "rnd": random_20char(5),
            "arguments": json.dumps([{
                "pageSize": "9999",
                "pageNo": 1
            }])
        }
        # "typeId": "1" 区分类别，1为公告
        _response = Session.post(
            "http://oa.jklife.com/seeyon/ajax.do", data=payload)
        return _response

    # #利用set去重
    sql = "SELECT * FROM jkdoc;"  # 从MySQL里提数据
    pandasData = pandas.read_sql(sql, connect.conn)  # !connect.conn  读MySQL数据
    # #redis字典填充数据
    for _url in pandasData['URL']:
        db_set.add(_url)
    pandasData = None
    # print(2222, len(db_set))

    # #开始获取页面内容
    _urls = []
    _response = _run()
    _dic = _response.json()
    _itlist = _dic['list']  # 当前页面项目列表
    for item in _itlist:
        if item['id'] not in db_set:
            _urls.append([item['title'].strip(), item['id']])
            db_set.add(item['id'])

    return _urls, connect


def down_content(Session, connect, title, url):
    path = 'd:/2/' + title
    path = path.strip().rstrip("\\")
    # 判断路径是否存在{存在:True;不存在:False}
    if not os.path.exists(path):
        # 如果不存在则创建目录
        os.makedirs(path)

    url_head = 'http://oa.jklife.com/seeyon/bulData.do?method=bulView&bulId='

    _res = sResponse(Session.get(url_head + url))
    # 写html文件 # @二进制文件模式上加'b'
    with open(path + '/' + title + '.html', 'wb') as f:
        f.write(_res.content)

    # #写txt文件
    公告正文 = ''.join(
        _res.html.xpath('//div[@class="contentText"]//text()')).replace(
            'xa0', ' ').replace(' ', ' ').replace('%', '%%')
    with open(path + '/' + title + '.txt', 'w', encoding='utf-8') as f:
        f.write(title + '\n\n' + 公告正文)

    with mutexA:
        connect.insert(
            {
                'TITLE': title,
                'URL': url,
                'content': 公告正文,
                'update_TIME': toMysqlDateTime()
            }, 'jkdoc')

    # #下载附件
    _附件下载 = _res.html.xpath('//div[@id="attFileDomain"]')[0].get('attsdata')
    # !关键get字符串str
    if not _附件下载:
        return

    _url = 'http://oa.jklife.com/seeyon/fileDownload.do'
    for item in json.loads(_附件下载):  # 转dict
        formdata = {
            'method': 'download',
            'fileId': item['fileUrl'],
            'v': item['v'],
            'createDate': item['createdate'].split(' ')[0],
            'filename': item['filename'],
        }
        _res = Session.get(url=_url, params=formdata, allow_redirects=True)
        with open(path + '/' + item['filename'], 'wb') as f:
            f.write(_res.content)
    return


def main():
    Session = login()
    urls, connect = get_download_url(Session, None)
    print(f'需要下载的公文数量为：{len(urls)}')
    # 创建多进程队列
    pool = Pool(25)
    _ = [
        pool.submit(down_content, Session, connect, item[0], item[1])
        for item in urls
    ]
    pool.shutdown(wait=True)


if __name__ == '__main__':
    # from xjLib.log import log
    # mylog = log()
    # print = mylog.print
    main()
