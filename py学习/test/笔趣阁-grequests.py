# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Descripttion : None
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-08-14 10:54:00
FilePath     : /xjLib/test/笔趣阁-grequests.py
LastEditTime : 2020-08-14 12:59:23
Github       : https://github.com/sandorn/home
#==============================================================

grequests.map()参数说明：
def grequests.map(requests, stream=False, size=None, exception_handler=None, gtimeout=None)

参数	说明	备注
size	协程的并发度（相当于线程数）	当一个协程在IO等待时，会将CPU交给其他协程
exception_handler	异常处理函数	用于处理单个请求出现异常的函数
gtimeout	设置所有请求的超时时间
grequests的底层是request，所以它也支持回调函数：

作者：flashine
链接：https://www.jianshu.com/p/01dc9e8c21b6
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''

import grequests
import os

from xt_Ls_Bqg import get_download_url, arrangeContent
from xt_File import savefile
from xt_Time import fn_timer
from xt_Response import ReqResult

texts = []


@fn_timer
def main(url):
    bookname, urls = get_download_url(url)
    print(bookname)
    rets = grequests.map([grequests.get(_url) for _url in urls])
    for index in range(len(rets)):
        print(11111, rets[index])
        if rets[index] is None:
            continue
        response = ReqResult(rets[index], None, index).element
        _title = "".join(response.xpath('//h1/text()'))
        title = _title.strip('\r\n').replace(u'\u3000', u' ').replace(u'\xa0', u' ')
        _showtext = response.xpath('//*[@id="content"]/text()')
        content = arrangeContent(_showtext)
        texts.append([index, title, content])

    texts.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + '.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.biqukan.com/38_38836/'
    main(url)

    urls = [
        'https://www.biqukan.com/38_38836/',
        'https://www.biqukan.com/2_2760/',
        'https://www.biqukan.com/2_2714/',
        'https://www.biqukan.com/73_73450/',
        'https://www.biqukan.com/76_76015/',
        'https://www.biqukan.com/75_75766/',
        'https://www.biqukan.com/46_46394/',
        'https://www.biqukan.com/61_61396/',
    ]

    # '38_38836'    #@  147秒 丢失大量数据
