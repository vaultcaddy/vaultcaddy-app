#!/usr/bin/env python3
"""
🔧 修复多语言支持的递归引用问题
"""

import os
import re

def fix_recursive_references():
    """修复 document-detail-new.js 中的递归引用"""
    
    file_path = 'document-detail-new.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到翻译对象的位置并修复
    pattern = r"invoiceDetails: '' \+ getInvoiceText\('invoiceDetails'\) \+ ''"
    if re.search(pattern, content):
        print("发现递归引用，正在修复...")
        
        # 替换英文部分的递归引用
        fixes = [
            (r"invoiceDetails: '' \+ getInvoiceText\('invoiceDetails'\) \+ ''", "invoiceDetails: 'Invoice Details'"),
            (r"invoiceNumber: '' \+ getInvoiceText\('invoiceNumber'\) \+ ''", "invoiceNumber: 'Invoice Number'"),
            (r"lineItems: '' \+ getInvoiceText\('lineItems'\) \+ ''", "lineItems: 'Line Items'"),
            (r"editable: '' \+ getInvoiceText\('editable'\) \+ ''", "editable: '(Editable)'"),
        ]
        
        for pattern, replacement in fixes:
            content = re.sub(pattern, replacement, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ 已修复递归引用")
        return True
    else:
        print("ℹ️  没有发现递归引用问题")
        return False

if __name__ == '__main__':
    fix_recursive_references()

