# !/usr/bin/env python
"""
==============================================================
Description  : 头部注释
Develop      : VSCode
Author       : sandorn sandorn@live.cn
Date         : 2025-06-16 13:20:56
LastEditTime : 2025-06-16 14:11:31
FilePath     : /CODE/xjLib/xt_unicodedata.py
Github       : https://github.com/sandorn/home
==============================================================
"""

import re
import unicodedata


def analyze_character_properties(text):
    """分析文本中每个字符的基本属性"""
    analysis_results = []

    for char in text:
        char_info = {
            "character": char,
            "name": unicodedata.name(char, "UNKNOWN"),
            "category": unicodedata.category(char),
            "numeric_value": unicodedata.numeric(char, None),
            "decimal_value": unicodedata.decimal(char, None),
            "digit_value": unicodedata.digit(char, None),
        }
        analysis_results.append(char_info)

    return analysis_results


class UnicodeCharacterAnalyzer:
    """Unicode字符分析器"""

    def __init__(self):
        self.category_descriptions = {
            "Lu": "大写字母",
            "Ll": "小写字母",
            "Lt": "词首大写字母",
            "Lm": "修饰字母",
            "Lo": "其他字母",
            "Mn": "非空格标记",
            "Mc": "空格组合标记",
            "Me": "封闭标记",
            "Nd": "十进制数字",
            "Nl": "字母数字",
            "No": "其他数字",
            "Pc": "连接标点",
            "Pd": "横线标点",
            "Ps": "开放标点",
            "Pe": "关闭标点",
            "Pi": "初始标点",
            "Pf": "最终标点",
            "Po": "其他标点",
            "Sm": "数学符号",
            "Sc": "货币符号",
            "Sk": "修饰符号",
            "So": "其他符号",
            "Zs": "空格分隔符",
            "Zl": "行分隔符",
            "Zp": "段落分隔符",
            "Cc": "控制字符",
            "Cf": "格式字符",
            "Cs": "代理字符",
            "Co": "私用字符",
            "Cn": "未分配字符",
        }

    def categorize_text(self, text):
        """按类别统计文本中的字符"""
        category_counts = {}
        detailed_analysis = []

        for char in text:
            category = unicodedata.category(char)
            category_counts[category] = category_counts.get(category, 0) + 1

            detailed_analysis.append(
                {
                    "char": char,
                    "category": category,
                    "description": self.category_descriptions.get(category, "未知分类"),
                    "name": unicodedata.name(char, f"U+{ord(char):04X}"),
                }
            )

        return category_counts, detailed_analysis

    def filter_by_category(self, text, target_categories):
        """根据字符类别过滤文本"""
        filtered_chars = []
        for char in text:
            if unicodedata.category(char) in target_categories:
                filtered_chars.append(char)
        return "".join(filtered_chars)


class AdvancedTextCleaner:
    """高级文本清理器"""

    def __init__(self):
        self.unwanted_categories = ["Cc", "Cf", "Cs", "Co", "Cn"]  # 控制字符等

    def clean_and_normalize(
        self, text, normalize_form="NFKC", remove_accents=True, keep_only_ascii=False
    ):
        """全面的文本清理和规范化"""

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
        cleaned_text = self._normalize_whitespace(cleaned_text)

        return cleaned_text

    def _remove_unwanted_chars(self, text):
        """移除不需要的Unicode字符类别"""
        return "".join(
            char
            for char in text
            if unicodedata.category(char) not in self.unwanted_categories
        )

    def _remove_accents(self, text):
        """移除重音符号，保留基础字符"""
        # 先分解为基础字符和组合标记
        nfd_text = unicodedata.normalize("NFD", text)
        # 移除组合标记（重音符号等）
        without_accents = "".join(
            char for char in nfd_text if unicodedata.category(char) != "Mn"
        )
        # 重新组合
        return unicodedata.normalize("NFC", without_accents)

    def _keep_ascii_only(self, text):
        """只保留ASCII字符"""
        return "".join(char for char in text if ord(char) < 128)

    def _normalize_whitespace(self, text):
        """规范化空白字符"""
        # 将所有空白字符替换为普通空格，并去除多余空格
        return re.sub(r"\s+", " ", text).strip()

    def analyze_cleaning_impact(self, original_text, cleaned_text):
        """分析清理效果"""
        return {
            "original_length": len(original_text),
            "cleaned_length": len(cleaned_text),
            "removed_chars": len(original_text) - len(cleaned_text),
            "reduction_percentage": (
                (len(original_text) - len(cleaned_text)) / len(original_text) * 100
            )
            if original_text
            else 0,
            "original_bytes": len(original_text.encode("utf-8")),
            "cleaned_bytes": len(cleaned_text.encode("utf-8")),
        }


class TextNormalizer:
    """文本规范化处理器"""

    def __init__(self):
        self.normalization_forms = ["NFC", "NFD", "NFKC", "NFKD"]
        self.form_descriptions = {
            "NFC": "规范组合形式 (Canonical Composition)",
            "NFD": "规范分解形式 (Canonical Decomposition)",
            "NFKC": "兼容组合形式 (Compatibility Composition)",
            "NFKD": "兼容分解形式 (Compatibility Decomposition)",
        }

    def normalize_text(self, text, form="NFC"):
        """使用指定形式规范化文本"""
        if form not in self.normalization_forms:
            raise ValueError(f"不支持的规范化形式: {form}")

        return unicodedata.normalize(form, text)

    def compare_normalizations(self, text):
        """比较不同规范化形式的结果"""
        results = {}

        for form in self.normalization_forms:
            normalized = unicodedata.normalize(form, text)
            results[form] = {
                "text": normalized,
                "length": len(normalized),
                "bytes": len(normalized.encode("utf-8")),
                "description": self.form_descriptions[form],
            }

        return results

    def is_normalized(self, text, form="NFC"):
        """检查文本是否已经是指定的规范化形式"""
        normalized = unicodedata.normalize(form, text)
        return text == normalized


if __name__ == "__main__":
    # 使用高级文本清理器
    cleaner = AdvancedTextCleaner()

    # 测试各种复杂文本
    test_cases = [
        "  Héllo   Wörld!  \t\n  ",  # 重音符号和多余空白
        "café＃①②③",  # 混合字符
        "文件名：résumé.txt",  # 中英混合带重音
    ]

    for i, test_text in enumerate(test_cases, 1):
        print(f"\n=== 测试案例 {i} ===")
        print(f"原文: '{test_text}'")

        # 不同级别的清理
        basic_clean = cleaner.clean_and_normalize(test_text)
        no_accents = cleaner.clean_and_normalize(test_text, remove_accents=True)
        ascii_only = cleaner.clean_and_normalize(
            test_text, remove_accents=True, keep_only_ascii=True
        )

        print(f"基础清理: '{basic_clean}'")
        print(f"移除重音: '{no_accents}'")
        print(f"仅ASCII: '{ascii_only}'")

        # 分析清理效果
        impact = cleaner.analyze_cleaning_impact(test_text, ascii_only)
        print(
            f"清理效果: 字符减少 {impact['removed_chars']} 个 ({impact['reduction_percentage']:.1f}%)"
        )

    # 输出示例:
    # === 测试案例 1 ===
    # 原文: '  Héllo   Wörld!
    #   '
    # 基础清理: 'Héllo Wörld!'
    # 移除重音: 'Hello World!'
    # 仅ASCII: 'Hello World!'
    # 清理效果: 字符减少 12 个 (60.0%)

    # 测试文本规范化
    normalizer = TextNormalizer()

    # 包含组合字符的测试文本
    test_strings = [
        "café",  # e + 组合重音符
        "café",  # 预组合的é
        "①②③",  # 圆圈数字
        "ﬁle",  # 连字符
    ]

    for test_str in test_strings:
        print(f"\n原始文本: '{test_str}' (长度: {len(test_str)})")

        comparison = normalizer.compare_normalizations(test_str)

        for form, result in comparison.items():
            equal_mark = "✓" if result["text"] == test_str else "✗"
            print(
                f"  {form}: '{result['text']}' (长度: {result['length']}, 字节: {result['bytes']}) {equal_mark}"
            )

    # 输出示例:
    # 原始文本: 'café' (长度: 4)
    #   NFC: 'café' (长度: 4, 字节: 5) ✓
    #   NFD: 'café' (长度: 5, 字节: 6) ✗
    #   NFKC: 'café' (长度: 4, 字节: 5) ✓
    #   NFKD: 'café' (长度: 5, 字节: 6) ✗
    # 测试不同类型的字符
    test_text = "Hello世界123！"
    results = analyze_character_properties(test_text)

    for result in results:
        print(f"字符: '{result['character']}' - 名称: {result['name']}")
        print(f"  分类: {result['category']}")
        if result["numeric_value"] is not None:
            print(f"  数值: {result['numeric_value']}")
        print("---")

    # 输出示例:
    # 字符: 'H' - 名称: LATIN CAPITAL LETTER H
    #   分类: Lu
    # ---
    # 字符: '世' - 名称: CJK UNIFIED IDEOGRAPH-4E16
    #   分类: Lo
    # ---
    # 字符: '1' - 名称: DIGIT ONE
    #   分类: Nd
    #   数值: 1.0
    # 使用字符分析器
    analyzer = UnicodeCharacterAnalyzer()

    sample_text = "Hello, 世界！123 $100 α+β=γ 🚀"
    category_counts, detailed_info = analyzer.categorize_text(sample_text)

    print("字符分类统计:")
    for category, count in sorted(category_counts.items()):
        description = analyzer.category_descriptions.get(category, "未知")
        print(f"  {category} ({description}): {count}个")

    print("\n仅保留字母和数字:")
    letters_and_digits = analyzer.filter_by_category(
        sample_text, ["Lu", "Ll", "Lo", "Nd"]
    )
    print(f"原文: {sample_text}")
    print(f"过滤后: {letters_and_digits}")

    # 输出示例:
    # 字符分类统计:
    #   Ll (小写字母): 4个
    #   Lo (其他字母): 2个
    #   Lu (大写字母): 1个
    #   Nd (十进制数字): 3个
    #   Po (其他标点): 2个
    #   ...
    #
    # 仅保留字母和数字:
    # 原文: Hello, 世界！123 $100 α+β=γ 🚀
    # 过滤后: Hello世界123100αβγ