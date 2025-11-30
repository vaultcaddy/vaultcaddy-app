#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除舊的 navbar-component.js 和 sidebar-component.js 系統
只保留新的統一系統：靜態 HTML + unified-auth.js
"""

import re

def remove_old_navbar_script(file_path):
    """移除 navbar-component.js 的引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否有 navbar-component.js
        if 'navbar-component.js' not in content:
            print(f"⏭️  跳過 {file_path}（沒有 navbar-component.js）")
            return False
        
        # 移除 navbar-component.js 的 <script> 標籤
        content = re.sub(
            r'<script[^>]*src=["\']navbar-component\.js[^"\']*["\'][^>]*></script>\s*',
            '',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已移除 navbar-component.js 從 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 處理 {file_path} 失敗: {e}")
        return False

def remove_old_sidebar_script(file_path):
    """移除 sidebar-component.js 的引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否有 sidebar-component.js
        if 'sidebar-component.js' not in content:
            print(f"⏭️  跳過 {file_path}（沒有 sidebar-component.js）")
            return False
        
        # 移除 sidebar-component.js 的 <script> 標籤
        content = re.sub(
            r'<script[^>]*src=["\']sidebar-component\.js[^"\']*["\'][^>]*></script>\s*',
            '',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已移除 sidebar-component.js 從 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 處理 {file_path} 失敗: {e}")
        return False

def update_unified_auth_dropdown():
    """更新 unified-auth.js 的下拉菜單，移除「儀表板」鏈接"""
    file_path = 'unified-auth.js'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到並移除「儀表板」鏈接
        # 舊的下拉菜單包含：儀表板、帳戶設定、計費、登出
        # 新的應該只有：帳戶、計費、登出
        
        # 移除儀表板鏈接（如果存在）
        old_pattern = r'<a href="/dashboard\.html"[^>]*>.*?儀表板.*?</a>\s*'
        if re.search(old_pattern, content, re.DOTALL):
            content = re.sub(old_pattern, '', content, flags=re.DOTALL)
            print(f"✅ 已從下拉菜單移除「儀表板」鏈接")
        else:
            print(f"⏭️  下拉菜單中未找到「儀表板」鏈接")
        
        # 更新「帳戶設定」為「帳戶」
        content = re.sub(r'帳戶設定', '帳戶', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已更新 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 處理 {file_path} 失敗: {e}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("🗑️  開始移除舊的組件系統...")
    print("=" * 60)
    
    # 1. 移除 navbar-component.js
    print("\n1️⃣ 移除 navbar-component.js 引用...")
    navbar_files = [
        'index.html',
        'dashboard.html',
        'account.html',
        'billing.html',
        'firstproject.html',
        'privacy.html',
        'terms.html',
    ]
    
    navbar_removed = 0
    for file in navbar_files:
        if remove_old_navbar_script(file):
            navbar_removed += 1
    
    # 2. 移除 sidebar-component.js
    print("\n2️⃣ 移除 sidebar-component.js 引用...")
    sidebar_files = [
        'dashboard.html',
        'account.html',
        'billing.html',
        'firstproject.html',
    ]
    
    sidebar_removed = 0
    for file in sidebar_files:
        if remove_old_sidebar_script(file):
            sidebar_removed += 1
    
    # 3. 更新 unified-auth.js 下拉菜單
    print("\n3️⃣ 更新 unified-auth.js 下拉菜單...")
    update_unified_auth_dropdown()
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！")
    print(f"   - 移除 navbar-component.js: {navbar_removed}/{len(navbar_files)} 個文件")
    print(f"   - 移除 sidebar-component.js: {sidebar_removed}/{len(sidebar_files)} 個文件")
    print("=" * 60)
    
    print("\n📝 現在的系統架構：")
    print("   ✅ 靜態導航欄 HTML（在每個頁面的 <body> 後）")
    print("   ✅ unified-auth.js（統一認證和用戶菜單）")
    print("   ✅ simple-auth.js（Firebase 認證）")
    print("   ✅ simple-data-manager.js（Firestore 數據）")
    print("\n   ❌ navbar-component.js（已移除）")
    print("   ❌ sidebar-component.js（已移除）")
    
    print("\n⚠️  注意：sidebar 現在需要新的實現！")
    print("   現在 dashboard.html 等頁面有 <aside class=\"sidebar\"></aside>")
    print("   但沒有 JavaScript 來渲染它。")
    print("   我們需要創建一個新的 sidebar 渲染邏輯。")

if __name__ == '__main__':
    main()

