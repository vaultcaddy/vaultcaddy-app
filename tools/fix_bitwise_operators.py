#!/usr/bin/env python3
"""
修复 firstproject.html 中的位运算符错误

问题：JavaScript代码中错误地使用了位运算符 | 而不是逻辑或 ||
这导致了 "TypeError: docsToRender is not iterable" 错误

作用：
1. 自动检测并修复所有应该是 || 但写成 | 的地方
2. 保留需要位运算的地方（如 currentPage === totalPages | totalPages === 0）
3. 创建备份文件

使用：python3 fix_bitwise_operators.py
"""

import re
import os
from datetime import datetime

def fix_bitwise_operators(file_path):
    """修复文件中的位运算符错误"""
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 创建备份
    backup_path = f"{file_path}.backup_bitwise_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已创建备份: {backup_path}")
    
    # 修复模式
    fixes = []
    
    # 模式1: window.filteredDocuments | allDocuments
    pattern1 = r'window\.filteredDocuments\s*\|\s+allDocuments'
    matches1 = re.finditer(pattern1, content)
    for match in matches1:
        fixes.append({
            'pattern': pattern1,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 模式2: dateFilters.dateFrom | dateFilters.dateTo
    pattern2 = r'dateFilters\.\w+\s*\|\s+dateFilters\.\w+'
    matches2 = re.finditer(pattern2, content)
    for match in matches2:
        fixes.append({
            'pattern': pattern2,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 模式3: processedData?.field1 | processedData?.field2 | ...
    # 这是最常见的错误
    pattern3 = r'(processedData\?\.\w+)\s*\|\s+(processedData\?\.\w+)'
    matches3 = re.finditer(pattern3, content)
    for match in matches3:
        fixes.append({
            'pattern': pattern3,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 模式4: data.field1 | data.field2 | 'default'
    pattern4 = r'(data\.\w+)\s*\|\s+(data\.\w+)'
    matches4 = re.finditer(pattern4, content)
    for match in matches4:
        if '===' not in match.group():  # 排除比较运算
            fixes.append({
                'pattern': pattern4,
                'old': match.group(),
                'new': match.group().replace('|', '||'),
                'line': content[:match.start()].count('\n') + 1
            })
    
    # 模式5: aData.field | bData.field
    pattern5 = r'([ab]Data\.\w+)\s*\|\s+([ab]Data\.\w+)'
    matches5 = re.finditer(pattern5, content)
    for match in matches5:
        fixes.append({
            'pattern': pattern5,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 模式6: doc.field1 | doc.field2 | 'default'
    pattern6 = r'(doc\.\w+)\s*\|\s+(doc\.\w+)'
    matches6 = re.finditer(pattern6, content)
    for match in matches6:
        if '===' not in match.group():
            fixes.append({
                'pattern': pattern6,
                'old': match.group(),
                'new': match.group().replace('|', '||'),
                'line': content[:match.start()].count('\n') + 1
            })
    
    # 模式7: (a.field | b.field)
    pattern7 = r'\(([a-zA-Z_]+\.\w+)\s*\|\s+([a-zA-Z_]+\.\w+)\)'
    matches7 = re.finditer(pattern7, content)
    for match in matches7:
        if '===' not in match.group():
            fixes.append({
                'pattern': pattern7,
                'old': match.group(),
                'new': match.group().replace('|', '||'),
                'line': content[:match.start()].count('\n') + 1
            })
    
    # 模式8: uploadDate | createdAt
    pattern8 = r'uploadDate\s*\|\s+createdAt'
    matches8 = re.finditer(pattern8, content)
    for match in matches8:
        fixes.append({
            'pattern': pattern8,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 模式9: window.allDocuments | []
    pattern9 = r'window\.allDocuments\s*\|\s+\[\]'
    matches9 = re.finditer(pattern9, content)
    for match in matches9:
        fixes.append({
            'pattern': pattern9,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 模式10: result.data | result.extractedData
    pattern10 = r'result\.data\s*\|\s+result\.extractedData'
    matches10 = re.finditer(pattern10, content)
    for match in matches10:
        fixes.append({
            'pattern': pattern10,
            'old': match.group(),
            'new': match.group().replace('|', '||'),
            'line': content[:match.start()].count('\n') + 1
        })
    
    # 显示所有待修复的地方
    if fixes:
        print(f"\n🔍 发现 {len(fixes)} 处需要修复的位运算符:\n")
        for i, fix in enumerate(fixes, 1):
            print(f"{i}. 第 {fix['line']} 行")
            print(f"   旧: {fix['old']}")
            print(f"   新: {fix['new']}")
            print()
    else:
        print("✅ 未发现需要修复的位运算符错误")
        return content, 0
    
    # 应用修复
    new_content = content
    fix_count = 0
    
    # 按照出现顺序修复（从后往前，避免位置偏移）
    patterns_to_replace = [
        (r'window\.filteredDocuments\s*\|\s+allDocuments', 'window.filteredDocuments || allDocuments'),
        (r'dateFilters\.dateFrom\s*\|\s+dateFilters\.dateTo', 'dateFilters.dateFrom || dateFilters.dateTo'),
        (r'dateFilters\.uploadDateFrom\s*\|\s+dateFilters\.uploadDateTo', 'dateFilters.uploadDateFrom || dateFilters.uploadDateTo'),
        (r'processedData\?\.invoiceDate\s*\|\s+processedData\?\.transactionDate\s*\|\s+processedData\?\.date', 
         'processedData?.invoiceDate || processedData?.transactionDate || processedData?.date'),
        (r'processedData\?\.totalAmount\s*\|\s+processedData\?\.amount\s*\|\s+processedData\?\.total', 
         'processedData?.totalAmount || processedData?.amount || processedData?.total'),
        (r'processedData\?\.vendor\s*\|\s+processedData\?\.supplier\s*\|\s+processedData\?\.merchantName', 
         'processedData?.vendor || processedData?.supplier || processedData?.merchantName'),
        (r'aData\.vendor\s*\|\s+aData\.supplier\s*\|\s+aData\.merchantName', 
         'aData.vendor || aData.supplier || aData.merchantName'),
        (r'bData\.vendor\s*\|\s+bData\.supplier\s*\|\s+bData\.merchantName', 
         'bData.vendor || bData.supplier || bData.merchantName'),
        (r'uploadDate\s*\|\s+createdAt', 'uploadDate || createdAt'),
        (r'doc\.processedData\s*\|\s+\{\}', 'doc.processedData || {}'),
        (r'window\.allDocuments\s*\|\s+\[\]', 'window.allDocuments || []'),
        (r'result\.data\s*\|\s+result\.extractedData', 'result.data || result.extractedData'),
        (r'doc\.name\s*\|\s+doc\.fileName', 'doc.name || doc.fileName'),
        (r'doc\.documentType\s*\|\s+doc\.type', 'doc.documentType || doc.type'),
        (r'a\.name\s*\|\s+a\.fileName', 'a.name || a.fileName'),
        (r'b\.name\s*\|\s+b\.fileName', 'b.name || b.fileName'),
        (r'currentUser\.displayName\s*\|\s+\'\'', 'currentUser.displayName || \'\''),
        (r'userDoc\.displayName\s*\|\s+userDisplayName', 'userDoc.displayName || userDisplayName'),
        (r'userDoc\.credits\s*\|\s+0', 'userDoc.credits || 0'),
    ]
    
    for pattern, replacement in patterns_to_replace:
        matches = re.finditer(pattern, new_content)
        count = len(list(re.finditer(pattern, new_content)))
        if count > 0:
            new_content = re.sub(pattern, replacement, new_content)
            fix_count += count
            print(f"✅ 修复了 {count} 处: {pattern[:50]}...")
    
    # 保存修复后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return new_content, fix_count

def main():
    """主函数"""
    print("🔧 FirstProject.html 位运算符修复工具\n")
    print("=" * 60)
    
    # 要修复的文件列表
    files_to_fix = [
        'en/firstproject.html',
        'jp/firstproject.html',
        'kr/firstproject.html',
        'firstproject.html',
    ]
    
    base_dir = '/Users/cavlinyeung/ai-bank-parser'
    total_fixes = 0
    
    for file_name in files_to_fix:
        file_path = os.path.join(base_dir, file_name)
        
        if not os.path.exists(file_path):
            print(f"⚠️  文件不存在: {file_name}")
            continue
        
        print(f"\n📄 处理文件: {file_name}")
        print("-" * 60)
        
        try:
            content, fix_count = fix_bitwise_operators(file_path)
            total_fixes += fix_count
            
            if fix_count > 0:
                print(f"\n✅ {file_name}: 修复了 {fix_count} 处错误")
            else:
                print(f"\n✅ {file_name}: 没有需要修复的错误")
                
        except Exception as e:
            print(f"\n❌ 处理 {file_name} 时出错: {e}")
    
    print("\n" + "=" * 60)
    print(f"\n🎉 完成！总共修复了 {total_fixes} 处位运算符错误")
    print("\n📝 修复摘要:")
    print("   - | 已替换为 ||")
    print("   - 所有文件都已创建备份")
    print("   - 可以直接使用修复后的文件")
    print("\n💡 下一步:")
    print("   1. 刷新浏览器页面")
    print("   2. 检查是否能正常显示30个文档")
    print("   3. 如有问题，可以从备份文件恢复")

if __name__ == '__main__':
    main()

