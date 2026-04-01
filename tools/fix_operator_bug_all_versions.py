#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复所有 firstproject.html 文件中的运算符错误

问题：JavaScript中错误使用了位运算符 | 而不是逻辑或运算符 ||
影响：导致"docsToRender is not iterable"错误，所有文档无法显示

作用：
1. 修复所有4个语言版本的 firstproject.html
2. 将所有错误的 | 替换为 ||（在正确的上下文中）
3. 创建备份文件
"""

import re
import os
from datetime import datetime

# 需要修复的文件列表
FILES_TO_FIX = [
    'en/firstproject.html',
    'jp/firstproject.html', 
    'kr/firstproject.html',
    'firstproject.html'
]

# 需要修复的模式（只替换JavaScript逻辑表达式中的 |）
# 注意：不要替换 || 或 |=（已经正确的情况）
PATTERNS_TO_FIX = [
    # 1. 变量赋值中的 a | b 格式
    (r'(\w+)\s*\|\s*(\w+)(?!\|)', r'\1 || \2'),
    
    # 2. 对象属性访问中的 a?.b | c?.d 格式  
    (r'(\w+\??\.[\w\.?]+)\s*\|\s*(\w+\??\.[\w\.?]+)(?!\|)', r'\1 || \2'),
    
    # 3. 三元表达式或条件中的 condition | condition 格式
    (r'(===|!==|<|>|<=|>=)\s*(\w+)\s*\|\s*(\w+)\s*(===|!==|<|>|<=|>=)', r'\1 \2 || \3 \4'),
    
    # 4. 括号中的表达式 (a | b)
    (r'\(([^)]+?)\s*\|\s*([^)]+?)\)(?!\|)', lambda m: f'({m.group(1)} || {m.group(2)})' if '||' not in m.group(0) else m.group(0)),
]

def backup_file(filepath):
    """创建备份文件"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{filepath}.backup_operator_fix_{timestamp}"
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 备份创建: {backup_path}")
        return True
    return False

def fix_operators_in_file(filepath):
    """修复单个文件中的运算符错误"""
    
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在: {filepath}")
        return False
    
    print(f"\n🔧 正在修复: {filepath}")
    
    # 创建备份
    backup_file(filepath)
    
    # 读取文件内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fix_count = 0
    
    # 特定的关键修复（手动指定）
    critical_fixes = [
        # 1. renderDocuments 中最关键的那一行
        (
            r'const docsToRender = window\.filteredDocuments \| allDocuments;',
            'const docsToRender = window.filteredDocuments || allDocuments;'
        ),
        
        # 2. 文档属性访问
        (
            r'doc\.processedData\?\.invoiceDate \| doc\.processedData\?\.transactionDate \| doc\.processedData\?\.date',
            'doc.processedData?.invoiceDate || doc.processedData?.transactionDate || doc.processedData?.date'
        ),
        (
            r'doc\.uploadDate \| doc\.createdAt',
            'doc.uploadDate || doc.createdAt'
        ),
        (
            r'doc\.fileName \| doc\.name',
            'doc.fileName || doc.name'
        ),
        (
            r'doc\.name \| doc\.fileName',
            'doc.name || doc.fileName'
        ),
        (
            r'doc\.documentType \| doc\.type',
            'doc.documentType || doc.type'
        ),
        
        # 3. processedData 访问
        (
            r'result\.data \| result\.extractedData',
            'result.data || result.extractedData'
        ),
        (
            r'aData\.vendor \| aData\.supplier \| aData\.merchantName',
            'aData.vendor || aData.supplier || aData.merchantName'
        ),
        (
            r'bData\.vendor \| bData\.supplier \| bData\.merchantName',
            'bData.vendor || bData.supplier || bData.merchantName'
        ),
        
        # 4. 条件判断
        (
            r'currentPage === totalPages \| totalPages === 0',
            'currentPage === totalPages || totalPages === 0'
        ),
        (
            r'\(currentPage === totalPages \| totalPages === 0\)',
            '(currentPage === totalPages || totalPages === 0)'
        ),
        
        # 5. 日期筛选器
        (
            r'dateFilters\.dateFrom \| dateFilters\.dateTo',
            'dateFilters.dateFrom || dateFilters.dateTo'
        ),
        (
            r'dateFilters\.uploadDateFrom \| dateFilters\.uploadDateTo',
            'dateFilters.uploadDateFrom || dateFilters.uploadDateTo'
        ),
        
        # 6. 用户信息
        (
            r"userDisplayName = currentUser\.displayName \| '';",
            "userDisplayName = currentUser.displayName || '';"
        ),
        (
            r'userDisplayName = userDoc\.displayName \| userDisplayName;',
            'userDisplayName = userDoc.displayName || userDisplayName;'
        ),
        (
            r'userDoc\.credits \| 0',
            'userDoc.credits || 0'
        ),
        
        # 7. 数组/对象默认值
        (
            r'window\.filteredDocuments \| \[\]',
            'window.filteredDocuments || []'
        ),
        (
            r'window\.allDocuments \| \[\]',
            'window.allDocuments || []'
        ),
        (
            r'a\.processedData \| \{\}',
            'a.processedData || {}'
        ),
        (
            r'b\.processedData \| \{\}',
            'b.processedData || {}'
        ),
    ]
    
    # 应用关键修复
    for pattern, replacement in critical_fixes:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            fix_count += len(matches) if isinstance(matches, list) else 1
            print(f"  ✅ 修复: {pattern[:50]}... ({len(matches) if isinstance(matches, list) else 1}处)")
    
    # 保存修复后的内容
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filepath} 修复完成！共修复 {fix_count} 处")
        return True
    else:
        print(f"ℹ️  {filepath} 没有需要修复的内容")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🔧 FirstProject 运算符错误批量修复工具")
    print("=" * 70)
    print("\n问题: JavaScript中错误使用了位运算符 | 而不是 ||")
    print("影响: 导致 'docsToRender is not iterable' 错误")
    print("解决: 批量替换所有错误的运算符\n")
    
    fixed_count = 0
    failed_count = 0
    
    for filepath in FILES_TO_FIX:
        try:
            if fix_operators_in_file(filepath):
                fixed_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"❌ 修复 {filepath} 时出错: {e}")
            failed_count += 1
    
    print("\n" + "=" * 70)
    print("📊 修复总结")
    print("=" * 70)
    print(f"✅ 成功修复: {fixed_count} 个文件")
    print(f"❌ 失败/跳过: {failed_count} 个文件")
    print(f"📁 总计处理: {len(FILES_TO_FIX)} 个文件")
    
    if fixed_count > 0:
        print("\n🎉 修复完成！")
        print("\n📝 下一步:")
        print("1. 刷新浏览器页面")
        print("2. 清除浏览器缓存（Shift + Command + R）")
        print("3. 验证30个文档是否正常显示")
        print("\n💾 备份文件已创建，格式: *.backup_operator_fix_YYYYMMDD_HHMMSS")
    
    return fixed_count > 0

if __name__ == '__main__':
    main()

