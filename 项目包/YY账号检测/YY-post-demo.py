# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:57
LastEditTime : 2022-12-22 20:53:06
FilePath     : /项目包/YY账号检测/YY-post-demo.py
Github       : https://github.com/sandorn/home
==============================================================
'''
import json

import requests


def set_cookies(cookies):
    # 将CookieJar转为字典：
    res_cookies_dic = requests.utils.dict_from_cookiejar(cookies)
    # 将新的cookies信息更新到手动cookies字典
    for i in res_cookies_dic.keys():
        cookies[i] = res_cookies_dic[i]
    return cookies


def main(user, pwd):
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'aq.yy.com',
        'RequestType': 'AJAX',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Referer': 'https://aq.yy.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }

    session = requests.session()
    #session.keep_alive = True
    # 设置请求头信息
    session.headers = head
    #requests.utils.add_dict_to_cookiejar(session.cookies, cookies)

    response = session.post("https://aq.yy.com/p/wklogin.do?callbackURL=https://aq.yy.com/welcome.do")
    # log.print(response.text)
    # log.print(response.cookies)
    session.cookies = set_cookies(response.cookies)

    _sp = json.loads(response.text)
    #ttokensec = _sp['ttokensec']
    url = _sp['url']
    #ttoken = ['ttoken']
    oauth_token = url.split('?')[1].split('=')[1]

    url = "https://lgn.yy.com/lgn/oauth/x2/s/login_asyn.do"
    data = "username=" + user + "&pwdencrypt=105bb78ffda9c8abd57ffda9d6085b39b518510a9bf849e37ce6d5ddab49600e9d8a128814458e93de4ab820f12e0fff4ce323daedb41dadd4cf37d4a4a955ac987aaacc7f26daa0f39cd8037116933f9efd18facf824d71e21c74aaeaa28f944fd63ce56f77a09891c4d2e90d105cfd5ddd4494136cf9ac897b053203beaa86&oauth_token=" + oauth_token + "&denyCallbackURL=&UIStyle=xelogin&appid=1&mxc=&vk=&isRemMe=0&mmc=&vv=&hiido=1"
    response = session.post(url, data)
    print(response.text)


if __name__ == "__main__":
    user = 'chen8997447@163.com'
    pwd = '1234567890'
    main(user, pwd)
