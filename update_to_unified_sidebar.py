#!/usr/bin/env python3
"""
更新頁面使用統一側邊欄
1. Dashboard/Account/Billing/FirstProject 使用 unified-sidebar.html
2. 博客頁面使用 unified-blog-sidebar.html
3. 添加 sidebar-container 和 load-unified-sidebar.js
"""

import re
import os

# 需要應用側邊欄的頁面
app_pages = [
    'dashboard.html',
    'account.html',
    'billing.html',
    'firstproject.html'
]

blog_pages = [
    'blog/how-to-convert-pdf-bank-statement-to-excel.html',
    'blog/ai-invoice-processing-guide.html',
    'blog/best-pdf-to-excel-converter.html',
    'blog/ocr-technology-for-accountants.html',
    'blog/automate-financial-documents.html'
]

def add_sidebar_container(content):
    """在 navbar-container 後添加 sidebar-container"""
    # 檢查是否已經有
    if 'id="sidebar-container"' in content:
        print('  ✓ sidebar-container 已存在')
        return content, False
    
    # 在 navbar-container 後添加
    pattern = r'(<div id="navbar-container"></div>)'
    replacement = r'\1\n    <div id="sidebar-container"></div>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print('  ✓ 添加 sidebar-container')
        return content, True
    else:
        print('  ⚠ 找不到 navbar-container')
        return content, False

def remove_existing_sidebar(content):
    """移除現有的側邊欄 HTML"""
    # 移除 <aside ... </aside>
    # 需要小心不要移除手機側邊欄（已經在 unified-navbar.html 中）
    
    # 嘗試移除左側欄（非 mobile-sidebar）
    patterns = [
        r'<aside(?:(?!id="mobile-sidebar")[^>])*?>.*?</aside>\s*',  # 不包含 mobile-sidebar 的 aside
        r'<div class="blog-sidebar">.*?</div>\s*',  # 博客側邊欄的特殊 div
    ]
    
    changed = False
    for pattern in patterns:
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            # 只移除包含側邊欄特徵的 aside
            for match in matches:
                if ('sidebar' in match.lower() or '側邊欄' in match or '文章導航' in match or '儀表板' in match) and 'mobile-sidebar' not in match:
                    content = content.replace(match, '', 1)
                    print(f'  ✓ 移除側邊欄 HTML ({len(match)} 字符)')
                    changed = True
    
    if not changed:
        print('  ⏭️  沒有找到需要移除的側邊欄')
    
    return content, changed

def add_sidebar_script(content, is_blog=False):
    """添加 load-unified-sidebar.js 腳本"""
    # 檢查是否已經有
    if 'load-unified-sidebar.js' in content:
        print('  ✓ load-unified-sidebar.js 已存在')
        return content, False
    
    # 決定腳本路徑
    script_path = '../load-unified-sidebar.js' if is_blog else 'load-unified-sidebar.js'
    
    # 在 </body> 前添加（或在 load-unified-navbar.js 後）
    if 'load-unified-navbar.js' in content:
        # 在 load-unified-navbar.js 後添加
        pattern = r'(<script src="[^"]*load-unified-navbar\.js[^"]*"></script>)'
        replacement = f'\\1\n    <script src="{script_path}?v=20251129"></script>'
        content = re.sub(pattern, replacement, content)
        print(f'  ✓ 在 navbar 腳本後添加 {script_path}')
        return content, True
    else:
        # 在 </body> 前添加
        pattern = r'(</body>)'
        replacement = f'    <script src="{script_path}?v=20251129"></script>\n\\1'
        content = re.sub(pattern, replacement, content)
        print(f'  ✓ 在 </body> 前添加 {script_path}')
        return content, True

def adjust_main_content_margin(content):
    """調整主內容區域的 margin-left 以適應側邊欄"""
    # 查找 main 或 .blog-container 的樣式
    # 確保有足夠的 margin-left 來避免被側邊欄遮擋
    
    # 博客頁面
    if 'blog-container' in content:
        pattern = r'\.blog-container\s*\{[^}]*margin-left:\s*\d+px'
        match = re.search(pattern, content)
        if match:
            old_text = match.group(0)
            new_text = re.sub(r'margin-left:\s*\d+px', 'margin-left: 280px', old_text)
            content = content.replace(old_text, new_text)
            print('  ✓ 調整 blog-container margin-left')
            return content, True
    
    # 應用頁面
    if '<main' in content:
        # 查找 main 標籤的 style
        pattern = r'<main[^>]*style="[^"]*margin-left:\s*\d+px[^"]*"'
        match = re.search(pattern, content)
        if match:
            old_text = match.group(0)
            new_text = re.sub(r'margin-left:\s*\d+px', 'margin-left: 280px', old_text)
            content = content.replace(old_text, new_text)
            print('  ✓ 調整 main margin-left')
            return content, True
    
    print('  ⏭️  無需調整 margin-left')
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
        
        # 1. 添加 sidebar-container
        content, c1 = add_sidebar_container(content)
        changed = changed or c1
        
        # 2. 移除現有的側邊欄
        content, c2 = remove_existing_sidebar(content)
        changed = changed or c2
        
        # 3. 添加 sidebar 腳本
        content, c3 = add_sidebar_script(content, is_blog)
        changed = changed or c3
        
        # 4. 調整主內容 margin
        content, c4 = adjust_main_content_margin(content)
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
    print('🚀 開始更新所有頁面使用統一側邊欄...\n')
    print('=' * 60)
    print('目標：')
    print('  1. 添加 <div id="sidebar-container"></div>')
    print('  2. 移除現有的側邊欄 HTML')
    print('  3. 添加 load-unified-sidebar.js 腳本')
    print('  4. 調整主內容區域的 margin-left')
    print('=' * 60)
    
    success_count = 0
    
    print('\n--- 應用頁面（Dashboard/Account/Billing/FirstProject）---')
    for page in app_pages:
        if process_file(page):
            success_count += 1
    
    print('\n--- 博客頁面 ---')
    for page in blog_pages:
        if process_file(page):
            success_count += 1
    
    total = len(app_pages) + len(blog_pages)
    print(f'\n✅ 完成！成功更新 {success_count}/{total} 個文件')
    print('\n📝 下一步：')
    print('  1. 檢查 unified-sidebar.html 和 unified-blog-sidebar.html')
    print('  2. 測試各個頁面的側邊欄顯示')
    print('  3. 提交並部署到 Firebase')

if __name__ == '__main__':
    main()

