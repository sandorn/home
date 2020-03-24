# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2020-03-20 12:45:12
@LastEditors: Even.Sand
@LastEditTime: 2020-03-20 14:20:54
'''
import os
import time

from celery import Celery

# 指定任务名tasks（和文件名一致）
task_name = os.path.basename(__file__).split(".")[0]
# 创建了celery实例app，实例化的过程中，传入了broker
my_task = Celery(task_name, broker="redis://127.0.0.1:6379", backend="redis://127.0.0.1:6379")


@my_task.task
def add(x,y):
    print('add ...')
    time.sleep(0.5)
    return x + y


#'celery -A tasks worker --loglevel=info'
#my_task.start(argv=[task_name, 'worker', '-l', 'info', '-f', 'logs/celery.log'])
my_task.start(argv=[task_name, 'worker', '-l', 'info'])
