'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-03 23:26:06
@LastEditors: Even.Sand
@LastEditTime: 2020-03-09 16:52:53
'''
# ！/usr/bin/env python
# -*-coding:utf-8-*-

dbconf = {
    'TXbook': {
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'passwd': '123456',
        'db': 'biqukan',
        'charset': 'utf8mb4',
    },
    'TXbx': {
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'sandorn',
        'passwd': '123456',
        # 'password': '123456',
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
    'STXbx': {
        'host': 'cdb-lfp74hz4.bj.tencentcdb.com',
        'port': 10014,
        'user': 'root',
        'passwd': 'Sand2808',
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
    'db4': {
        'host': 'db4free.net',
        'port': 3306,
        'user': 'sandorn',
        'passwd': 'eeM3sh4KPkp4sJ8A',
        'db': 'baoxianjihuashu',
        'charset': 'utf8mb4',
    },
}

dbconf['master'] = dbconf['TXbx']

'''
阿里已经欠费
    'ali': {
        'host': 'rm-8vbdh9h80t8m9smmuqo.mysql.zhangbei.rds.aliyuncs.com',
        'port': 3306,
        'user': 'sandorn',
        'passwd': '123456',
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
    'aliSuper': {
        'host': 'rm-8vbdh9h80t8m9smmuqo.mysql.zhangbei.rds.aliyuncs.com',
        'port': 3306,
        'user': 'root',
        'passwd': 'Sand2808',
        'db': 'bxflb',
        'charset': 'utf8mb4',
    },
'''
