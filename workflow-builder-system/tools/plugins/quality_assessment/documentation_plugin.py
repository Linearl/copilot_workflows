#!/usr/bin/env python3
"""
文档质量评估插件

评估工作流的文档质量，包括文档存在性、结构完整性、代码文档等。

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18
"""

from pathlib import Path
from typing import Dict, Any
import re
import logging

from ..quality_assessment_plugin import QualityAssessmentPlugin

logger = logging.getLogger("workflow_validator")


class DocumentationPlugin(QualityAssessmentPlugin):
    """
    文档质量评估插件

    评估工作流的文档质量，检查文档的完整性、结构和更新状态。

    评分标准:
    - README文件存在 (+2.5分)
    - 文档结构完整性 (+2.5分)
    - 代码文档存在 (+2.5分)
    - 文档更新时间 (+2.5分)
    """

    def __init__(self):
        super().__init__(
            name="documentation",
            version="1.0.0",
            description="评估工作流的文档质量",
            max_score=10.0,
        )

    def assess(self, workflow_dir: Path) -> float:
        """
        评估工作流文档质量

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            float: 文档质量得分 (0-10分)
        """
        if not self.validate_workflow_dir(workflow_dir):
            return 0.0

        logger.debug(f"开始评估文档质量: {workflow_dir}")

        score = 0.0
        total_checks = 4

        # 检查1: README文件存在 (2.5分)
        if self._check_readme_exists(workflow_dir):
            score += 2.5
            logger.debug("✓ README文件存在")
        else:
            logger.debug("✗ README文件缺失")

        # 检查2: 文档结构完整性 (2.5分)
        if self._check_documentation_structure(workflow_dir):
            score += 2.5
            logger.debug("✓ 文档结构完整")
        else:
            logger.debug("✗ 文档结构不完整")

        # 检查3: 代码文档存在 (2.5分)
        if self._check_code_documentation(workflow_dir):
            score += 2.5
            logger.debug("✓ 代码文档存在")
        else:
            logger.debug("✗ 代码文档缺失")

        # 检查4: 文档更新时间 (2.5分)
        if self._check_documentation_freshness(workflow_dir):
            score += 2.5
            logger.debug("✓ 文档更新及时")
        else:
            logger.debug("✗ 文档可能过期")

        final_score = min(score, self.max_score)
        logger.info(f"文档质量评估完成: {final_score:.1f}/10.0")
        return final_score

    def _check_readme_exists(self, workflow_dir: Path) -> bool:
        """检查README文件是否存在"""
        readme_files = list(workflow_dir.glob("README.md"))
        if readme_files:
            readme_path = readme_files[0]
            try:
                content = readme_path.read_text(encoding="utf-8")
                # 确保README有实质内容（不只是标题）
                lines = [line.strip() for line in content.split("\n") if line.strip()]
                return len(lines) >= 5  # 至少5行内容
            except Exception:
                return False
        return False

    def _check_documentation_structure(self, workflow_dir: Path) -> bool:
        """检查文档结构完整性"""
        md_files = []
        for md_file in workflow_dir.glob("**/*.md"):
            if not self.should_exclude_file(md_file, workflow_dir):
                md_files.append(md_file)

        if not md_files:
            return False

        # 检查是否有包含基本章节的文档
        required_sections = ["目标", "使用", "步骤"]
        found_sections = set()

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8")
                for section in required_sections:
                    if section in content:
                        found_sections.add(section)
            except Exception:
                continue

        # 要求至少包含2/3的基本章节
        return len(found_sections) >= 2

    def _check_code_documentation(self, workflow_dir: Path) -> bool:
        """检查代码文档存在"""
        python_files = []
        for py_file in workflow_dir.glob("**/*.py"):
            if not self.should_exclude_file(py_file, workflow_dir):
                python_files.append(py_file)

        if not python_files:
            return False

        documented_files = 0

        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                # 检查是否有文档字符串或详细注释
                if (
                    '"""' in content or "'''" in content or content.count("#") >= 10
                ):  # 至少10个注释
                    documented_files += 1
            except Exception:
                continue

        # 要求至少50%的Python文件有文档
        return documented_files >= len(python_files) * 0.5

    def _check_documentation_freshness(self, workflow_dir: Path) -> bool:
        """检查文档更新时间"""
        md_files = []
        for md_file in workflow_dir.glob("**/*.md"):
            if not self.should_exclude_file(md_file, workflow_dir):
                md_files.append(md_file)

        if not md_files:
            return False

        fresh_docs = 0

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8")
                # 检查是否包含时间信息
                time_patterns = [
                    r"2025",  # 当前年份
                    r"更新时间",
                    r"Last Updated",
                    r"Updated:",
                    r"修改时间",
                    r"\d{4}-\d{2}-\d{2}",  # 日期格式
                ]

                for pattern in time_patterns:
                    if re.search(pattern, content):
                        fresh_docs += 1
                        break
            except Exception:
                continue

        # 要求至少30%的文档有更新时间信息
        return fresh_docs >= len(md_files) * 0.3

    def get_assessment_details(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        获取文档质量评估的详细信息

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

        # 检查README文件
        if self._check_readme_exists(workflow_dir):
            passed_checks.append("README文件存在且内容充实")
        else:
            failed_checks.append("README文件缺失或内容不足")
            recommendations.append("创建或完善README.md文件，添加详细的项目说明")

        # 检查文档结构
        if self._check_documentation_structure(workflow_dir):
            passed_checks.append("文档结构完整")
        else:
            failed_checks.append("文档结构不完整")
            recommendations.append("确保文档包含目标、使用方法、操作步骤等基本章节")

        # 检查代码文档
        if self._check_code_documentation(workflow_dir):
            passed_checks.append("代码文档充足")
        else:
            failed_checks.append("代码文档不足")
            recommendations.append("为Python代码添加文档字符串和详细注释")

        # 检查文档更新时间
        if self._check_documentation_freshness(workflow_dir):
            passed_checks.append("文档更新及时")
        else:
            failed_checks.append("文档可能过期")
            recommendations.append("在文档中添加更新时间信息，保持文档的时效性")

        return {
            "score": self.assess(workflow_dir),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "recommendations": recommendations,
        }
