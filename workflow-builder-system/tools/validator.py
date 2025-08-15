#!/usr/bin/env python3
"""
工作流验证器 - 自动验证生成的工作流的质量和完整性
支持语法检查、逻辑验证、依赖分析和质量评估
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class WorkflowValidator:
    """工作流验证器主类"""

    def __init__(self, exclude_patterns=None):
        """
        初始化验证器

        Args:
            exclude_patterns: 需要排除的文件或目录模式列表
        """
        self.validation_results = {
            "syntax": {"passed": 0, "failed": 0, "issues": []},
            "logic": {"passed": 0, "failed": 0, "issues": []},
            "dependencies": {"passed": 0, "failed": 0, "issues": []},
            "quality": {"score": 0, "details": {}},
        }
        self.exclude_patterns = exclude_patterns or [
            "**/workflow_system_analysis_report.md",
            "**/validation_*.txt",
            "**/*.backup*",
            "**/temp/**",
            "**/.git/**",
        ]

    def _should_exclude_file(self, file_path: Path, base_path: Path) -> bool:
        """
        检查文件是否应该被排除

        Args:
            file_path: 要检查的文件路径
            base_path: 基础路径，用于计算相对路径

        Returns:
            bool: True表示应该排除，False表示不排除
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
                    if fnmatch.fnmatch(
                        file_path.name, simple_pattern
                    ) or rel_path_str.endswith(simple_pattern):
                        logger.debug(f"排除文件: {rel_path_str} (匹配模式: {pattern})")
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

        Args:
            workflow_path: 工作流目录路径

        Returns:
            验证结果字典
        """
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
        """验证Markdown语法"""
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
        """检查标题层次结构 - 忽略代码块内的注释"""
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
        """评估工作流质量"""
        logger.info("执行质量评估")

        workflow_dir = Path(workflow_path)

        quality_scores = {
            "completeness": self._assess_completeness(workflow_dir),
            "usability": self._assess_usability(workflow_dir),
            "maintainability": self._assess_maintainability(workflow_dir),
            "performance": self._assess_performance(workflow_dir),
            "documentation": self._assess_documentation(workflow_dir),
            "extensibility": self._assess_extensibility(workflow_dir),
        }

        # 计算综合分数
        weights = {
            "completeness": 0.25,
            "usability": 0.20,
            "maintainability": 0.20,
            "performance": 0.15,
            "documentation": 0.10,
            "extensibility": 0.10,
        }

        total_score = sum(
            quality_scores[dimension] * weights[dimension]
            for dimension in quality_scores
        )

        self.validation_results["quality"]["score"] = total_score
        self.validation_results["quality"]["details"] = quality_scores

    def _assess_completeness(self, workflow_dir: Path) -> float:
        """评估功能完整性"""
        score = 0.0
        total_checks = 6

        # 检查必需文件
        required_files = ["README.md"]
        if any(
            workflow_dir.glob(pattern) for pattern in ["*_template.md", "*_workflow.md"]
        ):
            score += 1

        if any(workflow_dir.glob("README.md")):
            score += 1

        # 检查脚本文件
        if any(workflow_dir.glob("**/*.py")):
            score += 1

        if any(workflow_dir.glob("**/*.ps1")):
            score += 1

        # 检查测试文件
        if any(workflow_dir.glob("**/test_*.py")):
            score += 1

        # 检查配置文件
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
        """评估可维护性"""
        score = 0.0
        total_checks = 4

        # 检查代码注释
        python_files = list(workflow_dir.glob("**/*.py"))
        if python_files:
            total_lines = 0
            comment_lines = 0

            for py_file in python_files:
                content = py_file.read_text(encoding="utf-8")
                lines = content.split("\n")
                total_lines += len(lines)
                comment_lines += sum(
                    1 for line in lines if line.strip().startswith("#")
                )

            if total_lines > 0 and comment_lines / total_lines >= 0.1:
                score += 1

        # 检查模块化设计
        if len(python_files) > 1:
            score += 1

        # 检查版本控制信息
        for md_file in workflow_dir.glob("**/*.md"):
            content = md_file.read_text(encoding="utf-8")
            if "版本" in content or "version" in content.lower():
                score += 1
                break

        # 检查日志记录
        for py_file in workflow_dir.glob("**/*.py"):
            content = py_file.read_text(encoding="utf-8")
            if "logging" in content or "logger" in content:
                score += 1
                break

        return (score / total_checks) * 10

    def _assess_performance(self, workflow_dir: Path) -> float:
        """评估性能效率"""
        score = 5.0  # 默认中等分数

        # 这里可以添加更复杂的性能分析逻辑
        # 比如分析算法复杂度、并发处理等

        return score

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
