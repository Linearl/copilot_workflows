# 版本对比分析汇总 [旧版本] → [新版本]

```yaml
summary_version: v2
range: [旧版本]->[新版本]
created: [日期]
analyst: GitHub Copilot
status: DRAFT # DRAFT/IN_REVIEW/FINAL
confidence: [0.0-1.0]
metrics_snapshot: summary_metrics.json # 来自 generate-summary-metrics.ps1
breaking_api_source: breaking_api_candidates.json # 来自 extract-breaking-api.ps1
risk_status_source: risk_status.json # 来自 risk-status-report.ps1
id_validation_source: id_validation.json # 来自 validate-ids.ps1
```

**分析日期**: [日期]  
**分析员**: GitHub Copilot  
**分析状态**: [进行中/已完成]  

---

## 🔔 执行摘要

| 指标 | 数值 | 说明 |
|------|------|------|
| 提交总数 | [数量] | git log range / summary_metrics.json |
| 变更文件数 | [数量] | unique changed files / summary_metrics.json |
| 新增代码行 | [数量] | add lines |
| 删除代码行 | [数量] | del lines |
| 净增长 | [数量] | add - del |
| 模块数 | [数量] | 受影响模块 |
| 破坏性 API 数 | [数量] | breaking_api_candidates.json |
| 风险数 | [数量] | risk_status.json (OPEN) |

### 统计 JSON（机器可读）

> 若已生成 `summary_metrics.json` 可直接粘贴其内容；否则使用占位并在最终版替换。

```json
{
  "range": "[旧版本]->[新版本]",
  "commits_total": 0,
  "files_changed": 0,
  "lines_added": 0,
  "lines_deleted": 0,
  "modules_impacted": 0,
  "apis_breaking": 0,
  "risks_open": 0,
  "generated_at": "[ISO8601]"
}
```

---

## 🎯 重大变更（引用 ID）

| 类型 | 引用ID | 标签 | 简述 | 影响等级 |
|------|--------|------|------|----------|
| 模块变更 | MOD- | label | 描述 | 高/中/低 |
| 重要发现 | DISC- | label | 描述 | 高/中/低 |
| 兼容性提示 | CMP- | label | 描述 | 中 |

> 详细内容见对应模块分析或阶段记录文件。

---

## 🧩 模块影响概览

| 模块 | 变更文件数 | 新增 | 删除 | 净变化 | 影响等级 | 主要变更ID |
|------|------------|------|------|--------|----------|------------|
| algorithm |  |  |  |  | 高 | MOD- |
| logic |  |  |  |  | 高 | MOD- |
| tools |  |  |  |  | 中 | MOD- |
| config |  |  |  |  | 中 | MOD- |

---

## 🛠️ 破坏性 API 列表

> 可由 `extract-breaking-api.ps1` 输出的 breaking_api_candidates.txt / .json 填充。人工复核后再确定 API_ID 与迁移建议。

| API_ID | 旧签名 | 新签名 | 变更类型 | 迁移建议 | 模块 | 影响等级 |
|--------|--------|--------|----------|----------|------|----------|
| API- |  |  | breaking/behavior | [迁移说明] | algorithm | 高 |

---

## ⚠️ 风险与兼容性

### 风险表

> 可使用 `risk-status-report.ps1` 结果 (risk_status.md) 复制核心行（按 ID 过滤相关版本）。

| RSK_ID | 等级 | 描述 | 影响 | 缓解措施 | 状态 |
|--------|------|------|------|----------|------|
| RSK- | 高 |  | 影响 | 处理方案 | OPEN |

### 兼容性摘要

- 向前兼容性: [良好/部分/差]
- 向后兼容性: [良好/部分/差]
- 升级难度: [低/中/高]

---

## 📦 依赖 / 配置变更

| 类型 | 名称 | 旧版本/值 | 新版本/值 | 影响描述 |
|------|------|-----------|-----------|----------|
| 依赖升级 | pkgA | 1.2.0 | 1.3.0 | 修复安全问题 |
| 配置新增 | settingX | 不存在 | true | 启用新功能 |

---

## 💡 升级与行动建议

| 建议类型 | 描述 | 优先级 | 相关ID |
|----------|------|--------|--------|
| 测试 | 回归 algorithm 临界路径 | 高 | MOD-/RSK- |
| 迁移 | 更新已废弃API调用 | 高 | API- |
| 文档 | 补充配置 settingX 说明 | 中 | DISC- |

---

## 📝 后续关注点

1. [关注点] - 说明（关联 ID: RSK-/DISC-）
2. [关注点] - 说明（关联 ID: RSK-/DISC-）
3. [关注点] - 说明（关联 ID: RSK-/DISC-）

---

## 🔍 可信度说明

> 可结合 `id_validation.json` (覆盖率、重复/孤立 ID)、`risk_status.json` (风险覆盖)、`breaking_api_candidates.json` (候选 vs 确认) 量化。

| 方面 | 完整度 | 说明 |
|------|--------|------|
| 提交覆盖 | [0-100%] | 采样/全量解析策略 |
| 模块扫描 | [0-100%] | 基于 module_impact.md / module_impact.json |
| API 变更检测 | [0-100%] | 候选 N / 确认 M |
| 风险评估 | [0-100%] | OPEN vs 总风险项 |

---

## ⏱️ 执行元数据

| 项 | 值 |
|----|----|
| 分析开始 | [开始时间] |
| 分析结束 | [结束时间] |
| 耗时 | [时长] |
| 脚本版本 | setup_worktree.ps1@[hash] |

---

**报告生成时间**: [生成时间]  
**报告版本**: v2.0  
**报告状态**: [草稿/最终版]
