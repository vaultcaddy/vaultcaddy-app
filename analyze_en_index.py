#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析英文版首页的结构，找出缺失的部分
"""

import re

print("📊 分析英文版首页结构...")
print("="*70)

with open('en/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找关键部分
sections = {
    'All-in-One': 'All-in-One AI Document Processing Platform',
    'Why Choose': 'Why Choose VaultCaddy',
    'Built for Accountants': 'Built for Accountants',
    'Ultra-Fast': 'Ultra-Fast Processing',
    'Highest Accuracy': 'Highest Accuracy',
    'Fair and Affordable (title)': 'Fair and Affordable',
    'Pricing Badge': 'FAIR AND AFFORDABLE PRICING',
    'Pricing Section': 'Easy Bank Statement Processing',
    'Monthly Plan': 'Monthly',
    'Yearly Plan': 'Yearly',
    'User Reviews': 'VaultCaddy User Reviews',
}

print("\n检查关键部分是否存在:")
for name, keyword in sections.items():
    count = content.count(keyword)
    status = '✓' if count > 0 else '✗ 缺失'
    print(f"  {status} {name}: {count}次")

# 查找"All-in-One"到"User Reviews"之间的主要section标签数量
all_in_one_pos = content.find('All-in-One AI Document Processing Platform')
user_reviews_pos = content.find('VaultCaddy User Reviews')

if all_in_one_pos != -1 and user_reviews_pos != -1:
    between_content = content[all_in_one_pos:user_reviews_pos]
    section_count = between_content.count('<section')
    print(f"\n从'All-in-One'到'User Reviews'之间有 {section_count} 个<section>标签")
    
    # 检查中间是否有具体内容
    if len(between_content) < 5000:
        print(f"⚠️  警告：中间内容太少（{len(between_content)}字符），可能缺失大量内容")
    else:
        print(f"✓ 中间内容长度：{len(between_content)}字符")
else:
    print("\n⚠️  无法定位'All-in-One'和'User Reviews'位置")

print("\n" + "="*70)

