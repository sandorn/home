# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-14 18:02:15
@LastEditors: Even.Sand
@LastEditTime: 2020-04-14 18:02:19


定义规则 urls:url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
'''
import os
from fake_useragent import UserAgent
'''
ip，端口，
类型(0高匿名，1透明)，
protocol(0 http,1 https),
country(国家),area(省市),
updatetime(更新时间)
 speed(连接速度)
'''

parserList = [{
    'urls': [
        'http://www.66ip.cn/%s.html' % n
        for n in ['index'] + list(range(2, 12))
    ],
    'type': 'xpath',
    'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': './td[4]',
        'protocol': ''
    }
}, {
    'urls': [
        'http://www.66ip.cn/areaindex_%s/%s.html' % (m, n)
        for m in range(1, 35)
        for n in range(1, 10)
    ],
    'type': 'xpath',
    'pattern': ".//*[@id='footer']/div/table/tr[position()>1]",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': './td[4]',
        'protocol': ''
    }
}, {
    'urls': ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218'],
    'type': 'xpath',
    'pattern': ".//table[@class='sortable']/tbody/tr",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': '',
        'protocol': ''
    }
}, {
    'urls': ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)],
    'type': 'xpath',
    'pattern': ".//table[@class='list']/tr",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': '',
        'protocol': ''
    }
}, {
    'urls': [
        'https://proxy-list.org/english/index.php?p=%s' % n
        for n in range(1, 10)
    ],
    'type': 'module',
    'moduleName': 'proxy_listPraser',
    'pattern': r'Proxy\(.+\)',
    'position': {
        'ip': 0,
        'port': -1,
        'type': -1,
        'protocol': 2
    }
}, {
    'urls': [
        'http://incloak.com/proxy-list/%s#list' % n
        for n in ([''] + ['?start=%s' % (64 * m) for m in range(1, 10)])
    ],
    'type': 'xpath',
    'pattern': ".//table[@class='proxy__t']/tbody/tr",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': '',
        'protocol': ''
    }
}, {
    'urls': [
        'http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 11)
    ],
    'type': 'xpath',
    'pattern': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': './td[3]',
        'protocol': './td[4]'
    }
}, {
    'urls': [
        'http://www.kuaidaili.com/free/%s/%s/' % (m, n)
        for m in ['inha', 'intr', 'outha', 'outtr']
        for n in range(1, 11)
    ],
    'type': 'xpath',
    'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': './td[3]',
        'protocol': './td[4]'
    }
}, {
    'urls': [
        'http://www.cz88.net/proxy/%s' % m
        for m in ['index.shtml'] + ['http_%s.shtml' % n for n in range(2, 11)]
    ],
    'type': 'xpath',
    'pattern': ".//*[@id='boxright']/div/ul/li[position()>1]",
    'position': {
        'ip': './div[1]',
        'port': './div[2]',
        'type': './div[3]',
        'protocol': ''
    }
}, {
    'urls': ['http://www.ip181.com/daili/%s.html' % n for n in range(1, 11)],
    'type': 'xpath',
    'pattern': ".//div[@class='row']/div[3]/table/tbody/tr[position()>1]",
    'position': {
        'ip': './td[1]',
        'port': './td[2]',
        'type': './td[3]',
        'protocol': './td[4]'
    }
}, {
    'urls': [
        'http://www.xicidaili.com/%s/%s' % (m, n)
        for m in ['nn', 'nt', 'wn', 'wt']
        for n in range(1, 8)
    ],
    'type': 'xpath',
    'pattern': ".//*[@id='ip_list']/tr[position()>1]",
    'position': {
        'ip': './td[2]',
        'port': './td[3]',
        'type': './td[5]',
        'protocol': './td[6]'
    }
}, {
    'urls': ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 11)],
    'type':
        'module',
    'moduleName':
        'CnproxyPraser',
    'pattern':
        r'<tr><td>(\d+\.\d+\.\d+\.\d+)<SCRIPT type=text/javascript>document.write\(\"\:\"(.+)\)</SCRIPT></td><td>(HTTP|SOCKS4)\s*',
    'position': {
        'ip': 0,
        'port': 1,
        'type': -1,
        'protocol': 2
    }
}]
'''
数据库的配置
'''
DB_CONFIG = {
    'DB_CONNECT_TYPE':
        'sqlalchemy',
    'DB_CONNECT_STRING':
        'mysql+mysqldb://sandorn:123456@cdb-lfp74hz4.bj.tencentcdb.com:10014/proxy?charset=utf8'
}
CHINA_AREA = [
    '河北', '山东', '辽宁', '黑龙江', '吉林', '甘肃', '青海', '河南', '江苏', '湖北', '湖南', '江西',
    '浙江', '广东', '云南', '福建', '台湾', '海南', '山西', '四川', '陕西', '贵州', '安徽', '重庆',
    '北京', '上海', '天津', '广西', '内蒙', '西藏', '新疆', '宁夏', '香港', '澳门'
]
QQWRY_PATH = os.path.dirname(__file__) + "/data/qqwry.dat"
THREADNUM = 5
API_PORT = 8000
'''
爬虫爬取和检测ip的设置条件
不需要检测ip是否已经存在，因为会定时清理
'''
UPDATE_TIME = 30 * 60  # 每半个小时检测一次是否有代理ip失效
MINNUM = 50  # 当有效的ip值小于一个时 需要启动爬虫进行爬取

TIMEOUT = 5  # socket延时
'''
反爬虫的设置
'''
'''
重试次数
'''
RETRY_TIME = 3
'''
USER_AGENTS 随机头信息
'''


def get_header():
    return {
        'User-Agent':
            UserAgent().random,
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':
            'en-US,en;q=0.5',
        'Connection':
            'keep-alive',
        'Accept-Encoding':
            'gzip, deflate',
    }


# 默认给抓取的ip分配20分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
DEFAULT_SCORE = 20

TEST_URL = 'http://ip.chinaz.com/getip.aspx'
TEST_IP = 'http://httpbin.org/ip'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
TEST_HTTPS_HEADER = 'https://httpbin.org/get'

# http://icanhazip.com
# CHECK_PROXY变量是为了用户自定义检测代理的函数
# 现在使用检测的网址是httpbin.org,但是即使ip通过了验证和检测
# 也只能说明通过此代理ip可以到达httpbin.org,但是不一定能到达用户爬取的网址
# 因此在这个地方用户可以自己添加检测函数,我以百度为访问网址尝试一下
# 大家可以看一下Validator.py文件中的baidu_check函数和detect_proxy函数就会明白

CHECK_PROXY = {'function': 'checkProxy'}  # {'function':'baidu_check'}

# 下面配置squid,现在还没实现
# SQUID={'path':None,'confpath':'C:/squid/etc/squid.conf'}

MAX_CHECK_PROCESS = 2  # CHECK_PROXY最大进程数
MAX_CHECK_CONCURRENT_PER_PROCESS = 30  # CHECK_PROXY时每个进程的最大并发
TASK_QUEUE_SIZE = 50  # 任务队列SIZE
MAX_DOWNLOAD_CONCURRENT = 3  # 从免费代理网站下载时的最大并发
CHECK_WATI_TIME = 1  # 进程数达到上限时的等待时间
