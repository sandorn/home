# ！/usr/bin/env python
# -*- coding:utf -8-*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@LastEditors: Even.Sand
@Date: 2019-05-08 19:18:48
@LastEditTime: 2019-05-10 15:38:21
'''

import requests
import time
from bs4 import BeautifulSoup


class downloader(object):

    def __init__(self):
        self.names = []  #存放关键字
        self.nums = 0  #设定页面数量
        self.text = {}  #链接名:网址

    def get_download_url(self, target):
        headers = {
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":
                "gzip, deflate, br",
            "Accept-Language":
                "zh-CN,zh;q=0.9",
            "Connection":
                "keep-alive",
            "Host":
                "www.baidu.com",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        while True:
            response = requests.get(url=target, headers=headers)
            if response.status_code == requests.codes.ok:
                break
            time.sleep(0.2)

        result = response.text
        #response.content.decode("utf-8")
        c_tools = BeautifulSoup(result, 'html5lib')
        #'html5lib','html.parser','lxml','html_parser')
        c_tools = c_tools.find_all(class_='c-tools')
        print('c_tools:', c_tools)
        for tr in c_tools:
            print(tr["data-tools"])

    def indict(self, name, text):
        '''
        @description:将获取到的章节内容保存到字典
        @param{name:章节名,text:章节内容}
        @return:None
        '''
        self.text[name] = text

    def writer(self):
        """
        函数说明:将爬取的文章内容写入文件
        Parameters:
            name - 章节名称(string)
            path - 当前路径下,小说保存名称(string)
            text - 章节内容(string)
        """
        with open(self.bookname + '.txt', 'a', encoding='utf-8') as f:
            for k, v in self.text.items():
                f.write(str(k) + '\n' + str(v) + '\n')


def fd():
    import win32ui
    _dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    _dlg.SetOFNInitialDir('c:/')  # 设置打开文件对话框中的初始显示目录
    _dlg.DoModal()
    filename = _dlg.GetPathName()  # 获取选择的文件名称
    return filename


def get_urls(pages):
    keys = []
    nums = []
    _file = fd()
    if not _file:
        return False

    with open(_file) as 文件:
        for row in 文件.readlines():
            row = row.strip()  #默认删除空白符
            keys.append(row)

    for page in range(0, pages, 10):  # 迭代 10 到 20 之间的数字
        nums.append(page)

    out_url = [
        "https://www.baidu.com/s?wd={}&pn={}".format(key, num)
        for key in keys
        for num in nums
    ]

    return out_url


if __name__ == "__main__":
    dl = downloader()
    #dl.get_download_url()
    urls = get_urls(30)
    print(urls)
    print(len(urls))
