#!/usr/bin/env python3
"""
更新 dashboard.html, firstproject.html, account.html, billing.html 的導航欄
使其與 index.html 的導航欄一致（包括漢堡菜單和手機版優化）
"""

import re

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 讀取 index.html 的導航欄
print("讀取 index.html...")
index_html = read_file('index.html')

# 提取導航欄（從 <!-- ✅ 統一靜態導航欄 --> 到 </nav>）
nav_pattern = r'(<!-- ✅ 統一靜態導航欄.*?</nav>)'
nav_match = re.search(nav_pattern, index_html, re.DOTALL)
if not nav_match:
    print("❌ 找不到導航欄")
    exit(1)

new_navbar = nav_match.group(1)
print(f"✅ 提取導航欄: {len(new_navbar)} 字符")

# 提取手機側邊欄
sidebar_pattern = r'(<!-- 手機側邊欄菜單 -->.*?<!-- 側邊欄遮罩 -->.*?</div>)'
sidebar_match = re.search(sidebar_pattern, index_html, re.DOTALL)
sidebar_html = sidebar_match.group(1) if sidebar_match else ''
print(f"✅ 提取側邊欄: {len(sidebar_html)} 字符")

# 提取用戶下拉菜單
dropdown_pattern = r'(<div id="user-dropdown".*?</div>\s*</div>\s*</div>)'
dropdown_match = re.search(dropdown_pattern, index_html, re.DOTALL)
dropdown_html = dropdown_match.group(1) if dropdown_match else ''
print(f"✅ 提取下拉菜單: {len(dropdown_html)} 字符")

# 提取漢堡菜單 JavaScript
js_pattern = r'(// ==================== 漢堡菜單功能.*?}\)\(\);)'
js_match = re.search(js_pattern, index_html, re.DOTALL)
hamburger_js = js_match.group(1) if js_match else ''
print(f"✅ 提取漢堡菜單 JS: {len(hamburger_js)} 字符")

# 提取響應式 CSS
css_pattern = r'(@media \(max-width: 768px\) \{.*?/\* 隱藏桌面版 Logo 和文字 \*/.*?display: none !important;.*?\})'
css_match = re.search(css_pattern, index_html, re.DOTALL)
mobile_css = css_match.group(1) if css_match else ''
print(f"✅ 提取響應式 CSS: {len(mobile_css)} 字符")

# 要更新的文件列表
files_to_update = [
    'dashboard.html',
    'firstproject.html',
    'account.html',
    'billing.html'
]

for filename in files_to_update:
    print(f"\n處理 {filename}...")
    
    try:
        content = read_file(filename)
        
        # 1. 替換導航欄
        # 找到現有的導航欄並替換
        old_nav_pattern = r'<nav class="vaultcaddy-navbar".*?</nav>'
        if re.search(old_nav_pattern, content, re.DOTALL):
            content = re.sub(old_nav_pattern, new_navbar, content, flags=re.DOTALL)
            print(f"  ✅ 已替換導航欄")
        else:
            print(f"  ⚠️  找不到舊導航欄")
        
        # 2. 添加/更新手機側邊欄（如果不存在）
        if '<!-- 手機側邊欄菜單 -->' not in content and sidebar_html:
            # 在導航欄後添加
            content = content.replace('</nav>', f'</nav>\n    \n    {sidebar_html}')
            print(f"  ✅ 已添加手機側邊欄")
        elif sidebar_html:
            # 替換現有的
            old_sidebar_pattern = r'<!-- 手機側邊欄菜單 -->.*?<!-- 側邊欄遮罩 -->.*?</div>'
            if re.search(old_sidebar_pattern, content, re.DOTALL):
                content = re.sub(old_sidebar_pattern, sidebar_html, content, flags=re.DOTALL)
                print(f"  ✅ 已更新手機側邊欄")
        
        # 3. 添加/更新用戶下拉菜單（如果不存在）
        if '<div id="user-dropdown"' not in content and dropdown_html:
            # 在側邊欄遮罩後添加
            if '<!-- 側邊欄遮罩 -->' in content:
                sidebar_overlay_end = content.find('</div>', content.find('<!-- 側邊欄遮罩 -->'))
                if sidebar_overlay_end != -1:
                    content = content[:sidebar_overlay_end+6] + f'\n    \n    {dropdown_html}' + content[sidebar_overlay_end+6:]
                    print(f"  ✅ 已添加用戶下拉菜單")
        elif dropdown_html:
            # 替換現有的
            old_dropdown_pattern = r'<div id="user-dropdown".*?</div>\s*</div>\s*</div>'
            if re.search(old_dropdown_pattern, content, re.DOTALL):
                content = re.sub(old_dropdown_pattern, dropdown_html, content, flags=re.DOTALL)
                print(f"  ✅ 已更新用戶下拉菜單")
        
        # 4. 添加/更新漢堡菜單 JavaScript
        if hamburger_js:
            if '// ==================== 漢堡菜單功能' not in content:
                # 在 </script> 前添加
                last_script = content.rfind('</script>')
                if last_script != -1:
                    content = content[:last_script] + f'\n        {hamburger_js}\n        ' + content[last_script:]
                    print(f"  ✅ 已添加漢堡菜單 JS")
            else:
                # 替換現有的
                old_js_pattern = r'// ==================== 漢堡菜單功能.*?}\)\(\);'
                if re.search(old_js_pattern, content, re.DOTALL):
                    content = re.sub(old_js_pattern, hamburger_js, content, flags=re.DOTALL)
                    print(f"  ✅ 已更新漢堡菜單 JS")
        
        # 5. 添加/更新響應式 CSS
        if mobile_css:
            if '@media (max-width: 768px)' not in content:
                # 在 </style> 前添加
                last_style = content.rfind('</style>')
                if last_style != -1:
                    content = content[:last_style] + f'\n        {mobile_css}\n        ' + content[last_style:]
                    print(f"  ✅ 已添加響應式 CSS")
            else:
                # 更新現有的（只更新導航欄相關的部分）
                print(f"  ℹ️  響應式 CSS 已存在，跳過")
        
        # 寫入文件
        write_file(filename, content)
        print(f"✅ {filename} 更新完成")
        
    except Exception as e:
        print(f"❌ 處理 {filename} 時出錯: {e}")

print("\n✅ 所有文件更新完成！")

