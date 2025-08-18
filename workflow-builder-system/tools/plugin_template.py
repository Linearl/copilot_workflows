#!/usr/bin/env python3
"""
插件模板 - 质量评估插件标准模板
用于创建新的质量评估插件

Author: Workflow Builder System
Version: 1.0.0
Last Updated: 2025-08-18

使用说明:
========

这个模板提供了创建新质量评估插件的标准结构和接口。
按照此模板创建的插件可以无缝集成到质量评估系统中。

创建步骤:
--------
1. 复制此模板文件并重命名为 your_plugin_name.py
2. 修改类名为 YourPluginNamePlugin
3. 实现 assess() 方法的具体逻辑
4. 更新插件信息（名称、描述、版本等）
5. 在 QualityAssessmentManager 中注册新插件

示例用法:
--------
```python
from plugin_template import TemplatePlugin

# 创建插件实例
plugin = TemplatePlugin()

# 评估工作流
score, details = plugin.assess(workflow_dir)
print(f"得分: {score:.1f}/10.0")
print(f"详细信息: {details}")
```

注意事项:
--------
1. 插件必须继承自 QualityAssessmentPlugin 基类
2. assess() 方法必须返回 (float, dict) 元组
3. 得分范围必须在 0.0 到 10.0 之间
4. 详细信息字典应包含 passed_checks、failed_checks、recommendations 等标准字段
5. 所有异常都应该被妥善处理，避免影响整体评估流程

插件开发指南:
------------
- 评估逻辑应该具体、可测量
- 检查项应该有明确的标准
- 建议应该具体、可操作
- 考虑不同类型的工作流场景
- 保持与其他插件的一致性
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any

# 导入基类
try:
    from .quality_assessment_plugin import QualityAssessmentPlugin
except ImportError:
    try:
        from quality_assessment_plugin import QualityAssessmentPlugin
    except ImportError:
        # 如果无法导入基类，定义一个简单的基类
        class QualityAssessmentPlugin:
            def __init__(self):
                pass

            def assess(self, workflow_dir: Path) -> Tuple[float, Dict[str, Any]]:
                raise NotImplementedError("子类必须实现 assess 方法")


class TemplatePlugin(QualityAssessmentPlugin):
    """
    插件模板类 - 演示如何创建质量评估插件

    这个模板展示了创建新插件所需的所有必要组件：
    - 插件元信息定义
    - 标准的评估接口实现
    - 检查项列表和评估逻辑
    - 详细信息收集和建议生成

    Attributes:
        name (str): 插件名称
        description (str): 插件描述
        version (str): 插件版本
        category (str): 插件类别
        weight (float): 默认权重

    Example:
        >>> plugin = TemplatePlugin()
        >>> score, details = plugin.assess(Path("/path/to/workflow"))
        >>> print(f"模板评估得分: {score:.1f}/10.0")
    """

    def __init__(self):
        """初始化模板插件"""
        super().__init__()

        # 插件元信息 - 请根据实际插件修改这些信息
        self.name = "template"
        self.description = "模板插件 - 演示插件开发标准"
        self.version = "1.0.0"
        self.category = "quality_assessment"
        self.weight = 1.0  # 默认权重，可在配置中覆盖

        # 初始化日志记录器
        self.logger = logging.getLogger(f"workflow_validator.plugins.{self.name}")

        # 定义检查项列表 - 请根据实际需求修改
        self.check_items = [
            {
                "name": "basic_structure",
                "description": "检查基本结构",
                "weight": 0.3,
                "critical": True,
            },
            {
                "name": "content_quality",
                "description": "检查内容质量",
                "weight": 0.3,
                "critical": False,
            },
            {
                "name": "standards_compliance",
                "description": "检查标准合规性",
                "weight": 0.2,
                "critical": False,
            },
            {
                "name": "best_practices",
                "description": "检查最佳实践",
                "weight": 0.2,
                "critical": False,
            },
        ]

        self.logger.debug(f"初始化 {self.name} 插件完成")

    def assess(self, workflow_dir: Path) -> Tuple[float, Dict[str, Any]]:
        """
        执行模板评估

        这是插件的核心方法，实现具体的评估逻辑。
        请根据您的评估需求修改此方法的实现。

        Args:
            workflow_dir (Path): 工作流目录路径

        Returns:
            Tuple[float, Dict[str, Any]]: (得分, 详细信息字典)

        评估标准:
        --------
        此模板使用以下评估标准（请根据实际需求修改）：
        1. 基本结构 (30%) - 检查必要文件和目录结构
        2. 内容质量 (30%) - 检查内容的完整性和准确性
        3. 标准合规 (20%) - 检查是否符合相关标准
        4. 最佳实践 (20%) - 检查是否遵循最佳实践
        """
        try:
            self.logger.debug(f"开始执行 {self.name} 插件评估")

            # 初始化评估结果
            total_score = 0.0
            passed_checks = []
            failed_checks = []
            recommendations = []
            check_details = {}

            # 执行各项检查
            for check_item in self.check_items:
                check_name = check_item["name"]
                check_weight = check_item["weight"]

                # 调用具体的检查方法
                check_passed, check_score, check_detail = self._execute_check(
                    workflow_dir, check_item
                )

                # 累计得分
                total_score += check_score * check_weight

                # 记录检查结果
                if check_passed:
                    passed_checks.append(check_item["description"])
                else:
                    failed_checks.append(check_item["description"])

                    # 为失败的检查项生成建议
                    recommendation = self._generate_recommendation(check_item)
                    if recommendation:
                        recommendations.append(recommendation)

                # 保存详细信息
                check_details[check_name] = {
                    "passed": check_passed,
                    "score": check_score,
                    "detail": check_detail,
                    "weight": check_weight,
                }

            # 确保得分在有效范围内
            final_score = max(0.0, min(10.0, total_score * 10.0))

            # 构建详细信息字典
            details = {
                "score": final_score,
                "passed_checks": passed_checks,
                "failed_checks": failed_checks,
                "recommendations": recommendations,
                "check_details": check_details,
                "summary": {
                    "total_checks": len(self.check_items),
                    "passed_count": len(passed_checks),
                    "failed_count": len(failed_checks),
                    "critical_failed": len(
                        [
                            item
                            for item in self.check_items
                            if item["critical"] and item["description"] in failed_checks
                        ]
                    ),
                },
            }

            self.logger.debug(f"{self.name} 插件评估完成，得分: {final_score:.1f}/10.0")
            return final_score, details

        except Exception as e:
            self.logger.error(f"{self.name} 插件评估失败: {e}")
            # 返回默认的失败结果
            return 0.0, {
                "score": 0.0,
                "passed_checks": [],
                "failed_checks": ["插件执行失败"],
                "recommendations": ["请检查插件配置和工作流目录"],
                "error": str(e),
            }

    def _execute_check(
        self, workflow_dir: Path, check_item: Dict[str, Any]
    ) -> Tuple[bool, float, str]:
        """
        执行单个检查项

        Args:
            workflow_dir (Path): 工作流目录
            check_item (Dict): 检查项配置

        Returns:
            Tuple[bool, float, str]: (是否通过, 得分, 详细说明)
        """
        check_name = check_item["name"]

        try:
            # 根据检查项名称执行相应的检查逻辑
            if check_name == "basic_structure":
                return self._check_basic_structure(workflow_dir)
            elif check_name == "content_quality":
                return self._check_content_quality(workflow_dir)
            elif check_name == "standards_compliance":
                return self._check_standards_compliance(workflow_dir)
            elif check_name == "best_practices":
                return self._check_best_practices(workflow_dir)
            else:
                self.logger.warning(f"未知的检查项: {check_name}")
                return False, 0.0, f"未实现的检查项: {check_name}"

        except Exception as e:
            self.logger.error(f"检查项 {check_name} 执行失败: {e}")
            return False, 0.0, f"检查执行失败: {str(e)}"

    def _check_basic_structure(self, workflow_dir: Path) -> Tuple[bool, float, str]:
        """
        检查基本结构

        示例检查：验证是否存在必要的文件和目录
        请根据实际需求修改此方法
        """
        required_files = ["README.md"]  # 根据需求修改必要文件列表
        required_dirs = []  # 根据需求修改必要目录列表

        missing_files = []
        missing_dirs = []

        # 检查必要文件
        for file_name in required_files:
            file_path = workflow_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)

        # 检查必要目录
        for dir_name in required_dirs:
            dir_path = workflow_dir / dir_name
            if not dir_path.exists() or not dir_path.is_dir():
                missing_dirs.append(dir_name)

        # 计算得分
        total_required = len(required_files) + len(required_dirs)
        if total_required == 0:
            score = 1.0
            passed = True
            detail = "无必要文件或目录要求"
        else:
            missing_count = len(missing_files) + len(missing_dirs)
            score = max(0.0, (total_required - missing_count) / total_required)
            passed = missing_count == 0

            if missing_files or missing_dirs:
                detail = f"缺少文件: {missing_files}, 缺少目录: {missing_dirs}"
            else:
                detail = "所有必要文件和目录都存在"

        return passed, score, detail

    def _check_content_quality(self, workflow_dir: Path) -> Tuple[bool, float, str]:
        """
        检查内容质量

        示例检查：验证Markdown文件的内容质量
        请根据实际需求修改此方法
        """
        md_files = list(workflow_dir.glob("**/*.md"))

        if not md_files:
            return False, 0.0, "未找到Markdown文件"

        quality_issues = []
        total_checks = 0
        passed_checks = 0

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8")
                total_checks += 3  # 假设每个文件检查3项

                # 检查1: 文件不能为空
                if content.strip():
                    passed_checks += 1
                else:
                    quality_issues.append(f"{md_file.name} 内容为空")

                # 检查2: 应该有标题
                if content.strip().startswith("#"):
                    passed_checks += 1
                else:
                    quality_issues.append(f"{md_file.name} 缺少标题")

                # 检查3: 内容长度合理（示例：至少50字符）
                if len(content.strip()) >= 50:
                    passed_checks += 1
                else:
                    quality_issues.append(f"{md_file.name} 内容过短")

            except Exception as e:
                quality_issues.append(f"{md_file.name} 读取失败: {e}")

        if total_checks == 0:
            return False, 0.0, "无可检查的内容"

        score = passed_checks / total_checks
        passed = len(quality_issues) == 0
        detail = (
            "内容质量良好" if passed else f"发现问题: {'; '.join(quality_issues[:3])}"
        )

        return passed, score, detail

    def _check_standards_compliance(
        self, workflow_dir: Path
    ) -> Tuple[bool, float, str]:
        """
        检查标准合规性

        示例检查：验证是否符合特定的标准或约定
        请根据实际需求修改此方法
        """
        # 示例：检查文件命名规范
        issues = []
        total_files = 0
        compliant_files = 0

        for file_path in workflow_dir.rglob("*"):
            if file_path.is_file():
                total_files += 1
                file_name = file_path.name

                # 示例规则：文件名应使用小写字母、数字、下划线和连字符
                if re.match(r"^[a-z0-9_\-\.]+$", file_name):
                    compliant_files += 1
                else:
                    issues.append(f"文件名不符合规范: {file_name}")

        if total_files == 0:
            return True, 1.0, "无文件需要检查"

        score = compliant_files / total_files
        passed = len(issues) == 0
        detail = "文件命名规范" if passed else f"发现问题: {'; '.join(issues[:3])}"

        return passed, score, detail

    def _check_best_practices(self, workflow_dir: Path) -> Tuple[bool, float, str]:
        """
        检查最佳实践

        示例检查：验证是否遵循最佳实践
        请根据实际需求修改此方法
        """
        best_practice_score = 0.0
        checks_performed = 0
        issues = []

        # 检查1: 是否有LICENSE文件
        license_file = workflow_dir / "LICENSE"
        checks_performed += 1
        if license_file.exists():
            best_practice_score += 1.0
        else:
            issues.append("建议添加LICENSE文件")

        # 检查2: 是否有版本信息
        version_indicators = ["version", "VERSION", "version.md", "CHANGELOG.md"]
        checks_performed += 1
        has_version = any(
            (workflow_dir / indicator).exists() for indicator in version_indicators
        )
        if has_version:
            best_practice_score += 1.0
        else:
            issues.append("建议添加版本信息文件")

        # 检查3: 是否有示例或文档
        doc_patterns = ["example*", "demo*", "docs/*", "*.md"]
        checks_performed += 1
        has_docs = False
        for pattern in doc_patterns:
            if list(workflow_dir.glob(pattern)):
                has_docs = True
                break

        if has_docs:
            best_practice_score += 1.0
        else:
            issues.append("建议添加示例或详细文档")

        if checks_performed == 0:
            return True, 1.0, "无最佳实践检查项"

        score = best_practice_score / checks_performed
        passed = len(issues) == 0
        detail = "遵循最佳实践" if passed else f"改进建议: {'; '.join(issues)}"

        return passed, score, detail

    def _generate_recommendation(self, check_item: Dict[str, Any]) -> str:
        """
        为失败的检查项生成改进建议

        Args:
            check_item: 失败的检查项配置

        Returns:
            str: 改进建议
        """
        check_name = check_item["name"]

        # 根据检查项生成具体建议
        recommendations = {
            "basic_structure": "请确保工作流包含所有必要的文件和目录结构",
            "content_quality": "请改进文档内容的完整性和准确性，确保每个文件都有适当的内容",
            "standards_compliance": "请检查文件命名和结构是否符合相关标准和约定",
            "best_practices": "请考虑添加LICENSE文件、版本信息和详细文档以提高项目质量",
        }

        return recommendations.get(check_name, f"请改进 {check_item['description']}")

    def get_info(self) -> Dict[str, Any]:
        """
        获取插件信息

        Returns:
            Dict[str, Any]: 插件元信息
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "weight": self.weight,
            "check_items": [
                {
                    "name": item["name"],
                    "description": item["description"],
                    "weight": item["weight"],
                    "critical": item["critical"],
                }
                for item in self.check_items
            ],
        }


# 导入必要的模块
import re

# 如果作为独立脚本运行，提供测试功能
if __name__ == "__main__":
    import sys
    from pathlib import Path

    def test_plugin():
        """测试插件功能"""
        print("=" * 50)
        print("插件模板测试")
        print("=" * 50)

        # 创建插件实例
        plugin = TemplatePlugin()

        # 显示插件信息
        info = plugin.get_info()
        print(f"插件名称: {info['name']}")
        print(f"插件描述: {info['description']}")
        print(f"插件版本: {info['version']}")
        print(f"检查项数量: {len(info['check_items'])}")
        print()

        # 测试评估功能
        if len(sys.argv) > 1:
            test_path = Path(sys.argv[1])
            if test_path.exists():
                print(f"测试路径: {test_path}")
                score, details = plugin.assess(test_path)
                print(f"评估得分: {score:.1f}/10.0")
                print(f"通过检查: {len(details['passed_checks'])}")
                print(f"失败检查: {len(details['failed_checks'])}")
                if details["recommendations"]:
                    print("改进建议:")
                    for rec in details["recommendations"]:
                        print(f"  • {rec}")
            else:
                print(f"错误: 路径不存在 - {test_path}")
        else:
            print("用法: python plugin_template.py <测试路径>")
            print("示例: python plugin_template.py /path/to/workflow")

    test_plugin()
