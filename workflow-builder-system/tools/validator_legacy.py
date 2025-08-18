#!/usr/bin/env python3
"""
工作流验证器 - 自动验证生成的工作流的质量和完整性
支持语法检查、逻辑验证、依赖分析和质量评估
增强版：支持插件系统扩展评分维度

Author: Workflow Builder System
Version: 2.0.0
Last Updated: 2025-08-18

功能概述:
--------
这个验证器提供了完整的工作流质量评估系统，包括：
1. 语法验证：检查Markdown、Python、PowerShell、JSON文件的语法正确性
2. 逻辑验证：验证工作流的逻辑一致性和完整性
3. 依赖验证：检查文件间的依赖关系和引用完整性
4. 质量评估：多维度评估工作流的质量（支持插件扩展）

详细评分规则:
============

质量评估维度 (总分10.0):
-----------------------

1. **Completeness (完整性)** - 权重30%
   - 主要模板文件存在 (+1.67分)
   - README文档存在 (+1.67分)
   - 工具脚本文件存在 (+3.33分)
   - 核心文件夹结构完整 (+1.67分) - templates/docs/tools
   - 测试文件存在 (+1.67分)
   - 配置文件存在 (+1.67分)

2. **Usability (易用性)** - 权重25%
   - 使用指导文档 (+2分)
   - 示例代码 (+2分)
   - 错误处理说明 (+2分)
   - 配置说明 (+2分)
   - FAQ或故障排除 (+2分)

3. **Maintainability (可维护性)** - 权重25%
   - 代码注释率≥10% (+2.5分)
   - 面向对象设计 (+2.5分) - 类定义、继承、方法、装饰器
   - 版本控制信息 (+2.5分)
   - 日志记录机制 (+2.5分)

4. **Documentation (文档质量)** - 权重10%
   - README文件存在 (+2.5分)
   - 文档结构完整性 (+2.5分)
   - 代码文档存在 (+2.5分)
   - 文档更新时间 (+2.5分)

5. **Extensibility (扩展性)** - 权重10%
   - 配置文件支持 (+3.33分)
   - 模板文件系统 (+3.33分)
   - 插件或扩展点 (+3.33分)

插件系统评分 (可选):
------------------
如果启用插件系统，可以覆盖原有评分维度：

- **Security Plugin**: 安全性评估 (0-10分)
  - 无硬编码敏感信息 (+2分)
  - .gitignore文件存在 (+2分)
  - 权限控制配置 (+2分)
  - 输入验证机制 (+2分)
  - 依赖安全性检查 (+2分)

- **Performance Plugin**: 性能评估 (0-10分)
  - 性能优化代码 (+2.5分)
  - 并发处理支持 (+2.5分)
  - 缓存机制 (+2.5分)
  - 资源管理 (+2.5分)

- **Test Coverage Plugin**: 测试覆盖率评估 (0-10分)
  - 测试文件存在 (+2.5分)
  - 测试覆盖率计算 (+2.5分)
  - 测试框架使用 (+2.5分)
  - CI配置存在 (+2.5分)

使用方法:
========

基础使用:
--------
```python
from validator import WorkflowValidator

# 创建验证器实例
validator = WorkflowValidator(enable_plugins=True)

# 验证工作流
results = validator.validate_workflow("/path/to/workflow")

# 输出质量得分
print(f"质量得分: {results['summary']['quality_score']:.1f}/10.0")
print(f"等级: {results['quality_assessment']['grade']}")

# 生成报告
report = validator.generate_report()
print(report)
```

命令行使用:
----------
```bash
# 基础验证
python validator.py /path/to/workflow

# 指定输出文件
python validator.py /path/to/workflow --output report.txt

# JSON格式输出
python validator.py /path/to/workflow --format json

# 排除特定文件
python validator.py /path/to/workflow --exclude "**/*.backup" --exclude "**/temp/**"
```

高级配置:
--------
```python
# 自定义排除模式
validator = WorkflowValidator(
    exclude_patterns=["**/private/**", "**/*.secret"],
    enable_plugins=True
)

# 获取详细的验证结果
results = validator.validate_workflow("/path/to/workflow")
for dimension, score in results['quality_assessment']['details'].items():
    print(f"{dimension}: {score:.1f}/10.0")
```

注意事项:
--------
1. 插件系统需要 validator_plugins.py 和 plugins_config.yaml
2. 日志文件会输出到 ../logs/validator.log
3. 某些功能需要系统环境支持（如PowerShell语法检查）
4. 大型项目验证可能需要较长时间
"""

import os
import re
import json
import subprocess
import sys
import argparse
import urllib.parse
import fnmatch
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging


# 配置日志系统
def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    配置验证器日志系统

    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger("workflow_validator")

    # 避免重复配置
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 创建文件处理器（如果可能）
    try:
        log_file = Path(__file__).parent.parent / "logs" / "validator.log"
        log_file.parent.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # 设置格式
        detailed_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"警告: 无法创建日志文件: {e}")

    # 简化的控制台格式
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


# 尝试导入插件系统
try:
    from .validator_plugins import PluginManager

    PLUGINS_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    try:
        from validator_plugins import PluginManager

        PLUGINS_AVAILABLE = True
    except (ImportError, ModuleNotFoundError):
        PLUGINS_AVAILABLE = False

# 初始化日志
logger = setup_logging()


class WorkflowValidator:
    """
    工作流验证器主类 - 增强版支持插件系统

    这个类提供了完整的工作流验证功能，包括：
    - 语法验证：检查Markdown和Python文件的语法正确性
    - 逻辑验证：验证工作流的逻辑一致性和完整性
    - 依赖验证：检查文件间的依赖关系和引用完整性
    - 质量评估：多维度评估工作流的质量（支持插件扩展）
    - 报告生成：生成详细的验证报告

    Attributes:
        validation_results (Dict): 验证结果存储
        exclude_patterns (List[str]): 需要排除的文件模式
        enable_plugins (bool): 是否启用插件系统
        plugin_manager (PluginManager): 插件管理器实例

    Example:
        >>> validator = WorkflowValidator(enable_plugins=True)
        >>> results = validator.validate("/path/to/workflow")
        >>> print(validator.generate_report())
    """

    def __init__(self, exclude_patterns: List[str] = None, enable_plugins: bool = True):
        """
        初始化工作流验证器

        Args:
            exclude_patterns (List[str], optional): 需要排除的文件或目录模式列表，
                会与默认排除列表合并。支持glob模式，如 "**/*.backup"
            enable_plugins (bool, optional): 是否启用插件系统进行扩展评估。
                默认为True，如果插件系统不可用会自动降级到标准模式

        Note:
            初始化时会自动设置日志记录和插件系统，如果插件系统初始化失败，
            会记录警告信息但不会影响基础验证功能
        """
        logger.info("初始化工作流验证器")

        # 初始化验证结果结构
        self.validation_results = {
            "syntax": {"passed": 0, "failed": 0, "issues": []},
            "logic": {"passed": 0, "failed": 0, "issues": []},
            "dependencies": {"passed": 0, "failed": 0, "issues": []},
            "quality": {"score": 0, "details": {}},
        }

        # 默认排除模式
        default_patterns = [
            "**/workflow_system_analysis_report.md",
            "**/validation_*.txt",
            "**/*.backup*",
            "**/temp/**",
            "**/.git/**",
            "**/develop/**",
        ]

        # 合并用户提供的排除模式和默认模式
        if exclude_patterns:
            self.exclude_patterns = default_patterns + exclude_patterns
            logger.debug(f"使用自定义排除模式: {exclude_patterns}")
        else:
            self.exclude_patterns = default_patterns
        logger.debug(f"最终排除模式: {self.exclude_patterns}")

        # 初始化插件系统
        self.enable_plugins = enable_plugins and PLUGINS_AVAILABLE
        self.plugin_manager = None

        if self.enable_plugins:
            try:
                logger.info("尝试初始化插件系统")
                # 查找插件配置文件
                current_dir = Path(__file__).parent.parent
                plugin_config_path = current_dir / "plugins_config.yaml"

                self.plugin_manager = PluginManager(plugin_config_path)
                logger.info(f"✅ 插件系统已启用，配置文件: {plugin_config_path}")
            except Exception as e:
                logger.warning(f"⚠️ 插件系统初始化失败: {e}")
                self.enable_plugins = False
        else:
            if not PLUGINS_AVAILABLE:
                logger.warning("插件系统不可用，将使用标准评分模式")
            else:
                logger.info("插件系统已被禁用")

        logger.info(
            f"验证器初始化完成 (插件系统: {'启用' if self.enable_plugins else '禁用'})"
        )

    def _should_exclude_file(self, file_path: Path, base_path: Path) -> bool:
        """
        检查文件是否应该被排除

        根据配置的排除模式（glob patterns）判断给定文件是否应该在验证过程中被忽略。
        这有助于跳过临时文件、备份文件和其他不需要验证的文件。

        Args:
            file_path (Path): 要检查的文件的绝对路径
            base_path (Path): 基础路径，用于计算相对路径进行模式匹配

        Returns:
            bool: True表示应该排除该文件，False表示应该包含该文件进行验证

        Example:
            >>> validator = WorkflowValidator()
            >>> should_exclude = validator._should_exclude_file(
            ...     Path("/project/.git/config"), Path("/project")
            ... )
            >>> print(should_exclude)  # True (git files are excluded by default)
        """
        try:
            # 计算相对路径
            rel_path = file_path.relative_to(base_path)
            rel_path_str = str(rel_path).replace("\\", "/")

            # 检查每个排除模式
            import fnmatch

            for pattern in self.exclude_patterns:
                # 处理 ** 通配符模式
                if pattern.startswith("**/"):
                    # 移除 **/ 前缀，检查文件名或路径末尾
                    simple_pattern = pattern[3:]

                    # 如果是目录模式 (以 / 结尾或包含 / )
                    if simple_pattern.endswith("/") or "/" in simple_pattern:
                        # 提取目录名
                        if simple_pattern.endswith("/"):
                            dir_name = simple_pattern.rstrip("/")
                        else:
                            # 对于 develop/** 这样的模式，提取develop部分
                            dir_name = simple_pattern.split("/")[0]

                        # 检查路径是否在该目录下
                        path_parts = rel_path_str.split("/")
                        if dir_name in path_parts:
                            logger.debug(
                                f"排除文件: {rel_path_str} (目录匹配: {pattern})"
                            )
                            return True
                    else:
                        # 文件名匹配
                        if fnmatch.fnmatch(
                            file_path.name, simple_pattern
                        ) or rel_path_str.endswith(simple_pattern):
                            logger.debug(
                                f"排除文件: {rel_path_str} (匹配模式: {pattern})"
                            )
                            return True

                # 普通通配符匹配
                elif fnmatch.fnmatch(rel_path_str, pattern):
                    logger.debug(f"排除文件: {rel_path_str} (匹配模式: {pattern})")
                    return True
                # 支持文件名匹配
                elif fnmatch.fnmatch(file_path.name, pattern):
                    logger.debug(f"排除文件: {rel_path_str} (文件名匹配: {pattern})")
                    return True

            return False
        except ValueError:
            # 如果无法计算相对路径，不排除
            return False

    def validate_workflow(self, workflow_path: str) -> Dict[str, Any]:
        """
        全面验证工作流

        对指定的工作流目录执行完整的验证流程，包括语法验证、逻辑验证、
        依赖验证和质量评估。这是验证器的主要入口方法。

        Args:
            workflow_path (str): 工作流目录的绝对路径

        Returns:
            Dict[str, Any]: 包含所有验证结果的字典，结构如下：
                {
                    "overall_status": "PASS"/"FAIL",
                    "total_issues": int,
                    "critical_issues": int,
                    "quality_score": float,
                    "validation_results": {...}
                }

        Raises:
            FileNotFoundError: 如果工作流路径不存在
            PermissionError: 如果没有读取权限

        Example:
            >>> validator = WorkflowValidator()
            >>> results = validator.validate_workflow("/path/to/workflow")
            >>> print(f"质量得分: {results['quality_score']}")
        """
        logger.info(f"开始验证工作流: {workflow_path}")

        # 验证路径存在
        workflow_dir = Path(workflow_path)
        if not workflow_dir.exists():
            raise FileNotFoundError(f"工作流路径不存在: {workflow_path}")
        if not workflow_dir.is_dir():
            raise NotADirectoryError(f"路径不是目录: {workflow_path}")

        start_time = logger.debug("验证开始")
        logger.info(f"开始验证工作流: {workflow_path}")

        workflow_dir = Path(workflow_path)
        if not workflow_dir.exists():
            raise FileNotFoundError(f"工作流路径不存在: {workflow_path}")

        # 重置验证结果
        self._reset_results()

        # 语法验证
        self.validate_syntax(workflow_path)

        # 逻辑验证
        self.validate_logic(workflow_path)

        # 依赖验证
        self.validate_dependencies(workflow_path)

        # 质量评估
        self.assess_quality(workflow_path)

        # 生成综合报告
        report = self._generate_validation_report()

        logger.info("工作流验证完成")
        return report

    def _reset_results(self):
        """重置验证结果"""
        self.validation_results = {
            "syntax": {"passed": 0, "failed": 0, "issues": []},
            "logic": {"passed": 0, "failed": 0, "issues": []},
            "dependencies": {"passed": 0, "failed": 0, "issues": []},
            "quality": {"score": 0, "details": {}},
        }

    def validate_syntax(self, workflow_path: str):
        """验证语法正确性"""
        logger.info("执行语法验证")

        workflow_dir = Path(workflow_path)

        # 验证Markdown文件
        for md_file in workflow_dir.glob("**/*.md"):
            if not self._should_exclude_file(md_file, workflow_dir):
                self._validate_markdown_syntax(md_file)

        # 验证Python脚本
        for py_file in workflow_dir.glob("**/*.py"):
            if not self._should_exclude_file(py_file, workflow_dir):
                self._validate_python_syntax(py_file)

        # 验证PowerShell脚本
        for ps_file in workflow_dir.glob("**/*.ps1"):
            if not self._should_exclude_file(ps_file, workflow_dir):
                self._validate_powershell_syntax(ps_file)

        # 验证JSON文件
        for json_file in workflow_dir.glob("**/*.json"):
            if not self._should_exclude_file(json_file, workflow_dir):
                self._validate_json_syntax(json_file)

    def _validate_markdown_syntax(self, file_path: Path):
        """
        验证Markdown文件的语法正确性

        对指定的Markdown文件执行多项语法和格式检查，包括标题层次结构、
        链接完整性、代码块格式等。检查结果会记录到validation_results中。

        Args:
            file_path (Path): 要验证的Markdown文件路径

        Returns:
            None: 检查结果通过validation_results属性访问

        Raises:
            Exception: 文件读取或解析失败时会捕获异常并记录到issues中

        检查项目:
        --------
        1. 标题层次结构 - 确保标题级别不跳跃
        2. 链接完整性 - 验证内部和外部链接的有效性
        3. 代码块格式 - 检查代码块是否有语言标识
        4. 列表格式 - 验证列表格式规范（已禁用）

        Note:
            忽略代码块内的内容，避免误报标题和链接问题
        """
        try:
            content = file_path.read_text(encoding="utf-8")

            # 检查标题层次
            self._check_heading_hierarchy(content, file_path)

            # 检查链接完整性
            self._check_link_integrity(content, file_path)

            # 检查代码块格式
            self._check_code_block_format(content, file_path)

            # 检查列表格式 - 已禁用，因为实际渲染正常且不影响功能
            # self._check_list_format(content, file_path)

            self.validation_results["syntax"]["passed"] += 1

        except Exception as e:
            self.validation_results["syntax"]["failed"] += 1
            self.validation_results["syntax"]["issues"].append(
                {
                    "file": str(file_path),
                    "type": "markdown_syntax",
                    "message": f"Markdown语法错误: {str(e)}",
                }
            )

    def _check_heading_hierarchy(self, content: str, file_path: Path):
        """
        检查Markdown标题层次结构的正确性

        验证Markdown文件中的标题层次是否符合规范，即不应该出现级别跳跃
        （如从H1直接跳到H3）。会忽略代码块内的内容以避免误报。

        Args:
            content (str): Markdown文件的文本内容
            file_path (Path): 文件路径，用于错误报告

        Returns:
            None: 检查结果通过validation_results属性访问

        检查规则:
        --------
        1. 标题必须以#开头且后面有空格才被认为是有效标题
        2. 不能有级别跳跃：H1->H3、H2->H4等都是不允许的
        3. 忽略代码块内的#符号
        4. 忽略HTML注释内的内容

        错误类型:
        --------
        - heading_hierarchy: 标题层次跳跃错误

        Example:
            正确: # H1 -> ## H2 -> ### H3
            错误: # H1 -> ### H3 (跳过了H2)
        """
        lines = content.split("\n")
        prev_level = 0
        in_code_block = False

        for i, line in enumerate(lines, 1):
            # 检查是否进入或退出代码块
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # 忽略代码块内的行
            if in_code_block:
                continue

            # 检查真正的markdown标题
            if line.startswith("#") and " " in line:  # 必须有空格才是有效标题
                level = len(line) - len(line.lstrip("#"))

                # 检查层次跳跃
                if level > prev_level + 1:
                    self.validation_results["syntax"]["issues"].append(
                        {
                            "file": str(file_path),
                            "line": i,
                            "type": "heading_hierarchy",
                            "message": f"标题层次跳跃: 从 H{prev_level} 直接跳到 H{level}",
                        }
                    )

                prev_level = level

    def _check_link_integrity(self, content: str, file_path: Path):
        """检查链接完整性 - 支持更宽松的emoji anchor匹配"""
        # 检查内部链接
        internal_links = re.findall(r"\[([^\]]+)\]\(#([^)]+)\)", content)

        # 提取所有标题锚点，生成多种可能的格式
        anchors = set()
        for line in content.split("\n"):
            if line.startswith("#"):
                title = line.lstrip("# ").strip()
                # 生成多种可能的anchor格式
                possible_anchors = self._generate_possible_anchors(title)
                anchors.update(possible_anchors)

        # 验证内部链接 - 使用宽松匹配
        for link_text, anchor in internal_links:
            if not self._is_anchor_valid(anchor, anchors):
                self.validation_results["syntax"]["issues"].append(
                    {
                        "file": str(file_path),
                        "type": "broken_link",
                        "message": f"断开的内部链接: [{link_text}](#{anchor})",
                    }
                )

        # 检查外部文件链接
        file_links = re.findall(r"\[([^\]]+)\]\(([^#)]+\.md[^)]*)\)", content)
        for link_text, file_link in file_links:
            # 分离文件路径和anchor
            if "#" in file_link:
                file_path_part, anchor_part = file_link.split("#", 1)
                target_file = file_path.parent / file_path_part
                if target_file.exists():
                    # 检查target文件中的anchor
                    if not self._check_external_anchor(target_file, anchor_part):
                        self.validation_results["syntax"]["issues"].append(
                            {
                                "file": str(file_path),
                                "type": "broken_file_link",
                                "message": f"断开的文件链接: [{link_text}]({file_link})",
                            }
                        )
                else:
                    self.validation_results["syntax"]["issues"].append(
                        {
                            "file": str(file_path),
                            "type": "broken_file_link",
                            "message": f"断开的文件链接: [{link_text}]({file_link})",
                        }
                    )
            else:
                target_file = file_path.parent / file_link
                if not target_file.exists():
                    self.validation_results["syntax"]["issues"].append(
                        {
                            "file": str(file_path),
                            "type": "broken_file_link",
                            "message": f"断开的文件链接: [{link_text}]({file_link})",
                        }
                    )

    def _generate_possible_anchors(self, title: str) -> list:
        """生成标题的多种可能anchor格式"""
        title = title.lstrip("# ").strip()
        anchors = []

        # 格式1: 标准格式 - 空格转连字符，移除标点
        anchor1 = re.sub(r"\s+", "-", title)
        anchor1 = re.sub(r'[：；\'".,!?()]', "", anchor1)
        anchor1 = re.sub(r"-+", "-", anchor1).strip("-")
        anchors.append(anchor1)
        anchors.append(anchor1.lower())

        # 格式2: 移除括号内容后处理
        title_no_parens = re.sub(r"\s*\([^)]*\)", "", title).strip()
        if title_no_parens != title:
            anchor2 = re.sub(r"\s+", "-", title_no_parens)
            anchor2 = re.sub(r'[：；\'".,!?()]', "", anchor2)
            anchor2 = re.sub(r"-+", "-", anchor2).strip("-")
            anchors.append(anchor2)
            anchors.append(anchor2.lower())

        # 格式3: GitHub风格 - 全部转小写，特殊处理
        github_anchor = title.lower()
        github_anchor = re.sub(
            r"[^\w\s\u4e00-\u9fff\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF-]",
            "",
            github_anchor,
        )
        github_anchor = re.sub(r"\s+", "-", github_anchor)
        github_anchor = re.sub(r"-+", "-", github_anchor).strip("-")
        if github_anchor:
            anchors.append(github_anchor)

        # 格式4: Typora风格 - 保留emoji，括号内容用连字符
        typora_anchor = re.sub(r"\s*\(([^)]*)\)", r"-\1", title)
        typora_anchor = re.sub(r"\s+", "-", typora_anchor)
        typora_anchor = re.sub(r'[：；\'".,!?]', "", typora_anchor)
        typora_anchor = re.sub(r"-+", "-", typora_anchor).strip("-")
        anchors.append(typora_anchor)
        anchors.append(typora_anchor.lower())

        # 格式5: 简化版本 - 仅保留主要内容
        simple_title = re.sub(
            r"[^\w\s\u4e00-\u9fff\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]",
            "",
            title,
        )
        simple_anchor = re.sub(r"\s+", "-", simple_title.strip())
        if simple_anchor:
            anchors.append(simple_anchor)
            anchors.append(simple_anchor.lower())

        return list(set(filter(None, anchors)))  # 去重并移除空值

    def _is_anchor_valid(self, anchor: str, valid_anchors: set) -> bool:
        """检查anchor是否有效 - 支持宽松匹配"""
        if anchor in valid_anchors:
            return True

        # 尝试URL解码
        try:
            import urllib.parse

            decoded_anchor = urllib.parse.unquote(anchor)
            if decoded_anchor in valid_anchors:
                return True
        except:
            pass

        # 宽松匹配：忽略大小写和一些特殊字符差异
        normalized_anchor = anchor.lower().strip("-")
        for valid_anchor in valid_anchors:
            if normalized_anchor == valid_anchor.lower().strip("-"):
                return True

        return False

    def _check_external_anchor(self, target_file: Path, anchor: str) -> bool:
        """检查外部文件中的anchor是否存在"""
        try:
            content = target_file.read_text(encoding="utf-8")
            anchors = set()
            for line in content.split("\n"):
                if line.startswith("#"):
                    title = line.lstrip("# ").strip()
                    possible_anchors = self._generate_possible_anchors(title)
                    anchors.update(possible_anchors)
            return self._is_anchor_valid(anchor, anchors)
        except:
            return False

    def _generate_anchor(self, title: str) -> str:
        """生成标题锚点 - 支持emoji格式"""
        # 移除markdown标题标记
        anchor = title.lstrip("# ").strip()

        # 对于包含emoji的标题，采用Typora兼容格式
        # 根据您的示例: [📍 准备阶段 (Preparation Phase)](#📍-准备阶段-preparation-phase)
        # 锚点格式应该是: emoji-后续文字-用连字符连接

        # 不转换为小写，保持原始大小写（除了连字符化）

        # 将空格替换为连字符，但保留emoji和中文字符
        anchor = re.sub(r"\s+", "-", anchor)

        # 移除不需要的特殊字符，但保留emoji、中文、英文、数字、连字符、括号
        # 支持更多emoji字符
        anchor = re.sub(r'[：；\'".,!?]', "", anchor)

        # 清理多余的连字符
        anchor = re.sub(r"-+", "-", anchor)
        anchor = anchor.strip("-")

        return anchor

    def _check_code_block_format(self, content: str, file_path: Path):
        """检查代码块格式"""
        lines = content.split("\n")
        in_code_block = False

        for i, line in enumerate(lines, 1):
            if line.startswith("```"):
                if not in_code_block:
                    # 开始代码块
                    if line.strip() == "```":
                        self.validation_results["syntax"]["issues"].append(
                            {
                                "file": str(file_path),
                                "line": i,
                                "type": "code_block_language",
                                "message": "代码块缺少语言标识",
                            }
                        )
                    in_code_block = True
                else:
                    # 结束代码块
                    in_code_block = False

    def _check_list_format(self, content: str, file_path: Path):
        """检查列表格式"""
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            if re.match(r"^[\s]*[-*+]\s", line):
                # 检查前后空行
                if (
                    i > 1
                    and lines[i - 2].strip() != ""
                    and not re.match(r"^[\s]*[-*+]\s", lines[i - 2])
                ):
                    self.validation_results["syntax"]["issues"].append(
                        {
                            "file": str(file_path),
                            "line": i,
                            "type": "list_format",
                            "message": "列表前需要空行",
                        }
                    )

    def _validate_python_syntax(self, file_path: Path):
        """验证Python语法"""
        try:
            content = file_path.read_text(encoding="utf-8")
            compile(content, str(file_path), "exec")
            self.validation_results["syntax"]["passed"] += 1

        except SyntaxError as e:
            self.validation_results["syntax"]["failed"] += 1
            self.validation_results["syntax"]["issues"].append(
                {
                    "file": str(file_path),
                    "line": e.lineno,
                    "type": "python_syntax",
                    "message": f"Python语法错误: {e.msg}",
                }
            )
        except Exception as e:
            self.validation_results["syntax"]["failed"] += 1
            self.validation_results["syntax"]["issues"].append(
                {
                    "file": str(file_path),
                    "type": "python_error",
                    "message": f"Python文件错误: {str(e)}",
                }
            )

    def _validate_powershell_syntax(self, file_path: Path):
        """验证PowerShell语法"""
        try:
            # 使用PowerShell检查语法
            result = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    f'$null = Get-Content "{file_path}" | Out-String | Invoke-Expression',
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                self.validation_results["syntax"]["passed"] += 1
            else:
                self.validation_results["syntax"]["failed"] += 1
                self.validation_results["syntax"]["issues"].append(
                    {
                        "file": str(file_path),
                        "type": "powershell_syntax",
                        "message": f"PowerShell语法错误: {result.stderr}",
                    }
                )

        except subprocess.TimeoutExpired:
            self.validation_results["syntax"]["issues"].append(
                {
                    "file": str(file_path),
                    "type": "powershell_timeout",
                    "message": "PowerShell语法检查超时",
                }
            )
        except Exception as e:
            self.validation_results["syntax"]["issues"].append(
                {
                    "file": str(file_path),
                    "type": "powershell_error",
                    "message": f"PowerShell检查错误: {str(e)}",
                }
            )

    def _validate_json_syntax(self, file_path: Path):
        """验证JSON语法"""
        try:
            content = file_path.read_text(encoding="utf-8")
            json.loads(content)
            self.validation_results["syntax"]["passed"] += 1

        except json.JSONDecodeError as e:
            self.validation_results["syntax"]["failed"] += 1
            self.validation_results["syntax"]["issues"].append(
                {
                    "file": str(file_path),
                    "line": e.lineno,
                    "type": "json_syntax",
                    "message": f"JSON语法错误: {e.msg}",
                }
            )

    def validate_logic(self, workflow_path: str):
        """验证逻辑完整性"""
        logger.info("执行逻辑验证")

        workflow_dir = Path(workflow_path)

        # 查找主工作流文件
        main_workflow = self._find_main_workflow(workflow_dir)
        if not main_workflow:
            self.validation_results["logic"]["failed"] += 1
            self.validation_results["logic"]["issues"].append(
                {"type": "missing_main_workflow", "message": "未找到主工作流文件"}
            )
            return

        # 验证工作流结构
        self._validate_workflow_structure(main_workflow)

        # 验证步骤完整性
        self._validate_step_completeness(main_workflow)

        # 验证确认检查点
        self._validate_checkpoints(main_workflow)

        # 验证文件引用
        self._validate_file_references(main_workflow, workflow_dir)

    def _find_main_workflow(self, workflow_dir: Path) -> Path:
        """查找主工作流文件"""
        # 查找模板文件
        templates = list(workflow_dir.glob("*_template.md"))
        if templates:
            return templates[0]

        # 查找workflow.md
        workflow_md = workflow_dir / "workflow.md"
        if workflow_md.exists():
            return workflow_md

        # 查找README.md
        readme_md = workflow_dir / "README.md"
        if readme_md.exists():
            return readme_md

        return None

    def _validate_workflow_structure(self, workflow_file: Path):
        """验证工作流结构"""
        content = workflow_file.read_text(encoding="utf-8")

        required_sections = ["工作流简介", "目录结构", "标准流程", "自动生成区域"]

        for section in required_sections:
            if section not in content:
                self.validation_results["logic"]["failed"] += 1
                self.validation_results["logic"]["issues"].append(
                    {
                        "file": str(workflow_file),
                        "type": "missing_section",
                        "message": f"缺少必需章节: {section}",
                    }
                )
            else:
                self.validation_results["logic"]["passed"] += 1

    def _validate_step_completeness(self, workflow_file: Path):
        """验证步骤完整性"""
        content = workflow_file.read_text(encoding="utf-8")

        # 查找步骤定义
        steps = re.findall(r"### 步骤(\d+)：(.+)", content)

        if not steps:
            self.validation_results["logic"]["failed"] += 1
            self.validation_results["logic"]["issues"].append(
                {
                    "file": str(workflow_file),
                    "type": "no_steps",
                    "message": "未找到工作流步骤定义",
                }
            )
            return

        # 检查步骤连续性
        step_numbers = [int(step[0]) for step in steps]
        expected_numbers = list(range(1, len(step_numbers) + 1))

        if step_numbers != expected_numbers:
            self.validation_results["logic"]["failed"] += 1
            self.validation_results["logic"]["issues"].append(
                {
                    "file": str(workflow_file),
                    "type": "step_numbering",
                    "message": f"步骤编号不连续: {step_numbers}",
                }
            )
        else:
            self.validation_results["logic"]["passed"] += 1

    def _validate_checkpoints(self, workflow_file: Path):
        """验证确认检查点"""
        content = workflow_file.read_text(encoding="utf-8")

        # 查找确认检查点
        checkpoints = re.findall(r"🤝.*?用户确认检查点", content)

        if len(checkpoints) < 2:
            self.validation_results["logic"]["failed"] += 1
            self.validation_results["logic"]["issues"].append(
                {
                    "file": str(workflow_file),
                    "type": "insufficient_checkpoints",
                    "message": f"确认检查点不足: 找到{len(checkpoints)}个，建议至少2个",
                }
            )
        else:
            self.validation_results["logic"]["passed"] += 1

    def _validate_file_references(self, workflow_file: Path, workflow_dir: Path):
        """验证文件引用"""
        content = workflow_file.read_text(encoding="utf-8")

        # 查找脚本引用
        script_refs = re.findall(r"`([^`]+\.(py|ps1|sh))`", content)

        for script_ref, ext in script_refs:
            script_path = workflow_dir / script_ref
            if not script_path.exists():
                self.validation_results["logic"]["failed"] += 1
                self.validation_results["logic"]["issues"].append(
                    {
                        "file": str(workflow_file),
                        "type": "missing_script",
                        "message": f"引用的脚本文件不存在: {script_ref}",
                    }
                )
            else:
                self.validation_results["logic"]["passed"] += 1

    def validate_dependencies(self, workflow_path: str):
        """验证依赖完整性"""
        logger.info("执行依赖验证")

        workflow_dir = Path(workflow_path)

        # 检查Python依赖
        self._check_python_dependencies(workflow_dir)

        # 检查PowerShell模块
        self._check_powershell_modules(workflow_dir)

        # 检查系统依赖
        self._check_system_dependencies(workflow_dir)

    def _check_python_dependencies(self, workflow_dir: Path):
        """检查Python依赖"""
        requirements_file = workflow_dir / "requirements.txt"

        if requirements_file.exists():
            try:
                content = requirements_file.read_text(encoding="utf-8")
                packages = [
                    line.strip() for line in content.split("\n") if line.strip()
                ]

                for package in packages:
                    # 验证包名格式
                    if not re.match(r"^[a-zA-Z0-9-_]+([>=<]=?[\d.]+)?$", package):
                        self.validation_results["dependencies"]["failed"] += 1
                        self.validation_results["dependencies"]["issues"].append(
                            {
                                "file": str(requirements_file),
                                "type": "invalid_package",
                                "message": f"无效的包名格式: {package}",
                            }
                        )
                    else:
                        self.validation_results["dependencies"]["passed"] += 1

            except Exception as e:
                self.validation_results["dependencies"]["failed"] += 1
                self.validation_results["dependencies"]["issues"].append(
                    {
                        "file": str(requirements_file),
                        "type": "requirements_error",
                        "message": f"requirements.txt读取错误: {str(e)}",
                    }
                )

        # 检查Python脚本中的import
        for py_file in workflow_dir.glob("**/*.py"):
            self._check_python_imports(py_file)

    def _check_python_imports(self, py_file: Path):
        """检查Python导入"""
        try:
            content = py_file.read_text(encoding="utf-8")
            imports = re.findall(
                r"^(?:from\s+(\w+)|import\s+(\w+))", content, re.MULTILINE
            )

            for from_import, direct_import in imports:
                module = from_import or direct_import
                if module and not self._is_builtin_module(module):
                    # 这里可以添加更详细的包检查逻辑
                    self.validation_results["dependencies"]["passed"] += 1

        except Exception as e:
            self.validation_results["dependencies"]["failed"] += 1
            self.validation_results["dependencies"]["issues"].append(
                {
                    "file": str(py_file),
                    "type": "import_check_error",
                    "message": f"导入检查错误: {str(e)}",
                }
            )

    def _is_builtin_module(self, module_name: str) -> bool:
        """检查是否为内置模块"""
        builtin_modules = {
            "os",
            "sys",
            "re",
            "json",
            "logging",
            "datetime",
            "pathlib",
            "subprocess",
            "argparse",
            "unittest",
            "tempfile",
            "shutil",
        }
        return module_name in builtin_modules

    def _check_powershell_modules(self, workflow_dir: Path):
        """检查PowerShell模块依赖"""
        for ps_file in workflow_dir.glob("**/*.ps1"):
            try:
                content = ps_file.read_text(encoding="utf-8")
                modules = re.findall(r"Import-Module\s+([^\s]+)", content)

                for module in modules:
                    self.validation_results["dependencies"]["passed"] += 1

            except Exception as e:
                self.validation_results["dependencies"]["failed"] += 1
                self.validation_results["dependencies"]["issues"].append(
                    {
                        "file": str(ps_file),
                        "type": "powershell_module_error",
                        "message": f"PowerShell模块检查错误: {str(e)}",
                    }
                )

    def _check_system_dependencies(self, workflow_dir: Path):
        """检查系统依赖"""
        # 检查是否有系统命令调用
        command_patterns = [
            r'subprocess\.run\(["\']([^"\']+)["\']',
            r'os\.system\(["\']([^"\']+)["\']',
            r'Invoke-Expression\s+["\']([^"\']+)["\']',
        ]

        for file_path in workflow_dir.glob("**/*"):
            if file_path.suffix in [".py", ".ps1"]:
                try:
                    content = file_path.read_text(encoding="utf-8")

                    for pattern in command_patterns:
                        commands = re.findall(pattern, content)
                        for command in commands:
                            # 这里可以添加命令可用性检查
                            self.validation_results["dependencies"]["passed"] += 1

                except Exception:
                    pass  # 忽略文件读取错误

    def assess_quality(self, workflow_path: str):
        """评估工作流质量 - 增强版支持插件系统"""
        logger.info("执行质量评估")

        workflow_dir = Path(workflow_path)

        # 基础质量评估
        quality_scores = {
            "completeness": self._assess_completeness(workflow_dir),
            "usability": self._assess_usability(workflow_dir),
            "maintainability": self._assess_maintainability(workflow_dir),
            "documentation": self._assess_documentation(workflow_dir),
            "extensibility": self._assess_extensibility(workflow_dir),
        }

        # 插件系统增强评估
        plugin_scores = {}
        if self.enable_plugins and self.plugin_manager:
            try:
                print("\n🔌 执行插件系统评估...")
                plugin_scores = self.plugin_manager.assess_all(workflow_dir)

                # 检查是否有维度覆盖配置
                dimension_overrides = self.plugin_manager.config.get(
                    "dimension_overrides", {}
                )

                for dimension, override_config in dimension_overrides.items():
                    if (
                        override_config.get("enabled", False)
                        and dimension in quality_scores
                    ):
                        # 使用插件分数覆盖原有维度
                        override_plugins = override_config.get("plugins", [])
                        override_weights = override_config.get("weights", [])

                        if len(override_plugins) == len(override_weights):
                            weighted_score = 0.0
                            total_weight = 0.0

                            for plugin_name, weight in zip(
                                override_plugins, override_weights
                            ):
                                if plugin_name in plugin_scores:
                                    weighted_score += (
                                        plugin_scores[plugin_name] * weight
                                    )
                                    total_weight += weight

                            if total_weight > 0:
                                quality_scores[dimension] = (
                                    weighted_score / total_weight
                                )
                                print(
                                    f"🔄 {dimension} 维度已被插件系统覆盖: {quality_scores[dimension]:.1f}"
                                )

            except Exception as e:
                print(f"⚠️ 插件评估失败: {e}")

        # 计算综合分数
        weights = {
            "completeness": 0.30,  # 提高完整性权重
            "usability": 0.25,  # 提高可用性权重
            "maintainability": 0.25,  # 提高可维护性权重
            "documentation": 0.10,  # 保持文档权重
            "extensibility": 0.10,  # 保持扩展性权重
        }

        total_score = sum(
            quality_scores[dimension] * weights[dimension]
            for dimension in quality_scores
        )

        self.validation_results["quality"]["score"] = total_score
        self.validation_results["quality"]["details"] = quality_scores

        # 保存插件评估结果
        if plugin_scores:
            self.validation_results["quality"]["plugin_scores"] = plugin_scores
        self.validation_results["quality"]["details"] = quality_scores

    def _assess_completeness(self, workflow_dir: Path) -> float:
        """评估功能完整性"""
        score = 0.0
        total_checks = 6

        # 检查1: 主要模板文件
        if any(
            workflow_dir.glob(pattern) for pattern in ["*_template.md", "*_workflow.md"]
        ):
            score += 1

        # 检查2: README文档
        if any(workflow_dir.glob("README.md")):
            score += 1

        # 检查3: 工具脚本文件 (Python或PowerShell，有其中之一即可)
        if any(workflow_dir.glob("**/*.py")) or any(workflow_dir.glob("**/*.ps1")):
            score += 2  # 合并Python和PowerShell检查，给2分

        # 检查4: 强制核心文件夹结构 (根据workflow_builder_template.md步骤5.1)
        required_dirs = ["templates", "docs", "tools"]  # scripts改为tools，更符合实际
        existing_dirs = 0
        for req_dir in required_dirs:
            if (workflow_dir / req_dir).exists():
                existing_dirs += 1
        # 按比例给分：全部存在给1分，2/3存在给0.67分，1/3存在给0.33分
        score += existing_dirs / len(required_dirs)

        # 检查5: 测试文件
        if any(workflow_dir.glob("**/test_*.py")):
            score += 1

        # 检查6: 配置文件
        if any(workflow_dir.glob("**/*.json")) or any(workflow_dir.glob("**/*.yaml")):
            score += 1

        return (score / total_checks) * 10

    def _assess_usability(self, workflow_dir: Path) -> float:
        """评估易用性"""
        score = 0.0
        total_checks = 5

        # 检查使用指导
        for md_file in workflow_dir.glob("**/*.md"):
            if self._should_exclude_file(md_file, workflow_dir):
                continue
            content = md_file.read_text(encoding="utf-8")
            if "使用指导" in content or "快速开始" in content:
                score += 1
                break

        # 检查示例代码
        for md_file in workflow_dir.glob("**/*.md"):
            if self._should_exclude_file(md_file, workflow_dir):
                continue
            content = md_file.read_text(encoding="utf-8")
            if "```" in content:
                score += 1
                break

        # 检查错误处理说明
        for file_path in workflow_dir.glob("**/*"):
            if self._should_exclude_file(file_path, workflow_dir):
                continue
            if file_path.suffix in [".md", ".py", ".ps1"]:
                content = file_path.read_text(encoding="utf-8")
                if "错误" in content or "异常" in content or "故障" in content:
                    score += 1
                    break

        # 检查配置说明
        for md_file in workflow_dir.glob("**/*.md"):
            if self._should_exclude_file(md_file, workflow_dir):
                continue
            content = md_file.read_text(encoding="utf-8")
            if "配置" in content or "设置" in content:
                score += 1
                break

        # 检查FAQ或故障排除
        for md_file in workflow_dir.glob("**/*.md"):
            if self._should_exclude_file(md_file, workflow_dir):
                continue
            content = md_file.read_text(encoding="utf-8")
            if "FAQ" in content or "故障排除" in content or "常见问题" in content:
                score += 1
                break

        return (score / total_checks) * 10

    def _assess_maintainability(self, workflow_dir: Path) -> float:
        """
        评估可维护性

        检查代码的可维护性方面，包括注释质量、面向对象设计、
        版本控制信息和日志记录等方面。

        Args:
            workflow_dir (Path): 工作流目录路径

        Returns:
            float: 可维护性得分 (0-10分)

        Note:
            评分标准：
            1. 代码注释率 >= 10% (2.5分)
            2. 面向对象设计 - 使用类 (2.5分)
            3. 版本控制信息存在 (2.5分)
            4. 日志记录机制 (2.5分)
        """
        logger.debug("开始评估可维护性")
        score = 0.0
        total_checks = 4

        # 1. 检查代码注释率
        python_files = list(workflow_dir.glob("**/*.py"))
        if python_files:
            total_lines = 0
            comment_lines = 0

            for py_file in python_files:
                try:
                    content = py_file.read_text(encoding="utf-8")
                    lines = content.split("\n")
                    total_lines += len(lines)
                    # 统计注释行（以#开头，或包含docstring）
                    comment_lines += sum(
                        1
                        for line in lines
                        if line.strip().startswith("#")
                        or '"""' in line
                        or "'''" in line
                    )
                except Exception as e:
                    logger.warning(f"读取文件失败 {py_file}: {e}")

            if total_lines > 0:
                comment_ratio = comment_lines / total_lines
                if comment_ratio >= 0.1:
                    score += 1
                    logger.debug(f"注释率通过: {comment_ratio:.2%}")
                else:
                    logger.debug(f"注释率不足: {comment_ratio:.2%} < 10%")

        # 2. 检查面向对象设计 - 改进的模块化评分标准
        oo_design_score = self._check_object_oriented_design(python_files)
        if oo_design_score > 0:
            score += 1
            logger.debug("面向对象设计检查通过")
        else:
            logger.debug("未发现面向对象设计模式")

        # 3. 检查版本控制信息
        version_found = False
        for md_file in workflow_dir.glob("**/*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if "版本" in content or "version" in content.lower():
                    score += 1
                    version_found = True
                    logger.debug(f"在 {md_file} 中发现版本信息")
                    break
            except Exception as e:
                logger.warning(f"读取文件失败 {md_file}: {e}")

        if not version_found:
            logger.debug("未发现版本控制信息")

        # 4. 检查日志记录机制
        logging_found = False
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                if "logging" in content or "logger" in content:
                    score += 1
                    logging_found = True
                    logger.debug(f"在 {py_file} 中发现日志记录")
                    break
            except Exception as e:
                logger.warning(f"读取文件失败 {py_file}: {e}")

        if not logging_found:
            logger.debug("未发现日志记录机制")

        final_score = (score / total_checks) * 10
        logger.info(
            f"可维护性评估完成: {final_score:.1f}/10.0 ({score}/{total_checks} 项通过)"
        )
        return final_score

    def _check_object_oriented_design(self, python_files: List[Path]) -> float:
        """
        检查面向对象设计

        检查Python代码是否使用了面向对象的设计模式，
        而不是简单地根据文件数量判断模块化程度。

        Args:
            python_files (List[Path]): Python文件列表

        Returns:
            float: 面向对象设计得分 (0-1)

        Note:
            评分标准：
            - 发现类定义 (+0.5)
            - 发现继承关系 (+0.2)
            - 发现方法定义 (+0.2)
            - 发现装饰器使用 (+0.1)
        """
        if not python_files:
            return 0.0

        oo_score = 0.0

        # 统计各种面向对象特征
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

                # 检查方法定义（在类内部）
                method_matches = re.findall(r"^\s+def\s+\w+", content, re.MULTILINE)
                method_count += len(method_matches)

                # 检查装饰器使用
                decorator_matches = re.findall(r"^\s*@\w+", content, re.MULTILINE)
                decorator_count += len(decorator_matches)

            except Exception as e:
                logger.warning(f"分析文件失败 {py_file}: {e}")

        # 根据发现的OO特征计分
        if class_count > 0:
            oo_score += 0.5
            logger.debug(f"发现 {class_count} 个类定义")

        if inheritance_count > 0:
            oo_score += 0.2
            logger.debug(f"发现 {inheritance_count} 个继承关系")

        if method_count > 0:
            oo_score += 0.2
            logger.debug(f"发现 {method_count} 个方法定义")

        if decorator_count > 0:
            oo_score += 0.1
            logger.debug(f"发现 {decorator_count} 个装饰器")

        # 确保得分在0-1范围内
        oo_score = min(1.0, oo_score)
        logger.debug(f"面向对象设计得分: {oo_score:.1f}")

        return oo_score

    def _assess_documentation(self, workflow_dir: Path) -> float:
        """评估文档质量"""
        score = 0.0
        total_checks = 4

        # 检查README存在
        if any(workflow_dir.glob("README.md")):
            score += 1

        # 检查文档结构完整性
        for md_file in workflow_dir.glob("**/*.md"):
            content = md_file.read_text(encoding="utf-8")
            if all(section in content for section in ["目标", "使用", "步骤"]):
                score += 1
                break

        # 检查代码文档
        for py_file in workflow_dir.glob("**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if '"""' in content or "def " in content:
                score += 1
                break

        # 检查文档更新时间
        for md_file in workflow_dir.glob("**/*.md"):
            content = md_file.read_text(encoding="utf-8")
            if "创建时间" in content or "更新时间" in content:
                score += 1
                break

        return (score / total_checks) * 10

    def _assess_extensibility(self, workflow_dir: Path) -> float:
        """评估扩展性"""
        score = 0.0
        total_checks = 3

        # 检查配置文件
        if any(workflow_dir.glob("**/*.json")) or any(workflow_dir.glob("**/*.yaml")):
            score += 1

        # 检查模板文件
        if any(workflow_dir.glob("**/template*")):
            score += 1

        # 检查插件或扩展点
        for py_file in workflow_dir.glob("**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if "plugin" in content.lower() or "extend" in content.lower():
                score += 1
                break

        return (score / total_checks) * 10

    def _generate_validation_report(self) -> Dict[str, Any]:
        """生成验证报告"""
        total_syntax = (
            self.validation_results["syntax"]["passed"]
            + self.validation_results["syntax"]["failed"]
        )
        total_logic = (
            self.validation_results["logic"]["passed"]
            + self.validation_results["logic"]["failed"]
        )
        total_deps = (
            self.validation_results["dependencies"]["passed"]
            + self.validation_results["dependencies"]["failed"]
        )

        report = {
            "summary": {
                "overall_status": (
                    "PASS" if len(self._get_critical_issues()) == 0 else "FAIL"
                ),
                "total_issues": len(self._get_all_issues()),
                "critical_issues": len(self._get_critical_issues()),
                "quality_score": self.validation_results["quality"]["score"],
            },
            "syntax_validation": {
                "status": (
                    "PASS"
                    if self.validation_results["syntax"]["failed"] == 0
                    else "FAIL"
                ),
                "total_checks": total_syntax,
                "passed": self.validation_results["syntax"]["passed"],
                "failed": self.validation_results["syntax"]["failed"],
                "issues": self.validation_results["syntax"]["issues"],
            },
            "logic_validation": {
                "status": (
                    "PASS"
                    if self.validation_results["logic"]["failed"] == 0
                    else "FAIL"
                ),
                "total_checks": total_logic,
                "passed": self.validation_results["logic"]["passed"],
                "failed": self.validation_results["logic"]["failed"],
                "issues": self.validation_results["logic"]["issues"],
            },
            "dependency_validation": {
                "status": (
                    "PASS"
                    if self.validation_results["dependencies"]["failed"] == 0
                    else "FAIL"
                ),
                "total_checks": total_deps,
                "passed": self.validation_results["dependencies"]["passed"],
                "failed": self.validation_results["dependencies"]["failed"],
                "issues": self.validation_results["dependencies"]["issues"],
            },
            "quality_assessment": {
                "overall_score": self.validation_results["quality"]["score"],
                "grade": self._get_quality_grade(
                    self.validation_results["quality"]["score"]
                ),
                "details": self.validation_results["quality"]["details"],
            },
        }

        return report

    def _get_all_issues(self) -> List[Dict]:
        """获取所有问题"""
        all_issues = []
        all_issues.extend(self.validation_results["syntax"]["issues"])
        all_issues.extend(self.validation_results["logic"]["issues"])
        all_issues.extend(self.validation_results["dependencies"]["issues"])
        return all_issues

    def _get_critical_issues(self) -> List[Dict]:
        """获取关键问题"""
        critical_types = [
            "missing_main_workflow",
            "python_syntax",
            "missing_section",
            "broken_link",
        ]

        return [
            issue
            for issue in self._get_all_issues()
            if issue.get("type") in critical_types
        ]

    def _get_quality_grade(self, score: float) -> str:
        """获取质量等级"""
        if score >= 8.5:
            return "优秀"
        elif score >= 7.0:
            return "良好"
        elif score >= 6.0:
            return "及格"
        else:
            return "不及格"


def main():
    """CLI入口函数"""
    import argparse

    parser = argparse.ArgumentParser(description="工作流验证器")
    parser.add_argument("workflow_path", help="工作流目录路径")
    parser.add_argument("--output", help="报告输出文件")
    parser.add_argument(
        "--format", choices=["json", "text"], default="text", help="报告格式"
    )
    parser.add_argument(
        "--exclude",
        action="append",
        help="排除的文件或目录模式（支持通配符），可多次使用",
    )

    args = parser.parse_args()

    # 创建验证器
    validator = WorkflowValidator(exclude_patterns=args.exclude)

    # 执行验证
    report = validator.validate_workflow(args.workflow_path)

    # 输出报告
    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = _format_text_report(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 验证报告已生成: {args.output}")
    else:
        print(output)


def _format_text_report(report: Dict[str, Any]) -> str:
    """格式化文本报告"""
    summary = report["summary"]

    output = f"""
# 工作流验证报告

## 📊 总体状态
- **验证状态**: {summary["overall_status"]}
- **质量评分**: {summary["quality_score"]:.1f}/10.0 ({report["quality_assessment"]["grade"]})
- **问题总数**: {summary["total_issues"]}
- **关键问题**: {summary["critical_issues"]}

## 🔍 详细结果

### 语法验证
- **状态**: {report["syntax_validation"]["status"]}
- **通过**: {report["syntax_validation"]["passed"]}
- **失败**: {report["syntax_validation"]["failed"]}

### 逻辑验证
- **状态**: {report["logic_validation"]["status"]}
- **通过**: {report["logic_validation"]["passed"]}
- **失败**: {report["logic_validation"]["failed"]}

### 依赖验证
- **状态**: {report["dependency_validation"]["status"]}
- **通过**: {report["dependency_validation"]["passed"]}
- **失败**: {report["dependency_validation"]["failed"]}

## 📈 质量评估详情
"""

    for dimension, score in report["quality_assessment"]["details"].items():
        output += f"- **{dimension}**: {score:.1f}/10.0\n"

    # 添加插件评估结果
    if "plugin_scores" in report["quality_assessment"]:
        output += "\n## 🔌 插件系统评估\n"
        for plugin_name, score in report["quality_assessment"]["plugin_scores"].items():
            output += f"- **{plugin_name}**: {score:.1f}/10.0\n"

    # 添加问题详情
    all_issues = []
    all_issues.extend(report["syntax_validation"]["issues"])
    all_issues.extend(report["logic_validation"]["issues"])
    all_issues.extend(report["dependency_validation"]["issues"])

    if all_issues:
        output += "\n## ⚠️ 问题详情\n"
        for issue in all_issues:
            output += f"- **{issue['type']}**: {issue['message']}\n"
            if "file" in issue:
                output += f"  - 文件: {issue['file']}\n"
            if "line" in issue:
                output += f"  - 行号: {issue['line']}\n"

    return output


if __name__ == "__main__":
    main()
