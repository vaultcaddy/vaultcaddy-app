#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 修复台灣用戶常見問題的内联样式问题
删除 display: none，让CSS的max-height控制显示/隐藏
"""

import os
import re
from pathlib import Path

def fix_inline_style(file_path):
    """删除faq-answer的display: none内联样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找并替换：将 display: none 从内联样式中删除
        # 但保留其他样式
        pattern = r'(<div class="faq-answer" style="display: none;)([^"]*")'
        replacement = r'<div class="faq-answer" style="\2'
        
        content = re.sub(pattern, replacement, content)
        
        # 如果style只剩下display: none，则完全删除style属性
        content = content.replace('<div class="faq-answer" style="display: none;">', '<div class="faq-answer">')
        
        # 清理可能出现的空style属性
        content = content.replace(' style=""', '')
        
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
    
    print("🔧 开始修复台灣用戶常見問題的内联样式...")
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
            if fix_inline_style(file_path):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
        total_fixed += fixed_count
    
    print("\n" + "=" * 80)
    print(f"🎉 内联样式修复完成！共修复 {total_fixed} 个页面")
    print("=" * 80)
    print("\n请刷新本地文件并测试台灣用戶常見問題！")

if __name__ == '__main__':
    main()

