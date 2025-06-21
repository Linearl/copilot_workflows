# 调试工作流程模板

完整的调试工作流模板包，用于系统化问题解决和代码调试。

## 📋 目录

- [功能特点](#-功能特点) 
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [使用方法](#-使用方法)
- [模板资源](#-模板资源)
- [文档说明](#-文档说明)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

## ✨ 功能特点

- **系统化调试流程**: 6步调试循环，确保问题解决的一致性
- **模板集合**: 预构建的文档和工作流管理模板
- **符号参考**: 全面的项目组织符号指南
- **人机协作**: 针对AI辅助调试优化的工作流
- **模块化结构**: 有序的文件系统，提高调试会话效率

## 📁 项目结构

```
debug-system/
├── workflow_template_v2.md          # V2核心工作流模板
├── templates/                       # 模板集合
│   ├── README-template.md           # 调试会话文档模板
│   ├── summary-template.md          # 项目总结模板
│   ├── experience-template.md       # 经验总结模板
│   ├── INDEX-template.md            # 调试索引模板
│   └── SUMMARY-TEMPLATE-UPDATE.md   # 更新版总结模板
└── docs/
    └── 常用符号.md                   # 符号参考指南
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Linearl/copilot_debug_workflow.git
cd copilot_debug_workflow
```

### 2. 创建新的调试会话

```powershell
# 为特定任务复制工作流模板
Copy-Item "debug-system\workflow_template_v2.md" "debug-system\workflow_[任务名称]_v2.md"

# 初始化调试环境
mkdir debug; cd debug; $round = 1
mkdir $round\{src,core,archive,deprecated,docs,logs,files}
Copy-Item "..\debug-system\templates\README-template.md" "$round\README.md"
```

## 🔄 使用方法

### 工作流文档使用方法

此包的核心功能是**工作流模板文档** (`workflow_template_v2.md`)。以下是有效使用方法：

#### 步骤1：将项目复制到你的工作空间

```bash
# 克隆或复制项目到本地工作空间
git clone https://github.com/Linearl/copilot_debug_workflow.git
# 或将debug-system文件夹复制到现有项目中
```

#### 步骤2：在VS Code中打开工作流文档

```powershell
# 在VS Code中打开工作流模板
code debug-system/workflow_template_v2.md
```

#### 步骤3：启用Copilot Agent模式

1. **启用Agent模式**: 在VS Code中使用`@workspace`或agent命令
2. **开始调试会话**: 按照工作流文档中的指引进行

#### 步骤4：描述问题并开始调试

只需用自然语言描述你的问题 - 工作流会自动处理解析和格式化：

1. **问题描述**: 自然地描述你的问题，agent会自动解析
2. **AI分析**: 让agent解析并理解你的问题
3. **用户确认**: 检查并确认agent的理解
4. **文档创建**: Agent创建任务专用工作流文档
5. **环境设置**: 初始化有组织的调试工作空间
6. **调试迭代**: 执行结构化调试循环
7. **文档记录**: 记录结果并整理文件

### 🤖 Agent配置建议

#### 模型和设置

- **推荐模型**: 使用Claude 4.0以获得最佳效果
- **启用思考模式**: 开启agent思考模式以获得更好的分析
- **终端访问权限**: 配置并启用终端使用权限

#### 预算和控制

- **请求预算**: 将每次会话的agent调用预算设置为10-20次
- **预算警告**: 过多的请求可能导致agent偏离主题
- **主动监控**: 监控agent进度，必要时进行干预

#### 最佳实践

⚠️ **重要提示**: 如果发现agent跑偏或有新的思路，请**立即暂停**并补充新指令。

- **保持参与**: 积极审查agent的分析和建议
- **提供反馈**: 就agent的方向给出明确反馈
- **纠正方向**: 当agent偏离轨道时不要犹豫进行重定向

### 文件组织系统

| 符号 | 目录 | 文件类型 | 存储规则 |
|------|------|----------|----------|
| 🔴 | core/ | 核心解决方案 | 5-10个关键文件 |
| 📚 | archive/ | 重要里程碑 | 重要调试历程 |
| 🗑️ | deprecated/ | 废弃/替换 | 无效或被替代文件 |
| 📝 | docs/ | 分析文档 | 分析和说明文档 |
| 📋 | logs/ | 测试日志 | 测试和运行日志 |
| 🗂️ | files/ | 其他文件 | 辅助和支持文件 |
| 🐍 | src/ | 工作目录 | 调试过程中的代码和脚本 |

## 📚 模板资源

`debug-system/templates/` 目录包含：

- **README-template.md**: 调试会话文档的标准模板
- **summary-template.md**: 项目总结模板，用于全面报告
- **experience-template.md**: 经验总结模板，用于记录经验教训
- **INDEX-template.md**: 调试索引模板，用于会话组织
- **SUMMARY-TEMPLATE-UPDATE.md**: 总结模板的更新版本

## 📖 文档说明

### 符号参考

详细的符号参考请查看 `debug-system/docs/常用符号.md`，包含：

- 🎯 核心符号表：通用符号和主要功能域常用符号
- 📊 完整符号表：项目中所有符号的全面索引
- 🎨 使用指南：优秀案例和使用规范
- 📋 工作流模板符号使用指南
- 📑 符号速查表

## 🤝 贡献指南

我们欢迎贡献！请随时提交问题和拉取请求。

1. 分叉仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开拉取请求

## 📄 许可证

此项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

---

**创建时间**: 2025年6月21日  
**版本**: v2.0  
**适用场景**: 技术项目调试、问题排查、系统优化
