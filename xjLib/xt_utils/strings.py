# !/us/bin/env python
"""
==============================================================
Description  : string  |  dict  |  list  |  tupe  |  json
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-02-25 04:31:14
FilePath     : /CODE/xjlib/xt_utils/string.py
Github       : https://github.com/sandorn/home
==============================================================
https://zhuanlan.zhihu.com/p/696103020
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import random
import re
import string
from collections.abc import Callable, Iterable, Sequence
from functools import reduce
from re import Pattern
from typing import Any, Literal

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def is_valid_id(id_number: str | int) -> bool:
    """
    验证中国身份证号码是否符合格式要求和校验规则

    仅支持18位新版身份证验证。
    18位身份证规则：6位地区码 + 8位出生日期(YYYYMMDD) + 3位顺序码 + 1位校验码

    Args:
        id_number: 身份证号码，可以是字符串或整数

    Returns:
        bool: 验证结果，True表示有效，False表示无效

    Raises:
        TypeError: 如果输入不是字符串或整数类型
    """
    # 确保输入是字符串类型
    if isinstance(id_number, int):
        id_number = str(id_number)
    elif not isinstance(id_number, str):
        raise TypeError('身份证号码必须是字符串或整数类型')

    # 移除可能存在的空格
    id_number = id_number.strip()

    # 验证18位身份证
    if len(id_number) == 18:
        # 18位身份证格式：前17位为数字，最后一位为数字或X/x
        pattern = r'^\d{17}(\d|X|x)$'
        if not re.match(pattern, id_number):
            return False

        # 计算校验码
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

        try:
            # 计算前17位与对应权重乘积的和
            sum_weights = sum(int(id_number[i]) * weights[i] for i in range(17))
            # 计算校验码
            calculated_check_code = check_codes[sum_weights % 11]
            # 检查校验码是否匹配（不区分大小写）
            return id_number[-1].upper() == calculated_check_code
        except (ValueError, IndexError):
            return False

    # 身份证长度不正确
    else:
        return False


def str_to_md5(data: str | bytes) -> str:
    """将输入字符串或字节数据转换为MD5哈希值。

    Args:
        data: 待处理的字符串或字节数据

    Returns:
        str: MD5哈希值（16进制字符串）

    Examples:
        >>> str_to_md5('hello')
        '5d41402abc4b2a76b9719d911017c592'
    """
    return encrypt_str(data, 'md5')


def str_to_sha1(data: str | bytes) -> str:
    """将输入字符串或字节数据转换为SHA1哈希值。

    Args:
        data: 待处理的字符串或字节数据

    Returns:
        str: SHA1哈希值（16进制字符串）

    Examples:
        >>> str_to_sha1('hello')
        'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d'
    """
    return encrypt_str(data, 'sha1')


def encrypt_str(data: str | bytes, algorithm: str = 'md5', key: str | None = None) -> str | bool:
    """对字符串进行加密或哈希处理。

    支持哈希算法(md5, sha1, sha256, sha512)和加密算法(aes-256-cbc)
    哈希算法不需要密钥，加密算法(aes)需要提供16/24/32字节的密钥

    Args:
        data: 待处理的字符串或字节数据
        algorithm: 加密/哈希算法，可选值: md5, sha1, sha256, sha512, aes-256-cbc
        key: 加密密钥，AES算法必填，长度应为16/24/32字节

    Returns:
        str: 处理后的结果
        bool: 发生错误时返回False

    Examples:
        >>> encrypt_str('hello', 'md5')
        '5d41402abc4b2a76b9719d911017c592'
        >>> encrypt_str('hello', 'sha256')
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    # 确保输入是字节类型
    if isinstance(data, str):
        data = data.encode('utf-8', 'ignore')

    # 哈希算法处理
    hash_algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }

    if algorithm in hash_algorithms:
        hash_obj = hash_algorithms[algorithm]()
        hash_obj.update(data)
        return hash_obj.hexdigest()

    # AES加密算法处理
    if algorithm == 'aes-256-cbc':
        if not key or len(key) not in [16, 24, 32]:
            print('AES密钥必须为16/24/32字节长度')
            return False

        try:
            # 生成随机IV
            iv = os.urandom(16)  # 随机生成16字节IV
            cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()

            # 数据填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()

            # 加密并编码(IV+密文)
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return base64.b64encode(iv + ciphertext).decode()
        except Exception as e:
            print(f'AES加密失败: {e!s}')
            return False

    else:
        print(f'不支持的算法: {algorithm}')
        return False


def decrypt_str(encrypted_data: str, algorithm: str = 'aes-256-cbc', key: str | None = None) -> str | bool:
    """对加密字符串进行解密。

    目前仅支持AES加密算法的解密

    Args:
        encrypted_data: 待解密的字符串
        algorithm: 解密算法，目前仅支持 aes-256-cbc
        key: 解密密钥，必须与加密时使用的密钥相同

    Returns:
        str: 解密后的原始字符串
        bool: 发生错误时返回False

    Examples:
        >>> # 假设已加密的数据为encrypted_text
        >>> # decrypt_str(encrypted_text, "aes-256-cbc", "mysecretkey123456")
    """
    if algorithm != 'aes-256-cbc':
        print(f'不支持的解密算法: {algorithm}')
        return False

    if not key or len(key) not in [16, 24, 32]:
        print('AES密钥必须为16/24/32字节长度')
        return False

    try:
        # 解码并提取IV
        decoded_data = base64.b64decode(encrypted_data)
        iv = decoded_data[:16]  # 提取前16字节作为IV
        cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # 解密并去除填充
        decrypted_data = decryptor.update(decoded_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(decrypted_data) + unpadder.finalize()

        return data.decode('utf-8', 'ignore')
    except Exception as e:
        print(f'解密失败: {e!s}')
        return False


def duplicate(
    iterable: Iterable[Any],
    keep: Callable[[Any], Any] = lambda x: x,
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False,
) -> list[Any]:
    """增强去重功能，解决重复元素可能覆盖的问题。

    Args:
        iterable: 需要去重的可迭代对象
        keep: 元素提取函数，用于指定保留的元素内容
        key: 去重键生成函数，用于判断元素是否重复
        reverse: 是否反向遍历原序列进行去重

    Returns:
        List[Any]: 去重后的元素列表

    Examples:
        >>> duplicate([1, 2, 3, 2, 1])
        [1, 2, 3]
        >>> duplicate([{'id': 1}, {'id': 2}, {'id': 1}], key=lambda x: x['id'])
        [{"id": 1}, {"id": 2}]
    """
    seen: dict[Any, Any] = {}
    result: list[Any] = []

    # 转换为列表以确保可以被reversed
    iterable_list = list(iterable)
    items = reversed(iterable_list) if reverse else iterable_list

    for item in items:
        keep_val = keep(item)
        key_val = key(item)
        if key_val not in seen:
            seen[key_val] = keep_val
            result.append(keep_val)

    return list(reversed(result)) if reverse else result


def align(str1: Any, distance: int = 36, alignment: Literal['L', 'C', 'R'] = 'L') -> str:
    """将字符串按指定宽度和对齐方式格式化。

    Args:
        str1: 要对齐的对象，会自动转换为字符串
        distance: 总宽度
        alignment: 对齐方式，可选值: L(左对齐), C(居中), R(右对齐)

    Returns:
        str: 对齐后的字符串

    Raises:
        ValueError: 如果对齐方式无效

    Examples:
        >>> align('hello', 10, 'L')
        'hello     '
        >>> align('hello', 10, 'C')
        '  hello   '
        >>> align('hello', 10, 'R')
        '     hello'
    """
    if alignment == 'C':
        return str(str1).center(distance, ' ')

    str1 = str(str1)
    # 计算UTF-8编码后的长度
    length = len(str1.encode('utf-8', 'ignore'))
    slen = max(0, distance - length)

    if alignment == 'L':
        aligned_str = f'{str1}{" " * slen}'
    elif alignment == 'R':
        aligned_str = f'{" " * slen}{str1}'
    else:
        raise ValueError("Alignment must be one of 'L', 'C', or 'R'")

    return aligned_str


def remove_all_blank(value: str, keep_blank: bool = True, custom_invisible: Pattern[str] | None = None) -> str:
    """移除字符串中的所有不可见字符。

    Args:
        value: 输入字符串
        keep_blank: 是否保留空格，默认为True
        custom_invisible: 自定义的不可见字符正则表达式

    Returns:
        str: 处理后的字符串

    Raises:
        TypeError: 如果输入不是字符串类型

    Examples:
        >>> remove_all_blank('Hello\tworld\n', keep_blank=False)
        'Helloworld'
        >>> remove_all_blank('Hello\tworld\n', keep_blank=True)
        'Hello world '
    """
    if not isinstance(value, str):
        raise TypeError(f'输入必须是字符串类型，当前输入类型为: {type(value)}')

    # 移除控制字符等不可见字符
    custom_invisible = custom_invisible or re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+')
    value = re.sub(custom_invisible, '', value)

    # 根据需要移除空格
    whitespace_set = set(string.whitespace)
    return ''.join([ch for ch in value if ch.isprintable() and (keep_blank or ch not in whitespace_set)])


def str_replace(replacement: str, trims: Sequence[tuple[str, str]], implementation: Literal['loop', 'reduce'] = 'reduce') -> str:
    """执行多组字符串替换操作。

    Args:
        replacement: 待处理的原始字符串
        trims: 替换规则序列，每个元素为(search, replace)元组
        implementation: 实现方式选择:
            - "loop": 循环遍历方式（最易读）
            - "reduce": 函数式编程方式（平衡性能与可读性）

    Returns:
        str: 完成所有替换后的字符串

    Raises:
        ValueError: 当替换规则无效时
        TypeError: 当输入类型不符合要求时

    Examples:
        >>> str_replace('abcde', [('a', 'A'), ('c', 'C')])
        'AbCde'
        >>> str_replace('hello', [('l', 'x')], implementation='loop')
        'hexxo'
    """
    # 输入验证
    if not isinstance(replacement, str):
        raise TypeError(f"'replacement'应为字符串类型，实际为{type(replacement).__name__}")

    for i, (search, replace) in enumerate(trims):
        if not isinstance(search, str) or not isinstance(replace, str):
            raise ValueError(f'替换规则[{i}]必须包含两个字符串')
        if not search:
            raise ValueError(f'替换规则[{i}]的查找字符串不能为空')

    if implementation == 'loop':
        # 实现方式1: 循环遍历（最直观）
        result = replacement
        for search, replace in trims:
            result = result.replace(search, replace)
        return result

    if implementation == 'reduce':
        # 实现方式2: 函数式编程（原始实现）
        return reduce(lambda strtmp, item: strtmp.replace(item[0], item[1]), trims, replacement)

    raise ValueError(f"无效实现方式: {implementation}，请选择'loop'/'reduce'")


def str_clean(replacement: str, trims: Sequence[str]) -> str:
    """字符清除，通过调用 str_replace 实现将指定子字符串替换为空字符串。

    Args:
        replacement: 待处理的字符串
        trims: 包含要清除的子字符串的序列

    Returns:
        str: 清除指定子字符串后的结果

    Examples:
        >>> str_clean('Hello###World!', ['#', '!'])
        'HelloWorld'
    """
    # 将清除规则转换为 str_replace 所需的 (search, replace) 格式
    replace_rules = [(item, '') for item in trims]
    # 使用 reduce 实现方式保持与原逻辑一致
    return str_replace(replacement, replace_rules, implementation='reduce')


def re_sub(replacement: str, trims: Sequence[tuple[str, str]]) -> str:
    """使用正则表达式序列对字符串进行替换。

    Args:
        replacement: 待处理的原始字符串
        trims: 包含正则替换规则的序列，每个规则为(search_pattern, replace_str)元组

    Returns:
        str: 应用所有替换规则后的结果字符串

    Raises:
        TypeError: 如果输入参数类型不符合要求
        re.error: 如果正则表达式模式无效

    Examples:
        >>> re_sub('abc123def', [('\\d+', ''), ('[a-c]', 'X')])
        'Xdef'
    """
    # 输入类型验证
    if not isinstance(replacement, str):
        raise TypeError(f"'replacement'必须是字符串，实际为{type(replacement).__name__}")

    # 预编译正则表达式并验证规则
    compiled_rules = []
    for idx, (pattern, repl) in enumerate(trims):
        if not isinstance(pattern, str) or not isinstance(repl, str):
            raise TypeError(f'规则[{idx}]必须包含两个字符串')
        try:
            compiled_pattern = re.compile(pattern)
            compiled_rules.append((compiled_pattern, repl))
        except re.error as e:
            raise re.error(f'规则[{idx}]正则表达式无效: {e}') from e

    if not compiled_rules:
        return replacement

    # 使用预编译模式进行替换，提升性能
    return reduce(lambda str_tmp, rule: rule[0].sub(rule[1], str_tmp), compiled_rules, replacement)


def re_compile(replacement: str, replace_rules: Sequence[tuple[str, str]]) -> str:
    """使用编译的正则表达式模式集对字符串进行一次性替换。

    与re_sub的功能区别:
    - re_compile: 一次性编译所有模式并执行单次替换，适用于简单字符串替换场景
    - re_sub: 按顺序应用多个替换规则，支持复杂正则表达式和预编译优化
    适用场景
        场景 推荐函数 原因 复杂正则表达式替换 re_sub 支持完整正则语法，如分组、断言等 简单字符串替换 re_compile 性能更优，避免多次正则匹配开销
        场景 推荐函数 原因 独立无依赖替换 re_sub 可实现"先替换A为B，再替换B为C"的链式操作 独立无依赖替换 re_compile 并行替换效率更高，无顺序依赖问题
        场景 推荐函数 原因 大量替换规则 re_compile 单次编译匹配，内存占用更低
    行为差异
        示例 ：对字符串"abc"应用规则 [('a', 'b'), ('b', 'c')]
        - re_sub 结果： 'cc' （先a→b，再b→c）
        - re_compile 结果： 'bc' （a→b和原b→c同时进行）

    Args:
        replacement: 待处理的原始字符串
        replace_rules: 包含替换规则的序列，每个规则为(search_str, replace_str)元组

    Returns:
        str: 应用所有替换规则后的结果字符串

    Raises:
        TypeError: 如果输入参数类型不符合要求
        re.error: 如果正则表达式模式无效

    Examples:
        >>> re_compile('A1B2C3', [('A', 'X'), ('B', 'Y'), ('C', 'Z')])
        'X1Y2Z3'

    pattern = re.compile("|".join(f"{re.escape(trim[0])}" for trim in trimsL))
    return pattern.sub(
        lambda x: next((trim[1] for trim in trimsL if trim[0] == x.group()), x.group()),
        replacement,
    )
    """

    # 输入类型验证
    if not isinstance(replacement, str):
        raise TypeError(f"'replacement'必须是字符串，实际为{type(replacement).__name__}")

    if not isinstance(replace_rules, Sequence):
        raise TypeError(f"'replace_rules'必须是序列类型，实际为{type(replace_rules).__name__}")

    # 验证规则格式并提取模式
    patterns = []
    replacements: dict[str, str] = {}
    for idx, rule in enumerate(replace_rules):
        if not isinstance(rule, tuple) or len(rule) != 2:
            raise TypeError(f'规则[{idx}]必须是包含两个元素的元组')

        pattern_str, repl_str = rule
        if not isinstance(pattern_str, str) or not isinstance(repl_str, str):
            raise TypeError(f'规则[{idx}]的元素必须是字符串')

        escaped_pattern = re.escape(pattern_str)
        patterns.append(escaped_pattern)
        replacements[pattern_str] = repl_str

    if not patterns:
        return replacement

    # 编译组合模式
    combined_pattern = re.compile('|'.join(patterns))

    # 执行替换
    def replace_match(match: re.Match) -> str:
        matched_str = match.group()
        return str(replacements.get(matched_str, matched_str))  # 明确转换为str类型

    return combined_pattern.sub(replace_match, replacement)


def str_split_limited_list(intext: str, minlen: int = 100, maxlen: int = 300) -> list[str]:
    """将输入的字符串分割成若干个段落，每个段落的长度在minlen和maxlen之间。

    优先在句子结束符（。！？）处分割，其次在逗号、分号处分割，最后在空格处分割

    Args:
        intext: 输入的字符串
        minlen: 最小段落长度
        maxlen: 最大段落长度

    Returns:
        list: 分割后的段落列表

    Examples:
        >>> paragraphs = str_split_limited_list('长文本内容...', 50, 200)
        >>> len(paragraphs)  # 返回段落数量
        5
    """

    # 清理文本
    cleaned_text = re.sub(r'[\r\u200b] | {2,}', '', intext)
    cleaned_text = re.sub(r'\n+', ' ', cleaned_text)
    cleaned_text = re.sub(r'([ 。！？]){2,}', r'\1', cleaned_text)
    cleaned_text = re.sub(r' ，{2,}', '，', cleaned_text)

    if len(cleaned_text) <= maxlen:
        return [cleaned_text] if cleaned_text else []

    segments = []
    start = 0

    while start < len(cleaned_text):
        end = min(start + maxlen, len(cleaned_text))
        segment = cleaned_text[start:end]

        # 优先查找句号、感叹号、问号
        for sep in [r'[。！？]', r'[，；]', r'\s']:
            matches = list(re.finditer(sep, segment))
            if matches:
                # 找到最后一个满足 minlen 条件的分割点
                for m in reversed(matches):
                    if m.end() > minlen:
                        split_pos = m.end()
                        segments.append(segment[:split_pos])
                        start += split_pos
                        break
                else:
                    # 没有满足 minlen 的分割点，则继续下一级分隔符
                    continue
                break
        else:
            # 无合适分割点时，强制截断
            segments.append(segment)
            start += maxlen

    # 合并最后一段如果太短
    if len(segments) > 1 and len(segments[-1]) < minlen:
        segments[-2] += segments.pop()

    return segments


def str2list(intext: str, maxlen: int = 300) -> list[str]:
    """将输入的字符串分割成若干个段落，每个段落的长度不超过 maxlen。

    基于中文句号分割文本，适用于中文段落处理

    Args:
        intext: 输入的字符串
        maxlen: 最大段落长度

    Returns:
        list: 分割后的段落列表

    Examples:
        >>> paragraphs = str2list('这是第一段。这是第二段。', 20)
        >>> len(paragraphs)  # 返回段落数量
        2
    """
    # 预处理文本，将各种换行符和特殊字符转换为句号
    processed_text = str_replace(
        intext,
        [('\r', '。'), ('\n', '。'), (' ', ''), ('\u200b', ''), ('。。', '。')],
    )

    # 分割文本
    sentence_list = processed_text.split('。')
    sentence_list = [f'{item}。' for item in sentence_list if item]

    result_list = []
    temp_str = ''

    for sentence in sentence_list:
        # 如果当前段落长度不超过最大长度，则继续添加新的句子
        if len(temp_str + sentence) <= maxlen:
            temp_str += sentence
        else:
            # 否则，当前段落结束，添加到段落列表中
            result_list.append(temp_str)
            temp_str = sentence

    # 处理最后一个段落
    if temp_str:
        result_list.append(temp_str)

    return result_list


def dict2qss(dict_tmp: dict) -> str:
    """字典形式的QSS转字符串。

    注意：此函数已弃用，推荐使用 qdarkstyle.utils.scss._dict_to_scss 替代

    Args:
        dict_tmp: 包含QSS样式的字典

    Returns:
        str: 转换后的QSS字符串
    """
    temp = json.dumps(dict_tmp)
    qss = str_replace(temp, [('[', ''), (']', ''), (',', ';'), ('"', ''), (': {', '{')])
    return qss.strip('{}')


def groupby(iterobj: Iterable[Any], key: Callable[[Any], Any]) -> dict[Any, list[Any]]:
    """按指定键对可迭代对象进行分组。

    自实现的groupby函数，与itertools.groupby不同之处在于：
    - 可以合并不连续但是相同的组
    - 返回的是普通字典，而非迭代器

    Args:
        iterobj: 要分组的可迭代对象
        key: 分组键函数，用于生成分组依据

    Returns:
        dict: 分组后的字典，键为分组依据，值为对应的元素列表

    Examples:
        >>> groupby([1, 2, 3, 4, 5], key=lambda x: x % 2)
        {1: [1, 3, 5], 0: [2, 4]}
    """
    groups: dict[Any, list[Any]] = {}
    for item in iterobj:
        groups.setdefault(key(item), []).append(item)
    return groups


def random_char(length: int = 20) -> str:
    """生成指定长度的随机字符串，包含数字、大写字母和小写字母。

    Args:
        length: 随机字符串的长度

    Returns:
        str: 生成的随机字符串

    Examples:
        >>> random_str = random_char(10)  # 生成10位随机字符串
        >>> len(random_str)  # 验证长度
        10
    """
    return ''.join(
        str(random.randint(0, 9))  # noqa: S311
        if random.randint(1, 2) == 1  # noqa: S311
        else (
            chr(
                random.randint(97, 122)  # 小写字母  # noqa: S311
                if random.randint(1, 2) == 1  # noqa: S311
                else random.randint(65, 90)  # 大写字母 # noqa: S311
            )
        )
        for _ in range(length)
    )


def class_add_dict(in_obj: Any) -> dict[str, Any]:
    """完善对象字典并转换为字典。

    确保对象具有__dict__属性，并将非私有、非可调用属性添加到字典中

    Args:
        in_obj: 要处理的对象

    Returns:
        dict: 对象的属性字典
    """
    if not hasattr(in_obj, '__dict__'):
        in_obj.__dict__ = {}

    # 更新字典，排除私有属性和可调用方法
    in_obj.__dict__.update({key: value for key, value in vars(in_obj).items() if not key.startswith('__') and not callable(value)})

    return in_obj.__dict__


def format_html_string(html_content: str) -> str:
    """格式化HTML字符串并清理内容。

    清理HTML字符串中的脚本标签、样式标签、注释、特殊字符和多余空白字符。

    Args:
        html_content: 要格式化的原始HTML字符串

    Returns:
        str: 格式化后的纯文本字符串

    Raises:
        TypeError: 如果输入不是字符串类型
        ValueError: 如果正则表达式错误
        RuntimeError: 如果HTML格式化过程失败

    Examples:
        >>> format_html_string('<p>Hello <script>test</script>World</p>')
        'Hello World'
    """
    # 输入验证
    if not isinstance(html_content, str):
        error_msg = f'输入必须是字符串，实际为{type(html_content).__name__}'
        raise TypeError(error_msg)

    if not html_content.strip():
        return ''

    try:
        # 增强HTML清理规则
        clean_rules: list[tuple[str, str]] = [
            (r'<\s*script[^>]*>.*?</\s*script\s*>', ''),  # 移除script标签
            (r'<br\s*/?>', ' '),  # 将br标签替换为空格
            (r'<\s*style[^>]*>.*?</\s*style\s*>', ''),  # 移除style标签
            (r'<a[^>]*>.*?</a>', ''),  # 移除a标签
            (r'<([a-z][a-z][a-z0-9]*)\s+[^>]*>', r'<\1>'),  # 移除标签属性
            (r'<!--.*?-->', ''),  # 移除HTML注释
            (r'[‘’“”]', "'"),  # 统一引号
            (r'﻿', ''),  # 移除BOM头
            (r'[•‣◦⁃]', ':'),  # 替换特殊符号
            (r'<[^>]*>', ''),  # 移除所有HTML标签
            (r'\s+', ' '),  # 合并多个空白字符
        ]

        # 使用re_sub应用所有清理规则
        return re_sub(html_content, clean_rules).strip()

    except re.error as e:
        print('处理失败', error_msg := f'正则表达式错误:{e!s}')
        raise ValueError(error_msg) from e
    except Exception as e:
        print('处理失败', error_msg := f'HTML格式化失败:{e!s}')
        raise RuntimeError(error_msg) from e


def obj_to_str(obj: Any) -> str:
    """将对象转换为字符串，递归处理所有嵌套对象。

    Args:
        obj: 要转换的对象

    Returns:
        str: 转换后的字符串表示
    """
    if isinstance(obj, (list, tuple, set)):
        return ', '.join(map(obj_to_str, obj))
    if isinstance(obj, dict):
        return ', '.join(f'{k}: {obj_to_str(v)}' for k, v in obj.items())
    if isinstance(obj, str):
        return re.sub(r'<([^<>]+)>', r'\\<\\1\\>', obj)
    return str(obj)


if __name__ == '__main__':
    # 测试函数定义
    def test_str_replace():
        replacement = 'aaa-bbb-ccc'
        trims = [('a', 'A'), ('b', 'B'), ('c', 'C')]
        print(str_replace(replacement, trims))

    def test_str_clean():
        test_str = '###Hello ?World'
        print(str_clean(test_str, ['#', '?']))

    def test_re_sub():
        replacement = 'This\n is \u2018a\u2019 test\ufeff string'
        trims = [('\n', ''), ('\u2018', "'"), ('\u2019', "'"), ('\ufeff', '')]
        print(re_sub(replacement, trims))

    def test_re_compile():
        replacement = 'hello A and B'
        trims_list = [('A', 'aaa'), ('B', 'bbb')]
        print(re_compile(replacement, trims_list))

    # 运行单元测试
    from unittest import TestCase

    class TestStringUtils(TestCase):
        def test_remove_whitespace(self):
            """测试移除多余空白字符"""
            html = 'New\n\t\r  Sea'
            self.assertEqual(format_html_string(html), 'New Sea')

        def test_remove_script_tags(self):
            """测试移除script标签"""
            html = '<script>alert(1)</script>Hello'
            self.assertEqual(format_html_string(html), 'Hello')

        def test_remove_a_tags(self):
            """测试移除a标签"""
            html = "<a href='#'>Link</a>Text"
            self.assertEqual(format_html_string(html), 'Text')

        def test_special_chars(self):
            """测试特殊字符替换"""
            html = "'Hello'\u2022World\ufeff"
            self.assertEqual(format_html_string(html), "'Hello':World")

    # 运行单元测试
    # main()

    # 可以取消注释以下行来运行特定的功能测试
    test_str_replace()
    test_str_clean()
    test_re_sub()
    test_re_compile()

    # 测试更多功能
    # str2 = "Powe, on；the 2333, 。哈哈 ！！\x08\x0e\U0001f914看看可以吗？一行代码就可以了！^_^"
    # print(remove_all_blank(str2, keep_blank=False))
    # print(remove_all_blank(str2, keep_blank=True))
