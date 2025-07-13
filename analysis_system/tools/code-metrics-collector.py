#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码指标收集工具

用于自动收集Python项目的基础代码指标

使用方法:
python code-metrics-collector.py --project-path /path/to/project --output metrics.json
"""

import os
import ast
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class FileMetrics:
    """单个文件的指标"""

    file_path: str
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    function_count: int
    class_count: int
    import_count: int
    max_complexity: int
    avg_complexity: float


@dataclass
class ProjectMetrics:
    """项目整体指标"""

    project_path: str
    total_files: int
    python_files: int
    total_lines: int
    code_lines: int
    blank_lines: int
    comment_lines: int
    total_functions: int
    total_classes: int
    total_imports: int
    avg_file_length: float
    max_file_length: int
    complexity_distribution: Dict[str, int]


class ComplexityAnalyzer(ast.NodeVisitor):
    """计算圈复杂度的AST访问器"""

    def __init__(self):
        self.complexity = 1  # 基础复杂度为1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)


class CodeMetricsCollector:
    """代码指标收集器"""

    def __init__(self):
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def analyze_file(self, file_path: Path) -> Optional[FileMetrics]:
        """分析单个Python文件"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            lines = content.split("\n")
            total_lines = len(lines)

            # 统计代码行、空行、注释行
            code_lines = 0
            blank_lines = 0
            comment_lines = 0

            for line in lines:
                stripped = line.strip()
                if not stripped:
                    blank_lines += 1
                elif stripped.startswith("#"):
                    comment_lines += 1
                else:
                    code_lines += 1

            # 解析AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                self.logger.warning(f"语法错误 {file_path}: {e}")
                return None

            # 统计函数、类、导入
            function_count = 0
            class_count = 0
            import_count = 0
            complexities = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_count += 1
                    # 计算函数复杂度
                    analyzer = ComplexityAnalyzer()
                    analyzer.visit(node)
                    complexities.append(analyzer.complexity)
                elif isinstance(node, ast.ClassDef):
                    class_count += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_count += 1

            # 计算复杂度统计
            max_complexity = max(complexities) if complexities else 0
            avg_complexity = (
                sum(complexities) / len(complexities) if complexities else 0
            )

            return FileMetrics(
                file_path=str(file_path),
                lines_of_code=code_lines,
                blank_lines=blank_lines,
                comment_lines=comment_lines,
                function_count=function_count,
                class_count=class_count,
                import_count=import_count,
                max_complexity=max_complexity,
                avg_complexity=avg_complexity,
            )

        except Exception as e:
            self.logger.error(f"分析文件失败 {file_path}: {e}")
            return None

    def collect_project_metrics(self, project_path: Path) -> ProjectMetrics:
        """收集项目级别的指标"""
        python_files = []

        # 查找所有Python文件
        for py_file in project_path.rglob("*.py"):
            if not any(part.startswith(".") for part in py_file.parts):
                python_files.append(py_file)

        self.logger.info(f"找到 {len(python_files)} 个Python文件")

        # 分析每个文件
        file_metrics = []
        for py_file in python_files:
            metrics = self.analyze_file(py_file)
            if metrics:
                file_metrics.append(metrics)

        # 计算项目级别指标
        total_files = len(file_metrics)
        total_lines = sum(
            m.lines_of_code + m.blank_lines + m.comment_lines for m in file_metrics
        )
        code_lines = sum(m.lines_of_code for m in file_metrics)
        blank_lines = sum(m.blank_lines for m in file_metrics)
        comment_lines = sum(m.comment_lines for m in file_metrics)
        total_functions = sum(m.function_count for m in file_metrics)
        total_classes = sum(m.class_count for m in file_metrics)
        total_imports = sum(m.import_count for m in file_metrics)

        # 计算平均值
        avg_file_length = total_lines / total_files if total_files > 0 else 0
        max_file_length = (
            max(
                (m.lines_of_code + m.blank_lines + m.comment_lines)
                for m in file_metrics
            )
            if file_metrics
            else 0
        )

        # 复杂度分布
        all_complexities = []
        for metrics in file_metrics:
            if metrics.max_complexity > 0:
                all_complexities.append(metrics.max_complexity)

        complexity_distribution = {
            "low": sum(1 for c in all_complexities if 1 <= c <= 10),
            "medium": sum(1 for c in all_complexities if 11 <= c <= 20),
            "high": sum(1 for c in all_complexities if 21 <= c <= 50),
            "very_high": sum(1 for c in all_complexities if c > 50),
        }

        return ProjectMetrics(
            project_path=str(project_path),
            total_files=total_files,
            python_files=len(python_files),
            total_lines=total_lines,
            code_lines=code_lines,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            total_functions=total_functions,
            total_classes=total_classes,
            total_imports=total_imports,
            avg_file_length=round(avg_file_length, 2),
            max_file_length=max_file_length,
            complexity_distribution=complexity_distribution,
        )

    def save_metrics(self, metrics: ProjectMetrics, output_path: Path):
        """保存指标到JSON文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2, ensure_ascii=False)

        self.logger.info(f"指标已保存到: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Python项目代码指标收集工具")
    parser.add_argument(
        "--project-path", type=str, required=True, help="项目根目录路径"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="metrics.json",
        help="输出文件路径 (默认: metrics.json)",
    )
    parser.add_argument("--verbose", action="store_true", help="显示详细日志")

    args = parser.parse_args()

    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # 验证项目路径
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"错误: 项目路径不存在: {project_path}")
        return 1

    if not project_path.is_dir():
        print(f"错误: 项目路径不是目录: {project_path}")
        return 1

    # 收集指标
    collector = CodeMetricsCollector()
    metrics = collector.collect_project_metrics(project_path)

    # 保存结果
    output_path = Path(args.output)
    collector.save_metrics(metrics, output_path)

    # 显示摘要
    print(f"\n📊 项目分析摘要:")
    print(f"项目路径: {metrics.project_path}")
    print(f"Python文件数: {metrics.python_files}")
    print(f"总代码行数: {metrics.code_lines}")
    print(f"函数数量: {metrics.total_functions}")
    print(f"类数量: {metrics.total_classes}")
    print(f"平均文件长度: {metrics.avg_file_length} 行")
    print(
        f"复杂度分布: 低({metrics.complexity_distribution['low']}) "
        f"中({metrics.complexity_distribution['medium']}) "
        f"高({metrics.complexity_distribution['high']}) "
        f"极高({metrics.complexity_distribution['very_high']})"
    )

    return 0


if __name__ == "__main__":
    exit(main())
