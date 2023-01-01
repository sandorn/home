# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  :
Develop      : VSCode
Author       : Even.Sand
Contact      : sandorn@163.com
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-01-01 21:41:19
FilePath     : /py学习/PY编程模式/代理模式-2.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


class Browser(object):

    def __init__(self, class_):
        if class_ == webdriver.Chrome:
            self.driver = webdriver.Chrome()

    def find_element_through_id(self, id):
        self.driver.find_element_by_id(id)
        print(f'通过 {id} 查找这个元素')


class Element():

    def __init__(self, ele):
        """
        :type ele:WebElement
        """
        self.ele = ele

    def click(self):
        self.ele.click()
        time.sleep(2)

    def input(self, value):
        self.ele.send_keys(value)
        print(f'填了一个值: {value}')
        time.sleep(3)


browser = Browser(webdriver.Chrome)
Element(browser.find_element_through_id('shurukuang_id')).input('hello world')
Element(browser.find_element_through_id('button_id')).click()
