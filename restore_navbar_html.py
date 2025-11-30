#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢復靜態導航欄 HTML 結構
從 Git commit 9272129 獲取原始導航欄 HTML
"""

import subprocess
import re

# 靜態導航欄 HTML（從原始版本複製）
NAVBAR_HTML = '''
    <!-- ✅ 統一靜態導航欄 -->
    <nav class="vaultcaddy-navbar" id="main-navbar" style="position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #ffffff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 2rem; z-index: 1000; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <!-- 漢堡菜單按鈕（僅手機顯示）-->
            <button id="mobile-menu-btn" style="display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; color: #1f2937; font-size: 1.5rem; -webkit-tap-highlight-color: rgba(0,0,0,0.1); touch-action: manipulation;">
                <i class="fas fa-bars" style="pointer-events: none;"></i>
            </button>
            
            <a href="/index.html" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: #1f2937; font-weight: 600; font-size: 1.125rem;">
                <div class="desktop-logo" style="width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1.25rem;">
                    V
                </div>
                <div class="desktop-logo-text">
                    <div>VaultCaddy</div>
                    <div style="font-size: 0.75rem; color: #6b7280; font-weight: 400; text-transform: uppercase; letter-spacing: 0.05em;">AI DOCUMENT PROCESSING</div>
                </div>
            </a>
        </div>
        <div style="display: flex; align-items: center; gap: 2rem;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <a href="/index.html#features" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">功能</a>
                <a href="/index.html#pricing" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">價格</a>
                <a href="/dashboard.html" style="color: #4b5563; text-decoration: none; font-size: 0.9375rem; font-weight: 500; transition: color 0.2s;">儀表板</a>
            </div>
            <div id="user-menu" style="position: relative; display: flex; align-items: center; gap: 0.75rem;">
                <!-- 初始狀態：登入按鈕 -->
                <button onclick="window.location.href='/auth.html'" style="padding: 0.5rem 1rem; background: #8b5cf6; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.875rem;" onmouseover="this.style.background='#7c3aed'" onmouseout="this.style.background='#8b5cf6'">登入</button>
            </div>
        </div>
    </nav>
    
    <!-- 手機側邊欄菜單 -->
    <div id="mobile-sidebar-overlay" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; opacity: 0; transition: opacity 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);"></div>
    <div id="mobile-sidebar" style="display: none; position: fixed; top: 0; left: 0; height: 100%; width: 280px; max-width: 80%; background: #ffffff; z-index: 1001; box-shadow: 2px 0 10px rgba(0,0,0,0.1); transform: translateX(-100%); transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94); will-change: transform;">
        <div style="padding: 1.5rem; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between;">
            <a href="/index.html" style="display: flex; align-items: center; gap: 0.75rem; text-decoration: none; color: #1f2937; font-weight: 600; font-size: 1.125rem;">
                <div style="width: 32px; height: 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 1rem;">V</div>
                <div>VaultCaddy</div>
            </a>
            <button onclick="window.closeMobileSidebar()" style="background: none; border: none; cursor: pointer; color: #6b7280; font-size: 1.5rem;">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <nav style="padding: 1.5rem;">
            <a href="/index.html#features" style="display: block; padding: 0.75rem 1rem; color: #4b5563; text-decoration: none; font-size: 1rem; font-weight: 500; border-radius: 6px; transition: background 0.2s;" onclick="closeMobileSidebar()" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">功能</a>
            <a href="/index.html#pricing" style="display: block; padding: 0.75rem 1rem; color: #4b5563; text-decoration: none; font-size: 1rem; font-weight: 500; border-radius: 6px; transition: background 0.2s;" onclick="closeMobileSidebar()" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">價格</a>
            <a href="/dashboard.html" style="display: block; padding: 0.75rem 1rem; color: #4b5563; text-decoration: none; font-size: 1rem; font-weight: 500; border-radius: 6px; transition: background 0.2s;" onclick="closeMobileSidebar()" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">儀表板</a>
            <a href="/blog/how-to-convert-pdf-bank-statement-to-excel.html" style="display: block; padding: 0.75rem 1rem; color: #4b5563; text-decoration: none; font-size: 1rem; font-weight: 500; border-radius: 6px; transition: background 0.2s;" onclick="closeMobileSidebar()" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">博客</a>
        </nav>
    </div>
'''

def add_navbar_to_file(file_path):
    """添加導航欄 HTML 到文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已經有導航欄
        if '<nav class="vaultcaddy-navbar"' in content:
            print(f"⏭️  跳過 {file_path}（已有導航欄）")
            return False
        
        # 在 <body> 標籤後插入導航欄
        pattern = r'(<body[^>]*>)'
        replacement = r'\1' + NAVBAR_HTML
        
        content = re.sub(pattern, replacement, content, count=1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加導航欄到 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 處理 {file_path} 失敗: {e}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始恢復靜態導航欄...")
    print("=" * 60)
    
    files = [
        'index.html',
        'dashboard.html',
        'account.html',
        'billing.html',
        'firstproject.html',
        'privacy.html',
        'terms.html',
    ]
    
    updated = 0
    for file in files:
        if add_navbar_to_file(file):
            updated += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共更新 {updated}/{len(files)} 個文件")
    print("=" * 60)

if __name__ == '__main__':
    main()

