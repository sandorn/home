# !/usr/bin/env python
# -*- coding: utf-8 -*-

from xjLib.mystr import myAlign
from xjLib.mystr import align


'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2020-02-20 16:51:43
@LastEditors: Even.Sand
@LastEditTime: 2020-02-20 17:55:30
'''

print(len('zh制订问题333333头部注释None'.encode('GBK')))
print(len('zh制订问题333333头部注释None'))
print(myAlign('zh制订问题333333', 40) + myAlign('zh制333', 30) + '\t|达成')
print(myAlign('zh制33', 40) + myAlign('zh制333', 30) + '\t|达成')
print(myAlign('zh制订问题333333头部注释None', 40) + myAlign('zh制333', 30) + '\t|达成')
print(myAlign('制订问题', 40) + myAlign('zh制333', 30) + '\t|达成')
print(align('姓名', 20), align('电话', 20), align('QQ', 20), align('邮箱', 20))

print(align('cxj', 20), align('17854264217', 20),
      align('1239112948', 20), align('1239112948@qq.com', 20))

print(align('陈丽丽', 20), align('17854264217', 20),
      align('1239112948', 20), align('1239112948@qq.com', 20))
