#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 修复台灣用戶常見問題的+号样式
1. 改为白色
2. 居中显示
"""

import os
import re
from pathlib import Path

def fix_taiwan_faq_style(file_path):
    """修复台灣用戶常見問題的+号样式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 查找台灣用戶常見問題部分
        taiwan_section_start = content.find('❓ 台灣用戶常見問題')
        
        if taiwan_section_start > 0:
            # 找到这个部分的结束位置（下一个section或文件末尾）
            next_section = content.find('<section', taiwan_section_start + 100)
            if next_section == -1:
                next_section = content.find('</body>', taiwan_section_start)
            
            taiwan_section = content[taiwan_section_start:next_section]
            
            # 修改这个部分的FAQ样式
            # 1. 将+号颜色改为白色
            taiwan_section = taiwan_section.replace(
                'color: #2d3748;',
                'color: #ffffff;'
            )
            
            # 2. 修改faq-question的布局，让+号居中
            # 查找并替换display: flex的样式
            taiwan_section = re.sub(
                r'(<div class="faq-question" style="display: flex;[^"]*?)">',
                lambda m: m.group(0).replace('justify-content: space-between;', 'justify-content: center;'),
                taiwan_section
            )
            
            # 如果+号在span中，添加居中样式
            taiwan_section = re.sub(
                r'(<span class="faq-icon" style="[^"]*?)">',
                lambda m: m.group(0).replace('font-size: 24px;', 'font-size: 24px; margin-left: 15px;') if 'margin-left' not in m.group(0) else m.group(0),
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
    
    print("🎨 开始修复台灣用戶常見問題的+号样式...")
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
            if fix_taiwan_faq_style(file_path):
                fixed_count += 1
            if i % 10 == 0:
                print(f"  进度: {i}/{len(lang_files)} (已修复: {fixed_count})")
        
        print(f"  ✅ 完成: {fixed_count}个页面")
        total_fixed += fixed_count
    
    print("\n" + "=" * 80)
    print(f"🎉 样式修复完成！共修复 {total_fixed} 个页面")
    print("=" * 80)
    print("\n修复内容：")
    print("  1. ✅ +号颜色改为白色（#ffffff）")
    print("  2. ✅ +号位置改为居中")
    print("\n请刷新本地文件查看效果！")

if __name__ == '__main__':
    main()

