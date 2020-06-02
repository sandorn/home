# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 16:31:38
@LastEditors: Even.Sand
@LastEditTime: 2020-03-23 16:33:16

实现代理池的数据库模块

      ●作用:用于对proxies 集合进行数据库的相关操作

      目标:实现对数据库增删改查相关操作步骤:

1.在init 中，建立数据连接,获取要操作的集合，在del方法中关闭数据库连接
2.提供基础的增删改查功能
      i.实现插入功能
      ii.实现修改该功能
      ili.实现删除代理:根据代理的IP删除代理
      iv.查询所有代理IP的功能
3.提供代理API模块使用的功能
      i.实现查询功能:根据条件进行查询，可以指定查询数量,先分数降序,速度升序排,保证优质的代理IP在上面.
      ii.实现根据协议类型和要访问网站的域名，获取代理IP列表
      ili.实现根据协议类型和要访问网站的域名，随机获取一个代理IP
      iv.实现把指定域名添加到指定IP的disable_plomain列表中.

'''
from domain import Proxy
from log import logger
from settings import MONGO_URL
import sys
import pymongo
from pymongo import MongoClient
sys.path.append("..")
sys.path.append("../..")


class MongoPool(object):
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        # 分别对应库和集合
        self.proxies = self.client['Proxies_pool']['proxies']

    def __del__(self):
        self.client.close()

    # mongdb中"_id"为主键
    def insert_one(self, proxy):
        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info("insert Success:{}".format(proxy))
        else:
            logger.warning("insert Default:{}".format(proxy))

    def update_proxy(self, proxy):
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info("delete ip: {}".format(proxy.ip))

    def find_all(self):
        all = self.proxies.find()
        for item in all:
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, condition={}, count=10):
        all = self.proxies.find(condition, limit=count).sort(
            [('socre', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)]
        )

        proxy_list = []
        for item in all:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=8, nick_type=0):
        condition = {'nick_type': nick_type}
        if protocol is None:
            condition['protocol'] = 2
        elif protocol.lower() == 'http':
            condition['protocol'] = {'$in': [0, 2]}
        else:
            condition['protocol'] = {'$in': [1, 2]}

        if domain:
            condition['disable_domains'] = {'$nin': [domain]}

        return self.find(condition, count=count)

    def add_disable_domain(self, ip, domain):
        if self.proxies.count_documents({'_id': ip, 'disable_domain': domain}) == 0:
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    '''
    proxy = Proxy('117.95.55.40', port='9999')

    mongo.insert_one(proxy)
    '''

    '''
    for proxy in mongo.find_all():
        print(proxy)
    '''

    mongo.add_disable_domain('117.95.55.40', 'jd.com')
