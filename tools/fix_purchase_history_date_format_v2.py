#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一修复4个版本account.html中Purchase History的日期格式
将所有语言的年月格式统一改为"MM/YYYY"格式
"""

import re

files = [
    ('account.html', 'zh', '年', '月'),        # 中文版
    ('en/account.html', 'en', 'year', 'month'),  # 英文版
    ('jp/account.html', 'jp', '年', '月'),      # 日文版
    ('kr/account.html', 'kr', '년', '월')       # 韩文版
]

print("🔧 开始修复Purchase History日期格式...")
print("="*70)

for file_path, lang, year_text, month_text in files:
    print(f"\n处理: {file_path} ({lang})")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复1: 月份选项显示格式 (JavaScript代码中)
    # 匹配各种格式:
    # ${year}year${parseInt(month)}month (英文)
    # ${year}年${parseInt(month)}月 (中文/日文)
    # ${year}년${parseInt(month)}월 (韩文)
    # 统一改为: ${parseInt(month)}/${year}
    
    patterns = [
        (rf'option\.textContent = `\${{year}}{year_text}\${{parseInt\(month\)}}{month_text}`;',
         r'option.textContent = `${parseInt(month)}/${year}`;'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # 修复2: Console log中的日期格式
    # 各种语言的console.log
    log_patterns = [
        (r'console\.log\(`📅 filter \$\{year\}year\$\{month\}month 的record`\);',
         r'console.log(`📅 Filter records for ${month}/${year}`);'),
        (r'console\.log\(`📅 filter \$\{year\}年\$\{month\}月 的record`\);',
         r'console.log(`📅 Filter records for ${month}/${year}`);'),
        (r'console\.log\(`📅 filter \$\{year\}년\$\{month\}월 의 record`\);',
         r'console.log(`📅 Filter records for ${month}/${year}`);'),
        (r'console\.log\(`📅 フィルター \$\{year\}年\$\{month\}月 的record`\);',
         r'console.log(`📅 Filter records for ${month}/${year}`);'),
    ]
    
    for pattern, replacement in log_patterns:
        content = re.sub(pattern, replacement, content)
    
    # 修复3: HTML中显示的日期
    # 2025年11月4日 / 2025year11month4日 -> 11/04/2025
    date_patterns = [
        (r'2025年(\d+)月(\d+)日', r'\1/\2/2025'),
        (r'2025year(\d+)month(\d+)日', r'\1/\2/2025'),
        (r'2025년(\d+)월(\d+)일', r'\1/\2/2025'),
    ]
    
    for pattern, replacement in date_patterns:
        content = re.sub(pattern, replacement, content)
    
    # 修复4: Placeholder中的日期示例
    placeholder_patterns = [
        (r'(for example|例如|例：|例如：|예：)：2025年1月Invoice', r'\1: 01/2025 Invoice'),
        (r'(for example|例如|例：|例如：|예：)：2025year1monthInvoice', r'\1: 01/2025 Invoice'),
        (r'(for example|例如|例：|例如：|예：)：2025년1월Invoice', r'\1: 01/2025 Invoice'),
    ]
    
    for pattern, replacement in placeholder_patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 已更新")
        
        # 显示变化的行数
        changes = sum(1 for a, b in zip(original_content.split('\n'), content.split('\n')) if a != b)
        print(f"     修改了 {changes} 行")
    else:
        print(f"  ℹ️  无需更改")

print("\n" + "="*70)
print("🎉 完成！所有4个版本的日期格式已统一为 MM/YYYY 格式")
print("\n修改示例:")
print("  Before:")
print("    中文: 2025年12月")
print("    英文: 2025year12month")
print("    日文: 2025年12月")
print("    韩文: 2025년12월")
print("\n  After:")
print("    统一: 12/2025")

