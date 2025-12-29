#!/usr/bin/env python3
"""
Phase 2: 批量生成49个银行页面（基于Chase v3模板）
包含完整内容：How It Works + Use Cases + Comparison + Extended FAQ + Technical Details
"""
import os
import re

print("=" * 70)
print("🚀 Phase 2: 批量生成49个银行页面")
print("=" * 70)
print("\n📋 基于模板: chase-bank-statement-v3.html")
print("📝 包含内容: 1,850+ words, 10 FAQ, 3 cases, 教程, 对比表")
print()

# 读取模板
with open('chase-bank-statement-v3.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 定义所有银行数据（Batch 1: 美国9个）
banks = [
    {
        'name': 'Bank of America',
        'code': 'bank-of-america',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Advantage Checking, Savings, Credit Cards, Business accounts',
        'specific_features': 'Zelle integration, Mobile Check Deposit, Bill Pay',
    },
    {
        'name': 'Wells Fargo',
        'code': 'wells-fargo',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Everyday Checking, Way2Save Savings, Credit Cards, Business accounts',
        'specific_features': 'Wells Fargo Online, Mobile Banking, ATM Deposit',
    },
    {
        'name': 'Citibank',
        'code': 'citibank',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Citi Checking, Savings, Citi Credit Cards, Business accounts',
        'specific_features': 'Global presence, Multi-currency accounts, International wire',
    },
    {
        'name': 'Capital One',
        'code': 'capital-one',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': '360 Checking, 360 Savings, Credit Cards, Business Banking',
        'specific_features': 'No fees, High-yield savings, 24/7 customer service',
    },
    {
        'name': 'US Bank',
        'code': 'us-bank',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Smartly Checking, Savings, Credit Cards, Business accounts',
        'specific_features': 'Mobile Banking, ATM access, Bill Pay',
    },
    {
        'name': 'PNC Bank',
        'code': 'pnc-bank',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Virtual Wallet, Savings, Credit Cards, Business accounts',
        'specific_features': 'Virtual Wallet app, Spending zone, Growth zone',
    },
    {
        'name': 'TD Bank',
        'code': 'td-bank',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Convenience Checking, Savings, Credit Cards, Business accounts',
        'specific_features': 'Extended hours, 7-day banking, Mobile deposit',
    },
    {
        'name': 'Truist Bank',
        'code': 'truist-bank',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Confidence Checking, Savings, Credit Cards, Business accounts',
        'specific_features': 'Digital banking, Mobile app, ATM network',
    },
    {
        'name': 'Ally Bank',
        'code': 'ally-bank',
        'country': 'USA',
        'region': 'United States',
        'currency': 'USD',
        'currency_symbol': '$',
        'monthly_price': '5.59',
        'annual_price': '46',
        'annual_original': '67.08',
        'extra_page': '0.06',
        'account_types': 'Interest Checking, Online Savings, CDs, Business accounts',
        'specific_features': 'Online-only, No fees, High interest rates',
    },
]

print(f"📊 Batch 1: US Banks = {len(banks)}")
print(f"📁 Template size: {len(template):,} characters")
print()

# 开始生成
success_count = 0
for i, bank in enumerate(banks, 1):
    print(f"\n{'='*70}")
    print(f"🏦 Bank {i}/9: {bank['name']}")
    print(f"{'='*70}")
    
    # 复制模板
    content = template
    
    # 替换所有Chase相关内容
    replacements = {
        'Chase Bank USA': bank['name'],
        'Chase Bank': bank['name'],
        'Chase': bank['name'],
        'chase-bank-statement-v2.html': f"{bank['code']}-statement-v3.html",
        'chase-og-image.jpg': f"{bank['code']}-og-image.jpg",
        'Chase Total Checking, Chase Savings, Chase Business Complete Banking, Chase Credit Cards (Sapphire, Freedom, Ink), Chase Private Client accounts, and Chase First Banking': bank['account_types'],
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # 写入文件
    filename = f"{bank['code']}-statement-v3.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    success_count += 1
    print(f"  ✅ Created: {filename}")
    print(f"  📄 Size: {len(content):,} characters")
    print(f"  💰 Pricing: ${bank['monthly_price']}/month, ${bank['annual_price']}/year")
    print(f"  🌍 Region: {bank['region']}")

print(f"\n{'='*70}")
print(f"🎉 Batch 1 Complete! US Banks")
print(f"{'='*70}")
print(f"\n✅ Successfully generated: {success_count}/9 bank pages")
print(f"📊 Each page: ~1,850 words, 10 FAQ, 3 cases")
print(f"⏭️  Next: Batch 2 (UK 5 banks)")
print(f"\n⏸️  Taking a 10-second break before Batch 2...")
