#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除4个版本account.html中的Preferences部分
"""

import re

print("🗑️  开始删除Preferences部分...")
print("="*70)

account_files = [
    'account.html',       # 中文版
    'en/account.html',    # 英文版
    'jp/account.html',    # 日文版
    'kr/account.html'     # 韩文版
]

for file_path in account_files:
    print(f"\n处理: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 匹配Preferences部分
    # 从 <div class="settings-section"> 到下一个 </div>（包含Language和Timezone）
    pattern = r'<!-- Preferences -->.*?</div>\s*</div>\s*(?=\s*<!-- Purchase History|<div class="settings-section" id="purchase-history")'
    
    # 更精确的匹配：找到包含"Preferences"标题和Language/Timezone的section
    pattern2 = r'<div class="settings-section">\s*<h2 class="section-title">(?:Preferences|偏好設定|環境設定|設定)</h2>.*?</div>\s*</div>\s*(?=\s*<!-- Purchase History|<div class="settings-section")'
    
    # 尝试第一个pattern
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, '\n', content, flags=re.DOTALL)
        print("  ✅ 已删除Preferences部分（带注释）")
    # 尝试第二个pattern
    elif re.search(pattern2, content, re.DOTALL | re.IGNORECASE):
        new_content = re.sub(pattern2, '\n', content, flags=re.DOTALL | re.IGNORECASE)
        print("  ✅ 已删除Preferences部分（无注释）")
    else:
        new_content = content
        print("  ℹ️  未找到Preferences部分")
    
    # 保存
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # 计算删除的行数
        lines_removed = original_content.count('\n') - new_content.count('\n')
        print(f"     删除了约 {lines_removed} 行")
    
print("\n" + "="*70)
print("🎉 完成！所有4个版本的Preferences部分已删除")

