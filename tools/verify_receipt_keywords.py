#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证所有银行页面是否包含收据关键词"""

import glob
import re

def check_file(file_path):
    """检查单个文件的SEO标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检测语言
        lang = 'zh'
        if '/en/' in file_path:
            lang = 'en'
        elif '/ja/' in file_path:
            lang = 'ja'
        elif '/kr/' in file_path:
            lang = 'kr'
        
        # 检查title
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else ''
        
        # 检查description
        desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
        description = desc_match.group(1) if desc_match else ''
        
        # 检查是否包含收据关键词
        receipt_keywords = {
            'zh': ['收據', 'receipt'],
            'en': ['Receipt', 'receipt'],
            'ja': ['領収書', 'レシート'],
            'kr': ['영수증', 'receipt']
        }
        
        has_receipt_in_title = any(kw in title for kw in receipt_keywords.get(lang, []))
        has_receipt_in_desc = any(kw in description for kw in receipt_keywords.get(lang, []))
        
        return {
            'lang': lang,
            'title': title[:80],
            'has_receipt_title': has_receipt_in_title,
            'has_receipt_desc': has_receipt_in_desc,
            'both_ok': has_receipt_in_title and has_receipt_in_desc
        }
    except Exception as e:
        return {'error': str(e)}

# 获取所有银行页面
patterns = [
    '*-bank-statement.html',
    'en/*-bank-statement.html',
    'ja/*-bank-statement.html',
    'kr/*-bank-statement.html',
]

all_files = []
for pattern in patterns:
    all_files.extend(glob.glob(pattern))

all_files = list(set(all_files))
all_files.sort()

print("=" * 70)
print("🔍 验证收据关键词")
print("=" * 70)
print()

ok_count = 0
missing_title = []
missing_desc = []
missing_both = []

for file_path in all_files:
    result = check_file(file_path)
    
    if result.get('both_ok'):
        ok_count += 1
    else:
        if not result.get('has_receipt_title'):
            missing_title.append(file_path)
        if not result.get('has_receipt_desc'):
            missing_desc.append(file_path)
        if not result.get('has_receipt_title') and not result.get('has_receipt_desc'):
            missing_both.append(file_path)

print(f"✅ 完全符合：{ok_count}/{len(all_files)} 个文件")
print()

if missing_both:
    print(f"⚠️  Title和Description都缺少收据：{len(missing_both)} 个")
    for f in missing_both[:5]:
        print(f"   - {f}")
    print()

if missing_title and len(missing_title) > len(missing_both):
    print(f"⚠️  Title缺少收据：{len(missing_title) - len(missing_both)} 个")
    for f in set(missing_title) - set(missing_both):
        if f in all_files[:3]:
            print(f"   - {f}")
    print()

if missing_desc and len(missing_desc) > len(missing_both):
    print(f"⚠️  Description缺少收据：{len(missing_desc) - len(missing_both)} 个")
    for f in set(missing_desc) - set(missing_both):
        if f in all_files[:3]:
            print(f"   - {f}")

print("=" * 70)
print("验证完成")
print("=" * 70)

