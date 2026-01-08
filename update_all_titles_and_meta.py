#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有页面的 title 和 meta description 中的价格
"""

import os
import re
from pathlib import Path

# 价格配置
PRICING_CONFIG = {
    'zh': {
        'from_text': '從 $28/月起',
        'lowest_text': '低至 $22/月'
    },
    'en': {
        'from_text': 'From $3.88/month',
        'lowest_text': 'From $2.88/month'
    },
    'jp': {
        'from_text': '月額 $2.88〜',
        'lowest_text': '月額 $2.88〜'
    },
    'kr': {
        'from_text': '월 $2.88부터',
        'lowest_text': '월 $2.88부터'
    }
}

def detect_language(filepath):
    """检测文件语言"""
    if '/en/' in filepath or filepath.startswith('en/'):
        return 'en'
    elif '/jp/' in filepath or filepath.startswith('jp/'):
        return 'jp'
    elif '/kr/' in filepath or filepath.startswith('kr/'):
        return 'kr'
    else:
        return 'zh'

def update_title_and_meta(content, lang):
    """更新 title 和 meta description 中的价格"""
    config = PRICING_CONFIG[lang]
    original_content = content
    updated = False
    
    if lang == 'zh':
        # 更新 <title> 中的价格
        content = re.sub(
            r'從\s*\$?\s*\d+/月起|低至\s*\$?\s*\d+/月|月費.*?\$?\s*\d+',
            config['from_text'],
            content
        )
        
        # 更新 meta description 中的价格
        content = re.sub(
            r'從\s*\$?\s*\d+/月起|低至\s*\$?\s*\d+/月|月費.*?\$?\s*\d+',
            config['from_text'],
            content
        )
        
        # 更新 og:title 和 og:description
        content = re.sub(
            r'從\s*\$?\s*\d+/月起|低至\s*\$?\s*\d+/月|月費.*?\$?\s*\d+',
            config['from_text'],
            content
        )
        
    elif lang == 'en':
        # 更新 <title> 中的价格
        content = re.sub(
            r'From\s*\$?\s*\d+\.?\d*/month|monthly.*?\$?\s*\d+\.?\d*',
            config['from_text'],
            content
        )
        
        # 更新 meta description 中的价格
        content = re.sub(
            r'From\s*\$?\s*\d+\.?\d*/month|monthly.*?\$?\s*\d+\.?\d*',
            config['from_text'],
            content
        )
        
        # 更新 og:title 和 og:description
        content = re.sub(
            r'From\s*\$?\s*\d+\.?\d*/month|monthly.*?\$?\s*\d+\.?\d*',
            config['from_text'],
            content
        )
    
    if content != original_content:
        updated = True
    
    return content, updated

def update_file(filepath):
    """更新单个文件"""
    lang = detect_language(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content, updated = update_title_and_meta(content, lang)
        
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
            
    except Exception as e:
        print(f"❌ 错误 {filepath}: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path('.')
    
    # 查找所有 HTML 文件
    html_files = []
    for html_file in base_dir.rglob('*.html'):
        # 排除 node_modules 和备份文件
        if 'node_modules' not in str(html_file) and 'backup' not in str(html_file):
            html_files.append(html_file)
    
    print(f"📋 找到 {len(html_files)} 个 HTML 文件\n")
    
    updated_count = 0
    for filepath in html_files:
        if update_file(str(filepath)):
            print(f"✅ 已更新: {filepath}")
            updated_count += 1
    
    print(f"\n✅ 完成！共更新 {updated_count} 个文件的 title 和 meta description")

if __name__ == '__main__':
    main()

