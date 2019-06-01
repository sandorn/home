'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-12 16:06:11
@LastEditors: Even.Sand
@LastEditTime: 2019-05-19 13:27:27
'''
import requests
import random
from lxml import etree
import os
import time
from multiprocess import process

# 爬取的主域名
HOST = 'http://www.biqugecom.com'
# User-Agent
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
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


# 爬取一本小说
class ScrapyOne(object):

    def __init__(self, rootLink):
        super(ScrapyOne, self).__init__()
        self.rootLink = rootLink

    # 爬取每章的链接
    def scrapyLink(self):
        try:
            # 随机生成请求头
            header = {"User-Agent": random.choice(user_agent)}
            res = requests.get(self.rootLink, headers=header)
            res.encoding = 'gbk'
            # 解析HTML
            data = etree.HTML(res.text)
            links = []
            # 获取书名
            bookname = data.xpath("//*[@id='info']/h1/text()")[0]
            # 获取每章的链接，由于前9个是推荐章节，因此从第10个开始爬
            for link in data.xpath("//*//dd//a/@href")[9:]:
                links.append(HOST + link)
            if links:
                return {'bookname': bookname, 'links': links}
            else:
                return []
        except Exception as e:
            print(e)
            return []

    # 爬取一章的内容
    def scrapyText(self, url):
        try:
            header = {"User-Agent": random.choice(user_agent)}
            res = requests.get(url, headers=header)
            res.encoding = 'gbk'
            data = etree.HTML(res.text)
            # 获取章节名
            name = data.xpath("//*[@class='bookname']/h1/text()")[0]
            texts = []
            # 获取小说内容
            for text in data.xpath("//*[@id='content']/text()"):
                text = text.replace('\r\n', '').replace('\xa0\xa0\xa0\xa0', '')
                if text:
                    texts.append(text)
            if texts:
                return {'name': name, 'texts': texts}
            else:
                return False
        except Exception as e:
            print(e)
            return False

    # 保存一章
    def save(self, bookname, name, texts):
        try:
            # 文件夹不存在则以小说名字创建
            if not os.path.exists('./' + bookname):
                os.makedirs('./' + bookname)
            with open(
                    './%s/%s.txt' % (bookname, name), 'w',
                    encoding='UTF - 8 - sig') as f:
                f.write(name + '\n')
                for text in texts:
                    f.write(text + '\n')
            f.close()
            return True
        except Exception as e:
            print(e)
            return False

    # 主函数
    def main(self):
        try:
            # 获取书的章节信息
            bookInfo = self.scrapyLink()
            # 这里的i主要是为了方便爬取出的小说在资源管理器好排序
            i = 0
            for link in bookInfo['links']:
                # 获取一章的内容
                time.sleep(random.randint(1, 3))
                info = self.scrapyText(link)
                if info:
                    if self.save(bookInfo['bookname'],
                                 str(i) + '-' + info['name'], info['texts']):
                        print('存储成功', info['name'])
                    else:
                        print('存储失败', info['name'])
                    i += 1
        except Exception as e:
            print(e)


# 获取每个分类下的小说链接
def scrapyRootLink(url):
    try:
        header = {"User-Agent": random.choice(user_agent)}
        res = requests.get(url, headers=header)
        res.encoding = 'gbk'
        data = etree.HTML(res.text)
        links = []
        for link in data.xpath(
                "//*[@class='media-heading book-title']/a/@href"):
            if link:
                links.append(link)
        if links:
            print('分类已完毕 %s' % (url))
            return links
        else:
            return []
    except Exception as e:
        print(e)
        return []


# 爬取进程
class ScrapyProcess(process):

    def __init__(self, typeLink):
        super(ScrapyProcess, self).__init__()
        self.typeLink = typeLink

    def run(self):
        rootLinks = scrapyRootLink(self.typeLink)
        for rootLink in rootLinks:
            print('开始爬取', rootLink)
            # 爬取一本小说
            one = ScrapyOne(rootLink)
            one.main()


if __name__ == "__main__":
    for i in range(1, 9):
        # 为每个分类下的爬取创建一个进程
        process = ScrapyProcess('http://www.xbiquge.la/fenlei/%s-1.html' %
                                (str(i)))
        process.start()
'''
---------------------
作者：程序猿洋洋
来源：CSDN
原文：https://blog.csdn.net/hhy1107786871/article/details/88177482
版权声明：本文为博主原创文章，转载请附上博文链接！'''
