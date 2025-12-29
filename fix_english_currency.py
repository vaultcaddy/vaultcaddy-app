#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修正英文版 SEO 文章的货币标注
将 HKD 改为 USD，并更新正确的美元价格
"""

import os
import re

# 英文版价格
USD_MONTHLY = "$5.59"
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

# 货币替换规则
REPLACEMENTS = [
    # 月费价格
    (r'HK\$69', USD_MONTHLY),
    (r'\$69', USD_MONTHLY),
    (r'HK\$69/month', f'{USD_MONTHLY}/month'),
    (r'\$69/month', f'{USD_MONTHLY}/month'),
    
    # 额外页面价格
    (r'HK\$0\.60/page', f'{USD_PER_PAGE}/page'),
    (r'\$0\.60/page', f'{USD_PER_PAGE}/page'),
    (r'HK\$0\.60 per page', f'{USD_PER_PAGE} per page'),
    (r'\$0\.60 per page', f'{USD_PER_PAGE} per page'),
    
    # 100页套餐
    (r'HK\$69/mo \(100 pages\)', f'{USD_MONTHLY}/mo (100 pages)'),
    (r'\$69/mo \(100 pages\)', f'{USD_MONTHLY}/mo (100 pages)'),
    
    # 年费计算 (HK$828 → $67.08)
    (r'HK\$828', '$67.08'),
    (r'\$828/year', '$67.08/year'),
    (r'\$828 per year', '$67.08 per year'),
    
    # 常见价格转换
    (r'HK\$1,000', '$130'),
    (r'HK\$5,000', '$650'),
    (r'HK\$10,000', '$1,300'),
    (r'HK\$20,000', '$2,600'),
    (r'HK\$50,000', '$6,500'),
    (r'HK\$100,000', '$13,000'),
    
    # 货币符号通用替换
    (r'HK\$', '$'),
    (r'HKD', 'USD'),
    (r'Hong Kong Dollar', 'US Dollar'),
    (r'Hong Kong dollars', 'US dollars'),
]

def fix_currency_in_file(file_path):
    """修正单个文件的货币标注"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # 应用所有替换规则
        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                changes_made += content.count(re.findall(pattern, content)[0]) if re.findall(pattern, content) else 0
                content = new_content
        
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
    print("="*60)
    print("🔧 批量修正英文版 SEO 文章的货币标注")
    print("="*60)
    print(f"📝 目标: 将 HKD 改为 USD")
    print(f"💰 新价格: {USD_MONTHLY}/month, {USD_PER_PAGE}/page")
    print("="*60)
    
    success_count = 0
    fail_count = 0
    total_changes = 0
    
    for article in ARTICLES:
        file_path = os.path.join("/Users/cavlinyeung/ai-bank-parser", article)
        
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {article}")
            fail_count += 1
            continue
        
        print(f"\n处理: {article}")
        success, changes = fix_currency_in_file(file_path)
        
        if success:
            print(f"✅ 成功修正 (变更: {changes}处)")
            success_count += 1
            total_changes += changes
        else:
            print(f"ℹ️  无需修改 (已是正确格式)")
    
    print("\n" + "="*60)
    print("📊 修正完成统计")
    print("="*60)
    print(f"✅ 成功修正: {success_count}/{len(ARTICLES)} 篇")
    print(f"📝 总变更数: {total_changes} 处")
    if fail_count > 0:
        print(f"❌ 失败: {fail_count} 篇")
    print("="*60)
    print("🎉 货币标注修正完成!")
    print("="*60)

if __name__ == "__main__":
    main()

