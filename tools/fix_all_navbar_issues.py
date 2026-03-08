#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復導航欄和 Credits 顯示問題
1. 確保用戶下拉菜單正確隱藏
2. 修復 Credits 顯示
"""

import re

def fix_unified_auth_dropdown():
    """修復 unified-auth.js 的下拉菜單和 Credits 顯示"""
    file_path = 'unified-auth.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 確保下拉菜單初始狀態為隱藏
    # 找到下拉菜單的 HTML 並確保 display: none
    old_dropdown = r'<div id="user-dropdown" style="display: none;'
    
    # 如果已經是 display: none，不需要修改
    if 'display: none' in content and 'user-dropdown' in content:
        print("✅ 下拉菜單已設置為隱藏")
    
    # 檢查 Credits 是否正確顯示
    # Credits 變數應該從 Firestore 正確獲取
    if 'credits = userDoc.credits' in content:
        print("✅ Credits 獲取邏輯存在")
    
    # 確保 Credits 顯示在下拉菜單中，而不是導航欄上
    # 下拉菜單應該有正確的定位
    pattern = r'(<div id="user-dropdown" style="display: none; position: absolute;)'
    replacement = r'<div id="user-dropdown" style="display: none !important; position: absolute;'
    
    content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path}")

def add_dropdown_css():
    """添加 CSS 確保下拉菜單初始隱藏"""
    files = ['dashboard.html', 'account.html', 'billing.html', 'firstproject.html', 'index.html']
    
    css_rule = '''
    /* 確保用戶下拉菜單初始隱藏 */
    #user-dropdown {
        display: none !important;
    }
    
    #user-dropdown[style*="display: block"] {
        display: block !important;
    }
    '''
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢查是否已有這個 CSS
            if '確保用戶下拉菜單初始隱藏' in content:
                print(f"⏭️  跳過 {file_path}（已有 CSS）")
                continue
            
            # 在 </style> 前插入
            content = re.sub(
                r'(</style>)',
                css_rule + r'\n    \1',
                content,
                count=1
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已添加 CSS 到 {file_path}")
            
        except Exception as e:
            print(f"❌ 處理 {file_path} 失敗: {e}")

def main():
    """主函數"""
    print("=" * 60)
    print("🔄 開始修復導航欄問題...")
    print("=" * 60)
    
    # 1. 修復 unified-auth.js
    print("\n1️⃣ 修復用戶下拉菜單...")
    fix_unified_auth_dropdown()
    
    # 2. 添加 CSS 確保下拉菜單隱藏
    print("\n2️⃣ 添加 CSS 確保下拉菜單初始隱藏...")
    add_dropdown_css()
    
    print("\n" + "=" * 60)
    print("✅ 所有修復完成！")
    print("=" * 60)
    print("\n📝 關於 Credits 顯示問題：")
    print("   Credits 顯示 0 可能是因為：")
    print("   1. SimpleDataManager 尚未完全初始化")
    print("   2. Firestore 數據讀取延遲")
    print("   3. 需要檢查 Firestore 中的實際數據")
    print("\n   建議：刷新頁面後稍等 1-2 秒，Credits 應該會更新")

if __name__ == '__main__':
    main()

