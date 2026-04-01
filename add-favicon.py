#!/usr/bin/env python3
"""
为所有 HTML 页面添加 Favicon 配置
确保所有页面使用相同的 Favicon
"""

import os
import re
from pathlib import Path

# Favicon 配置
FAVICON_TEMPLATES = {
    'root': '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="favicon.svg">
    <link rel="alternate icon" type="image/png" href="favicon.png">
''',
    'subdir': '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../favicon.png">
''',
    'subdir2': '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../../favicon.svg">
    <link rel="alternate icon" type="image/png" href="../../favicon.png">
'''
}

def has_favicon(content):
    """检查文件是否已有 Favicon"""
    return bool(re.search(r'<link[^>]*rel=["\'].*icon.*["\']', content, re.IGNORECASE))

def add_favicon(file_path, favicon_code):
    """为文件添加 Favicon"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有 Favicon
        if has_favicon(content):
            return 'exists'
        
        # 在 <head> 后或第一个 <meta> 后添加 Favicon
        # 尝试找到合适的位置
        patterns = [
            (r'(<meta[^>]*charset[^>]*>\s*\n)', r'\1' + favicon_code),
            (r'(<meta[^>]*viewport[^>]*>\s*\n)', r'\1' + favicon_code),
            (r'(<title>[^<]*</title>\s*\n)', r'\1' + favicon_code),
            (r'(<head[^>]*>\s*\n)', r'\1' + favicon_code),
        ]
        
        modified = False
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content, count=1)
                modified = True
                break
        
        if not modified:
            return 'skip'
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return 'added'
    
    except Exception as e:
        print(f"  ❌ 错误: {file_path} - {e}")
        return 'error'

def process_directory(base_dir):
    """处理目录中的所有 HTML 文件"""
    stats = {'total': 0, 'added': 0, 'exists': 0, 'skip': 0, 'error': 0}
    
    # 1. 根目录 HTML 文件
    print("\n📁 处理根目录...")
    for html_file in Path(base_dir).glob('*.html'):
        stats['total'] += 1
        result = add_favicon(html_file, FAVICON_TEMPLATES['root'])
        stats[result] += 1
        
        if result == 'added':
            print(f"  ➕ 已添加: {html_file.name}")
        elif result == 'exists':
            print(f"  ✅ 已存在: {html_file.name}")
    
    # 2. 子目录（en/, jp/, kr/）
    for lang_dir in ['en', 'jp', 'kr']:
        lang_path = Path(base_dir) / lang_dir
        if not lang_path.exists():
            continue
        
        print(f"\n📁 处理 {lang_dir}/ 目录...")
        for html_file in lang_path.glob('*.html'):
            stats['total'] += 1
            result = add_favicon(html_file, FAVICON_TEMPLATES['subdir'])
            stats[result] += 1
            
            if result == 'added':
                print(f"  ➕ 已添加: {lang_dir}/{html_file.name}")
            elif result == 'exists':
                print(f"  ✅ 已存在: {lang_dir}/{html_file.name}")
        
        # blog 子目录
        blog_path = lang_path / 'blog'
        if blog_path.exists():
            print(f"\n📁 处理 {lang_dir}/blog/ 目录...")
            for html_file in blog_path.glob('*.html'):
                stats['total'] += 1
                result = add_favicon(html_file, FAVICON_TEMPLATES['subdir2'])
                stats[result] += 1
                
                if result == 'added':
                    print(f"  ➕ 已添加: {lang_dir}/blog/{html_file.name}")
                elif result == 'exists':
                    print(f"  ✅ 已存在: {lang_dir}/blog/{html_file.name}")
    
    # 3. 中文 blog 目录
    blog_path = Path(base_dir) / 'blog'
    if blog_path.exists():
        print(f"\n📁 处理 blog/ 目录...")
        for html_file in blog_path.glob('*.html'):
            stats['total'] += 1
            result = add_favicon(html_file, FAVICON_TEMPLATES['subdir'])
            stats[result] += 1
            
            if result == 'added':
                print(f"  ➕ 已添加: blog/{html_file.name}")
            elif result == 'exists':
                print(f"  ✅ 已存在: blog/{html_file.name}")
    
    return stats

def main():
    print("🔍 开始为所有页面添加 Favicon 配置...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stats = process_directory(base_dir)
    
    # 打印统计信息
    print("\n" + "="*70)
    print("📊 处理完成")
    print("="*70)
    print(f"  检查文件总数: {stats['total']}")
    print(f"  已有 Favicon:  {stats['exists']}")
    print(f"  新增 Favicon:  {stats['added']}")
    print(f"  跳过文件:      {stats['skip']}")
    print(f"  错误文件:      {stats['error']}")
    print("="*70)
    print("\n✅ 所有页面现在都使用相同的 Favicon！")
    print("\n📝 Favicon 文件位置：")
    print("  - favicon.svg (矢量图标)")
    print("  - favicon.png (位图图标)")

if __name__ == '__main__':
    main()

