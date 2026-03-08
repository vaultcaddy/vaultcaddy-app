#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加 unified-sidebar.js 到需要左側欄的頁面
"""

import re

def add_unified_sidebar_script(file_path):
    """添加 unified-sidebar.js 腳本引用"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 檢查是否已有 unified-sidebar.js
        if 'unified-sidebar.js' in content:
            print(f"⏭️  跳過 {file_path}（已有 unified-sidebar.js）")
            return False
        
        # 在 </body> 前添加 unified-sidebar.js
        # 確保在 simple-data-manager.js 之後載入
        pattern = r'(</body>)'
        
        script_tag = '''    <!-- ✅ 統一左側欄系統 -->
    <script src="unified-sidebar.js?v=20251129"></script>

'''
        
        content = re.sub(pattern, script_tag + r'\1', content, count=1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加 unified-sidebar.js 到 {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 處理 {file_path} 失敗: {e}")
        return False

def main():
    """主函數"""
    print("=" * 60)
    print("📦 開始添加 unified-sidebar.js...")
    print("=" * 60)
    
    files = [
        'dashboard.html',
        'account.html',
        'billing.html',
        'firstproject.html',
    ]
    
    added = 0
    for file in files:
        if add_unified_sidebar_script(file):
            added += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！共添加 {added}/{len(files)} 個文件")
    print("=" * 60)

if __name__ == '__main__':
    main()

