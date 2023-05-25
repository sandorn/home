# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================
Description  : string  |  dict  |  list  |  tupe  |  json
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-02-25 04:31:14
FilePath     : /CODE/xjLib/xt_String.py
Github       : https://github.com/sandorn/home
==============================================================
'''

import hashlib
import json
import random
import re
import string
from functools import reduce


def Ex_md5(data):
    """将string转化为MD5"""
    my_md5 = hashlib.md5()  # 获取一个MD5的加密算法对象
    my_md5.update(data.encode("utf-8", 'ignore'))  # 得到MD5消息摘要
    return my_md5.hexdigest()


def Ex_sha1(data):
    my_sha = hashlib.sha1()
    my_sha.update(data.encode("utf-8", 'ignore'))
    return my_sha.hexdigest()


def encrypt_str(data, algorithm='md5'):
    """ 用不同算法对字符串进行加密
    :param data: 待加密的字符串
    :param algorithm: 加密算法，可以是 md5 or sha1
    :return: 密文
    """
    if algorithm == 'md5':
        my_encrypt = hashlib.md5()
    elif algorithm == 'sha1':
        my_encrypt = hashlib.sha1()
    else:
        print('Unsupported algorithm.')
        return False

    my_encrypt.update(data.encode("utf-8", 'ignore'))  # 得到MD5消息摘要
    return my_encrypt.hexdigest()


def duplicate(iterable, keep=lambda x: x, key=lambda x: x, reverse=False):
    """
    增强去重功能，解决了重复元素可能覆盖的问题
    :param iterable: 需要去重的可迭代对象
    :param keep: 需要保留的元素，例如只保留某个字段
    :param key: 重复元素的判断字段
    :param reverse: 是否反向去重
    :return: 去重后的可迭代对象
    """
    # 创建一个字典存储重复的key和其他值
    duplicator = {}
    # 使用列表来存储有效的值
    result = []
    if reverse: iterable = reversed(iterable)
    # 遍历所有元素
    for i in iterable:
        # 调用keep函数获取该元素值
        keep_field = keep(i)
        # 调用key函数获取该元素key值
        key_words = key(i)
        # 如果key值在字典中不存在，则将元素填入字典，并将该元素添加到result列表中
        if key_words not in duplicator:
            duplicator[key_words] = keep_field
            result.append(keep_field)
    return list(reversed(result)) if reverse else result


def align(str1, distance=66, alignment='L'):
    # #居中打印为string类方法
    if alignment == 'C': return str1.center(distance, ' ')
    if not isinstance(str1, str): str1 = str(str1)
    # #print打印对齐
    length = len(str1.encode('utf-8', 'ignore'))
    slen = max(0, distance - length)

    if alignment == 'L':
        aligned_str = f"{str1}{' ' * slen}"
    elif alignment == 'R':
        aligned_str = f"{' ' * slen}{str1}"
    else:
        raise ValueError("Alignment must be one of 'left', 'center', or 'right'")
    return aligned_str


def remove_all_blank(value, keep_blank=True):
    """移除所有不可见字符,默认保留空格"""
    if keep_blank:
        return ''.join(ch for ch in value if ch.isprintable())
    else:
        return ''.join(filter(lambda c: c.isprintable() and not c.isspace(), value))


def Str_Replace(replacement, trims):
    """
    # @字符替换，不支持正则
    replacement:欲处理的字符串
    trims:list内包含tuple或list: [('a', 'A'), ('b', 'B'), ('c', 'C')]
    trims[0]:查找,trims[1]:替换
    # 第一种方法
    # for item in trims:
    #     replacement = replacement.replace(item[0], item[1])
    # return replacement
    # 第二种方法  # replacement 为初始值,最后传入,在lambda中最先接收
    """

    return reduce(lambda strtmp, item: strtmp.replace(item[0], item[1]), trims, replacement)


def Str_Clean(replacement: str, trims: list):
    """
    # @字符清除，不支持正则
    replacement:欲处理的字符串
    trims:list内包含tuple或list,例:["#", "?"]
    """
    # 第一种方法
    # for item in trims:
    #     replacement = replacement.replace(item, '')
    # return replacement

    # 第二种方法  # replacement 为初始值，最后传入，在lambda中最先接收
    return reduce(lambda strtmp, item: strtmp.replace(item, ""), trims, replacement)


def Re_Sub(replacement, trims=None):
    """
    @ re.sub正则替换,自写表达式
    replacement:欲处理的字符串
    trims:list内包含tuple或list
    trims[0]:查找字符串,trims[1]:替换字符串
    """
    if trims is None:
        # #格式化html string, 去掉多余的字符，类，script等。
        trims = [
            ("\n", ''),
            ("\t", ''),
            ("\r", ''),
            ("  ", ''),
            ("\u2018", "'"),
            ("\u2019", "'"),
            ("\ufeff", ''),
            ("\u2022", ":"),
            (r"<([a-z][a-z0-9]*) [^>]*>", r'<\g<1>>'),
            (r"<\s*script[^>]*>[^<]*<\s*/\s*script\s*>", ''),
            (r"</?a.*?>", ''),
        ]
    # lamda表达式,参数与输入值顺序相反
    return reduce(lambda str_tmp, item: re.sub(item[0], item[1], str_tmp), trims, replacement)


def Re_Compile_D(replacement: str, trimsD: dict):
    """
    ! re.compile正则替换,自写表达式,字典key受限,暂留
    replacement:欲处理的字符串
    trims_dict:dict
    用法=Re_Compile(replacement,{'A':'aaa','B':'bbb'})
    """
    pattern = re.compile('|'.join(map(re.escape, trimsD)))
    return pattern.sub(lambda m: trimsD[m.group(0)], replacement)


def Re_Compile(replacement: str, trimsL: list):
    """
    re.compile正则替换,自写表达式
    replacement:欲处理的字符串
    trims:list内包含tuple或list
    用法=Re_Compile(replacement,[('A', 'aaa'), ('B', 'bbb')])
    """

    # for trim in trimsL:
    #     pattern = re.compile(trim[0])
    #     replacement = pattern.sub(trim[1], replacement)
    # return replacement
    if not isinstance(replacement, str):
        raise TypeError(f"Expected str, got {type(replacement)}")
    if not isinstance(trimsL, list):
        raise TypeError(f"Expected list, got {type(trimsL)}")
    if not all(isinstance(t, (tuple, list)) for t in trimsL):
        raise TypeError(f"Expected list of lists or tuples, got {trimsL}")
    pattern = re.compile('|'.join(t[0] for t in trimsL))
    return pattern.sub(
        lambda x: next((t[1] for t in trimsL if t[0] == x.group()), x.group()),
        replacement,
    )


def str_split_limited_list(intext, mixnum=100, maxnum=280):
    return ([intext] if len(intext) < mixnum else re.findall(r'[\s\S]{' + str(mixnum) + ',' + str(maxnum) + '}。', intext))


def str2list(intext, maxlen=300):
    """
    将输入的字符串分割成若干个段落，每个段落的长度不超过 maxlen。
    """
    # 按照句号（。）将原始字符串分割为一组子串
    sentence_list = re.split('。', Str_Replace(intext, [['\r', '。'], ['\n', '。'], [' ', '']]))
    # 过滤掉空子串，并添加句号
    sentence_list = [f'{item}。' for item in sentence_list if item]

    paragraph_list = []
    current_paragraph = ''
    for sentence in sentence_list:
        # 如果当前段落长度不超过最大长度，则继续添加新的句子
        if len(current_paragraph + sentence) <= maxlen:
            current_paragraph += sentence
        else:
            # 否则，当前段落结束，添加到段落列表中
            paragraph_list.append(current_paragraph)
            current_paragraph = sentence

    # 处理最后一个段落
    if current_paragraph:
        paragraph_list.append(current_paragraph)

    return paragraph_list


def dict2qss(dict_tmp):
    '''字典形式的QSS转字符串
        弃用: qdarkstyle.utils.scss._dict_to_scss 替代
    '''
    # # 排序  print key, dict[key] for key in sorted(dict.keys())
    if isinstance(dict_tmp, dict):
        temp = json.dumps(dict_tmp)
        qss = Str_Replace(temp, [(',', ';'), ('"', ''), (': {', '{')])
    return qss.strip('{}')


def groupby(iterobj, key):
    """
    自实现groupby,return: 字典对象
    itertool的groupby不能合并不连续但是相同的组, 且返回值是iter
    """
    groups = {}
    for item in iterobj:
        groups.setdefault(key(item), []).append(item)
    return groups


def random_char(length=20):
    """实现指定长度的随机数"""
    res_str = []
    for _ in range(length):
        x = random.randint(1, 2)
        y = str(random.randint(0, 9)) if x == 1 else chr(random.randint(97, 122))
        res_str.append(y)
    return ''.join(res_str)


def class_add_dict(in_obj):
    '''把对象转换成字典'''
    # in_obj.__dict__ = {key: getattr(in_obj, key) for key in dir(in_obj) if not key.startswith('__') and not callable(getattr(in_obj, key))}
    in_obj.__dict__ = {key: value for key, value in vars(in_obj).items() if not key.startswith('__') and not callable(value)}
    return in_obj.__dict__


# 不可见字符及图形字符
Invisible_Chars = [
    '\xfe',
    '\u0000',
    '\u0001',
    '\U0001d173',
    '\U0001d174',
    '\U0001d175',
    '\U0001d176',
    '\U0001d3f3',
    '\U0001d3f4',
    '\U0001d3f5',
    '\U0001d3f6',
    '\U0001d3f7',
    '\U0001d3f8',
    '\U0001d400',
    '\U0001d407',
    '\U0001d40c',
    '\U0001d412',
    '\U0001d413',
    '\U0001d418',
    '\U0001d41c',
    '\U0001d430',
    '\U0001d464',
    '\U0001d46e',
    '\U0001d47e',
    '\U0001d486',
    '\U0001d4a2',
    '\U0001d4db',
    '\U0001d4f0',
    '\U0001d4f8',
    '\U0001d4fd',
    '\U0001d54b',
    '\U0001d552',
    '\U0001d559',
    '\U0001d5e5',
    '\U0001d5ee',
    '\U0001d63f',
    '\U0001d642',
    '\U0001d644',
    '\U0001d648',
    '\U0001d652',
    '\U0001d653',
    '\U0001d656',
    '\U0001d65e',
    '\U0001d663',
    '\U0001d7ce',
    '\U0001d7cf',
    '\U0001d7d0',
    '\U0001d7d1',
    '\U0001d7d2',
    '\U0001d7d3',
    '\U0001d7d4',
    '\U0001d7d9',
    '\U0001d7da',
    '\U0001d7ef',
    '\U0001d7f0',
    '\U0001d7f1',
    '\U0001d7f3',
    '\U0001d7f5',
    '\U0001f004',
    '\U0001f0cf',
    '\U0001f170',
    '\U0001f171',
    '\U0001f17c',
    '\U0001f192',
    '\U0001f193',
    '\U0001f194',
    '\U0001f195',
    '\U0001f198',
    '\U0001f199',
    '\U0001f19a',
    '\U0001f1e6',
    '\U0001f1e7',
    '\U0001f1e8',
    '\U0001f1ec',
    '\U0001f1ed',
    '\U0001f1ee',
    '\U0001f1ef',
    '\U0001f1f0',
    '\U0001f1f1',
    '\U0001f1f2',
    '\U0001f1f3',
    '\U0001f1f5',
    '\U0001f1f7',
    '\U0001f1f9',
    '\U0001f1fa',
    '\U0001f21a',
    '\U0001f22f',
    '\U0001f232',
    '\U0001f233',
    '\U0001f235',
    '\U0001f236',
    '\U0001f237',
    '\U0001f23a',
    '\U0001f250',
    '\U0001f251',
    '\U0001f302',
    '\U0001f303',
    '\U0001f304',
    '\U0001f305',
    '\U0001f307',
    '\U0001f308',
    '\U0001f30a',
    '\U0001f30b',
    '\U0001f30c',
    '\U0001f30d',
    '\U0001f30e',
    '\U0001f310',
    '\U0001f314',
    '\U0001f319',
    '\U0001f31a',
    '\U0001f31b',
    '\U0001f31c',
    '\U0001f31d',
    '\U0001f31e',
    '\U0001f31f',
    '\U0001f321',
    '\U0001f324',
    '\U0001f325',
    '\U0001f327',
    '\U0001f328',
    '\U0001f32b',
    '\U0001f32c',
    '\U0001f330',
    '\U0001f331',
    '\U0001f332',
    '\U0001f333',
    '\U0001f334',
    '\U0001f335',
    '\U0001f336',
    '\U0001f337',
    '\U0001f338',
    '\U0001f339',
    '\U0001f33a',
    '\U0001f33b',
    '\U0001f33c',
    '\U0001f33d',
    '\U0001f33e',
    '\U0001f33f',
    '\U0001f340',
    '\U0001f341',
    '\U0001f342',
    '\U0001f343',
    '\U0001f344',
    '\U0001f345',
    '\U0001f346',
    '\U0001f347',
    '\U0001f348',
    '\U0001f349',
    '\U0001f34a',
    '\U0001f34b',
    '\U0001f34d',
    '\U0001f34e',
    '\U0001f34f',
    '\U0001f350',
    '\U0001f351',
    '\U0001f352',
    '\U0001f353',
    '\U0001f354',
    '\U0001f357',
    '\U0001f358',
    '\U0001f359',
    '\U0001f35a',
    '\U0001f35b',
    '\U0001f35c',
    '\U0001f35d',
    '\U0001f35e',
    '\U0001f35f',
    '\U0001f360',
    '\U0001f361',
    '\U0001f362',
    '\U0001f363',
    '\U0001f364',
    '\U0001f365',
    '\U0001f366',
    '\U0001f367',
    '\U0001f369',
    '\U0001f36a',
    '\U0001f36b',
    '\U0001f36c',
    '\U0001f36d',
    '\U0001f36f',
    '\U0001f370',
    '\U0001f371',
    '\U0001f372',
    '\U0001f373',
    '\U0001f375',
    '\U0001f376',
    '\U0001f377',
    '\U0001f379',
    '\U0001f37a',
    '\U0001f37b',
    '\U0001f37c',
    '\U0001f37d',
    '\U0001f37e',
    '\U0001f37f',
    '\U0001f380',
    '\U0001f381',
    '\U0001f382',
    '\U0001f383',
    '\U0001f384',
    '\U0001f385',
    '\U0001f386',
    '\U0001f388',
    '\U0001f389',
    '\U0001f38a',
    '\U0001f38b',
    '\U0001f38e',
    '\U0001f38f',
    '\U0001f390',
    '\U0001f393',
    '\U0001f399',
    '\U0001f3a3',
    '\U0001f3a4',
    '\U0001f3a5',
    '\U0001f3a6',
    '\U0001f3a7',
    '\U0001f3a8',
    '\U0001f3a9',
    '\U0001f3ab',
    '\U0001f3ac',
    '\U0001f3ad',
    '\U0001f3ae',
    '\U0001f3b1',
    '\U0001f3b2',
    '\U0001f3b5',
    '\U0001f3b6',
    '\U0001f3b8',
    '\U0001f3b9',
    '\U0001f3ba',
    '\U0001f3bc',
    '\U0001f3bf',
    '\U0001f3c0',
    '\U0001f3c2',
    '\U0001f3c3',
    '\U0001f3c4',
    '\U0001f3c5',
    '\U0001f3c6',
    '\U0001f3ca',
    '\U0001f3cc',
    '\U0001f3cd',
    '\U0001f3d0',
    '\U0001f3d8',
    '\U0001f3d9',
    '\U0001f3db',
    '\U0001f3dc',
    '\U0001f3dd',
    '\U0001f3de',
    '\U0001f3df',
    '\U0001f3e0',
    '\U0001f3e1',
    '\U0001f3e5',
    '\U0001f3e6',
    '\U0001f3e7',
    '\U0001f3e8',
    '\U0001f3e9',
    '\U0001f3eb',
    '\U0001f3ee',
    '\U0001f3ef',
    '\U0001f3f0',
    '\U0001f3f4',
    '\U0001f3f7',
    '\U0001f3fd',
    '\U0001f3fe',
    '\U0001f400',
    '\U0001f402',
    '\U0001f405',
    '\U0001f407',
    '\U0001f408',
    '\U0001f409',
    '\U0001f40a',
    '\U0001f40d',
    '\U0001f40e',
    '\U0001f40f',
    '\U0001f411',
    '\U0001f412',
    '\U0001f413',
    '\U0001f414',
    '\U0001f415',
    '\U0001f416',
    '\U0001f417',
    '\U0001f419',
    '\U0001f41a',
    '\U0001f41b',
    '\U0001f41c',
    '\U0001f41d',
    '\U0001f41e',
    '\U0001f41f',
    '\U0001f420',
    '\U0001f421',
    '\U0001f422',
    '\U0001f423',
    '\U0001f425',
    '\U0001f426',
    '\U0001f427',
    '\U0001f428',
    '\U0001f429',
    '\U0001f42b',
    '\U0001f42c',
    '\U0001f42d',
    '\U0001f42e',
    '\U0001f42f',
    '\U0001f430',
    '\U0001f431',
    '\U0001f432',
    '\U0001f433',
    '\U0001f434',
    '\U0001f436',
    '\U0001f437',
    '\U0001f438',
    '\U0001f439',
    '\U0001f43a',
    '\U0001f43b',
    '\U0001f43c',
    '\U0001f43d',
    '\U0001f43e',
    '\U0001f440',
    '\U0001f441',
    '\U0001f442',
    '\U0001f443',
    '\U0001f444',
    '\U0001f445',
    '\U0001f446',
    '\U0001f447',
    '\U0001f448',
    '\U0001f449',
    '\U0001f44a',
    '\U0001f44b',
    '\U0001f44c',
    '\U0001f44d',
    '\U0001f44e',
    '\U0001f44f',
    '\U0001f450',
    '\U0001f451',
    '\U0001f452',
    '\U0001f455',
    '\U0001f456',
    '\U0001f457',
    '\U0001f459',
    '\U0001f45b',
    '\U0001f45c',
    '\U0001f460',
    '\U0001f463',
    '\U0001f464',
    '\U0001f465',
    '\U0001f466',
    '\U0001f467',
    '\U0001f468',
    '\U0001f46a',
    '\U0001f46b',
    '\U0001f46c',
    '\U0001f46d',
    '\U0001f46e',
    '\U0001f470',
    '\U0001f471',
    '\U0001f474',
    '\U0001f475',
    '\U0001f476',
    '\U0001f477',
    '\U0001f478',
    '\U0001f47b',
    '\U0001f47c',
    '\U0001f47d',
    '\U0001f47f',
    '\U0001f480',
    '\U0001f481',
    '\U0001f483',
    '\U0001f484',
    '\U0001f485',
    '\U0001f486',
    '\U0001f48a',
    '\U0001f48b',
    '\U0001f48c',
    '\U0001f48d',
    '\U0001f48e',
    '\U0001f48f',
    '\U0001f490',
    '\U0001f491',
    '\U0001f492',
    '\U0001f493',
    '\U0001f494',
    '\U0001f495',
    '\U0001f496',
    '\U0001f497',
    '\U0001f498',
    '\U0001f499',
    '\U0001f49a',
    '\U0001f49b',
    '\U0001f49c',
    '\U0001f49d',
    '\U0001f49e',
    '\U0001f49f',
    '\U0001f4a0',
    '\U0001f4a1',
    '\U0001f4a2',
    '\U0001f4a3',
    '\U0001f4a4',
    '\U0001f4a5',
    '\U0001f4a6',
    '\U0001f4a7',
    '\U0001f4a8',
    '\U0001f4a9',
    '\U0001f4aa',
    '\U0001f4ab',
    '\U0001f4ad',
    '\U0001f4af',
    '\U0001f4b0',
    '\U0001f4b2',
    '\U0001f4b3',
    '\U0001f4b4',
    '\U0001f4b5',
    '\U0001f4b6',
    '\U0001f4b7',
    '\U0001f4b8',
    '\U0001f4bb',
    '\U0001f4bc',
    '\U0001f4bd',
    '\U0001f4bf',
    '\U0001f4c0',
    '\U0001f4c4',
    '\U0001f4c6',
    '\U0001f4c8',
    '\U0001f4c9',
    '\U0001f4cb',
    '\U0001f4cc',
    '\U0001f4cd',
    '\U0001f4ce',
    '\U0001f4d2',
    '\U0001f4d3',
    '\U0001f4d5',
    '\U0001f4d6',
    '\U0001f4d9',
    '\U0001f4da',
    '\U0001f4dc',
    '\U0001f4dd',
    '\U0001f4de',
    '\U0001f4e1',
    '\U0001f4e2',
    '\U0001f4e3',
    '\U0001f4e6',
    '\U0001f4e8',
    '\U0001f4e9',
    '\U0001f4ec',
    '\U0001f4ed',
    '\U0001f4ee',
    '\U0001f4f0',
    '\U0001f4f1',
    '\U0001f4f2',
    '\U0001f4f7',
    '\U0001f4f8',
    '\U0001f4fa',
    '\U0001f4fb',
    '\U0001f4fd',
    '\U0001f501',
    '\U0001f505',
    '\U0001f506',
    '\U0001f508',
    '\U0001f50a',
    '\U0001f50d',
    '\U0001f510',
    '\U0001f511',
    '\U0001f512',
    '\U0001f513',
    '\U0001f514',
    '\U0001f516',
    '\U0001f517',
    '\U0001f519',
    '\U0001f51a',
    '\U0001f51b',
    '\U0001f51c',
    '\U0001f51d',
    '\U0001f51f',
    '\U0001f525',
    '\U0001f528',
    '\U0001f52a',
    '\U0001f52b',
    '\U0001f52c',
    '\U0001f52e',
    '\U0001f531',
    '\U0001f534',
    '\U0001f535',
    '\U0001f536',
    '\U0001f538',
    '\U0001f539',
    '\U0001f53a',
    '\U0001f53b',
    '\U0001f54a',
    '\U0001f550',
    '\U0001f554',
    '\U0001f557',
    '\U0001f558',
    '\U0001f559',
    '\U0001f55b',
    '\U0001f560',
    '\U0001f56f',
    '\U0001f573',
    '\U0001f578',
    '\U0001f57a',
    '\U0001f58d',
    '\U0001f590',
    '\U0001f595',
    '\U0001f596',
    '\U0001f5a4',
    '\U0001f5bc',
    '\U0001f5d1',
    '\U0001f5dd',
    '\U0001f5e1',
    '\U0001f5e3',
    '\U0001f5ef',
    '\U0001f5fb',
    '\U0001f5fe',
    '\U0001f600',
    '\U0001f601',
    '\U0001f602',
    '\U0001f603',
    '\U0001f604',
    '\U0001f605',
    '\U0001f606',
    '\U0001f607',
    '\U0001f608',
    '\U0001f609',
    '\U0001f60a',
    '\U0001f60b',
    '\U0001f60c',
    '\U0001f60d',
    '\U0001f60e',
    '\U0001f60f',
    '\U0001f610',
    '\U0001f611',
    '\U0001f612',
    '\U0001f613',
    '\U0001f614',
    '\U0001f615',
    '\U0001f616',
    '\U0001f618',
    '\U0001f619',
    '\U0001f61a',
    '\U0001f61c',
    '\U0001f61d',
    '\U0001f61e',
    '\U0001f61f',
    '\U0001f620',
    '\U0001f621',
    '\U0001f622',
    '\U0001f623',
    '\U0001f624',
    '\U0001f625',
    '\U0001f627',
    '\U0001f628',
    '\U0001f629',
    '\U0001f62a',
    '\U0001f62b',
    '\U0001f62c',
    '\U0001f62d',
    '\U0001f62e',
    '\U0001f62f',
    '\U0001f630',
    '\U0001f631',
    '\U0001f632',
    '\U0001f633',
    '\U0001f634',
    '\U0001f635',
    '\U0001f636',
    '\U0001f637',
    '\U0001f638',
    '\U0001f639',
    '\U0001f63a',
    '\U0001f63b',
    '\U0001f63e',
    '\U0001f63f',
    '\U0001f640',
    '\U0001f641',
    '\U0001f642',
    '\U0001f643',
    '\U0001f644',
    '\U0001f645',
    '\U0001f646',
    '\U0001f647',
    '\U0001f648',
    '\U0001f649',
    '\U0001f64a',
    '\U0001f64b',
    '\U0001f64c',
    '\U0001f64d',
    '\U0001f64e',
    '\U0001f64f',
    '\U0001f680',
    '\U0001f684',
    '\U0001f685',
    '\U0001f686',
    '\U0001f689',
    '\U0001f68a',
    '\U0001f68b',
    '\U0001f68c',
    '\U0001f68e',
    '\U0001f692',
    '\U0001f693',
    '\U0001f694',
    '\U0001f695',
    '\U0001f697',
    '\U0001f698',
    '\U0001f699',
    '\U0001f69a',
    '\U0001f69c',
    '\U0001f69d',
    '\U0001f6a2',
    '\U0001f6a3',
    '\U0001f6a4',
    '\U0001f6ab',
    '\U0001f6ac',
    '\U0001f6ae',
    '\U0001f6b2',
    '\U0001f6b6',
    '\U0001f6b8',
    '\U0001f6b9',
    '\U0001f6ba',
    '\U0001f6bd',
    '\U0001f6be',
    '\U0001f6bf',
    '\U0001f6c0',
    '\U0001f6c1',
    '\U0001f6cb',
    '\U0001f6cd',
    '\U0001f6cf',
    '\U0001f6d2',
    '\U0001f6d7',
    '\U0001f6eb',
    '\U0001f6f0',
    '\U0001f6f3',
    '\U0001f6f4',
    '\U0001f6f5',
    '\U0001f6f8',
    '\U0001f6f9',
    '\U0001f6fa',
    '\U0001f7e2',
    '\U0001f90c',
    '\U0001f90d',
    '\U0001f90f',
    '\U0001f910',
    '\U0001f911',
    '\U0001f912',
    '\U0001f913',
    '\U0001f914',
    '\U0001f915',
    '\U0001f916',
    '\U0001f917',
    '\U0001f918',
    '\U0001f919',
    '\U0001f91a',
    '\U0001f91c',
    '\U0001f91d',
    '\U0001f91e',
    '\U0001f91f',
    '\U0001f921',
    '\U0001f922',
    '\U0001f923',
    '\U0001f924',
    '\U0001f925',
    '\U0001f926',
    '\U0001f927',
    '\U0001f928',
    '\U0001f929',
    '\U0001f92a',
    '\U0001f92b',
    '\U0001f92c',
    '\U0001f92d',
    '\U0001f92e',
    '\U0001f92f',
    '\U0001f930',
    '\U0001f931',
    '\U0001f932',
    '\U0001f933',
    '\U0001f934',
    '\U0001f935',
    '\U0001f937',
    '\U0001f93a',
    '\U0001f940',
    '\U0001f941',
    '\U0001f942',
    '\U0001f943',
    '\U0001f944',
    '\U0001f947',
    '\U0001f94a',
    '\U0001f950',
    '\U0001f951',
    '\U0001f954',
    '\U0001f955',
    '\U0001f957',
    '\U0001f958',
    '\U0001f959',
    '\U0001f95a',
    '\U0001f95b',
    '\U0001f95c',
    '\U0001f95d',
    '\U0001f95e',
    '\U0001f95f',
    '\U0001f961',
    '\U0001f962',
    '\U0001f963',
    '\U0001f964',
    '\U0001f965',
    '\U0001f96a',
    '\U0001f96b',
    '\U0001f96c',
    '\U0001f96d',
    '\U0001f96e',
    '\U0001f970',
    '\U0001f971',
    '\U0001f972',
    '\U0001f973',
    '\U0001f974',
    '\U0001f975',
    '\U0001f976',
    '\U0001f978',
    '\U0001f97a',
    '\U0001f980',
    '\U0001f981',
    '\U0001f984',
    '\U0001f985',
    '\U0001f986',
    '\U0001f988',
    '\U0001f98a',
    '\U0001f98b',
    '\U0001f98c',
    '\U0001f98d',
    '\U0001f990',
    '\U0001f996',
    '\U0001f999',
    '\U0001f99a',
    '\U0001f9a2',
    '\U0001f9b0',
    '\U0001f9b1',
    '\U0001f9b2',
    '\U0001f9b3',
    '\U0001f9b4',
    '\U0001f9b5',
    '\U0001f9b6',
    '\U0001f9b7',
    '\U0001f9c0',
    '\U0001f9c4',
    '\U0001f9c5',
    '\U0001f9c7',
    '\U0001f9ca',
    '\U0001f9cd',
    '\U0001f9ce',
    '\U0001f9d0',
    '\U0001f9d2',
    '\U0001f9d3',
    '\U0001f9d4',
    '\U0001f9d5',
    '\U0001f9d6',
    '\U0001f9d7',
    '\U0001f9da',
    '\U0001f9dc',
    '\U0001f9e0',
    '\U0001f9e1',
    '\U0001f9e2',
    '\U0001f9e7',
    '\U0001f9e8',
    '\U0001f9ea',
    '\U0001f9ec',
    '\U0001f9ee',
    '\U0001f9f1',
    '\U0001f9f6',
    '\U0001f9f8',
    '\U0001f9f9',
    '\U0001f9fa',
    '\U0001f9fb',
    '\U0001f9ff',
    '\U0001fa70',
    '\U0001fa78',
    '\U0001fa80',
    '\U0001fa82',
    '\U0001fa84',
    '\U0001fa86',
    '\U0001fa90',
    '\U0001fa96',
    '\U0001fa9e',
    '\U0001faa1',
    '\U0001fab6',
    '\U0001fad3',
    '\U0001fad6',
    '\u0002',
    '\U000201a4',
    '\u0003',
    '\u0004',
    '\u0005',
    '\u0006',
    '\u0007',
    '\u0008',
    '\u0009',
    '\u000a',
    '\u000b',
    '\u000c',
    '\u000d',
    '\u000e',
    '\u000f',
    '\U000fe4ed',
    '\u0010',
    '\U001003ae',
    '\u0011',
    '\u0012',
    '\u0013',
    '\u0014',
    '\u0015',
    '\u0016',
    '\u0017',
    '\u0018',
    '\u0019',
    '\u001a',
    '\u001b',
    '\u001c',
    '\u001d',
    '\u001e',
    '\u001f',
    '\u007f',
    '\u0080',
    '\u0081',
    '\u0082',
    '\u0083',
    '\u0084',
    '\u0085',
    '\u0086',
    '\u0087',
    '\u0088',
    '\u0089',
    '\u008a',
    '\u008b',
    '\u008c',
    '\u008d',
    '\u008e',
    '\u008f',
    '\u0090',
    '\u0091',
    '\u0092',
    '\u0093',
    '\u0094',
    '\u0095',
    '\u0096',
    '\u0097',
    '\u0098',
    '\u0099',
    '\u009a',
    '\u009b',
    '\u009c',
    '\u009d',
    '\u009e',
    '\u009f',
    '\u00a0',
    '\u00ad',
    '\u010e',
    '\u0125',
    '\u014c',
    '\u014e',
    '\u0150',
    '\u0160',
    '\u016c',
    '\u016e',
    '\u0171',
    '\u0178',
    '\u0295',
    '\u029a',
    '\u029c',
    '\u02ae',
    '\u02b0',
    '\u02d8',
    '\u02e1',
    '\u02f6',
    '\u0301',
    '\u0308',
    '\u030c',
    '\u0329',
    '\u032e',
    '\u032f',
    '\u0348',
    '\u034f',
    '\u035e',
    '\u035f',
    '\u0361',
    '\u0364',
    '\u03af',
    '\u03ea',
    '\u0455',
    '\u04e7',
    '\u04f0',
    '\u053e',
    '\u0648',
    '\u0665',
    '\u0669',
    '\u06e9',
    '\u06ec',
    '\u06f0',
    '\u06f6',
    '\u0847',
    '\u0952',
    '\u0967',
    '\u0ae2',
    '\u0b67',
    '\u0b87',
    '\u0b90',
    '\u0ca0',
    '\u0ca1',
    '\u0ca5',
    '\u0dc6',
    '\u0e01',
    '\u0e05',
    '\u0e07',
    '\u0e17',
    '\u0e1f',
    '\u0e21',
    '\u0e23',
    '\u0e2d',
    '\u0e34',
    '\u0e3f',
    '\u0e40',
    '\u0e47',
    '\u0e51',
    '\u0eb4',
    '\u0f0a',
    '\u0f0b',
    '\u0f3e',
    '\u0f40',
    '\u0f58',
    '\u0f72',
    '\u0f80',
    '\u0fb3',
    '\u10e6',
    '\u1111',
    '\u11ba',
    '\u1564',
    '\u1566',
    '\u17b5',
    '\u180e',
    '\u196c',
    '\u1b44',
    '\u1ba8',
    '\u1d17',
    '\u1d2c',
    '\u1d33',
    '\u1d34',
    '\u1d35',
    '\u1d39',
    '\u1d3e',
    '\u1d40',
    '\u1d43',
    '\u1d48',
    '\u1d55',
    '\u1d57',
    '\u1dc5',
    '\u1f62',
    '\u2000',
    '\u2001',
    '\u2002',
    '\u2003',
    '\u2004',
    '\u2005',
    '\u2006',
    '\u2007',
    '\u2008',
    '\u2009',
    '\u200a',
    '\u200b',
    '\u200c',
    '\u200d',
    '\u200e',
    '\u200f',
    '\u2022',
    '\u2023',
    '\u2027',
    '\u2028',
    '\u2029',
    '\u202a',
    '\u202b',
    '\u202c',
    '\u202d',
    '\u202e',
    '\u202f',
    '\u2039',
    '\u203a',
    '\u203c',
    '\u203e',
    '\u203f',
    '\u2049',
    '\u2060',
    '\u2061',
    '\u2062',
    '\u2063',
    '\u2064',
    '\u2065',
    '\u2066',
    '\u2067',
    '\u2068',
    '\u2069',
    '\u206a',
    '\u206b',
    '\u206c',
    '\u206d',
    '\u206e',
    '\u206f',
    '\u207d',
    '\u207e',
    '\u208d',
    '\u20ab',
    '\u20ac',
    '\u20db',
    '\u20dd',
    '\u20de',
    '\u20e3',
    '\u210d',
    '\u2122',
    '\u2134',
    '\u2194',
    '\u21d2',
    '\u21e8',
    '\u2200',
    '\u2202',
    '\u2207',
    '\u22b1',
    '\u22b9',
    '\u22c8',
    '\u22cc',
    '\u22db',
    '\u22ef',
    '\u231a',
    '\u231b',
    '\u2323',
    '\u2328',
    '\u23e9',
    '\u23eb',
    '\u23f0',
    '\u23f1',
    '\u2449',
    '\u246f',
    '\u2470',
    '\u24de',
    '\u24e5',
    '\u24ff',
    '\u2579',
    '\u2580',
    '\u2590',
    '\u2591',
    '\u2592',
    '\u25a3',
    '\u25a5',
    '\u25a6',
    '\u25a7',
    '\u25aa',
    '\u25ab',
    '\u25ac',
    '\u25b6',
    '\u25b7',
    '\u25b8',
    '\u25ba',
    '\u25bf',
    '\u25c2',
    '\u25c3',
    '\u25c4',
    '\u25c8',
    '\u25ca',
    '\u25cd',
    '\u25d1',
    '\u25d2',
    '\u25d5',
    '\u25d8',
    '\u25d9',
    '\u25e0',
    '\u25e1',
    '\u25e6',
    '\u25fe',
    '\u2600',
    '\u2601',
    '\u2602',
    '\u2603',
    '\u2604',
    '\u260c',
    '\u260d',
    '\u260e',
    '\u260f',
    '\u2611',
    '\u2614',
    '\u2615',
    '\u2618',
    '\u261c',
    '\u261d',
    '\u261e',
    '\u261f',
    '\u2620',
    '\u262a',
    '\u262f',
    '\u2639',
    '\u263a',
    '\u263b',
    '\u263c',
    '\u2648',
    '\u2650',
    '\u2651',
    '\u2652',
    '\u2653',
    '\u2659',
    '\u265b',
    '\u2660',
    '\u2661',
    '\u2662',
    '\u2663',
    '\u2665',
    '\u2666',
    '\u2668',
    '\u266a',
    '\u266b',
    '\u266c',
    '\u266f',
    '\u267e',
    '\u2695',
    '\u2696',
    '\u2699',
    '\u269b',
    '\u269c',
    '\u26a0',
    '\u26a1',
    '\u26aa',
    '\u26ab',
    '\u26b0',
    '\u26bd',
    '\u26c4',
    '\u26e9',
    '\u26ea',
    '\u26f0',
    '\u26f1',
    '\u26f8',
    '\u26fd',
    '\u2702',
    '\u2705',
    '\u2708',
    '\u2709',
    '\u270a',
    '\u270b',
    '\u270c',
    '\u270d',
    '\u270f',
    '\u2710',
    '\u2712',
    '\u2713',
    '\u2714',
    '\u2716',
    '\u2718',
    '\u2721',
    '\u2726',
    '\u2727',
    '\u2728',
    '\u272a',
    '\u2730',
    '\u2732',
    '\u2740',
    '\u2744',
    '\u2749',
    '\u274c',
    '\u2753',
    '\u2754',
    '\u2755',
    '\u2757',
    '\u275c',
    '\u275d',
    '\u2763',
    '\u2764',
    '\u2765',
    '\u2776',
    '\u2777',
    '\u2778',
    '\u2779',
    '\u277a',
    '\u277b',
    '\u277c',
    '\u277d',
    '\u277e',
    '\u278a',
    '\u278b',
    '\u2795',
    '\u2796',
    '\u2797',
    '\u279d',
    '\u27a1',
    '\u27a4',
    '\u27a8',
    '\u27ad',
    '\u27b0',
    '\u27b9',
    '\u27bf',
    '\u2af7',
    '\u2af8',
    '\u2b05',
    '\u2b06',
    '\u2b07',
    '\u2b1b',
    '\u2b1c',
    '\u2b50',
    '\u2b55',
    '\u2c19',
    '\u2f12',
    '\u2f25',
    '\u2f45',
    '\u2fa5',
    '\u3000',
    '\u301c',
    '\u3030',
    '\u30fb',
    '\u3142',
    '\u314b',
    '\u3160',
    '\u3164',
    '\u317f',
    '\u325b',
    '\u3268',
    '\u3297',
    '\u3299',
    '\u3405',
    '\u36ac',
    '\u36c7',
    '\u36f0',
    '\u375a',
    '\u379e',
    '\u3873',
    '\u40fc',
    '\u41b3',
    '\u45a1',
    '\u4d8a',
    '\u4d97',
    '\u4dae',
    '\u9fba',
    '\ua0c5',
    '\ua34f',
    '\ua426',
    '\ua4a6',
    '\ua9bf',
    '\ua9c1',
    '\uac1c',
    '\uac74',
    '\uadfc',
    '\uae30',
    '\ub098',
    '\ub208',
    '\ub85c',
    '\ube44',
    '\uc131',
    '\uc18c',
    '\uc5ed',
    '\uc601',
    '\uc608',
    '\uc694',
    '\uc7ac',
    '\ucc28',
    '\ucc98',
    '\uccab',
    '\uce74',
    '\ud2b8',
    '\ud32c',
    '\ud3ec',
    '\ue004',
    '\ue021',
    '\ue022',
    '\ue031',
    '\ue0ed',
    '\ue10e',
    '\ue112',
    '\ue115',
    '\ue12e',
    '\ue14c',
    '\ue312',
    '\ue32e',
    '\ue404',
    '\ue412',
    '\ue41d',
    '\ue4e1',
    '\ue536',
    '\ue627',
    '\ue768',
    '\ue804',
    '\uf0d8',
    '\ufe00',
    '\ufe01',
    '\ufe02',
    '\ufe03',
    '\ufe04',
    '\ufe05',
    '\ufe06',
    '\ufe07',
    '\ufe08',
    '\ufe09',
    '\ufe0a',
    '\ufe0b',
    '\ufe0c',
    '\ufe0d',
    '\ufe0e',
    '\ufe0f',
    '\ufe20',
    '\ufecc',
    '\ufeff',
    '\uff61',
    '\uff62',
    '\uff63',
    '\uff64',
    '\uff65',
    '\uff6a',
    '\uff89',
    '\uff9f',
    '\uffa0',
    '\uffe8',
    '\ufff9',
    '\ufffa',
    '\ufffb',
    '\ufffc',
    '\ufffd',
    '\uffff',
    '\x00',
    '\x01',
    '\x02',
    '\x03',
    '\x04',
    '\x05',
    '\x06',
    '\x07',
    '\x08',
    '\x0b',
    '\x0c',
    '\x0e',
    '\x0f',
    '\xa0',
    '\xa1',
    '\xa3',
    '\xa5',
    '\xa6',
    '\xa9',
    '\xac',
    '\xad',
    '\xae',
    '\xaf',
    '\xb2',
    '\xb3',
    '\xb4',
    '\xb8',
    '\xba',
    '\xbd',
    '\xbe',
    '\xbf',
    '\xc0',
    '\xc4',
    '\xd0',
    '\xd2',
    '\xd3',
    '\xd4',
    '\xd5',
    '\xd6',
    '\xd8',
    '\xdd',
    '\xde',
    '\xe2',
    '\xee',
    '\xf1',
    '\xfb',
    # '\u033',
]

if __name__ == '__main__':
    ttt = '''
    立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年
——广大青年认真学习贯彻党的二十大精神
2022年10月27日08:26   来源：人民网－人民日报

“青年强，则国家强。当代中国青年生逢其时，施展才干的舞台无比广阔，实现梦想的前景无比光明。”习近平总书记在党的二十大报告中勉励广大青年坚定不移听党话、跟党走，怀抱梦想又脚踏实地，敢想敢为又善作善成，立志做有理想、敢担当、能吃苦、肯奋斗的新时代好青年，让青春在全面建设社会主义现代化国家的火热实践中绽放绚丽之花。

未来属于青年，希望寄予青年。认真学习贯彻党的二十大精神，广大青年纷纷表示，一定牢记习近平总书记嘱托，坚定理想信念，筑牢精神之基，厚植爱国情怀，矢志不渝跟党走，以实现中华民族伟大复兴为己任，增强做中国人的志气、骨气、底气，不负时代，不负韶华，不负党和人民的殷切期望。

在海南省陵水海域，全球首座10万吨级深水半潜式生产储油平台“深海一号”钻机轰鸣，作业忙碌。甲板上，气田开发生产团队工艺工程师刘昱亮正和同事们一起调试设备。过去5年来，这支青年人占比七成以上的团队先后攻克一系列行业技术难题。展望未来，刘昱亮和团队成员充满信心：“我们将围绕党的二十大报告提出的‘加大油气资源勘探开发和增储上产力度’部署要求，为保障国家能源安全作出新的贡献。”

这几天，南京大学现代工程与应用科学学院教授李喆，正带领课题组探讨针对动脉粥样硬化疾病的新型纳米治疗方法。李喆在国外获得博士学位后，于2015年回国。今年5月，习近平总书记给南京大学的留学归国青年学者回信，勉励他们“在坚持立德树人、推动科技自立自强上再创佳绩，在坚定文化自信、讲好中国故事上争做表率”。李喆深感重任在肩，调整课题方向专攻生物医学应用研究。铭记习近平总书记殷切期望，李喆表示：“生逢伟大时代，肩负光荣使命，我将努力为国家培养更多人才，在科学研究中不断突破创新。”

西藏自治区林芝市巴宜区委组织部干部黄海芬，最近正和同事深入基层收集记录红色故事，为巴宜区筹办红色研学主题教育展馆准备素材。5年前，广东姑娘黄海芬大学毕业后放弃舒适的工作，怀揣梦想奔赴雪域高原。学习领会党的二十大精神，黄海芬更加坚定了自己的选择：“西藏是我施展才干的广阔舞台，我将铸牢中华民族共同体意识，为民族团结进步事业多作贡献。”

深秋的可可西里，昆仑负雪，大地苍茫。今年33岁的三江源国家公园长江源园区可可西里管理处索南达杰保护站副站长龙周才加，已在这片土地上守护藏羚羊10多年。“如今在可可西里保护站，80后、90后青年已成为骨干和主力。在党的二十大精神指引下，我们将携手奋斗，守护好‘中华水塔’，保护好青藏高原生态环境。”

在长沙机场改扩建工程T3航站楼项目现场，对着施工样板，中国建筑五局总承包公司项目质量总监邹彬为工友们讲解如何确保工序质量标准。这位95后党员曾获第四十三届世界技能大赛砌筑项目优胜奖。“这些年，培育新型产业工人方面出台了很多好政策，给了青年技能人才越来越大的施展平台。”学习领会党的二十大精神，邹彬感受颇深，“一定珍惜这个伟大时代，做新时代的奋斗者，带领更多青年走技能成才、技能报国之路。”

哈尔滨电气集团有限公司首席技师、高技能专家孙柏慧从一名学徒工干起，迄今已带领团队完成一系列技术革新，主导完成科研、攻关、发明专利等40余项。“党的二十大报告充分回应包括青年在内的广大干部群众对美好生活的向往，为我们青年建功立业提供了广阔舞台。”今年32岁的孙柏慧说，作为一名产业技术工人，将潜心钻研业务、练就过硬本领，努力在新征程中书写精彩人生。

这几天，西安交通大学各班陆续举办学习党的二十大精神主题班会。上世纪50年代，一批交大人响应党的号召从上海迁至西安，用高昂情怀和满腔热血铸就了“胸怀大局、无私奉献、弘扬传统、艰苦创业”的“西迁精神”。如今，参观交大西迁博物馆、学习西迁精神，成为西安交大学子的必修课。“学习贯彻党的二十大精神，我们要把青年工作作为战略性工作来抓，用习近平新时代中国特色社会主义思想武装青年，用党的初心使命感召青年，做青年朋友的知心人、青年工作的热心人、青年群众的引路人。”从事班主任工作12年的西安交大机械工程学院青年教授雷亚国表示，将进一步激励交大学子当好“西迁精神”新传人，到祖国建设最需要的地方建功立业。
    '''

    # for c in str2list(ttt):
    #     print(len(c), c)
    # print('end')
    import unittest

    class TestStrReplace(unittest.TestCase):

        def setUp(self):
            self.replacement = 'aaabbbccc'
            self.trims = [('a', 'A'), ('b', 'B'), ('c', 'C')]

        def test_str_replace(self):
            self.assertEqual(Str_Replace(self.replacement, self.trims), 'AAA BBB CCC')

    # unittest.main()

    def test_str_clean():
        test_str = "###hello?world"
        result = Str_Clean(test_str, ["#", "?"])

        assert result == "hello|world", result

    # test_str_clean()

    def test_Re_Sub():
        replacement = "This\n is \u2018a\u2019 test\ufeff string"
        trims = None
        expected_result = "This is 'a' test string!"
        result = Re_Sub(replacement, trims)
        assert result == expected_result, result

    # test_Re_Sub()

    def test_Re_Compile_D():
        replacement = 'hello A and B'
        trims_dict = {'A': 'aaa', 'B': 'bbb'}
        result = Re_Compile_D(replacement, trims_dict)
        assert result == 'hello aaa and bbb.', result

        # replacement = '@A@'
        # trims_dict = {'A': 'aaa'}
        # result = Re_Compile(replacement, trims_dict)
        # assert result == '@aaa.@', result

    # test_Re_Compile_D()

    def test_Re_Compile():
        replacement = 'hello A and B'
        trims_list = [('A', 'aaa'), ('B', 'bbb')]
        result = Re_Compile(replacement, trims_list)
        print(result)

    # test_Re_Compile()

    print(remove_all_blank(
        "Powe, on；the 2333, 。哈哈 ！！\U0001f914看看可以吗？一行代码就可以了！^_^",
        keep_blank=False,
    ))
    for i in Invisible_Chars:
        ...
        # print(i, i.isprintable())
