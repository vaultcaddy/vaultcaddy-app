#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢復原始的 sidebar-component.js 和 navbar-component.js 系統
保留聯動功能但使用原來可工作的代碼
"""

import subprocess
import re

def restore_files_from_commit():
    """從 Git 歷史恢復文件"""
    # 從 9272129 提交恢復原始文件
    commit = '9272129'
    
    files_to_restore = [
        'sidebar-component.js',
        'navbar-component.js',
    ]
    
    for file in files_to_restore:
        try:
            # 使用 git show 獲取文件內容
            result = subprocess.run(
                ['git', 'show', f'{commit}:{file}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # 寫入文件
            with open(file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            print(f"✅ 已恢復 {file} (從提交 {commit})")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 恢復 {file} 失敗: {e}")

def update_html_files():
    """更新 HTML 文件使用原始組件"""
    html_files = [
        'dashboard.html',
        'account.html',
        'billing.html',
        'firstproject.html',
        'index.html',
    ]
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. 移除 unified 系統的腳本
            content = re.sub(
                r'<script src="load-unified-navbar\.js.*?"></script>\s*',
                '',
                content
            )
            content = re.sub(
                r'<script src="load-unified-sidebar\.js.*?"></script>\s*',
                '',
                content
            )
            
            # 2. 移除 div 容器
            content = re.sub(
                r'<div id="navbar-container"></div>\s*',
                '',
                content
            )
            content = re.sub(
                r'<div id="sidebar-container"></div>\s*',
                '',
                content
            )
            
            # 3. 添加回原始的 sidebar-component.js（在需要的頁面）
            if file_path in ['dashboard.html', 'account.html', 'billing.html', 'firstproject.html']:
                # 在 config.js 之後添加
                if 'sidebar-component.js' not in content:
                    content = re.sub(
                        r'(<script src="config\.js"></script>)',
                        r'\1\n    <script src="sidebar-component.js?v=20251105-table-optimize"></script>',
                        content
                    )
                
                # 添加 <aside class="sidebar"></aside>（如果不存在）
                if '<aside class="sidebar"></aside>' not in content:
                    # 在 main content 之前添加
                    content = re.sub(
                        r'(<main class="main-content")',
                        r'<aside class="sidebar"></aside>\n        \1',
                        content
                    )
            
            # 4. 添加回 navbar-component.js（所有頁面）
            if 'navbar-component.js' not in content:
                content = re.sub(
                    r'(<script src="config\.js"></script>)',
                    r'<script src="navbar-component.js?v=20251120-unified"></script>\n    \1',
                    content
                )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新 {file_path}")
            
        except Exception as e:
            print(f"❌ 更新 {file_path} 失敗: {e}")

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始恢復原始組件系統...")
    print("=" * 60)
    
    # 1. 從 Git 恢復原始文件
    print("\n1️⃣ 從 Git 歷史恢復原始組件文件...")
    restore_files_from_commit()
    
    # 2. 更新 HTML 文件
    print("\n2️⃣ 更新 HTML 文件使用原始組件...")
    update_html_files()
    
    print("\n" + "=" * 60)
    print("✅ 恢復完成！")
    print("=" * 60)
    print("\n📝 變更說明：")
    print("   - 恢復 sidebar-component.js（可工作的版本）")
    print("   - 恢復 navbar-component.js（可工作的版本）")
    print("   - 移除 unified-navbar.html 和 unified-sidebar.html 系統")
    print("   - 保留聯動功能：修改組件文件會影響所有頁面")

if __name__ == '__main__':
    main()

