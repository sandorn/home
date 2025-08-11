# !/us/bin/env python
"""
==============================================================
Description  : string  |  dict  |  list  |  tupe  |  json
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2022-12-22 17:35:56
LastEditTime : 2023-02-25 04:31:14
FilePath     : /CODE/xjLib/xt_String.py
Github       : https://github.com/sandorn/home
==============================================================
https://zhuanlan.zhihu.com/p/696103020
"""

import base64
import hashlib
import json
import os
import random
import re
import string
from functools import reduce
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Literal,
    Optional,
    Pattern,
    Sequence,  # Sequence是更通用的类型，可以包含列表和元组
    Tuple,
    Union,
)

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def is_valid_id(id_number: Union[str, int]) -> bool:
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
        raise TypeError("身份证号码必须是字符串或整数类型")

    # 移除可能存在的空格
    id_number = id_number.strip()

    # 验证18位身份证
    if len(id_number) == 18:
        # 18位身份证格式：前17位为数字，最后一位为数字或X/x
        pattern = r"^\d{17}(\d|X|x)$"
        if not re.match(pattern, id_number):
            return False

        # 计算校验码
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

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


def str_to_md5(data):
    return encrypt_str(data, "md5")


def str_to_sha1(data):
    return encrypt_str(data, "sha1")


def encrypt_str(
    data: Union[str, bytes], algorithm: str = "md5", key: Optional[str] = None
) -> Union[str, bool]:
    """
    对字符串进行加密或哈希处理

    支持哈希算法(md5, sha1, sha256, sha512)和加密算法(aes-256-cbc)
    哈希算法不需要密钥，加密算法(aes)需要提供16/24/32字节的密钥

    Args:
        data: 待处理的字符串或字节数据
        algorithm: 加密/哈希算法，可选值: md5, sha1, sha256, sha512, aes-256-cbc
        key: 加密密钥，AES算法必填，长度应为16/24/32字节

    Returns:
        str: 处理后的结果
        bool: 发生错误时返回False
    """
    # 确保输入是字节类型
    if isinstance(data, str):
        data = data.encode("utf-8", "ignore")

    # 哈希算法处理
    hash_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }

    if algorithm in hash_algorithms:
        hash_obj = hash_algorithms[algorithm]()
        hash_obj.update(data)
        return hash_obj.hexdigest()

    # AES加密算法处理
    elif algorithm == "aes-256-cbc":
        if not key or len(key) not in [16, 24, 32]:
            print("AES密钥必须为16/24/32字节长度")
            return False

        try:
            # 生成随机IV
            iv = os.urandom(16)  # 随机生成16字节IV
            cipher = Cipher(
                algorithms.AES(key.encode()), modes.CBC(iv), backend=default_backend()
            )
            encryptor = cipher.encryptor()

            # 数据填充
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()

            # 加密并编码(IV+密文)
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return base64.b64encode(iv + ciphertext).decode()
        except Exception as e:
            print(f"AES加密失败: {str(e)}")
            return False

    else:
        print(f"不支持的算法: {algorithm}")
        return False


def decrypt_str(
    encrypted_data: str, algorithm: str = "aes-256-cbc", key: Optional[str] = None
) -> Union[str, bool]:
    """
    对加密字符串进行解密

    目前仅支持AES加密算法的解密

    Args:
        encrypted_data: 待解密的字符串
        algorithm: 解密算法，目前仅支持 aes-256-cbc
        key: 解密密钥，必须与加密时使用的密钥相同

    Returns:
        str: 解密后的原始字符串
        bool: 发生错误时返回False
    """
    if algorithm != "aes-256-cbc":
        print(f"不支持的解密算法: {algorithm}")
        return False

    if not key or len(key) not in [16, 24, 32]:
        print("AES密钥必须为16/24/32字节长度")
        return False

    try:
        # 解码并提取IV
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:16]  # 提取前16字节作为IV
        cipher = Cipher(
            algorithms.AES(key.encode()), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()

        # 解密并去除填充
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(decrypted_data) + unpadder.finalize()

        return data.decode("utf-8", "ignore")
    except Exception as e:
        print(f"解密失败: {str(e)}")
        return False


def duplicate(
    iterable: Iterable[Any],
    keep: Callable[[Any], Any] = lambda x: x,
    key: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False,
) -> List[Any]:
    """
    增强去重功能，解决重复元素可能覆盖的问题

    Args:
        iterable: 需要去重的可迭代对象
        keep: 元素提取函数，用于指定保留的元素内容
        key: 去重键生成函数，用于判断元素是否重复
        reverse: 是否反向遍历原序列进行去重

    Returns:
        List[Any]: 去重后的元素列表
    """
    seen: dict[Any, Any] = {}
    result: List[Any] = []
    items = reversed(iterable) if reverse else iterable

    for item in items:
        keep_val = keep(item)
        key_val = key(item)
        if key_val not in seen:
            seen[key_val] = keep_val
            result.append(keep_val)

    return list(reversed(result)) if reverse else result


def align(str1, distance=36, alignment="L"):
    # #居中打印为string类方法
    if alignment == "C":
        return str1.center(distance, " ")
    if not isinstance(str1, str):
        str1 = str(str1)
    # #print打印对齐
    length = len(str1.encode("utf-8", "ignore"))
    slen = max(0, distance - length)

    if alignment == "L":
        aligned_str = f"{str1}{' ' * slen}"
    elif alignment == "R":
        aligned_str = f"{' ' * slen}{str1}"
    else:
        raise ValueError("Alignment must be one of 'left', 'center', or 'right'")
    return aligned_str


def remove_all_blank(
    value: str, keep_blank: bool = True, custom_invisible: Optional[Pattern] = None
) -> str:
    """
    移除字符串中的所有不可见字符

    Args:
        value: 输入字符串
        keep_blank: 是否保留空格，默认为True

    Returns:
        str: 处理后的字符串

    Raises:
        TypeError: 如果输入不是字符串类型
    """
    if not isinstance(value, str):
        raise TypeError(f"输入必须是字符串类型，当前输入类型为: {type(value)}")

    custom_invisible = custom_invisible or r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+"
    value = re.sub(custom_invisible, "", value)

    whitespace_set = set(string.whitespace)
    return "".join(
        [
            ch
            for ch in value
            if ch.isprintable() and (keep_blank or ch not in whitespace_set)
        ]
    )


def str_replace(
    replacement: str,
    trims: Sequence[tuple[str, str]],
    implementation: Literal["loop", "reduce"] = "reduce",
) -> str:
    """
    执行多组字符串替换操作

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
        >>> str_replace("abcde", [("a", "A"), ("c", "C")])
        'AbCde'
        >>> str_replace("hello", [("l", "x")], implementation="loop")
        'hexxo'
    """
    # 输入验证
    if not isinstance(replacement, str):
        raise TypeError(
            f"'replacement'应为字符串类型，实际为{type(replacement).__name__}"
        )

    for i, (search, replace) in enumerate(trims):
        if not isinstance(search, str) or not isinstance(replace, str):
            raise ValueError(f"替换规则[{i}]必须包含两个字符串")
        if not search:
            raise ValueError(f"替换规则[{i}]的查找字符串不能为空")

    if implementation == "loop":
        # 实现方式1: 循环遍历（最直观）
        result = replacement
        for search, replace in trims:
            result = result.replace(search, replace)
        return result

    elif implementation == "reduce":
        # 实现方式2: 函数式编程（原始实现）
        return reduce(
            lambda strtmp, item: strtmp.replace(item[0], item[1]), trims, replacement
        )

    else:
        raise ValueError(
            f"无效实现方式: {implementation}，请选择'loop'/'reduce'/'translate'"
        )


def str_clean(replacement: str, trims: Sequence[str]) -> str:
    """
    字符清除，通过调用 str_replace 实现将指定子字符串替换为空字符串

    Args:
        replacement: 待处理的字符串
        trims: 包含要清除的子字符串的序列

    Returns:
        str: 清除指定子字符串后的结果
    """
    # 将清除规则转换为 str_replace 所需的 (search, replace) 格式
    replace_rules = [(item, "") for item in trims]
    # 使用 reduce 实现方式保持与原逻辑一致
    return str_replace(replacement, replace_rules, implementation="reduce")


def re_sub(replacement: str, trims: Sequence[Tuple[str, str]]) -> str:
    """
    使用正则表达式序列对字符串进行替换

    Args:
        replacement: 待处理的原始字符串
        trims: 包含正则替换规则的序列，每个规则为(search_pattern, replace_str)元组

    Returns:
        str: 应用所有替换规则后的结果字符串

    Raises:
        TypeError: 如果输入参数类型不符合要求
        re.error: 如果正则表达式模式无效

    Examples:
        >>> re_sub("abc123def", [("\\d+", ""), ("[a-c]", "X")])
        'Xdef'
    """
    # 输入类型验证
    if not isinstance(replacement, str):
        raise TypeError(
            f"'replacement'必须是字符串，实际为{type(replacement).__name__}"
        )

    # 预编译正则表达式并验证规则
    compiled_rules = []
    for idx, (pattern, repl) in enumerate(trims):
        if not isinstance(pattern, str) or not isinstance(repl, str):
            raise TypeError(f"规则[{idx}]必须包含两个字符串")
        try:
            compiled_pattern = re.compile(pattern)
            compiled_rules.append((compiled_pattern, repl))
        except re.error as e:
            raise re.error(f"规则[{idx}]正则表达式无效: {e}") from e

    if not compiled_rules:
        return replacement

    # 使用预编译模式进行替换，提升性能
    return reduce(
        lambda str_tmp, rule: rule[0].sub(rule[1], str_tmp), compiled_rules, replacement
    )


def re_compile(replacement: str, replace_rules: Sequence[Tuple[str, str]]) -> str:
    """
    使用编译的正则表达式模式集对字符串进行一次性替换

    与re_sub的功能区别:
    - re_compile: 一次性编译所有模式并执行单次替换，适用于简单字符串替换场景
    - re_sub: 按顺序应用多个替换规则，支持复杂正则表达式和预编译优化
    适用场景
        场景 推荐函数 原因 复杂正则表达式替换 re_sub 支持完整正则语法，如分组、断言等 简单字符串替换 re_compile 性能更优，避免多次正则匹配开销 有依赖关系的替换 re_sub 可实现"先替换A为B，再替换B为C"的链式操作 独立无依赖替换 re_compile 并行替换效率更高，无顺序依赖问题 大量替换规则 re_compile 单次编译匹配，内存占用更低
    行为差异
        示例 ：对字符串"abc"应用规则 [('a', 'b'), ('b', 'c')]
        - re_sub 结果： 'cc' （先a→b，再b→c）
        - re_compile 结果： 'bc' （a→b和原b→c同时进行）
    性能特点
        - re_sub ：
            - 优点：支持渐进式替换，逻辑直观
            - 缺点：多次正则匹配，性能随规则数量线性下降
        - re_compile ：
            - 优点：单次匹配完成所有替换，O(n)复杂度
            - 缺点：不支持依赖关系替换，复杂模式可能产生冲突
    错误处理
        - re_sub ：在预编译阶段验证每个正则表达式，提供具体错误位置
        - re_compile ：验证规则格式，但组合模式错误定位较困难 6. 最佳实践
        - 当需要 复杂正则功能 或 顺序依赖替换 时使用 re_sub
        - 当进行 简单字符串替换 且规则 相互独立 时使用 re_compile
        - 对性能敏感的批量替换任务优先考虑 re_compile
    Args:
        replacement: 待处理的原始字符串
        replace_rules: 包含替换规则的序列，每个规则为(search_str, replace_str)元组

    Returns:
        str: 应用所有替换规则后的结果字符串

    Raises:
        TypeError: 如果输入参数类型不符合要求
        re.error: 如果正则表达式模式无效

    Examples:
        >>> re_compile("A1B2C3", [("A", "X"), ("B", "Y"), ("C", "Z")])
        'X1Y2Z3'

    pattern = re.compile("|".join(f"{re.escape(trim[0])}" for trim in trimsL))
    return pattern.sub(
        lambda x: next((trim[1] for trim in trimsL if trim[0] == x.group()), x.group()),
        replacement,
    )
    """

    # 输入类型验证
    if not isinstance(replacement, str):
        raise TypeError(
            f"'replacement'必须是字符串，实际为{type(replacement).__name__}"
        )

    if not isinstance(replace_rules, Sequence):
        raise TypeError(
            f"'replace_rules'必须是序列类型，实际为{type(replace_rules).__name__}"
        )

    # 验证规则格式并提取模式
    patterns = []
    replacements = {}
    for idx, rule in enumerate(replace_rules):
        if not isinstance(rule, Tuple) or len(rule) != 2:
            raise TypeError(f"规则[{idx}]必须是包含两个元素的元组")

        pattern_str, repl_str = rule
        if not isinstance(pattern_str, str) or not isinstance(repl_str, str):
            raise TypeError(f"规则[{idx}]的元素必须是字符串")

        escaped_pattern = re.escape(pattern_str)
        patterns.append(escaped_pattern)
        replacements[pattern_str] = repl_str

    if not patterns:
        return replacement

    # 编译组合模式
    combined_pattern = re.compile("|".join(patterns))

    # 执行替换
    def replace_match(match: re.Match) -> str:
        matched_str = match.group()
        return replacements.get(matched_str, matched_str)

    return combined_pattern.sub(replace_match, replacement)


def str_split_limited_list(intext, minlen=100, maxlen=300):
    """
    将输入的字符串分割成若干个段落，每个段落的长度在minlen和maxlen之间
    优先在句子结束符（。！？）处分割，其次在逗号、分号处分割，最后在空格处分割

    Args:
        intext: 输入的字符串
        minlen: 最小段落长度
        maxlen: 最大段落长度

    Returns:
        list: 分割后的段落列表
    """
    # 清理文本：移除特殊字符，合并多余标点
    cleaned_text = re.sub(r"[\r\u200b]| {2,}", "", intext)  # 删除特殊字符和多余空格
    cleaned_text = re.sub(r"\n+", " ", cleaned_text)  # 换行符转空格
    cleaned_text = re.sub(r"([。！？]){2,}", r"\1", cleaned_text)  # 合并连续标点
    cleaned_text = re.sub(r"，{2,}", "，", cleaned_text)  # 合并连续逗号

    # 处理短文本情况
    if len(cleaned_text) <= minlen:
        return [cleaned_text] if cleaned_text else [intext]

    segments = []
    start = 0
    text_len = len(cleaned_text)

    while start < text_len:
        # 确定当前段的结束位置
        end = min(start + maxlen, text_len)

        # 如果剩余文本不足最小长度，直接取剩余部分
        if text_len - start <= minlen:
            segments.append(cleaned_text[start:])
            break

        # 查找最佳分割点（从后往前找）
        segment = cleaned_text[start:end]
        split_pos = -1

        # 优先在句子结束符处分割
        for match in re.finditer(r"[。！？]", segment):
            split_pos = match.end()

        # 其次在逗号/分号处分割
        if split_pos == -1:
            for match in re.finditer(r"[，；]", segment):
                if match.end() > minlen:
                    split_pos = match.end()

        # 最后在空格处分割
        if split_pos == -1:
            space_match = list(re.finditer(r"\s", segment))
            if space_match and space_match[-1].end() > minlen:
                split_pos = space_match[-1].end()

        # 无合适分割点时，在maxlen处强制分割
        if split_pos == -1 or split_pos < minlen:
            segments.append(segment)
            start = end
        else:
            segments.append(cleaned_text[start : start + split_pos])
            start += split_pos

    # 处理最后一段过短的情况（与前一段合并）
    if len(segments) > 1 and len(segments[-1]) < minlen:
        last_segment = segments.pop()
        segments[-1] += last_segment

    return segments


def str2list(intext, maxlen=300):
    """
    将输入的字符串分割成若干个段落，每个段落的长度不超过 maxlen。
    """
    sentence_list = re.split(
        "。",
        str_replace(
            intext,
            [["\r", "。"], ["\n", "。"], [" ", ""], ["\u200b", ""], ["。。", "。"]],
        ),
    )
    sentence_list = [f"{item}。" for item in sentence_list if item]

    resturn_list = []
    temp_str = ""

    for sentence in sentence_list:
        # 如果当前段落长度不超过最大长度，则继续添加新的句子
        if len(temp_str + sentence) <= maxlen:
            temp_str += sentence
        else:
            # 否则，当前段落结束，添加到段落列表中
            resturn_list.append(temp_str)
            temp_str = sentence

    # 处理最后一个段落
    if temp_str:
        resturn_list.append(temp_str)

    return resturn_list


def dict2qss(dict_tmp: dict):
    """字典形式的QSS转字符串。弃用!
    qdarkstyle.utils.scss._dict_to_scss 替代
    """
    # # 排序  print key, dict[key] for key in sorted(dict.keys())
    temp = json.dumps(dict_tmp)
    qss = str_replace(temp, [(",", ";"), ('"', ""), (": {", "{")])
    return qss.strip("{}")


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
    """
    实现指定长度的随机数,有数字、大写字母、小写字母
    length: 随机数的长度
    """
    return "".join(
        str(random.randint(0, 9))
        if random.randint(1, 2) == 1
        else (
            chr(
                random.randint(97, 122)
                if random.randint(1, 2) == 1
                else random.randint(65, 90)
            )
        )
        for _ in range(length)
    )


def class_add_dict(in_obj):
    """完善对象字典并转出字典"""
    if not hasattr(in_obj, "__dict__"):
        in_obj.__dict__ = {}

    in_obj.__dict__.update(
        {
            key: value
            for key, value in vars(in_obj).items()
            if not key.startswith("__") and not callable(value)
        }
    )

    return in_obj.__dict__


def format_html_string(html_content: str) -> str:
    """
    格式化HTML字符串并支持对话框输出

    移除多余字符、标签和属性，并可选择在对话框中显示结果

    Args:
        html_content: 要格式化的原始HTML字符串

    Returns:
        str: 格式化后的纯文本字符串

    Examples:
        >>> format_html_string('<p>Hello <script>test</script>World</p>', show_dialog=False)
        'Hello World'
    """
    # 输入验证
    if not isinstance(html_content, str):
        error_msg = f"输入必须是字符串，实际为{type(html_content).__name__}"
        raise TypeError(error_msg)

    if not html_content.strip():
        return ""

    try:
        # 增强HTML清理规则
        clean_rules: List[Tuple[str, str]] = [
            (r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", ""),  # 移除script标签
            (r"<br\s*/?>", " "),  # 将br标签替换为空格
            (r"<\s*style[^>]*>.*?<\s*/\s*style\s*>", ""),  # 移除style标签
            (r"<a[^>]*>.*?</a>", ""),
            (r"<([a-z][a-z][a-z0-9]*)\s+[^>]*>", r"<\1>"),  # 移除标签属性
            (r"<!--.*?-->", ""),  # 移除HTML注释
            (r"[\u2018\u2019\u201c\u201d]", "'"),  # 统一引号
            (r"\ufeff", ""),  # 移除BOM头
            (r"[\u2022\u2023\u25e6\u2043]", ":"),  # 替换特殊符号
            (r"<[^>]*>", ""),  # 移除所有HTML标签
            (r"\s+", " "),  # 合并多个空白字符
        ]

        # 使用re_sub应用所有清理规则
        result = re_sub(html_content, clean_rules).strip()
        return result

    except re.error as e:
        error_msg = f"正则表达式错误:{str(e)}"
        print("处理失败", error_msg)
        raise ValueError(error_msg) from e
    except Exception as e:
        error_msg = f"HTML格式化失败:{str(e)}"
        print("处理失败", error_msg)
        raise RuntimeError(error_msg) from e


if __name__ == "__main__":

    def test_str_replace():
        replacement = "aaa-bbb-ccc"
        trims = [("a", "A"), ("b", "B"), ("c", "C")]
        print(str_replace(replacement, trims))

    # test_str_replace()

    def test_str_clean():
        test_str = "###Hello ?World"
        print(str_clean(test_str, ["#", "?"]))

    # test_str_clean()

    def test_Re_Sub():
        replacement = "This\n is \u2018a\u2019 test\ufeff string"
        trims = [("\n", ""), ("\u2018", "'"), ("\u2019", "'"), ("\ufeff", "")]
        print(re_sub(replacement, trims))

    # test_Re_Sub()

    def test_Re_Compile():
        replacement = "hello A and B"
        trims_list = [("A", "aaa"), ("B", "bbb")]
        print(re_compile(replacement, trims_list))

    # test_Re_Compile()
    # str2 = "Powe, on；the 2333, 。哈哈 ！！\U0001f914看看可以吗？一行代码就可以了！^_^"
    # print(remove_all_blank(str2, keep_blank=False))
    # print(remove_all_blank(str2, keep_blank=True))

    strr = """
    当前正值【母公司】新老主体切换的关键阶段，外部环境复杂敏感，各级政府部门及监管机构的调研、考察及访谈活动有所增加。为【确保在应对各类外部来访时】高效、规范、有序【响应】，切实维护【公司】形象，保障信息传递的准确性、一致性与及时性，【并严格落实重大事项报告制度】，现就加强母子公司信息协同管理工作提出如下要求：
一、 【严守报告制度，落实主体责任】
【各子公司须严格执行《君康人寿保险股份有限公司控股子公司管理暂行办法》等规章制度中关于重大事项报告的规定。】在经营管理及应对外部来访过程中，【凡涉及】需上报的重大事项，【各子公司】必须依照【既定】程序和时间要求，【第一时间】向【母公司】或相关管理部门进行【详尽、准确】的汇报【，确保重大信息及时上传】。此项要求是【有效协同应对】外部来访的【基础】。
二、 明确责任，快速响应
各子公司须高度重视外部来访事项，立即指定至少一名高管人员作为直接责任人，专项负责接收、处理各级政府及监管职能部门提出的调研、考察及访谈等请求。责任人在接到相关通知后，须立即响应，主动、全面掌握来访单位、人员、目的、时间、内容等详细信息，【并】严格执行重大事项报告制度，在第一时间将完整、准确的信息报送至【母公司】对口部门。
三、 信息协同，统一口径【，严守保密】
各子公司在应对外部要求前，必须与【母公司】相关主管部门进行充分沟通，严格按照【母公司】确认的统一口径、表述规范及注意事项进行回复。对于任何不确定或需进一步核实的信息，必须及时向【母公司】请示确认，不得擅自解释、发表意见或提供未经核实、批准的信息。所有对外提供的信息、数据及材料，须确保与【母公司】保持高度一致。【同时，必须严格执行信息保密及信息安全相关规定（详见附件1），并严守采访纪律（详见附件2）。】
四、 预案管理，妥善应对
各子公司应针对不同类型的调研、考察及访谈活动，提前制定应急预案。预案内容须涵盖接待流程、信息材料准备、舆情监测与应对措施等关键环节。各子公司应组织模拟演练，检验预案有效性，及时发现并整改潜在问题，提升应对突发情况的快速响应与专业处置能力，确保各类活动平稳有序进行。【预案制定与演练应充分考虑信息保密要求（附件1）及采访纪律规范（附件2）。】
各子公司必须严格贯彻落实本通知要求，将外部来访协同管理【及重大事项报告】视为当前一项关键任务，扎实细致地推进。务必确保【重大事项及时报告、】快速响应、信息高效协同、预案周全完备，以高度的责任心和卓越的执行力，【并严格遵守附件规定】，规范有序地应对各类外部挑战，坚决维护公司整体形象，保障公司全局利益。

附件：1. 关于再次重申加强信息保密及信息安全管理的通知
2. 关于严守采访纪律及加强信息保密管理的通知
    """
    # print(res := str_split_limited_list(strr), "\n", len(res))
    # print(res := str2list(strr), len(res))
    # print(random_char(20))
    import unittest

    class TestRandomChar(unittest.TestCase):
        def test_remove_whitespace(self):
            """测试移除多余空白字符"""
            html = "New\n\t\r  Sea"
            self.assertEqual(format_html_string(html), "New Sea")

        def test_remove_script_tags(self):
            """测试移除script标签"""
            html = "<script>alert(1)</script>Hello"
            self.assertEqual(format_html_string(html), "Hello")

        def test_remove_a_tags(self):
            """测试移除a标签"""
            html = "<a href='#'>Link</a>Text"
            self.assertEqual(format_html_string(html), "Text")

        def test_special_chars(self):
            """测试特殊字符替换"""
            html = "‘Hello’\u2022World\ufeff"
            self.assertEqual(format_html_string(html), "'Hello':World")

    unittest.main()
