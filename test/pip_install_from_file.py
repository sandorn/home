# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pip安装脚本

读取c:\r.txt文件中的每一行包名，使用pip install逐行安装
支持包名带版本号，如：requests==2.28.1
"""

import subprocess
import sys
from typing import List


def read_package_list(file_path: str) -> List[str]:
    """读取包列表文件

    Args:
        file_path: 包含包名的文件路径

    Returns:
        包名列表

    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取文件失败
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # 读取所有行，去除空行和注释行，并去除前后空白
            packages = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#")
            ]
        return packages
    except FileNotFoundError:
        raise FileNotFoundError(f"包列表文件不存在: {file_path}")
    except IOError as e:
        raise IOError(f"读取文件失败: {file_path}, 错误: {e}")


def install_package(package: str) -> bool:
    """安装单个包

    Args:
        package: 包名，可带版本号

    Returns:
        是否安装成功
    """
    try:
        print(f"正在安装: {package}...")
        # 执行pip install命令
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            print(f"✓ 安装成功: {package}")
            return True
        else:
            print(f"✗ 安装失败: {package}")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 安装过程异常: {package}")
        print(f"异常信息: {str(e)}")
        return False


def batch_install_packages(packages: List[str]) -> dict:
    """批量安装包

    Args:
        packages: 包名列表

    Returns:
        安装结果统计
    """
    total = len(packages)
    success_count = 0
    failed_packages = []

    print(f"共发现 {total} 个包需要安装\n")

    for i, package in enumerate(packages, 1):
        print(f"[{i}/{total}]")
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
        print("-" * 50)

    return {
        "total": total,
        "success": success_count,
        "failed": len(failed_packages),
        "failed_packages": failed_packages,
    }


def main() -> None:
    """主函数"""
    file_path = "c:\\r.txt"

    try:
        print("===== pip安装脚本 =====")
        print(f"读取包列表文件: {file_path}")

        # 读取包列表
        packages = read_package_list(file_path)

        # 批量安装包
        if packages:
            result = batch_install_packages(packages)

            # 输出安装结果统计
            print("\n===== 安装结果统计 =====")
            print(f"总包数: {result['total']}")
            print(f"成功安装: {result['success']}")
            print(f"安装失败: {result['failed']}")

            if result["failed_packages"]:
                print("\n安装失败的包:")
                for package in result["failed_packages"]:
                    print(f"- {package}")
        else:
            print("未找到需要安装的包")

    except Exception as e:
        print(f"脚本执行失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
