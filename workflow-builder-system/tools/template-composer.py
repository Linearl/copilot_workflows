#!/usr/bin/env python3
"""
模板组装器 - 负责将模板组件组装成完整的工作流文档
支持参数化模板、条件渲染和动态内容生成
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TemplateComposer:
    """模板组装器主类"""

    def __init__(self):
        self.template_cache = {}
        self.component_registry = {}

    def load_component(self, component_path: str) -> str:
        """
        加载模板组件

        Args:
            component_path: 组件文件路径

        Returns:
            组件内容
        """
        path = Path(component_path)
        if not path.exists():
            raise FileNotFoundError(f"模板组件不存在: {component_path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        self.template_cache[component_path] = content
        return content

    def register_component(self, name: str, content: str):
        """
        注册模板组件

        Args:
            name: 组件名称
            content: 组件内容
        """
        self.component_registry[name] = content

    def render_template(self, template: str, parameters: Dict[str, Any]) -> str:
        """
        渲染模板

        Args:
            template: 模板内容
            parameters: 渲染参数

        Returns:
            渲染后的内容
        """
        # 处理条件渲染
        template = self._process_conditionals(template, parameters)

        # 处理循环渲染
        template = self._process_loops(template, parameters)

        # 处理变量替换
        template = self._substitute_variables(template, parameters)

        # 处理函数调用
        template = self._process_functions(template, parameters)

        return template

    def _process_conditionals(self, template: str, parameters: Dict[str, Any]) -> str:
        """处理条件渲染 {%if condition%}...{%endif%}"""
        pattern = r"\{\%if\s+(.+?)\%\}(.*?)\{\%endif\%\}"

        def replace_conditional(match):
            condition = match.group(1).strip()
            content = match.group(2)

            # 简单的条件评估
            if self._evaluate_condition(condition, parameters):
                return content
            else:
                return ""

        return re.sub(pattern, replace_conditional, template, flags=re.DOTALL)

    def _process_loops(self, template: str, parameters: Dict[str, Any]) -> str:
        """处理循环渲染 {%for item in list%}...{%endfor%}"""
        pattern = r"\{\%for\s+(\w+)\s+in\s+(\w+)\%\}(.*?)\{\%endfor\%\}"

        def replace_loop(match):
            item_name = match.group(1)
            list_name = match.group(2)
            content = match.group(3)

            if list_name not in parameters:
                return ""

            result = []
            for item in parameters[list_name]:
                # 创建新的参数上下文
                loop_params = parameters.copy()
                loop_params[item_name] = item

                # 递归处理循环内容
                rendered_content = self._substitute_variables(content, loop_params)
                result.append(rendered_content)

            return "\n".join(result)

        return re.sub(pattern, replace_loop, template, flags=re.DOTALL)

    def _substitute_variables(self, template: str, parameters: Dict[str, Any]) -> str:
        """替换变量 {variable_name}"""

        def replace_var(match):
            var_name = match.group(1)
            return str(parameters.get(var_name, f"{{{var_name}}}"))

        return re.sub(r"\{([^%\s][^}]*)\}", replace_var, template)

    def _process_functions(self, template: str, parameters: Dict[str, Any]) -> str:
        """处理函数调用 {{function_name(args)}}"""
        pattern = r"\{\{(\w+)\((.*?)\)\}\}"

        def replace_function(match):
            func_name = match.group(1)
            args_str = match.group(2)

            # 解析参数
            args = []
            if args_str.strip():
                args = [arg.strip().strip("\"'") for arg in args_str.split(",")]

            # 调用内置函数
            if hasattr(self, f"_func_{func_name}"):
                func = getattr(self, f"_func_{func_name}")
                return str(func(*args, parameters=parameters))
            else:
                return f"{{{{{func_name}({args_str})}}}}"

        return re.sub(pattern, replace_function, template)

    def _evaluate_condition(self, condition: str, parameters: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        # 简单的条件评估，支持基本比较
        if "==" in condition:
            left, right = condition.split("==", 1)
            left_val = parameters.get(left.strip(), left.strip())
            right_val = right.strip().strip("\"'")
            return str(left_val) == str(right_val)
        elif "!=" in condition:
            left, right = condition.split("!=", 1)
            left_val = parameters.get(left.strip(), left.strip())
            right_val = right.strip().strip("\"'")
            return str(left_val) != str(right_val)
        elif "in" in condition:
            left, right = condition.split(" in ", 1)
            left_val = parameters.get(left.strip(), left.strip())
            right_val = parameters.get(right.strip(), [])
            return left_val in right_val
        else:
            # 直接检查变量是否存在且为真
            return bool(parameters.get(condition.strip(), False))

    # 内置函数
    def _func_upper(self, text: str, **kwargs) -> str:
        """转大写"""
        return text.upper()

    def _func_lower(self, text: str, **kwargs) -> str:
        """转小写"""
        return text.lower()

    def _func_title(self, text: str, **kwargs) -> str:
        """标题格式"""
        return text.title()

    def _func_date(self, format: str = "%Y-%m-%d", **kwargs) -> str:
        """当前日期"""
        from datetime import datetime

        return datetime.now().strftime(format)

    def _func_repeat(self, text: str, count: str, **kwargs) -> str:
        """重复文本"""
        return text * int(count)

    def _func_join(self, separator: str, list_name: str, **kwargs) -> str:
        """连接列表"""
        parameters = kwargs.get("parameters", {})
        items = parameters.get(list_name, [])
        return separator.join(str(item) for item in items)

    def _func_len(self, list_name: str, **kwargs) -> str:
        """获取列表长度"""
        parameters = kwargs.get("parameters", {})
        items = parameters.get(list_name, [])
        return str(len(items))

    def compose_workflow(
        self, base_template: str, components: List[str], parameters: Dict[str, Any]
    ) -> str:
        """
        组装完整的工作流

        Args:
            base_template: 基础模板路径或内容
            components: 要包含的组件列表
            parameters: 渲染参数

        Returns:
            组装后的工作流内容
        """
        logger.info("开始组装工作流")

        # 加载基础模板
        if Path(base_template).exists():
            template = self.load_component(base_template)
        else:
            template = base_template

        # 添加组件内容到参数中
        for component in components:
            if component in self.component_registry:
                component_content = self.component_registry[component]
            elif Path(component).exists():
                component_content = self.load_component(component)
            else:
                logger.warning(f"组件不存在: {component}")
                continue

            # 使用组件名作为参数名
            component_name = (
                Path(component).stem
                if "/" in component or "\\" in component
                else component
            )
            parameters[f"component_{component_name}"] = component_content

        # 渲染模板
        result = self.render_template(template, parameters)

        # 后处理
        result = self._post_process(result)

        logger.info("工作流组装完成")
        return result

    def _post_process(self, content: str) -> str:
        """后处理，清理和格式化"""
        # 移除多余的空行
        content = re.sub(r"\n{3,}", "\n\n", content)

        # 修复markdown格式
        content = self._fix_markdown_formatting(content)

        return content.strip()

    def _fix_markdown_formatting(self, content: str) -> str:
        """修复markdown格式问题"""
        # 确保代码块前后有空行
        content = re.sub(r"([^\n])\n```", r"\1\n\n```", content)
        content = re.sub(r"```\n([^\n])", r"```\n\n\1", content)

        # 确保标题前后有空行
        content = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", content)
        content = re.sub(r"(#{1,6}\s[^\n]+)\n([^\n#])", r"\1\n\n\2", content)

        return content

    def generate_toc(self, content: str) -> str:
        """生成目录"""
        lines = content.split("\n")
        toc_items = []

        for line in lines:
            if line.startswith("#"):
                # 提取标题级别和内容
                level = len(line) - len(line.lstrip("#"))
                title = line.lstrip("# ").strip()

                # 生成锚点
                anchor = title.lower()
                anchor = re.sub(r"[^\w\s-]", "", anchor)
                anchor = re.sub(r"[-\s]+", "-", anchor)

                # 生成TOC项
                indent = "  " * (level - 1)
                toc_item = f"{indent}- [{title}](#{anchor})"
                toc_items.append(toc_item)

        return "\n".join(toc_items)

    def extract_sections(self, content: str) -> Dict[str, str]:
        """提取文档中的各个章节"""
        sections = {}
        lines = content.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith("#"):
                # 保存前一个章节
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content)

                # 开始新章节
                current_section = line.lstrip("# ").strip()
                current_content = [line]
            else:
                if current_section:
                    current_content.append(line)

        # 保存最后一个章节
        if current_section and current_content:
            sections[current_section] = "\n".join(current_content)

        return sections


def main():
    """CLI入口函数"""
    import argparse

    parser = argparse.ArgumentParser(description="模板组装器")
    parser.add_argument("--template", required=True, help="基础模板文件")
    parser.add_argument("--parameters", help="参数文件(JSON/YAML)")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--components", nargs="*", help="组件文件列表")

    args = parser.parse_args()

    # 创建组装器
    composer = TemplateComposer()

    # 加载参数
    parameters = {}
    if args.parameters:
        with open(args.parameters, "r", encoding="utf-8") as f:
            if args.parameters.endswith(".json"):
                parameters = json.load(f)
            else:
                parameters = yaml.safe_load(f)

    # 组装工作流
    result = composer.compose_workflow(args.template, args.components or [], parameters)

    # 输出结果
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✅ 工作流已生成: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
