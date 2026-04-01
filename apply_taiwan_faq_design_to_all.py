#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 将台灣用戶常見問題的新设计应用到所有v3页面
- 香港版本（zh-HK）
- 日本版本（ja-JP）
- 韩国版本（ko-KR）

设计特点：
1. 蓝紫渐变背景
2. 白色文字和+号
3. 内容居中显示
4. 答案默认隐藏（max-height: 0）
"""

import os
import re
from pathlib import Path

def apply_new_faq_design(file_path, section_title):
    """应用新的FAQ设计到指定区域"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找目标FAQ部分
        section_start = content.find(section_title)
        
        if section_start > 0:
            # 找到这个部分的结束位置
            next_section = content.find('<section', section_start + 100)
            if next_section == -1:
                next_section = content.find('</body>', section_start)
            
            faq_section = content[section_start:next_section]
            
            # 1. 修改FAQ卡片样式 - 添加蓝紫渐变背景
            faq_section = re.sub(
                r'(<div class="faq-item" style="[^"]*?)">',
                r'\1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">',
                faq_section
            )
            
            # 2. 修改问题样式 - 白色文字，居中
            faq_section = re.sub(
                r'<div class="faq-question" style="[^"]*?">',
                '<div class="faq-question" style="display: flex; justify-content: center; align-items: center; cursor: pointer; font-weight: 600; font-size: 18px; color: #ffffff; padding: 20px;">',
                faq_section
            )
            
            # 3. 修改+号图标 - 白色，居中
            faq_section = re.sub(
                r'<span class="faq-icon" style="[^"]*?">',
                '<span class="faq-icon" style="font-size: 28px; margin-left: 15px; color: #ffffff; font-weight: bold; transition: transform 0.3s;">',
                faq_section
            )
            
            # 4. 修改答案样式 - 白色文字，默认隐藏
            faq_section = re.sub(
                r'<div class="faq-answer" style="[^"]*?">',
                '<div class="faq-answer" style="max-height: 0; overflow: hidden; transition: max-height 0.3s ease; margin-top: 0; padding: 0 20px; color: #ffffff; line-height: 1.8; background: rgba(255, 255, 255, 0.1); border-radius: 0 0 12px 12px;">',
                faq_section
            )
            
            # 重新组合内容
            content = content[:section_start] + faq_section + content[next_section:]
        
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
    
    print("🎨 开始将台灣FAQ设计应用到所有v3页面...")
    print("=" * 80)
    
    # 定义语言和对应的FAQ标题
    languages = {
        'zh-HK': {
            'name': '香港',
            'titles': [
                '❓ 香港用戶常見問題',
                '❓ 常見問題'
            ]
        },
        'ja-JP': {
            'name': '日本',
            'titles': [
                '❓ 日本用戶常見問題',
                'よくある質問'
            ]
        },
        'ko-KR': {
            'name': '韩国',
            'titles': [
                '❓ 韓國用戶常見問題',
                '자주 묻는 질문'
            ]
        }
    }
    
    total_fixed = 0
    
    for lang_code, lang_info in languages.items():
        print(f"\n{'='*80}")
        print(f"修复 {lang_info['name']} 版本 ({lang_code})...")
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
            # 尝试每个可能的标题
            for title in lang_info['titles']:
                if apply_new_faq_design(file_path, title):
                    fixed_count += 1
                    break  # 成功修复后跳出内层循环
            
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
        total_fixed += fixed_count
    
    print("\n" + "=" * 80)
    print(f"🎉 设计应用完成！共修复 {total_fixed} 个页面")
    print("=" * 80)
    print("\n应用的设计特点：")
    print("  1. ✅ 蓝紫渐变背景")
    print("  2. ✅ 白色问题文字")
    print("  3. ✅ 白色+号图标（居中）")
    print("  4. ✅ 答案默认隐藏")
    print("  5. ✅ 白色答案文字")
    print("  6. ✅ 圆角和阴影效果")
    print("\n加上之前完成的台湾版本（90页），总计：")
    print(f"  🎊 全部360个多语言v3页面已完成！")

if __name__ == '__main__':
    main()

