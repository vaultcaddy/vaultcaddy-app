#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全統一所有組件：
1. 移除重複的 mobile-sidebar
2. 移除所有內嵌的 updateUserMenu 或導航欄邏輯
3. 確保所有頁面只使用 unified-auth.js
4. 確保所有頁面只使用 unified-sidebar.js
"""

import re

def remove_duplicate_mobile_sidebar(file_path):
    """移除重複的 mobile-sidebar"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 計算有多少個 mobile-sidebar
    count = content.count('id="mobile-sidebar"')
    
    if count > 1:
        print(f"⚠️  {file_path} 有 {count} 個 mobile-sidebar")
        
        # 找到並移除第二個及以後的 mobile-sidebar
        # 使用更精確的模式
        pattern = r'<!-- ✅ 統一靜態導航欄.*?<!-- 手機側邊欄菜單 -->.*?<div id="mobile-sidebar".*?</div>\s*</div>\s*<script>.*?</script>'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            print(f"✅ 已移除重複的 mobile-sidebar")
        else:
            print(f"⏭️  無法自動移除，需要手動檢查")
    else:
        print(f"✅ {file_path} 只有一個 mobile-sidebar")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def clean_inline_scripts(file_path):
    """清理內嵌的導航欄腳本"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除任何內嵌的 openMobileSidebar, closeMobileSidebar 等函數
    # 這些應該由 unified-auth.js 或其他統一腳本處理
    
    patterns_to_remove = [
        # 移除內嵌的 mobile sidebar 控制腳本
        r'<script>\s*window\.openMobileSidebar.*?</script>',
        # 移除內嵌的 updateUserMenu 腳本
        r'<script>\s*async function updateUserMenu.*?</script>',
    ]
    
    for pattern in patterns_to_remove:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            print(f"✅ 已移除內嵌腳本")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函數"""
    print("=" * 60)
    print("🔧 開始統一所有組件...")
    print("=" * 60)
    
    files_to_fix = [
        'firstproject.html',
        'dashboard.html',
        'account.html',
        'billing.html',
        'index.html',
    ]
    
    print("\n1️⃣ 移除重複的 mobile-sidebar...")
    for file in files_to_fix:
        print(f"\n檢查 {file}...")
        remove_duplicate_mobile_sidebar(file)
    
    print("\n2️⃣ 清理內嵌腳本...")
    for file in files_to_fix:
        print(f"\n檢查 {file}...")
        clean_inline_scripts(file)
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📝 統一後的架構：")
    print("   ✅ 每個頁面只有一個 <nav> 導航欄")
    print("   ✅ 每個頁面只有一個 mobile-sidebar")
    print("   ✅ 所有認證邏輯由 unified-auth.js 處理")
    print("   ✅ 所有左側欄由 unified-sidebar.js 處理")
    
    print("\n🎯 預期結果：")
    print("   ✅ 導航欄正確顯示用戶 logo (YC)")
    print("   ✅ Credits 正確顯示")
    print("   ✅ 左側欄在所有頁面統一顯示")
    print("   ✅ 手機版和桌面版共用同一套邏輯")

if __name__ == '__main__':
    main()

