#!/usr/bin/env python3
"""
🔥 修复 Invoice 中文和 Export 问题

问题1：document-detail-new.js 中硬编码的中文文本
问题2：document-detail.html 中 Export 菜单的运算符错误（| 应该是 ||）
问题3：页面切换时空白卡住（可能与运算符错误有关）
"""

import os
import re

def fix_invoice_chinese_in_js():
    """修复 document-detail-new.js 中的中文文本"""
    file_path = 'document-detail-new.js'
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复发票详情部分的中文
    replacements = [
        # 发票详情标题
        (r'<i class="fas fa-file-invoice"[^>]*></i>\s*發票詳情',
         '<i class="fas fa-file-invoice" style="color: #3b82f6; margin-right: 0.5rem;"></i>\n                Invoice Details'),
        
        # 发票字段标签
        (r'<label[^>]*>發票號碼</label>', 
         '<label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">Invoice Number</label>'),
        
        (r'<label[^>]*>日期</label>', 
         '<label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">Date</label>'),
        
        (r'<label[^>]*>供應商</label>', 
         '<label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">Vendor</label>'),
        
        (r'<label[^>]*>總金額</label>', 
         '<label style="display: block; font-size: 0.75rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 600;">Total Amount</label>'),
        
        # 项目明细标题
        (r'<i class="fas fa-list"[^>]*></i>\s*項目明細',
         '<i class="fas fa-list" style="color: #8b5cf6; margin-right: 0.5rem;"></i>\n                Line Items'),
        
        # 项目明细可编辑提示
        (r'<span[^>]*>\(可編輯\)</span>',
         '<span style="font-size: 0.875rem; color: #6b7280; font-weight: normal; margin-left: 0.5rem;">(Editable)</span>'),
        
        # 表头中文
        (r'<th>代碼</th>', '<th>Code</th>'),
        (r'<th>描述</th>', '<th>Description</th>'),
        (r'<th[^>]*>數量</th>', '<th style="text-align: right;">Quantity</th>'),
        (r'<th[^>]*>單位</th>', '<th style="text-align: right;">Unit</th>'),
        (r'<th[^>]*>單價</th>', '<th style="text-align: right;">Unit Price</th>'),
        (r'<th[^>]*>金額</th>', '<th style="text-align: right;">Amount</th>'),
        
        # 单位默认值
        (r"item\.unit \|\| '件'", "item.unit || 'pcs'"),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已修复 {file_path} 中的中文文本")
        return True
    else:
        print(f"ℹ️  {file_path} 没有需要修复的中文文本")
        return False

def fix_export_operators_in_html(file_path):
    """修复 document-detail.html 中 Export 相关的运算符错误"""
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复 Export 菜单中的运算符错误
    fixes = [
        # 1. docType 获取逻辑
        (r"docType = window\.currentDocument\.type \| window\.currentDocument\.documentType \| 'general'",
         "docType = window.currentDocument.type || window.currentDocument.documentType || 'general'"),
        
        # 2. docType 判断条件
        (r"if \(docType === 'invoice' \| docType === 'Invoice' \| docType === 'invoices'\)",
         "if (docType === 'invoice' || docType === 'Invoice' || docType === 'invoices')"),
        
        # 3. 其他可能的运算符错误
        (r"if \(docType === 'bank_statement' \| docType === 'bankStatement' \| docType === 'Bank Statement'\)",
         "if (docType === 'bank_statement' || docType === 'bankStatement' || docType === 'Bank Statement')"),
        
        # 4. Receipt 类型判断
        (r"if \(docType === 'receipt' \| docType === 'Receipt'\)",
         "if (docType === 'receipt' || docType === 'Receipt')"),
    ]
    
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已修复 {file_path} 中的运算符错误")
        return True
    else:
        print(f"ℹ️  {file_path} 没有需要修复的运算符错误")
        return False

def main():
    print("🔧 开始修复 Invoice 中文和 Export 问题...\n")
    
    # 1. 修复 document-detail-new.js 中的中文
    print("=" * 60)
    print("第1步：修复 document-detail-new.js 中的中文文本")
    print("=" * 60)
    fix_invoice_chinese_in_js()
    
    # 2. 修复所有版本的 document-detail.html 中的运算符错误
    print("\n" + "=" * 60)
    print("第2步：修复 document-detail.html 中的运算符错误")
    print("=" * 60)
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    for html_file in html_files:
        if os.path.exists(html_file):
            fix_export_operators_in_html(html_file)
        else:
            print(f"⚠️  文件不存在: {html_file}")
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    print("\n📋 修复内容总结：")
    print("1. ✅ 修复 document-detail-new.js 中的中文文本（发票详情、项目明细等）")
    print("2. ✅ 修复 document-detail.html 中 Export 菜单的运算符错误（| 改为 ||）")
    print("3. ✅ 这些修复应该同时解决页面空白卡住的问题")
    print("\n🔍 验证步骤：")
    print("1. 刷新页面，查看 Invoice 详情是否显示为英文")
    print("2. 点击 Export 按钮，确认菜单正常显示")
    print("3. 在功能页面间切换，观察是否还会出现空白页面")

if __name__ == '__main__':
    main()

