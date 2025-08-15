# Git Worktree 工作区配置模板

---
<!-- 新增：YAML Front Matter 便于自动化解析 -->
```yaml
setup_version: v1
old_version: [旧版本标签]
new_version: [新版本标签]
setup_timestamp: [执行时间]
setup_owner: GitHub Copilot
worktree_path: [worktree路径]
SETUP_VERSION: [唯一快照ID]
```

**任务名称**: [任务名称]  
**创建日期**: [日期]  
**工作区状态**: [已创建/使用中/已清理]  

---

## 📋 工作区信息

### 基本配置

- **旧版本**: [旧版本标签]
- **新版本**: [新版本标签]
- **工作区路径**: [worktree路径]
- **分析员**: GitHub Copilot

### 版本信息

- **起始提交**: [起始提交哈希]
- **目标提交**: [目标提交哈希]
- **提交差异**: [提交数量] 个提交
- **时间跨度**: [版本时间跨度]

---

## 🛠️ 工作区设置（脚本化）

> 推荐使用脚本：`scripts/setup_worktree.ps1 -Old [旧版本] -New [新版本] -Path [worktree路径]`

### 执行示例（最小）

```powershell
# 初始化（不再内联全部命令）
./scripts/setup_worktree.ps1 -Old V1.86 -New V1.87 -Path analysis/worktree_V1.86_V1.87
```

### 关键脚本职责

| 步骤 | 动作 | 说明 |
|------|------|------|
| 1 | 参数校验 | 版本标签 / 目标路径可写 |
| 2 | 创建 worktree | 双版本（如需要）或单旧版本镜像 |
| 3 | 生成初始差异文件 | commits_overview / files_stat / changed_files |
| 4 | 验证核心文件存在 | 关键模块路径探测 |
| 5 | 输出 JSON 快照 | worktree_setup_snapshot.json |

<!-- NOTE: 已移除 snippet 机制，所有引用表格需在各模板内联维护。 -->

---

## 🔍 工作区验证

### 验证表（执行后填写）

| 项 | 检查命令/方式 | 结果(✓/✗) | 备注 |
|----|----------------|-----------|------|
| worktree 创建成功 | git worktree list |  |  |
| 标签解析正确 | git describe --tags |  |  |
| 关键模块存在 algorithm | Test-Path algorithm/ |  |  |
| 关键模块存在 logic | Test-Path logic/ |  |  |
| 关键模块存在 tools | Test-Path tools/ |  |  |
| Git 状态干净 | git status --porcelain |  |  |

### 路径 / 版本确认（示例脚本输出）

```text
old_version: V1.86
new_version: V1.87
worktree_path: analysis/worktree_V1.86_V1.87
```

---

## 📁 目录存在性检查（可选）

| 目录 | 期望 | 存在(✓/✗) | 说明 |
|------|------|-----------|------|
| algorithm/ | 核心算法 |  |  |
| logic/ | 业务逻辑 |  |  |
| tools/ | 工具支撑 |  |  |
| ui/ | UI 模块 |  |  |
| file/ | 配置文件 |  |  |

---

## 🔄 分析准备最小集合

| 检查项 | 结果(✓/✗) | 备注 |
|--------|-----------|------|
| git diff 可用 |  |  |
| 文件读取可用 |  |  |
| 模块自动发现脚本 |  |  |
| 指标快照写入 |  |  |

> 目录结构详细说明已迁移至主 README / reference，不再在本模板展开。

---

## 🧹 清理计划（结构化）

| 条件 | 是否满足(✓/✗) | 备注 |
|------|---------------|------|
| 分析结果归档完成 |  |  |
| 汇总报告生成 |  |  |
| 更新日志草稿生成 |  |  |
| 用户确认可清理 |  |  |

### 清理命令（脚本）

```powershell
./scripts/cleanup_worktree.ps1 -Path analysis/worktree_V1.86_V1.87
```

---

## 📋 故障排除（摘要）

> 详细 FAQ → `reference/worktree_troubleshooting.md`

| 问题 | 症状 | 快速处理 |
|------|------|-----------|
| 路径已存在 | fatal: already exists | 移除残留目录后重试 |
| 标签解析失败 | invalid reference | git fetch --tags 后重试 |
| 路径过长 | Windows 限制 | 使用短路径别名 |

---

**配置完成时间**: [完成时间]  
**工作区生命周期**: [预期使用时长]  
**负责人**: GitHub Copilot  

<!-- 原有长命令块与逐项说明已精简；如需历史版本请查看存档。 -->
