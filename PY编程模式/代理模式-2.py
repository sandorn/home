# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-07-20 09:44:05
#FilePath     : /PY编程模式/代理模式-2.py
#LastEditTime : 2020-07-20 09:44:28
#Github       : https://github.com/sandorn/home
#==============================================================
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
        print('通过 ' + id + ' 查找这个元素')


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
        print('填了一个值: ' + value)
        time.sleep(3)


browser = Browser(webdriver.Chrome)
Element(browser.find_element_through_id('shurukuang_id')).input('hello world')
Element(browser.find_element_through_id('button_id')).click()
