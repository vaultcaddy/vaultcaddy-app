#!/usr/bin/env python3
"""
更新主要頁面使用統一認證系統
"""

import re
import os

# 需要更新的頁面
pages = [
    'dashboard.html',
    'account.html',
    'billing.html',
    'firstproject.html',
    'privacy.html',
    'terms.html'
]

def add_unified_auth(content):
    """添加 unified-auth.js"""
    if 'unified-auth.js' in content:
        print('  ✓ unified-auth.js 已存在')
        return content
    
    # 在 simple-data-manager.js 之後添加
    pattern = r'(<script[^>]*src="[^"]*simple-data-manager\.js[^"]*"[^>]*></script>)'
    replacement = r'\1\n    <script defer src="unified-auth.js?v=20251129"></script>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print('  ✓ 添加 unified-auth.js')
        return content
    
    # 如果找不到，嘗試在 simple-auth.js 之後
    pattern = r'(<script[^>]*src="[^"]*simple-auth\.js[^"]*"[^>]*></script>)'
    replacement = r'\1\n    <script defer src="unified-auth.js?v=20251129"></script>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print('  ✓ 在 simple-auth.js 後添加 unified-auth.js')
        return content
    
    print('  ⚠ 找不到合適的位置添加 unified-auth.js')
    return content

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
        
        # 添加統一認證腳本
        content = add_unified_auth(content)
        
        # 只在內容有變化時寫入
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  ✅ 更新完成')
            return True
        else:
            print(f'  ⏭️  無需更新')
            return False
    except Exception as e:
        print(f'  ❌ 處理時出錯: {e}')
        return False

def main():
    print('🚀 開始更新主要頁面...\n')
    
    success_count = 0
    for page in pages:
        if process_file(page):
            success_count += 1
    
    print(f'\n✅ 完成！成功更新 {success_count}/{len(pages)} 個文件')

if __name__ == '__main__':
    main()

