#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""类型检查脚本 - 验证aiomysqlpool.py的类型注解是否符合Python 3.10+语法规范"""

import ast
import sys
import os
from typing import Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_type_annotations(file_path: str) -> dict[str, list[str]]:
    """检查文件中的类型注解是否符合Python 3.10+语法规范"""
    results = {
        'valid': [],
        'invalid': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用AST解析文件
        tree = ast.parse(content, filename=file_path)
        
        # 检查import语句
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == 'typing':
                    for name in node.names:
                        if name.name in ['List', 'Dict', 'Union', 'Optional']:
                            results['invalid'].append(
                                f"使用了过时的typing类型: {name.name} (第{node.lineno}行)"
                            )
                        else:
                            results['valid'].append(f"导入了允许的typing类型: {name.name}")
        
        # 检查函数定义中的类型注解
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                check_function_annotations(node, results)
            elif isinstance(node, ast.ClassDef):
                for method in node.body:
                    if isinstance(method, ast.FunctionDef):
                        check_function_annotations(method, results)
    except Exception as e:
        results['invalid'].append(f"解析文件时出错: {str(e)}")
    
    return results

def check_function_annotations(node: ast.FunctionDef, results: dict[str, list[str]]):
    """检查函数定义中的类型注解"""
    func_name = node.name
    lineno = node.lineno
    
    # 检查返回值类型注解
    if hasattr(node, 'returns') and node.returns:
        returns_str = ast.unparse(node.returns).strip()
        if any(t in returns_str for t in ['List[', 'Dict[', 'Union[', 'Optional[']):
            results['invalid'].append(
                f"函数 {func_name} 的返回值使用了过时的类型注解: {returns_str} (第{lineno}行)"
            )
        else:
            results['valid'].append(f"函数 {func_name} 的返回值类型注解符合规范: {returns_str}")
    
    # 检查参数类型注解
    for arg in node.args.args:
        if hasattr(arg, 'annotation') and arg.annotation:
            arg_name = arg.arg
            annotation_str = ast.unparse(arg.annotation).strip()
            if any(t in annotation_str for t in ['List[', 'Dict[', 'Union[', 'Optional[']):
                results['invalid'].append(
                    f"函数 {func_name} 的参数 {arg_name} 使用了过时的类型注解: {annotation_str} (第{lineno}行)"
                )
            else:
                results['valid'].append(f"函数 {func_name} 的参数 {arg_name} 类型注解符合规范: {annotation_str}")

def print_results(results: dict[str, list[str]]):
    """打印检查结果"""
    print("\n类型注解检查结果:")
    print("==================")
    
    # 打印有效结果
    if results['valid']:
        print(f"✓ 符合规范的类型注解 ({len(results['valid'])}项):")
        for item in results['valid']:
            print(f"  - {item}")
    
    # 打印无效结果
    if results['invalid']:
        print(f"✗ 不符合规范的类型注解 ({len(results['invalid'])}项):")
        for item in results['invalid']:
            print(f"  - {item}")
    
    if not results['invalid']:
        print("\n🎉 所有类型注解均符合Python 3.10+语法规范！")
    else:
        print("\n⚠️ 发现不符合规范的类型注解，请进行修正。")

def main():
    """主函数"""
    file_path = os.path.join(
        'd:\\CODE',
        'xjlib', 'xt_database', 'aiomysqlpool.py'
    )
    
    print(f"检查文件: {file_path}")
    print(f"Python版本: {sys.version}")
    
    results = check_type_annotations(file_path)
    print_results(results)
    
    # 尝试直接导入模块验证
    try:
        print("\n尝试直接导入模块验证...")
        from xjlib.xt_database import aiomysqlpool
        print("✅ 模块导入成功！")
    except ImportError as e:
        print(f"❌ 模块导入失败: {str(e)}")
    
    # 返回退出码
    sys.exit(0 if not results['invalid'] else 1)

if __name__ == '__main__':
    main()