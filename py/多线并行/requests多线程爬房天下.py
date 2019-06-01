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
@Date: 2019-05-10 15:09:43
@LastEditTime: 2019-05-16 14:10:01
'''
import random
import re
import threading
import time

import requests
from lxml import etree

lock = threading.Lock()

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
count = 0


def fang_com(page_url):  ##列表页

    header = {}

    header['User-Agent'] = random.choice(user_agent_list)
    header.update({"Host": "esf.sz.fang.com"})
    while (1):
        ###这个主要是，fang.com会随机返回几个10054或者10053，如果连页面都没读取到，
        # 提取就是后话了，这网站没有封杀，即使使用单ip只会很少时候随机来几个10054
        # ('Connection aborted.', error(10054, ''))
        text = ''
        try:
            text = requests.get(page_url, headers=header, timeout=10).text
            #print text
        except Exception as e:
            print(e)
        if text != '':
            break

    se = etree.HTML(text)  ###########为了利于大家学习，这段演示xpath提取信息
    all_dl = se.xpath('//dl[@class="list rel"]')
    print(len(all_dl))
    for dl in all_dl:
        title = dl.xpath(
            './/dd[@class="info rel floatr"]/p[@class="title"]/a/text()')[0]

        url = dl.xpath(
            './/dd[@class="info rel floatr"]/p[@class="title"]/a/@href')[0]
        url = 'http://esf.sz.fang.com' + url

        info_list = dl.xpath(
            './/dd[@class="info rel floatr"]/p[@class="mt12"]/text()')
        #print json.dumps(info,ensure_ascii=False)    #py2显示汉字，py3可以直接print mt12
        info = ''
        for l in info_list:
            l2 = re.findall('\S*', l)[0]  ###消除空白和换行
            #print m_str
            info += l2 + '|'

        time.sleep(1)
        total_price, price_squere, huxin, cankao_shoufu, shiyong_mianji, jianzhu_mianji, years, discription = get_detail(
            url)

        lock.acquire()
        #这里叫锁，一是保证count计数准确，而是不会导致多个线程乱print，导致看不清楚。
        #加锁的目的是别的线程不能运行这段代码了。但我之前看到有的人乱加锁，把消耗时间很长的代码加锁，那样导致多线程就基本个废物
        global count
        count += 1
        print(time.strftime('%H:%M:%S', time.localtime(time.time())), '    ',
              count)
        print('列表页：')
        print(' title: %s\n url: %s\n info: %s\n' % (title, url, info))

        print('详情页:')
        print(
            ' total_price: %s\n price_squere: %s\n huxin: %s\n cankao_shoufu: %s\n shiyong_mianji: %s\n jianzhu_mianji: %s\n years: %s \n'
            % (total_price, price_squere, huxin, cankao_shoufu, shiyong_mianji,
               jianzhu_mianji, years))
        print('**************************************************************')
        lock.release()


def get_detail(url):  ###详情页

    header = {'User-Agent': random.choice(user_agent_list)}
    header.update({"Host": "esf.sz.fang.com"})

    while (1):
        content = ''
        try:
            content = requests.get(url, headers=header, timeout=10).content
        except Exception as e:
            print(e)
            pass
        if content != '':
            break

    content = content.decode('gbk').encode('utf8')
    ##查看网页源代码可看到是gbk编码，直接print的话，
    # 如果你在pycharm设置控制台是utf8编码，
    # 那么控制台的中文则会乱码，cmd是gbk的恰好可以显示。
    # 如果你在pycharm设置控制台是utf8编码，需要这样做
    #print content

    inforTxt = getlist0(
        re.findall('(<div class="inforTxt">[\s\S]*?)<ul class="tool">',
                   content))
    ###########为了利于大家学习，这段演示正则表达式提取信息，某些信息可能在有的房子界面没有，要做好判断
    #print inforTxt

    total_price = getlist0(
        re.findall('</span>价：<span class="red20b">(.*?)</span>', inforTxt))

    price_squere = getlist0(
        re.findall(
            'class="black">万</span>\((\d+?)元[\s\S]*?<a id="agantesfxq_B02_03"',
            inforTxt))
    huxin = getlist0(
        re.findall(
            '<dd class="gray6"><span class="gray6">户<span class="padl27"></span>型：</span>(.*?)</dd>',
            inforTxt))
    cankao_shoufu = getlist0(
        re.findall('参考首付：</span><span class="black floatl">(.*?万)</span> </dd>',
                   inforTxt))
    shiyong_mianji = getlist0(
        re.findall('>使用面积：<span class="black ">(.*?)</span></dd>', inforTxt))
    shiyong_mianji = getlist0(re.findall('\d+', shiyong_mianji))
    jianzhu_mianji = getlist0(
        re.findall('建筑面积：<span class="black ">(.*?)</span></dd>', inforTxt))
    jianzhu_mianji = getlist0(re.findall('\d+', jianzhu_mianji))
    years = getlist0(
        re.findall(
            '<span class="gray6">年<span class="padl27"></span>代：</span>(.*?)</dd>',
            inforTxt))

    discription = getlist0(
        re.findall(
            'style="-moz-user-select: none;">([\s\S]*?)<div class="leftBox"',
            content))
    #print discription
    #print total_price,price_squere,huxin,cankao_shoufu,shiyong_mianji,jianzhu_mianji,years

    return total_price, price_squere, huxin, cankao_shoufu, shiyong_mianji, jianzhu_mianji, years, discription


#get_detail('http://esf.sz.fang.com/chushou/3_193928457.htm')
def getlist0(list):
    if list:
        return list[0]
    else:
        return '空'


if __name__ == '__main__':
    '''
    ##这个是单线程，单线程爬很慢，3000个房子信息，一个5秒，那也得15000秒了，很耽误时间
    for i in range(1,101):
        page_url='http://esf.sz.fang.com/house/i3%s'%i
        fang_com(page_url)
    '''
    threads = []  ###这个是演示多线程爬取
    for i in range(1, 101):  #开了100线程，这样开100线程去爬100页面的详情页面，因为fang.com只能看100页
        t = threading.Thread(target=fang_com,
                             args=('http://esf.sz.fang.com/house/i3%s' % i,))

        threads.append(t)

        t.start()

    for t in threads:
        t.join()

    print('over')
'''
---------------------
作者：北风之神0509
来源：CSDN
原文：https://blog.csdn.net/qq_32897089/article/details/74519646
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
