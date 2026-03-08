#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一修复4个版本account.html中Purchase History的日期格式
将"2025year12month"改为"12/2025"格式
"""

import re

files = [
    'account.html',       # 中文版
    'en/account.html',    # 英文版
    'jp/account.html',    # 日文版
    'kr/account.html'     # 韩文版
]

print("🔧 开始修复Purchase History日期格式...")
print("="*70)

for file_path in files:
    print(f"\n处理: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复1: 月份选项显示格式 (JavaScript代码中)
    # 从 `${year}year${parseInt(month)}month` 改为 `${parseInt(month)}/${year}`
    content = re.sub(
        r'option\.textContent = `\$\{year\}year\$\{parseInt\(month\)\}month`;',
        r'option.textContent = `${parseInt(month)}/${year}`;',
        content
    )
    
    # 修复2: Console log中的日期格式
    # 从 console.log(`📅 filter ${year}year${month}month 的record`);
    # 改为 console.log(`📅 Filter records for ${month}/${year}`);
    content = re.sub(
        r'console\.log\(`📅 filter \$\{year\}year\$\{month\}month 的record`\);',
        r'console.log(`📅 Filter records for ${month}/${year}`);',
        content
    )
    
    # 修复3: HTML中显示的日期（如果有）
    # 2025year11month4日 -> 11/04/2025
    content = re.sub(
        r'2025year(\d+)month(\d+)日',
        r'\1/\2/2025',
        content
    )
    
    # 修复4: Placeholder中的日期示例
    # for example：2025year1monthInvoice -> for example: 01/2025 Invoice
    content = re.sub(
        r'(for example|例如|例：|例如：)：2025year1monthInvoice',
        r'\1: 01/2025 Invoice',
        content
    )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 已更新")
    else:
        print(f"  ℹ️  无需更改")

print("\n" + "="*70)
print("🎉 完成！所有4个版本的日期格式已统一为 MM/YYYY 格式")
print("\n修改内容:")
print("  1. Purchase History月份选择器: 12/2025")
print("  2. Console日志: Filter records for 12/2025")
print("  3. 重置日期显示: 11/04/2025")
print("  4. 示例文本: 01/2025 Invoice")

