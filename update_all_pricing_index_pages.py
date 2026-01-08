#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有 index.html 和 landing page 的价格
根据方案4双层定价更新价格信息
"""

import os
import re
from pathlib import Path

# 价格配置
PRICING_CONFIG = {
    'zh': {
        'starter_monthly': '28',
        'starter_yearly': '22',
        'pro_monthly': '118',
        'pro_yearly': '93',
        'overage': '0.3',
        'currency': 'HKD $',
        'currency_symbol': '$',
        'monthly_text': '/月',
        'yearly_text': '/月',
        'yearly_save': '（省20%）',
        'overage_text': '超出 $0.3/頁',
        'starter_name': 'Starter 入門版',
        'pro_name': 'Pro Unlimited'
    },
    'en': {
        'starter_monthly': '3.88',
        'starter_yearly': '2.88',
        'pro_monthly': '14.99',
        'pro_yearly': '11.99',
        'overage': '0.038',
        'currency': 'USD $',
        'currency_symbol': '$',
        'monthly_text': '/month',
        'yearly_text': '/month',
        'yearly_save': '(Save 20%)',
        'overage_text': 'Then $0.038/page',
        'starter_name': 'Starter',
        'pro_name': 'Pro Unlimited'
    },
    'jp': {
        'starter_monthly': '599',
        'starter_yearly': '479',
        'pro_monthly': '2348',
        'pro_yearly': '1878',
        'overage': '6',
        'currency': 'JPY ¥',
        'currency_symbol': '¥',
        'monthly_text': '/月',
        'yearly_text': '/月',
        'yearly_save': '（省20%）',
        'overage_text': '超過後1ページ ¥6',
        'starter_name': 'Starter 入門版',
        'pro_name': 'Pro Unlimited'
    },
    'kr': {
        'starter_monthly': '5,588',
        'starter_yearly': '4,468',
        'pro_monthly': '21,699',
        'pro_yearly': '17,359',
        'overage': '55',
        'currency': 'KRW ₩',
        'currency_symbol': '₩',
        'monthly_text': '/월',
        'yearly_text': '/월',
        'yearly_save': '（省20%）',
        'overage_text': '초과 시 페이지당 ₩55',
        'starter_name': 'Starter 입문판',
        'pro_name': 'Pro Unlimited'
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

def update_index_html(filepath):
    """更新 index.html 文件的价格"""
    lang = detect_language(filepath)
    config = PRICING_CONFIG[lang]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 更新超出后每页价格
        if lang == 'zh':
            # 中文：超出 $0.3/頁
            content = re.sub(
                r'超出\s*\$?0?\.?5/頁',
                f'超出 {config["currency_symbol"]}{config["overage"]}/頁',
                content
            )
            content = re.sub(
                r'超出後每頁\s*\$?0?\.?5',
                f'超出後每頁 {config["currency_symbol"]}{config["overage"]}',
                content
            )
        elif lang == 'en':
            # 英文：Then $0.038/page
            content = re.sub(
                r'Then\s*\$?0?\.?0?5/page',
                f'Then ${config["overage"]}/page',
                content
            )
            content = re.sub(
                r'100 Credits/month \(Then \$0\.05/page\)',
                f'100 Credits/month ({config["overage_text"]})',
                content
            )
        elif lang == 'jp':
            # 日文：超過後1ページ ¥6
            content = re.sub(
                r'超過後1ページあたり¥?\d+',
                config["overage_text"],
                content
            )
        elif lang == 'kr':
            # 韩文：초과 시 페이지당 ₩55
            content = re.sub(
                r'초과 시 페이지당\s*₩?\d+',
                config["overage_text"],
                content
            )
        
        # 更新其他价格提及（在描述、标题等地方）
        if lang == 'zh':
            # 更新标题和描述中的价格
            content = re.sub(
                r'從\s*\$?\d+/月起',
                f'從 {config["currency_symbol"]}{config["starter_monthly"]}/月起',
                content
            )
            content = re.sub(
                r'低至\s*HK\$?0?\.?5',
                f'低至 HK{config["currency_symbol"]}{config["overage"]}',
                content
            )
        elif lang == 'en':
            content = re.sub(
                r'From\s*\$?\d+\.?\d*/month',
                f'From ${config["starter_monthly"]}/month',
                content
            )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已更新: {filepath}")
            return True
        else:
            print(f"⏭️  无需更新: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ 错误 {filepath}: {e}")
        return False

def main():
    """主函数"""
    base_dir = Path('.')
    
    # 更新所有 index.html
    index_files = [
        'index.html',
        'en/index.html',
        'jp/index.html',
        'kr/index.html'
    ]
    
    updated_count = 0
    for index_file in index_files:
        filepath = base_dir / index_file
        if filepath.exists():
            if update_index_html(str(filepath)):
                updated_count += 1
    
    print(f"\n✅ 完成！共更新 {updated_count} 个文件")
    print("\n📝 注意：")
    print("1. 日文和韩文版的 index.html 需要手动更新为双层定价结构（Starter 和 Pro Unlimited）")
    print("2. Landing pages (v1, v2, v3) 需要单独更新")
    print("3. 学习中心页面需要单独更新")

if __name__ == '__main__':
    main()

