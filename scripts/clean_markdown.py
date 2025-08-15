#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用Markdown文档行号范围编辑工具
支持删除指定行号范围的内容，或替换为新内容
"""

import argparse
import os
import sys
from typing import List


def read_file_utf8(file_path: str) -> List[str]:
    """读取UTF-8编码的文件，返回行列表"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"错误: 文件不存在 '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"错误: 无法以UTF-8编码读取文件 '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件失败 - {e}", file=sys.stderr)
        sys.exit(1)


def write_file_utf8(file_path: str, lines: List[str]) -> bool:
    """写入UTF-8编码的文件"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return True
    except Exception as e:
        print(f"错误: 写入文件失败 - {e}", file=sys.stderr)
        return False


def create_backup(file_path: str) -> str:
    """创建文件备份"""
    import time

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"

    try:
        import shutil

        shutil.copy2(file_path, backup_path)
        print(f"✓ 已创建备份: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"警告: 创建备份失败 - {e}", file=sys.stderr)
        return ""


def validate_line_numbers(start_line: int, end_line: int, total_lines: int) -> bool:
    """验证行号的有效性"""
    if start_line < 1 or start_line > total_lines:
        print(
            f"错误: 起始行号 {start_line} 超出文件范围 (1-{total_lines})",
            file=sys.stderr,
        )
        return False

    if end_line < 1 or end_line > total_lines:
        print(
            f"错误: 结束行号 {end_line} 超出文件范围 (1-{total_lines})", file=sys.stderr
        )
        return False

    if start_line > end_line:
        print(
            f"错误: 起始行号 {start_line} 不能大于结束行号 {end_line}", file=sys.stderr
        )
        return False

    return True


def process_file(
    file_path: str,
    start_line: int,
    end_line: int,
    replacement: str = None,
    backup: bool = False,
) -> None:
    """处理文件的主函数"""
    # 读取文件
    lines = read_file_utf8(file_path)
    total_lines = len(lines)

    print(f"文件总行数: {total_lines}")

    # 验证行号
    if not validate_line_numbers(start_line, end_line, total_lines):
        sys.exit(1)

    # 创建备份（如果用户要求备份）
    if backup:
        create_backup(file_path)

    # 显示将要操作的内容
    print(f"\n将要操作的内容 (行 {start_line} 到 {end_line}):")
    print("-" * 50)
    for i in range(start_line - 1, end_line):
        print(f"{i + 1:4d}: {lines[i].rstrip()}")
    print("-" * 50)

    # 执行操作
    if replacement is not None:
        # 替换操作
        print(f"\n替换为:")
        print(f'"{replacement}"')

        # 保留起始行前的内容
        new_lines = lines[: start_line - 1]

        # 添加替换内容（如果不是空字符串）
        if replacement:
            # 确保替换内容以换行符结尾
            if not replacement.endswith("\n"):
                replacement += "\n"
            new_lines.append(replacement)

        # 添加结束行后的内容
        new_lines.extend(lines[end_line:])

    else:
        # 删除操作
        print(f"\n删除行 {start_line} 到 {end_line}")

        # 删除指定范围的行
        new_lines = lines[: start_line - 1] + lines[end_line:]

    # 写入文件
    if write_file_utf8(file_path, new_lines):
        print(f"\n✓ 操作完成!")
        print(f"文件行数变化: {total_lines} → {len(new_lines)}")
        if replacement is not None:
            print(f"操作类型: 替换 (行 {start_line}-{end_line})")
        else:
            print(f"操作类型: 删除 (行 {start_line}-{end_line})")
    else:
        print("\n✗ 操作失败!")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="通用Markdown文档行号范围编辑工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 删除第10到20行
  python clean_markdown.py file.md 10 20
  
  # 将第5到8行替换为新内容
  python clean_markdown.py file.md 5 8 --replace "# 新标题\\n\\n新内容\\n"
  
  # 删除第15行（单行）
  python clean_markdown.py file.md 15 15
  
  # 替换第3行为空（相当于删除）
  python clean_markdown.py file.md 3 3 --replace ""
  
  # 创建备份文件
  python clean_markdown.py file.md 10 20 --backup

注意:
  - 行号从1开始计算
  - 自动使用UTF-8编码处理文件
  - 默认不创建备份文件，使用--backup参数创建备份
  - 替换内容中的\\n会被转换为实际换行符
        """,
    )

    # 必选参数
    parser.add_argument("file", help="要编辑的Markdown文件路径")
    parser.add_argument("start_line", type=int, help="起始行号 (从1开始)")
    parser.add_argument("end_line", type=int, help="结束行号 (包含)")

    # 可选参数
    parser.add_argument(
        "-r",
        "--replace",
        type=str,
        help="替换内容 (用引号包裹)。如果不提供此参数，则删除指定行",
    )
    parser.add_argument("--backup", action="store_true", help="创建备份文件")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")

    # 解析参数
    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.file):
        print(f"错误: 文件不存在 '{args.file}'", file=sys.stderr)
        sys.exit(1)

    # 处理替换内容中的转义字符
    replacement = None
    if args.replace is not None:
        replacement = args.replace.replace("\\n", "\n").replace("\\t", "\t")

    # 执行操作
    try:
        process_file(
            args.file, args.start_line, args.end_line, replacement, args.backup
        )
    except KeyboardInterrupt:
        print("\n操作被用户取消", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
