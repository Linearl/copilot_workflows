#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证器插件系统 - 工作流质量验证器的扩展插件框架
Plugin System for Workflow Quality Validator

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18

功能概述:
--------
这个插件系统为工作流验证器提供了可扩展的评分维度和自定义评估规则。
通过插件架构，用户可以：
1. 添加新的评估维度（如安全性、性能、测试覆盖率）
2. 覆盖现有的评分规则
3. 自定义评分权重和配置
4. 动态加载自定义插件

核心组件:
--------

1. **BasePlugin**: 所有插件的抽象基类
   - 定义了插件的基本接口和属性
   - 要求实现assess()方法进行具体评估

2. **内置插件**:
   - SecurityPlugin: 安全性评估插件
   - PerformancePlugin: 性能评估插件
   - TestCoveragePlugin: 测试覆盖率评估插件

3. **PluginManager**: 插件管理器
   - 负责插件的注册、配置和执行
   - 支持从配置文件加载设置
   - 提供加权评分和结果聚合

评分算法:
========

每个插件独立进行评估，返回0-10分的得分。
最终通过PluginManager进行加权平均计算总分。

插件评分标准:
------------

SecurityPlugin (安全性):
- 无硬编码敏感信息 (2分)
- .gitignore文件存在 (2分)
- 权限控制配置 (2分)
- 输入验证机制 (2分)
- 依赖安全性检查 (2分)

PerformancePlugin (性能):
- 性能优化代码 (2.5分)
- 并发处理支持 (2.5分)
- 缓存机制 (2.5分)
- 资源管理 (2.5分)

TestCoveragePlugin (测试覆盖率):
- 测试文件存在 (2.5分)
- 测试覆盖率≥70% (2.5分)
- 测试框架使用 (2.5分)
- CI配置存在 (2.5分)

使用方法:
========

基础使用:
--------
```python
from validator_plugins import PluginManager

# 创建插件管理器
manager = PluginManager("plugins_config.yaml")

# 评估工作流
scores = manager.assess_all(Path("/path/to/workflow"))

# 获取加权总分
total_score = manager.get_weighted_score(scores)

print(f"插件评估结果: {scores}")
print(f"加权总分: {total_score:.1f}/10.0")
```

自定义插件:
----------
```python
from validator_plugins import BasePlugin

class CustomPlugin(BasePlugin):
    def __init__(self):
        super().__init__("custom", "1.0.0")

    @property
    def description(self) -> str:
        return "自定义评估插件"

    def assess(self, workflow_dir: Path) -> float:
        # 实现自定义评估逻辑
        score = 0.0
        # ... 评估代码 ...
        return score

# 注册插件
manager.register_plugin(CustomPlugin())
```

配置文件格式:
------------
```yaml
enabled_plugins:
  - "security"
  - "performance"
  - "test_coverage"

plugin_weights:
  security: 1.5      # 安全性权重更高
  performance: 1.0   # 标准权重
  test_coverage: 1.2 # 测试覆盖率权重较高

dimension_overrides:
  maintainability:
    enabled: true
    plugins: ["security", "test_coverage"]
    weights: [0.6, 0.4]
```

注意事项:
--------
1. 所有插件都必须继承BasePlugin基类
2. assess()方法必须返回0-10范围内的分数
3. 插件执行失败会记录警告但不影响其他插件
4. 配置文件格式必须为有效的YAML
5. 自定义插件应放在plugins/目录下
"""

import os
import json
import yaml
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import importlib.util


class BasePlugin(ABC):
    """
    验证器插件抽象基类

    所有验证器插件都必须继承此基类并实现必要的抽象方法。
    这个基类定义了插件的标准接口和基本属性。

    Attributes:
        name (str): 插件名称，用于标识和配置
        version (str): 插件版本号
        enabled (bool): 插件是否启用

    Abstract Methods:
        assess(): 执行具体的评估逻辑
        description: 插件功能描述属性

    Example:
        >>> class MyPlugin(BasePlugin):
        ...     def __init__(self):
        ...         super().__init__("my_plugin", "1.0.0")
        ...
        ...     @property
        ...     def description(self) -> str:
        ...         return "我的自定义插件"
        ...
        ...     def assess(self, workflow_dir: Path) -> float:
        ...         return 8.0  # 返回评估分数
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        初始化插件基类

        Args:
            name (str): 插件名称，应该是唯一的标识符
            version (str, optional): 插件版本号。默认为"1.0.0"

        Note:
            插件默认处于启用状态，可以通过设置enabled属性来控制
        """
        self.name = name
        self.version = version
        self.enabled = True

    @abstractmethod
    def assess(self, workflow_dir: Path) -> float:
        """
        执行工作流评估

        这是插件的核心方法，用于评估指定工作流目录的质量。

        Args:
            workflow_dir (Path): 要评估的工作流目录路径

        Returns:
            float: 评估分数，必须在0.0-10.0范围内

        Raises:
            NotImplementedError: 子类必须实现此方法

        Note:
            - 返回值应该在0-10范围内
            - 如果评估失败，建议返回0.0而不是抛出异常
            - 可以使用日志记录详细的评估过程
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        插件功能描述

        返回插件的功能描述，用于显示和文档生成。

        Returns:
            str: 插件功能的简短描述

        Example:
            return "评估工作流的安全性配置和敏感信息处理"
        """
        pass

    @property
    def weight(self) -> float:
        """
        插件权重

        返回插件在综合评分中的权重，默认为1.0。
        子类可以重写此方法来设置不同的默认权重。

        Returns:
            float: 插件权重值，通常在0.1-2.0范围内

        Note:
            实际使用的权重可能会被配置文件中的设置覆盖
        """
        return 1.0

    @abstractmethod
    def description(self) -> str:
        """插件描述"""
        pass

    @property
    def weight(self) -> float:
        """插件权重，默认为1.0"""
        return 1.0


class SecurityPlugin(BasePlugin):
    """
    安全性评估插件

    评估工作流的安全性配置和敏感信息处理，包括硬编码检查、
    权限控制、输入验证和依赖安全性等方面。

    评估项目 (总分10分):
    ------------------
    1. 敏感信息硬编码检查 (2分)
       - 检查Python文件中是否有硬编码的密码、密钥等
       - 检查模式: password=, secret=, token=, api_key=, private_key=

    2. .gitignore文件存在 (2分)
       - 确保项目有适当的版本控制忽略文件

    3. 权限控制配置 (2分)
       - 检查config.yaml中是否有安全性或权限相关配置

    4. 输入验证机制 (2分)
       - 检查代码中是否使用了输入验证函数
       - 检查模式: validate, sanitize, isinstance, assert

    5. 依赖安全性 (2分)
       - 检查requirements.txt中是否固定了版本号
       - 要求≥70%的依赖包有固定版本

    Example:
        >>> plugin = SecurityPlugin()
        >>> score = plugin.assess(Path("/path/to/workflow"))
        >>> print(f"安全性得分: {score}/10.0")
    """

    def __init__(self):
        """初始化安全性评估插件"""
        super().__init__("security", "1.0.0")

    @property
    def description(self) -> str:
        """返回插件功能描述"""
        return "评估工作流的安全性配置和敏感信息处理"

    def assess(self, workflow_dir: Path) -> float:
        """
        执行安全性评估

        Args:
            workflow_dir (Path): 工作流目录路径

        Returns:
            float: 安全性得分 (0-10分)

        Note:
            每个检查项目满足条件得2分，最终按比例计算总分
        """
        score = 0.0
        total_checks = 5

        # 1. 检查敏感信息是否硬编码
        if self._check_no_hardcoded_secrets(workflow_dir):
            score += 1

        # 2. 检查是否有.gitignore文件
        if (workflow_dir / ".gitignore").exists():
            score += 1

        # 3. 检查权限控制配置
        if self._check_permission_config(workflow_dir):
            score += 1

        # 4. 检查输入验证
        if self._check_input_validation(workflow_dir):
            score += 1

        # 5. 检查依赖安全性
        if self._check_dependency_security(workflow_dir):
            score += 1

        return (score / total_checks) * 10

    def _check_no_hardcoded_secrets(self, workflow_dir: Path) -> bool:
        """
        检查是否有硬编码的敏感信息

        扫描所有Python文件，查找可能硬编码的敏感信息，如密码、
        API密钥、访问令牌等。

        Args:
            workflow_dir (Path): 工作流目录路径

        Returns:
            bool: True表示没有发现硬编码敏感信息，False表示发现了

        检查模式:
        --------
        - password = "..."
        - secret = '...'
        - token = "..."
        - api_key = "..."
        - private_key = "..."

        Note:
            只检查Python文件，忽略测试文件和示例文件
        """
        sensitive_patterns = ["password", "secret", "token", "api_key", "private_key"]

        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore").lower()
            for pattern in sensitive_patterns:
                if f'{pattern} = "' in content or f"{pattern} = '" in content:
                    return False
        return True

    def _check_permission_config(self, workflow_dir: Path) -> bool:
        """检查权限控制配置"""
        config_file = workflow_dir / "config.yaml"
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    return "security" in config or "permissions" in config
            except:
                pass
        return False

    def _check_input_validation(self, workflow_dir: Path) -> bool:
        """检查输入验证"""
        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(
                pattern in content
                for pattern in ["validate", "sanitize", "isinstance", "assert"]
            ):
                return True
        return False

    def _check_dependency_security(self, workflow_dir: Path) -> bool:
        """检查依赖安全性"""
        requirements_file = workflow_dir / "requirements.txt"
        if requirements_file.exists():
            content = requirements_file.read_text()
            # 检查是否固定版本号
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            pinned_versions = sum(1 for line in lines if "==" in line)
            return pinned_versions / len(lines) >= 0.7 if lines else False
        return True  # 如果没有requirements.txt，认为通过


class PerformancePlugin(BasePlugin):
    """性能评估插件"""

    def __init__(self):
        super().__init__("performance", "1.0.0")

    @property
    def description(self) -> str:
        return "评估工作流的执行性能和效率"

    def assess(self, workflow_dir: Path) -> float:
        """评估性能"""
        score = 0.0
        total_checks = 4

        # 1. 检查是否有性能优化代码
        if self._check_performance_optimizations(workflow_dir):
            score += 1

        # 2. 检查并发处理
        if self._check_concurrency_support(workflow_dir):
            score += 1

        # 3. 检查缓存机制
        if self._check_caching_mechanisms(workflow_dir):
            score += 1

        # 4. 检查资源管理
        if self._check_resource_management(workflow_dir):
            score += 1

        return (score / total_checks) * 10

    def _check_performance_optimizations(self, workflow_dir: Path) -> bool:
        """检查性能优化"""
        optimization_patterns = [
            "lru_cache",
            "functools.cache",
            "asyncio",
            "multiprocessing",
        ]

        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern in content for pattern in optimization_patterns):
                return True
        return False

    def _check_concurrency_support(self, workflow_dir: Path) -> bool:
        """检查并发支持"""
        concurrency_patterns = [
            "threading",
            "asyncio",
            "concurrent.futures",
            "multiprocessing",
        ]

        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern in content for pattern in concurrency_patterns):
                return True
        return False

    def _check_caching_mechanisms(self, workflow_dir: Path) -> bool:
        """检查缓存机制"""
        cache_patterns = ["cache", "memoize", "lru_cache"]

        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern in content for pattern in cache_patterns):
                return True
        return False

    def _check_resource_management(self, workflow_dir: Path) -> bool:
        """检查资源管理"""
        resource_patterns = ["with open", "context manager", "__enter__", "__exit__"]

        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern in content for pattern in resource_patterns):
                return True
        return False


class TestCoveragePlugin(BasePlugin):
    """测试覆盖率评估插件"""

    def __init__(self):
        super().__init__("test_coverage", "1.0.0")

    @property
    def description(self) -> str:
        return "评估工作流的测试覆盖率和测试质量"

    def assess(self, workflow_dir: Path) -> float:
        """评估测试覆盖率"""
        score = 0.0
        total_checks = 4

        # 1. 检查测试文件存在
        if self._check_test_files_exist(workflow_dir):
            score += 1

        # 2. 检查测试覆盖率
        test_coverage = self._calculate_test_coverage(workflow_dir)
        if test_coverage >= 0.7:
            score += 1
        elif test_coverage >= 0.5:
            score += 0.5

        # 3. 检查测试框架
        if self._check_test_framework(workflow_dir):
            score += 1

        # 4. 检查持续集成配置
        if self._check_ci_configuration(workflow_dir):
            score += 1

        return (score / total_checks) * 10

    def _check_test_files_exist(self, workflow_dir: Path) -> bool:
        """检查测试文件"""
        test_patterns = ["**/test_*.py", "**/tests/*.py", "**/*_test.py"]

        for pattern in test_patterns:
            if list(workflow_dir.glob(pattern)):
                return True
        return False

    def _calculate_test_coverage(self, workflow_dir: Path) -> float:
        """计算测试覆盖率（简化版本）"""
        source_files = list(workflow_dir.glob("**/*.py"))
        test_files = []

        test_patterns = ["**/test_*.py", "**/tests/*.py", "**/*_test.py"]
        for pattern in test_patterns:
            test_files.extend(workflow_dir.glob(pattern))

        source_files = [f for f in source_files if f not in test_files]

        if not source_files:
            return 1.0

        return len(test_files) / len(source_files)

    def _check_test_framework(self, workflow_dir: Path) -> bool:
        """检查测试框架"""
        framework_patterns = ["pytest", "unittest", "nose", "doctest"]

        for file_path in workflow_dir.glob("**/*.py"):
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if any(pattern in content for pattern in framework_patterns):
                return True
        return False

    def _check_ci_configuration(self, workflow_dir: Path) -> bool:
        """检查CI配置"""
        ci_files = [
            ".github/workflows/*.yml",
            ".github/workflows/*.yaml",
            ".gitlab-ci.yml",
            "Jenkinsfile",
            ".travis.yml",
        ]

        for pattern in ci_files:
            if list(workflow_dir.glob(pattern)):
                return True
        return False


class PluginManager:
    """插件管理器"""

    def __init__(self, config_path: Optional[Path] = None):
        self.plugins: Dict[str, BasePlugin] = {}
        self.config_path = config_path
        self.load_config()
        self._register_builtin_plugins()

    def load_config(self):
        """加载插件配置"""
        self.config = {
            "enabled_plugins": ["security", "performance", "test_coverage"],
            "plugin_weights": {
                "security": 1.0,
                "performance": 1.0,
                "test_coverage": 1.0,
            },
            "custom_plugins_dir": "plugins/",
        }

        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}
                    self.config.update(user_config)
            except Exception as e:
                print(f"警告: 无法加载插件配置 {self.config_path}: {e}")

    def _register_builtin_plugins(self):
        """注册内置插件"""
        builtin_plugins = [SecurityPlugin(), PerformancePlugin(), TestCoveragePlugin()]

        for plugin in builtin_plugins:
            if plugin.name in self.config["enabled_plugins"]:
                self.register_plugin(plugin)

    def register_plugin(self, plugin: BasePlugin):
        """注册插件"""
        self.plugins[plugin.name] = plugin
        print(f"已注册插件: {plugin.name} v{plugin.version}")

    def load_custom_plugins(self, plugins_dir: Path):
        """加载自定义插件"""
        if not plugins_dir.exists():
            return

        for plugin_file in plugins_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(
                    plugin_file.stem, plugin_file
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 查找插件类
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, BasePlugin)
                        and attr != BasePlugin
                    ):
                        plugin = attr()
                        if plugin.name in self.config["enabled_plugins"]:
                            self.register_plugin(plugin)
                        break
            except Exception as e:
                print(f"警告: 无法加载插件 {plugin_file}: {e}")

    def assess_all(self, workflow_dir: Path) -> Dict[str, float]:
        """执行所有插件评估"""
        results = {}

        for name, plugin in self.plugins.items():
            if plugin.enabled:
                try:
                    score = plugin.assess(workflow_dir)
                    results[name] = min(10.0, max(0.0, score))  # 确保在0-10范围内
                    print(f"插件 {name}: {results[name]:.1f}/10.0")
                except Exception as e:
                    print(f"警告: 插件 {name} 评估失败: {e}")
                    results[name] = 0.0

        return results

    def get_weighted_score(self, scores: Dict[str, float]) -> float:
        """计算加权总分"""
        total_weight = 0.0
        weighted_sum = 0.0

        for name, score in scores.items():
            weight = self.config["plugin_weights"].get(name, 1.0)
            weighted_sum += score * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def list_plugins(self) -> List[Dict[str, Any]]:
        """列出所有插件"""
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "enabled": plugin.enabled,
                "weight": self.config["plugin_weights"].get(plugin.name, 1.0),
            }
            for plugin in self.plugins.values()
        ]


# 示例：自定义插件配置
def create_sample_plugin_config(config_path: Path):
    """创建示例插件配置文件"""
    sample_config = {
        "enabled_plugins": ["security", "performance", "test_coverage"],
        "plugin_weights": {
            "security": 1.5,  # 安全性权重更高
            "performance": 1.0,  # 标准权重
            "test_coverage": 1.2,  # 测试覆盖率权重较高
        },
        "custom_plugins_dir": "plugins/",
        "plugin_settings": {
            "security": {"strict_mode": True, "check_dependencies": True},
            "performance": {"performance_threshold": 0.8},
            "test_coverage": {"minimum_coverage": 0.7},
        },
    }

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(sample_config, f, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    # 示例用法
    workflow_dir = Path(".")
    plugin_manager = PluginManager()

    print("=== 插件系统测试 ===")
    print("\n已注册的插件:")
    for plugin_info in plugin_manager.list_plugins():
        print(
            f"  - {plugin_info['name']} v{plugin_info['version']}: {plugin_info['description']}"
        )

    print(f"\n正在评估工作流: {workflow_dir}")
    scores = plugin_manager.assess_all(workflow_dir)

    print(f"\n=== 评估结果 ===")
    for name, score in scores.items():
        print(f"{name}: {score:.1f}/10.0")

    overall_score = plugin_manager.get_weighted_score(scores)
    print(f"\n加权总分: {overall_score:.1f}/10.0")
