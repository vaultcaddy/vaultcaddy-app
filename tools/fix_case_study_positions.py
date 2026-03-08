#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复5个银行页面的案例section位置"""

from bs4 import BeautifulSoup
import re

print("=" * 70)
print("修复银行页面的案例section位置")
print("=" * 70)
print()

files = [
    'hsbc-bank-statement.html',
    'bankcomm-bank-statement.html',
    'citic-bank-statement.html',
    'dahsing-bank-statement.html',
    'citibank-bank-statement.html'
]

for filename in files:
    print(f"处理: {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份
        with open(f'{filename}.backup_case_fix', 'w', encoding='utf-8') as f:
            f.write(content)
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找案例section（包含"香港中小企業真實案例"的section）
        case_section = None
        for section in soup.find_all('section'):
            if '香港中小企業真實案例' in section.get_text() or '香港中小企成功案例' in section.get_text():
                # 确保这是案例section而不是其他section
                h2_tag = section.find('h2')
                if h2_tag and ('真實案例' in h2_tag.get_text() or '成功案例' in h2_tag.get_text()):
                    case_section = section
                    break
        
        # 查找FAQ section
        faq_section = None
        for section in soup.find_all('section'):
            if 'faq' in section.get('class', []) or '常見問題' in section.get_text():
                h2_tag = section.find('h2')
                if h2_tag and '常見問題' in h2_tag.get_text():
                    faq_section = section
                    break
        
        if case_section and faq_section:
            # 检查案例是否在FAQ之后
            case_index = list(soup.find_all()).index(case_section)
            faq_index = list(soup.find_all()).index(faq_section)
            
            if case_index > faq_index:
                print(f"   ❌ 案例在FAQ之后，需要移动")
                # 从原位置移除
                case_section_copy = case_section.extract()
                # 插入到FAQ之前
                faq_section.insert_before(case_section_copy)
                print(f"   ✅ 已移动案例到FAQ之前")
            elif case_index < faq_index:
                # 检查案例是否在Hero section之前
                hero_section = soup.find('section', class_='hero')
                if hero_section:
                    hero_index = list(soup.find_all()).index(hero_section)
                    if case_index < hero_index:
                        print(f"   ❌ 案例在Hero section之前，需要移动")
                        # 从原位置移除
                        case_section_copy = case_section.extract()
                        # 插入到FAQ之前
                        faq_section.insert_before(case_section_copy)
                        print(f"   ✅ 已移动案例到FAQ之前")
                    else:
                        print(f"   ✅ 案例位置正确（在Hero之后，FAQ之前）")
                else:
                    print(f"   ✅ 案例在FAQ之前")
            
            # 保存
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(soup))
        
        elif case_section:
            print(f"   ⚠️  有案例但没有FAQ section")
        elif faq_section:
            print(f"   ⚠️  有FAQ但没有案例section")
        else:
            print(f"   ⚠️  既没有案例也没有FAQ")
    
    except Exception as e:
        print(f"   ❌ 处理失败: {e}")
    
    print()

print("=" * 70)
print("✅ 所有文件处理完成！")
print("=" * 70)

