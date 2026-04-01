#!/usr/bin/env python3
"""
改进版：自动为所有HTML页面添加Favicon
支持更多<head>结构
"""

import os
import re
from pathlib import Path

def calculate_favicon_path(file_path):
    """计算相对于文件的favicon路径"""
    depth = str(file_path).count(os.sep) - 1
    if depth == 0:
        return 'favicon.svg', 'favicon.png'
    else:
        prefix = '../' * depth
        return f'{prefix}favicon.svg', f'{prefix}favicon.png'

def add_favicon_to_file(file_path):
    """为单个HTML文件添加favicon"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有favicon
        if 'favicon' in content.lower():
            return False, "已有favicon"
        
        # 计算相对路径
        svg_path, png_path = calculate_favicon_path(Path(file_path))
        
        # 生成favicon代码
        favicon_code = f'''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="{svg_path}">
    <link rel="alternate icon" type="image/png" href="{png_path}">
'''
        
        # 尝试多种插入位置（按优先级）
        patterns = [
            # 1. 在<meta charset>之后
            (r'(<meta charset="[^"]+">)\n', r'\1\n' + favicon_code),
            # 2. 在第一个<link rel="preconnect">之前
            (r'(\s*)(<link rel="preconnect")', r'\1' + favicon_code + r'\2'),
            # 3. 在<meta name="viewport">之后
            (r'(<meta name="viewport"[^>]*>)\n', r'\1\n' + favicon_code),
            # 4. 在<head>之后
            (r'(<head>)\n', r'\1\n' + favicon_code),
            # 5. 在<head>之后（没有换行）
            (r'(<head>)', r'\1\n' + favicon_code),
        ]
        
        new_content = None
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                new_content = re.sub(pattern, replacement, content, count=1)
                break
        
        if new_content is None:
            return False, "未找到合适的插入点"
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"已添加（{svg_path}）"
        
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    print("=" * 70)
    print("🎨 批量添加 Favicon（改进版v2）")
    print("=" * 70)
    print()
    
    total = 0
    added = 0
    skipped = 0
    errors = 0
    
    exclude_dirs = {'node_modules', '.git', 'backup_latest', 'backup_before_restore'}
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                total += 1
                
                success, message = add_favicon_to_file(file_path)
                
                if success:
                    print(f"✅ {file_path}")
                    added += 1
                elif "已有favicon" in message:
                    skipped += 1
                else:
                    print(f"❌ {file_path} - {message}")
                    errors += 1
    
    print()
    print("=" * 70)
    print("📊 统计")
    print("=" * 70)
    print(f"总HTML文件数：{total}")
    print(f"✅ 新添加favicon：{added}")
    print(f"⏭️  已有favicon（跳过）：{skipped}")
    print(f"❌ 无法添加：{errors}")
    print()
    
    # 最终验证
    print("🔍 最终验证...")
    with_favicon = 0
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        if 'favicon' in f.read().lower():
                            with_favicon += 1
                except:
                    pass
    
    print(f"✨ 最终结果：{with_favicon}/{total} 个页面有 favicon")
    print()

if __name__ == '__main__':
    main()

