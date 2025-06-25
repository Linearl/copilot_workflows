#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重复文件处理工具
基于duplicate_detector.py生成的报告处理重复文件
支持多种处理策略：删除、移动到备份目录、创建硬链接等
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from typing import Dict, List
import time

class DuplicateFileProcessor:
    """重复文件处理器"""
    
    def __init__(self, report_file: str, backup_dir: str = None):
        self.report_file = report_file
        self.backup_dir = Path(backup_dir) if backup_dir else None
        self.report_data = None
        self.processed_count = 0
        self.space_saved = 0
        
    def load_report(self) -> bool:
        """加载重复文件检测报告"""
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                self.report_data = json.load(f)
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"加载报告文件失败: {e}")
            return False
    
    def create_backup_directory(self) -> bool:
        """创建备份目录"""
        if not self.backup_dir:
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            self.backup_dir = Path(f"duplicate_files_backup_{timestamp}")
        
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            print(f"备份目录: {self.backup_dir}")
            return True
        except OSError as e:
            print(f"创建备份目录失败: {e}")
            return False
    
    def process_duplicates(self, strategy: str = 'backup', dry_run: bool = True) -> None:
        """处理重复文件"""
        if not self.report_data:
            print("错误: 未加载报告数据")
            return
        
        duplicate_groups = self.report_data.get('duplicate_groups', {})
        if not duplicate_groups:
            print("未发现重复文件，无需处理")
            return
        
        print(f"处理策略: {strategy}")
        print(f"预览模式: {'是' if dry_run else '否'}")
        print(f"待处理组数: {len(duplicate_groups)}")
        
        if strategy == 'backup' and not dry_run:
            if not self.create_backup_directory():
                return
        
        for group_name, group_info in duplicate_groups.items():
            print(f"\n处理 {group_name}:")
            self._process_group(group_info, strategy, dry_run)
        
        print(f"\n处理完成!")
        print(f"处理文件数: {self.processed_count}")
        print(f"节省空间: {round(self.space_saved / (1024*1024), 2)} MB")
    
    def _process_group(self, group_info: Dict, strategy: str, dry_run: bool) -> None:
        """处理单个重复文件组"""
        files = group_info['files']
        if len(files) < 2:
            return
        
        # 保留第一个文件（最新的），处理其余文件
        keep_file = files[0]
        duplicate_files = files[1:]
        
        print(f"  保留: {keep_file['name']}")
        
        for i, file_info in enumerate(duplicate_files, 1):
            file_path = Path(file_info['path'])
            
            if not file_path.exists():
                print(f"  跳过: {file_info['name']} (文件不存在)")
                continue
            
            if strategy == 'delete':
                self._delete_file(file_path, file_info, dry_run)
            elif strategy == 'backup':
                self._backup_file(file_path, file_info, dry_run, i)
            elif strategy == 'hardlink':
                self._create_hardlink(file_path, keep_file, file_info, dry_run)
            
            if not dry_run:
                self.space_saved += file_info['size']
                self.processed_count += 1
    
    def _delete_file(self, file_path: Path, file_info: Dict, dry_run: bool) -> None:
        """删除重复文件"""
        if dry_run:
            print(f"  [预览] 删除: {file_info['name']}")
        else:
            try:
                file_path.unlink()
                print(f"  ✅ 已删除: {file_info['name']}")
            except OSError as e:
                print(f"  ❌ 删除失败: {file_info['name']} - {e}")
    
    def _backup_file(self, file_path: Path, file_info: Dict, dry_run: bool, index: int) -> None:
        """移动重复文件到备份目录"""
        if dry_run:
            print(f"  [预览] 备份: {file_info['name']}")
            return
        
        try:
            # 在备份目录中保持相对路径结构
            backup_path = self.backup_dir / f"duplicate_{index}_{file_path.name}"
            
            # 确保备份文件名唯一
            counter = 1
            while backup_path.exists():
                name_parts = file_path.stem, counter, file_path.suffix
                backup_path = self.backup_dir / f"duplicate_{index}_{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                counter += 1
            
            shutil.move(str(file_path), str(backup_path))
            print(f"  ✅ 已备份: {file_info['name']} -> {backup_path.name}")
        except (OSError, shutil.Error) as e:
            print(f"  ❌ 备份失败: {file_info['name']} - {e}")
    
    def _create_hardlink(self, file_path: Path, keep_file: Dict, file_info: Dict, dry_run: bool) -> None:
        """创建硬链接替换重复文件"""
        if dry_run:
            print(f"  [预览] 创建硬链接: {file_info['name']}")
            return
        
        try:
            keep_path = Path(keep_file['path'])
            file_path.unlink()  # 删除重复文件
            file_path.hardlink_to(keep_path)  # 创建硬链接
            print(f"  ✅ 已创建硬链接: {file_info['name']}")
        except OSError as e:
            print(f"  ❌ 硬链接失败: {file_info['name']} - {e}")
    
    def generate_processing_script(self, strategy: str = 'backup') -> str:
        """生成PowerShell处理脚本"""
        if not self.report_data:
            return ""
        
        script_lines = [
            "# 重复文件处理脚本",
            "# 由duplicate_processor.py自动生成",
            f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"# 处理策略: {strategy}",
            "",
            "Write-Host '开始处理重复文件...'",
            ""
        ]
        
        if strategy == 'backup':
            backup_dir = f"duplicate_files_backup_{time.strftime('%Y%m%d_%H%M%S')}"
            script_lines.extend([
                f"$backupDir = '{backup_dir}'",
                "New-Item -ItemType Directory -Path $backupDir -Force | Out-Null",
                "Write-Host '创建备份目录: $backupDir'",
                ""
            ])
        
        duplicate_groups = self.report_data.get('duplicate_groups', {})
        for group_name, group_info in duplicate_groups.items():
            files = group_info['files']
            if len(files) < 2:
                continue
            
            script_lines.append(f"# 处理 {group_name}")
            script_lines.append(f"Write-Host '处理 {group_name}...'")
            
            keep_file = files[0]
            script_lines.append(f"# 保留: {keep_file['name']}")
            
            for i, file_info in enumerate(files[1:], 1):
                file_path = file_info['path'].replace('\\', '\\\\')
                
                if strategy == 'delete':
                    script_lines.append(f"Remove-Item '{file_path}' -Force")
                elif strategy == 'backup':
                    backup_name = f"duplicate_{i}_{Path(file_info['path']).name}"
                    script_lines.append(f"Move-Item '{file_path}' (Join-Path $backupDir '{backup_name}')")
            
            script_lines.append("")
        
        script_lines.extend([
            "Write-Host '重复文件处理完成!'",
            "Write-Host '请检查处理结果'"
        ])
        
        return "\n".join(script_lines)

def main():
    parser = argparse.ArgumentParser(description='重复文件处理工具')
    parser.add_argument('--report', '-r', required=True,
                       help='重复文件检测报告路径 (JSON格式)')
    parser.add_argument('--strategy', '-s', 
                       choices=['delete', 'backup', 'hardlink'],
                       default='backup',
                       help='处理策略: delete(删除), backup(备份), hardlink(硬链接)')
    parser.add_argument('--backup-dir', '-b',
                       help='备份目录路径 (仅backup策略)')
    parser.add_argument('--execute', action='store_true',
                       help='执行处理 (默认为预览模式)')
    parser.add_argument('--generate-script', action='store_true',
                       help='生成PowerShell处理脚本')
    
    args = parser.parse_args()
    
    # 验证报告文件是否存在
    if not os.path.exists(args.report):
        print(f"错误: 报告文件 '{args.report}' 不存在")
        return 1
    
    try:
        processor = DuplicateFileProcessor(args.report, args.backup_dir)
        
        if not processor.load_report():
            return 1
        
        if args.generate_script:
            script_content = processor.generate_processing_script(args.strategy)
            script_file = f"process_duplicates_{args.strategy}.ps1"
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
            print(f"处理脚本已生成: {script_file}")
        else:
            processor.process_duplicates(args.strategy, dry_run=not args.execute)
        
        return 0
        
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
