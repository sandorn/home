'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-14 20:44:26
@LastEditors: Even.Sand
@LastEditTime: 2019-05-14 21:00:51
'''
import requests
from lxml import etree
import time
from multiprocessing import Pool


def main(url):
    time.sleep(1)
    html = requests.get(url)
    html.encoding = 'gb2312'
    data = etree.HTML(html.text)
    title = data.xpath('//a[@class="ulink"]/text()')
    summary = data.xpath('//td[@colspan="2"]/text()')
    urls = data.xpath('//a[@class="ulink"]/@href')
    for t, s, u in zip(title, summary, urls):
        print(t)
        print('【url:】http://www.dytt8.net' + u)
        print('【简介】>>>>>>>' + s)


if __name__ == '__main__':
    start = time.time()
    url = 'http://www.dytt8.net/html/gndy/dyzz/'
    pg_url = [url + 'list_23_{}.html'.format(str(x)) for x in range(1, 10)]
    # for pg_u in pg_url:
    #     main(pg_u)
    p = Pool()
    p.map(main, pg_url)
    end = time.time()
    print("共计用时%.4f秒" % (end - start))
