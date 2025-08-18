#!/usr/bin/env python3
"""
可维护性评估插件

评估工作流的可维护性，包括代码注释质量、面向对象设计、版本控制信息、日志记录等。

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18
"""

from pathlib import Path
from typing import Dict, Any, List
import re
import logging

from ..quality_assessment_plugin import QualityAssessmentPlugin

logger = logging.getLogger("workflow_validator")


class MaintainabilityPlugin(QualityAssessmentPlugin):
    """
    可维护性评估插件

    评估工作流的可维护性，检查代码质量、文档完整性、版本管理等方面。

    评分标准:
    - 代码注释率≥10% (+2.5分)
    - 面向对象设计 (+2.5分) - 类定义、继承、方法、装饰器
    - 版本控制信息 (+2.5分)
    - 日志记录机制 (+2.5分)
    """

    def __init__(self):
        super().__init__(
            name="maintainability",
            version="1.0.0",
            description="评估工作流的可维护性",
            max_score=10.0,
        )

    def assess(self, workflow_dir: Path) -> float:
        """
        评估工作流可维护性

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            float: 可维护性得分 (0-10分)
        """
        if not self.validate_workflow_dir(workflow_dir):
            return 0.0

        logger.debug(f"开始评估可维护性: {workflow_dir}")

        score = 0.0
        total_checks = 4

        # 检查1: 代码注释率 (2.5分)
        comment_score = self._check_code_comment_ratio(workflow_dir)
        score += comment_score
        if comment_score > 0:
            logger.debug("✓ 代码注释率达标")
        else:
            logger.debug("✗ 代码注释率不足")

        # 检查2: 面向对象设计 (2.5分)
        oo_score = self._check_object_oriented_design(workflow_dir)
        score += oo_score
        if oo_score > 0:
            logger.debug("✓ 面向对象设计检查通过")
        else:
            logger.debug("✗ 未发现面向对象设计模式")

        # 检查3: 版本控制信息 (2.5分)
        version_score = self._check_version_control_info(workflow_dir)
        score += version_score
        if version_score > 0:
            logger.debug("✓ 版本控制信息存在")
        else:
            logger.debug("✗ 版本控制信息缺失")

        # 检查4: 日志记录机制 (2.5分)
        logging_score = self._check_logging_mechanism(workflow_dir)
        score += logging_score
        if logging_score > 0:
            logger.debug("✓ 日志记录机制存在")
        else:
            logger.debug("✗ 日志记录机制缺失")

        final_score = min(score, self.max_score)
        logger.info(f"可维护性评估完成: {final_score:.1f}/10.0")
        return final_score

    def _check_code_comment_ratio(self, workflow_dir: Path) -> float:
        """检查代码注释率"""
        python_files = []
        for py_file in workflow_dir.glob("**/*.py"):
            if not self.should_exclude_file(py_file, workflow_dir):
                python_files.append(py_file)

        if not python_files:
            logger.debug("没有找到Python文件")
            return 0.0

        total_lines = 0
        comment_lines = 0

        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                total_lines += len(lines)

                # 统计注释行（以#开头，或包含docstring）
                for line in lines:
                    stripped = line.strip()
                    if (
                        stripped.startswith("#")
                        or '"""' in stripped
                        or "'''" in stripped
                    ):
                        comment_lines += 1

            except Exception as e:
                logger.warning(f"读取文件失败 {py_file}: {e}")

        if total_lines == 0:
            return 0.0

        comment_ratio = comment_lines / total_lines
        logger.debug(f"代码注释率: {comment_ratio:.2%} ({comment_lines}/{total_lines})")

        # 注释率≥10%得满分，否则按比例给分
        if comment_ratio >= 0.1:
            return 2.5
        else:
            return (comment_ratio / 0.1) * 2.5

    def _check_object_oriented_design(self, workflow_dir: Path) -> float:
        """检查面向对象设计"""
        python_files = []
        for py_file in workflow_dir.glob("**/*.py"):
            if not self.should_exclude_file(py_file, workflow_dir):
                python_files.append(py_file)

        if not python_files:
            return 0.0

        oo_score = 0.0

        # 统计面向对象特征
        class_count = 0
        inheritance_count = 0
        method_count = 0
        decorator_count = 0

        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")

                # 检查类定义
                class_matches = re.findall(r"^class\s+\w+", content, re.MULTILINE)
                class_count += len(class_matches)

                # 检查继承关系
                inheritance_matches = re.findall(
                    r"^class\s+\w+\([^)]+\)", content, re.MULTILINE
                )
                inheritance_count += len(inheritance_matches)

                # 检查方法定义
                method_matches = re.findall(r"^\s+def\s+\w+", content, re.MULTILINE)
                method_count += len(method_matches)

                # 检查装饰器
                decorator_matches = re.findall(r"^\s*@\w+", content, re.MULTILINE)
                decorator_count += len(decorator_matches)

            except Exception as e:
                logger.warning(f"读取文件失败 {py_file}: {e}")

        # 根据发现的OO特征计分
        if class_count > 0:
            oo_score += 1.25  # 发现类定义
            logger.debug(f"发现 {class_count} 个类定义")

        if inheritance_count > 0:
            oo_score += 0.5  # 发现继承关系
            logger.debug(f"发现 {inheritance_count} 个继承关系")

        if method_count > 0:
            oo_score += 0.5  # 发现方法定义
            logger.debug(f"发现 {method_count} 个方法定义")

        if decorator_count > 0:
            oo_score += 0.25  # 发现装饰器
            logger.debug(f"发现 {decorator_count} 个装饰器")

        # 确保得分在0-2.5范围内
        return min(2.5, oo_score)

    def _check_version_control_info(self, workflow_dir: Path) -> float:
        """检查版本控制信息"""
        version_found = False

        # 检查Markdown文件中的版本信息
        for md_file in workflow_dir.glob("**/*.md"):
            if self.should_exclude_file(md_file, workflow_dir):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                if any(
                    keyword in content.lower()
                    for keyword in [
                        "版本",
                        "version",
                        "v1.",
                        "v2.",
                        "更新日志",
                        "changelog",
                    ]
                ):
                    version_found = True
                    break
            except Exception:
                continue

        # 检查Python文件中的版本信息
        if not version_found:
            for py_file in workflow_dir.glob("**/*.py"):
                if self.should_exclude_file(py_file, workflow_dir):
                    continue
                try:
                    content = py_file.read_text(encoding="utf-8")
                    if any(
                        keyword in content.lower()
                        for keyword in [
                            "__version__",
                            "version =",
                            "version:",
                            "v1.",
                            "v2.",
                        ]
                    ):
                        version_found = True
                        break
                except Exception:
                    continue

        return 2.5 if version_found else 0.0

    def _check_logging_mechanism(self, workflow_dir: Path) -> float:
        """检查日志记录机制"""
        logging_found = False

        for py_file in workflow_dir.glob("**/*.py"):
            if self.should_exclude_file(py_file, workflow_dir):
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
                if any(
                    keyword in content
                    for keyword in [
                        "logging",
                        "logger",
                        "log(",
                        ".info(",
                        ".debug(",
                        ".warning(",
                        ".error(",
                    ]
                ):
                    logging_found = True
                    break
            except Exception:
                continue

        return 2.5 if logging_found else 0.0

    def get_assessment_details(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        获取可维护性评估的详细信息

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            Dict[str, Any]: 详细评估信息
        """
        if not self.validate_workflow_dir(workflow_dir):
            return {
                "score": 0.0,
                "passed_checks": [],
                "failed_checks": ["工作流目录无效"],
                "recommendations": ["确保提供有效的工作流目录路径"],
            }

        passed_checks = []
        failed_checks = []
        recommendations = []

        # 检查代码注释率
        comment_score = self._check_code_comment_ratio(workflow_dir)
        if comment_score >= 2.5:
            passed_checks.append("代码注释率充足")
        elif comment_score > 0:
            passed_checks.append(f"代码注释率部分达标 ({comment_score:.1f}/2.5分)")
            recommendations.append("提高代码注释率到10%以上")
        else:
            failed_checks.append("代码注释率不足")
            recommendations.append("为Python代码添加详细的注释和文档字符串")

        # 检查面向对象设计
        oo_score = self._check_object_oriented_design(workflow_dir)
        if oo_score >= 2.5:
            passed_checks.append("面向对象设计完善")
        elif oo_score > 0:
            passed_checks.append(f"面向对象设计部分采用 ({oo_score:.1f}/2.5分)")
            recommendations.append("完善面向对象设计，增加类的继承和方法封装")
        else:
            failed_checks.append("未采用面向对象设计")
            recommendations.append("重构代码使用类和方法，提高代码的模块化和可维护性")

        # 检查版本控制信息
        version_score = self._check_version_control_info(workflow_dir)
        if version_score > 0:
            passed_checks.append("版本控制信息存在")
        else:
            failed_checks.append("版本控制信息缺失")
            recommendations.append("在文档或代码中添加版本号和更新日志")

        # 检查日志记录机制
        logging_score = self._check_logging_mechanism(workflow_dir)
        if logging_score > 0:
            passed_checks.append("日志记录机制存在")
        else:
            failed_checks.append("日志记录机制缺失")
            recommendations.append("为Python脚本添加日志记录功能，便于调试和监控")

        return {
            "score": self.assess(workflow_dir),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "recommendations": recommendations,
        }
