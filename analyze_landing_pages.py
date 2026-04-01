#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析现有landing page，为创建对比版本做准备"""

import glob
import os

def analyze_pages():
    """分析所有现有的landing page"""
    
    # 1. 银行页面
    bank_patterns = [
        '*-bank-statement.html',
        'en/*-bank-statement.html',
        'jp/*-bank-statement.html',
        'kr/*-bank-statement.html',
    ]
    
    bank_pages = []
    for pattern in bank_patterns:
        bank_pages.extend(glob.glob(pattern))
    
    # 2. 行业解决方案页面
    solution_patterns = [
        'solutions/*/index.html',
        'en/solutions/*/index.html',
        'jp/solutions/*/index.html',
        'kr/solutions/*/index.html',
    ]
    
    solution_pages = []
    for pattern in solution_patterns:
        solution_pages.extend(glob.glob(pattern))
    
    # 3. 博客页面（不创建对比版本，博客是教育内容）
    blog_patterns = [
        'blog/*.html',
        'en/blog/*.html',
        'jp/blog/*.html',
        'kr/blog/*.html',
    ]
    
    blog_pages = []
    for pattern in blog_patterns:
        pages = glob.glob(pattern)
        # 排除index.html
        blog_pages.extend([p for p in pages if not p.endswith('index.html')])
    
    # 统计
    print("=" * 70)
    print("📊 现有Landing Page统计")
    print("=" * 70)
    print()
    
    print(f"🏦 银行页面：{len(bank_pages)} 个")
    print(f"   - 中文：{len([p for p in bank_pages if '/' not in p])} 个")
    print(f"   - 英文：{len([p for p in bank_pages if p.startswith('en/')])} 个")
    print(f"   - 日文：{len([p for p in bank_pages if p.startswith('jp/')])} 个")
    print(f"   - 韩文：{len([p for p in bank_pages if p.startswith('kr/')])} 个")
    print()
    
    print(f"💼 行业解决方案：{len(solution_pages)} 个")
    print(f"   - 中文：{len([p for p in solution_pages if p.startswith('solutions/')])} 个")
    print(f"   - 英文：{len([p for p in solution_pages if p.startswith('en/solutions/')])} 个")
    print(f"   - 日文：{len([p for p in solution_pages if p.startswith('jp/solutions/')])} 个")
    print(f"   - 韩文：{len([p for p in solution_pages if p.startswith('kr/solutions/')])} 个")
    print()
    
    print(f"📝 博客页面：{len(blog_pages)} 个（不创建对比版本）")
    print()
    
    print("=" * 70)
    print(f"📦 需要创建对比版本的页面总数：{len(bank_pages) + len(solution_pages)} 个")
    print("=" * 70)
    print()
    
    # 详细列表
    print("🏦 银行页面详细列表（中文版示例）：")
    chinese_banks = sorted([p for p in bank_pages if '/' not in p])
    for i, page in enumerate(chinese_banks[:5], 1):
        print(f"   {i}. {page}")
    print(f"   ... （共{len(chinese_banks)}个）")
    print()
    
    print("💼 行业解决方案详细列表（中文版示例）：")
    chinese_solutions = sorted([p for p in solution_pages if p.startswith('solutions/')])
    for i, page in enumerate(chinese_solutions[:5], 1):
        solution_name = page.split('/')[1]
        print(f"   {i}. {solution_name}")
    print(f"   ... （共{len(chinese_solutions)}个）")
    print()
    
    return {
        'bank_pages': bank_pages,
        'solution_pages': solution_pages,
        'total': len(bank_pages) + len(solution_pages)
    }

if __name__ == '__main__':
    result = analyze_pages()
    
    print("=" * 70)
    print("🎯 对比版Landing Page命名规则")
    print("=" * 70)
    print()
    print("原页面：hsbc-bank-statement.html")
    print("新页面：hsbc-vs-manual.html 或 hsbc-comparison.html")
    print()
    print("原页面：solutions/restaurant/index.html")
    print("新页面：solutions/restaurant/comparison.html")
    print()

analyze_pages()
