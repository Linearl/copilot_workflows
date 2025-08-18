#!/usr/bin/env python3
"""
扩展性评估插件

评估工作流的扩展性，包括配置文件支持、模板文件系统、插件或扩展点等。

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18
"""

from pathlib import Path
from typing import Dict, Any
import logging

from ..quality_assessment_plugin import QualityAssessmentPlugin

logger = logging.getLogger("workflow_validator")


class ExtensibilityPlugin(QualityAssessmentPlugin):
    """
    扩展性评估插件

    评估工作流的扩展性，检查是否支持配置化、模板化和插件化扩展。

    评分标准:
    - 配置文件支持 (+3.33分)
    - 模板文件系统 (+3.33分)
    - 插件或扩展点 (+3.33分)
    """

    def __init__(self):
        super().__init__(
            name="extensibility",
            version="1.0.0",
            description="评估工作流的扩展性",
            max_score=10.0,
        )

    def assess(self, workflow_dir: Path) -> float:
        """
        评估工作流扩展性

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            float: 扩展性得分 (0-10分)
        """
        if not self.validate_workflow_dir(workflow_dir):
            return 0.0

        logger.debug(f"开始评估扩展性: {workflow_dir}")

        score = 0.0
        total_checks = 3

        # 检查1: 配置文件支持 (3.33分)
        if self._check_configuration_support(workflow_dir):
            score += 3.33
            logger.debug("✓ 配置文件支持存在")
        else:
            logger.debug("✗ 配置文件支持缺失")

        # 检查2: 模板文件系统 (3.33分)
        if self._check_template_system(workflow_dir):
            score += 3.33
            logger.debug("✓ 模板文件系统存在")
        else:
            logger.debug("✗ 模板文件系统缺失")

        # 检查3: 插件或扩展点 (3.34分)
        if self._check_plugin_extensibility(workflow_dir):
            score += 3.34
            logger.debug("✓ 插件或扩展点存在")
        else:
            logger.debug("✗ 插件或扩展点缺失")

        final_score = min(score, self.max_score)
        logger.debug(f"扩展性评估完成: {final_score:.1f}/10.0")
        return final_score

    def _check_configuration_support(self, workflow_dir: Path) -> bool:
        """检查配置文件支持"""
        # 检查各种配置文件格式
        config_patterns = [
            "**/*.json",
            "**/*.yaml",
            "**/*.yml",
            "**/*.toml",
            "**/*.ini",
            "**/*config*",
        ]

        for pattern in config_patterns:
            config_files = list(workflow_dir.glob(pattern))
            for config_file in config_files:
                if not self.should_exclude_file(config_file, workflow_dir):
                    logger.debug(f"发现配置文件: {config_file.name}")
                    return True

        return False

    def _check_template_system(self, workflow_dir: Path) -> bool:
        """检查模板文件系统"""
        template_indicators = [
            "**/template*",
            "**/*template*",
            "**/templates/**",
            "**/*.template",
        ]

        for pattern in template_indicators:
            template_files = list(workflow_dir.glob(pattern))
            for template_file in template_files:
                if not self.should_exclude_file(template_file, workflow_dir):
                    logger.debug(f"发现模板文件: {template_file.name}")
                    return True

        return False

    def _check_plugin_extensibility(self, workflow_dir: Path) -> bool:
        """检查插件或扩展点"""
        # 检查Python文件中的插件相关代码
        python_files = []
        for py_file in workflow_dir.glob("**/*.py"):
            if not self.should_exclude_file(py_file, workflow_dir):
                python_files.append(py_file)

        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                # 检查插件相关关键词
                plugin_keywords = [
                    "plugin",
                    "Plugin",
                    "extend",
                    "extension",
                    "hook",
                    "Hook",
                    "registry",
                    "Registry",
                    "factory",
                    "Factory",
                    "interface",
                    "Interface",
                    "abc.ABC",
                    "abstractmethod",
                ]

                for keyword in plugin_keywords:
                    if keyword in content:
                        logger.debug(f"在 {py_file.name} 中发现插件扩展点: {keyword}")
                        return True

            except Exception:
                continue

        # 检查是否有plugins目录
        plugins_dirs = [
            workflow_dir / "plugins",
            workflow_dir / "extensions",
            workflow_dir / "addons",
        ]

        for plugins_dir in plugins_dirs:
            if plugins_dir.exists() and plugins_dir.is_dir():
                logger.debug(f"发现插件目录: {plugins_dir.name}")
                return True

        return False

    def get_assessment_details(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        获取扩展性评估的详细信息

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

        # 检查配置文件支持
        if self._check_configuration_support(workflow_dir):
            passed_checks.append("配置文件支持存在")
        else:
            failed_checks.append("配置文件支持缺失")
            recommendations.append("添加配置文件(JSON/YAML)支持用户自定义设置")

        # 检查模板文件系统
        if self._check_template_system(workflow_dir):
            passed_checks.append("模板文件系统存在")
        else:
            failed_checks.append("模板文件系统缺失")
            recommendations.append("设计模板文件系统，支持工作流定制化生成")

        # 检查插件或扩展点
        if self._check_plugin_extensibility(workflow_dir):
            passed_checks.append("插件或扩展点存在")
        else:
            failed_checks.append("插件或扩展点缺失")
            recommendations.append("设计插件接口或扩展点，支持功能模块化扩展")

        return {
            "score": self.assess(workflow_dir),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "recommendations": recommendations,
        }
