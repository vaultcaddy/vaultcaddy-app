#!/usr/bin/env python3
"""
更新 /tc/ 目錄中所有 HTML 文件的鏈接
將相對鏈接更新為 /tc/ 路徑
"""

import os
import re
from pathlib import Path

# 需要更新的文件
TC_DIR = Path('tc')
HTML_FILES = [
    'home.html',
    'dashboard.html',
    'firstproject.html',
    'account.html',
    'billing.html',
    'privacy.html',
    'terms.html'
]

# 鏈接映射
LINK_MAPPINGS = {
    # 導航鏈接
    r'href="index\.html"': 'href="/tc/home.html"',
    r'href="dashboard\.html"': 'href="/tc/dashboard.html"',
    r'href="firstproject\.html"': 'href="/tc/firstproject.html"',
    r'href="account\.html"': 'href="/tc/account.html"',
    r'href="billing\.html"': 'href="/tc/billing.html"',
    r'href="privacy\.html"': 'href="/tc/privacy.html"',
    r'href="terms\.html"': 'href="/tc/terms.html"',
    
    # 帶 hash 的鏈接
    r'href="index\.html#features"': 'href="/tc/home.html#features"',
    r'href="index\.html#pricing"': 'href="/tc/home.html#pricing"',
    r'href="#pricing"': 'href="/tc/home.html#pricing"',
    
    # JavaScript 中的鏈接
    r"location\.href\s*=\s*['\"]index\.html['\"]": "location.href = '/tc/home.html'",
    r"location\.href\s*=\s*['\"]dashboard\.html['\"]": "location.href = '/tc/dashboard.html'",
    r"location\.href\s*=\s*['\"]account\.html['\"]": "location.href = '/tc/account.html'",
    r"location\.href\s*=\s*['\"]billing\.html['\"]": "location.href = '/tc/billing.html'",
    
    r"window\.location\.href\s*=\s*['\"]index\.html['\"]": "window.location.href = '/tc/home.html'",
    r"window\.location\.href\s*=\s*['\"]dashboard\.html['\"]": "window.location.href = '/tc/dashboard.html'",
    r"window\.location\.href\s*=\s*['\"]account\.html['\"]": "window.location.href = '/tc/account.html'",
    r"window\.location\.href\s*=\s*['\"]billing\.html['\"]": "window.location.href = '/tc/billing.html'",
}

def update_html_file(file_path):
    """更新單個 HTML 文件的鏈接"""
    print(f'\n處理文件: {file_path}')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_count = 0
    
    # 應用所有映射
    for pattern, replacement in LINK_MAPPINGS.items():
        matches = re.findall(pattern, content)
        if matches:
            print(f'  找到 {len(matches)} 個匹配: {pattern}')
            changes_count += len(matches)
        content = re.sub(pattern, replacement, content)
    
    # 如果有變更，寫入文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ 已更新 {changes_count} 個鏈接')
        return changes_count
    else:
        print(f'  ⚠️  沒有需要更新的鏈接')
        return 0

def main():
    print('🔄 開始更新 /tc/ 目錄中的鏈接...\n')
    
    total_changes = 0
    
    for html_file in HTML_FILES:
        file_path = TC_DIR / html_file
        if file_path.exists():
            changes = update_html_file(file_path)
            total_changes += changes
        else:
            print(f'❌ 文件不存在: {file_path}')
    
    print(f'\n✅ 完成！總共更新了 {total_changes} 個鏈接')

if __name__ == '__main__':
    main()

