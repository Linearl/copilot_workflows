@echo off
echo ===================================
echo Windows长路径支持启用工具
echo ===================================
echo.
echo 此工具将帮助启用Windows长路径支持功能
echo 以解决备份过程中的路径长度限制问题
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo 检测到管理员权限，启动工具...
    echo.
    python "%~dp0enable_long_path.py"
) else (
    echo 需要管理员权限才能修改系统设置
    echo 正在请求管理员权限...
    echo.
    
    REM 请求管理员权限并重新运行
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d %~dp0 && python enable_long_path.py && pause' -Verb RunAs"
)

pause
