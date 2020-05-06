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
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-05-06 10:44:09

定义规则 urls:url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
'''

from fake_useragent import UserAgent

parserList = [{
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
        for m in ['inha', 'intr']
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
}]

UPDATE_TIME = 30 * 60  # 每半个小时检测一次是否有代理ip失效

TIMEOUT = 5  # socket延时


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

MAX_CHECK_PROCESS = 2  # CHECK_PROXY最大进程数
MAX_CHECK_CONCURRENT_PER_PROCESS = 30  # CHECK_PROXY时每个进程的最大并发
TASK_QUEUE_SIZE = 50  # 任务队列SIZE
MAX_DOWNLOAD_CONCURRENT = 3  # 从免费代理网站下载时的最大并发
CHECK_WATI_TIME = 1  # 进程数达到上限时的等待时间
'''
{
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
    },
    {
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
    },
    {
        # #免费HTTP代理提取
        'urls': 'http://www.66ip.cn/mo.php?&tqsl=%s' % 20,
        'type': 'module',
        'moduleName': 'ipcn66_praser',
        'pattern': "//body/*/text()",  #!难度*
        'position': {'ip': 0, 'port': 1, 'type': -1, 'protocol': 2}
    },

    def ipcn66_praser(response, parser):
    proxylist = []

    temp_list = [
        item.strip()
        for item in response.xpath(parser['pattern'])
        if item.strip() != ''
    ]
    print(temp_list)
    for item in temp_list:
        ip = item.split(':')[0]
        port = item.split(':')[1]
        type = 0
        protocol = 0
        proxy = {
            'ip': ip,
            'port': int(port),
            'types': type,
            'protocol': protocol,
            'speed': 100
        }
        proxylist.append(proxy)
    return proxylist

'''
