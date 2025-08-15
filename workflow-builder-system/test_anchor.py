#!/usr/bin/env python3
from tools.validator import WorkflowValidator
from pathlib import Path

v = WorkflowValidator()

# 测试标题锚点生成
title = "## 📖 工作流简介"
anchors = v._generate_possible_anchors(title)
print(f"标题: {title}")
print(f"所有生成的锚点: {anchors}")
print(f"是否匹配 '📖-工作流简介': {v._is_anchor_valid('📖-工作流简介', set(anchors))}")

# 测试文件中的实际内容
content = Path("templates/workflow-base-template.md").read_text(encoding="utf-8")
print("\n=== 提取所有标题 ===")
for line in content.split("\n"):
    if line.startswith("#"):
        if (
            "工作流简介" in line
            or "任务信息" in line
            or "标准流程" in line
            or "循环控制" in line
            or "使用指导" in line
        ):
            anchors = v._generate_possible_anchors(line)
            print(f"{line} -> {anchors}")
