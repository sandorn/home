# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# ==============================================================
# Descripttion : None
# Develop      : VSCode
# Author       : Even.Sand
# Contact      : sandorn@163.com
# Date         : 2020-02-14 13:57:28
#FilePath     : /xjLib/xt_String.py
#LastEditTime : 2020-06-16 19:13:44
# Github       : https://github.com/sandorn/home
# ==============================================================
#  string  |  dict  |  list  |  tupe  |  json
'''

import hashlib
import json
import random
import re
from functools import reduce


def md5(data):
    my_md5 = hashlib.md5(data.encode("utf-8", 'ignore'))
    return my_md5.hexdigest()


def Exmd5(data):
    """将string转化为MD5"""
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(data.encode("utf-8", 'ignore'))  # 得到MD5消息摘要
    my_md5_Digest = my_md5.hexdigest()  # 以16进制返回消息摘要，32位
    return my_md5_Digest


def sha1(data):
    my_sha = hashlib.sha1()
    my_sha.update(data.encode("utf-8", 'ignore'))
    my_sha_Digest = my_sha.hexdigest()
    return my_sha_Digest


def duplicate(iterable, keep=lambda x: x, key=lambda x: x, reverse=False):
    """
    保序去重
    :param iterable:
    :param keep: 去重的同时要对element做的操作
    :param key: 使用哪一部分去重
    :param reverse: 是否反向去重
    :return:
    """
    result = list()
    duplicator = list()
    if reverse:
        iterable = reversed(iterable)
    for i in iterable:
        keep_field = keep(i)
        key_words = key(i)
        if key_words not in duplicator:
            result.append(keep_field)
            duplicator.append(key_words)
    return list(reversed(result)) if reverse else result


def chain_all(iterobj):
    """连接多个序列或字典"""
    iterobj = list(iterobj)
    if not iterobj:
        return []
    if isinstance(iterobj[0], dict):
        result = {}
        for i in iterobj:
            result.update(i)
    else:
        result = reduce(lambda x, y: list(x) + list(y), iterobj)
    return result


def align(str1, distance=66, alignment='left'):
    # #居中打印为string类方法
    if alignment == 'center':
        return (str1.center(distance, ' '))

    # #print打印对齐
    length = len(str1.encode('gbk', 'ignore'))
    slen = distance - length if distance > length else 0

    if alignment == 'left':
        str1 = str1 + ' ' * slen
    elif alignment == 'right':
        str1 = ' ' * slen + str1
    return str1


def Ex_Re_Repl(string, trims=None):
    '''
        格式化html string, 去掉多余的字符，类，script等。
        #!正则替换，自写正则表达式
        string:欲处理的字符串
        trims:list内包含tuple或list
        tuple[0]:被替换
        tuple[1]:替换为
    '''
    # 第一种方法
    if trims is None:
        trims = [(r'\n', ''), (r'\t', ''), (r'\r', ''), (r'  ', ''),
                 (r'\u2018', "'"), (r'\u2019', "'"), (r'\ufeff', ''),
                 (r'\u2022', ":"), (r"<([a-z][a-z0-9]*)\ [^>]*>", r'<\g<1>>'),
                 (r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', ''),
                 (r"</?a.*?>", '')]

    def run(str_tmp, replacement):
        return re.sub(replacement[0], replacement[1], str_tmp)

    return reduce(run, trims, string)
    # 第二种写法，用lamda # string为初始值，最后传入，在lambda中最先接收
    # return reduce(lambda str_tmp, replacement: re.sub(replacement[0], replacement[1], str_tmp), trims, string)
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


def Ex_Str_Replace(string, trims):
    '''
        # @字符替换，不支持正则表达式
        string:欲处理的字符串
        trims:list内包含tuple或list
        tuple[0]:被替换
        tuple[1]:替换为
    '''
    # 第一种方法
    # for item in trims:
    #     string = string.replace(item[0], item[1])
    # return string

    # 第二种方法  # string为初始值，最后传入，在lambda中最先接收
    return reduce(lambda string, item: string.replace(item[0], item[1]), trims,
                  string)


def Ex_Re_Clean(oldtext, parlist):
    '''
    #!正则清除，自写正则表达式
    用法 newtext=Ex_Re_Clean(oldtext,['aaa','bbb'])
    '''
    pattern = re.compile('|'.join(parlist))
    return pattern.sub('', oldtext)


def Ex_Re_Replace(string, REPLACEMENTS):
    '''
    #!正则替换，自写正则表达式
    用法 newtext=Ex_Re_Replace(oldtext,{'a':aaa','b':bbb'})
    '''
    pattern = re.compile('|'.join(REPLACEMENTS.keys()))
    return pattern.sub(lambda m: REPLACEMENTS[m.group(0)], string)


def Ex_Re_Sub(string, REPLACEMENTS):
    '''
    # @正则替换，不支持正则表达式
    用法 newtext=Ex_Re_Sub(string,{'a':aaa','b':bbb'})
    '''
    pattern = re.compile('|'.join(map(re.escape, REPLACEMENTS.keys())))

    def one_xlat(match):
        return REPLACEMENTS[match.group(0)]

    return pattern.sub(one_xlat, string)


def string_split_limited_list(string, maxlen=300):
    # #仅按照长度分割
    # #newText = [string[i:i+maxlen] for i in range(0, len(string), maxlen)]
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


def dict2qss(dict_tmp):
    '''字典形式的QSS转字符串'''
    # # 排序  print key, dict[key] for key in sorted(dict.keys())
    isinstance(dict_tmp, dict)
    temp = json.dumps(dict_tmp)
    qss = Ex_Re_Sub(temp, {',': ';', '"': '', ': {': '{'})
    return qss.strip('{}')


def groupby(iterobj, key):
    '''
    自实现groupby，return: 字典对象
    itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    '''
    groups = dict()
    for item in iterobj:
        groups.setdefault(key(item), []).append(item)
    return groups


def random_char(length=20, string=[]):
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


def class_to_dict(in_obj):
    '''把对象转换成字典'''
    dict = {}
    if len(in_obj.__dict__) > 0:
        dict.update(in_obj.__dict__)
    else:
        dict.update({
            key: getattr(in_obj, key)
            for key in dir(in_obj)
            if not key.startswith('__') and not callable(getattr(in_obj, key))
        })
    return dict


if __name__ == "__main__":
    print(align('myAliggn1', 66))
    print(align('myAliggn2', 66, alignment='right'))
    print(align('myAliggn3', 66, alignment='center'))
