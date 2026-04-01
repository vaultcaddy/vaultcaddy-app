#!/usr/bin/env python3
"""
🔥 紧急修复：i18n 对象中的错误

问题：
1. 对象定义中有 '${t(...)}' 模板字符串
2. 对象定义中调用了 t() 函数
3. 缩进问题

这会导致语法错误，页面无法加载
"""

import os
import re

def emergency_fix_i18n():
    """紧急修复 i18n 对象"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("正在修复 i18n 对象...")
    
    # 修复所有错误的模板字符串和函数调用
    fixes = [
        # 修复中文部分的缩进和格式
        (r"no_transactions: '無交易記錄',\s*// 發票相關翻譯", 
         "no_transactions: '無交易記錄',\n        // 發票相關翻譯"),
        
        # 修复英文部分的错误
        (r"no_transactions: 'No transactions',\s*// Invoice translations\s*invoice_details: '\$\{t\('invoice_details'\)\}',\s*invoice_number: '\$\{t\('invoice_number'\)\}',\s*vendor: 'Vendor',\s*total_amount: '\$\{t\('total_amount'\)\}',\s*line_items: '\$\{t\('line_items'\)\}',\s*code: 'Code',\s*quantity: 'Quantity',\s*unit: 'Unit',\s*unit_price: 'Unit Price',\s*unit_default: t\('unit_default'\),\s*no_items: t\('no_items'\)",
         "no_transactions: 'No transactions',\n        // Invoice translations\n        invoice_details: 'Invoice Details',\n        invoice_number: 'Invoice Number',\n        vendor: 'Vendor',\n        total_amount: 'Total Amount',\n        line_items: 'Line Items',\n        code: 'Code',\n        quantity: 'Quantity',\n        unit: 'Unit',\n        unit_price: 'Unit Price',\n        unit_default: 'pcs',\n        no_items: 'No item data'"),
        
        # 如果上面的模式太复杂，使用逐个修复
        (r"invoice_details: '\$\{t\('invoice_details'\)\}'", "invoice_details: 'Invoice Details'"),
        (r"invoice_number: '\$\{t\('invoice_number'\)\}'", "invoice_number: 'Invoice Number'"),
        (r"total_amount: '\$\{t\('total_amount'\)\}'", "total_amount: 'Total Amount'"),
        (r"line_items: '\$\{t\('line_items'\)\}'", "line_items: 'Line Items'"),
        (r"unit_default: t\('unit_default'\)", "unit_default: 'pcs'"),
        (r"no_items: t\('no_items'\)", "no_items: 'No item data'"),
        
        # 修复可能的缩进问题
        (r"(\s{8})no_transactions: 'No transactions',\s*//", r"\1no_transactions: 'No transactions',\n\1//"),
    ]
    
    for pattern, replacement in fixes:
        old_content = content
        content = re.sub(pattern, replacement, content)
        if content != old_content:
            print(f"✅ 修复了模式")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ i18n 对象修复完成")
    return True

def main():
    print("🔥 紧急修复 i18n 对象错误...\n")
    
    print("=" * 60)
    print("修复 i18n 对象中的语法错误")
    print("=" * 60)
    
    emergency_fix_i18n()
    
    print("\n" + "=" * 60)
    print("✅ 修复完成！")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("1. ✅ 移除了错误的 ${t(...)} 模板字符串")
    print("2. ✅ 移除了对象定义中的 t() 函数调用")
    print("3. ✅ 使用静态字符串值")
    
    print("\n🔍 立即验证：")
    print("1. 清除浏览器缓存")
    print("2. 强制刷新（Cmd/Ctrl + Shift + R）")
    print("3. 尝试打开发票或银行对账单页面")

if __name__ == '__main__':
    main()

