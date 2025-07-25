# 🛠️ 调试工作流程模板

> **版本特点**: 简洁语言 + 人工确认机制 + 精炼经验总结

## 📑 快速导航

- [📋 标准流程](#-标准流程) - 7步完整调试流程
- [🔄 调试循环](#-调试循环) - 6步核心循环
- [📁 目录结构](#-目录结构) - 标准化文件组织
- [💡 调试原则](#-调试原则) - 核心方法论

## 🤖 自动生成区域

> **说明**: 任务专用文档中，AI将自动填充以下内容

### 📝 任务信息

- **项目**: [自动识别项目类型和技术栈]
- **问题**: [用户描述的具体问题]
- **目标**: [解决方案和成功标准]
- **环境**: [技术环境和依赖]

---

## 📁 目录结构

```text
debug-system/
├── debug_workflow_template.md      # 调试工作流模板
├── debug_workflow_任务名.md         # 任务专用文档
├── templates/                     # 模板文件
│   ├── mgmt-bug-list.md          # Bug清单模板
│   ├── report-bug-detail.md      # Bug详细报告模板
│   ├── mgmt-task-index.md        # 任务索引模板
│   ├── mgmt-debug-index.md       # 调试索引模板
│   ├── debug-round-record.md     # 轮次记录模板
│   ├── report-debug-summary.md   # 调试总结报告模板
│   ├── report-lessons-learned.md # 经验教训模板
│   ├── report-final-analysis.md  # 最终分析报告模板
│   └── debug-environment-setup.md # 环境配置模板
├── buglist/                       # Bug管理目录
│   ├── bug_list.md               # Bug简要记录和统计 (从模板创建)
│   ├── to_fix/                   # 待修复Bug说明文档
│   └── fixed/                    # 已解决Bug说明文档
└── debug/
    ├── workflow_archive/          # 已完成任务的工作流文档存档
    └── 1_任务描述/                # 任务专用文件夹
        ├── INDEX.md              # 任务调试索引
        ├── debug_workflow_任务名.md # 工作流文档副本
        └── 1/                    # 调试轮次
            ├── README.md         # 调试记录
            ├── src/              # 工作文件
            ├── core/             # 核心解决方案
            ├── archive/          # 重要历程和文件备份
            │   └── backup_sources.md # 备份文件来源说明
            ├── deprecated/       # 废弃文件
            ├── docs/             # 分析文档
            ├── logs/             # 测试日志
            └── files/            # 其他文件
```

---

## 📋 标准流程

### 步骤1：用户描述问题

**格式**: "我的[项目类型]项目使用[技术栈]，在[操作]时出现[错误现象]。希望[解决目标]。"

### 步骤2：AI解析并格式化

AI提取关键信息并生成标准化任务描述。

### 步骤3：用户确认信息

必须暂停执行，等待用户手动检查AI解析结果，确认或修正任务信息，这一步骤可能持续多轮（步骤2/3），直至用户同意进入下一步骤。

### 步骤4：创建专用文档

**AI必须执行以下操作**：

```powershell
cd debug-system
Copy-Item "debug_workflow_template.md" "debug_workflow_任务名.md"
```

- **首先进入debug-system目录**：确保在工作流模板文档所在的正确目录
- 为当前调试任务创建专用的工作流文档
- 文档名应反映具体的调试任务（如：debug_workflow_高DPI缩放问题.md）
- **更新自动生成区域**：在任务专用文档中填充具体的任务信息
- 暂停执行，提示用户切换到专用工作流文档再继续

### 步骤5：初始化调试环境

**AI必须执行以下操作**：

```powershell
# 首先初始化Bug管理系统（如果不存在）
mkdir buglist -ErrorAction SilentlyContinue
Copy-Item "templates\mgmt-bug-list.md" "buglist\bug_list.md" -ErrorAction SilentlyContinue
# 创建debug目录并进入
mkdir debug; cd debug
# 确定任务编号和创建任务专用文件夹
$taskId = (Get-ChildItem -Directory -Name | Where-Object { $_ -match '^\d+_' } | Measure-Object).Count + 1
$taskFolder = "${taskId}_任务描述"  # 用实际任务描述替换
mkdir $taskFolder; cd $taskFolder
# 创建任务索引文件
Copy-Item "..\..\templates\mgmt-task-index.md" "INDEX.md"
# 创建第一轮调试环境
mkdir 1\{src,core,archive,deprecated,docs,logs,files}
Copy-Item "..\..\templates\debug-round-record.md" "1\README.md"
# 创建备份来源说明文件
"# 备份文件来源说明`n`n本文件记录archive目录下各备份文件的来源和备份时间。`n`n## 备份记录`n" | Out-File "1\archive\backup_sources.md" -Encoding UTF8
```

- 首先初始化Bug管理系统（不依赖于debug文件夹）
- 创建任务专用文件夹，命名格式：`数字_任务描述`
- 创建任务级INDEX.md，用于记录该专题的调试历程
- 初始化第一轮调试环境和标准目录结构
- 创建备份来源说明文件，用于记录文件备份信息

### 步骤6：开始调试循环

进入6步调试循环，详见下节。

### 步骤7：完成检查决策

评估问题解决状态，决定生成报告或开展下一轮调试。

**评估标准**：

- ✅ 主要目标已达成
- ✅ 核心问题已解决
- ✅ 系统运行稳定
- ✅ 无重大新问题

**决策流程**：

**满足条件** → **执行最终归档** → **复制工作流文档** → **更新任务INDEX.md** → **存档工作流文档** → **生成总结报告**

**不满足** → 创建下轮调试环境

**满足条件时的归档步骤**：

1. **🗂️ 执行最终归档**: 将各轮次src中的文件按重要性分类到core/archive/deprecated目录
2. **📋 检查并处理Bug列表**:
   - **检查bug_list.md**: 仔细查看 `buglist/bug_list.md`中的待修复Bug列表，确认本次调试是否解决了其中的问题
   - **移动已解决Bug文档**: 如果本次解决了bug_list.md中记录的Bug，将对应的Bug说明文档从 `buglist/to_fix/`移动到 `buglist/fixed/`
   - **更新Bug说明文档**: 在移动后的Bug说明文档中添加解决信息（解决日期、解决方案、相关文件等）
   - **更新bug_list.md**: 将已解决的Bug从待修复列表移至已解决列表，更新Bug统计信息
   - **创建新Bug文档**: 为新发现的问题编写详细的Bug说明文档，使用 `templates/report-bug-detail.md`模板，保存到 `buglist/to_fix/`目录，并在bug_list.md中添加记录
3. **📄 复制工作流文档**: 将 `debug_workflow_任务名.md`复制到任务文件夹根目录
4. **📋 更新任务INDEX.md**: 记录该专题调试的完整历程、问题、进展、结论，并更新任务状态
5. **🏷️ 存档工作流文档**: 将 `debug_workflow_任务名.md`移动到 `debug/workflow_archive/`目录进行存档
6. **📝 生成总结报告**: 完成任务的总结文档

> **📁 最终归档要求**: 生成报告前必须完成所有调试轮次的最终归档，确保core目录包含完整解决方案
>
> **📄 工作流文档管理**: 将任务专用工作流文档复制到任务文件夹根目录，然后移动原文档到workflow_archive进行存档
>
> **📋 任务INDEX.md更新要求**: 问题完全解决后必须更新任务文件夹内的 `INDEX.md`，记录该专题调试的完整历程、问题、进展、结论，并更新任务状态
>
> **📄 任务INDEX.md模板**: 使用 `templates/mgmt-task-index.md`创建任务级索引文件

**文件命名规范**：

- 任务文件夹：`数字_任务描述` (如：1_高DPI缩放问题, 2_仿真图像保存错误)
- 调试轮次：数字编号 (1/, 2/, ...)
- 备份文件：原文件名_bak.扩展名
- 工作流文档：debug_workflow_任务名.md
- 归档文件：按重要性分类存放

**任务完成归档示例**：

```powershell
# 复制工作流文档到任务文件夹
Copy-Item "debug_workflow_仿真图像保存错误.md" "debug\3_仿真图像保存错误\"
# 更新任务INDEX.md（手动编辑完成调试记录）
# 移动工作流文档到存档目录
Move-Item "debug_workflow_仿真图像保存错误.md" "debug\workflow_archive\"
```

**Bug处理操作示例**：

```powershell
# 步骤1：检查bug_list.md，确认本次调试解决的Bug
Get-Content "buglist\bug_list.md" | Select-String "BUG-\d+" | ForEach-Object { Write-Host $_.Line }

# 步骤2：如果解决了现有Bug（如BUG-001），执行以下操作：
# 移动Bug说明文档到已解决目录
Move-Item "buglist\to_fix\BUG-001_高DPI缩放问题.md" "buglist\fixed\"

# 步骤3：更新被移动的Bug说明文档，添加解决信息
# 在文档中添加：
# - 解决日期：2025-XX-XX
# - 解决方案：[具体解决方案描述]
# - 相关文件：[修改的文件列表]
# - 调试轮次：第X轮

# 步骤4：更新bug_list.md
# 从待修复列表中移除已解决的Bug
# 在已解决列表中添加该Bug
# 更新统计信息（待修复数量-1，已解决数量+1）

# 步骤5：如果发现新Bug，创建新的Bug说明文档
Copy-Item "templates\report-bug-detail.md" "buglist\to_fix\BUG-XXX_新问题描述.md"
# 在bug_list.md中添加新Bug的记录
```

---

## 🔄 调试循环

### 6.1 📋 计划

- 确定本轮调试目标
- 分析上轮遗留问题
- 制定具体测试计划

### 6.2 🔍 分析

- 复现问题现象
- 定位问题范围
- 确定关键链路
- 分析错误原因
- **AI可以请求**: 网络资源、环境信息、配置详情等额外信息
- **推荐**: 使用小工作集方法隔离问题
- **注意**: 谋定而后动，充分和仔细的观察和思考会大幅度提升工作效率

### 6.3 💡 修正

- 设计解决方案
- 评估方案风险
- 选择最优策略

### 6.4 ⚙️ 执行

- **文件备份**: 修改任何文件前，先备份到当前轮次的archive目录
- 实施代码修改（务必生成代码文件作为过程资产，不要使用-c在终端执行python代码）
- 执行测试验证

**文件备份规范**：

```powershell
# 备份文件到archive目录，文件名加_bak后缀
Copy-Item "原文件路径" "当前轮次\archive\原文件名_bak.扩展名"
# 在backup_sources.md中记录备份信息
"- 原文件名_bak.扩展名: 来源 `"原文件路径`" (备份时间: $(Get-Date))" | Add-Content "当前轮次\archive\backup_sources.md"
```

> **🤖 AI限制提醒**:
>
> - AI可能无法直接查看测试执行结果
> - 此时应请求**用户手动执行测试**并反馈结果
> - **反馈格式**: "测试结果：[成功/失败]，现象：[具体描述]"

### 6.5 ✅ 检查

- 检查日志文件和控制台输出
- 分析用户反馈的测试结果
- 确认问题解决状态
- 识别新出现问题（如有）

> **说明**: 此阶段检查6.4执行结果，不执行新操作

### 6.6 📊 记录

- 更新调试文档
- **🗂️ 执行本轮归档**: 将src中的文件按重要性分类到core/archive/deprecated目录
- **📋 更新任务INDEX.md**: 记录本轮调试的进展和发现
- 规划下轮目标

**轮次归档规范**：

```powershell
# 创建下一轮环境（如果需要继续）
$nextRound = $currentRound + 1
mkdir $nextRound\{src,core,archive,deprecated,docs,logs,files}
Copy-Item "..\..\templates\debug-round-record.md" "$nextRound\README.md"
"# 备份文件来源说明`n`n本文件记录archive目录下各备份文件的来源和备份时间。`n`n## 备份记录`n" | Out-File "$nextRound\archive\backup_sources.md" -Encoding UTF8
```

---

## 💡 调试原则

### 🎯 核心方法论

#### 小工作集调试法

- **原理**: 创建最小化独立测试环境
- **适用**: 复杂系统中特定问题隔离
- **步骤**: 简化环境 → 简化数据 → 精确监控 → 问题复现

#### 分层归档原则

- **🔴 Core**: 5-10个核心解决方案文件
- **📚 Archive**: 重要调试历程和阶段成果
- **🗑️ Deprecated**: 无效或被替代的文件

#### 人机协作模式

- **AI负责**: 分析、建议、代码生成
- **用户负责**: 测试执行、结果确认、决策选择、提供额外信息
- **信息请求**: AI可能请求网络资源、环境信息、配置详情等
- **协作要点**: 及时反馈测试结果，明确描述现象，配合信息收集

#### 多层级测试策略

- **原理**: 建立自动化测试金字塔，快速定位问题层级
- **适用**: 复杂系统调试和修复验证
- **步骤**: 单元测试 → 集成测试 → 端到端测试 → 问题定位

#### 数据流验证法

- **原理**: 验证工作流间参数传递的完整性和正确性
- **适用**: 多模块协作和接口调用问题
- **步骤**: 输入验证 → 处理监控 → 输出检查 → 异常捕获

#### 前置条件检查

- **原理**: 执行前确认环境和依赖满足运行条件
- **适用**: 环境敏感和依赖复杂的系统
- **步骤**: 环境检查 → 依赖验证 → 权限确认 → 资源评估

#### 结构化日志记录

- **原理**: 建立详细的执行轨迹和状态记录机制
- **适用**: 问题复现困难和调试信息不足场景
- **步骤**: 关键节点记录 → 异常详情捕获 → 性能指标监控 → 状态快照保存

#### 官方文档验证法

- **原理**: 通过官方文档确认API正确用法，避免基于错误假设的调试
- **工具支持**: 使用fetch_webpage工具获取官方文档和示例代码
- **适用场景**: 第三方库使用错误、API调用失败、版本兼容问题
- **实施步骤**:
  1. 识别相关技术栈和库的官方文档
  2. 使用工具获取官方示例和最佳实践
  3. 对比当前代码与官方示例的差异
  4. 基于官方标准修正代码实现
- **核心价值**: 确保解决方案符合官方标准，提高代码质量和稳定性

### 📋 最佳实践

#### 问题定位

- **优先使用官方文档验证**: 通过fetch_webpage工具获取官方示例，确认API正确用法
- 创建独立测试脚本
- 对比不同版本差异
- 精确监控状态变化

#### 测试策略

- 使用数学函数作标准测试数据
- 建立操作前后状态对比
- 设计可重复执行的测试
- 保留每次测试的完整日志

#### 文档记录

- 实时更新调试记录
- 详细记录失败原因
- 总结有效解决方案
- 归档可复用的方法

#### 版本管理

- 新项目推荐最新稳定版本组合
- 现有项目评估升级成本和风险
- 记录版本兼容性测试结果
- 建立版本降级应急方案

---

## 📋 文档规范

### 调试记录结构

调试记录应使用标准化模板确保信息完整性和一致性。系统已在步骤5中自动使用 `templates/debug-round-record.md` 创建每轮调试的记录文档。

**模板包含的完整结构**：

- 📋 调试目标（目标、优先级、预期时间）
- 🔍 问题分析（当前状态、复现步骤、根因分析）
- 💡 解决方案（多方案对比、选定方案）
- ⚙️ 实施记录（代码变更、配置调整、测试命令）
- ✅ 测试结果（测试环境、功能验证、性能指标）
- 📊 结果评估（成功项目、遗留问题、意外发现）
- 🎯 下一轮计划（待解决问题、建议方向、测试目标）

> **💡 使用建议**: 直接使用模板文件，无需手动创建调试记录结构。模板文件位置：`templates/debug-round-record.md`

---

## 📚 附录

### 附录A：环境配置

#### 必需工具

- **PowerShell 5.1+**: 执行调试脚本和文件操作
- **Git**: 版本控制和代码管理
- **VS Code**: 代码编辑和调试环境

#### 常用调试工具

- **Python调试器**: pdb、ipdb
- **日志分析**: tail、grep、findstr
- **性能分析**: time、Measure-Command
- **网络调试**: curl、wget、Invoke-WebRequest
- **系统监控**: Get-Process、Task Manager

#### 环境准备

```powershell
# 验证PowerShell版本
$PSVersionTable.PSVersion

# 创建调试工作空间
cd debug-system
mkdir debug -ErrorAction SilentlyContinue

# 初始化Bug管理系统
mkdir buglist -ErrorAction SilentlyContinue
Copy-Item "templates\mgmt-bug-list.md" "buglist\bug_list.md" -ErrorAction SilentlyContinue

# 验证模板文件
Get-ChildItem templates\*.md | Select-Object Name
```

### 附录B：调试检查清单

#### 调试前检查

- [ ] 确认问题描述清晰完整
- [ ] 备份重要文件和配置
- [ ] 准备测试环境和数据
- [ ] 明确调试目标和成功标准
- [ ] 检查依赖和环境要求

#### 调试过程检查

- [ ] 问题复现步骤准确
- [ ] 文件修改前已备份
- [ ] 测试结果记录完整
- [ ] 方案评估客观公正
- [ ] 轮次文档及时更新

#### 调试后检查

- [ ] 解决方案验证通过
- [ ] 相关文件正确归档
- [ ] Bug列表状态更新
- [ ] 经验教训总结记录
- [ ] 工作流文档存档

### 附录C：可用模板文件列表

#### 核心模板 (Core Templates)

| 模板文件 | 作用描述 | 使用场景 |
|---------|----------|----------|
| `report-bug-detail.md` | Bug详细报告模板 | 详细记录发现的问题和解决方案 |
| `debug-round-record.md` | 调试记录模板 | 每轮调试的完整过程记录 |
| `report-debug-summary.md` | 调试总结报告模板 | 调试任务完成后的总结文档 |

#### 管理模板 (Management Templates)

| 模板文件 | 作用描述 | 使用场景 |
|---------|----------|----------|
| `mgmt-bug-list.md` | Bug清单管理模板 | 管理项目中的所有Bug记录 |
| `mgmt-task-index.md` | 任务索引模板 | 记录调试任务的完整历程 |
| `mgmt-debug-index.md` | 调试索引模板 | 创建调试文档的导航索引 |

#### 分析和文档模板 (Analysis & Documentation Templates)

| 模板文件 | 作用描述 | 使用场景 |
|---------|----------|----------|
| `report-lessons-learned.md` | 经验总结模板 | 记录调试过程中的经验教训 |
| `report-final-analysis.md` | 最终分析报告模板 | 调试完成后的深度分析总结 |
| `debug-environment-setup.md` | 环境配置模板 | 记录调试环境的配置和准备工作 |

#### 模板使用说明

1. **自动创建**: 工作流会在步骤5中自动使用相应模板创建文档
2. **文件命名**: 模板复制后应使用具体的任务名称重命名
3. **内容填充**: 按照模板结构填充具体的调试信息
4. **保持一致**: 使用统一模板确保文档结构和质量一致性
5. **适当调整**: 根据具体调试任务对模板进行必要调整

#### 模板选择指南

**新建调试任务时**:

- 使用 `debug_workflow_template.md` 创建任务专用工作流文档
- 系统自动使用 `debug-round-record.md` 创建轮次记录

**Bug管理时**:

- 使用 `report-bug-detail.md` 创建详细的Bug说明文档
- 使用 `mgmt-bug-list.md` 管理Bug的整体状态

**任务完成时**:

- 使用 `report-debug-summary.md` 创建调试总结报告
- 使用 `report-lessons-learned.md` 记录经验教训
- 使用 `report-final-analysis.md` 进行深度分析总结

---

**开始调试**: 遵循7步标准流程，从用户问题描述开始您的系统化调试之旅。

**获取支持**: 查看 `templates/` 目录获取标准模板，参考 `docs/` 了解符号使用规范。

**版本信息**: 调试工作流模板 v2.3.4 | 更新历史详见 `docs/update_log.md`
