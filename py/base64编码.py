# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-06-27 13:43:34
@LastEditors: Even.Sand
@LastEditTime: 2019-06-27 14:06:06
'''
import base64

#import urllib.parse
chinese_str = bytes('中mbaoir=3-p.0927820985文', 'utf8')
# 先进行gb2312编码
#chinese_str = chinese_str.encode('gb2312')
# print(chinese_str)
# 输出 b'\xd6\xd0mbaoir=3-p.0927820985\xce\xc4'
# 再进行urlencode编码
#chinese_str_url = urllib.parse.quote(chinese_str)
# print(chinese_str_url)
# 输出 %D6%D0%CE%C4

base64_data = base64.b64encode(chinese_str)
print(base64_data.decode())

ori_data = str(base64.b64decode(base64_data), 'utf8')
print(ori_data)
