#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复resources.html中的银行链接"""

import re

def fix_english_resources():
    """修复英文版resources.html"""
    file_path = 'en/resources.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复英文版的银行链接
    # HSBC
    content = re.sub(
        r'<a href="/en/auth\.html" class="link-card">\s*<strong>🏦 HSBC</strong>',
        '<a href="/en/hsbc-bank-statement.html" class="link-card">\n                        <strong>🏦 HSBC</strong>',
        content
    )
    
    # Citibank (第一个)
    content = re.sub(
        r'<a href="/en/auth\.html" class="link-card">\s*<strong>🏦 Citibank</strong>\s*<small>US Banking Leader',
        '<a href="/en/citibank-bank-statement.html" class="link-card">\n                        <strong>🏦 Citibank</strong>\n                        <small>US Banking Leader',
        content
    )
    
    # Standard Chartered
    content = re.sub(
        r'<a href="/en/auth\.html" class="link-card">\s*<strong>🏦 Standard Chartered</strong>',
        '<a href="/en/sc-bank-statement.html" class="link-card">\n                        <strong>🏦 Standard Chartered</strong>',
        content
    )
    
    # DBS Bank
    content = re.sub(
        r'<a href="/en/auth\.html" class="link-card">\s*<strong>🏦 DBS Bank</strong>',
        '<a href="/en/dbs-bank-statement.html" class="link-card">\n                        <strong>🏦 DBS Bank</strong>',
        content
    )
    
    # Bank of America - 保持auth.html（没有对应页面）
    # JPMorgan Chase - 保持auth.html（没有对应页面）
    
    if content != original:
        with open(file_path + '.backup_bank_links', 'w', encoding='utf-8') as f:
            f.write(original)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    return False

def fix_korean_resources():
    """修复韩文版resources.html"""
    file_path = 'kr/resources.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修复韩文版的银行链接
    # KB국민은행
    content = re.sub(
        r'<a href="/kr/auth\.html" class="link-card">\s*<strong>🏦 KB국민은행</strong>',
        '<a href="/kr/kb-bank-statement.html" class="link-card">\n                        <strong>🏦 KB국민은행</strong>',
        content
    )
    
    # 신한은행
    content = re.sub(
        r'<a href="/kr/auth\.html" class="link-card">\s*<strong>🏦 신한은행</strong>',
        '<a href="/kr/shinhan-bank-statement.html" class="link-card">\n                        <strong>🏦 신한은행</strong>',
        content
    )
    
    # 하나은행
    content = re.sub(
        r'<a href="/kr/auth\.html" class="link-card">\s*<strong>🏦 하나은행</strong>',
        '<a href="/kr/hana-bank-statement.html" class="link-card">\n                        <strong>🏦 하나은행</strong>',
        content
    )
    
    # 우리은행
    content = re.sub(
        r'<a href="/kr/auth\.html" class="link-card">\s*<strong>🏦 우리은행</strong>',
        '<a href="/kr/woori-bank-statement.html" class="link-card">\n                        <strong>🏦 우리은행</strong>',
        content
    )
    
    # NH농협은행
    content = re.sub(
        r'<a href="/kr/auth\.html" class="link-card">\s*<strong>🏦 NH농협은행</strong>',
        '<a href="/kr/nh-bank-statement.html" class="link-card">\n                        <strong>🏦 NH농협은행</strong>',
        content
    )
    
    if content != original:
        with open(file_path + '.backup_bank_links', 'w', encoding='utf-8') as f:
            f.write(original)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    return False

# 执行修复
print("=" * 70)
print("🔧 修复resources.html中的银行链接")
print("=" * 70)
print()

print("1. 修复英文版（en/resources.html）")
if fix_english_resources():
    print("   ✅ 已修复：HSBC, Citibank, Standard Chartered, DBS Bank")
    print("   ⏭️  保留auth.html：Bank of America, JPMorgan Chase（无对应页面）")
else:
    print("   ⏭️  无需修改")

print()
print("2. 修复韩文版（kr/resources.html）")
if fix_korean_resources():
    print("   ✅ 已修复：KB국민은행, 신한은행, 하나은행, 우리은행, NH농협은행")
else:
    print("   ⏭️  无需修改")

print()
print("=" * 70)
print("✅ 修复完成！")
print()
print("📝 下一步：")
print("   1. 检查韩文版是否有对应的银行页面文件")
print("   2. 为日文版创建5个日本银行页面")
print("=" * 70)

