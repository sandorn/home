# !/usr/bin/env python
"""
==============================================================
Description  : Unicode工具模块 - 精确处理 Unicode 文本,提供Unicode字符分析、文本规范化和清理功能
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-06-16 13:20:56
LastEditTime : 2025-09-17 14:30:00
FilePath     : /CODE/xjlib/xt_utils/unicode.py
Github       : https://github.com/sandorn/home

本模块提供以下核心功能:
- Unicode字符属性分析与分类
- 文本规范化处理(NFC、NFD、NFKC、NFKD)
- 高级文本清理功能(控制字符移除、重音符号处理、ASCII转换)
- 字符类别过滤

主要特性:
- 全面的Unicode字符属性查询(名称、类别、数值等)
- 支持多种Unicode规范化形式比较
- 细粒度的文本清理控制选项
- 清理效果分析和统计
- 完整的类型注解支持
- 与xjlib其他模块一致的API设计和文档风格
==============================================================
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from typing import Any, TypeVar

T = TypeVar('T')


def analyze_character_properties(text: str) -> list[dict[str, Any]]:
    """
    分析文本中每个字符的基本Unicode属性

    Args:
        text: 要分析的文本字符串

    Returns:
        List[Dict[str, Any]]: 包含每个字符属性信息的字典列表
            - character: 原始字符
            - name: Unicode字符名称
            - category: Unicode字符分类
            - numeric_value: 数字值(如果适用)
            - decimal_value: 十进制值(如果适用)
            - digit_value: 数字值(如果适用)

    Example:
        >>> results = analyze_character_properties('Hello123')
        >>> for result in results:
        >>>     print(f"字符: '{result['character']}' - 名称: {result['name']} - 分类: {result['category']}")
    """
    analysis_results: list[dict[str, Any]] = []

    for char in text:
        char_info = {
            'character': char,
            'name': unicodedata.name(char, 'UNKNOWN'),
            'category': unicodedata.category(char),
            'numeric_value': unicodedata.numeric(char, None),
            'decimal_value': unicodedata.decimal(char, None),
            'digit_value': unicodedata.digit(char, None),
        }
        analysis_results.append(char_info)

    return analysis_results


class UnicodeCharacterAnalyzer:
    """Unicode字符分析器 - 提供字符分类统计和过滤功能"""

    def __init__(self) -> None:
        """初始化字符分析器，加载Unicode字符分类描述映射"""
        self.category_descriptions: Mapping[str, str] = {
            'Lu': '大写字母',
            'Ll': '小写字母',
            'Lt': '词首大写字母',
            'Lm': '修饰字母',
            'Lo': '其他字母',
            'Mn': '非空格标记',
            'Mc': '空格组合标记',
            'Me': '封闭标记',
            'Nd': '十进制数字',
            'Nl': '字母数字',
            'No': '其他数字',
            'Pc': '连接标点',
            'Pd': '横线标点',
            'Ps': '开放标点',
            'Pe': '关闭标点',
            'Pi': '初始标点',
            'Pf': '最终标点',
            'Po': '其他标点',
            'Sm': '数学符号',
            'Sc': '货币符号',
            'Sk': '修饰符号',
            'So': '其他符号',
            'Zs': '空格分隔符',
            'Zl': '行分隔符',
            'Zp': '段落分隔符',
            'Cc': '控制字符',
            'Cf': '格式字符',
            'Cs': '代理字符',
            'Co': '私用字符',
            'Cn': '未分配字符',
        }

    def categorize_text(self, text: str) -> tuple[dict[str, int], list[dict[str, str]]]:
        """
        按Unicode类别统计文本中的字符分布并提供详细分析

        Args:
            text: 要分类的文本字符串

        Returns:
            Tuple[Dict[str, int], List[Dict[str, str]]]:
                - 第一个元素: 字符类别到出现次数的映射
                - 第二个元素: 每个字符的详细分析信息列表

        Example:
            >>> analyzer = UnicodeCharacterAnalyzer()
            >>> category_counts, detailed_info = analyzer.categorize_text('Hello, 世界！123')
            >>> # 输出类别统计
            >>> for category, count in sorted(category_counts.items()):
            >>>     print(f"类别 {category}: {count}个字符")
        """
        category_counts: dict[str, int] = {}
        detailed_analysis: list[dict[str, str]] = []

        for char in text:
            category = unicodedata.category(char)
            category_counts[category] = category_counts.get(category, 0) + 1

            detailed_analysis.append({
                'char': char,
                'category': category,
                'description': self.category_descriptions.get(category, '未知分类'),
                'name': unicodedata.name(char, f'U+{ord(char):04X}'),
            })

        return category_counts, detailed_analysis

    def filter_by_category(self, text: str, target_categories: list[str]) -> str:
        """
        根据Unicode字符类别过滤文本，只保留指定类别的字符

        Args:
            text: 要过滤的文本字符串
            target_categories: 要保留的字符类别列表

        Returns:
            str: 过滤后的文本字符串

        Example:
            >>> analyzer = UnicodeCharacterAnalyzer()
            >>> # 只保留字母和数字
            >>> filtered_text = analyzer.filter_by_category('Hello, 世界！123', ['Lu', 'Ll', 'Lo', 'Nd'])
            >>> print(filtered_text)  # 输出: Hello世界123
        """
        filtered_chars: list[str] = []
        for char in text:
            if unicodedata.category(char) in target_categories:
                filtered_chars.append(char)
        return ''.join(filtered_chars)


class AdvancedTextCleaner:
    """高级文本清理器 - 提供全面的文本规范化和清理功能"""

    def __init__(self) -> None:
        """初始化文本清理器，设置默认清理参数"""
        self.unwanted_categories: list[str] = ['Cc', 'Cf', 'Cs', 'Co', 'Cn']  # 控制字符等

    def clean_and_normalize(
        self,
        text: str,
        normalize_form: str = 'NFKC',
        remove_accents: bool = True,
        keep_only_ascii: bool = False,
    ) -> str:
        """
        全面的文本清理和规范化处理

        Args:
            text: 要清理的文本字符串
            normalize_form: Unicode规范化形式(NFC、NFD、NFKC、NFKD)
            remove_accents: 是否移除重音符号
            keep_only_ascii: 是否只保留ASCII字符

        Returns:
            str: 清理后的文本字符串

        Example:
            >>> cleaner = AdvancedTextCleaner()
            >>> text = '  Héllo   Wörld!  \t\n  '
            >>> # 基础清理
            >>> basic_clean = cleaner.clean_and_normalize(text)
            >>> # 移除重音
            >>> no_accents = cleaner.clean_and_normalize(text, remove_accents=True)
            >>> # 仅保留ASCII
            >>> ascii_only = cleaner.clean_and_normalize(text, keep_only_ascii=True)
        """
        # 1. Unicode规范化
        cleaned_text = unicodedata.normalize(normalize_form, text)

        # 2. 移除不需要的控制字符
        cleaned_text = self._remove_unwanted_chars(cleaned_text)

        # 3. 可选：移除重音符号
        if remove_accents:
            cleaned_text = self._remove_accents(cleaned_text)

        # 4. 可选：只保留ASCII字符
        if keep_only_ascii:
            cleaned_text = self._keep_ascii_only(cleaned_text)

        # 5. 规范化空白字符
        return self._normalize_whitespace(cleaned_text)

    def _remove_unwanted_chars(self, text: str) -> str:
        """移除不需要的Unicode字符类别(内部方法)"""
        return ''.join(char for char in text if unicodedata.category(char) not in self.unwanted_categories)

    def _remove_accents(self, text: str) -> str:
        """移除重音符号，保留基础字符(内部方法)"""
        # 先分解为基础字符和组合标记
        nfd_text = unicodedata.normalize('NFD', text)
        # 移除组合标记（重音符号等）
        without_accents = ''.join(char for char in nfd_text if unicodedata.category(char) != 'Mn')
        # 重新组合
        return unicodedata.normalize('NFC', without_accents)

    def _keep_ascii_only(self, text: str) -> str:
        """只保留ASCII字符(内部方法)"""
        return ''.join(char for char in text if ord(char) < 128)

    def _normalize_whitespace(self, text: str) -> str:
        """规范化空白字符(内部方法)"""
        # 将所有空白字符替换为普通空格，并去除多余空格
        return re.sub(r'\s+', ' ', text).strip()

    def analyze_cleaning_impact(self, original_text: str, cleaned_text: str) -> dict[str, int | float]:
        """
        分析文本清理的效果和影响

        Args:
            original_text: 原始文本
            cleaned_text: 清理后的文本

        Returns:
            Dict[str, Union[int, float]]: 包含清理效果统计的字典
                - original_length: 原始字符长度
                - cleaned_length: 清理后字符长度
                - removed_chars: 移除的字符数量
                - reduction_percentage: 字符减少百分比
                - original_bytes: 原始字节大小
                - cleaned_bytes: 清理后字节大小

        Example:
            >>> cleaner = AdvancedTextCleaner()
            >>> original = '  Héllo   Wörld!  \t\n  '
            >>> cleaned = cleaner.clean_and_normalize(original)
            >>> impact = cleaner.analyze_cleaning_impact(original, cleaned)
            >>> print(f'字符减少: {impact["removed_chars"]}个 ({impact["reduction_percentage"]:.1f}%)')
        """
        original_len = len(original_text)
        return {
            'original_length': original_len,
            'cleaned_length': len(cleaned_text),
            'removed_chars': original_len - len(cleaned_text),
            'reduction_percentage': ((original_len - len(cleaned_text)) / original_len * 100) if original_len else 0,
            'original_bytes': len(original_text.encode('utf-8')),
            'cleaned_bytes': len(cleaned_text.encode('utf-8')),
        }


class TextNormalizer:
    """文本规范化处理器 - 提供Unicode规范化和比较功能"""

    def __init__(self) -> None:
        """初始化文本规范化器，设置支持的规范化形式"""
        self.normalization_forms: list[str] = ['NFC', 'NFD', 'NFKC', 'NFKD']
        self.form_descriptions: Mapping[str, str] = {
            'NFC': '规范组合形式 (Canonical Composition)',
            'NFD': '规范分解形式 (Canonical Decomposition)',
            'NFKC': '兼容组合形式 (Compatibility Composition)',
            'NFKD': '兼容分解形式 (Compatibility Decomposition)',
        }

    def normalize_text(self, text: str, form: str = 'NFC') -> str:
        """
        使用指定的Unicode规范化形式处理文本

        Args:
            text: 要规范化的文本
            form: 规范化形式(NFC、NFD、NFKC、NFKD)

        Returns:
            str: 规范化后的文本

        Raises:
            ValueError: 当指定了不支持的规范化形式时

        Example:
            >>> normalizer = TextNormalizer()
            >>> text = 'café'  # 预组合的é
            >>> normalized = normalizer.normalize_text(text, form='NFD')
        """
        if form not in self.normalization_forms:
            raise ValueError(f'不支持的规范化形式: {form}')

        return unicodedata.normalize(form, text)

    def compare_normalizations(self, text: str) -> dict[str, dict[str, str | int]]:
        """
        比较不同Unicode规范化形式对文本的影响

        Args:
            text: 要比较的文本

        Returns:
            Dict[str, Dict[str, Union[str, int]]]: 不同规范化形式的结果比较
                - 键: 规范化形式(NFC、NFD、NFKC、NFKD)
                - 值: 包含规范化后文本、长度、字节数和描述的字典

        Example:
            >>> normalizer = TextNormalizer()
            >>> comparisons = normalizer.compare_normalizations('café')
            >>> for form, result in comparisons.items():
            >>>     print(f"{form}: 长度={result['length']}, 字节数={result['bytes']}")
        """
        results: dict[str, dict[str, str | int]] = {}

        for form in self.normalization_forms:
            normalized = unicodedata.normalize(form, text)
            results[form] = {
                'text': normalized,
                'length': len(normalized),
                'bytes': len(normalized.encode('utf-8')),
                'description': self.form_descriptions[form],
            }

        return results

    def is_normalized(self, text: str, form: str = 'NFC') -> bool:
        """
        检查文本是否已经是指定的Unicode规范化形式

        Args:
            text: 要检查的文本
            form: 规范化形式(NFC、NFD、NFKC、NFKD)

        Returns:
            bool: 如果文本已经是指定的规范化形式则返回True

        Example:
            >>> normalizer = TextNormalizer()
            >>> text = 'café'  # 预组合的é
            >>> is_normal = normalizer.is_normalized(text, form='NFC')  # 返回True
        """
        normalized = unicodedata.normalize(form, text)
        return text == normalized


# 创建全局实例，方便直接使用
unicode_analyzer = UnicodeCharacterAnalyzer()
text_cleaner = AdvancedTextCleaner()
text_normalizer = TextNormalizer()


def get_character_name(char: str, default: str = 'UNKNOWN') -> str:
    """
    获取单个字符的Unicode名称

    Args:
        char: 要查询的字符
        default: 无法获取名称时的默认值

    Returns:
        str: Unicode字符名称或默认值

    Example:
        >>> get_character_name('A')  # 返回: 'LATIN CAPITAL LETTER A'
        >>> get_character_name('世')  # 返回: 'CJK UNIFIED IDEOGRAPH-4E16'
    """
    return unicodedata.name(char, default)


def get_character_category(char: str) -> str:
    """
    获取单个字符的Unicode类别

    Args:
        char: 要查询的字符

    Returns:
        str: Unicode字符类别代码

    Example:
        >>> get_character_category('A')  # 返回: 'Lu'
        >>> get_character_category('1')  # 返回: 'Nd'
    """
    return unicodedata.category(char)


def get_category_description(category: str) -> str:
    """
    获取Unicode字符类别的中文描述

    Args:
        category: Unicode字符类别代码

    Returns:
        str: 类别描述文本

    Example:
        >>> get_category_description('Lu')  # 返回: '大写字母'
        >>> get_category_description('Nd')  # 返回: '十进制数字'
    """
    analyzer = UnicodeCharacterAnalyzer()
    return analyzer.category_descriptions.get(category, '未知分类')


def is_control_character(char: str) -> bool:
    """
    检查字符是否为控制字符

    Args:
        char: 要检查的字符

    Returns:
        bool: 如果是控制字符则返回True

    Example:
        >>> is_control_character('\n')  # 返回: True
        >>> is_control_character('A')  # 返回: False
    """
    return unicodedata.category(char).startswith('C')


def normalize_whitespace(text: str) -> str:
    """
    规范化文本中的空白字符

    Args:
        text: 要处理的文本

    Returns:
        str: 规范化后的文本

    Example:
        >>> normalize_whitespace('  Hello   \t\nWorld  ')  # 返回: 'Hello World'
    """
    return re.sub(r'\s+', ' ', text).strip()


if __name__ == '__main__':
    # 使用高级文本清理器
    cleaner = AdvancedTextCleaner()

    # 测试各种复杂文本
    test_cases = [
        '  Héllo   Wörld!  \t\n  ',  # 重音符号和多余空白
        'café＃①②③',  # 混合字符
        '文件名：résumé.txt',  # 中英混合带重音
    ]

    for i, test_text in enumerate(test_cases, 1):
        print(f'\n=== 测试案例 {i} ===')
        print(f"原文: '{test_text}'")

        # 不同级别的清理
        basic_clean = cleaner.clean_and_normalize(test_text)
        no_accents = cleaner.clean_and_normalize(test_text, remove_accents=True)
        ascii_only = cleaner.clean_and_normalize(test_text, remove_accents=True, keep_only_ascii=True)

        print(f"基础清理: '{basic_clean}'")
        print(f"移除重音: '{no_accents}'")
        print(f"仅ASCII: '{ascii_only}'")

        # 分析清理效果
        impact = cleaner.analyze_cleaning_impact(test_text, ascii_only)
        print(f'清理效果: 字符减少 {impact["removed_chars"]} 个 ({impact["reduction_percentage"]:.1f}%)')

    # 测试文本规范化
    normalizer = TextNormalizer()

    # 包含组合字符的测试文本
    test_strings = [
        'café',  # e + 组合重音符
        'café',  # 预组合的é
        '①②③',  # 圆圈数字
        'ﬁle',  # 连字符
    ]

    for test_str in test_strings:
        print(f"\n原始文本: '{test_str}' (长度: {len(test_str)})")

        comparison = normalizer.compare_normalizations(test_str)

        for form, result in comparison.items():
            equal_mark = '✓' if result['text'] == test_str else '✗'
            print(f"  {form}: '{result['text']}' (长度: {result['length']}, 字节: {result['bytes']}) {equal_mark}")

    # 测试不同类型的字符
    test_text = 'Hello世界123！'
    results = analyze_character_properties(test_text)

    for result in results:
        print(f"字符: '{result['character']}' - 名称: {result['name']}")
        print(f'  分类: {result["category"]}')
        if result['numeric_value'] is not None:
            print(f'  数值: {result["numeric_value"]}')
        print('---')

    # 使用字符分析器
    analyzer = UnicodeCharacterAnalyzer()

    sample_text = 'Hello, 世界！123 $100 α+β=γ 🚀'
    category_counts, detailed_info = analyzer.categorize_text(sample_text)

    print('字符分类统计:')
    for category, count in sorted(category_counts.items()):
        description = analyzer.category_descriptions.get(category, '未知')
        print(f'  {category} ({description}): {count}个')

    print('\n仅保留字母和数字:')
    letters_and_digits = analyzer.filter_by_category(sample_text, ['Lu', 'Ll', 'Lo', 'Nd'])
    print(f'原文: {sample_text}')
    print(f'过滤后: {letters_and_digits}')
