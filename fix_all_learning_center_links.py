#!/usr/bin/env python3
"""
批量修复所有页面的学习中心链接
将 resources.html 或 /blog/ 改为相对路径 blog/
"""

import os
import re

def fix_learning_center_links(filepath):
    """修复单个文件的学习中心链接"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替换所有错误的链接为正确的相对路径 blog/
        # 1. 替换 resources.html
        content = content.replace('href="resources.html"', 'href="blog/"')
        content = content.replace("href='resources.html'", "href='blog/'")
        
        # 2. 替换 /blog/（绝对路径）为 blog/（相对路径）
        content = content.replace('href="/blog/"', 'href="blog/"')
        content = content.replace("href='/blog/'", "href='blog/'")
        
        # 检查是否有修改
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "已修复"
        else:
            return False, "无需修复"
            
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    print("=" * 70)
    print("🔧 批量修复所有页面的学习中心链接")
    print("=" * 70)
    print()
    
    fixed = 0
    skipped = 0
    errors = 0
    
    # 要处理的目录和文件模式
    directories = [
        ('', '*.html'),           # 根目录
        ('en', 'en/*.html'),      # 英文版
        ('jp', 'jp/*.html'),      # 日文版
        ('kr', 'kr/*.html'),      # 韩文版
    ]
    
    fixed_files = []
    skipped_files = []
    
    for dir_name, pattern in directories:
        import glob
        files = glob.glob(pattern)
        
        for filepath in files:
            # 跳过备份文件
            if 'backup' in filepath or 'bak' in filepath or '.bak' in filepath:
                continue
            
            success, message = fix_learning_center_links(filepath)
            
            if success:
                print(f"✅ {filepath}")
                fixed_files.append(filepath)
                fixed += 1
            elif "无需修复" in message:
                skipped += 1
                skipped_files.append(filepath)
            else:
                print(f"❌ {filepath} - {message}")
                errors += 1
    
    print()
    print("=" * 70)
    print("📊 统计")
    print("=" * 70)
    print(f"✅ 已修复：{fixed} 个文件")
    print(f"⏭️  无需修复：{skipped} 个文件")
    print(f"❌ 错误：{errors} 个文件")
    print()
    
    if fixed > 0:
        print("=" * 70)
        print("📝 已修复的文件列表")
        print("=" * 70)
        for f in fixed_files[:20]:  # 只显示前20个
            print(f"  • {f}")
        if len(fixed_files) > 20:
            print(f"  ... 还有 {len(fixed_files) - 20} 个文件")
        print()

if __name__ == '__main__':
    main()

