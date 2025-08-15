# 📊 分析索引

```yaml
index_version: v1
range: [旧版本]->[新版本]
created: [YYYY-MM-DD]
status: PLANNED # PLANNED/ACTIVE/DONE/PAUSED/CANCELLED
owner: GitHub Copilot
```

## 任务基本信息

- **任务名称**: [版本对比任务名称]
- **版本范围**: [旧版本] → [新版本]
- **分析目标**: [更新日志补充/变更分析/升级指导]
- **任务状态**: 🔄 进行中 / ✅ 已完成 / ⚠️ 暂停 / ❌ 已取消

## 阶段进度表

| 阶段ID | 名称 | 迭代号 | 状态 | 计划完成 | 实际完成 | 备注 |
|--------|------|--------|------|----------|----------|------|
| PH1 | 总体变更分析 | 1 | ACTIVE | 2025-08-15 |  |  |
| PH2 | 模块深度对比 | 1 | PLANNED | 2025-08-16 |  |  |
| PH3 | 文档变更分析 | 1 | PLANNED | 2025-08-17 |  |  |
| SUM | 汇总与报告 | 1 | PLANNED | 2025-08-18 |  |  |

## 关键发现指针（只列 ID + 标签）

| DISC_ID | 标签 | 简述 | 所属阶段 |
|---------|------|------|----------|
| DISC-001 | config-change | 配置结构新增字段 | PH1 |
| DISC-002 | perf-risk | 算法路径耗时上升 | PH2 |

> 详细内容见各阶段 README 与模块分析文档。

## 风险列表

| RSK_ID | 等级 | 描述 | 影响 | 缓解 | 状态 |
|--------|------|------|------|------|------|
| RSK- |  |  |  |  | OPEN |

## 模块分析计划

| 模块 | 预估影响等级 | 计划顺序 | 分析文件 |
|------|--------------|----------|----------|
| algorithm | 高 | 1 | stage_2_modules/algorithm_analysis.md |
| logic | 高 | 2 | stage_2_modules/logic_analysis.md |
| tools | 中 | 3 | stage_2_modules/tools_analysis.md |
| config | 中 | 4 | stage_2_modules/config_analysis.md |

## 指标快照

```json
{
  "range": "[旧版本]->[新版本]",
  "commits_total": 0,
  "files_changed": 0,
  "lines_added": 0,
  "lines_deleted": 0,
  "modules": {}
}
```

## 文件导航

- stage_1_overview/README.md
- stage_2_modules/README.md
- stage_3_documentation/README.md
- summary/version_comparison_report.md
- summary/update_log_draft.md

## 完成标准检查

| 项 | 状态(✓/✗) | 备注 |
|----|-----------|------|
| 分析阶段全部完成 |  |  |
| 关键发现全部记录 |  |  |
| 破坏性 API 已列出 |  |  |
| 更新日志草稿生成 |  |  |
| 升级提示块完善 |  |  |

## 归档检查

| 项 | 状态(✓/✗) | 备注 |
|----|-----------|------|
| 工作流文档归档 |  |  |
| 指标快照保存 |  |  |
| 风险表冻结 |  |  |
| 相关脚本版本记录 |  |  |
