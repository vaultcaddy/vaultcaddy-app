#!/usr/bin/env python3
"""
批量修復所有頁面中的 Hero 區域問題
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_page(filename):
    print(f"\n處理 {filename}...")
    
    try:
        content = read_file(filename)
        original_length = len(content)
        
        # 查找 Hero 區域的開始
        # 從 <!-- 主要內容區域 --> 或 <!-- 🎨 全新 Hero 區域 --> 開始
        # 到 關鍵數據的結束 </div> 或實際內容開始
        
        # 方法1: 找到整個 Hero section 並替換
        pattern1 = r'<!-- 主要內容區域 -->\s*<main[^>]*>\s*<!-- 🎨 全新 Hero 區域 -->.*?</div>\s*</div>\s*</div>\s*(?=<!--|\s*<div class="dashboard-container"|<div class="main-content"|<main class="main-content"|<h1)'
        
        if re.search(pattern1, content, re.DOTALL):
            content = re.sub(pattern1, '<!-- 主要內容區域 -->\n    <main style="padding-top: 60px;">\n    ', content, flags=re.DOTALL)
            print(f"  ✅ 使用方法1修復")
        else:
            # 方法2: 只移除 section
            pattern2 = r'<section style="background: linear-gradient\(135deg.*?</div>\s*</div>\s*</div>\s*(?=<!--|\s*<div|<h1|<main)'
            if re.search(pattern2, content, re.DOTALL):
                content = re.sub(pattern2, '', content, flags=re.DOTALL)
                print(f"  ✅ 使用方法2修復")
            else:
                print(f"  ℹ️  沒有找到需要修復的內容")
                return False
        
        new_length = len(content)
        removed = original_length - new_length
        
        if removed > 0:
            print(f"  ✅ 已移除 {removed} 字符")
            write_file(filename, content)
            return True
        else:
            print(f"  ℹ️  沒有變化")
            return False
            
    except Exception as e:
        print(f"  ❌ 處理失敗: {e}")
        return False

# 要修復的文件
files = ['account.html', 'billing.html', 'privacy.html', 'terms.html']

fixed_count = 0
for filename in files:
    if fix_page(filename):
        fixed_count += 1

print(f"\n✅ 完成！成功修復 {fixed_count}/{len(files)} 個文件")

