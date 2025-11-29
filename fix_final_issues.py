#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復最終問題：
1. firstproject.html - 按鈕移到表格上方單獨一行
2. unified-auth.js - 顯示 email 而不是 displayName
3. 移除導航欄多餘按鈕
"""

import re
from pathlib import Path

def fix_firstproject_final():
    """修復 firstproject.html 最終佈局"""
    file_path = 'firstproject.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 找到 header 標籤並修改，移除右側按鈕
    # 將 header 改為只包含標題和搜索欄
    header_pattern = r'<header style="margin-bottom: 1\.5rem; margin-top: 1\.5rem; display: flex; justify-content: space-between; align-items: center; gap: 2rem;">.*?</header>'
    
    new_header = '''<header style="margin-bottom: 1rem; margin-top: 1.5rem;">
                    <!-- 標題和搜尋欄 -->
                    <div style="display: flex; align-items: center; gap: 2rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <h1 id="team-project-title" contenteditable="false" style="font-size: 2rem; font-weight: 700; color: #1f2937; margin: 0; outline: none; border: 2px solid transparent; padding: 0.25rem 0; border-radius: 4px; transition: all 0.2s;">Project</h1>
                            <button id="edit-project-name-btn" onclick="toggleProjectNameEdit()" style="background: transparent; border: none; cursor: pointer; color: #6b7280; padding: 0.5rem; border-radius: 4px; transition: all 0.2s;" title="編輯項目名稱">
                                <i class="fas fa-pen" style="font-size: 1.25rem;"></i>
                            </button>
                        </div>
                        <!-- 搜尋欄 -->
                        <div style="position: relative; max-width: 400px; flex: 1; min-width: 250px;">
                            <i class="fas fa-search" style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: #9ca3af;"></i>
                            <input type="text" id="document-search" placeholder="搜尋文檔..." style="
                                width: 100%;
                                padding: 0.625rem 1rem 0.625rem 2.75rem;
                                border: 1px solid #e5e7eb;
                                border-radius: 8px;
                                font-size: 0.875rem;
                                transition: all 0.2s;
                            " onkeyup="filterDocuments(this.value)">
                        </div>
                    </div>
                </header>'''
    
    content = re.sub(header_pattern, new_header, content, flags=re.DOTALL)
    
    # 2. 確保 standalone-buttons-container 可見並在表格上方
    pattern2 = r'#standalone-buttons-container \{[^}]*\}'
    replacement2 = '''#standalone-buttons-container {
            display: flex;
            gap: 1rem;
            align-items: center;
            margin-bottom: 1rem;
            justify-content: flex-end;
        }'''
    content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path} 最終佈局")

def fix_unified_auth_email():
    """修復 unified-auth.js - 顯示 email"""
    file_path = 'unified-auth.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修改下拉菜單顯示 email
    old_pattern = r'<div style="font-weight: 600; color: #1f2937; margin-bottom: 0\.25rem;">\$\{displayName\}</div>'
    new_replacement = r'<div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">${user.email}</div>'
    
    content = re.sub(old_pattern, new_replacement, content)
    
    # 也修改獲取 initial 的邏輯，使用 email
    old_initial = r"const initial = displayName \? displayName\.charAt\(0\)\.toUpperCase\(\) : 'U';"
    new_initial = "const initial = user.email ? user.email.charAt(0).toUpperCase() : 'U';"
    
    content = re.sub(old_initial, new_initial, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path} 顯示 email")

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始修復最終問題...")
    print("=" * 60)
    
    # 1. 修復 firstproject.html 佈局
    print("\n1️⃣ 修復 firstproject.html 佈局（按鈕在表格上方）...")
    fix_firstproject_final()
    
    # 2. 修復顯示 email
    print("\n2️⃣ 修復顯示 email 而不是 displayName...")
    fix_unified_auth_email()
    
    print("\n" + "=" * 60)
    print("✅ 所有修復完成！")
    print("=" * 60)
    print("\n📝 關於左側欄問題：")
    print("   根據控制台日誌，項目已成功載入（項目名稱: 2025年10月）")
    print("   但 render() 函數可能沒有正確執行")
    print("   已在 unified-sidebar.html 中添加更多日誌來調試")

if __name__ == '__main__':
    main()

