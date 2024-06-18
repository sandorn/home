"""
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2022-12-29 00:45:59
FilePath     : /项目包/线程小成果/CF-Pool进程池.PY
Github       : https://github.com/sandorn/home
==============================================================
python线程池ThreadPoolExecutor与进程池ProcessPoolExecutor - Harvard_Fly - 博客园
https://www.cnblogs.com/FG123/p/9704233.html
"""

import os

# from concurrent.futures import ProcessPoolExecutor as Pool  # 进程池模块
from concurrent.futures import ThreadPoolExecutor as Pool  # 线程池模块
from concurrent.futures import as_completed, wait

from xt_File import savefile
from xt_Ls_Bqg import get_contents, get_download_url
from xt_Time import fn_timer

texts = []


def callback_func(future):
    # 回调方式获取线程结果
    index, name, text = future.result()  # 回调函数取得返回值
    texts.append([index, name, text])


@fn_timer
def main_callback(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        _ = [pool.submit(get_contents, index, urls[index]).add_done_callback(callback_func) for index in range(len(urls))]

    texts.sort(key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}add_done_callback.txt', texts, br='\n')


@fn_timer
def main_completed(max, bookname, urls):
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = [pool.submit(get_contents, index, urls[index]) for index in range(len(urls))]

    texts = []
    for future in as_completed(future_tasks):  # 迭代生成器
        try:
            resp = future.result()
            texts.append(resp)
        except Exception as e:
            print(f'{e}')

    textssord = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}main_as_completed.txt', textssord, br='\n')


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
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}main_wait.txt', textssord, br='\n')


@fn_timer
def main_map(max, bookname, urls):
    indexs: list[int] = list(range(len(urls)))
    # 创建多进程队列
    with Pool(max) as pool:
        future_tasks = pool.map(get_contents, indexs, urls)

    texts = list(future_tasks)
    texts = sorted(texts, key=lambda x: x[0])
    files = os.path.split(__file__)[-1].split('.')[0]
    savefile(f'{files}&{bookname}main_map.txt', texts, br='\n')


if __name__ == '__main__':
    url = 'https://www.bigee.cc/book/6909/'
    bookname, urls, _ = get_download_url(url)
    urls = urls
    # main_map(60, bookname, urls)
    main_wait(200, bookname, urls[:20])
    # main_completed(32, bookname, urls)
    # main_callback(200, bookname, urls)

r"""
1、建立线程池:executor = ThreadPoolExecutor(max_workers= )
2、提交执行函数到线程池:task = executor.submit(func,(args))
3、获取执行结果:task.result()
4、判断线程是否完成:task.done()
5、取消还没执行的线程:task.cancel()
6、利用as_completed获取线程完成结果
all_task = [executor.submit(get_html,(url)) for url in urls]
for future in as_completed(all_task):
    data = future.result()
    print("get page {}".format(data))

7、通过executor的map获取已经完成的task值
for data in executor.map(get_html,urls):
    print(data)

8、使用wait()方法阻塞线程
"""
