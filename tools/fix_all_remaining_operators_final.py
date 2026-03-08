#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终彻底修复所有剩余的位运算符错误

包括：
1. Invoice/Receipt数据提取
2. Bank Statement Balance字段
3. Date字段
4. 所有数据访问逻辑
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
    backup_path = f"{filepath}.backup_final_fix_{timestamp}"
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 备份: {backup_path}")
        return True
    return False

def fix_file(filepath):
    """修复单个文件中所有剩余的位运算符错误"""
    
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filepath}")
        return False
    
    print(f"\n🔧 修复: {filepath}")
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fix_count = 0
    
    # 非常具体的修复模式（按行匹配）
    specific_fixes = [
        # 第3054行
        (r"typeof doc\.createdAt === 'string' \| typeof doc\.createdAt === 'number'",
         "typeof doc.createdAt === 'string' || typeof doc.createdAt === 'number'"),
        
        # 第3092-3093行：Bank Statement Balance
        (r'const openingBalance = data\.openingBalance \| data\.opening_balance \| 0;',
         'const openingBalance = data.openingBalance || data.opening_balance || 0;'),
        (r'const closingBalance = data\.closingBalance \| data\.closing_balance \| data\.balance \| data\.endBalance \| data\.finalBalance \| 0;',
         'const closingBalance = data.closingBalance || data.closing_balance || data.balance || data.endBalance || data.finalBalance || 0;'),
        
        # 第3104行：Statement Period
        (r"let statementPeriod = data\.statementPeriod \| data\.statement_period \| data\.period \|\| '';",
         "let statementPeriod = data.statementPeriod || data.statement_period || data.period || '';"),
        
        # 第3120行：Statement Date
        (r"date = statementPeriod \| data\.statementDate \| data\.statement_date \| data\.date \|\| '-';",
         "date = statementPeriod || data.statementDate || data.statement_date || data.date || '-';"),
        
        # 第3123-3126行：Invoice/Receipt数据（最关键！）
        (r"vendor = data\.vendor \| data\.supplier \| data\.merchantName \| data\.source \|\| '-';",
         "vendor = data.vendor || data.supplier || data.merchantName || data.source || '-';"),
        (r"amount = data\.totalAmount \| data\.amount \| data\.total;",
         "amount = data.totalAmount || data.amount || data.total;"),
        (r"date = data\.invoiceDate \| data\.transactionDate \| data\.date \|\| '-';",
         "date = data.invoiceDate || data.transactionDate || data.date || '-';"),
        
        # 第3137行：Document name
        (r"doc\.name \|\| doc\.fileName \| 'not命名'",
         "doc.name || doc.fileName || 'not命名'"),
        
        # 第3861-3864行：Merge balance
        (r"totalOpeningBalance = parseFloat\(data\.openingBalance \| data\.opening_balance\) \| 0;",
         "totalOpeningBalance = parseFloat(data.openingBalance || data.opening_balance) || 0;"),
        (r"totalClosingBalance = parseFloat\(data\.closingBalance \| data\.closing_balance\) \| 0;",
         "totalClosingBalance = parseFloat(data.closingBalance || data.closing_balance) || 0;"),
        
        # 第4390-4392行：Export grouping
        (r"} else if \(docType === 'invoice' \| docType === 'invoices'\) \{",
         "} else if (docType === 'invoice' || docType === 'invoices') {"),
        (r"} else if \(docType === 'receipt' \| docType === 'receipts'\) \{",
         "} else if (docType === 'receipt' || docType === 'receipts') {"),
    ]
    
    # 应用具体修复
    for pattern, replacement in specific_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            fix_count += 1
            print(f"  ✅ {pattern[:70]}...")
    
    # 通用模式修复（补充遗漏的）
    general_patterns = [
        # 数据字段访问模式：data.field1 | data.field2 | default
        (r'(data\.\w+) \| (data\.\w+) \| (data\.\w+)(?!\|)', r'\1 || \2 || \3'),
        (r'(data\.\w+) \| (data\.\w+)(?!\|)', r'\1 || \2'),
        
        # 类型检查：typeof x === 'type' | typeof x === 'type'
        (r"(typeof \w+\.?\w* === '[^']+') \| (typeof \w+\.?\w* === '[^']+')", r'\1 || \2'),
        
        # 条件判断中的或
        (r"(\w+ === '[^']+') \| (\w+ === '[^']+')", r'\1 || \2'),
        
        # parseFloat/parseInt结果
        (r'parseFloat\(([^)]+)\) \| 0', r'parseFloat(\1) || 0'),
        (r'parseInt\(([^)]+)\) \| 0', r'parseInt(\1) || 0'),
    ]
    
    for pattern, replacement in general_patterns:
        matches = re.findall(pattern, content)
        if matches:
            before = content
            content = re.sub(pattern, replacement, content)
            if content != before:
                fix_count += len(matches) if isinstance(matches[0], tuple) else 1
                print(f"  ✅ {pattern[:60]}... ({len(matches)}处)")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 修复完成！共 {fix_count} 处")
        return True
    else:
        print(f"ℹ️  没有需要修复的内容")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🔧 最终彻底修复 - 所有位运算符错误")
    print("=" * 70)
    print("\n修复内容:")
    print("1. ✅ Invoice/Receipt vendor和date字段")
    print("2. ✅ Bank Statement balance字段")
    print("3. ✅ Date和timestamp处理")
    print("4. ✅ 所有数据访问逻辑\n")
    
    fixed = 0
    total_fixes = 0
    
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
        print("\n🎉 最终修复完成！")
        print("\n📝 现在应该修复的问题:")
        print("  ✅ Invoice显示vendor和date")
        print("  ✅ Bank Statement显示正确的balance")
        print("  ✅ 所有数据字段正确提取")
        print("\n🔄 下一步:")
        print("  1. 强制刷新浏览器 (Shift + Command + R)")
        print("  2. 检查Invoice行是否显示supplier和date")
        print("  3. 验证所有文档类型数据完整")
    
    return fixed > 0

if __name__ == '__main__':
    main()

