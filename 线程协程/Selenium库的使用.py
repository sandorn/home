# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-20 19:04:42
@LastEditors: Even.Sand
@LastEditTime: 2019-05-20 19:06:49
'''

from selenium import webdriver


browser = webdriver.Chrome()
browser.get("http://www.taobao.com")
lis = browser.find_elements_by_css_selector('.service-bd li')
print(lis)
browser.close()
