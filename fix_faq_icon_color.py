#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 修复FAQ图标颜色和黑色条样式
1. 台灣用戶常見問題的+号改为深灰色（在白色背景上可见）
2. 删除AES-256加密上方的黑色条
"""

import os
import re
from pathlib import Path

def fix_styles(file_path):
    """修复样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. 修改台灣用戶常見問題部分的+号颜色
        # 从蓝色 (#6366f1) 改为深灰色 (#2d3748)
        # 只修改台灣用戶常見問題部分的样式（有内联样式的那部分）
        
        # 查找台灣用戶常見問題的开始
        taiwan_section_start = content.find('❓ 台灣用戶常見問題')
        if taiwan_section_start > 0:
            # 只在这个部分之后查找和替换
            taiwan_section = content[taiwan_section_start:]
            
            # 替换这个部分的+号颜色
            taiwan_section = taiwan_section.replace(
                'color: #6366f1;',
                'color: #2d3748;'
            )
            
            # 重新组合内容
            content = content[:taiwan_section_start] + taiwan_section
        
        # 2. 删除黑色条 - 查找Trust Badges部分的深色背景
        # 找到Trust Badges section并修改其背景色
        content = re.sub(
            r'<section[^>]*style="[^"]*background:\s*#0f172a[^"]*"[^>]*>',
            lambda m: m.group(0).replace('background: #0f172a', 'background: #ffffff'),
            content
        )
        
        # 也处理其他可能的深色背景
        content = re.sub(
            r'background:\s*var\(--dark\)',
            'background: #ffffff',
            content
        )
        
        # 写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"  ❌ 失败: {file_path.name} - {e}")
        return False

def main():
    root_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    
    print("🎨 开始修复FAQ图标颜色和黑色条样式...")
    print("=" * 80)
    
    languages = {
        'zh-TW': '台湾',
        'zh-HK': '香港',
        'ja-JP': '日本',
        'ko-KR': '韩国'
    }
    
    total_fixed = 0
    
    for lang_code, lang_name in languages.items():
        print(f"\n{'='*80}")
        print(f"修复 {lang_name} 版本 ({lang_code})...")
        print(f"{'='*80}")
        
        lang_dir = root_dir / lang_code
        if not lang_dir.exists():
            print(f"  ⚠️ 目录不存在: {lang_dir}")
            continue
        
        lang_files = list(lang_dir.glob('*-v3.html'))
        lang_files = [f for f in lang_files if 'test' not in f.name and 'backup' not in f.name]
        
        print(f"  找到 {len(lang_files)} 个页面")
        
        fixed_count = 0
        for i, file_path in enumerate(lang_files, 1):
            if fix_styles(file_path):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
        total_fixed += fixed_count
    
    print("\n" + "=" * 80)
    print(f"🎉 样式修复完成！共修复 {total_fixed} 个页面")
    print("=" * 80)
    print("\n修复内容：")
    print("  1. ✅ 台灣用戶常見問題的+号改为深灰色（#2d3748）")
    print("  2. ✅ Trust Badges部分的黑色背景改为白色")
    print("\n请刷新本地文件查看效果！")

if __name__ == '__main__':
    main()

