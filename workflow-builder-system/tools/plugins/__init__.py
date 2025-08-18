"""
质量评估插件系统

This module provides the plugin system for workflow quality assessment.
"""

from .quality_assessment_plugin import QualityAssessmentPlugin
from .quality_assessment_manager import QualityAssessmentManager
from .quality_assessment import (
    CompletenessPlugin,
    UsabilityPlugin,
    MaintainabilityPlugin,
    DocumentationPlugin,
    ExtensibilityPlugin,
)

__all__ = [
    "QualityAssessmentPlugin",
    "QualityAssessmentManager",
    "CompletenessPlugin",
    "UsabilityPlugin",
    "MaintainabilityPlugin",
    "DocumentationPlugin",
    "ExtensibilityPlugin",
]
