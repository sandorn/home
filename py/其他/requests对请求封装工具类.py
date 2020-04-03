# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-04-02 17:20:52
@LastEditors: Even.Sand
@LastEditTime: 2020-04-02 17:21:12
'''


import requests
import json

from apitest.resquestsTests import datas_tests


class requestsUtils:
    def post_main(self, method, url, data, header):
        global res
        if method == "post":
            if header == "form-data":
                res = requests.post(url=url, data=data)

            if header == "Content-type:application/json":
                res = requests.post(url=url, json=data)
        return json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=4)

    def get_main(self, method, url, data, header):
        global res
        if method == "get":
            if header is not None:
                res = requests.get(url=url, data=data, headers=header)
            else:
                res = requests.get(url=url, data=data)
        return json.dumps(res.json(), ensure_ascii=False, sort_keys=True, indent=4)


if __name__ == '__main__':
    print(requestsUtils().post_main(method=datas_tests.post_method, url=datas_tests.test_url + datas_tests.get_lujing, data={"userid": datas_tests.uid, "activityid": datas_tests.activityid}, header=datas_tests.header))
