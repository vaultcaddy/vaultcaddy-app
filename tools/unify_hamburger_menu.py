#!/usr/bin/env python3
"""
統一所有頁面的漢堡菜單功能
從 index.html 複製漢堡菜單腳本到其他頁面
"""

import re

# 讀取 index.html 的漢堡菜單腳本
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# 提取漢堡菜單腳本（在 </body> 標籤之前）
hamburger_script_pattern = r'(    <!-- 🔥 漢堡菜單超級簡單修復方案 -->.*?</script>)'
match = re.search(hamburger_script_pattern, index_content, re.DOTALL)

if not match:
    print("❌ 找不到漢堡菜單腳本！")
    exit(1)

hamburger_script = match.group(1)
print(f"✅ 找到漢堡菜單腳本（{len(hamburger_script)} 字符）")

# 需要更新的頁面
pages = [
    'account.html',
    'billing.html',
    'firstproject.html',
    'dashboard.html',
    'privacy.html',
    'terms.html'
]

for page in pages:
    print(f"\n處理 {page}...")
    
    try:
        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已經有漢堡菜單腳本
        if '<!-- 🔥 漢堡菜單超級簡單修復方案 -->' in content:
            print(f"  ⚠️ {page} 已有漢堡菜單腳本，跳過")
            continue
        
        # 在 </body> 之前插入漢堡菜單腳本
        if '</body>' in content:
            content = content.replace('</body>', f'\n{hamburger_script}\n</body>')
            
            with open(page, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {page} 已添加漢堡菜單腳本")
        else:
            print(f"  ❌ {page} 找不到 </body> 標籤")
    
    except FileNotFoundError:
        print(f"  ❌ {page} 不存在")
    except Exception as e:
        print(f"  ❌ {page} 處理失敗: {e}")

print("\n✅ 完成！")

