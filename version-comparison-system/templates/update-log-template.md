# ANC Host 更新日志 [旧版本] → [新版本]

```yaml
update_log_version: v2
range: [旧版本]->[新版本]
period: [开始日期]-[结束日期]
status: DRAFT # DRAFT/REVIEW/FINAL
release_date: [发布日期]
upgrade_difficulty: [低/中/高]
commits_summary_file: commits_summary.txt # generate-commits-summary.ps1
metrics_snapshot: summary_metrics.json # generate-summary-metrics.ps1
breaking_api_source: breaking_api_candidates.json # extract-breaking-api.ps1
risk_status_source: risk_status.json # risk-status-report.ps1
```

**最后更新**: [生成时间]  
**版本状态**: ✅ 已完成 / 🚧 进行中 / 📨 草稿  

---

## 1. 新增 (Features)

| 功能ID | 描述 | 模块 | 影响等级 | 相关DISC/MOD |
|--------|------|------|----------|--------------|
| FEAT- |  |  | 高/中/低 | DISC-/MOD- |

## 2. 修复 (Fixes)

| 修复ID | 描述 | 模块 | 问题来源 | 相关DISC/RSK |
|--------|------|------|----------|--------------|
| FIX- |  |  | 用户反馈/内部发现 | DISC-/RSK- |

## 3. 优化 (Improvements / Refactor / Performance)

| 项ID | 描述 | 类型 | 模块 | 相关ID |
|------|------|------|------|--------|
| IMP- |  | 重构/性能/代码质量 |  | MOD-/DISC- |

## 4. 兼容性提示 (Compatibility Notes)

| CMP_ID | 类型(API/配置/数据) | 描述 | 升级建议 | 影响等级 |
|--------|--------------------|------|----------|----------|
| CMP- | API |  | 迁移步骤 | 中 |

### 破坏性 API

> 若已运行 `extract-breaking-api.ps1`，可基于 breaking_api_candidates.txt 过滤并人工确认后填入；保留必要迁移说明。

| API_ID | 旧签名 | 新签名 | 变更类型 | 迁移建议 |
|--------|--------|--------|----------|----------|
| API- |  |  | breaking |  |

## 5. 特别注意 (Important Notes)

| 项 | 描述 | 优先级 | 相关ID |
|----|------|--------|--------|
| NOTE- |  | 高/中/低 | RSK-/DISC-/MOD- |

---

## 6. 版本总结 (Summary & Insights)

### 🎯 目标达成情况

- **核心功能**: ✅ [完成度]% 完成
- **性能优化**: ✅ [完成度]% 完成  
- **代码质量**: ✅ [完成度]% 完成
- **安全/合规**: [状态] [完成度]% 完成
- **其他目标**: [目标标签] [完成度]% 完成

### 📈 技术成果

| 维度 | 指标 | 说明 |
|------|------|------|
| 代码变更 | [统计数据] | 行/文件/提交汇总 |
| 性能提升 | [具体数据] | 例如: 吞吐 +15% / 延迟 -8% |
| 架构改进 | [主要改进] | 重构/抽象/解耦 |
| 质量提升 | [质量指标] | 覆盖率/复杂度/缺陷率 |

### 💡 开发洞察

#### 成功经验

[主要成功经验要点，列表形式]

#### 架构设计原则

[关键架构原则 / 设计决策摘要]

#### 经验总结

[重要经验总结 / 教训 / 可复用模式]

### 🔍 关键变更记录

#### Git 提交记录汇总（精选）

```text
[提交哈希] - [类型(模块)]: [提交描述] ([日期])
[提交哈希] - [类型(模块)]: [提交描述] ([日期])
```

**注**: 仅列具有代表性或高影响的提交，完整列表见 commits_summary.txt

---

## 已知限制 / 已知问题

| ISSUE_ID | 描述 | 影响 | 临时方案 | 状态 |
|----------|------|------|----------|------|
| KNOWN- |  |  |  | OPEN |

---

## 统计与指标

> 建议直接引用 `summary_metrics.json` 并补充本版本特定业务指标；breaking_api / risks 可与对应脚本输出对齐。

```json
{
  "range": "[旧]->[新]",
  "commits_total": 0,
  "features": 0,
  "fixes": 0,
  "improvements": 0,
  "breaking_api": 0,
  "known_issues": 0
}
```

---

## 提交摘要 (来自外部文件)

> 文件: commits_summary.txt （generate-commits-summary.ps1 生成 + 人工精炼）

```text
[示例]
feat: xxx
fix: yyy
refactor: zzz
```

---

## 升级指导 (Upgrade Guide)

| 步骤 | 操作 | 说明 | 相关ID |
|------|------|------|--------|
| 1 | 备份配置 |  |  |
| 2 | 应用新版本 |  |  |
| 3 | 更新配置项 |  | CMP- |
| 4 | 验证核心功能 |  | DISC- |

---

## 版本评价 (Summary)

| 维度 | 评价 | 说明 |
|------|------|------|
| 稳定性 | 优秀/良好/一般 |  |
| 性能 | 优秀/良好/一般 |  |
| 安全性 | 优秀/良好/一般 |  |
| 升级难度 | 低/中/高 |  |

---

**生成时间**: [时间]  
**模板版本**: v2  
**状态**: [草稿/最终]
