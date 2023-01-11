# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2023-01-10 17:07:19
LastEditTime : 2023-01-10 17:07:20
FilePath     : /项目包/君康制度下载/君康制度下载_orm_改版.py
Github       : https://github.com/sandorn/home
==============================================================
未完成登录
'''
import json
import os

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT
from sqlalchemy.sql import text
from xt_DAO.xt_chemyMeta import Base_Model
from xt_DAO.xt_sqlalchemy import SqlConnection
from xt_Requests import SessionClient
from xt_String import random_char
from xt_Thread import WorkManager


class Jkdoc(Base_Model):
    __tablename__ = 'jkdoc'

    ID = Column(INTEGER(6), primary_key=True)
    TITLE = Column(String(255, 'utf8mb4_bin'), nullable=False)
    URL = Column(String(64, 'utf8mb4_bin'), nullable=False)
    content = Column(LONGTEXT)
    update_TIME = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


Session = SessionClient()


def get_download_url(connect, stop=None):
    # #登录,并保存cookies
    res = Session['post'](
        'http://oa.jklife.com/seeyon/main.do?method=login',
        data={
            'login_username': 'liuxinjun',
            'login_password': 'U2FsdGVkX1+FSC7gcXU2/WpBDDXBWtbz5xfyK3PmX1w=',
        },
    )
    print(res, "||||||||||||||||||", Session.sson.cookies)
    Session.get('https://oa.jklife.com/seeyon/main.do?method=main')
    print(res, "||||||||||||||||||", Session.sson.cookies)
    # Session.update_headers({'CSRFTOKEN': 'RBOJ-GFZV-HT0M-PHSV-RFSB-950L-SSED-W3L6'})
    data = {
        "method": "bulIndex",
        'typeId': 1,
        "CSRFTOKEN": 'RBOJ-GFZV-HT0M-PHSV-RFSB-950L-SSED-W3L6',
    }
    res = Session.post("https://oa.jklife.com/seeyon/bulData.do", data=data)
    print(res, res.text, "||||||||||||||||||", Session.sson.cookies)
    return
    ## 'CSRFTOKEN: RBOJ-GFZV-HT0M-PHSV-RFSB-950L-SSED-W3L6'
    ## 'https://oa.jklife.com/seeyon/bulData.do?method=bulIndex&CSRFTOKEN=RBOJ-GFZV-HT0M-PHSV-RFSB-950L-SSED-W3L6'
    ## 'https://oa.jklife.com/seeyon/bulData.do?method=bulIndex&typeId=1&spaceType=&spaceId=&CSRFTOKEN=RBOJ-GFZV-HT0M-PHSV-RFSB-950L-SSED-W3L6'
    ## 'https://oa.jklife.com/seeyon/ajax.do?method=ajaxAction&managerName=bulDataManager&rnd=87434'
    ## managerMethod: findBulDatas
    ## arguments: [{"pageSize":"20","pageNo":2,"spaceType":"","spaceId":"","typeId":"1","search":"null","textfield2":"","myBul":""}]
    # #获取公文列表
    getlistdata = {
        'managerMethod': 'findBulDatas',
        "method": "ajaxAction",
        'managerName': 'bulDataManager',
        'rnd': 87434,
        'typeId': 1,
        "CSRFTOKEN": 'RBOJ-GFZV-HT0M-PHSV-RFSB-950L-SSED-W3L6',
        "arguments": json.dumps([{
            "pageSize": "9999",
            "pageNo": 1
        }]),
    }
    # #"typeId": 区分类别,1为公告

    _itlist = Session.post("https://oa.jklife.com/seeyon/ajax.do", data=getlistdata).json['list']

    # #利用set去重,填充数据库已有公文
    db_urls_list = [item[0] for item in connect.select(Columns=['URL'])]

    # #将未下载公文的编号进行保存
    _urls = []
    for item in _itlist:
        if item['id'] not in db_urls_list:
            _urls.append([item['title'].strip(), item['id']])
            db_urls_list.append(item['id'])

    return _urls


def down_content(connect, title, url):
    path = f'd:/1/{title}'.strip().rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path)

    _res = Session.get(f'http://oa.jklife.com/seeyon/bulData.do?method=bulView&bulId={url}')

    公告正文 = ''.join(_res.html.xpath('//div[@class="contentText"]//text()')).replace('xa0', ' ').replace(' ', ' ').replace('%', '%%')

    # #写数据库
    connect.insert({'TITLE': title, 'URL': url, 'content': 公告正文})

    # # 写html文件,二进制文件模式加b
    open(path + '/' + title + '.html', 'wb').write(_res.content)
    # #写txt文件
    open(path + '/' + title + '.txt', 'w', encoding='utf-8').write(title + '\n\n' + 公告正文)

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

            _res = Session.get('http://oa.jklife.com/seeyon/fileDownload.do', params=formdata)

            open(path + '/' + item['filename'], 'wb').write(_res.raw.content)

    print(f'《{title}》\t下载完成')
    return


def main():
    mywork = WorkManager()
    connect = SqlConnection(Jkdoc, 'Jkdoc')
    urls = get_download_url(connect)
    print(f'需要下载的公文数量为：{len(urls)}')
    mywork.add_work_queue([down_content, connect, item[0], item[1]] for item in urls)
    mywork.getAllResult()


if __name__ == '__main__':
    main()
