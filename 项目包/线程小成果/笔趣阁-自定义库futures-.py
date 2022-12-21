# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
LastEditTime : 2022-12-21 14:23:05
FilePath     : /项目包/线程小成果/笔趣阁-自定义库futures-.py
Github       : https://github.com/sandorn/home
==============================================================
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2020-11-26 19:38:49
LastEditTime : 2022-12-09 15:10:53
FilePath     : /项目包/线程小成果/笔趣阁-自定义库futures-.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import os

from xt_Ahttp import ahttpGetAll
from xt_File import savefile
from xt_Ls_Bqg import get_biqugse_download_url, 结果处理
from xt_Requests import get
from xt_Thread import ProcessPool, ThreadPool


def multpool_ahttp_All(url):
    bookname, urls, _ = get_biqugse_download_url(url)
    resps = ahttpGetAll(urls)
    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'ahttp_All.txt', text_list, br='\n')


def multpool(urls):
    mypool = ProcessPool()
    mypool.add_map(multpool_ahttp_All, urls)
    mypool.wait_completed()


def thrtpool(url_list):
    mypool = ThreadPool()
    bookname, urls, _ = get_biqugse_download_url(url_list[0])
    urls = [[url] for url in urls]
    mypool.add_sub(get, urls)
    resps = mypool.wait_completed()

    text_list = 结果处理(resps)
    text_list.sort(key=lambda x: x[0])  # #排序
    files = os.path.basename(__file__).split(".")[0]
    savefile(files + '＆' + bookname + 'thrtpool.txt', text_list, br='\n')


if __name__ == '__main__':
    url = 'http://www.biqugse.com/96703/'
    # multpool_ahttp_All(url)

    urls = [
        'http://www.biqugse.com/96703/',
        'http://www.biqugse.com/96717/',
        # 'http://www.biqugse.com/2367/',
        # 'http://www.biqugse.com/2367/',
    ]
    multpool(urls)
    thrtpool(urls)
