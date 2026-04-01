#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除HTML文件中的console.log语句
保留关键错误信息，移除调试日志
"""

import re
import os

def remove_console_logs(file_path):
    """移除文件中的console.log语句"""
    print(f"\n处理文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 统计原始console语句数量
    console_logs = len(re.findall(r'console\.log\s*\(', content))
    console_errors = len(re.findall(r'console\.error\s*\(', content))
    console_warns = len(re.findall(r'console\.warn\s*\(', content))
    
    print(f"  找到 {console_logs} 个 console.log")
    print(f"  找到 {console_errors} 个 console.error")
    print(f"  找到 {console_warns} 个 console.warn")
    
    # 方法1: 注释掉console.log (保留代码便于调试)
    # content = re.sub(r'(\s*)console\.log\s*\([^;]*\);?', r'\1// console.log removed', content)
    
    # 方法2: 完全删除console.log行 (更干净)
    content = re.sub(r'\s*console\.log\s*\([^)]*\);\s*\n?', '\n', content)
    
    # 保留重要的console.error (用于错误追踪)
    # content = re.sub(r'\s*console\.error\s*\([^)]*\);\s*\n?', '\n', content)
    
    # 删除console.warn
    content = re.sub(r'\s*console\.warn\s*\([^)]*\);\s*\n?', '\n', content)
    
    # 删除空的console对象调用 (跨行的)
    content = re.sub(r'console\.log\s*\([^)]*\)', '', content)
    
    # 清理多余的空行
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 已移除console日志")
    else:
        print(f"  ℹ️  没有需要移除的内容")
    
    # 统计移除后的数量
    remaining_logs = len(re.findall(r'console\.log\s*\(', content))
    remaining_errors = len(re.findall(r'console\.error\s*\(', content))
    
    print(f"  剩余 {remaining_logs} 个 console.log")
    print(f"  剩余 {remaining_errors} 个 console.error (保留用于错误追踪)")

def main():
    """主函数"""
    print("=== 🧹 清理控制台日志 ===")
    
    # 需要处理的文件列表
    files = [
        'dashboard.html',
        'firstproject.html',
        'document-detail.html',
    ]
    
    for file_path in files:
        if os.path.exists(file_path):
            remove_console_logs(file_path)
        else:
            print(f"⚠️  文件不存在: {file_path}")
    
    print("\n=== ✅ 清理完成 ===")
    print("\n注意事项:")
    print("1. console.error 已保留（用于错误追踪）")
    print("2. console.log 和 console.warn 已移除")
    print("3. 如需恢复，请从备份中还原")

if __name__ == '__main__':
    main()

