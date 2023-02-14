# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""xx查询

Usage:
miguQuery <session> <inputfile> <outputfile>


"""

from docopt import docopt
import aiohttp
import asyncio
import sys
import os
from datetime import datetime
import json

# 使用async以及await关键字将函数异步化。在hello()中实际上有两个异步操作：首先异步获取相应，然后异步读取响应的内容。


async def fetchTest(url, jsessionId):
    async with aiohttp.ClientSession(headers={"Cookie": f"JSESSIONID={jsessionId}"}) as session:
        async with session.get(url) as resp:
            return await resp.read()


async def fetch(url, session, sem):
    # conn = aiohttp.TCPConnector(limit=30)
    # async with aiohttp.ClientSession(headers={"Cookie":"JSESSIONID={}".format(jsessionId)}) as session:
    async with sem:
        async with session.get(url) as resp:
            # 不加下面这一行的话，不会实现协程异步
            await asyncio.sleep(0)
            # read()是一个异步操作，这意味着它不会立即返回结果，仅仅返回生成器，所以添加上了await
            return await resp.read()


async def run(url, jsessionId, inputfile, outputfile):
    tasks = []
    numbers = []
    count = 0
    # 脚本名：sys.argv[0],参数1：sys.argv[1],参数2：sys.argv[2]
    #file = sys.argv[1]
    file = inputfile
    # 会报：concurrent.futures._base.TimeoutError原因为：Once it's a big number such as 30,000 it can't be physically done within 10 seconds due to networks/ram/cpu capacity.所以需要限制携程的信号量
    sem = asyncio.Semaphore(1000)
    # 将session以参数传入fetch中，让所有请求只使用一个session，而不用每个请求都创建一个session
    async with aiohttp.ClientSession(headers={"Cookie": f"JSESSIONID={jsessionId}"}) as session:
        with open(file, mode='r') as f:
            for line in f:
                # split()默认以空格分隔
                phoneNumber = line.split()[0]
                numbers.append(phoneNumber)
                # print(url.format(phoneNumber))
                #task = asyncio.ensure_future(fetch(url.format(phoneNumber), jssessionId))
                # 包装在asyncio的Future对象中，然后将Future对象列表作为任务传递给事件循环。
                task = fetch(url.format(phoneNumber), session, sem)
                tasks.append(task)

    # 它搜集所有的Future对象，然后等待他们返回
    responses = await asyncio.gather(*tasks)
    with open(outputfile, 'w') as file:
        for j in range(len(responses)):
            resJson = json.loads(responses[j].decode('utf-8'))
            if resJson["reDesc"] != "[FCMG]操作成功":
                # print('{}:{}'.format(numbers[j],responses[j].decode('utf-8')))
                file.write(f"{numbers[j]}:{responses[j].decode('utf-8')}\n")
                count += 1
    print(f"总计查询到包月号码:{count}个")
    print(f"查询结果输出到:{outputfile}")


if __name__ == '__main__':
    # 将绑定交互参数
    miguQuery = docopt(__doc__)
    session = miguQuery['<session>']
    inputfile = miguQuery['<inputfile>']
    outputfile = miguQuery['<outputfile>']
    url = "http://xxx?msisdn={}"

    if not os.path.isfile(inputfile):
        print(f"找不到此文件:{inputfile}")
        exit(0)
    if os.path.isfile(outputfile):
        print(f"文件: {outputfile} 已经存在，请保存为另一个名字")
        exit(0)
    # 创建一个asyncio loop的实例， 然后将任务加入其中
    loop = asyncio.get_event_loop()
    resp = loop.run_until_complete(fetchTest(url.format('13666198249'), session)).decode('utf-8')
    if 'login.jsp' in resp:
        print(f"当前session:{session} 不正确或已过期，请重新传入session参数")
        loop.close()
        exit(0)

    a = datetime.now()
    loop.run_until_complete(run(url, session, inputfile, outputfile))
    loop.close()
    b = datetime.now()
    print(f'Cost {(b - a).seconds} seconds')
