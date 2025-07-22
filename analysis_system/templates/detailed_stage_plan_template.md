# 🚀 渐进重构 - 第x阶段详细计划

> **计划制定时间**: {{PLAN_DATE}}
> **基于成果**: {{PREVIOUS_STAGE_ACHIEVEMENTS}}
> **实施目标**: {{STAGE_OBJECTIVES}}

## 📋 第}阶段总体目标

### 🎯 核心目标

**主要目标**:

- {{MAIN_OBJECTIVE_1}}
- {{MAIN_OBJECTIVE_2}}
- {{MAIN_OBJECTIVE_3}}
- {{MAIN_OBJECTIVE_4}}

**成功标准**:

- ✅ {{SUCCESS_CRITERIA_1}}
- ✅ {{SUCCESS_CRITERIA_2}}
- ✅ {{SUCCESS_CRITERIA_3}}
- ✅ {{SUCCESS_CRITERIA_4}}
- ✅ {{SUCCESS_CRITERIA_5}}
- ✅ {{SUCCESS_CRITERIA_6}}

## 🏗️ 第}阶段架构设计

### 📁 目标模块结构

```
{{TARGET_MODULE_STRUCTURE}}
```

### 🔄 数据流设计

```
{{DATA_FLOW_DESIGN}}
```

## 📅 实施计划详细分解

### 🔥 任务}.1：}

**目标**: {{TASK_1_OBJECTIVE}}

**预计时间**: {{TASK_1_DURATION}}
**风险等级**: {{TASK_1_RISK_LEVEL}}
**预期收益**: {{TASK_1_BENEFITS}}

#### }

**{{TASK_1_SOURCE_DESCRIPTION}}**:

{{TASK_1_SOURCE_LIST}}

#### 新增函数清单

| 类别                    | 函数名 | 功能描述 | 来源说明 | 预计代码行数 | 优先级 | 实施状态 |
| ----------------------- | ------ | -------- | -------- | ------------ | ------ | -------- |
| {{FUNCTION_TABLE_ROWS}} |        |          |          |              |        |          |

**优先级说明**:

- **P0 (核心功能)**: 必须实现，直接影响{{MODULE_NAME}}核心流程，来自原有代码迁移
- **P1 (重要功能)**: 应该实现，提升系统稳定性和可维护性
- **P2 (扩展功能)**: 可以延后，主要用于用户体验和系统完善

**函数依赖关系**:

{{FUNCTION_DEPENDENCIES}}

**总计**: {{TOTAL_FUNCTIONS}}个新增函数，预计新增代码约 **{{NEW_CODE_LINES}}行**，从{{SOURCE_FILE}}移除约 **{{REMOVED_CODE_LINES}}行**

#### 设计方案

**{{DESIGN_APPROACH_TITLE}}**:

```python
{{DESIGN_CODE_EXAMPLE}}
```

#### 实施步骤

**📋 前置步骤：代码备份**

在开始任何代码修改之前，必须执行完整的代码备份：

```powershell
# 创建备份目录（格式：backup_阶段名_日期）
$backupDir = "backups/backup_stage{{STAGE_NUMBER}}_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
mkdir $backupDir -Force

# 备份需要修改的源文件
{{BACKUP_FILE_LIST}}

# 创建备份记录文件
@{
    "backup_time" = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "stage" = "{{STAGE_NUMBER}}"
    "purpose" = "{{STAGE_OBJECTIVES}}"
    "files" = @({{BACKUP_FILES_ARRAY}})
    "git_commit" = (git rev-parse HEAD)
} | ConvertTo-Json | Out-File "$backupDir/backup_metadata.json" -Encoding UTF8

Write-Host "✅ 代码备份完成: $backupDir" -ForegroundColor Green
```

**🔒 备份验证**:

- [ ] 确认所有目标文件已成功备份
- [ ] 验证备份文件完整性（文件大小和修改时间）
- [ ] 记录当前Git提交哈希值
- [ ] 确认备份元数据文件已生成

**⚠️ 重要提醒**: 如果备份失败，不得开始任何代码修改工作

---

**📅 阶段实施步骤**：

{{IMPLEMENTATION_STEPS}}

{{ADDITIONAL_TASKS}}

## 📊 第}阶段成功标准

### 功能验证标准

**{{MAIN_MODULE_CATEGORY}}**:

{{FUNCTION_VALIDATION_CRITERIA}}

### 性能标准

{{PERFORMANCE_STANDARDS}}

### 代码质量标准

{{CODE_QUALITY_STANDARDS}}

## 🚨 风险管理和应对

### 主要风险识别

**技术风险**:

{{TECHNICAL_RISKS}}

### 应对策略

**开发策略**:

{{DEVELOPMENT_STRATEGY}}

**测试策略**:

{{TESTING_STRATEGY}}

**回滚预案**:

{{ROLLBACK_PLAN}}

## 📈 预期收益评估

### 代码架构收益

**量化指标**:

{{QUANTITATIVE_METRICS}}

**质量指标**:

{{QUALITY_METRICS}}

### 开发效率收益

**维护效率**:

{{MAINTENANCE_EFFICIENCY}}

**扩展性收益**:

{{EXTENSIBILITY_BENEFITS}}

---

**第{{STAGE_NUMBER}}阶段详细计划制定完成，需要通过完整测试验证后方可进入下一阶段。**

**预计总工期**: {{STAGE_DURATION}}
**预计完成时间**: {{STAGE_COMPLETION_DATE}}
**下一阶段**: 第{{NEXT_STAGE}}阶段 - {{NEXT_STAGE_FOCUS}}
