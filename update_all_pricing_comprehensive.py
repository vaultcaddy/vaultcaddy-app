#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面更新所有页面的价格信息
包括：landing pages、学习中心、title、meta description
"""

import os
import re
from pathlib import Path

# 价格配置
PRICING_CONFIG = {
    'zh': {
        'monthly': '28',
        'yearly': '22',
        'overage': '0.3',
        'currency': 'HKD',
        'currency_symbol': '$',
        'monthly_text': '$28/月',
        'yearly_text': '$22/月',
        'from_text': '從 $28/月起',
        'lowest_text': '低至 $22/月'
    },
    'en': {
        'monthly': '3.88',
        'yearly': '2.88',
        'overage': '0.038',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_text': '$3.88/month',
        'yearly_text': '$2.88/month',
        'from_text': 'From $3.88/month',
        'lowest_text': 'From $2.88/month'
    },
    'jp': {
        'monthly': '599',
        'yearly': '479',
        'overage': '6',
        'currency': 'JPY',
        'currency_symbol': '¥',
        'monthly_text': '¥599/月',
        'yearly_text': '¥479/月',
        'from_text': '月額 $2.88〜',
        'lowest_text': '月額 $2.88〜'
    },
    'kr': {
        'monthly': '5,588',
        'yearly': '4,468',
        'overage': '55',
        'currency': 'KRW',
        'currency_symbol': '₩',
        'monthly_text': '₩5,588/월',
        'yearly_text': '₩4,468/월',
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

def update_pricing_in_content(content, lang):
    """更新内容中的价格"""
    config = PRICING_CONFIG[lang]
    original_content = content
    
    if lang == 'zh':
        # 更新月付价格
        content = re.sub(
            r'HKD\s*\$?\s*\d+/月|HK\$\s*\d+/月|\$\s*\d+/月',
            f'HKD ${config["monthly"]}/月',
            content
        )
        # 更新年付价格
        content = re.sub(
            r'年付.*?\$?\s*\d+/月|年費.*?\$?\s*\d+/月',
            f'年付僅 ${config["yearly"]}/月',
            content
        )
        # 更新超出后每页
        content = re.sub(
            r'超出.*?\$?\s*0?\.?\d+/頁|超出後.*?\$?\s*0?\.?\d+/頁',
            f'超出後每頁 ${config["overage"]}/頁',
            content
        )
        # 更新标题中的价格
        content = re.sub(
            r'從\s*\$?\s*\d+/月起|低至\s*\$?\s*\d+/月',
            config['from_text'],
            content
        )
        
    elif lang == 'en':
        # 更新月付价格
        content = re.sub(
            r'USD\s*\$?\s*\d+\.?\d*/month|\$\s*\d+\.?\d*/month',
            f'USD ${config["monthly"]}/month',
            content
        )
        # 更新年付价格
        content = re.sub(
            r'Yearly.*?\$?\s*\d+\.?\d*/month|Annual.*?\$?\s*\d+\.?\d*/month',
            f'Yearly: ${config["yearly"]}/month',
            content
        )
        # 更新超出后每页
        content = re.sub(
            r'Then\s*\$?\s*0?\.?\d+/page|overage.*?\$?\s*0?\.?\d+/page',
            f'Then ${config["overage"]}/page',
            content
        )
        # 更新标题中的价格
        content = re.sub(
            r'From\s*\$?\s*\d+\.?\d*/month',
            config['from_text'],
            content
        )
        
    elif lang == 'jp':
        # 更新月付价格
        content = re.sub(
            r'¥\s*\d+,?\d+/月',
            f'¥{config["monthly"]}/月',
            content
        )
        # 更新年付价格
        content = re.sub(
            r'年払い.*?¥\s*\d+,?\d+/月',
            f'年払い ¥{config["yearly"]}/月',
            content
        )
        # 更新超出后每页
        content = re.sub(
            r'超過後.*?¥\s*\d+/頁',
            f'超過後1ページ ¥{config["overage"]}',
            content
        )
        
    elif lang == 'kr':
        # 更新月付价格
        content = re.sub(
            r'₩\s*\d+,?\d+/월',
            f'₩{config["monthly"]}/월',
            content
        )
        # 更新年付价格
        content = re.sub(
            r'연간.*?₩\s*\d+,?\d+/월',
            f'연간 ₩{config["yearly"]}/월',
            content
        )
        # 更新超出后每页
        content = re.sub(
            r'초과.*?₩\s*\d+/頁',
            f'초과 시 페이지당 ₩{config["overage"]}',
            content
        )
    
    return content, content != original_content

def update_title_and_meta(content, lang):
    """更新 title 和 meta description 中的价格"""
    config = PRICING_CONFIG[lang]
    original_content = content
    
    if lang == 'zh':
        # 更新 title 中的价格
        content = re.sub(
            r'從\s*\$?\s*\d+/月起|低至\s*\$?\s*\d+/月',
            config['from_text'],
            content
        )
        # 更新 meta description 中的价格
        content = re.sub(
            r'從\s*\$?\s*\d+/月起|低至\s*\$?\s*\d+/月',
            config['from_text'],
            content
        )
        
    elif lang == 'en':
        # 更新 title 中的价格
        content = re.sub(
            r'From\s*\$?\s*\d+\.?\d*/month',
            config['from_text'],
            content
        )
        # 更新 meta description 中的价格
        content = re.sub(
            r'From\s*\$?\s*\d+\.?\d*/month',
            config['from_text'],
            content
        )
    
    return content, content != original_content

def update_file(filepath):
    """更新单个文件"""
    lang = detect_language(filepath)
    config = PRICING_CONFIG[lang]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updated = False
        
        # 更新内容中的价格
        content, pricing_updated = update_pricing_in_content(content, lang)
        if pricing_updated:
            updated = True
        
        # 更新 title 和 meta 中的价格
        content, meta_updated = update_title_and_meta(content, lang)
        if meta_updated:
            updated = True
        
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
    
    # 查找所有需要更新的文件
    files_to_update = []
    
    # 1. Landing pages (v1, v2, v3)
    for pattern in ['*-v1.html', '*-v2.html', '*-v3.html']:
        files_to_update.extend(base_dir.rglob(pattern))
    
    # 2. Solutions 目录下的 landing pages
    solutions_dir = base_dir / 'solutions'
    if solutions_dir.exists():
        for html_file in solutions_dir.rglob('*.html'):
            if html_file.name != 'index.html':  # 排除 index.html
                files_to_update.append(html_file)
    
    # 3. 学习中心 (blog 目录)
    blog_dir = base_dir / 'blog'
    if blog_dir.exists():
        for html_file in blog_dir.rglob('*.html'):
            files_to_update.append(html_file)
    
    # 4. 其他语言版本的 solutions 和 blog
    for lang_dir in ['en', 'jp', 'kr']:
        lang_path = base_dir / lang_dir
        if lang_path.exists():
            # solutions
            solutions_lang = lang_path / 'solutions'
            if solutions_lang.exists():
                for html_file in solutions_lang.rglob('*.html'):
                    if html_file.name != 'index.html':
                        files_to_update.append(html_file)
            # blog
            blog_lang = lang_path / 'blog'
            if blog_lang.exists():
                for html_file in blog_lang.rglob('*.html'):
                    files_to_update.append(html_file)
    
    # 去重
    files_to_update = list(set(files_to_update))
    
    print(f"📋 找到 {len(files_to_update)} 个文件需要更新\n")
    
    updated_count = 0
    for filepath in files_to_update:
        if update_file(str(filepath)):
            print(f"✅ 已更新: {filepath}")
            updated_count += 1
        else:
            print(f"⏭️  无需更新: {filepath}")
    
    print(f"\n✅ 完成！共更新 {updated_count} 个文件")

if __name__ == '__main__':
    main()

