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
@LastEditTime: 2019-05-20 20:53:59
'''

import time
from xjLib import threadPool
from retrying import retry
import requests
from pyquery import PyQuery as pq

myhead = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    # 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch, br',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    'Proxy-Connection': 'no-cache'
    # 'Host': 'www.baidu.com'
}


def parse_url(url, params=None, headers=myhead, proxies=None, timeout=6, ecode='utf-8',
              wait_random_min=200, wait_random_max=3000, stop_max_attempt_number=100):

    @retry(wait_random_min=wait_random_min, wait_random_max=wait_random_max, stop_max_attempt_number=stop_max_attempt_number)
    def _parse_url(url):
        response = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=timeout)
        assert response.status_code == 200
        # return response.text
        return response.content.decode(ecode)

    try:
        # 以下except捕获当requests请求异常
        response = _parse_url(url)
    except requests.exceptions.ConnectionError as e:
        print('ConnectionError:', e, url, flush=True)
        response = None
    except requests.exceptions.ChunkedEncodingError as e:
        print('ChunkedEncodingError:', e, url, flush=True)
        response = None
    except Exception as e:
        print('Unfortunitely Unknow Error:', e, url, flush=True)
        response = None
    return response


def fd():
    import win32ui
    _dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
    _dlg.SetOFNInitialDir('c:/')  # 设置打开文件对话框中的初始显示目录
    _dlg.DoModal()
    filename = _dlg.GetPathName()  # 获取选择的文件名称
    return filename


def make_urls(pages):
    _k = []
    _file = fd()  # 'D:/CODE/关键字检索/关键词 (200).txt'  #
    if not _file:
        return False
    res = _file.split('.')[0:-1]  # 文件名，含完整路径，去掉后缀

    with open(_file) as f:
        for row in f.readlines():
            row = row.strip()  # 默认删除空白符  '#^\s*$'
            if len(row) == 0:
                break  # 去除行len为0的行
            _k.append(row)
    keys = sorted(set(_k), key=_k.index)

    out_url = [(key, page, "http://www.baidu.com/s?wd={}&pn={}".format(key, page * 10),) for key in keys for page in range(pages)]

    return res[0], out_url


def getkeys(key, page, url):
    '''
    @description:
    @return:
    15*10=7.8829169273376465//13
    200*10=110.2550950050354
    '''
    _texts = []
    response = parse_url(url=url)
    result = pq(response)
    index = 0
    for each in result("h3 a").items():
        href = each.attr('href')
        title = each.text()
        if '百度' in title:
            break
        if not href.startswith('http'):
            break
        baidu_url = requests.get(url=href, headers=myhead, allow_redirects=False)
        real_url = baidu_url.headers['Location']  # 得到网页原始地址
        if real_url.startswith('http'):
            index += 1
            _texts.append([key, page, index, title, real_url])

    return _texts


def savefile(_filename, lists):
    # 函数说明:将爬取的文章lists写入文件
    print('[' + _filename + ']开始保存......', end='', flush=True)
    lists.sort()

    with open(_filename, 'a', encoding='utf-8') as f:
        for lists_line in lists:
            for index, item in enumerate(lists_line):
                f.write('key:' + item[0] + '\tpage:' + str(item[1]) + '\tindex:' + str(item[2]) + '\ttitle:' + item[3] + '\turl:' + item[4] + '\n')

    print('[' + _filename + ']保存完成。', flush=True)


def main():
    start = time.time()
    try:
        _name, urls = make_urls(10)
    except Exception as e:
        print(e)
        return False

    work_manager = threadPool.WorkManager(getkeys, urls)  # 调用函数,参数:list内tupe,线程数量
    texts = work_manager.wait_allcomplete()
    savefile(_name + '_百度词频.txt', texts)
    print("threadPool cost all time: %s" % (time.time() - start), flush=True)


if __name__ == "__main__":
    main()
