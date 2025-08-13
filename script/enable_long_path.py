# -*- coding: utf-8 -*-
"""
Windows长路径支持启用工具

用于检测和启用Windows系统的长路径支持功能
"""

import argparse
import sys
import subprocess
import os


def check_admin_privileges():
    """检查是否具有管理员权限"""
    try:
        # 尝试访问需要管理员权限的注册表项
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion",
            0,
            winreg.KEY_READ,
        )
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def check_long_path_support():
    """检查长路径支持状态"""
    if sys.platform != "win32":
        print("此工具仅适用于Windows系统")
        return False

    try:
        import winreg

        key_path = r"SYSTEM\CurrentControlSet\Control\FileSystem"

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            try:
                value, reg_type = winreg.QueryValueEx(key, "LongPathsEnabled")
                return value == 1
            except FileNotFoundError:
                return False
            finally:
                winreg.CloseKey(key)
        except Exception:
            return False

    except ImportError:
        print("错误：无法导入winreg模块")
        return False


def enable_long_path_support():
    """启用长路径支持"""
    if not check_admin_privileges():
        print("❌ 错误：需要管理员权限才能修改注册表")
        print("请以管理员身份运行此脚本")
        return False

    try:
        import winreg

        key_path = r"SYSTEM\CurrentControlSet\Control\FileSystem"

        # 打开注册表项
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE
        )

        # 设置LongPathsEnabled为1
        winreg.SetValueEx(key, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)

        print("✓ 长路径支持已成功启用")
        print("⚠️  注意：某些应用程序可能需要重启计算机后才能生效")
        return True

    except Exception as e:
        print(f"❌ 启用长路径支持失败: {e}")
        return False


def enable_via_powershell():
    """通过PowerShell命令启用长路径支持"""
    print("尝试通过PowerShell启用长路径支持...")

    powershell_cmd = [
        "powershell.exe",
        "-Command",
        "Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem' -Name 'LongPathsEnabled' -Value 1",
    ]

    try:
        result = subprocess.run(
            powershell_cmd, capture_output=True, text=True, check=True
        )
        print("✓ 通过PowerShell成功启用长路径支持")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PowerShell命令执行失败: {e}")
        print("可能需要管理员权限")
        return False
    except Exception as e:
        print(f"❌ 执行PowerShell命令时出错: {e}")
        return False


def show_manual_instructions():
    """显示手动启用说明"""
    print("\n=== 手动启用长路径支持的方法 ===")
    print("\n方法1: 通过PowerShell（推荐）")
    print("1. 以管理员身份运行PowerShell")
    print("2. 执行以下命令：")
    print(
        '   Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" -Name "LongPathsEnabled" -Value 1'
    )
    print("3. 验证设置：")
    print(
        '   Get-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" -Name "LongPathsEnabled"'
    )

    print("\n方法2: 通过组策略编辑器")
    print("1. 按Win+R，输入gpedit.msc")
    print("2. 导航至：计算机配置 → 管理模板 → 系统 → 文件系统")
    print("3. 找到并启用：启用 Win32 长路径")

    print("\n方法3: 通过注册表编辑器")
    print("1. 按Win+R，输入regedit")
    print(
        "2. 导航至：HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\FileSystem"
    )
    print("3. 创建或修改DWORD值：LongPathsEnabled = 1")

    print("\n⚠️  重要提示：")
    print("- 修改后可能需要重启计算机")
    print("- 只有Windows 10版本1607或更高版本支持此功能")
    print("- 应用程序需要支持长路径API才能受益")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Windows长路径支持检测和启用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
注意事项:
  • 此工具仅适用于Windows 10版本1607或更高版本
  • 启用长路径支持需要管理员权限
  • 修改后可能需要重启计算机才能生效
  • 应用程序需要支持长路径API才能受益

示例:
  %(prog)s                # 检查状态并交互式启用
  %(prog)s --check        # 仅检查状态
  %(prog)s --enable       # 自动启用（需要管理员权限）
  %(prog)s --manual       # 显示手动启用说明
        """,
    )
    parser.add_argument(
        "--check", action="store_true", help="仅检查长路径支持状态，不进行任何修改"
    )
    parser.add_argument(
        "--enable", action="store_true", help="自动启用长路径支持（需要管理员权限）"
    )
    parser.add_argument("--manual", action="store_true", help="显示手动启用说明")
    parser.add_argument("--force", action="store_true", help="强制执行，跳过确认提示")

    args = parser.parse_args()

    print("=== Windows长路径支持工具 ===\n")

    # 检查平台
    if sys.platform != "win32":
        print("此工具仅适用于Windows系统")
        return 1

    # 仅显示手动说明
    if args.manual:
        show_manual_instructions()
        return 0

    # 检查当前状态
    print("检查当前长路径支持状态...")
    is_enabled = check_long_path_support()

    if is_enabled:
        print("✓ 长路径支持已启用")
        if args.check:
            return 0
    else:
        print("❌ 长路径支持未启用")

    # 仅检查模式
    if args.check:
        return 0 if is_enabled else 1

    # 如果已启用，无需操作
    if is_enabled and not args.force:
        return 0

    # 检查管理员权限
    if not check_admin_privileges():
        print("\n⚠️  当前没有管理员权限")
        print("为了启用长路径支持，需要管理员权限")

        if not args.enable:
            if args.force or input("\n是否显示手动启用说明？(y/n): ").lower() == "y":
                show_manual_instructions()
        return 1

    # 自动启用模式
    if args.enable or args.force:
        print("\n检测到管理员权限，尝试启用长路径支持...")
    else:
        choice = input("\n检测到管理员权限，是否继续启用长路径支持？(y/n): ").lower()
        if choice != "y":
            print("操作已取消")
            return 0

    # 执行启用操作
    success = enable_long_path_support()

    # 如果失败，尝试PowerShell
    if not success:
        print("\n尝试备选方案...")
        success = enable_via_powershell()

    # 验证结果
    if success:
        print("\n验证设置...")
        if check_long_path_support():
            print("✓ 长路径支持启用成功并已验证")
            return 0
        else:
            print("⚠️  设置可能需要重启后生效")
            return 0
    else:
        print("\n❌ 自动启用失败，请使用手动方法")
        if not args.enable:
            show_manual_instructions()
        return 1


if __name__ == "__main__":
    sys.exit(main())
