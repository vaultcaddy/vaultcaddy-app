#!/usr/bin/env python3
"""
自动为所有HTML页面添加Favicon
作用: 确保所有页面都有统一的favicon配置
"""

import os
import re
from pathlib import Path

# Favicon HTML代码（标准配置）
FAVICON_HTML = '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="alternate icon" type="image/png" href="favicon.png">'''

def calculate_favicon_path(file_path):
    """计算相对于文件的favicon路径"""
    depth = str(file_path).count(os.sep) - 1  # 减1因为根目录不计
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
        
        # 生成favicon代码（使用相对路径）
        favicon_code = f'''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="{svg_path}">
    <link rel="alternate icon" type="image/png" href="{png_path}">'''
        
        # 查找<head>标签后的插入点（在charset之后）
        # 优先在<meta charset>之后插入
        if '<meta charset=' in content:
            pattern = r'(<meta charset="[^"]+">)'
            replacement = r'\1\n' + favicon_code
            new_content = re.sub(pattern, replacement, content, count=1)
        # 如果没有charset，在<head>之后插入
        elif '<head>' in content:
            pattern = r'(<head>)'
            replacement = r'\1\n' + favicon_code
            new_content = re.sub(pattern, replacement, content, count=1)
        else:
            return False, "未找到<head>标签"
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, f"已添加（{svg_path}）"
        
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    print("=" * 70)
    print("🎨 批量添加 Favicon 到所有 HTML 页面")
    print("=" * 70)
    print()
    
    # 统计
    total = 0
    added = 0
    skipped = 0
    errors = 0
    
    # 排除的目录
    exclude_dirs = {'node_modules', '.git', 'backup_latest', 'backup_before_restore'}
    
    # 遍历所有HTML文件
    for root, dirs, files in os.walk('.'):
        # 过滤排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                total += 1
                
                success, message = add_favicon_to_file(file_path)
                
                if success:
                    print(f"✅ {file_path} - {message}")
                    added += 1
                elif "已有favicon" in message:
                    # print(f"⏭️  {file_path} - {message}")
                    skipped += 1
                else:
                    print(f"❌ {file_path} - {message}")
                    errors += 1
    
    print()
    print("=" * 70)
    print("📊 统计")
    print("=" * 70)
    print(f"总HTML文件数：{total}")
    print(f"✅ 已添加favicon：{added}")
    print(f"⏭️  已有favicon（跳过）：{skipped}")
    print(f"❌ 错误：{errors}")
    print()
    print(f"✨ 完成！现在所有 {total} 个页面都有 favicon 了！")
    print()

if __name__ == '__main__':
    main()

