#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 修复台灣用戶常見問題的样式
为FAQ卡片添加蓝色背景，文字和+号都是白色，并且居中
"""

import os
import re
from pathlib import Path

def fix_taiwan_faq_complete(file_path):
    """完整修复台灣用戶常見問題的样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找台灣用戶常見問題部分
        taiwan_section_start = content.find('❓ 台灣用戶常見問題')
        
        if taiwan_section_start > 0:
            # 找到这个部分的结束位置
            next_section = content.find('<section', taiwan_section_start + 100)
            if next_section == -1:
                next_section = content.find('</body>', taiwan_section_start)
            
            taiwan_section = content[taiwan_section_start:next_section]
            
            # 修改FAQ卡片样式，添加蓝色背景
            taiwan_section = re.sub(
                r'(<div class="faq-item" style="[^"]*?)">',
                r'\1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">',
                taiwan_section
            )
            
            # 修改问题的样式：白色文字，居中，蓝色背景
            taiwan_section = re.sub(
                r'<div class="faq-question" style="[^"]*?">',
                '<div class="faq-question" style="display: flex; justify-content: center; align-items: center; cursor: pointer; font-weight: 600; font-size: 18px; color: #ffffff; padding: 20px;">',
                taiwan_section
            )
            
            # 修改+号的样式：白色，有适当的左边距
            taiwan_section = re.sub(
                r'<span class="faq-icon" style="[^"]*?">',
                '<span class="faq-icon" style="font-size: 28px; margin-left: 15px; color: #ffffff; font-weight: bold; transition: transform 0.3s;">',
                taiwan_section
            )
            
            # 修改答案的样式：白色文字
            taiwan_section = re.sub(
                r'<div class="faq-answer" style="[^"]*?">',
                '<div class="faq-answer" style="margin-top: 0; padding: 0 20px 20px 20px; color: #ffffff; line-height: 1.8; background: rgba(255, 255, 255, 0.1); border-radius: 0 0 12px 12px;">',
                taiwan_section
            )
            
            # 重新组合内容
            content = content[:taiwan_section_start] + taiwan_section + content[next_section:]
        
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
    
    print("🎨 开始为台灣用戶常見問題添加蓝色背景...")
    print("=" * 80)
    
    lang_dir = root_dir / 'zh-TW'
    
    if not lang_dir.exists():
        print(f"  ⚠️ 目录不存在: {lang_dir}")
        return
    
    lang_files = list(lang_dir.glob('*-v3.html'))
    lang_files = [f for f in lang_files if 'test' not in f.name and 'backup' not in f.name]
    
    print(f"  找到 {len(lang_files)} 个页面")
    
    fixed_count = 0
    for i, file_path in enumerate(lang_files, 1):
        if fix_taiwan_faq_complete(file_path):
            fixed_count += 1
        if i % 10 == 0:
            print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
    
    print(f"\n  ✅ 完成: {fixed_count}个页面")
    print("\n" + "=" * 80)
    print("🎉 样式修复完成！")
    print("=" * 80)
    print("\n修复内容：")
    print("  1. ✅ FAQ卡片添加漂亮的蓝紫渐变背景")
    print("  2. ✅ 问题文字和+号都是白色")
    print("  3. ✅ 内容居中显示")
    print("  4. ✅ 答案文字也是白色")
    print("  5. ✅ 添加圆角和阴影效果")
    print("\n请刷新本地文件查看效果！")

if __name__ == '__main__':
    main()

