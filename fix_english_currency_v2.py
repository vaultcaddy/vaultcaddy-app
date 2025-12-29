#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修正英文版 SEO 文章的货币标注 V2
将所有价格改为正确的美元价格
"""

import os
import re

# 英文版正确价格
USD_BASE = "$5.59"
USD_PER_PAGE = "$0.06"

# 需要处理的9篇文章
ARTICLES = [
    "en/blog/vaultcaddy-vs-dext-comparison-2025.html",
    "en/blog/how-to-convert-bank-statements-to-excel-2025.html",
    "en/blog/top-10-accounting-software-2025.html",
    "en/blog/vaultcaddy-vs-expensify-comparison-2025.html",
    "en/blog/pdf-bank-statement-cannot-copy-text-solutions-2025.html",
    "en/blog/quickbooks-import-bank-statement-error-fix-2025.html",
    "en/blog/vaultcaddy-vs-quickbooks-comparison-2025.html",
    "en/blog/restaurant-accounting-system-guide-2025.html",
    "en/blog/manual-data-entry-vs-ai-automation-2025.html",
]

def fix_currency_in_file(file_path):
    """修正单个文件的货币标注"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替换规则（按顺序执行，从具体到一般）
        replacements = [
            # VaultCaddy 基础价格 ($46 → $5.59)
            (r'\$46/month \(100 pages\)', f'{USD_BASE}/month (100 pages)'),
            (r'\$46/mo \(100 pages\)', f'{USD_BASE}/mo (100 pages)'),
            (r'\$46 per month \(100 pages\)', f'{USD_BASE} per month (100 pages)'),
            (r'\$46/month', f'{USD_BASE}/month'),
            (r'\$46/mo', f'{USD_BASE}/mo'),
            (r'\$46 per month', f'{USD_BASE} per month'),
            
            # 150页价格 ($96 → $8.59: $5.59 + 50×$0.06)
            (r'\$96/month \(150 pages\)', '$8.59/month (150 pages)'),
            (r'\$96/mo \(150 pages\)', '$8.59/mo (150 pages)'),
            (r'\$96 per month', '$8.59 per month'),
            (r'\$96/month', '$8.59/month'),
            (r'\$96/mo', '$8.59/mo'),
            
            # 200页价格 ($128 → $11.59: $5.59 + 100×$0.06)
            (r'\$128/month \(200 pages\)', '$11.59/month (200 pages)'),
            (r'\$128/mo \(200 pages\)', '$11.59/mo (200 pages)'),
            (r'\$128 per month', '$11.59 per month'),
            (r'\$128/month', '$11.59/month'),
            (r'\$128/mo', '$11.59/mo'),
            
            # 300页价格 ($196 → $17.59: $5.59 + 200×$0.06)
            (r'\$196/month \(300 pages\)', '$17.59/month (300 pages)'),
            (r'\$196/mo \(300 pages\)', '$17.59/mo (300 pages)'),
            (r'\$196 per month', '$17.59 per month'),
            (r'\$196/month', '$17.59/month'),
            (r'\$196/mo', '$17.59/mo'),
            
            # 500页价格 ($336 → $29.59: $5.59 + 400×$0.06)
            (r'\$336/month \(500 pages\)', '$29.59/month (500 pages)'),
            (r'\$336/mo \(500 pages\)', '$29.59/mo (500 pages)'),
            (r'\$336 per month', '$29.59 per month'),
            (r'\$336/month', '$29.59/month'),
            (r'\$336/mo', '$29.59/mo'),
            
            # 年费 ($552 → $67.08: $5.59×12)
            (r'\$552/year', '$67.08/year'),
            (r'\$552 per year', '$67.08 per year'),
            (r'\$552 annually', '$67.08 annually'),
            
            # 额外页面价格
            (r'\$0\.70/page', f'{USD_PER_PAGE}/page'),
            (r'\$0\.70 per page', f'{USD_PER_PAGE} per page'),
            
            # 其他常见价格转换（基于 HKD→USD 汇率 1:0.13）
            (r'\$1,152/year', '$149.76/year'),
            (r'\$2,304/year', '$299.52/year'),
            (r'\$4,032/year', '$523.92/year'),
            
            # HKD相关
            (r'HK\$69', USD_BASE),
            (r'HK\$', '$'),
            (r'HKD', 'USD'),
            (r'Hong Kong Dollar', 'US Dollar'),
            (r'Hong Kong dollars', 'US dollars'),
        ]
        
        changes_made = 0
        for pattern, replacement in replacements:
            matches = re.findall(pattern, content)
            if matches:
                changes_made += len(matches)
                content = re.sub(pattern, replacement, content)
        
        # 只有在有变化时才写入
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        return False, 0
        
    except Exception as e:
        print(f"❌ 错误处理 {file_path}: {e}")
        return False, 0

def main():
    print("="*70)
    print("🔧 批量修正英文版 SEO 文章的货币标注 V2")
    print("="*70)
    print(f"📝 修正目标:")
    print(f"   • $46/month → {USD_BASE}/month")
    print(f"   • $96/month → $8.59/month (150 pages)")
    print(f"   • $128/month → $11.59/month (200 pages)")
    print(f"   • 额外页面: {USD_PER_PAGE}/page")
    print("="*70)
    
    success_count = 0
    total_changes = 0
    modified_files = []
    
    for article in ARTICLES:
        file_path = os.path.join("/Users/cavlinyeung/ai-bank-parser", article)
        
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {article}")
            continue
        
        print(f"\n处理: {os.path.basename(article)}")
        success, changes = fix_currency_in_file(file_path)
        
        if success:
            print(f"   ✅ 成功修正 {changes} 处价格")
            success_count += 1
            total_changes += changes
            modified_files.append(os.path.basename(article))
        else:
            print(f"   ℹ️  无需修改")
    
    print("\n" + "="*70)
    print("📊 修正完成统计")
    print("="*70)
    print(f"✅ 成功修正: {success_count}/{len(ARTICLES)} 篇")
    print(f"📝 总变更数: {total_changes} 处")
    
    if modified_files:
        print(f"\n修改的文件:")
        for f in modified_files:
            print(f"   • {f}")
    
    print("="*70)
    print("🎉 货币标注修正完成!")
    print(f"💰 新价格: {USD_BASE}/month (100 pages), {USD_PER_PAGE}/page")
    print("="*70)

if __name__ == "__main__":
    main()

