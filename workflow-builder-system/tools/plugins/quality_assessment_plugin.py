#!/usr/bin/env python3
"""
质量评估插件基类

定义了工作流质量评估插件的标准接口，所有评估维度插件都应该继承此基类。

Author: Workflow Builder System
Version: 2.0.0
Last Updated: 2025-08-18
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any
import logging

logger = logging.getLogger("workflow_validator")


class QualityAssessmentPlugin(ABC):
    """
    质量评估插件基类

    所有质量评估维度的插件都应该继承此基类并实现必要的抽象方法。

    Attributes:
        name (str): 插件名称
        version (str): 插件版本
        description (str): 插件描述
        max_score (float): 最大得分，默认为10.0
    """

    def __init__(
        self,
        name: str,
        version: str = "1.0.0",
        description: str = "",
        max_score: float = 10.0,
    ):
        """
        初始化质量评估插件

        Args:
            name: 插件名称
            version: 插件版本
            description: 插件描述
            max_score: 最大得分
        """
        self.name = name
        self.version = version
        self.description = description
        self.max_score = max_score

    @abstractmethod
    def assess(self, workflow_dir: Path) -> float:
        """
        评估工作流质量

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            float: 评估得分 (0 到 max_score)

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        pass

    @abstractmethod
    def get_assessment_details(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        获取详细的评估信息

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            Dict[str, Any]: 包含评估详情的字典，至少包含：
                - score: 评估得分
                - passed_checks: 通过的检查项
                - failed_checks: 失败的检查项
                - recommendations: 改进建议

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        pass

    def validate_workflow_dir(self, workflow_dir: Path) -> bool:
        """
        验证工作流目录是否有效

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            bool: 是否为有效的工作流目录
        """
        if not workflow_dir.exists():
            logger.error(f"工作流目录不存在: {workflow_dir}")
            return False

        if not workflow_dir.is_dir():
            logger.error(f"路径不是目录: {workflow_dir}")
            return False

        return True

    def should_exclude_file(
        self, file_path: Path, workflow_dir: Path, exclude_patterns: List[str] = None
    ) -> bool:
        """
        检查文件是否应该被排除

        Args:
            file_path: 文件路径
            workflow_dir: 工作流目录
            exclude_patterns: 排除模式列表

        Returns:
            bool: 是否应该排除
        """
        if exclude_patterns is None:
            exclude_patterns = [
                "**/workflow_system_analysis_report.md",
                "**/validation_*.txt",
                "**/*.backup*",
                "**/temp/**",
                "**/.git/**",
                "**/develop/**",
            ]

        try:
            import fnmatch

            rel_path = file_path.relative_to(workflow_dir)
            rel_path_str = str(rel_path).replace("\\", "/")

            for pattern in exclude_patterns:
                if pattern.startswith("**/"):
                    simple_pattern = pattern[3:]
                    if simple_pattern.endswith("/") or "/" in simple_pattern:
                        if simple_pattern.endswith("/"):
                            dir_name = simple_pattern.rstrip("/")
                        else:
                            dir_name = simple_pattern.split("/")[0]
                        path_parts = rel_path_str.split("/")
                        if dir_name in path_parts:
                            return True
                    else:
                        if fnmatch.fnmatch(
                            file_path.name, simple_pattern
                        ) or rel_path_str.endswith(simple_pattern):
                            return True
                elif fnmatch.fnmatch(rel_path_str, pattern) or fnmatch.fnmatch(
                    file_path.name, pattern
                ):
                    return True

            return False
        except ValueError:
            return False

    def get_plugin_info(self) -> Dict[str, str]:
        """
        获取插件信息

        Returns:
            Dict[str, str]: 插件信息字典
        """
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "max_score": str(self.max_score),
        }

    def __str__(self) -> str:
        """字符串表示"""
        return f"{self.name} v{self.version}"

    def __repr__(self) -> str:
        """调试表示"""
        return f"QualityAssessmentPlugin(name='{self.name}', version='{self.version}')"
