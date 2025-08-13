# Git Worktree 工作区配置模板

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

## 🛠️ 工作区设置

### 创建命令记录
```powershell
# 工作区创建命令
cd [项目根目录]
git worktree add [工作区路径] [版本标签]

# 验证工作区
git worktree list
cd [工作区路径]
git log --oneline -5
```

### 预期输出
```
# git worktree list 输出示例
[主工作区路径]                    [当前分支]  [主分支]
[worktree工作区路径]             [版本哈希]  [detached HEAD]

# git log 输出示例
[提交哈希] (HEAD, tag: [版本标签]) [提交信息]
...
```

---

## 🔍 工作区验证

### 基本验证清单
- [ ] 工作区已成功创建
- [ ] 版本标签正确
- [ ] 文件结构完整
- [ ] Git状态正常

### 路径验证
```powershell
# 验证关键文件存在
Test-Path "[工作区路径]\anc_host.py"
Test-Path "[工作区路径]\algorithm"
Test-Path "[工作区路径]\logic"
Test-Path "[工作区路径]\tools"
```

### 版本确认
```powershell
# 在工作区中确认版本信息
cd [工作区路径]
git describe --tags
git log --oneline -1
```

---

## 📁 目录结构对比

### 主要模块确认
- [ ] `algorithm/` - 核心算法模块存在
- [ ] `logic/` - 业务逻辑模块存在  
- [ ] `tools/` - 工具支撑模块存在
- [ ] `ui/` - 界面模块存在
- [ ] `file/` - 配置文件目录存在

### 配置文件确认
- [ ] `file/config.yaml` - 主配置文件
- [ ] `file/config/` - 配置目录
- [ ] `requirements.txt` - 依赖文件
- [ ] `pyproject.toml` - 项目配置

---

## 🔄 分析准备

### AI 环境准备
1. **工作区访问确认**
   ```
   工作区位于项目内: [是/否]
   AI可以访问工作区: [是/否]
   相对路径正确: [是/否]
   ```

2. **分析工具准备**
   - [ ] `git diff` 命令可用
   - [ ] `git log` 命令可用
   - [ ] 文件读取功能正常
   - [ ] 代码搜索功能正常

### 分析计划确认
- [ ] 分析模块顺序已确定
- [ ] 分析深度已规划
- [ ] 总结节奏已设定
- [ ] 输出格式已约定

---

## 📝 使用说明

### 分析阶段使用
1. **概览分析阶段**
   - 在工作区中执行 `git log` 和 `git diff --stat`
   - 分析整体变更规模和分布

2. **模块对比阶段**
   - 逐个模块进行 `git diff` 对比
   - 深入分析关键文件变更

3. **文档分析阶段**
   - 检查文档目录变更
   - 快速浏览重要文档修改

### 注意事项
- ⚠️ **不要在工作区中修改文件**
- ⚠️ **不要在工作区中执行构建命令**
- ⚠️ **仅用于只读分析对比**
- ⚠️ **分析完成后及时清理**

---

## 🧹 清理计划

### 清理时机
- [ ] 分析任务完全完成
- [ ] 分析结果已保存
- [ ] 用户确认可以清理
- [ ] 备份已创建(如需要)

### 清理命令
```powershell
# 清理工作区 (需用户确认)
cd [项目根目录]
git worktree remove [工作区路径]

# 验证清理结果
git worktree list
```

### 清理后验证
```powershell
# 确认工作区已删除
Test-Path "[工作区路径]" # 应返回 False

# 确认主工作区正常
git status
git worktree list
```

---

## 📋 故障排除

### 常见问题

#### 工作区创建失败
**问题**: `fatal: '[路径]' already exists`
**解决**: 
```powershell
# 清理已存在的目录
Remove-Item "[工作区路径]" -Recurse -Force
git worktree add [工作区路径] [版本标签]
```

#### 版本标签不存在  
**问题**: `fatal: invalid reference: [版本标签]`
**解决**:
```powershell
# 获取远程标签
git fetch --tags

# 查看可用标签
git tag -l | Sort-Object

# 使用提交哈希代替标签
git worktree add [工作区路径] [提交哈希]
```

#### 工作区路径过长
**问题**: Windows路径长度限制
**解决**:
```powershell
# 使用更短的路径名
git worktree add "analysis/v186" V1.86
```

### 紧急清理
```powershell
# 强制清理(最后手段)
git worktree remove --force [工作区路径]
Remove-Item "[工作区路径]" -Recurse -Force -ErrorAction SilentlyContinue
```

---

## 📚 参考信息

### Git Worktree 命令参考
```powershell
# 创建工作区
git worktree add <路径> <分支/标签/提交>

# 列出工作区
git worktree list

# 删除工作区
git worktree remove <路径>

# 修复工作区(如路径移动)
git worktree repair

# 锁定工作区(防止清理)
git worktree lock <路径>
```

### 最佳实践
1. **路径命名**: 使用描述性名称，如 `worktree_V1.86`
2. **定期清理**: 分析完成后及时清理，避免磁盘空间浪费
3. **只读原则**: 工作区仅用于分析，不做修改
4. **路径长度**: 注意Windows路径长度限制
5. **权限检查**: 确保有足够权限创建和删除目录

---

**配置完成时间**: [完成时间]  
**工作区生命周期**: [预期使用时长]  
**负责人**: GitHub Copilot
