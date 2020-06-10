# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-06-09 14:49:33
#FilePath     : /py学习/grab爬虫框架学习.py
#LastEditTime : 2020-06-09 15:48:30
#Github       : https://github.com/sandorn/home
#==============================================================
'''
import logging

from grab.spider import Spider, Task

logging.basicConfig(level=logging.DEBUG)


class ExampleSpider(Spider):
    def task_generator(self):
        for lang in 'python', 'ruby', 'perl':
            url = 'https://www.baidu.com/s?wd=%s' % lang
            yield Task('search', url=url, lang=lang)

    def task_search(self, grab, task):
        print('%s: %s' % (task.lang,
                          grab.doc('//div[@class="f13"]//a').text()))


bot = ExampleSpider(thread_number=2)
bot.run()
