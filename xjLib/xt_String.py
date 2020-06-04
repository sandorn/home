# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#==============================================================
#Descripttion : None
#Develop      : VSCode
#Author       : Even.Sand
#Contact      : sandorn@163.com
#Date         : 2020-02-14 13:57:28
#FilePath     : /xjLib/xt_String.py
#LastEditTime : 2020-06-04 14:11:10
#Github       : https://github.com/sandorn/home
#==============================================================
'''

import hashlib
import os
import random
import re
import threading
import time
from functools import wraps


class qsstools:
    def __init__(self):
        pass

    """定义一个读取样式的工具类"""

    @classmethod
    def set(cls, file_path, obj):
        with open(file_path, 'r', encoding='UTF-8') as f:
            obj.setStyleSheet(f.read())


def Singleton_warp(cls):
    """单例装饰器"""
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


class Singleton(object):
    """单例类"""

    """实例化 obj = Singleton()"""
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = super().__new__(cls, *args, **kwargs)
        return Singleton._instance

    def __init__(self):
        pass


def fn_timer(function):
    '''定义一个装饰器来测量函数的执行时间'''

    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running with [%s]: %.2f seconds" % (function.__name__, t1 - t0))
        return result

    return function_timer


def txt2List(filepath):
    res_list = []
    with open(filepath, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            res_list.append(line)
    return res_list


def md5(data):
    my_md5 = hashlib.md5(data.encode("utf-8", 'ignore'))
    return my_md5.hexdigest()


def stringtomd5(data):
    """将string转化为MD5"""
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(data.encode("utf-8", 'ignore'))  # 得到MD5消息摘要
    my_md5_Digest = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return my_md5_Digest


def get_sha1_value(data):
    my_sha = hashlib.sha1()
    my_sha.update(data.encode("utf-8", 'ignore'))
    my_sha_Digest = my_sha.hexdigest()
    return my_sha_Digest


def myAlign(text, distance=0):
    # #print打印对齐
    if distance == 0:
        return text
    slen = distance - len(text.encode('gbk', 'ignore'))
    text = text + ' ' * slen
    return text


def align(str1, distance, alignment='left'):
    # #print打印对齐
    length = len(str1.encode('gbk', 'ignore'))
    slen = distance - length if distance > length else 0
    if (slen % 2) == 1:
        slen = slen + 1

    if alignment == 'left':
        str1 = str1 + ' ' * slen
    elif alignment == 'right':
        str1 = ' ' * slen + str1
    elif alignment == 'center':
        str1 = ' ' * (slen // 2) + str1 + ' ' * (slen // 2)
    return str1


class filesize:
    def __init__(self, filePath):
        self.Bytes = os.path.getsize(filePath)
        self.KB = round(self.Bytes / float(1024), 2)
        self.MB = round(self.KB / float(1024), 2)

    def __str__(self):
        if self.MB > 10:
            res = str(format(self.MB, ',')) + ' MB'
        elif self.KB > 10:
            res = str(format(self.KB, ',')) + ' KB'
        else:
            res = str(format(self.Bytes, ',')) + ' Bytes'
        return res


def Ex_Re_Clean(oldtext, parlist):
    '''
    #!正则清除，自写正则表达式
    用法 newtext=Ex_Re_Clean(oldtext,['aaa','bbb'])
    '''
    pattern = re.compile('|'.join(parlist))
    return pattern.sub('', oldtext)


def Ex_Re_Replace(oldtext, REPLACEMENTS):
    '''
    #!正则替换，自写正则表达式
    用法 newtext=Ex_Re_Replace(oldtext,{'a':aaa','b':bbb'})
    '''
    pattern = re.compile('|'.join(REPLACEMENTS.keys()))
    return pattern.sub(lambda m: REPLACEMENTS[m.group(0)], oldtext)


def Ex_Re_Sub(oldtext, REPLACEMENTS):
    '''
    #@正则替换，不支持正则表达式
    用法 newtext=Ex_Re_Sub(oldtext,{'a':aaa','b':bbb'})
    '''
    pattern = re.compile('|'.join(map(re.escape, REPLACEMENTS.keys())))

    def one_xlat(match):
        return REPLACEMENTS[match.group(0)]

    return pattern.sub(one_xlat, oldtext)
    '''
    re.sub(`pattern`, `repl`, `string`, `count=0`, `flags=0`)
    `pattern`, `repl`, `string` 为必选参数
    `count`, `flags` 为可选参数
    `pattern`正则表达式
    `repl`被替换的内容，可以是字符串，也可以是函数
    `string`正则表达式匹配的内容
    `count`由于正则表达式匹配的结果是多个，使用count来限定替换的个数从左向右，默认值是0，替换所有的匹配到的结果
    `flags`是匹配模式，`re.I`忽略大小写，`re.L`表示特殊字符集\w,\W,\b,\B,\s,\S，`re.M`表示多行模式，`re.S` ‘.’包括换行符在内的任意字符，`re.U`表示特殊字符集\w,\W,\b,\B,\d,\D,\s,\D
    '''


def Ex_Str_Replace(oldtext, adict):
    '''
    #@字符替换，不支持正则表达式
    用法 newtext=Ex_Str_Replace(oldtext,{'a':aaa','b':bbb'})
    '''

    def _run(_text, key, value):
        return _text.replace(key, value)

    for key in adict:
        oldtext = _run(oldtext, key, adict[key])
    return oldtext


def string_split_join_with_maxlen_list(string, maxlen=300):
    newText = []
    _temp = ''

    _temp_list = string.strip().split('\n')
    line_Text = [item.strip() for item in _temp_list]
    line_Text[0] = line_Text[0] + '。'  # 章节标题加间隔

    for index, text in enumerate(line_Text):
        if len(text) > maxlen:
            if _temp != '':
                newText.append(_temp)
                _temp = ''

            temp = text.strip().split('。')
            long = round(len(temp) / 2)
            newText.append('。'.join(temp[:long]) + '。')
            newText.append('。'.join(temp[long:]))
            continue

        if len(_temp) < maxlen:
            if len(_temp + text.strip()) < maxlen:
                _temp += text
                # @ 标记1
            else:
                newText.append(_temp)
                newText.append(text)
                _temp = ''

    # @ 标记1,最后处理临时变量
    if _temp != '':
        newText.append(_temp)
        _temp = ''

    return newText


def dict2qss(dict):
    '''字典形式的QSS转字符串'''
    # # 排序  print key, dict[key] for key in sorted(dict.keys())
    import json

    temp = json.dumps(dict)
    qss = Ex_Re_Sub(temp, {',': ';', '"': '', ': {': '{'})
    return qss.strip('{}')


def list2file(_filename, _list_texts, br='\t'):
    # 函数说明:将爬取的文章内容写入文件,只能1层
    print('[' + _filename + ']开始保存......')
    _list_texts.sort()
    with open(_filename, 'w', encoding='utf-8') as file:
        file.write(_filename + '\n')
        file.write('   key   \tpage\tindex\ttitle\turl\t\n')
        for key in _list_texts:  # 区分关键字
            for index in key:  # 区分记录index
                [file.write(str(v) + br) for v in index]
                file.write('\n')

    size = f"size: {filesize(_filename)}"
    print('[{}]保存完成\t{}\ttime:{}。'.format(_filename, size, get_time()))

    # #换行有问题[f.write(str(v) + '\t') for key in lists for index in key for v in index]


def savefile(_filename, _list_texts, br=''):
    '''   函数说明:将爬取的文章内容写入文件,迭代多层   '''
    '''   br为标题换行标志，可以用'\t'   '''
    '''   多层次的list 或 tuple写入文件   '''

    with open(_filename, 'w', encoding='utf-8') as file:
        file.write(_filename + '\n')

        def each(data):
            for index, value in enumerate(data):
                if isinstance(value, list) or isinstance(value, tuple):
                    each(value)
                else:
                    file.write(str(value) + br)
                    if index == len(data) - 1:
                        file.write('\n')

        each(_list_texts)

    size = f"size: {filesize(_filename)}"
    print('[{}]保存完成\t{}\ttime:{}。'.format(_filename, size, get_time()))


def flatten(nested):
    try:
        # 不要迭代类似字符串的对象：
        # if isinstance(variate,list) or isinstance(variate,tuple):
        try:
            nested + ''
        except TypeError:
            pass
        else:
            raise TypeError

        for sublist in nested:
            for element in flatten(sublist):
                yield element
    except TypeError:
        yield nested


def get_stime():
    import datetime

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return time_now


def get_time():
    import datetime

    time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    return time_now


def timestr_10_timestamp(timestr):
    '''
    函数功能：获取特定时间的时间戳；时间字符串->时间戳
    '''
    # timestr = '2017-12-20 12:00:00'
    timearray = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    # 将时间数组转换成时间戳，使用mktime()函数得到的是一个浮点数，需要进行强制类型转换
    timestamp = int(time.mktime(timearray))
    return timestamp


def timestr_to_13timestamp(timestr):
    '''
    函数作用：将制定的时间字符串转换成13位时间戳
    '''
    return timestr_10_timestamp(timestr) * 1000


def get_10_timestamp():
    '''
    函数功能：获取当前时间的时间戳（10位）
    '''
    # 13位时间戳的获取方式跟10位时间戳获取方式一样
    # 两者之间的区别在于10位时间戳是秒级，13位时间戳是毫秒级
    timestamp = time.time()
    return int(round(timestamp))


def get_13_timestamp():
    '''
    函数功能：获取当前时间的时间戳（13位）
    '''
    return get_10_timestamp() * 1000


def random_20char(length, string=[]):
    """实现指定长度的随机数"""
    for i in range(length):
        x = random.randint(1, 2)
        if x == 1:
            y = str(random.randint(0, 9))
        else:
            y = chr(random.randint(97, 122))
        string.append(y)
    string = ''.join(string)
    return string


def toMysqlDateTime():
    import datetime

    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return dt


class _x:
    """
     从简单数据类型转换成python对象

     p = _x({'name':'boob','body':{'color':'black'},'toys':[1,2,3,],'age':100})
     print p['toys'][1]
     print len(p.toys)
     print p.body.colors
     """

    def __init__(self, primitive):
        self.data = primitive

    def __getattr__(self, item):
        value = self.data.get(item, None)
        if isinstance(value, dict):
            value = _x(value)
        return value

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __getitem__(self, item):
        # value = self.__getattribute__(item)
        value = None
        if type(self.data) in (list, tuple):
            value = self.data[item]
            if type(value) in (dict, list, tuple):
                value = _x(value)
        elif isinstance(self.data, dict):
            value = self.__getattr__(item)
        return value


if __name__ == "__main__":
    pass
