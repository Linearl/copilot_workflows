#!/usr/bin/env python3
"""
完整性评估插件

评估工作流的功能完整性，包括必要文件、目录结构、配置文件等的存在性。

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18
"""

from pathlib import Path
from typing import Dict, Any
import logging

from ..quality_assessment_plugin import QualityAssessmentPlugin

logger = logging.getLogger("workflow_validator")


class CompletenessPlugin(QualityAssessmentPlugin):
    """
    完整性评估插件

    评估工作流的功能完整性，检查必要的文件、目录结构、配置文件等是否存在。

    评分标准:
    - 主要模板文件存在 (+1.67分)
    - README文档存在 (+1.67分)
    - 工具脚本文件存在 (+3.33分)
    - 核心文件夹结构完整 (+1.67分) - templates/docs/tools
    - 测试文件存在 (+1.67分)
    - 配置文件存在 (+1.67分)
    """

    def __init__(self):
        super().__init__(
            name="completeness",
            version="1.0.0",
            description="评估工作流的功能完整性",
            max_score=10.0,
        )

    def assess(self, workflow_dir: Path) -> float:
        """
        评估工作流完整性

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            float: 完整性得分 (0-10分)
        """
        if not self.validate_workflow_dir(workflow_dir):
            return 0.0

        logger.debug(f"开始评估完整性: {workflow_dir}")

        score = 0.0
        total_checks = 6

        # 检查1: 主要模板文件 (1.67分)
        if any(
            workflow_dir.glob(pattern) for pattern in ["*_template.md", "*_workflow.md"]
        ):
            score += 1.67
            logger.debug("✓ 主要模板文件存在")
        else:
            logger.debug("✗ 主要模板文件缺失")

        # 检查2: README文档 (1.67分)
        if any(workflow_dir.glob("README.md")):
            score += 1.67
            logger.debug("✓ README文档存在")
        else:
            logger.debug("✗ README文档缺失")

        # 检查3: 工具脚本文件 (3.33分) - Python或PowerShell，有其中之一即可
        if any(workflow_dir.glob("**/*.py")) or any(workflow_dir.glob("**/*.ps1")):
            score += 3.33
            logger.debug("✓ 工具脚本文件存在")
        else:
            logger.debug("✗ 工具脚本文件缺失")

        # 检查4: 核心文件夹结构 (1.67分)
        required_dirs = ["templates", "docs", "tools"]
        existing_dirs = 0
        for req_dir in required_dirs:
            if (workflow_dir / req_dir).exists():
                existing_dirs += 1
                logger.debug(f"✓ 目录存在: {req_dir}")
            else:
                logger.debug(f"✗ 目录缺失: {req_dir}")
        # 按比例给分
        score += (existing_dirs / len(required_dirs)) * 1.67

        # 检查5: 测试文件 (1.67分)
        if any(workflow_dir.glob("**/test_*.py")):
            score += 1.67
            logger.debug("✓ 测试文件存在")
        else:
            logger.debug("✗ 测试文件缺失")

        # 检查6: 配置文件 (1.67分)
        if any(workflow_dir.glob("**/*.json")) or any(workflow_dir.glob("**/*.yaml")):
            score += 1.67
            logger.debug("✓ 配置文件存在")
        else:
            logger.debug("✗ 配置文件缺失")

        final_score = min(score, self.max_score)
        logger.debug(f"完整性评估完成: {final_score:.1f}/10.0")
        return final_score

    def get_assessment_details(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        获取完整性评估的详细信息

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

        # 检查主要模板文件
        if any(
            workflow_dir.glob(pattern) for pattern in ["*_template.md", "*_workflow.md"]
        ):
            passed_checks.append("主要模板文件存在")
        else:
            failed_checks.append("主要模板文件缺失")
            recommendations.append("创建主要的工作流模板文件 (如 *_template.md)")

        # 检查README文档
        if any(workflow_dir.glob("README.md")):
            passed_checks.append("README文档存在")
        else:
            failed_checks.append("README文档缺失")
            recommendations.append("创建README.md文档说明工作流用途和使用方法")

        # 检查工具脚本文件
        if any(workflow_dir.glob("**/*.py")) or any(workflow_dir.glob("**/*.ps1")):
            passed_checks.append("工具脚本文件存在")
        else:
            failed_checks.append("工具脚本文件缺失")
            recommendations.append("添加Python或PowerShell脚本来支持工作流自动化")

        # 检查核心文件夹结构
        required_dirs = ["templates", "docs", "tools"]
        existing_dirs = []
        missing_dirs = []
        for req_dir in required_dirs:
            if (workflow_dir / req_dir).exists():
                existing_dirs.append(req_dir)
            else:
                missing_dirs.append(req_dir)

        if existing_dirs:
            passed_checks.append(f"核心目录存在: {', '.join(existing_dirs)}")
        if missing_dirs:
            failed_checks.append(f"核心目录缺失: {', '.join(missing_dirs)}")
            recommendations.append(f"创建缺失的核心目录: {', '.join(missing_dirs)}")

        # 检查测试文件
        if any(workflow_dir.glob("**/test_*.py")):
            passed_checks.append("测试文件存在")
        else:
            failed_checks.append("测试文件缺失")
            recommendations.append("添加测试文件来验证工作流功能")

        # 检查配置文件
        if any(workflow_dir.glob("**/*.json")) or any(workflow_dir.glob("**/*.yaml")):
            passed_checks.append("配置文件存在")
        else:
            failed_checks.append("配置文件缺失")
            recommendations.append("添加配置文件来支持工作流自定义设置")

        return {
            "score": self.assess(workflow_dir),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "recommendations": recommendations,
        }
