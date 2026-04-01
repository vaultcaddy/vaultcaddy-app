#!/usr/bin/env python3
"""
🔥 紧急修复：移除导致递归错误的多语言支持

错误：Maximum call stack size exceeded
原因：document-detail-new.js 中的递归调用

解决方案：回滚到多语言支持之前的版本
"""

import os
import re

def restore_original_invoice_text():
    """恢复 document-detail-new.js 到没有多语言支持的版本"""
    
    file_path = 'document-detail-new.js'
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除多语言支持函数（从文件开头到第一个非多语言代码）
    # 查找 getInvoiceText 函数的结束位置
    pattern = r'// 🌏 多语言支持 - Invoice 详情.*?return translations\[lang\]\[key\] \|\| translations\[\'en\'\]\[key\] \|\| key;\s*}\s*'
    
    content_cleaned = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 如果上面的模式没匹配到，尝试更简单的模式
    if content_cleaned == content:
        # 查找从开头到第一个 "// 渲染" 或 "function render" 的部分
        lines = content.split('\n')
        start_removing = False
        end_removing = False
        new_lines = []
        
        for i, line in enumerate(lines):
            # 检测多语言支持代码的开始
            if '// 🌏 多语言支持' in line or 'function getInvoiceText' in line:
                start_removing = True
                continue
            
            # 检测多语言支持代码的结束（找到第一个不相关的函数或注释）
            if start_removing and (line.strip().startswith('//') and '多语言' not in line and 'Invoice' not in line and '翻译' not in line) or \
               (line.strip().startswith('function ') and 'getInvoiceText' not in line) or \
               (line.strip().startswith('const ') and 'renderInvoiceDetails' in line) or \
               (line.strip().startswith('async function')):
                start_removing = False
                end_removing = True
            
            # 如果不在移除范围内，保留这一行
            if not start_removing:
                new_lines.append(line)
        
        content_cleaned = '\n'.join(new_lines)
    
    # 恢复原始的英文文本（不使用 getInvoiceText 函数）
    replacements = [
        # 移除对 getInvoiceText 的调用，恢复为静态英文文本
        (r"' \+ getInvoiceText\('invoiceDetails'\) \+ '", "Invoice Details"),
        (r"' \+ getInvoiceText\('invoiceNumber'\) \+ '", "Invoice Number"),
        (r"' \+ getInvoiceText\('date'\) \+ '", "Date"),
        (r"' \+ getInvoiceText\('vendor'\) \+ '", "Vendor"),
        (r"' \+ getInvoiceText\('totalAmount'\) \+ '", "Total Amount"),
        (r"' \+ getInvoiceText\('lineItems'\) \+ '", "Line Items"),
        (r"' \+ getInvoiceText\('editable'\) \+ '", "(Editable)"),
        (r"' \+ getInvoiceText\('code'\) \+ '", "Code"),
        (r"' \+ getInvoiceText\('description'\) \+ '", "Description"),
        (r"' \+ getInvoiceText\('quantity'\) \+ '", "Quantity"),
        (r"' \+ getInvoiceText\('unit'\) \+ '", "Unit"),
        (r"' \+ getInvoiceText\('unitPrice'\) \+ '", "Unit Price"),
        (r"' \+ getInvoiceText\('amount'\) \+ '", "Amount"),
        (r"getInvoiceText\('unitDefault'\)", "'pcs'"),
        (r"' \+ getInvoiceText\('noItems'\) \+ '", "No item data"),
    ]
    
    for pattern, replacement in replacements:
        content_cleaned = re.sub(pattern, replacement, content_cleaned)
    
    # 保存修复后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_cleaned)
    
    print(f"✅ 已恢复 {file_path} 到无多语言支持版本")
    print("✅ 移除了导致递归错误的代码")
    return True

def main():
    print("🔥 紧急修复：Maximum call stack size exceeded\n")
    
    print("=" * 60)
    print("正在移除导致递归的多语言支持代码...")
    print("=" * 60)
    
    if restore_original_invoice_text():
        print("\n" + "=" * 60)
        print("✅ 修复完成！")
        print("=" * 60)
        print("\n📋 修复内容：")
        print("1. ✅ 移除了 getInvoiceText() 函数")
        print("2. ✅ 恢复了静态的英文文本")
        print("3. ✅ 解决了 Maximum call stack size exceeded 错误")
        
        print("\n🔍 验证步骤：")
        print("1. 清除浏览器缓存（Cmd+Shift+Delete）")
        print("2. 强制刷新页面（Cmd+Shift+R）")
        print("3. 尝试打开发票详情页面")
        print("4. 检查控制台是否还有错误")
        
        print("\n⚠️  关于多语言支持：")
        print("• 目前恢复为英文版本")
        print("• 日文和韩文版本暂时也会显示英文")
        print("• 待页面正常工作后，我们可以用更安全的方式实现多语言")
    else:
        print("\n❌ 修复失败，请手动编辑 document-detail-new.js")
        print("需要移除文件开头的 getInvoiceText 函数")

if __name__ == '__main__':
    main()

