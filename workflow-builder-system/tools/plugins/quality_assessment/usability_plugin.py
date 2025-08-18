#!/usr/bin/env python3
"""
易用性评估插件

评估工作流的易用性，包括使用指导、示例代码、错误处理说明等。

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18
"""

from pathlib import Path
from typing import Dict, Any
import logging

from ..quality_assessment_plugin import QualityAssessmentPlugin

logger = logging.getLogger("workflow_validator")


class UsabilityPlugin(QualityAssessmentPlugin):
    """
    易用性评估插件

    评估工作流的易用性，检查使用指导、示例代码、错误处理说明等是否完善。

    评分标准:
    - 使用指导文档 (+2分)
    - 示例代码 (+2分)
    - 错误处理说明 (+2分)
    - 配置说明 (+2分)
    - FAQ或故障排除 (+2分)
    """

    def __init__(self):
        super().__init__(
            name="usability",
            version="1.0.0",
            description="评估工作流的易用性",
            max_score=10.0,
        )

    def assess(self, workflow_dir: Path) -> float:
        """
        评估工作流易用性

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            float: 易用性得分 (0-10分)
        """
        if not self.validate_workflow_dir(workflow_dir):
            return 0.0

        logger.debug(f"开始评估易用性: {workflow_dir}")

        score = 0.0
        total_checks = 5

        # 检查1: 使用指导文档 (2分)
        if self._check_usage_guidance(workflow_dir):
            score += 2
            logger.debug("✓ 使用指导文档存在")
        else:
            logger.debug("✗ 使用指导文档缺失")

        # 检查2: 示例代码 (2分)
        if self._check_example_code(workflow_dir):
            score += 2
            logger.debug("✓ 示例代码存在")
        else:
            logger.debug("✗ 示例代码缺失")

        # 检查3: 错误处理说明 (2分)
        if self._check_error_handling_docs(workflow_dir):
            score += 2
            logger.debug("✓ 错误处理说明存在")
        else:
            logger.debug("✗ 错误处理说明缺失")

        # 检查4: 配置说明 (2分)
        if self._check_configuration_docs(workflow_dir):
            score += 2
            logger.debug("✓ 配置说明存在")
        else:
            logger.debug("✗ 配置说明缺失")

        # 检查5: FAQ或故障排除 (2分)
        if self._check_faq_or_troubleshooting(workflow_dir):
            score += 2
            logger.debug("✓ FAQ或故障排除文档存在")
        else:
            logger.debug("✗ FAQ或故障排除文档缺失")

        final_score = min(score, self.max_score)
        logger.info(f"易用性评估完成: {final_score:.1f}/10.0")
        return final_score

    def _check_usage_guidance(self, workflow_dir: Path) -> bool:
        """检查使用指导文档"""
        for md_file in workflow_dir.glob("**/*.md"):
            if self.should_exclude_file(md_file, workflow_dir):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                if any(
                    keyword in content
                    for keyword in [
                        "使用指导",
                        "快速开始",
                        "Getting Started",
                        "使用方法",
                    ]
                ):
                    return True
            except Exception:
                continue
        return False

    def _check_example_code(self, workflow_dir: Path) -> bool:
        """检查示例代码"""
        for md_file in workflow_dir.glob("**/*.md"):
            if self.should_exclude_file(md_file, workflow_dir):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                if "```" in content:
                    return True
            except Exception:
                continue
        return False

    def _check_error_handling_docs(self, workflow_dir: Path) -> bool:
        """检查错误处理说明"""
        for file_path in workflow_dir.glob("**/*"):
            if self.should_exclude_file(file_path, workflow_dir):
                continue
            if file_path.suffix in [".md", ".py", ".ps1"]:
                try:
                    content = file_path.read_text(encoding="utf-8")
                    if any(
                        keyword in content
                        for keyword in [
                            "错误",
                            "异常",
                            "故障",
                            "Error",
                            "Exception",
                            "Troubleshooting",
                        ]
                    ):
                        return True
                except Exception:
                    continue
        return False

    def _check_configuration_docs(self, workflow_dir: Path) -> bool:
        """检查配置说明"""
        for md_file in workflow_dir.glob("**/*.md"):
            if self.should_exclude_file(md_file, workflow_dir):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                if any(
                    keyword in content
                    for keyword in ["配置", "设置", "Configuration", "Settings"]
                ):
                    return True
            except Exception:
                continue
        return False

    def _check_faq_or_troubleshooting(self, workflow_dir: Path) -> bool:
        """检查FAQ或故障排除文档"""
        for md_file in workflow_dir.glob("**/*.md"):
            if self.should_exclude_file(md_file, workflow_dir):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                if any(
                    keyword in content
                    for keyword in [
                        "FAQ",
                        "故障排除",
                        "常见问题",
                        "Troubleshooting",
                        "问题解答",
                    ]
                ):
                    return True
            except Exception:
                continue
        return False

    def get_assessment_details(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        获取易用性评估的详细信息

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

        # 检查使用指导文档
        if self._check_usage_guidance(workflow_dir):
            passed_checks.append("使用指导文档存在")
        else:
            failed_checks.append("使用指导文档缺失")
            recommendations.append("添加使用指导或快速开始章节到README.md中")

        # 检查示例代码
        if self._check_example_code(workflow_dir):
            passed_checks.append("示例代码存在")
        else:
            failed_checks.append("示例代码缺失")
            recommendations.append("在文档中添加代码示例和使用演示")

        # 检查错误处理说明
        if self._check_error_handling_docs(workflow_dir):
            passed_checks.append("错误处理说明存在")
        else:
            failed_checks.append("错误处理说明缺失")
            recommendations.append("添加错误处理和异常情况的说明文档")

        # 检查配置说明
        if self._check_configuration_docs(workflow_dir):
            passed_checks.append("配置说明存在")
        else:
            failed_checks.append("配置说明缺失")
            recommendations.append("添加配置文件和自定义设置的说明")

        # 检查FAQ或故障排除
        if self._check_faq_or_troubleshooting(workflow_dir):
            passed_checks.append("FAQ或故障排除文档存在")
        else:
            failed_checks.append("FAQ或故障排除文档缺失")
            recommendations.append("添加常见问题解答或故障排除指南")

        return {
            "score": self.assess(workflow_dir),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "recommendations": recommendations,
        }
