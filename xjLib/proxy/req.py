# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-05-06 11:04:01
#LastEditTime : 2020-05-06 12:39:28
#Github       : https://github.com/sandorn/home
#License      : (C)Copyright 2009-2020, NewSea
#==============================================================
'''

import random
import config
from db import sqlhelper

import requests
import chardet
from retrying import retry

from xjLib.head import myhead
from xjLib.Response import sResponse


class Html_Downloader(object):

    @staticmethod
    def download(url):
        try:
            r = requests.get(
                url=url, headers=config.get_header(), timeout=config.TIMEOUT)
            r.encoding = chardet.detect(r.content)['encoding']
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text

        except Exception:
            count = 0  # 重试次数
            proxylist = sqlhelper.select(10)
            if not proxylist:
                return None

            while count < config.RETRY_TIME:
                try:
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {
                        "http": "http://%s:%s" % (ip, port),
                        "https": "http://%s:%s" % (ip, port)
                    }

                    r = requests.get(
                        url=url,
                        headers=config.get_header(),
                        timeout=config.TIMEOUT,
                        proxies=proxies)
                    r.encoding = chardet.detect(r.content)['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None
