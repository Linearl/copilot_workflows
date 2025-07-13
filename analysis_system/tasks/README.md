# 分析轮次归档目录

本目录用于存储和管理每轮分析的完整记录和归档文件。

## 📁 目录结构

```text
tasks/
├── INDEX.md                     # 分析轮次索引和进展记录
├── workflow_archive/            # 已完成任务的工作流文档存档
└── {轮次号}/                   # 具体分析轮次目录
    ├── round_{轮次号}_summary.md # 轮次总结记录
    ├── core_analysis/           # 核心分析报告和解决方案
    ├── supporting_docs/         # 辅助文档、数据文件、参考资料
    ├── deprecated/              # 过时或无效的分析文件
    ├── reports/                 # 各类分析报告
    ├── metrics/                 # 代码指标和量化数据
    ├── analysis/                # 详细分析过程和结果
    ├── backup/                  # 重要文件备份
    ├── docs/                    # 技术文档和说明
    ├── logs/                    # 分析日志和执行记录
    └── files/                   # 其他相关文件
```

## � 使用说明

### 新建分析轮次

当开始新的分析轮次时，AI会自动创建标准化的目录结构：

```powershell
$round = 1
mkdir $round\{core_analysis,supporting_docs,deprecated,reports,metrics,analysis,backup,docs,logs,files}
Copy-Item "templates\round-analysis-template.md" "$round\round_${round}_summary.md"
```

### 归档规则

#### Core Analysis (核心分析目录)

存放最重要的分析成果：

- 主要分析报告 (analysis_report_roundX.md)
- 关键发现总结 (key_findings.md)
- 问题识别清单 (issues_identified.md)
- 解决方案建议 (solution_recommendations.md)
- 重要的数据分析结果

#### Supporting Docs (辅助文档目录)

存放支撑性文档：

- 代码审查报告
- 性能分析数据
- 重构计划文档
- 参考资料和外部文档
- 中间分析文件

#### Deprecated (废弃文件目录)

存放不再使用的文件：

- 被替代的分析版本
- 无效的假设或结论
- 错误的分析方向
- 临时工作文件

### 进展记录

每轮分析完成后，必须更新以下文件：

1. **INDEX.md**: 添加本轮分析记录，更新统计信息
2. **round_{轮次号}_summary.md**: 填写详细的轮次总结
3. **workflow_archive/**: 归档对应的工作流文档

### 质量管理

- 定期检查归档文件的完整性
- 确保核心分析文件的质量和可读性
- 及时清理deprecated目录中的过期文件
- 维护INDEX.md的准确性和时效性

## 📋 归档检查清单

分析轮次完成时的必检项目：

- [ ] core_analysis目录包含完整的核心分析文件
- [ ] round_summary.md已完整填写
- [ ] INDEX.md已更新本轮记录
- [ ] 工作流文档已复制并归档
- [ ] 重要文件已适当备份
- [ ] deprecated文件已正确分类
- [ ] 目录结构符合标准规范

## 🔍 快速查找

- **最新分析**: 查看编号最大的轮次目录
- **核心成果**: 各轮次的core_analysis目录
- **完整进展**: INDEX.md文件
- **工作流历史**: workflow_archive目录

---

**目录更新时间**: 2025年7月11日  
**维护说明**: 本目录已从reports/重命名为tasks/，以更好地反映分析轮次管理功能
