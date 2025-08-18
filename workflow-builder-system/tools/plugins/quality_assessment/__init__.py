"""
质量评估插件包

包含所有标准的质量评估维度插件。

插件列表:
- CompletenessPlugin: 完整性评估
- UsabilityPlugin: 易用性评估
- MaintainabilityPlugin: 可维护性评估
- DocumentationPlugin: 文档质量评估
- ExtensibilityPlugin: 扩展性评估
"""

from .completeness_plugin import CompletenessPlugin
from .usability_plugin import UsabilityPlugin
from .maintainability_plugin import MaintainabilityPlugin
from .documentation_plugin import DocumentationPlugin
from .extensibility_plugin import ExtensibilityPlugin

__all__ = [
    "CompletenessPlugin",
    "UsabilityPlugin",
    "MaintainabilityPlugin",
    "DocumentationPlugin",
    "ExtensibilityPlugin",
]
