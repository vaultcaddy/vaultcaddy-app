#!/usr/bin/env python3
"""
更新所有頁面使用統一導航欄
1. 在 <body> 開頭添加 <div id="navbar-container"></div>
2. 移除現有的導航欄 HTML
3. 添加 load-unified-navbar.js 腳本
"""

import re
import os

# 需要更新的頁面
pages = [
    'index.html',
    'dashboard.html',
    'account.html',
    'billing.html',
    'firstproject.html',
    'privacy.html',
    'terms.html',
    'blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html'
]

def add_navbar_container(content):
    """在 <body> 後添加 navbar-container"""
    # 檢查是否已經有 navbar-container
    if 'id="navbar-container"' in content:
        print('  ✓ navbar-container 已存在')
        return content, False
    
    # 在 <body> 後添加
    pattern = r'(<body[^>]*>)'
    replacement = r'\1\n    <!-- 統一導航欄容器 -->\n    <div id="navbar-container"></div>\n'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content, count=1)
        print('  ✓ 添加 navbar-container')
        return content, True
    else:
        print('  ⚠ 找不到 <body> 標籤')
        return content, False

def remove_existing_navbar(content):
    """移除現有的導航欄 HTML"""
    # 移除 <nav class="vaultcaddy-navbar" ... </nav>
    # 使用非貪婪匹配，從 <nav 到對應的 </nav>
    pattern = r'<nav class="vaultcaddy-navbar"[^>]*>.*?</nav>\s*'
    
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        print(f'  ✓ 找到 {len(matches)} 個導航欄，移除中...')
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        return content, True
    else:
        print('  ⏭️  沒有找到需要移除的導航欄')
        return content, False

def remove_mobile_sidebar(content):
    """移除手機側邊欄（因為統一導航欄已包含）"""
    # 移除 overlay
    pattern1 = r'<div id="mobile-sidebar-overlay"[^>]*>.*?</div>\s*'
    # 移除 sidebar
    pattern2 = r'<aside id="mobile-sidebar"[^>]*>.*?</aside>\s*'
    
    changed = False
    
    if re.search(pattern1, content, re.DOTALL):
        content = re.sub(pattern1, '', content, flags=re.DOTALL)
        print('  ✓ 移除 mobile-sidebar-overlay')
        changed = True
    
    if re.search(pattern2, content, re.DOTALL):
        content = re.sub(pattern2, '', content, flags=re.DOTALL)
        print('  ✓ 移除 mobile-sidebar')
        changed = True
    
    if not changed:
        print('  ⏭️  沒有找到需要移除的手機側邊欄')
    
    return content, changed

def add_navbar_script(content, is_blog=False):
    """添加 load-unified-navbar.js 腳本"""
    # 檢查是否已經有
    if 'load-unified-navbar.js' in content:
        print('  ✓ load-unified-navbar.js 已存在')
        return content, False
    
    # 決定腳本路徑
    script_path = '../load-unified-navbar.js' if is_blog else 'load-unified-navbar.js'
    
    # 在 </body> 前添加
    pattern = r'(</body>)'
    replacement = f'    <script src="{script_path}?v=20251129"></script>\n\\1'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print(f'  ✓ 添加 {script_path}')
        return content, True
    else:
        print('  ⚠ 找不到 </body> 標籤')
        return content, False

def process_file(filepath):
    """處理單個文件"""
    print(f'\n處理: {filepath}')
    
    if not os.path.exists(filepath):
        print(f'  ⚠ 文件不存在')
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changed = False
        
        # 判斷是否為博客頁面
        is_blog = filepath.startswith('blog/')
        
        # 1. 添加 navbar-container
        content, c1 = add_navbar_container(content)
        changed = changed or c1
        
        # 2. 移除現有的導航欄
        content, c2 = remove_existing_navbar(content)
        changed = changed or c2
        
        # 3. 移除手機側邊欄
        content, c3 = remove_mobile_sidebar(content)
        changed = changed or c3
        
        # 4. 添加 navbar 腳本
        content, c4 = add_navbar_script(content, is_blog)
        changed = changed or c4
        
        # 只在內容有變化時寫入
        if changed or content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  ✅ 更新完成')
            return True
        else:
            print(f'  ⏭️  無需更新')
            return False
    except Exception as e:
        print(f'  ❌ 處理時出錯: {e}')
        import traceback
        traceback.print_exc()
        return False

def main():
    print('🚀 開始更新所有頁面使用統一導航欄...\n')
    print('=' * 60)
    print('目標：')
    print('  1. 添加 <div id="navbar-container"></div>')
    print('  2. 移除現有的導航欄 HTML')
    print('  3. 移除手機側邊欄（已包含在統一導航欄）')
    print('  4. 添加 load-unified-navbar.js 腳本')
    print('=' * 60)
    
    success_count = 0
    for page in pages:
        if process_file(page):
            success_count += 1
    
    print(f'\n✅ 完成！成功更新 {success_count}/{len(pages)} 個文件')
    print('\n📝 下一步：')
    print('  1. 檢查 unified-navbar.html 是否正確')
    print('  2. 測試各個頁面的導航欄顯示')
    print('  3. 提交並部署到 Firebase')

if __name__ == '__main__':
    main()

