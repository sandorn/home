# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2020, NewSea
@Date: 2019-05-03 23:26:06
@LastEditors: Even.Sand
@LastEditTime: 2020-04-03 11:02:56
'''


def example1():
    some_tuple = (1, 2, 3, 'a')
    some_variable = {
        'long':
        'Long code lines should be wrapped within 79 characters.',
        'other': [
            math.pi, 100, 200, 300, 9876543210,
            'This is a long string that goes on'
        ],
        'more': {
            'inner': 'This whole logical line should be wrapped.',
            some_tuple: [1, 20, 300, 40000, 500000000, 60000000000000000]
        }
    }
    return (some_tuple, some_variable)


def example2():
    return ('' in {'f': 2}) in {'has_key() is deprecated': True}


class Example3(object):
    def __init__(self, bar):
        # Comments should have a space after the hash.
        if bar:
            bar += 1
            bar = bar * bar
        else:
            some_string = """
                       Indentation in multiline strings should not be touched.Only actual code should be reindented.
                        """
