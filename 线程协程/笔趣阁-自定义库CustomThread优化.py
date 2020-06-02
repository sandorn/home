# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-31 12:12:40
#LastEditors  : Please set LastEditors
#LastEditTime : 2020-06-02 18:15:02
'''

import os

from xjLib.mystr import savefile
from xjLib.Thread import CustomThread
from xjLib.ls import get_download_url, get_contents


def main(bookname, args):
    _ = [CustomThread(get_contents, index, url) for index, url in enumerate(urls)]
    texts = CustomThread.wait_completed()
    texts.sort(key=lambda x: x[0])
    texts = [[row[i] for i in range(1, 3)] for row in texts]
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'CustomThread.txt', texts, br='\n')


if __name__ == "__main__":
    bookname, urls = get_download_url('http://www.biqukan.com/2_2760/')
    # # 38_38836  #2_2714  2_2760

    main(bookname, urls)
