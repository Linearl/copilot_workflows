# 终端UTF-8编码配置

## 概述

为了解决PowerShell终端中中文字符显示乱码（如"鐢熸垚瀹屾垚"等mojibake）问题，项目配置了自动UTF-8编码初始化。

## 文件说明

### `.vscode/terminal-init.ps1`

终端初始化脚本，包含以下功能：

- 设置控制台代码页为UTF-8 (`chcp 65001`)
- 设置Python IO编码为UTF-8
- 设置PowerShell输入/输出编码为UTF-8
- 显示初始化状态信息

### `.vscode/settings.json`

VS Code工作区设置，包含：

- 配置默认终端为标准"PowerShell"配置文件
- 自动加载终端初始化脚本
- 通过环境变量设置Python IO编码
- 启用终端Shell集成功能

## 使用方法

1. **自动启用**：在VS Code中打开新终端时，会自动应用UTF-8配置
2. **手动运行**：在现有终端中执行 `.\.vscode\terminal-init.ps1`
3. **验证设置**：终端启动时会显示绿色的"Terminal initialized: UTF-8"消息

## 解决的问题

- 修复中文字符显示为乱码（如"鐢熸垚瀹屾垚"变为"生成完成"）
- 确保Python脚本输出的中文正确显示
- 统一项目中所有脚本的编码环境

## 注意事项

- 脚本需要PowerShell执行策略允许（已在配置中使用`-ExecutionPolicy Bypass`）
- 更改仅影响当前VS Code工作区的终端
- 系统级终端设置不受影响
