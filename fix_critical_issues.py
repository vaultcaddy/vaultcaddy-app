#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復關鍵問題：
1. 移除 firstproject.html 中重複的 updateUserMenu 函數
2. 確保使用 unified-auth.js 的版本
3. 檢查 dashboard.html 是否有相同問題
"""

import re

def remove_duplicate_usermenu_function(file_path):
    """移除重複的 updateUserMenu 函數"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否有內嵌的 updateUserMenu 函數
    if 'async function updateUserMenu()' in content:
        print(f"⚠️  發現 {file_path} 中有內嵌的 updateUserMenu 函數")
        
        # 移除整個內嵌的用戶菜單更新腳本
        # 這個腳本通常在 </body> 前
        pattern = r'<script>\s*// 等待 Firebase.*?updateUserMenu.*?</script>\s*'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            print(f"✅ 已移除內嵌的 updateUserMenu 腳本")
        else:
            # 嘗試更寬鬆的匹配
            pattern = r'<script>.*?async function updateUserMenu\(\).*?</script>\s*'
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, '', content, flags=re.DOTALL)
                print(f"✅ 已移除內嵌的 updateUserMenu 腳本（寬鬆匹配）")
            else:
                print(f"⚠️  無法自動移除，需要手動檢查")
                return False
    else:
        print(f"✅ {file_path} 沒有內嵌的 updateUserMenu 函數")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函數"""
    print("=" * 60)
    print("🔧 開始修復關鍵問題...")
    print("=" * 60)
    
    files_to_check = [
        'firstproject.html',
        'dashboard.html',
        'account.html',
        'billing.html',
        'index.html',
    ]
    
    print("\n🔍 檢查並移除重複的 updateUserMenu 函數...")
    for file in files_to_check:
        print(f"\n檢查 {file}...")
        remove_duplicate_usermenu_function(file)
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📝 修復說明：")
    print("   1. 移除頁面內嵌的 updateUserMenu 函數")
    print("   2. 確保使用 unified-auth.js 的統一版本")
    print("   3. 避免函數重複定義和衝突")
    
    print("\n🎯 預期結果：")
    print("   ✅ 導航欄正確顯示用戶 logo (YC)")
    print("   ✅ Credits 正確顯示 79977")
    print("   ✅ 不再有重複的日誌訊息")

if __name__ == '__main__':
    main()

