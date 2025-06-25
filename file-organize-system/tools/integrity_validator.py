#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件整理完整性验证工具
验证文件整理过程的完整性和正确性
"""

import os
import json
import argparse
from pathlib import Path
from collections import defaultdict

class IntegrityValidator:
    def __init__(self):
        self.original_files = {}
        self.organized_files = {}
        self.issues = []
    
    def scan_directory(self, directory, recursive=True):
        """扫描目录，获取所有文件信息"""
        files = {}
        directory = Path(directory)
        
        if not directory.exists():
            return files
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                try:
                    stat = file_path.stat()
                    relative_path = str(file_path.relative_to(directory))
                    files[relative_path] = {
                        'name': file_path.name,
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'path': str(file_path)
                    }
                except Exception as e:
                    print(f"无法读取文件 {file_path}: {e}")
        
        return files
    
    def validate_original_empty(self, original_dir, organized_dir=None):
        """验证原目录是否完全清空"""
        print(f"检查原目录是否清空: {original_dir}")
        
        remaining_files = self.scan_directory(original_dir)
        
        # 排除已整理目录
        if organized_dir:
            organized_relative = os.path.relpath(organized_dir, original_dir)
            remaining_files = {
                k: v for k, v in remaining_files.items() 
                if not k.startswith(organized_relative)
            }
        
        if remaining_files:
            self.issues.append({
                'type': 'incomplete_cleanup',
                'severity': 'high',
                'message': f'原目录中仍有 {len(remaining_files)} 个文件未处理',
                'files': list(remaining_files.keys())
            })
            print(f"⚠️ 发现 {len(remaining_files)} 个未处理的文件:")
            for file_path in remaining_files:
                print(f"  - {file_path}")
            return False
        else:
            print("✅ 原目录已完全清空")
            return True
    
    def validate_file_integrity(self, before_dir, after_dir):
        """验证文件完整性（文件数量、大小等）"""
        print(f"验证文件完整性...")
        
        before_files = self.scan_directory(before_dir)
        after_files = self.scan_directory(after_dir)
        
        # 按大小和名称匹配文件
        before_by_size_name = defaultdict(list)
        after_by_size_name = defaultdict(list)
        
        for path, info in before_files.items():
            key = (info['size'], info['name'])
            before_by_size_name[key].append(path)
        
        for path, info in after_files.items():
            key = (info['size'], info['name'])
            after_by_size_name[key].append(path)
        
        # 检查是否有文件丢失
        missing_files = []
        for key, paths in before_by_size_name.items():
            if key not in after_by_size_name:
                missing_files.extend(paths)
            elif len(paths) > len(after_by_size_name[key]):
                # 部分文件丢失
                missing_count = len(paths) - len(after_by_size_name[key])
                missing_files.extend(paths[:missing_count])
        
        if missing_files:
            self.issues.append({
                'type': 'missing_files',
                'severity': 'high',
                'message': f'有 {len(missing_files)} 个文件可能丢失',
                'files': missing_files
            })
            print(f"⚠️ 可能丢失的文件:")
            for file_path in missing_files:
                print(f"  - {file_path}")
            return False
        
        # 检查文件数量
        if len(before_files) != len(after_files):
            self.issues.append({
                'type': 'file_count_mismatch',
                'severity': 'medium',
                'message': f'文件数量不匹配: 原{len(before_files)}个，现{len(after_files)}个'
            })
            print(f"⚠️ 文件数量不匹配: 原{len(before_files)}个，现{len(after_files)}个")
        else:
            print(f"✅ 文件数量匹配: {len(after_files)}个文件")
        
        return len(missing_files) == 0
    
    def validate_classification(self, organized_dir, classification_rules=None):
        """验证文件分类的正确性"""
        print("验证文件分类...")
        
        organized_files = self.scan_directory(organized_dir)
        misclassified = []
        
        # 基本分类规则
        default_rules = {
            '01_学术教育资料': ['.pdf', '.docx', '.doc', '.pptx', '.ppt'],
            '02_政策法规文档': ['.pdf', '.docx', '.doc'],
            '03_商业投资资料': ['.pdf', '.xlsx', '.xls', '.docx'],
            '04_软件工具': ['.exe', '.msi', '.zip', '.7z', '.rar'],
            '05_办公文档': ['.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt'],
            '06_媒体文件': ['.mp4', '.avi', '.mkv', '.jpg', '.png', '.gif'],
            '07_数据分析': ['.csv', '.xlsx', '.xls', '.json', '.xml'],
            '99_待确认': []  # 任何类型都可以
        }
        
        rules = classification_rules or default_rules
        
        for file_path, file_info in organized_files.items():
            # 获取文件所在的分类目录
            parts = file_path.split(os.sep)
            if len(parts) < 2:
                continue
                
            category = parts[0]
            file_ext = Path(file_info['name']).suffix.lower()
            
            # 检查分类是否正确
            if category in rules and rules[category]:
                if file_ext not in rules[category]:
                    misclassified.append({
                        'file': file_path,
                        'category': category,
                        'extension': file_ext,
                        'expected_extensions': rules[category]
                    })
        
        if misclassified:
            self.issues.append({
                'type': 'misclassification',
                'severity': 'low',
                'message': f'有 {len(misclassified)} 个文件可能分类错误',
                'details': misclassified
            })
            print(f"⚠️ 可能分类错误的文件:")
            for item in misclassified:
                print(f"  - {item['file']} (类型{item['extension']}, 在{item['category']})")
        else:
            print("✅ 文件分类验证通过")
        
        return len(misclassified) == 0
    
    def generate_report(self, output_file=None):
        """生成验证报告"""
        report = {
            'validation_time': os.popen('date').read().strip(),
            'total_issues': len(self.issues),
            'issues_by_severity': {
                'high': len([i for i in self.issues if i['severity'] == 'high']),
                'medium': len([i for i in self.issues if i['severity'] == 'medium']),
                'low': len([i for i in self.issues if i['severity'] == 'low'])
            },
            'issues': self.issues
        }
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"验证报告已保存到: {output_file}")
        
        return report
    
    def print_summary(self):
        """打印验证结果摘要"""
        print("\n" + "="*50)
        print("📊 验证结果摘要")
        print("="*50)
        
        if not self.issues:
            print("✅ 所有验证项目都通过了！整理工作完成得很好。")
        else:
            high_issues = [i for i in self.issues if i['severity'] == 'high']
            medium_issues = [i for i in self.issues if i['severity'] == 'medium']
            low_issues = [i for i in self.issues if i['severity'] == 'low']
            
            print(f"总问题数: {len(self.issues)}")
            if high_issues:
                print(f"🔴 高优先级问题: {len(high_issues)}个")
            if medium_issues:
                print(f"🟡 中优先级问题: {len(medium_issues)}个")
            if low_issues:
                print(f"🟢 低优先级问题: {len(low_issues)}个")
        
        print("="*50)

def main():
    parser = argparse.ArgumentParser(description='文件整理完整性验证工具')
    parser.add_argument('--original', required=True, help='原始目录路径')
    parser.add_argument('--organized', help='整理后的目录路径')
    parser.add_argument('--backup', help='备份目录路径（用于完整性对比）')
    parser.add_argument('--output', help='输出报告文件路径')
    parser.add_argument('--skip-empty-check', action='store_true', help='跳过原目录清空检查')
    
    args = parser.parse_args()
    
    validator = IntegrityValidator()
    
    print("🔍 开始文件整理完整性验证...")
    print(f"原始目录: {args.original}")
    if args.organized:
        print(f"整理后目录: {args.organized}")
    if args.backup:
        print(f"备份目录: {args.backup}")
    print("-" * 50)
    
    # 检查原目录是否清空
    if not args.skip_empty_check:
        validator.validate_original_empty(args.original, args.organized)
    
    # 检查文件完整性
    if args.backup and args.organized:
        validator.validate_file_integrity(args.backup, args.organized)
    
    # 检查分类正确性
    if args.organized:
        validator.validate_classification(args.organized)
    
    # 生成报告
    validator.generate_report(args.output)
    validator.print_summary()

if __name__ == '__main__':
    main()
