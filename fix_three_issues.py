#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复3个问题：
1. HSBC居中问题
2. BOC HK银行名称颜色改为黑色
3. 5个银行页面将案例移到FAQ之上
"""

from bs4 import BeautifulSoup
import re

print("=" * 70)
print("开始修复3个问题")
print("=" * 70)
print()

# ============= 问题1: 修复HSBC居中 =============
print("1. 修复 hsbc-bank-statement.html 的居中问题")
print("-" * 70)

with open('hsbc-bank-statement.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('hsbc-bank-statement.html.backup_fix3', 'w', encoding='utf-8') as f:
    f.write(content)

# 检查是否已经有flex布局
if 'display: flex;' in content and '.hero-content' in content:
    print("   ✅ HSBC页面已经有flex布局，无需修复")
else:
    # 需要添加flex布局
    # 找到.hero-content的CSS并添加flex布局
    pattern = r'(\.hero-content\s*\{[^}]*?)(text-align:\s*center;)([^}]*?\})'
    replacement = r'\1display: flex;\n            flex-direction: column;\n            align-items: center;\n            \2\3'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open('hsbc-bank-statement.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("   ✅ 已添加flex布局确保居中")

print()

# ============= 问题2: 修复BOC HK银行名称颜色 =============
print("2. 修复 bochk-bank-statement.html 的银行名称颜色")
print("-" * 70)

with open('bochk-bank-statement.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份
with open('bochk-bank-statement.html.backup_fix3', 'w', encoding='utf-8') as f:
    f.write(content)

# 找到银行名称的HTML，将颜色改为黑色
# 查找包含 "中國銀行(香港)" 和 "BOC Hong Kong" 的strong标签
pattern1 = r'(<strong[^>]*?color:\s*#DB0011[^>]*?>)(中國銀行\(香港\))'
replacement1 = r'<strong style="color: #1f2937; font-size: 1.8rem;">\2'
content = re.sub(pattern1, replacement1, content)

# 同时修复英文名称的颜色
pattern2 = r'(<span[^>]*?color:\s*rgba\(255,255,255,0\.7\)[^>]*?>)(BOC Hong Kong)'
replacement2 = r'<span style="font-size: 0.7em; font-weight: 400; color: #4b5563;">\2'
content = re.sub(pattern2, replacement2, content)

with open('bochk-bank-statement.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("   ✅ 已将银行名称颜色改为黑色")
print("      - 中文名称：#DB0011 → #1f2937（深灰黑）")
print("      - 英文名称：rgba(255,255,255,0.7) → #4b5563（灰色）")
print()

# ============= 问题3: 5个银行页面将案例移到FAQ之上 =============
print("3. 修复5个银行页面：将案例section移到FAQ之上")
print("-" * 70)

bank_files = [
    'bea-bank-statement.html',
    'citibank-bank-statement.html',
    'dahsing-bank-statement.html',
    'citic-bank-statement.html',
    'bankcomm-bank-statement.html'
]

for bank_file in bank_files:
    print(f"\n   处理: {bank_file}")
    
    try:
        with open(bank_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 备份
        with open(f'{bank_file}.backup_fix3', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找FAQ section（包含"常見問題"的section）
        faq_section = None
        for section in soup.find_all('section'):
            if '常見問題' in section.get_text() or 'FAQ' in section.get_text():
                faq_section = section
                break
        
        # 查找案例section（包含"香港中小企"的section）
        case_section = None
        for section in soup.find_all('section'):
            if '香港中小企' in section.get_text() or '真實案例' in section.get_text():
                # 确保不是FAQ section
                if section != faq_section:
                    case_section = section
                    break
        
        if faq_section and case_section:
            # 移动案例section到FAQ之前
            # 先从原位置移除
            case_section_copy = case_section.extract()
            # 插入到FAQ之前
            faq_section.insert_before(case_section_copy)
            
            # 保存修改
            with open(bank_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            print(f"      ✅ 已移动案例section到FAQ之前")
        elif not faq_section:
            print(f"      ⚠️  未找到FAQ section，跳过")
        elif not case_section:
            print(f"      ⚠️  未找到案例section，跳过")
        else:
            print(f"      ⚠️  未找到必要的sections，跳过")
    
    except Exception as e:
        print(f"      ❌ 处理失败: {e}")

print()
print("=" * 70)
print("✅ 所有修复完成！")
print("=" * 70)
print()
print("📊 修复统计：")
print("   1. ✅ hsbc-bank-statement.html - Hero居中")
print("   2. ✅ bochk-bank-statement.html - 银行名称颜色改为黑色")
print("   3. ✅ 5个银行页面 - 案例移到FAQ之上")
print()
print("📝 备份文件：")
print("   - hsbc-bank-statement.html.backup_fix3")
print("   - bochk-bank-statement.html.backup_fix3")
print("   - bea-bank-statement.html.backup_fix3")
print("   - citibank-bank-statement.html.backup_fix3")
print("   - dahsing-bank-statement.html.backup_fix3")
print("   - citic-bank-statement.html.backup_fix3")
print("   - bankcomm-bank-statement.html.backup_fix3")
print()
print("💡 下一步：")
print("   1. 上传修复后的7个文件到服务器")
print("   2. 清除浏览器缓存")
print("   3. 验证修复效果")
print("=" * 70)

