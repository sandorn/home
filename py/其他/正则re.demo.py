'''
@Descripttion: 头部注释None
@Develop: VSCode
@Author: Even.Sand
@Contact: sandorn@163.com
@Github: https://github.com/sandorn/home
@License: (C)Copyright 2009-2019, NewSea
@Date: 2019-05-20 13:33:42
@LastEditors: Even.Sand
@LastEditTime: 2019-05-20 13:34:33
'''
import re
regex = r'^[^\\/:\*\?"<>\|]+$'  # 不能为空，不能含有\/:*?"<>|等字符
tests = ['abc_def',
         'abc.def',
         'abc/def',
         '\?"',
         '']
matches = [i for i in tests if re.match(regex, i)]
print(matches)
