#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余的运算符错误 - Type字段修复

作用：修复所有剩余的 | 运算符错误，特别是Type字段相关的
"""

import re
import os
from datetime import datetime

FILES_TO_FIX = [
    'en/firstproject.html',
    'jp/firstproject.html',
    'kr/firstproject.html',
    'firstproject.html'
]

def backup_file(filepath):
    """创建备份"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_type_fix_{timestamp}"
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 备份: {backup_path}")
        return True
    return False

def fix_file(filepath):
    """修复单个文件"""
    
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filepath}")
        return False
    
    print(f"\n🔧 修复: {filepath}")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # 所有需要修复的模式
    patterns = [
        # Type相关
        (r'a\.documentType \| a\.type', 'a.documentType || a.type'),
        (r'b\.documentType \| b\.type', 'b.documentType || b.type'),
        (r'doc\.documentType \| doc\.type', 'doc.documentType || doc.type'),
        (r'd\.documentType \| d\.type', 'd.documentType || d.type'),
        
        # 混合使用的情况
        (r'\|\| doc\.type \| \'\'', '|| doc.type || \'\''),
        (r'doc\.documentType \|\| doc\.type \| \'\'', 'doc.documentType || doc.type || \'\''),
        
        # 条件判断中的错误
        (r"docType === 'bank_statement' \| docType === 'bank_statements'", 
         "docType === 'bank_statement' || docType === 'bank_statements'"),
        (r"documentType === 'invoice' \| documentType === 'receipt'",
         "documentType === 'invoice' || documentType === 'receipt'"),
        
        # 文件名相关（还有一个漏掉的）
        (r'a\.name \|\| a\.fileName \| \'\'', 'a.name || a.fileName || \'\''),
        (r'b\.name \|\| b\.fileName \| \'\'', 'b.name || b.fileName || \'\''),
        
        # vendor相关（还有漏掉的）
        (r'aData\.vendor \|\| aData\.supplier \|\| aData\.merchantName \| \'-\'',
         'aData.vendor || aData.supplier || aData.merchantName || \'-\''),
        (r'bData\.vendor \|\| bData\.supplier \|\| bData\.merchantName \| \'-\'',
         'bData.vendor || bData.supplier || bData.merchantName || \'-\''),
        
        # Bank Statement数据提取
        (r'data\.bankName \| data\.bank_name \| data\.bank', 
         'data.bankName || data.bank_name || data.bank'),
        (r'data\.accountHolder \| data\.account_holder',
         'data.accountHolder || data.account_holder'),
        (r'data\.accountNumber \| data\.account_number',
         'data.accountNumber || data.account_number'),
        
        # 数据合并
        (r'results\[0\]\.data \| results\[0\]\.extractedData',
         'results[0].data || results[0].extractedData'),
        
        # 类型检查
        (r'\(doc\.documentType \| \'\'\)\.toLowerCase\(\)',
         '(doc.documentType || \'\').toLowerCase()'),
        (r'\(d\.documentType \| d\.type \| \'\'\)\.toLowerCase\(\)',
         '(d.documentType || d.type || \'\').toLowerCase()'),
        
        # Export相关
        (r"\.toLowerCase\(\)\.includes\('bank'\)", 
         ".toLowerCase().includes('bank')"),  # 保持不变，只是检查模式
        
        # 通用模式：变量 | ''
        (r"(\w+\.[\w\.]+) \| ''", r"\1 || ''"),
        (r"(\w+\.[\w\.]+) \| '-'", r"\1 || '-'"),
        
        # types对象返回
        (r'types\[type\] \| types\[\'general\'\]',
         'types[type] || types[\'general\']'),
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            count = len(re.findall(pattern, content))
            content = re.sub(pattern, replacement, content)
            fixes.append(f"  ✅ {pattern[:60]}... ({count}处)")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成！共 {len(fixes)} 个模式")
        for fix in fixes:
            print(fix)
        return True
    else:
        print(f"ℹ️  没有需要修复的内容")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🔧 FirstProject Type字段修复工具")
    print("=" * 70)
    print("\n问题: Type列显示 'undefined'")
    print("原因: documentType字段访问仍使用错误的运算符\n")
    
    fixed = 0
    for filepath in FILES_TO_FIX:
        try:
            if fix_file(filepath):
                fixed += 1
        except Exception as e:
            print(f"❌ 修复失败: {e}")
    
    print("\n" + "=" * 70)
    print(f"✅ 成功修复: {fixed}/{len(FILES_TO_FIX)} 个文件")
    print("=" * 70)
    
    if fixed > 0:
        print("\n🎉 修复完成！")
        print("\n📝 下一步:")
        print("1. 强制刷新浏览器 (Shift + Command + R)")
        print("2. Type列应该显示正确的文档类型")

if __name__ == '__main__':
    main()

