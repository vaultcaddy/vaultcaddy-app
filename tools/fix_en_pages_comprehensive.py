#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文版页面的所有中文内容和优化排版
"""

import re

print("🔧 开始修复英文版页面...")
print("="*70)

# ============================================================
# 任务1: 优化en/index.html Hero标题排版
# ============================================================
print("\n📝 任务1: 优化Hero标题排版...")

with open('en/index.html', 'r', encoding='utf-8') as f:
    en_index = f.read()

# 找到Hero标题并优化排版
# 原标题太长，需要更好的断行
old_hero_title = r'<h1 style="font-size: 4rem; font-weight: 900; line-height: 1\.1; margin-bottom: 1\.5rem; text-shadow: 0 4px 20px rgba\(0,0,0,0\.2\);">\s*<span>VaultCaddy - Bank Statement & Receipt AI Processing Expert \| QuickBooks Integration</span><br>'

new_hero_title = '''<h1 style="font-size: 4rem; font-weight: 900; line-height: 1.2; margin-bottom: 1.5rem; text-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                    <span style="display: block; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">VaultCaddy</span>
                    <span style="display: block; font-size: 1.75rem; font-weight: 600; line-height: 1.3;">Bank Statement & Receipt AI Expert</span>
                    <span style="display: block; font-size: 1.5rem; font-weight: 600; margin-top: 0.5rem;">QuickBooks Integration</span><br>'''

if re.search(old_hero_title, en_index):
    en_index = re.sub(old_hero_title, new_hero_title, en_index)
    print("  ✅ Hero标题排版已优化")
else:
    print("  ℹ️  未找到Hero标题（可能已优化）")

# ============================================================
# 任务2: 修复定价区域动画文字（合理且實惠的價格）
# ============================================================
print("\n📝 任务2: 修复定价区域动画文字...")

# 这些是动态内容，需要在JavaScript中修复
pricing_translations = [
    ('合理且實惠的價格', 'FAIR AND AFFORDABLE PRICING'),
    ('輕鬆處理銀行對帳單', 'Easy Bank Statement Processing'),
    ('data-translate="pricing_badge">合理且實惠的價格', 'data-translate="pricing_badge">FAIR AND AFFORDABLE PRICING'),
    ('data-translate="pricing_title" style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">輕鬆處理銀行對帳單', 
     'data-translate="pricing_title" style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">Easy Bank Statement Processing'),
]

for old, new in pricing_translations:
    if old in en_index:
        en_index = en_index.replace(old, new)
        print(f"  ✅ 已替换: {old[:30]}...")

# ============================================================
# 任务3: Learning Center文字改为白色
# ============================================================
print("\n📝 任务3: Learning Center文字改为白色...")

# 找到Learning Center标题
old_learning_title = r'<h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: #1f2937;">📚 Learning [Cc]enter</h2>'
new_learning_title = '<h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem; color: white;">📚 Learning Center</h2>'

if re.search(old_learning_title, en_index):
    en_index = re.sub(old_learning_title, new_learning_title, en_index)
    print("  ✅ Learning Center标题已改为白色")
else:
    print("  ℹ️  未找到Learning Center标题")

# 找到Learning Center描述
old_learning_desc = r'<p style="font-size: 1\.125rem; color: #6b7280;">Learn how to maximize VaultCaddy for your financial documents</p>'
new_learning_desc = '<p style="font-size: 1.125rem; color: white; opacity: 0.95;">Learn how to maximize VaultCaddy for your financial documents</p>'

if re.search(old_learning_desc, en_index):
    en_index = re.sub(old_learning_desc, new_learning_desc, en_index)
    print("  ✅ Learning Center描述已改为白色")
else:
    print("  ℹ️  未找到Learning Center描述")

# 保存en/index.html
with open('en/index.html', 'w', encoding='utf-8') as f:
    f.write(en_index)

print("  ✅ en/index.html 修复完成")

# ============================================================
# 任务4: 修复en/dashboard.html验证banner
# ============================================================
print("\n📝 任务4: 修复Dashboard验证banner...")

with open('en/dashboard.html', 'r', encoding='utf-8') as f:
    en_dashboard = f.read()

# 替换验证banner的中文
dashboard_translations = [
    ('立即驗證您的 email 即送 20 Credits 試用！', 'Verify your email now and get 20 Credits free trial!'),
    ('立即驗證', 'Verify Now'),
    ('🎁\n                立即驗證您的 email 即送 20 Credits 試用！', '🎁\n                Verify your email now and get 20 Credits free trial!'),
]

for old, new in dashboard_translations:
    if old in en_dashboard:
        en_dashboard = en_dashboard.replace(old, new)
        print(f"  ✅ 已替换: {old[:30]}...")

# ============================================================
# 任务5: 修复Dashboard搜索栏placeholder
# ============================================================
print("\n📝 任务5: 修复Dashboard搜索栏...")

# 这个应该在sidebar-component.js中已经处理了，但我们再检查一次
search_translations = [
    ('篩選文檔名稱...', 'Filter documents...'),
    ('placeholder="篩選文檔名稱..."', 'placeholder="Filter documents..."'),
    ('data-i18n-placeholder="filter-documents" placeholder="篩選文檔名稱..."', 
     'data-i18n-placeholder="filter-documents" placeholder="Filter documents..."'),
]

for old, new in search_translations:
    if old in en_dashboard:
        en_dashboard = en_dashboard.replace(old, new)
        print(f"  ✅ 已替换搜索栏: {old[:20]}...")

# 保存en/dashboard.html
with open('en/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(en_dashboard)

print("  ✅ en/dashboard.html 修复完成")

# ============================================================
# 任务6: 修复en/document-detail.html字段
# ============================================================
print("\n📝 任务6: 修复Document detail页面...")

with open('en/document-detail.html', 'r', encoding='utf-8') as f:
    en_document = f.read()

# 发票详情字段翻译
document_translations = [
    # 主要标题
    ('發票詳情', 'Invoice Details'),
    ('發票號碼', 'Invoice Number'),
    ('日期', 'Date'),
    ('供應商', 'Vendor'),
    ('總金額', 'Total Amount'),
    ('項目明細 (可編輯)', 'Line Items (Editable)'),
    ('項目明細', 'Line Items'),
    
    # 表格列头
    ('代碼', 'Code'),
    ('描述', 'Description'),
    ('數量', 'Quantity'),
    ('單位', 'Unit'),
    ('單價', 'Unit Price'),
    ('金額', 'Amount'),
    
    # 状态信息
    ('無項目數據', 'No line items'),
    ('加載中...', 'Loading...'),
    ('篩選文檔名稱', 'Filter documents'),
]

for old, new in document_translations:
    if old in en_document:
        en_document = en_document.replace(old, new)
        print(f"  ✅ 已替换: {old} → {new}")

# 保存en/document-detail.html
with open('en/document-detail.html', 'w', encoding='utf-8') as f:
    f.write(en_document)

print("  ✅ en/document-detail.html 修复完成")

print("\n" + "="*70)
print("🎉 所有修复完成！")
print("\n修改总结:")
print("  1. ✅ 优化Hero标题排版（更好的视觉层次）")
print("  2. ✅ 修复定价区域动画文字为英文")
print("  3. ✅ Learning Center文字改为白色")
print("  4. ✅ Dashboard验证banner改为英文")
print("  5. ✅ Dashboard搜索栏改为英文")
print("  6. ✅ Document detail页面字段改为英文")

