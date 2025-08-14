# Terminal Initialization Script for UTF-8 Encoding
# 为终端设置UTF-8编码，解决中文字符显示问题

# 设置控制台代码页为UTF-8
chcp 65001 | Out-Null

# 设置Python IO编码为UTF-8
$env:PYTHONIOENCODING = "utf-8"

# 设置PowerShell输出编码为UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# 显示初始化完成信息
Write-Host "Terminal initialized: UTF-8" -ForegroundColor Green
Write-Host "Code Page: $(chcp)" -ForegroundColor Gray
Write-Host "Python IO Encoding: $env:PYTHONIOENCODING" -ForegroundColor Gray
