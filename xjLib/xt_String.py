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
'''
    #统计一个list中各个元素出现的次数
    #方法1，使用字典
    from random import randint
    data = [randint(1,10) for _ in rang(10)]
    # 把data里的数据作为key来创建一个字典，且value初始化为0
    dic = dict.fromkeys(data, 0)
    for x in data:
    dic[x] += 1
    #dic 中key为元素，value为该元素出现次数

    #方法2，使用Counter()
    from collections import Counter()
    data = [randint(1,10) for _ in range(10)]
    # 得到的dic2和方法1的dic一样，一条代码解决问题！
    dic2 = Counter(data)
    # 并且还可以使用most_common(n)方法来直接统计出出现频率最高的n个元素
    dic2.most_common(2)
    # 输出一个list ,其中的元素为（key,value）的键值对，类似[(6, 4), (3, 2)]这样"

    #对字典排序
    #以上一例子的dic作为排序对象
    dic = {0: 1, 2: 2, 4: 4, 6: 1, 7: 1, -6: 1}
    dic_after = sorted(dic.items(), key=lambda x:x[1])
    # 如果想按key来排序则sorted(dic.items(), key=lambda x:x[0])
    # dic_after为一个列表： [(0, 1), (6, 1), (7, 1), (-6, 1), (2, 2), (4, 4)]

    #正则匹配查找
    import re
    sentence = 'this is a test, not testing.'
    it = re.finditer('\\btest\\b', sentence)
    for match in it:
        print 'match position: ' + str(match.start()) +'-'+ str(match.end())

    #使用正则表达式分割文本
    import re
    s = 'ab,wer.wer,wer|wer||,wwer wer,wer3'
    re.split(r'[,|.]+', s)
    Out[6]: ['ab', 'wer', 'wer', 'wer', 'wer', 'wwer wer', 'wer3']"

    # 分割为所有单词组成的list, W匹配非字母数字及下划线
    import re
    result = re.split('W+', text)


    #使用正则表达式提取文本
    import re
    #用(?P<year>...)括住一个群，并命名为year
    m = re.search('output_(?P<year>d{4})', 'output_1986.txt')
    print(m.group('year') #输出1986


    #正则 调整文本格式
    import re
    s = '1991-02-28'
    re.sub(r'(d{4})-(d{2})-(d{2})', r'\\1/\\2/\\3')
    #Out[6]: '1991/02/28'

    #利用set是一个不同的对象的集合，删除列表中的重复元素。然且维持顺序
    from collections import OrderedDict
    x = [1, 8, 4, 5, 5, 5, 8, 1, 8]
    list(OrderedDict.fromkeys(x))"

    #筛选列表中的数据
    #列表解析
    from random import randint
    data = [randint(-10,10) for _ in range(10)]
    data_after=[x for x in data if x > 0]
    # or
    targetList = [v for v in targetList if not v.strip()=='']
    # or
    targetList = filter(lambda x: len(x)>0, targetList)

    #筛选字典中的数据，字典解析
    from random import randint
    d = {x: randint(60,100) for x in range(1,21)}
    d_after = {k:v for k,v in d.items() if v > 90}

    #使用命名元组为每个元素命名
    from collections import namedtuple
    Student = namedtuple('Student', ['name', 'age', 'sex'])
    s = Student('aaa',18,'male')
    s2= Student(name='bbb', age=12, sex='female')

    if s.name == 'aaa':
        pass
'''
