# 🔄 版本对比工作流程模板

> **版本特点**: 分阶段分析 + 模块化对比 + 上下文管理 + 安全工作区

## 📑 目录结构

- [📖 工作流简介](#-工作流简介)
- [📑 快速导航](#-快速导航)
- [🤖 自动生成区域](#-自动生成区域)
  - [📝 任务信息](#-任务信息)
- [📁 目录结构](#-目录结构)
- [📋 标准流程](#-标准流程)
  - [步骤1：用户描述对比需求](#步骤1用户描述对比需求)
  - [步骤2：AI解析并格式化](#步骤2ai解析并格式化)
  - [步骤3：用户确认信息](#步骤3用户确认信息)
  - [步骤4：创建专用文档](#步骤4创建专用文档)
  - [步骤5：初始化分析环境](#步骤5初始化分析环境)
  - [步骤6：创建版本工作区](#步骤6创建版本工作区)
  - [步骤7：总体变更分析](#步骤7总体变更分析)
  - [步骤8：核心模块深度对比（循环）](#步骤8核心模块深度对比循环)
  - [步骤9：文档变更分析](#步骤9文档变更分析)
  - [步骤10：最终汇总流程](#步骤10最终汇总流程)
- [💡 对比原则](#-对比原则)
  - [🎯 核心方法论](#-核心方法论)
  - [📋 最佳实践](#-最佳实践)
- [📚 附录](#-附录)
  - [附录A：模板文件说明](#附录a模板文件说明)
  - [附录B：脚本工具说明](#附录b脚本工具说明)
  - [附录C：常见模块分析重点](#附录c常见模块分析重点)

## 📖 工作流简介

本工作流专为多版本差异分析和变更管理设计，采用三阶段分析模式和Git worktree隔离技术确保分析的全面性和准确性。适用于版本升级影响评估、变更日志补充、代码演进分析等场景，当前主要支持Python、C/C++项目的深度代码分析。

## 📑 快速导航

- [📋 标准流程](#-标准流程) - 10步完整对比流程
- [🔄 对比循环](#-对比循环) - 步骤8循环分析
- [📁 目录结构](#-目录结构) - 标准化文件组织
- [💡 对比原则](#-对比原则) - 核心方法论

## 🤖 自动生成区域

> **说明**: 任务专用文档中，AI将自动填充以下内容

### 📝 任务信息

- **项目**: [自动识别项目名称]
- **版本范围**: [如 V1.86 → V1.87]
- **对比目标**: [更新日志补充/变更分析/升级指导]
- **技术栈**: [主要技术框架和语言]

---

## 📁 目录结构

```text
version-comparison-system/
├── version-comparison-workflow-template.md    # 工作流模板
├── scripts/                                   # 脚本目录
│   ├── setup_worktree.ps1                     # 创建 worktree + 差异基础数据
│   ├── cleanup_worktree.ps1                   # 清理 worktree 与输出
│   ├── generate-summary-metrics.ps1           # 生成 summary_metrics.json 汇总指标
│   ├── generate-commits-summary.ps1           # 生成 commits_summary.txt 提交分组摘要
│   ├── compare-code-metrics.ps1               # 比较行数 & 方法数 metrics_files.csv
│   ├── extract-breaking-api.ps1               # 提取潜在破坏性 API 变更候选
│   ├── generate-module-impact.ps1             # 聚合模块变更并生成 module_impact.*
│   ├── risk-status-report.ps1                 # 汇总风险 ID 状态 (RSK-*
│   └── validate-ids.ps1                       # 校验 ID 唯一性与引用完整性
├── templates/
│   ├── mgmt-analysis-index.md                 # 分析索引模板
│   ├── report-module-analysis.md              # 模块分析报告模板
│   ├── report-version-summary.md              # 版本对比总结模板 (v2: ID 引用 + JSON 指标)
│   ├── analysis-stage-record.md               # 阶段分析记录模板
│   ├── update-log-template.md                 # 更新日志模板 (v2: 五段结构)
│   └── worktree-setup.md                      # 工作区设置模板
└── analysis/
    └── <任务目录>/                             
        ├── INDEX.md
        ├── worktree_outputs/                  # 建议：脚本输出归档目录
        │   ├── commits_overview.txt
        │   ├── files_stat.txt
        │   ├── changed_files.txt
        │   ├── module_stats.json
        │   ├── worktree_setup_snapshot.json
        │   ├── summary_metrics.json
        │   ├── commits_summary.txt
        │   ├── metrics_summary.json
        │   ├── metrics_files.csv
        │   ├── breaking_api_candidates.txt
        │   ├── breaking_api_candidates.json
        │   ├── risk_status.json
        │   └── risk_status.md
        ├── stage_1_overview/
        ├── stage_2_modules/
        ├── stage_3_documentation/
        └── summary/
```

---

## 📋 标准流程

### 步骤1：用户描述对比需求

**格式**: "分析[旧版本]到[新版本]的变更，重点关注[模块/功能]，目标是[补充更新日志/升级指导/影响评估]。"

### 步骤2：AI解析并格式化

AI提取关键信息并生成标准化任务描述。

### 步骤3：用户确认信息

必须暂停执行，等待用户手动检查AI解析结果，确认或修正任务信息。

### 步骤4：创建专用文档

**AI必须执行以下操作**：

```powershell
# 示例命令 - 实际路径需根据当前工作目录调整
cd version-comparison-system
Copy-Item "version-comparison-workflow-template.md" "version-comparison-任务名.md"
```

- **首先进入version-comparison-system目录**
- 为当前对比任务创建专用的工作流文档
- 文档名应反映具体的对比任务（如：version-comparison-V1.86到V1.87.md）
- **重要的文档更新要求**：
  - **更新标题**：将专用文档的标题修改为"# 🔄 版本对比工作流程 [旧版本] → [新版本]"
  - **填充任务信息**：在自动生成区域中替换所有[]内容为具体信息
  - **确认路径正确性**：检查所有相对路径引用是否正确
- 暂停执行，提示用户切换到专用工作流文档再继续

### 步骤5：初始化分析环境

**AI必须执行以下操作**：

```powershell
# 示例命令 - 实际路径需根据当前工作目录调整
# 创建analysis目录并进入
mkdir analysis -ErrorAction SilentlyContinue; cd analysis
# 确定任务编号和创建任务专用文件夹
$taskId = (Get-ChildItem -Directory -Name | Where-Object { $_ -match '^\d+_' } | Measure-Object).Count + 1
$taskFolder = "${taskId}_版本对比描述"  # 用实际对比描述替换
mkdir $taskFolder; cd $taskFolder
# 创建分析索引文件 (使用模板: templates/mgmt-analysis-index.md)
Copy-Item "..\..\templates\mgmt-analysis-index.md" "INDEX.md"
# 创建阶段目录结构
mkdir stage_1_overview, stage_2_modules, stage_3_documentation, summary
# 为每个阶段创建README.md (使用模板: templates/analysis-stage-record.md)
Copy-Item "..\..\templates\analysis-stage-record.md" "stage_1_overview\README.md"
Copy-Item "..\..\templates\analysis-stage-record.md" "stage_2_modules\README.md"
Copy-Item "..\..\templates\analysis-stage-record.md" "stage_3_documentation\README.md"
# 为记录工作区配置复制模板 (使用模板: templates/worktree-setup.md)
Copy-Item "..\..\templates\worktree-setup.md" "worktree_setup.md"
```

- 创建任务专用文件夹，命名格式：`数字_版本对比描述`
- 创建任务级INDEX.md，用于记录该对比分析的历程
- 初始化三个分析阶段的目录和记录文件
- 创建最终汇总目录

### 步骤6：创建版本工作区

> 现在推荐使用脚本：`./scripts/setup_worktree.ps1 -Old <旧版本> -New <新版本> -Path <analysis/任务目录/worktree_outputs>`

**⚠️ 编码问题提示**: 如果在Git提交信息中遇到中文乱码显示问题，请使用编码检测脚本：

```powershell
# 智能编码检测和修复Git提交信息乱码
./scripts/git-encoding-detector.ps1 -OldVersion <旧版本> -NewVersion <新版本> -OutputDir "stage_1_overview"

# 测试模式（仅预览，不生成文件）
./scripts/git-encoding-detector.ps1 -OldVersion <旧版本> -NewVersion <新版本> -OutputDir "stage_1_overview" -TestMode
```

该脚本将：
- 自动检测Git存储编码和终端编码不匹配问题
- 设置PowerShell UTF-8输出编码解决显示乱码
- 生成正确编码的提交信息文件
- 支持UTF-8、GBK、GB2312、Big5、ISO-8859-1等多种编码

**创建后立即执行基础指标与提交摘要生成（可选自动化）**：

```powershell
# 生成汇总指标 JSON (含提交/文件/行数/模块/风险等)
./scripts/generate-summary-metrics.ps1 -Old <旧版本> -New <新版本> -Output worktree_outputs/summary_metrics.json
# 生成提交分类摘要 (commits_summary.txt)
./scripts/generate-commits-summary.ps1 -Old <旧版本> -New <新版本> -Output worktree_outputs/commits_summary.txt
# 生成行数 & 方法数差异 (目录模式需传入已创建的两个 worktree 路径)
./scripts/compare-code-metrics.ps1 -OldPath worktree_outputs/worktree_<旧版本> -NewPath worktree_outputs/worktree_<新版本> -OutputDir worktree_outputs
```

新增：代码指标分为两类：
- 全量聚合(多语言+函数计数可信度)：run-code-metrics.ps1 → metrics_code_enriched.json（供 summary 富集）
- 差异视角(Python/C/C++ 行 & 函数差异 + 可选函数长度估算)：compare-code-metrics.ps1 → metrics_summary.json / metrics_files.csv

执行顺序建议：
1. 创建 worktree (setup_worktree.ps1 或手动 git worktree)
2. （可选）运行 run-code-metrics.ps1 针对新版本工作区（或两个版本分别）获取基线多语言代码规模
3. 运行 compare-code-metrics.ps1 获取差异数据
4. 运行 extract-breaking-api / generate-module-impact / risk-status-report
5. 汇总 generate-summary-metrics.ps1 带上 -CodeMetricsJson 进行富集

示例：
```powershell
./scripts/setup_worktree.ps1 -Old <旧> -New <新> -Path worktree_outputs
# 多语言聚合（新版本）
./scripts/run-code-metrics.ps1 -Root worktree_outputs/worktree_<新> -OutputDir worktree_outputs
# 代码差异 (目录模式)
./scripts/compare-code-metrics.ps1 -OldPath worktree_outputs/worktree_<旧> -NewPath worktree_outputs/worktree_<新> -OutputDir worktree_outputs -ApproximateLength
# 破坏性 API 候选
./scripts/extract-breaking-api.ps1 -Old <旧> -New <新> -OutputDir worktree_outputs
# 模块影响
./scripts/generate-module-impact.ps1 -Old <旧> -New <新> -StageDir stage_1_overview -EmitAuto -IncludeJSON
# 风险状态
./scripts/risk-status-report.ps1 -Root . -OutputDir worktree_outputs
# 汇总（富集所有来源）
./scripts/generate-summary-metrics.ps1 -Old <旧> -New <新> -Output worktree_outputs/summary_metrics.json `
  -RiskStatusJson worktree_outputs/risk_status.json `
  -BreakingApiJson worktree_outputs/breaking_api_candidates.json `
  -ModuleImpactJson stage_1_overview/module_impact.json `
  -CodeMetricsJson worktree_outputs/metrics_code_enriched.json
```

生成的文件在后续步骤将被引用：

- summary_metrics.json → 版本汇总(report-version-summary.md)
- metrics_code_enriched.json → summary 富集中的 code_metrics_* 字段
- metrics_summary.json / metrics_files.csv → 差异统计与热点文件分析
- module_impact.* → 模块分析计划与优先级排序
- breaking_api_candidates.* → 兼容性评估引用
- risk_status.* → 风险与可信度引用

**AI必须执行以下操作**：

```powershell
# 示例命令 - 实际版本号需要替换为具体值
# 获取版本信息（从任务描述中提取）
$oldVersion = "V1.86"  # 替换为实际旧版本
$newVersion = "V1.87"  # 替换为实际新版本

# 创建两个版本的工作区进行对比 (需要在项目根目录执行)
git worktree add "worktree_${oldVersion}" $oldVersion
git worktree add "worktree_${newVersion}" $newVersion

# 验证工作区创建成功
git worktree list

# 生成基础对比数据
git log --oneline ${oldVersion}..${newVersion} > stage_1_overview\commits_overview.txt
git diff --stat ${oldVersion}..${newVersion} > stage_1_overview\files_stat.txt
git diff --name-only ${oldVersion}..${newVersion} > stage_1_overview\changed_files.txt

# 按模块生成统计数据 - 自动发现项目模块
$projectModules = git diff --name-only ${oldVersion}..${newVersion} | ForEach-Object { ($_ -split '/')[0] } | Sort-Object -Unique | Where-Object { $_ -match '^[a-zA-Z_]' }
foreach ($module in $projectModules) {
    if (Test-Path "..\..\..\..\$module") {
        git diff --stat ${oldVersion}..${newVersion} -- $module/ > "stage_1_overview\${module}_changes_stat.txt"
    }
}
```

**重要改进**:

- ✅ **双版本工作区**: 创建新旧两个版本的完整工作区
- ✅ **自动模块发现**: 根据实际变更文件自动识别项目模块
- ✅ **工作区验证**: 确保工作区创建成功
- ✅ **便于对比**: 两个完整的代码版本便于深度对比分析

### 步骤7：总体变更分析

进入分阶段分析流程。

#### 7.1 📊 提交记录分析

> 如已运行 `generate-commits-summary.ps1`，可直接引用 worktree_outputs/commits_summary.txt 中的分类统计与示例提交；否则手动分析 commits_overview.txt。

- 分析commits_overview.txt，按功能类型分类：
  - `feat`: 新功能特性
  - `fix`: 问题修复
  - `refactor`: 重构优化
  - `docs`: 文档更新
  - `perf`: 性能优化
  - `chore`: 维护任务

#### 7.2 📈 文件变更统计

> 若已生成 summary_metrics.json，可直接获取 files_changed / lines_added / lines_deleted；compare-code-metrics.ps1 的 metrics_files.csv 可辅助识别热点文件。

可选：提取潜在破坏性 API 变更候选（供兼容性评估 / report-version-summary 与更新日志使用）:

```powershell
./scripts/extract-breaking-api.ps1 -Old $oldVersion -New $newVersion -OutputDir worktree_outputs
# 输出: breaking_api_candidates.txt / .json
```

- 分析files_stat.txt，识别变更热点：
  - 变更行数最多的文件
  - 新增/删除的文件
  - 重构影响范围

#### 7.3 🗂️ 模块影响分析

执行目标：识别受影响模块、聚合模块变更规模并生成结构化 `module_impact.md` 支撑 7.4 计划确认。

推荐使用脚本：`./scripts/generate-module-impact.ps1`

示例：

```powershell
# 基于旧/新版本直接生成 (自动创建 changed_files.txt)
./scripts/generate-module-impact.ps1 -Old $oldVersion -New $newVersion -StageDir stage_1_overview -EmitAuto -IncludeJSON

# 若已存在 changed_files.txt
./scripts/generate-module-impact.ps1 -ChangedFilesPath stage_1_overview/changed_files.txt -StageDir stage_1_overview -Depth 1 -EmitAuto
```

脚本要点：

- 动态抽取路径前 Depth 层（默认1）作为模块键；根目录文件归类 `_root`
- 输出: module_impact.md (+ 可选 module_impact_auto.txt / module_impact.json)
- 表格含：模块 | 变更文件数 | 示例文件 (前N=5)
- 供人工补充优先级、行为影响、风险 (RSK-)、破坏性 API、依赖影响

> 若项目源代码集中在 `src/` 等单一路径，可使用 `-Depth 2` 获得 `src/子目录` 级聚合；后续可扩展脚本支持忽略前缀目录参数。

可选：生成风险状态汇总，便于后续在版本总结 / 更新日志的风险与可信度部分引用：

```powershell
./scripts/risk-status-report.ps1 -Root . -OutputDir worktree_outputs
# 输出: risk_status.json / risk_status.md
```

生成后：快速人工检查 `module_impact.md` 模块划分是否合理，然后进入 7.4 计划确认。

#### 7.4 🎯 模块分析计划确认

- AI根据变更分布**自动生成模块分析计划**
- 在stage_1_overview/module_impact.md中列出：
  - 📊 **变更统计**: 各模块的文件数量和变更行数
  - 🎯 **建议分析的模块**: 按影响程度排序
  - ⚠️ **风险评估**: 各模块变更的潜在影响
- **必须暂停执行，等待用户确认**：
  - [ ] 确定需要深度分析的模块
  - [ ] 确定可以跳过的模块（如仅样式调整）
  - [ ] **确定分析顺序**: 用户最终确认模块分析的优先级顺序
- 用户确认后，**动态创建**对应模块的分析文件：

```powershell
# 示例命令 - 实际模块名需要替换
# 为确认需要分析的模块创建分析文件 (使用模板: templates/report-module-analysis.md)
Copy-Item "..\..\templates\report-module-analysis.md" "stage_2_modules\${module_name}_analysis.md"
```

**记录要点**: 在stage_1_overview/module_impact.md中记录总体变更规模、主要模块影响和优先级排序，以及**用户确认的最终分析计划和执行顺序**。

---



### 步骤8：核心模块深度对比（循环）

> **💡 提示**: 这是对比循环阶段，会根据用户确认的模块列表进行循环分析

**⚠️ 重要流程变更**: 步骤8的分析模块**不再预设**，而是基于步骤7的自动识别结果和用户确认。

#### 8.1 循环执行模块分析

##### 动态模块分析流程

1. **基于步骤7结果**: 从module_impact.md获取需要分析的模块列表
2. **按影响程度排序**: 优先分析变更较大的模块
3. **用户确认后执行**: 只分析用户确认需要的模块
4. **自底向上分析**: 按依赖关系顺序分析（基础→业务→核心）

##### 标准模块分析模板

对于每个确认需要分析的模块，使用以下模板：

```bash
# 通用模块分析命令模板
git diff --stat $oldVersion..$newVersion -- [模块路径]/
git diff --name-only $oldVersion..$newVersion -- [模块路径]/
git log --oneline $oldVersion..$newVersion -- [模块路径]/
```

> **📋 参考**: 各模块的具体分析重点请参见附录C：常见模块分析重点

#### 8.2 定期总结策略

- **时间间隔**: 每运行2-5分钟进行一次总结
- **文件数量**: 每查看5-10个文件后进行一次总结
- **分析深度**: 每完成一个模块分析后立即总结

---

### 步骤9：文档变更分析

#### 9.1 📝 文档变更分析

```bash
# 分析文档变更
git diff $oldVersion..$newVersion -- docs/
git diff $oldVersion..$newVersion -- workflow/
git diff $oldVersion..$newVersion -- "*.md"
```

**记录方式**: 在stage_3_documentation/documentation_changes.md中简要记录：

- 新增文档类型和用途
- 重要文档更新内容
- 文档结构变更
- 工作流和模板系统变化

**注**: documentation_changes.md无需使用特定模板，直接记录文档变更即可

---

### 步骤10：最终汇总流程

#### 10.1 版本对比报告 (version_comparison_report.md)

> 可直接嵌入或引用 worktree_outputs/summary_metrics.json 与 metrics_summary.json（如已生成），避免重复人工统计。

**使用模板**: `templates/report-version-summary.md`

将各阶段的分析结果整合到summary/version_comparison_report.md中：

```powershell
# 示例命令 - 需要在正确的目录层级执行
# 复制版本对比报告模板
Copy-Item "..\..\templates\report-version-summary.md" "summary\version_comparison_report.md"
```

**填充内容要求**:

- 基于各阶段分析结果填充模板内容
- 重大变更概览：新增功能、优化重构、问题修复
- 模块变更详情：基础支撑、业务逻辑、核心功能模块
- 兼容性影响评估：破坏性变更、配置变更、依赖变更

#### 10.2 更新日志草稿生成

> 使用 worktree_outputs/commits_summary.txt 提供“提交摘要”；必要时引用 metrics_summary.json 支撑“技术成果”数据。

**使用模板**: `templates/update-log-template.md`

基于分析结果生成更新日志草稿：

```powershell
# 示例命令 - 需要在正确的目录层级执行
# 复制更新日志模板
Copy-Item "..\..\templates\update-log-template.md" "summary\update_log_draft.md"
```

**填充内容要求**:

- **版本信息**: 从任务描述提取版本号和时间范围
- **新增功能**: 基于Stage 2模块分析的功能性变更
- **优化重构**: 基于性能优化和架构改进分析
- **问题修复**: 基于bug修复和稳定性改进
- **技术成果**: 基于代码统计和性能数据
- **破坏性变更**: 需要特别注意的兼容性问题

**📋 质量保证检查**:

生成更新日志草稿时，需要保证：

- [ ] 分析结果的准确性
- [ ] 更新日志内容的完整性
- [ ] 更新日志格式的一致性

**⚠️ 重要**: 此步骤生成的是更新日志草稿，用于后续编辑和完善

#### 10.3 现有更新日志文件更新确认

**目标**: 检查是否存在需要更新的现有更新日志文件

#### 🔍 更新日志文件检查

**用户确认步骤**:

1. **询问用户**: 是否存在现有的更新日志文件需要更新？
2. **文件路径确认**: 如果存在，请用户提供具体文件路径
3. **更新策略确认**: 确认是追加内容还是替换特定章节

#### 📝 执行更新操作

**如果用户提供了现有更新日志文件路径**:

```powershell
# 示例命令 - 实际路径由用户提供
# 备份现有更新日志文件
Copy-Item "[用户提供的路径]" "[用户提供的路径].backup"

# 基于草稿内容更新现有更新日志
# 具体更新方式根据用户确认的策略执行
```

**更新内容要求**:

- **版本章节**: 基于summary/update_log_draft.md中的内容
- **保持格式**: 与现有更新日志的格式风格保持一致
- **追加方式**: 在适当位置插入新版本的更新内容
- **时间排序**: 确保版本按时间顺序正确排列

**⚠️ 重要确认点**:

- [ ] 现有更新日志文件路径正确性
- [ ] 更新内容的准确性和完整性
- [ ] 格式风格的一致性
- [ ] 用户确认执行更新操作

**暂停执行**: 等待用户确认所有更新内容无误后再继续

#### 10.4 工作区清理确认

**⚠️ 重要**: 完成分析后，用户可以选择是否清理工作区。

#### 🔍 清理前确认

1. **用户选择**: 向用户确认是否清理工作区
   - 选择1: 立即清理工作区（节省存储空间）
   - 选择2: 保留工作区（便于后续深度分析）
2. **结果验证**: 确保所有重要发现都已记录
3. **获得清理许可**: 仅在用户明确选择清理时才执行

#### 💾 保留工作区的优势

- **深度分析**: 可以进行更详细的文件对比
- **问题验证**: 遇到疑问时可以快速验证
- **后续分析**: 支持多轮分析和补充分析
- **学习参考**: 保留完整的版本状态便于学习

#### 🗑️ 清理工作区的优势

- **节省空间**: 释放磁盘存储空间
- **保持整洁**: 避免工作区累积
- **避免混淆**: 减少多个工作区的版本混淆

**清理命令** (仅在用户选择清理时执行):

```bash
# 示例命令 - 实际路径和版本号需要替换
# 清理两个版本工作区
git worktree remove analysis/任务文件夹/worktree_V1.86
git worktree remove analysis/任务文件夹/worktree_V1.87

# 确认清理完成
git worktree list
```

#### 10.5 归档任务专用文档

**(新增) 首先执行 ID 校验脚本，确保所有引用一致性**：

```powershell
# 在任务根目录 (analysis/<任务目录>) 调用，输出至 worktree_outputs
./scripts/validate-ids.ps1 -Root . -OutputDir worktree_outputs -FailOnDuplicate:$false
```

脚本校验：

- ID 前缀: RSK-/DISC-/MOD-/API-/CMP-
- 唯一性：检测重复 ID 并列出出现位置
- 引用完整性：统计各 ID 出现次数，供人工确认是否缺少定义或说明
- 输出: id_validation.json / id_validation.md

**目标**: 将任务专用工作流文档归档到分析文件夹，便于完整记录

```powershell
# 示例命令 - 实际路径需要根据当前目录调整
# 将任务专用文档从根目录复制到当前分析目录
Copy-Item "..\..\version-comparison-任务名.md" "."

# 重命名为标准归档格式
Rename-Item "version-comparison-任务名.md" "workflow_document_archive.md"
```

**文档来源**: 从`version-comparison-system/version-comparison-任务名.md`复制并重命名
**归档目标**: 当前分析任务目录下的`workflow_document_archive.md`

**归档内容**:

- 完整的工作流执行记录
- 用户确认和决策记录
- 分析过程中的调整和优化
- 遇到的问题和解决方案

**归档价值**:

- **完整性**: 保留完整的分析执行过程
- **可复现**: 后续分析时可以参考执行细节
- **经验积累**: 为改进工作流程提供依据
- **团队学习**: 团队成员可以学习分析方法

#### 10.6 一致性对齐校验（新增）

在清理前运行对齐校验脚本，确保所有关键产出内部一致：
```powershell
./scripts/alignment-checker.ps1 -AnalysisDir analysis/<任务目录> -FailOnMismatch
```
校验内容：
- summary_metrics.json 核心数值 vs 实际 git 统计
- enrichment 中 *_source 文件是否存在
- metrics_summary.json 一致性提示（若存在）
- id_validation.json 中 ID 在报告/更新日志引用覆盖
- 缺失/未引用/数值差异列出于 alignment_report.*

若失败（pass=false），需整改后重跑；仅在通过后再考虑 cleanup。

---

## 💡 对比原则

### 🎯 核心方法论

#### 自底向上分析法

- **原理**: 从基础工具层开始，逐层向上分析依赖关系
- **顺序**: tools → logic → algorithm → config → docs
- **优势**: 确保理解变更的完整影响链

#### 分阶段定期总结

- **原理**: 避免上下文过载，保持分析质量
- **策略**: 每2-5分钟或5-10个文件后总结
- **记录**: 使用标准模板记录阶段发现

#### 版本工作区隔离

- **原理**: 使用Git worktree创建安全的版本对比环境
- **位置**: 在分析目录内，确保AI可访问
- **管理**: 分析完成后需用户确认才清理

#### 模块化文档组织

- **原理**: 按分析阶段和模块分别记录
- **结构**: 阶段目录 + 模块文件 + 汇总报告
- **索引**: 使用INDEX.md维护导航结构

### 📋 最佳实践

#### 变更识别

- 重点关注功能性变更，界面变更简要记录
- 识别破坏性变更和兼容性影响
- 评估性能和稳定性影响

#### 文档质量

- 使用统一的分析模板
- 保持客观的变更描述
- 提供具体的代码示例

#### 协作效率

- 及时记录分析发现
- 定期与用户确认方向
- 保持分析节奏稳定

---

## 📚 附录

### 附录A：模板文件说明

| 模板 | 版本 | 功能 | 关键特性 | 主要变化 |
|------|------|------|----------|----------|
| mgmt-analysis-index.md | v1 | 任务导航/阶段总览 | 阶段进度 + 发现指针 | ID 指针最小化描述 |
| analysis-stage-record.md | v1 | 单阶段执行记录 | Checkpoints + 风险表 | 多 checkpoint 支持 |
| report-module-analysis.md | v1 | 模块级深度对比 | 模块/文件/函数多级表 | 内联破坏性 API & 风险表 |
| report-version-summary.md | v2 | 全局聚合总结 | ID 引用 + JSON 指标 | 去重 + 可信度块 |
| update-log-template.md | v2 | 面向发布说明 | 五段结构 + 指标 JSON | 兼容性与已知问题分离 |
| worktree-setup.md | v1 | 工作区建立记录 | 脚本化创建/验证/清理 | 去除 snippet 机制 |

### 附录B：脚本工具说明

| 脚本 | 作用 | 主要输出 | 典型使用阶段 |
|------|------|----------|--------------|
| setup_worktree.ps1 | 创建双版本 worktree & 初始差异文件 | commits_overview.txt 等 | 步骤6 |
| cleanup_worktree.ps1 | 清理 worktree 与输出 | (清理动作) | 10.4 |
| git-encoding-detector.ps1 | **智能编码检测和Git数据提取** ⭐ | UTF-8编码的commits文件，编码分析报告 | 步骤6 (编码问题修复) |
| run-code-metrics.ps1 | 多语言代码规模/函数聚合 | metrics_code_enriched.json | 6 (可选) |
| compare-code-metrics.ps1 | Python/C/C++ 差异行/函数统计 | metrics_summary.json / metrics_files.csv | 6 后 / 7.2 |
| generate-summary-metrics.ps1 | 汇总核心 & 富集指标 | summary_metrics.json | 6/7 结束后 |
| generate-commits-summary.ps1 | 提交分组摘要 | commits_summary.txt | 6 后 / 7.1 |
| extract-breaking-api.ps1 | 破坏性 API 候选 | breaking_api_candidates.* | 7.2 / 7.3 |
| generate-module-impact.ps1 | 模块变更聚合 | module_impact.* | 7.3 |
| risk-status-report.ps1 | 风险状态汇总 | risk_status.* | 7.3 / 10 |
| validate-ids.ps1 | ID 唯一 & 引用统计 | id_validation.* | 10.5 前 |
| alignment-checker.ps1 | 产出一致性校验 | alignment_report.* | 10.6 |

> 说明：compare-code-metrics 与 run-code-metrics 互补：前者针对版本差异，后者提供新版本(或各版本)整体规模与外部工具置信度；summary_metrics 只直接读取 run-code-metrics 产物。encoding-aware-git-extractor-fixed.ps1 专门用于解决混合编码环境下的Git信息提取问题，支持UTF-8、GBK、GB2312、Big5、ISO-8859-1等编码。

### 附录C：常见模块分析重点

以下表格列出了各模块的主要分析重点，供步骤8循环分析时参考：

| 模块 | 分析重点 | 关注要素 |
|------|----------|----------|
| 🛠️ **tools/** | 新增工具组件和MCP服务器、公共组件重构、文件IO处理变更、配置管理工具变更 | 工具功能、组件复用、性能优化 |
| ⚙️ **logic/** | 配置管理系统变更、通信模块变更、设计模块变更、新增业务功能 | 业务逻辑、接口设计、功能完整性 |
| 🧮 **algorithm/** | 新增/删除的核心组件、核心功能逻辑变更、接口变更和兼容性影响、性能优化相关变更 | 算法准确性、性能指标、数值稳定性 |
| 🎨 **ui/** | 界面组件变更、用户交互优化、样式和布局调整 | 用户体验、界面一致性、交互逻辑 |
| 💾 **persistence/** | 数据存储机制变更、备份和导出功能、数据格式升级 | 数据完整性、兼容性、性能影响 |
| 📁 **file/** | 配置文件结构变更、新增配置项、废弃配置清理、配置管理流程变更 | 配置规范、向后兼容性、文档同步 |

> **使用说明**: 根据步骤7.4的用户确认结果，重点分析相应模块的变更内容

---

**开始分析**: 遵循10步标准流程，从版本对比需求描述开始您的系统化分析之旅。

**获取支持**: 查看 `templates/` 目录获取标准模板，参考分析索引了解进度管理。

**版本信息**: 版本对比工作流模板 v1.0.0 | 基于debug-system架构设计
