
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-18 05:28:03
@LastEditors: Even.Sand
@LastEditTime: 2020-03-30 21:24:21

python线程池ThreadPoolExecutor与进程池ProcessPoolExecutor - Harvard_Fly - 博客园
https://www.cnblogs.com/FG123/p/9704233.html
'''


# from concurrent.futures import ProcessPoolExecutor as Pool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
from concurrent.futures import as_completed, wait
import os

from xjLib.mystr import Ex_Re_Sub, savefile, Ex_Replace, fn_timer
from xjLib.req import parse_get


def get_download_url(target):
    urls = []  # 存放章节链接
    response = parse_get(target).html
    _bookname = response.xpath('//meta[@property="og:title"]//@content')[0]
    全部章节节点 = response.xpath('//div[@class="listmain"]/dl/dt[2]/following-sibling::dd/a/@href')

    for item in 全部章节节点:
        _ZJHERF = 'https://www.biqukan.com' + item
        urls.append(_ZJHERF)
    return _bookname, urls


def get_contents(index, target):
    response = parse_get(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  \xa0"),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            '\xa0': '',  # 表示空格  &nbsp;
            '\u3000': '',  # 全角空格
            'www.biqukan.com。': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            '笔趣看;': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '<br />': '',
            '\r\r': '\n',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        },
    )

    return [index, name, '    ' + text]


def map_get_contents(args):
    [index, target] = args
    response = parse_get(target).html

    _name = "".join(response.xpath('//h1/text()'))
    _showtext = "".join(response.xpath('//*[@id="content"]/text()'))
    name = Ex_Re_Sub(_name, {' ': ' ', '\xa0': ' '})
    text = Ex_Replace(
        _showtext.strip("\n\r　  \xa0"),
        {
            '　　': '\n',
            ' ': ' ',
            '\', \'': '',
            '\xa0': '',  # 表示空格  &nbsp;
            '\u3000': '',  # 全角空格
            'www.biqukan.com。': '',
            'm.biqukan.com': '',
            'wap.biqukan.com': '',
            'www.biqukan.com': '',
            '笔趣看;': '',
            '百度搜索“笔趣看小说网”手机阅读:': '',
            '请记住本书首发域名:': '',
            '请记住本书首发域名：': '',
            '笔趣阁手机版阅读网址:': '',
            '笔趣阁手机版阅读网址：': '',
            '[]': '',
            '<br />': '',
            '\r\r': '\n',
            '\r': '\n',
            '\n\n': '\n',
            '\n\n': '\n',
        },
    )

    return [index, name, '    ' + text]


texts = []


def callback(future):
    # 回调方式获取线程结果
    index, name, text = future.result()  # 回调函数取得返回值
    texts.append([index, name, text])


@fn_timer
def main_add_done_callback(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        _ = [
            pool.submit(get_contents, index, urls[index]).add_done_callback(callback)
            for index in range(len(urls))
        ]

    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'add_done_callback.txt', texts, br='\n')


@fn_timer
def main_as_completed(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = [pool.submit(get_contents, index, urls[index]) for index in range(len(urls))]

    texts = []
    for future in as_completed(future_tasks):  # 迭代生成器
        try:
            resp = future.result()
            texts.append(resp)
        except Exception as e:
            print('%s' % e)

    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'main_as_completed.txt', textssord, br='\n')


@fn_timer
def main_wait(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = [pool.submit(get_contents, index, urls[index]) for index in range(len(urls))]

    texts = []

    try:
        result = wait(future_tasks)
        done_set = result[0]
        for future in done_set:
            resp = future.result()
            texts.append(resp)
    except Exception as e:
        print('exception :', e)

    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'main_wait.txt', textssord, br='\n')


@fn_timer
def main_map(max, bookname, urls):
    args = []
    for index, url in enumerate(urls):
        args.append([index, url])
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = pool.map(map_get_contents, args)

    texts = []
    for resp in future_tasks:  # 此时将阻塞 , 直到线程完成或异常
        texts.append(resp)

    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split(".")[0]
    savefile(files + '＆' + bookname + 'main_map.txt', textssord, br='\n')


if __name__ == '__main__':
    bookname, urls = get_download_url('https://www.biqukan.com/2_2714/')

    main_map(99, bookname, urls)
    main_wait(99, bookname, urls)
    main_as_completed(99, bookname, urls)
    main_add_done_callback(99, bookname, urls)

    '''
    # "2_2714"   #《武炼巅峰》664万字 99线程。
    [笔趣阁-CF-Pool进程池＆武炼巅峰main_map.txt]保存完成	size：46.46 MB	time:21:18:08.876504。
    Total time running with [main_map]: 73.25 seconds
    [笔趣阁-CF-Pool进程池＆武炼巅峰main_wait.txt]保存完成	size：46.46 MB	time:21:19:17.762426。
    Total time running with [main_wait]: 68.89 seconds
    [笔趣阁-CF-Pool进程池＆武炼巅峰main_as_completed.txt]保存完成	size：46.46 MB	time:21:20:27.554502。
    Total time running with [main_as_completed]: 69.79 seconds
    [笔趣阁-CF-Pool进程池＆武炼巅峰add_done_callback.txt]保存完成	size：46.46 MB	time:21:21:39.551876。
    Total time running with [main_add_done_callback]: 71.97 seconds
    '''

'''
1、建立线程池：executor = ThreadPoolExecutor(max_workers= )
2、提交执行函数到线程池：task = executor.submit(func,(args))
3、获取执行结果：task.result()
4、判断线程是否完成：task.done()
5、取消还没执行的线程：task.cancel()
6、利用as_completed获取线程完成结果
all_task = [executor.submit(get_html,(url)) for url in urls]
for future in as_completed(all_task):
    data = future.result()
    print("get page {}".format(data))

7、通过executor的map获取已经完成的task值
for data in executor.map(get_html,urls):
    print(data)

8、使用wait()方法阻塞线程
————————————————
版权声明：本文为CSDN博主「释晓」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sinat_34461756/article/details/83866300
'''
