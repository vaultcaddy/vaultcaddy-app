#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Title优化脚本 - 批量优化所有页面Title
目标：提升CTR，降低CPC，提高排名
"""

import os
import re
from pathlib import Path

# 高CTR Title优化规则
TITLE_RULES = {
    # 银行页面 - v3版本
    "chase-bank-statement-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>Chase Statement → Excel in 3s | 98% AI Accurate | Free 20 Pages</title>",
        "keywords": ["chase bank statement", "chase to excel", "chase pdf converter"]
    },
    "hsbc-bank-statement-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>HSBC Statement → QuickBooks/Excel | 3-Second AI | Try Free</title>",
        "keywords": ["hsbc bank statement", "hsbc to excel", "hsbc quickbooks"]
    },
    "bank-of-america-statement-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>Bank of America Statement → Excel | 98% Accurate | $5.59/mo</title>",
        "keywords": ["bank of america statement", "boa to excel"]
    },
    "dbs-bank-statement-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>DBS Statement → Excel/QuickBooks | 3s AI Processing | Free Trial</title>",
        "keywords": ["dbs bank statement", "dbs singapore"]
    },
    "wells-fargo-statement-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>Wells Fargo Statement → Excel | AI Converter | 20 Pages Free</title>",
        "keywords": ["wells fargo statement", "wells fargo to excel"]
    },
    
    # 博客文章
    "blog/bank-statement-automation-guide-2025.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>Bank Statement Automation 2025 | Save 20 Hours/Month | 98% Accurate</title>",
        "keywords": ["bank statement automation", "automate bank statement"]
    },
    "blog/hsbc-bank-statement-to-excel-guide-2025.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>HSBC Statement to Excel Guide 2025 | 3 Methods Compared | Free Tool</title>",
        "keywords": ["hsbc statement to excel", "convert hsbc to excel"]
    },
    
    # 行业解决方案
    "restaurant-accounting-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>Restaurant Accounting Software | Save $6K/Year | AI Automation</title>",
        "keywords": ["restaurant accounting", "restaurant bookkeeping"]
    },
    "ecommerce-accounting-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>E-commerce Accounting | Multi-Platform Reconciliation | Try Free</title>",
        "keywords": ["ecommerce accounting", "online store accounting"]
    },
    "travel-agency-accounting-v3.html": {
        "old_pattern": r"<title>.*?</title>",
        "new_title": "<title>Travel Agency Accounting | Commission Tracking | Free Trial</title>",
        "keywords": ["travel agency accounting", "travel bookkeeping"]
    }
}

# Meta Description优化
META_DESCRIPTIONS = {
    "chase-bank-statement-v3.html": 
        '<meta name="description" content="Convert Chase bank statements to Excel/QuickBooks in 3 seconds with 98% AI accuracy. Trusted by 500+ businesses. Try 20 pages free—no credit card required. $5.59/month.">',
    
    "hsbc-bank-statement-v3.html":
        '<meta name="description" content="HSBC statement converter. AI-powered processing in 3 seconds, 98% accurate. Export to Excel, QuickBooks, Xero. Free 20-page trial. No credit card needed.">',
    
    "blog/bank-statement-automation-guide-2025.html":
        '<meta name="description" content="Complete guide to bank statement automation. Save 20 hours/month with AI. 98% accuracy, $6,000+/year savings. 500+ businesses automated. Start free trial.">',
}

def optimize_title(file_path, title_config):
    """优化单个文件的Title"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换Title
        new_content = re.sub(
            title_config['old_pattern'],
            title_config['new_title'],
            content,
            count=1,
            flags=re.DOTALL
        )
        
        # 检查是否修改
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, title_config['new_title']
        return False, "未修改"
        
    except Exception as e:
        return False, f"错误: {str(e)}"

def optimize_meta_description(file_path, meta_desc):
    """优化Meta Description"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找并替换Meta Description
        pattern = r'<meta name="description"[^>]*>'
        if re.search(pattern, content):
            new_content = re.sub(pattern, meta_desc, content, count=1)
        else:
            # 如果没有，在</title>后插入
            new_content = content.replace('</title>', f'</title>\n    {meta_desc}')
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
        
    except Exception as e:
        print(f"错误: {file_path} - {str(e)}")
        return False

def main():
    print("=" * 80)
    print("🚀 SEO Title优化脚本")
    print("=" * 80)
    print()
    
    base_dir = Path("/Users/cavlinyeung/ai-bank-parser")
    
    total_files = len(TITLE_RULES)
    optimized_count = 0
    
    # 优化Title
    print("📝 开始优化Title标签...")
    print()
    
    for filename, config in TITLE_RULES.items():
        file_path = base_dir / filename
        
        if file_path.exists():
            success, result = optimize_title(file_path, config)
            
            if success:
                optimized_count += 1
                print(f"✅ {filename}")
                print(f"   新Title: {config['new_title'][7:-8]}")  # 去掉<title>标签
                print(f"   关键词: {', '.join(config['keywords'])}")
            else:
                print(f"⚠️  {filename}: {result}")
        else:
            print(f"❌ 文件不存在: {filename}")
        
        print()
    
    # 优化Meta Description
    print("\n📝 开始优化Meta Description...")
    print()
    
    meta_optimized = 0
    for filename, meta_desc in META_DESCRIPTIONS.items():
        file_path = base_dir / filename
        
        if file_path.exists():
            if optimize_meta_description(file_path, meta_desc):
                meta_optimized += 1
                print(f"✅ {filename} - Meta Description已优化")
        else:
            print(f"❌ 文件不存在: {filename}")
    
    print()
    print("=" * 80)
    print("📊 优化完成统计")
    print("=" * 80)
    print(f"总文件数: {total_files}")
    print(f"Title已优化: {optimized_count}")
    print(f"Meta Description已优化: {meta_optimized}")
    print(f"成功率: {(optimized_count/total_files)*100:.1f}%")
    print()
    print("💡 下一步:")
    print("   1. 在Google Search Console提交已优化的URL")
    print("   2. 等待1-2周观察排名变化")
    print("   3. 预期CTR提升30-50%")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
