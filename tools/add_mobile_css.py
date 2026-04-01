#!/usr/bin/env python3
"""
將 mobile-responsive.css 添加到所有頁面
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def add_mobile_css(filename):
    print(f"\n處理 {filename}...")
    
    try:
        content = read_file(filename)
        
        # 檢查是否已經有 mobile-responsive.css
        if 'mobile-responsive.css' in content:
            print(f"  ℹ️  已經包含 mobile-responsive.css，跳過")
            return False
        
        # 在 </head> 之前添加 CSS 鏈接
        css_link = '    <link rel="stylesheet" href="mobile-responsive.css">\n</head>'
        content = content.replace('</head>', css_link)
        
        write_file(filename, content)
        print(f"  ✅ 已添加 mobile-responsive.css")
        return True
        
    except Exception as e:
        print(f"  ❌ 處理失敗: {e}")
        return False

# 要更新的文件
files = [
    'index.html',
    'dashboard.html',
    'firstproject.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html'
]

success_count = 0
for filename in files:
    if add_mobile_css(filename):
        success_count += 1

print(f"\n✅ 完成！成功添加到 {success_count}/{len(files)} 個文件")

