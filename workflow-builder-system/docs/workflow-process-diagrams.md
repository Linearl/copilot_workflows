# 🏗️ 工作流构建器 - 流程可视化图表

> **文档状态**: 独立附录文件 - workflow-builder-system流程图表  
> **最后更新**: 2025年8月18日  
> **图表类型**: Mermaid流程图，支持VS Code实时预览  
> **用途**: 将IPD 6步骤工作流程可视化，提供图表化的流程指南

---

## 📑 目录

- [🎯 总体流程概览](#🎯-总体流程概览)
- [📍 准备阶段流程图](#📍-准备阶段流程图)
- [📐 设计阶段流程图](#📐-设计阶段流程图)  
- [⚙️ 执行阶段流程图](#⚙️-执行阶段流程图)
- [🔍 验证阶段流程图](#🔍-验证阶段流程图)
- [🔄 多层循环控制图](#🔄-多层循环控制图)
- [🚪 阶段门控制图](#🚪-阶段门控制图)

---

## 🎯 总体流程概览

### 📊 IPD 6步骤工作流总览

```mermaid
graph TB
    subgraph "📍 准备阶段 (Preparation)"
        A1[步骤1: 需求概念化<br/>Concept]
        A2[步骤2: 需求分析<br/>Analysis]
    end
    
    subgraph "📐 设计阶段 (Design)"
        B1[步骤3: 概念设计<br/>Conceptual Design]
        B2[步骤4: 详细设计<br/>Detailed Design]
    end
    
    subgraph "⚙️ 执行阶段 (Execution)"
        C1[步骤5: 开发构建<br/>Development]
    end
    
    subgraph "🔍 验证阶段 (Verification)"
        D1[步骤6: 质量检查<br/>Quality Assurance]
    end
    
    START([🚀 用户启动]) --> A1
    A1 --> Gate1{🚪 阶段门1<br/>概念审批}
    Gate1 --> A2
    A2 --> Gate2{🚪 阶段门2<br/>分析确认}
    Gate2 --> B1
    B1 --> Gate3{🚪 阶段门3<br/>概念设计审批}
    Gate3 --> B2
    B2 --> Gate4{🚪 阶段门4<br/>详细设计确认}
    Gate4 --> C1
    C1 --> Gate5{🚪 阶段门5<br/>开发质量门}
    Gate5 --> D1
    D1 --> Gate6{🚪 阶段门6<br/>质量确认门}
    Gate6 --> END([✅ 工作流完成])
    
    classDef phase fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef step fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef gate fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef start fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    
    class A1,A2,B1,B2,C1,D1 step
    class Gate1,Gate2,Gate3,Gate4,Gate5,Gate6 gate
    class START,END start
```

---

## 📍 准备阶段流程图

### 📊 步骤1: 需求概念化流程

```mermaid
graph LR
    A[📥 用户输入<br/>业务需求] --> B[🔍 业务概念定义<br/>痛点识别+价值主张]
    B --> C[📏 需求范围边界<br/>功能边界+技术约束]
    C --> D[📋 生成概念化报告<br/>templates/step1_*]
    D --> E[🤝 用户确认检查点<br/>⚠️ 必须暂停]
    E --> F{📊 业务概念<br/>是否明确?}
    F -->|否，需调整| B
    F -->|是| G[🚪 阶段门1: 概念审批<br/>✅ 通过进入下一步]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef gate fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class A input
    class B,C,D process
    class E output
    class F decision
    class G gate
```

### 📊 步骤2: 需求分析流程

```mermaid
graph LR
    A[📊 概念化结果输入] --> B[🔍 需求深度分析<br/>复杂度+风险+依赖]
    B --> C[🌐 解决方案空间探索<br/>技术调研+最佳实践]
    C --> D[💡 可行性研究<br/>技术+经济可行性]
    D --> E[📋 生成分析报告<br/>templates/step2_*]
    E --> F[🤝 用户确认检查点<br/>⚠️ 必须暂停]
    F --> G{📊 分析结果<br/>是否满意?}
    G -->|否，需深入| B
    G -->|是| H[🚪 阶段门2: 分析确认<br/>✅ 进入设计阶段]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef gate fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class A input
    class B,C,D,E process
    class F output
    class G decision
    class H gate
```

---

## 📐 设计阶段流程图

### 📊 步骤3: 概念设计流程

```mermaid
graph TB
    A[📊 分析结果输入] --> B[🏗️ 解决方案概念设计<br/>架构理念+核心模式]
    B --> C[⚖️ 方案组合生成]
    
    subgraph "方案选择"
        C1[💡 轻量级方案<br/>10-15分钟]
        C2[⚡ 标准方案<br/>30-60分钟]  
        C3[🏆 专业方案<br/>1-3小时]
    end
    
    C --> C1
    C --> C2
    C --> C3
    
    C1 --> D[📋 生成概念设计文档<br/>templates/step3_*]
    C2 --> D
    C3 --> D
    
    D --> E[🤝 用户方案选择<br/>⚠️ 必须暂停]
    E --> F{🎯 方案是否<br/>符合预期?}
    F -->|否，重新设计| B
    F -->|是| G[🚪 阶段门3: 概念设计审批<br/>✅ 进入详细设计]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef option fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef gate fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class A input
    class B,D process
    class C1,C2,C3 option
    class E output
    class F decision
    class G gate
```

### 📊 步骤4: 详细设计流程

```mermaid
graph LR
    A[🎯 选定概念方案] --> B[🏗️ 系统架构设计<br/>整体架构+组件关系]
    B --> C[📋 工作流步骤规范<br/>功能定义+模板需求]
    C --> D[📁 文件结构规范<br/>目录设计+命名规范]
    D --> E[⚙️ 技术实现规范<br/>开发标准+技术栈]
    E --> F[📋 生成详细设计文档<br/>templates/step4_*]
    F --> G[🤝 用户确认检查点<br/>⚠️ 必须暂停]
    G --> H{🔧 设计规范<br/>是否完整?}
    H -->|否，需完善| B
    H -->|是| I[🚪 阶段门4: 详细设计确认<br/>✅ 进入开发阶段]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef gate fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class A input
    class B,C,D,E,F process
    class G output
    class H decision
    class I gate
```

---

## ⚙️ 执行阶段流程图

### 📊 步骤5: 开发构建总体流程

```mermaid
graph TB
    A[📋 详细设计输入] --> B[🏗️ 环境初始化<br/>创建项目结构]
    B --> C[🔄 第一层循环: L1<br/>步骤级开发循环]
    
    subgraph "L1 循环控制"
        D[🎯 L1.1 步骤选择<br/>P0→P1→P2→P3]
        E[🔄 L1.2 进入L2循环<br/>单步骤开发]
        F[✅ L1.3 完成性检查<br/>是否还有剩余步骤]
    end
    
    C --> D
    D --> E
    E --> L2[📊 第二层循环详情<br/>见下图]
    L2 --> F
    F -->|有剩余| D
    F -->|全部完成| G[🚪 阶段门5: 开发质量门<br/>✅ 进入验证阶段]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef loop fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef gate fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class A input
    class B process
    class D,E,F,L2 loop
    class G gate
```

### 📊 步骤5: L2循环详细流程

```mermaid
graph TB
    A[🎯 当前步骤输入] --> B[📊 L2.1 格式化拆分<br/>提取步骤信息]
    B --> C[📝 L2.2 内容描述<br/>添加到工作流模板]
    C --> D[📋 L2.3 编写模板文件<br/>创建templates/*]
    D --> E[⚙️ L2.4 编写脚本文件<br/>创建scripts/*]
    E --> F[🔍 L2.5 质量校验<br/>乱码+错排+一致性]
    F --> G[🔧 L2.6 修复质量问题<br/>自动修复+质量确认]
    G --> H[🤝 L2.7 用户确认检查点<br/>⚠️ 必须暂停]
    H --> I{✅ 步骤开发<br/>是否满意?}
    I -->|否，需修改| J[📝 确定修改内容]
    J --> C
    I -->|是| K[📋 L2.8 经验教训总结<br/>templates/step5_summary]
    K --> L[📊 L2.9 全局任务管理<br/>更新进度跟踪]
    L --> M[✅ L2循环完成<br/>返回L1循环]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef process fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef quality fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef user fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef decision fill:#ffccbc,stroke:#e64a19,stroke-width:2px
    classDef output fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    
    class A input
    class B,C,D,E process
    class F,G quality
    class H user
    class I decision
    class J,K,L,M output
```

---

## 🔍 验证阶段流程图

### 📊 步骤6: 质量检查流程

```mermaid
graph LR
    A[⚙️ 开发成果输入] --> B[🔍 内容真实性检查<br/>虚构内容+引用验证]
    B --> C[📋 描述一致性检查<br/>术语+风格+逻辑]
    C --> D[📄 模板完整性检查<br/>语法+结构+编码]
    D --> E[⚙️ 基本功能验证<br/>模板可用性+脚本执行]
    E --> F[📋 生成质量检查报告<br/>templates/step6_*]
    F --> G[🤝 用户确认检查点<br/>⚠️ 必须暂停]
    G --> H{✅ 质量检查<br/>是否通过?}
    H -->|否，需修复| I[🔧 质量问题修复]
    I --> B
    H -->|是| J[🚪 阶段门6: 质量确认门<br/>✅ 工作流完成]
    
    classDef input fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef check fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef output fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef user fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef decision fill:#ffccbc,stroke:#e64a19,stroke-width:2px
    classDef fix fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef gate fill:#ffebee,stroke:#c62828,stroke-width:2px
    
    class A input
    class B,C,D,E,F check
    class G output
    class H decision
    class I fix
    class J gate
```

---

## 🔄 多层循环控制图

### 📊 L1-L2 双层循环架构

```mermaid
graph TB
    subgraph "🔄 L1 - 阶段层循环控制"
        L1_1[📍 准备阶段<br/>Preparation]
        L1_2[📐 设计阶段<br/>Design]
        L1_3[⚙️ 执行阶段<br/>Execution]
        L1_4[🔍 验证阶段<br/>Verification]
    end
    
    subgraph "🔄 L2 - 步骤层循环控制"
        L2_1[🎯 步骤执行<br/>Step Execution]
        L2_2[🔍 中间检查<br/>Intermediate Check]
        L2_3[🤝 用户确认<br/>User Confirmation]
        L2_4[⚖️ 继续/重做决策<br/>Continue/Redo Decision]
    end
    
    START([🚀 循环开始]) --> L1_1
    L1_1 --> L1_2
    L1_2 --> L1_3
    L1_3 --> L1_4
    L1_4 --> Gate{🚪 阶段门检查}
    
    Gate -->|❌ 返回| L1_1
    Gate -->|✅ 通过| END([✅ 循环完成])
    Gate -->|🔄 循环优化| L1_2
    
    L1_1 -.-> L2_1
    L1_2 -.-> L2_1
    L1_3 -.-> L2_1
    L1_4 -.-> L2_1
    
    L2_1 --> L2_2
    L2_2 --> L2_3
    L2_3 --> L2_4
    L2_4 -->|🔄 重做| L2_1
    L2_4 -->|✅ 继续| L2_END([步骤完成])
    L2_4 -->|⏸️ 暂停| L2_PAUSE([等待输入])
    
    classDef l1 fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    classDef l2 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef decision fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef endpoint fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    
    class L1_1,L1_2,L1_3,L1_4 l1
    class L2_1,L2_2,L2_3,L2_4 l2
    class Gate decision
    class START,END,L2_END,L2_PAUSE endpoint
```

---

## 🚪 阶段门控制图

### 📊 IPD 6个阶段门控制流程

```mermaid
graph TB
    subgraph "🚪 阶段门控制系统"
        Gate1[🚪 阶段门1<br/>概念审批<br/>✅ 业务价值确认]
        Gate2[🚪 阶段门2<br/>分析确认<br/>✅ 需求理解一致性]
        Gate3[🚪 阶段门3<br/>概念设计审批<br/>✅ 设计理念认可]
        Gate4[🚪 阶段门4<br/>详细设计确认<br/>✅ 架构设计完整性]
        Gate5[🚪 阶段门5<br/>开发质量门<br/>✅ 开发成果验证]
        Gate6[🚪 阶段门6<br/>质量确认门<br/>✅ 最终质量检查]
    end
    
    Flow1[步骤1: 需求概念化] --> Gate1
    Gate1 -->|✅ 通过| Flow2[步骤2: 需求分析]
    Gate1 -->|❌ 返回| Flow1
    
    Flow2 --> Gate2
    Gate2 -->|✅ 通过| Flow3[步骤3: 概念设计]
    Gate2 -->|❌ 返回| Flow2
    
    Flow3 --> Gate3
    Gate3 -->|✅ 通过| Flow4[步骤4: 详细设计]
    Gate3 -->|❌ 返回| Flow3
    
    Flow4 --> Gate4
    Gate4 -->|✅ 通过| Flow5[步骤5: 开发构建]
    Gate4 -->|❌ 返回| Flow4
    
    Flow5 --> Gate5
    Gate5 -->|✅ 通过| Flow6[步骤6: 质量检查]
    Gate5 -->|❌ 返回| Flow5
    
    Flow6 --> Gate6
    Gate6 -->|✅ 通过| SUCCESS[🎉 工作流成功完成]
    Gate6 -->|❌ 返回| Flow6
    
    classDef step fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef gate fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    classDef success fill:#e8f5e8,stroke:#388e3c,stroke-width:3px
    
    class Flow1,Flow2,Flow3,Flow4,Flow5,Flow6 step
    class Gate1,Gate2,Gate3,Gate4,Gate5,Gate6 gate
    class SUCCESS success
```

---

## 📚 使用说明

### 🎯 图表使用指导

1. **总体流程概览**: 用于快速理解整个workflow-builder-system的6个步骤结构
2. **阶段详细图表**: 用于深入了解每个步骤的具体执行流程
3. **循环控制图**: 用于理解复杂的多层循环控制机制
4. **阶段门控制**: 用于掌握IPD方法论的质量控制要点

### 🔧 VS Code预览

- 安装 `Mermaid Preview` 插件
- 使用 `Ctrl+Shift+P` → `Mermaid: Preview`
- 实时查看图表渲染效果

### 📋 图表更新

- 图表与 `workflow_builder_template.md` 保持同步
- 工作流程变更时需同步更新图表
- 建议定期检查图表的准确性

---

**文档信息**:
- **创建日期**: 2025年8月18日
- **图表版本**: v1.0.0  
- **对应工作流版本**: v2.0.0
- **图表总数**: 10个主要流程图
- **支持工具**: Mermaid.js + VS Code预览
