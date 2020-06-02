# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-23 11:50:11
@LastEditors: Even.Sand
@LastEditTime: 2020-03-23 13:12:05

实现_ init_ 方法, 负责初始化,包含如下字段:
ip: 代理的IP地址
port:代理IP的端口号
protocol: 代理IP支持的协议类型,http是0, https是1, https和http都支持是2
nick_ type: 代理IP的匿名程度,高匿:0,匿名: 1,透明:2
speed:代理IP的响应速度，单位s
area:代理IP所在地区
score:代理IP的评分，用于衡量代理的可用性;默认分值可以通过配置文件进行配置.在进行代理可用性检查的时候，每遇到一次请求失败就减1份,减到0的时候从池中删除.如果检查代理可用,就恢复默认分值
disable_domains:不可用域名列表,有些代理IP在某些域名下不可用，但是在其他域名下可用在配置文件:
settings.py中定义MAX_ _SCORE = 50,表示代理IP的默认最高分数提供_ _str__方法， 返回数据字符串
https://www.cnblogs.com/kongbursi-2292702937/p/12173647.html
'''

from settings import MAX_SCORE
# 从settings模块中导入MAX_SCORE变量，这个变量的意思就是给每一个IP一个分数（分数高代表这个IP可用性强，初始化为MAX_SCORE）


class Proxy(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_ip=[]):
        self.ip = ip  # 代理ip
        self.port = port  # 代理ip端口
        self.protocol = protocol  # 代表代理ip的协议类型
        self.nick_type = nick_type  # 匿名程度
        self.speed = speed  # 代理ip速度
        self.area = area  # 代理ip地址
        self.score = score  # ip分数
        self.disable_ip = disable_ip

    def __str__(self):
        return str(self.__dict__)  # __dict__ : 类的属性（包含一个字典，由类的数据属性组成）
