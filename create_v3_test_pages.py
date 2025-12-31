#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建2个v3测试页面
确保：1. 纯英文  2. 正确定价  3. 正确auth链接
"""

import os
import re
from pathlib import Path

def create_test_pages():
    root_dir = Path('/Users/cavlinyeung/ai-bank-parser')
    
    print("🧪 创建v3测试页面...")
    print("=" * 80)
    
    # 读取v3模板
    template_path = root_dir / 'chase-bank-statement-v3.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        v3_template = f.read()
    
    # 确认v3模板是纯英文且定价正确
    print("\n✅ v3模板检查:")
    lang_check = 'en-US ✅' if 'lang="en-US"' in v3_template else '❌ 未知'
    price_check = '$5.59/month ✅' if '$5.59' in v3_template else '❌ 错误'
    auth_check = '/en/auth.html ✅' if 'href="/en/auth.html"' in v3_template else '/auth.html ⚠️'
    print(f"  - 语言: {lang_check}")
    print(f"  - 定价: {price_check}")
    print(f"  - Auth链接: {auth_check}")
    
    # 测试页面1: chase-bank-statement-v2.html
    test1_source = root_dir / 'chase-bank-statement-v2.html'
    test1_target = root_dir / 'chase-bank-statement-v3-test.html'
    
    print("\n📄 测试页面1: Chase Bank")
    print(f"  源文件: {test1_source.name}")
    print(f"  目标文件: {test1_target.name}")
    
    # 直接复制v3模板（因为都是Chase Bank）
    with open(test1_target, 'w', encoding='utf-8') as f:
        f.write(v3_template)
    print(f"  ✅ 创建成功")
    
    # 测试页面2: restaurant-accounting-v2.html
    # 这个需要修改内容
    test2_source = root_dir / 'restaurant-accounting-v2.html'
    test2_target = root_dir / 'restaurant-accounting-v3-test.html'
    
    print("\n📄 测试页面2: Restaurant Accounting")
    print(f"  源文件: {test2_source.name}")
    print(f"  目标文件: {test2_target.name}")
    
    # 读取v2内容以获取行业特定信息
    with open(test2_source, 'r', encoding='utf-8') as f:
        v2_content = f.read()
    
    # 提取标题
    title_match = re.search(r'<title>(.*?)</title>', v2_content, re.DOTALL)
    if title_match:
        old_title = title_match.group(1)
        # 清理标题，移除中文
        clean_title = re.sub(r'[^\x00-\x7F]+', '', old_title).strip()
        print(f"  原标题: {old_title[:80]}...")
        print(f"  清理后: {clean_title[:80]}...")
    
    # 修改v3模板适配Restaurant
    restaurant_v3 = v3_template.replace('Chase Bank', 'Restaurant')
    restaurant_v3 = restaurant_v3.replace('chase.com', 'restaurant-industry.com')
    restaurant_v3 = restaurant_v3.replace('bank statement', 'financial document')
    restaurant_v3 = restaurant_v3.replace('Bank Statement', 'Financial Document')
    
    # 更新标题
    restaurant_v3 = re.sub(
        r'<title>.*?</title>',
        '<title>Restaurant Accounting Solution | AI Financial Management | VaultCaddy</title>',
        restaurant_v3,
        flags=re.DOTALL
    )
    
    # 更新描述
    restaurant_v3 = re.sub(
        r'<meta name="description" content=".*?">',
        '<meta name="description" content="AI-powered restaurant accounting solution. Automate financial management, invoice processing, and reporting. From $5.59/month | 500+ restaurants trust us">',
        restaurant_v3
    )
    
    with open(test2_target, 'w', encoding='utf-8') as f:
        f.write(restaurant_v3)
    print(f"  ✅ 创建成功")
    
    print("\n" + "=" * 80)
    print("🎉 测试页面创建完成！")
    print("=" * 80)
    print("\n请测试以下页面:")
    print(f"  1. 🏦 https://vaultcaddy.com/{test1_target.name}")
    print(f"  2. 🏢 https://vaultcaddy.com/{test2_target.name}")
    print("\n请检查:")
    print("  ✅ 整页是否完全是英文")
    print("  ✅ 定价是否正确（$5.59/month, $7/month）")
    print("  ✅ 点击按钮是否跳转到 /en/auth.html")
    print("  ✅ FAQ '+' 号是否可以点击展开")
    print("  ✅ 设计是否现代化美观")

if __name__ == '__main__':
    create_test_pages()

