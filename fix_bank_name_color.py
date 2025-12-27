#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复银行名称颜色：改为白色，在红色背景上更清晰"""

import glob
import re

def fix_bank_name_color(file_path):
    """修复银行名称颜色"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # ========== 修复bank-logo中的颜色 ==========
        # 查找并替换bank-logo中的颜色
        # 从红色改为白色
        bank_logo_pattern = r'(<div class="bank-logo"[^>]*>\s*<strong style="color: )#CC092F(; font-size: 1\.8rem;">)([^<]+)(<br><span style="font-size: 0\.7em; font-weight: 400; color: )#999(;">)'
        
        def replace_colors(match):
            return (
                match.group(1) + 
                'white' +  # 中文名称改为白色
                match.group(2) +
                match.group(3) +
                match.group(4) +
                'rgba(255,255,255,0.7)' +  # 英文名称改为半透明白色
                match.group(5)
            )
        
        content = re.sub(bank_logo_pattern, replace_colors, content)
        
        if content != original:
            changes.append('修改银行名称颜色为白色')
            
            with open(file_path + '.backup_color', 'w', encoding='utf-8') as f:
                f.write(original)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        else:
            return False, ['未找到需要修改的颜色']
        
    except Exception as e:
        return False, [f'错误: {str(e)}']

# 获取所有银行页面
patterns = [
    'bochk-bank-statement.html',
    'hsbc-bank-statement.html',
    'hangseng-bank-statement.html',
    'dbs-bank-statement.html',
    'sc-bank-statement.html',
    'citibank-bank-statement.html',
    'bankcomm-bank-statement.html',
]

all_files = patterns

print("=" * 70)
print("🔧 修复银行名称颜色（改为白色）")
print("=" * 70)
print()
print(f"处理 {len(all_files)} 个文件")
print()

processed = 0

for i, file_path in enumerate(all_files, 1):
    success, messages = fix_bank_name_color(file_path)
    
    if success:
        processed += 1
        print(f"✅ [{i}/{len(all_files)}] {file_path}")
        print(f"   {', '.join(messages)}")
    else:
        print(f"⏭️  [{i}/{len(all_files)}] {file_path} - {messages[0]}")

print()
print("=" * 70)
print(f"✅ 已处理：{processed}/{len(all_files)} 个文件")
print("🎉 完成！")

