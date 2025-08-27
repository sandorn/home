import os

from bs4 import BeautifulSoup


def remove_duplicates(html_file):
    # 读取HTML文件
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # 统计原始书签数量
    original_count = len(soup.find_all("a"))

    # 去重处理
    seen_links = set()
    duplicates_removed = 0

    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href in seen_links:
            tag.decompose()  # 删除重复项
            duplicates_removed += 1
        else:
            seen_links.add(href)

    # 保存去重后的文件
    output_file = html_file.replace(".html", "_cleaned.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print("去重完成！")
    print(f"原始书签数量: {original_count}")
    print(f"移除重复数: {duplicates_removed}")
    print(f"剩余书签数: {original_count - duplicates_removed}")
    print(f"已保存到: {output_file}")


if __name__ == "__main__":
    # 直接指定文件路径
    file_path = r"C:\Users\Administrator\Desktop\bookmarks_2025_8_26.html"

    # 检查文件是否存在
    if os.path.exists(file_path):
        remove_duplicates(file_path)
    else:
        print(f"错误: 文件 '{file_path}' 不存在")
