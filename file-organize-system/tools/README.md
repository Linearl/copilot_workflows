# 🛠️ 重复文件检测工具使用指南

> **工具版本**: v1.0  
> **创建时间**: 2025年6月24日  
> **适用场景**: 文件整理工作流中的重复文件处理

---

## 📦 工具清单

### 1. duplicate_detector.py
**功能**: 扫描目录，检测基于文件内容hash的重复文件  
**输出**: JSON格式的详细检测报告

### 2. duplicate_processor.py  
**功能**: 基于检测报告处理重复文件  
**支持策略**: 删除、备份、硬链接

---

## 🚀 快速开始

### 基本用法
```bash
# 1. 检测重复文件
python duplicate_detector.py --directory "C:\待整理的目录" --output "重复文件报告.json"

# 2. 预览处理方案
python duplicate_processor.py --report "重复文件报告.json" --strategy backup

# 3. 执行处理（备份策略）
python duplicate_processor.py --report "重复文件报告.json" --strategy backup --execute
```

---

## 📋 详细使用说明

### duplicate_detector.py 参数说明

| 参数 | 简写 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| --directory | -d | ✅ | 要扫描的目录路径 | `--directory "C:\Users\待整理"` |
| --output | -o | ❌ | 输出报告文件路径 | `--output "report.json"` |
| --quiet | -q | ❌ | 静默模式，只输出摘要 | `--quiet` |

### duplicate_processor.py 参数说明

| 参数 | 简写 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| --report | -r | ✅ | 检测报告文件路径 | `--report "report.json"` |
| --strategy | -s | ❌ | 处理策略 | `--strategy backup` |
| --backup-dir | -b | ❌ | 备份目录路径 | `--backup-dir "备份文件夹"` |
| --execute | 无 | ❌ | 执行处理（默认预览） | `--execute` |
| --generate-script | 无 | ❌ | 生成PowerShell脚本 | `--generate-script` |

---

## 🎯 处理策略说明

### 1. backup (推荐)
- **操作**: 将重复文件移动到备份目录
- **特点**: 最安全，可以恢复
- **适用**: 不确定文件重要性时

```bash
python duplicate_processor.py --report "report.json" --strategy backup --execute
```

### 2. delete
- **操作**: 直接删除重复文件
- **特点**: 节省空间，不可恢复
- **适用**: 确认文件可以删除时

```bash
python duplicate_processor.py --report "report.json" --strategy delete --execute
```

### 3. hardlink
- **操作**: 用硬链接替换重复文件
- **特点**: 节省空间，保持文件可访问
- **适用**: 同一分区内的文件

```bash
python duplicate_processor.py --report "report.json" --strategy hardlink --execute
```

---

## 📊 报告格式说明

### JSON报告结构
```json
{
  "scan_info": {
    "directory": "扫描目录",
    "scan_time": "扫描时间",
    "scan_duration_seconds": 123.45
  },
  "statistics": {
    "total_files": 1000,
    "total_size": 2147483648,
    "duplicate_groups": 5,
    "duplicate_files": 12,
    "space_wasted": 104857600,
    "scan_time": 30.5
  },
  "duplicate_groups": {
    "group_1": {
      "hash": "md5哈希值",
      "file_count": 3,
      "file_size": 1048576,
      "wasted_space_mb": 2.0,
      "files": [...],
      "recommended_action": "处理建议"
    }
  },
  "summary": {
    "has_duplicates": true,
    "total_duplicate_groups": 5,
    "total_duplicate_files": 12,
    "potential_space_saving_mb": 100.0
  }
}
```

---

## 🔧 PowerShell集成

### 在文件整理工作流中使用

```powershell
# 1. 在分析阶段运行重复文件检测
$targetDir = "C:\Users\yinji\OneDrive - zknu.edu.cn\待整理"
$reportFile = "duplicate_report.json"

python "file-organize-system\tools\duplicate_detector.py" --directory $targetDir --output $reportFile

# 2. 检查是否发现重复文件
$report = Get-Content $reportFile | ConvertFrom-Json
if ($report.summary.has_duplicates) {
    Write-Host "发现 $($report.summary.total_duplicate_groups) 组重复文件"
    Write-Host "可节省空间: $($report.summary.potential_space_saving_mb) MB"
    
    # 3. 生成处理脚本
    python "file-organize-system\tools\duplicate_processor.py" --report $reportFile --strategy backup --generate-script
    
    # 4. 预览处理效果
    python "file-organize-system\tools\duplicate_processor.py" --report $reportFile --strategy backup
} else {
    Write-Host "未发现重复文件"
}
```

### 自动化脚本生成

```powershell
# 生成并执行处理脚本
python duplicate_processor.py --report "report.json" --strategy backup --generate-script
.\process_duplicates_backup.ps1
```

---

## ⚠️ 使用注意事项

### 安全建议
1. **备份重要数据**: 在执行任何删除操作前，确保有完整备份
2. **预览模式**: 首次使用建议先用预览模式查看处理效果
3. **分批处理**: 对于大量文件，建议分批处理
4. **权限检查**: 确保对目标文件有完整的读写权限

### 性能考虑
1. **大文件处理**: 大文件的hash计算可能需要较长时间
2. **内存使用**: 大量文件可能占用较多内存
3. **网络驱动器**: OneDrive等网络驱动器可能影响性能

### 限制说明
1. **硬链接限制**: 硬链接仅支持同一分区内的文件
2. **权限问题**: 系统文件或只读文件可能无法处理
3. **文件占用**: 正在使用的文件可能无法移动或删除

---

## 🐛 故障排除

### 常见问题

**Q: 提示"文件不存在"错误**  
A: 检查文件路径是否正确，或文件是否被其他程序占用

**Q: Python脚本无法运行**  
A: 确保已安装Python 3.6+，且PATH环境变量配置正确

**Q: 权限不足错误**  
A: 以管理员身份运行PowerShell或命令提示符

**Q: 处理后文件无法找到**  
A: 检查备份目录，或查看工具输出的详细日志

### 恢复操作

```powershell
# 从备份目录恢复文件
$backupDir = "duplicate_files_backup_20250624_130000"
Get-ChildItem $backupDir | ForEach-Object {
    $originalName = $_.Name -replace '^duplicate_\d+_', ''
    Copy-Item $_.FullName "恢复目录\$originalName"
}
```

---

## 📈 性能优化建议

### 提高扫描速度
1. **排除系统目录**: 避免扫描系统文件夹
2. **文件类型过滤**: 只扫描特定类型的文件
3. **并行处理**: 对于多核CPU，可以考虑并行化

### 减少内存使用
1. **分批处理**: 将大目录分成小批次处理
2. **文件大小限制**: 设置最小文件大小阈值
3. **及时清理**: 处理完成后清理临时数据

---

## 🔄 更新日志

### v1.0 (2025-06-24)
- ✅ 初始版本发布
- ✅ 支持基于MD5的重复文件检测
- ✅ 支持三种处理策略：删除、备份、硬链接
- ✅ 支持JSON格式报告输出
- ✅ 支持PowerShell脚本生成
- ✅ 提供详细的统计信息和处理建议

---

## 📞 技术支持

如有问题或建议，请：
1. 查看本使用指南的故障排除部分
2. 检查工具输出的错误信息
3. 确认Python和PowerShell环境配置正确
4. 记录详细的错误信息和操作步骤
