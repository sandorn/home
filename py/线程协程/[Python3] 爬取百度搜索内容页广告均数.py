# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-20 18:17:54
@LastEditors: Even.Sand
@LastEditTime: 2019-05-20 18:19:16
'''
import requests
from bs4 import BeautifulSoup
from itertools import repeat

# 发送HTTP请求时的HEAD信息，用于伪装为浏览器
headersParameters = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

# 迭代取均值


def develop(line):
    count = 0
    for i in range(10):
        count = request(line, count)

    num = count / 10
    print("关键词:" + line + "\t总广告数:", count)
    data.write(line + "\t" + str(num) + "\n")

# 爬取整理


def request(key_word, count):
    httpRsp = requests.get("http://www.baidu.com/s?wd=" + key_word, headers=headersParameters)
    # httpResult = requests.get("https://www.zxxblog.cn", headers=headersParameters)
    # print(httpRsp.text)
    if httpRsp.status_code != 200:
        print("数据获取失败")
    else:
        soup = BeautifulSoup(httpRsp.text, "lxml")
        result = soup.find_all('span')
        # print(soup.prettify())
        for arr in result:
            if "广告" in arr:
                count = count + 1

        return count


# MAIN方法
if __name__ == "__main__":
    data = open('data.txt', 'w+', encoding='utf-8')
    file = open('D:/CODE/关键字检索/关键词 (015).txt', 'r', encoding='gbk')
    data.write("关键词\t广告均数\n")

    for line in file:
        line = line.strip('\n')
        develop(line)

    # END
    file.close()
    data.close()
'''
---------------------
作者：Takio_
来源：CSDN
原文：https://blog.csdn.net/qq_36791314/article/details/86724025
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
