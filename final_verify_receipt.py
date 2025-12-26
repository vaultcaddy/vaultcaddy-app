#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终验证收据关键词"""

import glob
import re

def check_receipt(file_path):
    """检查单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lang = 'zh'
        if '/en/' in file_path:
            lang = 'en'
        elif '/ja/' in file_path:
            lang = 'ja'
        elif '/kr/' in file_path:
            lang = 'kr'
        
        # 提取title和description
        title_match = re.search(r'<title>(.*?)</title>', content)
        desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
        
        title = title_match.group(1) if title_match else ''
        desc = desc_match.group(1) if desc_match else ''
        
        # 检查收据关键词
        receipt_ok = False
        if lang == 'zh':
            receipt_ok = '收據' in title and '收據' in desc
        elif lang == 'en':
            receipt_ok = 'Receipt' in title and 'receipt' in desc
        elif lang == 'ja':
            receipt_ok = '領収書' in title and '領収書' in desc
        elif lang == 'kr':
            receipt_ok = '영수증' in title and '영수증' in desc
        
        return {
            'ok': receipt_ok,
            'title': title[:80],
            'lang': lang
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}

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

ok_count = 0
by_lang = {'zh': [0, 0], 'en': [0, 0], 'ja': [0, 0], 'kr': [0, 0]}
failed = []

for file_path in all_files:
    result = check_receipt(file_path)
    lang = result.get('lang', 'zh')
    
    by_lang[lang][1] += 1  # total
    
    if result.get('ok'):
        ok_count += 1
        by_lang[lang][0] += 1  # ok
    else:
        failed.append((file_path, result.get('title', '')))

print("=" * 70)
print("🎉 最终验证结果")
print("=" * 70)
print()
print(f"✅ 完全符合：{ok_count}/{len(all_files)} 个文件")
print()
print("各语言统计：")
print(f"  中文版：{by_lang['zh'][0]}/{by_lang['zh'][1]} ✅")
print(f"  英文版：{by_lang['en'][0]}/{by_lang['en'][1]} ✅")
print(f"  日文版：{by_lang['ja'][0]}/{by_lang['ja'][1]} ✅")
print(f"  韩文版：{by_lang['kr'][0]}/{by_lang['kr'][1]} ✅")
print()

if failed:
    print(f"⚠️  仍需处理：{len(failed)} 个文件")
    for fp, title in failed[:5]:
        print(f"   - {fp}")
        print(f"     {title[:60]}...")
else:
    print("🎉 所有文件都已包含收据关键词！")

print()
print("=" * 70)

