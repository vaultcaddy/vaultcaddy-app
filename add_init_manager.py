#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加 init-manager.js 到所有頁面
確保它在所有其他腳本之前載入
"""

import re

def add_init_manager(file_path):
    """添加 init-manager.js 到頁面"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否已有 init-manager.js
    if 'init-manager.js' in content:
        print(f"✅ {file_path} 已有 init-manager.js")
        return False
    
    # 在第一個 Firebase SDK 腳本之前插入 init-manager.js
    # 或者在 simple-auth.js 之前插入
    
    # 找到 Firebase SDK 的位置
    firebase_pattern = r'(<script[^>]*src=["\']https://www\.gstatic\.com/firebasejs/[^"\']*firebase-app[^"\']*["\'][^>]*></script>)'
    
    if re.search(firebase_pattern, content):
        # 在 Firebase SDK 之前插入
        init_script = '    <!-- ✅ 統一初始化管理器 -->\n    <script defer src="init-manager.js?v=20251130"></script>\n\n'
        content = re.sub(firebase_pattern, init_script + r'\1', content, count=1)
        print(f"✅ {file_path} 已添加 init-manager.js（在 Firebase SDK 之前）")
    else:
        # 找到 simple-auth.js 的位置
        auth_pattern = r'(<script[^>]*src=["\']simple-auth\.js[^"\']*["\'][^>]*></script>)'
        
        if re.search(auth_pattern, content):
            init_script = '    <!-- ✅ 統一初始化管理器 -->\n    <script defer src="init-manager.js?v=20251130"></script>\n\n'
            content = re.sub(auth_pattern, init_script + r'\1', content, count=1)
            print(f"✅ {file_path} 已添加 init-manager.js（在 simple-auth.js 之前）")
        else:
            print(f"⚠️  {file_path} 找不到合適的插入點")
            return False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """主函數"""
    print("=" * 60)
    print("📦 添加 init-manager.js 到所有頁面...")
    print("=" * 60)
    
    files = [
        'index.html',
        'dashboard.html',
        'firstproject.html',
        'account.html',
        'billing.html',
        'privacy.html',
        'terms.html',
    ]
    
    added = 0
    for file in files:
        print(f"\n處理 {file}...")
        if add_init_manager(file):
            added += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共添加 {added}/{len(files)} 個文件")
    print("=" * 60)
    
    print("\n📝 優化效果：")
    print("   ✅ 統一的初始化流程")
    print("   ✅ 減少重複的等待和重試")
    print("   ✅ 更清晰的初始化日誌")
    print("   ✅ 更快的頁面載入速度")
    
    print("\n🎯 預期結果：")
    print("   ✅ 不再有大量 '等待 200ms 後重試' 訊息")
    print("   ✅ 初始化流程更快、更穩定")
    print("   ✅ 控制台日誌更清晰易讀")

if __name__ == '__main__':
    main()

