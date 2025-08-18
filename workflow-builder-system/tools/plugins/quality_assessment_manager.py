#!/usr/bin/env python3
"""
质量评估插件管理器

管理所有质量评估维度插件的加载、执行和结果汇总。

Author: Workflow Builder System
Version: 2.0.0
Last Updated: 2025-08-18
"""

from pathlib import Path
from typing import Dict, List, Any, Type
import logging

from .quality_assessment_plugin import QualityAssessmentPlugin
from .quality_assessment import (
    CompletenessPlugin,
    UsabilityPlugin,
    MaintainabilityPlugin,
    DocumentationPlugin,
    ExtensibilityPlugin,
)

logger = logging.getLogger("workflow_validator")


class QualityAssessmentManager:
    """
    质量评估插件管理器

    负责管理和协调所有质量评估维度插件的执行。

    Attributes:
        plugins (Dict[str, QualityAssessmentPlugin]): 已注册的插件
        weights (Dict[str, float]): 各维度的权重
    """

    def __init__(self, custom_weights: Dict[str, float] = None):
        """
        初始化质量评估管理器

        Args:
            custom_weights: 自定义权重配置，如果不提供则使用默认权重
        """
        self.plugins: Dict[str, QualityAssessmentPlugin] = {}

        # 默认权重配置
        self.weights = {
            "completeness": 0.30,  # 完整性 30%
            "usability": 0.25,  # 易用性 25%
            "maintainability": 0.25,  # 可维护性 25%
            "documentation": 0.10,  # 文档质量 10%
            "extensibility": 0.10,  # 扩展性 10%
        }

        # 应用自定义权重
        if custom_weights:
            self.weights.update(custom_weights)
            logger.debug(f"应用自定义权重: {custom_weights}")

        # 注册标准插件
        self._register_standard_plugins()

    def _register_standard_plugins(self):
        """注册标准质量评估插件"""
        standard_plugins = [
            CompletenessPlugin(),
            UsabilityPlugin(),
            MaintainabilityPlugin(),
            DocumentationPlugin(),
            ExtensibilityPlugin(),
        ]

        for plugin in standard_plugins:
            self.register_plugin(plugin)

    def register_plugin(self, plugin: QualityAssessmentPlugin):
        """
        注册质量评估插件

        Args:
            plugin: 要注册的插件实例
        """
        if not isinstance(plugin, QualityAssessmentPlugin):
            raise TypeError(f"插件必须继承自QualityAssessmentPlugin: {type(plugin)}")

        self.plugins[plugin.name] = plugin
        logger.debug(f"已注册质量评估插件: {plugin}")

    def unregister_plugin(self, plugin_name: str):
        """
        取消注册插件

        Args:
            plugin_name: 插件名称
        """
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            logger.debug(f"已取消注册插件: {plugin_name}")
        else:
            logger.warning(f"尝试取消注册不存在的插件: {plugin_name}")

    def assess_quality(self, workflow_dir: Path) -> Dict[str, Any]:
        """
        执行完整的质量评估

        Args:
            workflow_dir: 工作流目录路径

        Returns:
            Dict[str, Any]: 质量评估结果，包含各维度得分和总分
        """
        if not workflow_dir.exists():
            raise FileNotFoundError(f"工作流目录不存在: {workflow_dir}")

        logger.info(f"开始质量评估: {workflow_dir}")

        # 执行各插件评估
        dimension_scores = {}
        plugin_details = {}

        for plugin_name, plugin in self.plugins.items():
            try:
                logger.debug(f"执行插件评估: {plugin_name}")
                score = plugin.assess(workflow_dir)
                dimension_scores[plugin_name] = score

                # 获取详细评估信息
                details = plugin.get_assessment_details(workflow_dir)
                plugin_details[plugin_name] = details

                logger.debug(f"插件 {plugin_name} 评估完成: {score:.1f}/10.0")

            except Exception as e:
                logger.error(f"插件 {plugin_name} 评估失败: {e}")
                dimension_scores[plugin_name] = 0.0
                plugin_details[plugin_name] = {
                    "score": 0.0,
                    "passed_checks": [],
                    "failed_checks": [f"插件执行失败: {str(e)}"],
                    "recommendations": ["检查插件配置和工作流目录权限"],
                }

        # 计算加权总分
        total_score = self._calculate_weighted_score(dimension_scores)

        # 生成质量等级
        grade = self._get_quality_grade(total_score)

        result = {
            "overall_score": total_score,
            "grade": grade,
            "dimension_scores": dimension_scores,
            "plugin_details": plugin_details,
            "weights": self.weights.copy(),
            "summary": self._generate_summary(dimension_scores, plugin_details),
        }

        logger.info(f"质量评估完成 - 总分: {total_score:.1f}/10.0 ({grade})")
        return result

    def _calculate_weighted_score(self, dimension_scores: Dict[str, float]) -> float:
        """计算加权总分"""
        total_score = 0.0
        total_weight = 0.0

        for dimension, score in dimension_scores.items():
            weight = self.weights.get(dimension, 0.0)
            total_score += score * weight
            total_weight += weight

        # 如果权重总和不为1，进行标准化
        if total_weight > 0 and total_weight != 1.0:
            total_score = total_score / total_weight

        return min(10.0, total_score)

    def _get_quality_grade(self, score: float) -> str:
        """根据得分获取质量等级"""
        if score >= 9.0:
            return "优秀"
        elif score >= 8.0:
            return "良好"
        elif score >= 7.0:
            return "中等"
        elif score >= 6.0:
            return "一般"
        else:
            return "需要改进"

    def _generate_summary(
        self, dimension_scores: Dict[str, float], plugin_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """生成评估摘要"""
        total_passed = 0
        total_failed = 0
        all_recommendations = []

        for plugin_name, details in plugin_details.items():
            total_passed += len(details.get("passed_checks", []))
            total_failed += len(details.get("failed_checks", []))
            all_recommendations.extend(details.get("recommendations", []))

        # 找出最高分和最低分的维度
        if dimension_scores:
            best_dimension = max(dimension_scores, key=dimension_scores.get)
            worst_dimension = min(dimension_scores, key=dimension_scores.get)
        else:
            best_dimension = worst_dimension = "无"

        return {
            "total_checks": total_passed + total_failed,
            "passed_checks": total_passed,
            "failed_checks": total_failed,
            "best_dimension": best_dimension,
            "worst_dimension": worst_dimension,
            "top_recommendations": list(set(all_recommendations))[:5],  # 去重并取前5个
        }

    def get_registered_plugins(self) -> List[Dict[str, str]]:
        """获取已注册的插件列表"""
        return [plugin.get_plugin_info() for plugin in self.plugins.values()]

    def get_plugin_by_name(self, plugin_name: str) -> QualityAssessmentPlugin:
        """
        根据名称获取插件

        Args:
            plugin_name: 插件名称

        Returns:
            QualityAssessmentPlugin: 插件实例

        Raises:
            KeyError: 插件不存在
        """
        if plugin_name not in self.plugins:
            raise KeyError(f"插件不存在: {plugin_name}")
        return self.plugins[plugin_name]

    def update_weights(self, new_weights: Dict[str, float]):
        """
        更新权重配置

        Args:
            new_weights: 新的权重配置
        """
        # 验证权重
        total_weight = sum(new_weights.values())
        if not (0.8 <= total_weight <= 1.2):  # 允许一定的容差
            logger.warning(f"权重总和不是1.0: {total_weight}")

        self.weights.update(new_weights)
        logger.info(f"权重配置已更新: {new_weights}")

    def __str__(self) -> str:
        """字符串表示"""
        return f"QualityAssessmentManager(plugins={len(self.plugins)})"

    def __repr__(self) -> str:
        """调试表示"""
        plugin_names = list(self.plugins.keys())
        return f"QualityAssessmentManager(plugins={plugin_names})"
