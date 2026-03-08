#!/usr/bin/env python3
"""
修復 dashboard.html 和 firstproject.html
移除錯誤的 index.html 內容（紫色背景區域）
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 要修復的文件
files = ['dashboard.html', 'firstproject.html', 'account.html', 'billing.html']

for filename in files:
    print(f"\n處理 {filename}...")
    
    try:
        content = read_file(filename)
        original_length = len(content)
        
        # 查找並移除紫色背景 Hero 區域
        # 從 <section style="background: linear-gradient 開始
        # 到對應的 </section> 結束
        pattern = r'<section[^>]*background:\s*linear-gradient\([^)]+\)[^>]*>.*?</section>\s*'
        
        # 計算匹配次數
        matches = re.findall(pattern, content, re.DOTALL)
        match_count = len(matches)
        
        if match_count > 0:
            print(f"  找到 {match_count} 個紫色背景區域")
            
            # 移除匹配的內容
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            new_length = len(content)
            removed = original_length - new_length
            
            print(f"  ✅ 已移除 {removed} 字符")
            
            # 寫入文件
            write_file(filename, content)
            print(f"  ✅ {filename} 已更新")
        else:
            print(f"  ℹ️  沒有找到需要移除的內容")
            
    except Exception as e:
        print(f"  ❌ 處理失敗: {e}")

print("\n✅ 完成！")

