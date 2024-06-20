# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2024-06-20 09:41:02
LastEditTime : 2024-06-20 09:41:09
FilePath     : /CODE/py学习/脚本/inspect-test.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import inspect
import traceback


def foo():
    bar()


def bar():
    stack = inspect.stack()
    print('<<<<<<<<<<<<<<<<<<<<<<<', stack, '>>>>>>>>>>>>>>>>>>>>>>')
    for frame_info in stack:
        frame = frame_info.frame
        filename = frame.f_code.co_filename.split('\\')[-1].split('.')[0]
        lineno = frame.f_lineno
        function_name = frame.f_code.co_name
        print(f'File: {filename}, Line: {lineno}, Function: {function_name}')


def aa():
    res = traceback.extract_stack()[-2].filename
    print(res)


aa()
# foo()
