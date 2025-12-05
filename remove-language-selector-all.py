#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除所有页面的语言选择器
Remove language selector from all pages
"""

import os
import re
from pathlib import Path

def remove_language_selector(filepath):
    """删除文件中的语言选择器"""
    print(f"\n处理: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # 1. 删除桌面版语言选择器 div
        patterns_to_remove = [
            # 桌面版选择器（多种可能的格式）
            r'<!-- 🌍 桌面版語言選擇器 -->\s*<div id="language-selector-desktop"></div>',
            r'<div id="language-selector-desktop"></div>',
            r'<div id="language-selector-desktop"[^>]*></div>',
            
            # 手机版选择器
            r'<!-- 🌍 手機版語言選擇器 -->\s*<div id="language-selector-mobile"[^>]*></div>',
            r'<div id="language-selector-mobile"[^>]*></div>',
            
            # 注释
            r'<!-- 🌍 桌面版語言選擇器 -->',
            r'<!-- 🌍 手機版語言選擇器 -->',
        ]
        
        for pattern in patterns_to_remove:
            new_content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
            if new_content != content:
                changes_made.append(f"删除匹配: {pattern[:50]}...")
                content = new_content
        
        # 2. 删除 language-selector.js 引用
        js_patterns = [
            r'<!-- 🌍 語言選擇器 -->\s*<script src="[^"]*language-selector\.js[^"]*"></script>',
            r'<script src="[^"]*language-selector\.js[^"]*"></script>',
            r'<!-- 語言選擇器 -->\s*<script src="[^"]*language-selector\.js[^"]*"></script>',
        ]
        
        for pattern in js_patterns:
            new_content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
            if new_content != content:
                changes_made.append("删除 language-selector.js 引用")
                content = new_content
        
        # 3. 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 如果有改动，保存文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ 已更新，改动：{len(changes_made)}项")
            for change in changes_made:
                print(f"     - {change}")
            return True
        else:
            print(f"  ℹ️ 无需更新（未找到语言选择器）")
            return False
            
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("🗑️ 删除所有页面的语言选择器")
    print("="*60)
    print()
    
    # 获取所有需要处理的 HTML 文件
    root_dir = Path('.')
    
    # 1. 根目录的 HTML 文件
    root_html_files = list(root_dir.glob('*.html'))
    
    # 2. blog 目录的 HTML 文件
    blog_html_files = list((root_dir / 'blog').glob('*.html')) if (root_dir / 'blog').exists() else []
    
    all_files = root_html_files + blog_html_files
    
    print(f"📁 找到 {len(all_files)} 个 HTML 文件")
    print(f"   - 根目录: {len(root_html_files)} 个")
    print(f"   - blog/: {len(blog_html_files)} 个")
    print()
    
    # 处理所有文件
    updated_count = 0
    skipped_count = 0
    
    for filepath in all_files:
        if remove_language_selector(filepath):
            updated_count += 1
        else:
            skipped_count += 1
    
    # 总结
    print()
    print("="*60)
    print("✅ 处理完成！")
    print("="*60)
    print(f"总文件数: {len(all_files)}")
    print(f"已更新: {updated_count}")
    print(f"跳过: {skipped_count}")
    print()
    
    if updated_count > 0:
        print("🎉 语言选择器已从所有页面删除！")
    else:
        print("ℹ️ 未找到语言选择器（可能已删除）")
    
    print()
    print("📋 已处理的文件类型:")
    print("  ✅ 根目录所有 .html 文件")
    print("  ✅ blog/ 目录所有 .html 文件")
    print()

if __name__ == '__main__':
    main()

