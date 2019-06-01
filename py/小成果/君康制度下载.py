# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-16 00:20:05
@LastEditors: Even.Sand
@LastEditTime: 2019-06-01 17:02:35

使用beautifulsoup和pyquery爬小说 - 坚强的小蚂蚁 - 博客园
https://www.cnblogs.com/regit/p/8529222.html
'''

from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
from pyquery import PyQuery
from xjLib.req import parse_get
from xjLib.req import parse_post
import json

head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'oa.jklife.com',
    'Origin': 'http://oa.jklife.com',
    'RequestType': 'AJAX',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie': 'JSESSIONID=C5D8EF3FD6E8903D068D37D9B5F0D80D; avatarImageUrl=7597432631771349600; loginPageURL=; login_locale=zh_CN',
    'Referer': 'http://oa.jklife.com/seeyon/bulData.do?method=bulIndex&typeId=&boardId=&_isModalDialog=true&openFrom=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}


def get_download_url():
    _urls = []
    payload = {"managerMethod": "findBulDatas",
               "arguments": json.dumps([{"pageSize": "20", "pageNo": 1, "spaceType": "", "spaceId": "", "typeId": "", "condition": "", "textfield1": "", "textfield2": "", "myBul": ""}])}

    _response = parse_post("http://oa.jklife.com/seeyon/ajax.do?method=ajaxAction&managerName=bulDataManager&rnd=97013",
                           headers=head, data=payload)
    # log.p(_response.text)
    _dic = _response.json()
    pages = int(_dic['pages'])  # 总页数
    size = _dic['size']  # 总项目数量
    log.p('总页数：' + str(pages) + '\t总size数：' + str(size))

    # @上一次下载到的文件位置，停止标志
    stop = '君保发〔2019〕106号关于2019年端午节放假的通知'

    for i in range(pages):
        pageNo = i + 1
        payload = {"managerMethod": "findBulDatas",
                   "arguments": json.dumps([{"pageSize": "20", "pageNo": pageNo, "spaceType": "", "spaceId": "", "typeId": "", "condition": "", "textfield1": "", "textfield2": "", "myBul": ""}])}
        _response = parse_post("http://oa.jklife.com/seeyon/ajax.do?method=ajaxAction&managerName=bulDataManager&rnd=40592",
                               headers=head, data=payload)

        _dic = _response.json()
        _itlist = _dic['list']  # 当前页面项目列表
        for item in _itlist:
            if item['title'].strip() == stop:
                return _urls  # !匹配到停止标志，break
            _urls.append((item['title'].strip(), item['id']))

    return _urls


def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在{存在:True;不存在:False}
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        log.p(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        log.p(path + ' 目录已存在')
        return False


def getdown(title, url):
    path = 'd:/1/' + title
    if not mkdir(path):
        return

    _res = parse_get(url, headers=head)
    # log.p(_res.headers)
    with open(path + '/' + title + '.html', 'w', encoding='utf-8') as f:
        f.write(_res.content.decode('utf-8'))
    soup = PyQuery(_res.content.decode('utf-8'))
    _公告正文 = soup('tr').text()
    # log.p(_公告正文)
    with open(path + '/' + title + '.txt', 'w', encoding='utf-8') as f:
        f.write(title + '\n\n' + _公告正文)

    soup = PyQuery(_res.content.decode('utf-8'))
    _附件下载 = soup('#attFileDomain').attr('attsdata')  # str
    if _附件下载 == '' or _附件下载 is None:
        return
    附件跳转列表 = []
    _url = 'http://oa.jklife.com/seeyon/fileDownload.do'
    for item in json.loads(_附件下载):  # list
        # log.p(item)
        formdata = {
            'method': 'download',
            'fileId': item['fileUrl'],
            'v': item['v'],
            'createDate': item['createdate'].split(' ')[0],
            'filename': item['filename'],
        }
        _res = parse_get(url=_url, params=formdata, headers=head, allow_redirects=False)
        # requests.get(url=_url, params=formdata, headers=head, allow_redirects=False)
        real_url = _res.headers['Location']  # 得到网页原始地址
        log.p(real_url)
        附件跳转列表.append((item['filename'], real_url))

    _t = 'http://oa.jklife.com'
    for item in 附件跳转列表:
        _res = parse_get(url=_t + item[1], headers=head, allow_redirects=False)
        # log.p(_res.text)
        with open(path + '/' + item[0], 'wb') as f:
            f.write(_res.content)


def main():
    log.p('开始下载公告，获取列表信息......')
    urls = get_download_url()
    log.p('总项目：' + str(len(urls)))
    log.p('获取列表信息完成，开始下载正文及附件......')
    t = 'http://oa.jklife.com/seeyon/bulData.do?method=bulView&bulId='
    # 创建多进程队列
    with Pool(25) as p:
        _ = [
            p.submit(getdown, item[0], t + item[1])for item in urls]
    '''
    for index, item in enumerate(urls):
        log.p('项目序号：' + str(index))
        getdown(item[0], t + item[1])'''
    log.p('公告正文及附件下载完成，请检查。')


if __name__ == '__main__':
    from xjLib.log import log
    log = log()
    main()
