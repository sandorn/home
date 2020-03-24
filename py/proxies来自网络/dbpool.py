# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 12:04:45
@LastEditors: Even.Sand
@LastEditTime: 2020-03-23 20:19:30
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 12:04:45
@LastEditors: Even.Sand
@LastEditTime: 2020-03-23 16:42:07

实现代理池的数据库模块
●作用:用于对proxies 集合进行数据库的相关操作
目标:实现对数据库增删改查相关操作步骤:
1.在init 中，建立数据连接,获取要操作的集合，在del方法中关闭数据库连接
2.提供基础的增删改查功能
    i.实现插入功能;
    ii.实现修改该功能
    iii.实现删除代理:根据代理的IP删除代理
    iv.查询所有代理IP的功能
3.提供代理API模块使用的功能
    i.实现查询功能:根据条件进行查询，可以指定查询数量,先分数降序,速度升序排,保证优质的代理IP在上面.
    ii.实现根据协议类型和要访问网站的域名，获取代理IP列表
    iii.实现根据协议类型和要访问网站的域名，随机获取一个代理IP
    iv.实现把指定域名添加到指定IP的isable_plomain列表中.
'''
from domain import Proxy
from log import logger
import MySQLdb
from xjLib.mssql import MySQLConnection as mysql
import pymongo
import pandas
import numpy
import sys
from xjLib.dBrouter import dbconf
sys.path.append("..")
sys.path.append("../..")

'''
CREATE TABLE `proxy` (
`ip` VARCHAR ( 19 ) COLLATE utf8mb4_bin NOT NULL,
`port` VARCHAR ( 8 ) COLLATE utf8mb4_bin DEFAULT NULL,
`protocol` SMALLINT ( 2 ) DEFAULT NULL,
`nick_type` SMALLINT ( 2 ) DEFAULT NULL,
`speed` DOUBLE DEFAULT NULL,
`area` VARCHAR ( 255 ) COLLATE utf8mb4_bin DEFAULT NULL,
`score` SMALLINT ( 4 ) DEFAULT NULL,
`disable_ip` VARCHAR ( 255 ) COLLATE utf8mb4_bin DEFAULT NULL,
PRIMARY KEY ( `ip` )
) ENGINE = INNODB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_bin;


SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
-- ----------------------------
-- Table structure for proxy
-- ----------------------------
DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy`  (
  `ip` varchar(19) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `port` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `protocol` smallint(2) NULL DEFAULT NULL,
  `nick_type` smallint(2) NULL DEFAULT NULL,
  `speed` double NULL DEFAULT NULL,
  `area` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `score` smallint(4) NULL DEFAULT NULL,
  `disable_ip` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`ip`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
'''


class mysqlPool(object):
    def __init__(self):
        self.connect = MySQLdb.connect(**dbconf['proxy'])
        self.cur = self.connect.cursor()

    def __del__(self):
        self.connect.close()

    def insert(self, proxy):
        # _sql = """
        # Insert into `proxy` (`ip`,`port`,`protocol`,`nick_type`,`speed`,`area`,#`score`,`disable_ip`) values ('%s',%d ,'%s','%s')
        # """ % (proxy.__dict__)
        _sql = "Insert into `proxy` %s" % (proxy.__dict__)
        self.cur.execute(_sql)
        logger.exception("Insert into `proxy' %s" % (proxy.__dict__))

    def update(self, proxy):
        _sql = f"""
        UPDATE `proxy` SET %s WHERE `ip`='{proxy.ip}'
        """ % (proxy.__dict__)
        self.connect.execute(_sql)
        self.connect.commit()

    def delete(self, proxy):
        _sql = f"""
        DELETE  FROM `proxy` WHERE `ip`='{proxy.ip}'
        """
        self.connect.execute(_sql)
        self.connect.commit()

    def find_all(self):
        sql = "SELECT * FROM proxy;"  # 从MySQL里提数据
        pandasData = pandas.read_sql(sql, self.connect)  # 读MySQL数据
        logger.exception('pandasData:', pandasData)
        _data = numpy.array(pandasData)  # np.ndarray()
        return _data.tolist()

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
    mongo = mysqlPool()
    '''
    proxy = Proxy('117.95.55.40', port='9999')

    mongo.insert_one(proxy)
    '''

    '''
    for proxy in mongo.find_all():
        print(proxy)
    '''

    mongo.add_disable_domain('117.95.55.40', 'jd.com')
