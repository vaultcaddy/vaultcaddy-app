#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 修复FAQ答案初始状态 - 确保未打开时隐藏
"""

import os
import re
from pathlib import Path

def fix_faq_initial_state(file_path):
    """修复FAQ答案的初始状态"""
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
            
            # 修改答案部分，确保初始状态是隐藏的（max-height: 0）
            taiwan_section = re.sub(
                r'<div class="faq-answer" style="[^"]*?">',
                '<div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease; margin-top: 0; padding: 0 20px; color: #ffffff; line-height: 1.8; background: rgba(255, 255, 255, 0.1); border-radius: 0 0 12px 12px;">',
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
    
    print("🔧 开始修复FAQ答案的初始状态...")
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
        if fix_faq_initial_state(file_path):
            fixed_count += 1
        if i % 10 == 0:
            print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
    
    print(f"\n  ✅ 完成: {fixed_count}个页面")
    print("\n" + "=" * 80)
    print("🎉 修复完成！")
    print("=" * 80)
    print("\n修复内容：")
    print("  ✅ 答案初始状态设置为隐藏（max-height: 0）")
    print("  ✅ 添加overflow: hidden确保内容不显示")
    print("  ✅ 添加transition实现平滑动画")
    print("\n请刷新本地文件，答案现在应该默认隐藏！")

if __name__ == '__main__':
    main()

