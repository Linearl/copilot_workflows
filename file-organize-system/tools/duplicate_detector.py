#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件重复检测工具
基于文件内容的MD5和SHA256哈希值检测重复文件
支持JSON格式输出报告，便于后续处理
"""

import os
import hashlib
import json
import argparse
import time
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

class DuplicateFileDetector:
    """重复文件检测器"""
    
    def __init__(self, directory: str, output_file: str = None):
        self.directory = Path(directory)
        self.output_file = output_file
        self.file_hashes = defaultdict(list)
        self.scan_stats = {
            'total_files': 0,
            'total_size': 0,
            'duplicate_groups': 0,
            'duplicate_files': 0,
            'space_wasted': 0,
            'scan_time': 0
        }
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = 'md5') -> str:
        """计算文件哈希值"""
        hash_obj = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                # 分块读取，适合大文件
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except (IOError, OSError) as e:
            print(f"无法读取文件 {file_path}: {e}")
            return None
    
    def scan_directory(self) -> None:
        """扫描目录中的所有文件"""
        print(f"开始扫描目录: {self.directory}")
        start_time = time.time()
        
        for file_path in self.directory.rglob('*'):
            if file_path.is_file():
                self.scan_stats['total_files'] += 1
                
                try:
                    file_size = file_path.stat().st_size
                    self.scan_stats['total_size'] += file_size
                    
                    # 计算文件哈希
                    file_hash = self.calculate_file_hash(file_path, 'md5')
                    if file_hash:
                        file_info = {
                            'path': str(file_path),
                            'name': file_path.name,
                            'size': file_size,
                            'size_mb': round(file_size / (1024 * 1024), 2),
                            'modified_time': file_path.stat().st_mtime,
                            'extension': file_path.suffix.lower()
                        }
                        self.file_hashes[file_hash].append(file_info)
                    
                    # 进度显示
                    if self.scan_stats['total_files'] % 100 == 0:
                        print(f"已扫描 {self.scan_stats['total_files']} 个文件...")
                        
                except (OSError, IOError) as e:
                    print(f"跳过文件 {file_path}: {e}")
                    continue
        
        self.scan_stats['scan_time'] = round(time.time() - start_time, 2)
        print(f"扫描完成！共处理 {self.scan_stats['total_files']} 个文件")
    
    def find_duplicates(self) -> Dict:
        """查找重复文件并生成报告"""
        duplicate_groups = {}
        group_id = 1
        
        for file_hash, files in self.file_hashes.items():
            if len(files) > 1:
                # 按修改时间排序，最新的在前
                files.sort(key=lambda x: x['modified_time'], reverse=True)
                
                # 计算浪费的空间（除了保留最新的一个文件）
                file_size = files[0]['size']
                wasted_space = file_size * (len(files) - 1)
                self.scan_stats['space_wasted'] += wasted_space
                
                duplicate_groups[f"group_{group_id}"] = {
                    'hash': file_hash,
                    'file_count': len(files),
                    'file_size': file_size,
                    'file_size_mb': round(file_size / (1024 * 1024), 2),
                    'wasted_space_mb': round(wasted_space / (1024 * 1024), 2),
                    'files': files,
                    'recommended_action': self._get_recommendation(files)
                }
                
                self.scan_stats['duplicate_files'] += len(files)
                group_id += 1
        
        self.scan_stats['duplicate_groups'] = len(duplicate_groups)
        self.scan_stats['space_wasted_mb'] = round(self.scan_stats['space_wasted'] / (1024 * 1024), 2)
        
        return duplicate_groups
    
    def _get_recommendation(self, files: List[Dict]) -> str:
        """根据文件信息生成处理建议"""
        if len(files) == 2:
            return "保留最新文件，删除旧版本"
        elif len(files) > 2:
            return "保留最新文件，将其他版本移至备份目录"
        else:
            return "无需处理"
    
    def generate_report(self) -> Dict:
        """生成完整的检测报告"""
        print("正在分析重复文件...")
        duplicate_groups = self.find_duplicates()
        
        report = {
            'scan_info': {
                'directory': str(self.directory),
                'scan_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                'scan_duration_seconds': self.scan_stats['scan_time']
            },
            'statistics': self.scan_stats,
            'duplicate_groups': duplicate_groups,
            'summary': {
                'has_duplicates': len(duplicate_groups) > 0,
                'total_duplicate_groups': len(duplicate_groups),
                'total_duplicate_files': self.scan_stats['duplicate_files'],
                'potential_space_saving_mb': self.scan_stats['space_wasted_mb']
            }
        }
        
        return report
    
    def save_report(self, report: Dict) -> None:
        """保存报告到文件"""
        if self.output_file:
            try:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                print(f"报告已保存到: {self.output_file}")
            except IOError as e:
                print(f"保存报告失败: {e}")
    
    def print_summary(self, report: Dict) -> None:
        """打印检测结果摘要"""
        stats = report['statistics']
        summary = report['summary']
        
        print("\n" + "="*60)
        print("重复文件检测结果摘要")
        print("="*60)
        print(f"扫描目录: {report['scan_info']['directory']}")
        print(f"扫描时间: {report['scan_info']['scan_time']}")
        print(f"扫描耗时: {stats['scan_time']} 秒")
        print(f"总文件数: {stats['total_files']}")
        print(f"总大小: {round(stats['total_size'] / (1024*1024), 2)} MB")
        print(f"重复文件组: {summary['total_duplicate_groups']}")
        print(f"重复文件数: {summary['total_duplicate_files']}")
        print(f"可节省空间: {summary['potential_space_saving_mb']} MB")
        
        if summary['has_duplicates']:
            print(f"\n发现 {summary['total_duplicate_groups']} 组重复文件:")
            for group_name, group_info in report['duplicate_groups'].items():
                print(f"\n📁 {group_name}:")
                print(f"   文件数量: {group_info['file_count']}")
                print(f"   文件大小: {group_info['file_size_mb']} MB")
                print(f"   浪费空间: {group_info['wasted_space_mb']} MB")
                print(f"   处理建议: {group_info['recommended_action']}")
                for i, file_info in enumerate(group_info['files'][:3]):  # 只显示前3个
                    status = "📌 最新" if i == 0 else f"📄 副本{i}"
                    print(f"   {status}: {file_info['name']}")
                    print(f"        路径: {file_info['path']}")
                if len(group_info['files']) > 3:
                    print(f"   ... 还有 {len(group_info['files']) - 3} 个文件")
        else:
            print("\n✅ 未发现重复文件！")
        
        print("="*60)

def main():
    parser = argparse.ArgumentParser(description='重复文件检测工具')
    parser.add_argument('--directory', '-d', required=True,
                       help='要扫描的目录路径')
    parser.add_argument('--output', '-o', 
                       help='输出报告文件路径 (JSON格式)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='静默模式，只输出摘要')
    
    args = parser.parse_args()
    
    # 验证目录是否存在
    if not os.path.exists(args.directory):
        print(f"错误: 目录 '{args.directory}' 不存在")
        return 1
    
    # 设置默认输出文件名
    if not args.output:
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        args.output = f"duplicate_files_report_{timestamp}.json"
    
    try:
        # 创建检测器并运行
        detector = DuplicateFileDetector(args.directory, args.output)
        detector.scan_directory()
        report = detector.generate_report()
        
        # 保存和显示报告
        detector.save_report(report)
        if not args.quiet:
            detector.print_summary(report)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n检测被用户中断")
        return 1
    except Exception as e:
        print(f"检测过程中发生错误: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
