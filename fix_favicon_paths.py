#!/usr/bin/env python3
"""
修复子目录中favicon路径错误的问题
将 href="favicon 改为 href="../favicon
"""

import os
import re

def fix_favicon_path(file_path):
    """修复单个文件的favicon路径"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否需要修复
        if 'href="favicon' not in content:
            return False, "无需修复"
        
        # 替换错误的路径
        new_content = content.replace('href="favicon', 'href="../favicon')
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "已修复"
        
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    print("=" * 70)
    print("🔧 修复子目录中的Favicon路径")
    print("=" * 70)
    print()
    
    fixed = 0
    skipped = 0
    errors = 0
    
    # 要检查的目录
    directories = ['en', 'jp', 'kr']
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        for filename in os.listdir(directory):
            if filename.endswith('.html'):
                file_path = os.path.join(directory, filename)
                success, message = fix_favicon_path(file_path)
                
                if success:
                    print(f"✅ {file_path}")
                    fixed += 1
                elif "无需修复" in message:
                    skipped += 1
                else:
                    print(f"❌ {file_path} - {message}")
                    errors += 1
    
    print()
    print("=" * 70)
    print("📊 统计")
    print("=" * 70)
    print(f"✅ 已修复：{fixed}")
    print(f"⏭️  无需修复：{skipped}")
    print(f"❌ 错误：{errors}")
    print()

if __name__ == '__main__':
    main()

