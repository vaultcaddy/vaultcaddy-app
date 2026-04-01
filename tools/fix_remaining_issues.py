#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復剩餘問題：
1. unified-auth.js - 修改用戶下拉菜單（刪除儀表板，動態 Credits）
2. firstproject.html - 刪除右上角重複按鈕，調整佈局
"""

import re
from pathlib import Path

def fix_unified_auth():
    """修復 unified-auth.js 用戶下拉菜單"""
    file_path = 'unified-auth.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到並替換下拉菜單 HTML
    old_dropdown_pattern = r'<div id="user-dropdown"[^>]*>.*?</div>\s*</div>'
    
    new_dropdown = '''<div id="user-dropdown" style="display: none; position: absolute; top: 50px; right: 0; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); min-width: 200px; z-index: 1000; border: 1px solid #e5e7eb;">
                            <div style="padding: 1rem; border-bottom: 1px solid #e5e7eb;">
                                <div style="font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">${displayName}</div>
                                <div style="font-size: 0.75rem; color: #6b7280;">Credits: ${credits}</div>
                            </div>
                            <a href="/account.html" style="display: block; padding: 0.75rem 1rem; color: #374151; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">
                                <i class="fas fa-user" style="margin-right: 0.5rem; color: #667eea;"></i>
                                帳戶設定
                            </a>
                            <a href="/billing.html" style="display: block; padding: 0.75rem 1rem; color: #374151; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">
                                <i class="fas fa-credit-card" style="margin-right: 0.5rem; color: #667eea;"></i>
                                計費
                            </a>
                            <div style="border-top: 1px solid #e5e7eb; margin: 0.5rem 0;"></div>
                            <a href="#" onclick="event.preventDefault(); handleLogout();" style="display: block; padding: 0.75rem 1rem; color: #ef4444; text-decoration: none; transition: background 0.2s;" onmouseover="this.style.background='#fef2f2'" onmouseout="this.style.background='transparent'">
                                <i class="fas fa-sign-out-alt" style="margin-right: 0.5rem;"></i>
                                登出
                            </a>
                        </div>
                    </div>'''
    
    content = re.sub(old_dropdown_pattern, new_dropdown, content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path} 用戶下拉菜單")

def fix_firstproject_layout():
    """修復 firstproject.html 佈局"""
    file_path = 'firstproject.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 刪除 header 中的右側按鈕區域
    # 找到 <!-- 右側：操作按鈕 --> 到 </header> 之間的內容並刪除
    pattern1 = r'<!-- 右側：操作按鈕 -->.*?</div>\s*</header>'
    replacement1 = '</div>\n                </header>'
    content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # 2. 修改標題區域的 flexbox 佈局，使標題、搜索欄和按鈕在同一行
    # 找到 header 標籤並修改其樣式
    pattern2 = r'<header style="margin-bottom: 2rem; margin-top: 1\.5rem; display: flex; justify-content: space-between; align-items: center;">'
    replacement2 = '<header style="margin-bottom: 1.5rem; margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; gap: 2rem;">'
    content = re.sub(pattern2, replacement2, content)
    
    # 3. 調整 standalone-buttons-container 的 margin-bottom
    pattern3 = r'#standalone-buttons-container \{[^}]*\}'
    replacement3 = '''#standalone-buttons-container {
            display: none; /* 隱藏獨立按鈕區域 */
        }'''
    content = re.sub(pattern3, replacement3, content, flags=re.DOTALL)
    
    # 4. 在 header 中的搜索欄後面直接添加按鈕
    # 找到搜索欄的結束位置
    search_pattern = r'(</div>\s*</div>\s*</div>\s*</div>\s*</header>)'
    
    buttons_html = '''
                        </div>
                    </div>
                    
                    <!-- 操作按鈕（與標題同一行）-->
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <button id="upload-btn" onclick="openUploadModal()" style="background: #8b5cf6; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500; white-space: nowrap;">
                            <span>Upload files</span>
                            <i class="fas fa-arrow-right"></i>
                        </button>
                        <div class="dropdown" id="export-dropdown" style="position: relative;">
                            <button id="export-btn" onclick="toggleExportMenu()" style="background: #10b981; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500; white-space: nowrap;">
                                <i class="fas fa-download"></i>
                                <span>Export</span>
                                <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i>
                            </button>
                        </div>
                        <button onclick="deleteSelectedDocuments()" id="delete-selected-btn" disabled style="background: #ef4444; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-weight: 500; opacity: 0.5; white-space: nowrap;">
                            <i class="fas fa-trash"></i>
                            <span>Delete</span>
                            <span id="delete-count" style="display: none;"></span>
                        </button>
                    </div>
                </header>'''
    
    content = re.sub(search_pattern, buttons_html, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path} 佈局")

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始修復剩餘問題...")
    print("=" * 60)
    
    # 1. 修復用戶下拉菜單
    print("\n1️⃣ 修復用戶下拉菜單...")
    fix_unified_auth()
    
    # 2. 修復 firstproject.html 佈局
    print("\n2️⃣ 修復 firstproject.html 佈局...")
    fix_firstproject_layout()
    
    print("\n" + "=" * 60)
    print("✅ 所有修復完成！")
    print("=" * 60)
    print("\n📝 注意：左側欄文件夾顯示問題可能需要檢查瀏覽器控制台")

if __name__ == '__main__':
    main()

