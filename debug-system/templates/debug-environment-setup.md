# 🛠️ 调试环境初始化模板

> **任务**: {任务名称}  
> **初始化日期**: {yyyy-MM-dd}  
> **操作人员**: {姓名}

## 📋 环境配置检查清单

### 系统环境验证

#### 基础工具检查

- [ ] **PowerShell版本验证**
  ```powershell
  $PSVersionTable.PSVersion
  # 要求: PowerShell 5.1+
  ```

- [ ] **Git环境检查**
  ```powershell
  git --version
  git config --global user.name
  git config --global user.email
  ```

- [ ] **VS Code环境**
  ```powershell
  code --version
  # 检查必要扩展是否安装
  ```

#### 项目特定工具

- [ ] **Python环境** (如适用)
  ```powershell
  python --version
  pip --version
  ```

- [ ] **Node.js环境** (如适用)
  ```powershell
  node --version
  npm --version
  ```

- [ ] **其他特定工具**
  ```powershell
  # 根据项目需求添加
  {工具名} --version
  ```

### 调试工作空间初始化

#### 目录结构创建

```powershell
# 验证当前位置
Get-Location

# 创建调试工作空间
cd debug-system
mkdir debug -ErrorAction SilentlyContinue

# 初始化Bug管理系统
mkdir buglist -ErrorAction SilentlyContinue
Copy-Item "templates\mgmt-bug-list.md" "buglist\bug_list.md" -ErrorAction SilentlyContinue

# 验证模板文件
Get-ChildItem templates\*.md | Select-Object Name

# 检查目录结构
tree /F
```

#### 任务专用环境

```powershell
# 进入debug目录
cd debug

# 确定任务编号
$taskId = (Get-ChildItem -Directory -Name | Where-Object { $_ -match '^\d+_' } | Measure-Object).Count + 1
Write-Host "下一个任务编号: $taskId"

# 创建任务文件夹 (待填充具体任务名)
$taskFolder = "${taskId}_{任务描述}"
mkdir $taskFolder
cd $taskFolder

# 复制索引模板
Copy-Item "..\..\templates\mgmt-task-index.md" "INDEX.md"

# 创建第一轮调试环境
$directories = @("src", "core", "archive", "deprecated", "docs", "logs", "files")
mkdir "1"
foreach ($dir in $directories) {
    mkdir "1\$dir"
}

# 复制轮次记录模板
Copy-Item "..\..\templates\debug-round-record.md" "1\README.md"

# 创建备份来源说明文件
$backupContent = @"
# 备份文件来源说明

本文件记录archive目录下各备份文件的来源和备份时间。

## 备份记录

"@
$backupContent | Out-File "1\archive\backup_sources.md" -Encoding UTF8
```

### 权限和访问验证

#### 文件系统权限

- [ ] **读取权限**: 确认对项目文件有读取权限
- [ ] **写入权限**: 确认对工作目录有写入权限
- [ ] **执行权限**: 确认可以执行必要的脚本和工具

#### 网络访问

- [ ] **互联网连接**: 验证网络连接正常
- [ ] **代理设置**: 确认代理配置正确 (如适用)
- [ ] **防火墙**: 确认防火墙不会阻止必要的网络请求

### 项目特定配置

#### 依赖项检查

```powershell
# Python项目依赖 (如适用)
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

# Node.js项目依赖 (如适用)
if (Test-Path "package.json") {
    npm install
}

# 其他项目特定依赖
{项目特定的依赖安装命令}
```

#### 配置文件验证

- [ ] **环境变量**: 检查必要的环境变量设置
- [ ] **配置文件**: 验证配置文件存在且格式正确
- [ ] **密钥文件**: 确认访问密钥和证书配置正确 (如适用)

### 调试工具配置

#### 日志配置

```powershell
# 配置日志输出目录
$logDir = "1\logs"
if (-not (Test-Path $logDir)) {
    mkdir $logDir
}

# 设置日志级别和格式 (根据项目需求)
{日志配置命令}
```

#### 监控工具

- [ ] **系统监控**: 配置系统资源监控
- [ ] **应用监控**: 配置应用性能监控 (如适用)
- [ ] **网络监控**: 配置网络请求监控 (如适用)

## 📝 初始化验证

### 功能验证测试

```powershell
# 基础功能验证
{基础功能测试命令}

# 关键组件验证
{关键组件测试命令}

# 端到端验证
{完整流程测试命令}
```

### 验证检查清单

- [ ] **环境变量正确设置**
- [ ] **必要工具已安装并可用**
- [ ] **项目依赖已正确安装**
- [ ] **配置文件格式正确**
- [ ] **权限设置适当**
- [ ] **网络连接正常**
- [ ] **日志系统工作正常**
- [ ] **基础功能验证通过**

## 🚨 常见问题和解决方案

### PowerShell执行策略

```powershell
# 如果遇到执行策略限制
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 路径问题

```powershell
# 处理路径中的中文字符
[System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::Default.GetBytes($pwd.Path))

# 使用绝对路径避免相对路径问题
$workspaceRoot = (Get-Location).Path
```

### 依赖安装失败

```powershell
# Python依赖安装问题
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Node.js依赖安装问题
npm cache clean --force
npm install
```

## 📋 完成确认

### 初始化完成标志

- [ ] **工作空间目录结构完整**
- [ ] **模板文件已正确复制**
- [ ] **环境变量已设置**
- [ ] **必要工具已验证可用**
- [ ] **项目特定配置已完成**
- [ ] **基础功能验证通过**

### 后续步骤

1. **开始调试循环**: 进入6步调试循环
2. **文档更新**: 在任务专用文档中记录初始化结果
3. **备份确认**: 确认重要文件备份策略已设置

---

**初始化完成时间**: {yyyy-MM-dd HH:mm:ss}  
**环境配置版本**: v1.0  
**验证状态**: {✅ 完成 / ❌ 需要修复}
