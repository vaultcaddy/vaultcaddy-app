#!/usr/bin/env python3
"""
🔥 修复 Export 按钮问题 - 运算符错误

问题：document-detail.html 中的 Export 菜单判断使用了错误的运算符 |
应该使用: ||
"""

import os
import re

def fix_export_operators():
    """修复所有版本的 document-detail.html 中的 Export 运算符"""
    
    html_files = [
        'en/document-detail.html',
        'jp/document-detail.html',
        'kr/document-detail.html',
        'document-detail.html'
    ]
    
    fixed_count = 0
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            print(f"⚠️  文件不存在: {html_file}")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复 docType 条件判断中的运算符
        patterns = [
            # Invoice 类型判断
            (r"if \(docType === 'invoice' \| docType === '([^']+)' \| docType === 'invoices'\)",
             r"if (docType === 'invoice' || docType === '\1' || docType === 'invoices')"),
            
            # 通用的 | 改为 ||（在条件判断中）
            (r"if \(docType === '([^']+)' \| docType === '([^']+)' \| docType === '([^']+)'\)",
             r"if (docType === '\1' || docType === '\2' || docType === '\3')"),
            
            # Bank Statement 类型判断
            (r"if \(docType === 'bank_statement' \| docType === '([^']+)' \| docType === 'Bank Statement'\)",
             r"if (docType === 'bank_statement' || docType === '\1' || docType === 'Bank Statement')"),
            
            # Receipt 类型判断
            (r"if \(docType === 'receipt' \| docType === '([^']+)'\)",
             r"if (docType === 'receipt' || docType === '\1')"),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已修复 {html_file}")
            fixed_count += 1
        else:
            print(f"ℹ️  {html_file} 无需修复")
    
    return fixed_count

def main():
    print("🔧 修复 Export 按钮运算符错误...\n")
    
    print("=" * 60)
    print("检查并修复所有 document-detail.html 文件")
    print("=" * 60)
    
    fixed = fix_export_operators()
    
    print("\n" + "=" * 60)
    print(f"✅ 修复完成！共修复 {fixed} 个文件")
    print("=" * 60)
    
    print("\n📋 修复内容：")
    print("• 修复了 Export 菜单中的 docType 条件判断")
    print("• 将位运算符 | 改为逻辑运算符 ||")
    print("• 确保 Export 菜单能正确显示内容")
    
    print("\n🔍 验证步骤：")
    print("1. 清除浏览器缓存")
    print("2. 访问之前打不开的页面")
    print("3. 点击 Export 按钮")
    print("4. 应该能看到完整的导出选项菜单")

if __name__ == '__main__':
    main()

