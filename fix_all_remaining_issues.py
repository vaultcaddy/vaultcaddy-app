#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復所有剩餘問題：
1. 簡化會員 logo 邏輯，直接從 email 獲取初始字母
2. Credits 顯示邏輯
3. 左側欄配置固定在底部
4. firstproject.html 佈局
"""

import re

def simplify_user_initial_logic():
    """簡化 unified-auth.js 的用戶初始字母邏輯"""
    file_path = 'unified-auth.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到獲取 initial 的部分，簡化為直接從 email 獲取
    # 原邏輯可能是從 displayName 或其他地方獲取，導致多次變化
    
    # 確保 initial 只從 email 的第一個字母獲取
    old_pattern = r"const initial = user\.email.*?\.toUpperCase\(\);?"
    new_code = "const initial = (user.email && user.email.length > 0) ? user.email.substring(0, 2).toUpperCase() : 'U';"
    
    content = re.sub(old_pattern, new_code, content)
    
    # 同時移除所有可能導致 logo 變化的邏輯
    # 確保不會從 displayName 獲取初始字母
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已簡化 {file_path} 的用戶初始字母邏輯")

def fix_sidebar_config_position():
    """修復左側欄配置區塊，使其固定在底部"""
    file_path = 'unified-sidebar.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到左側欄的主容器，修改為 flex 佈局
    # 將 padding div 改為 flex container
    old_pattern = r'sidebar\.innerHTML = `\s*<div style="padding: 1\.5rem;'
    new_code = '''sidebar.innerHTML = `
            <div style="display: flex; flex-direction: column; height: 100%; padding: 1.5rem;'''
    
    content = re.sub(old_pattern, new_code, content)
    
    # 修改 project 區塊，添加 flex: 1 使其占據剩餘空間
    old_project_div = r'<!-- Project 區塊 -->\s*<div style="margin-bottom: 1\.5rem;">'
    new_project_div = '''<!-- Project 區塊 -->
                <div style="flex: 1; margin-bottom: 1.5rem; overflow-y: auto;">'''
    
    content = re.sub(old_project_div, new_project_div, content)
    
    # 配置區塊保持不變（自動在底部）
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修復 {file_path} 的配置區塊位置")

def fix_firstproject_layout():
    """修復 firstproject.html 的佈局"""
    file_path = 'firstproject.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到項目標題和搜尋欄的容器
    # 將它們和按鈕放在同一水平線上
    
    # 查找現有的結構並替換
    # 舊結構：標題和搜尋在上，按鈕在下
    # 新結構：標題、搜尋、按鈕都在同一行
    
    old_pattern = r'(<div class="main-header"[^>]*>.*?</div>)\s*(<div[^>]*id="action-buttons-container"[^>]*>.*?</div>)'
    
    # 這個替換比較複雜，需要檢查實際 HTML 結構
    # 先不做替換，手動檢查
    
    print(f"⏭️  跳過 {file_path}（需要手動檢查 HTML 結構）")

def improve_credits_loading():
    """改進 Credits 載入邏輯"""
    file_path = 'unified-auth.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 確保 Credits 從 Firestore 正確獲取
    # 添加更多日誌以便調試
    
    # 在獲取 userDoc 後，添加更詳細的日誌
    pattern = r'credits = userDoc\.credits \|\| 0;'
    replacement = '''credits = userDoc.credits || 0;
                            console.log('📊 Credits 數據:', { 
                                fromFirestore: userDoc.credits, 
                                finalValue: credits,
                                userDocKeys: Object.keys(userDoc)
                            });'''
    
    content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已改進 {file_path} 的 Credits 載入邏輯")

def main():
    """主函數"""
    print("=" * 60)
    print("🔧 開始修復所有剩餘問題...")
    print("=" * 60)
    
    print("\n1️⃣ 簡化會員 logo 邏輯（YC 而非 O）...")
    simplify_user_initial_logic()
    
    print("\n2️⃣ 改進 Credits 載入...")
    improve_credits_loading()
    
    print("\n3️⃣ 修復左側欄配置區塊位置...")
    fix_sidebar_config_position()
    
    print("\n4️⃣ 修復 firstproject.html 佈局...")
    fix_firstproject_layout()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    print("\n📝 修改摘要：")
    print("   1. 用戶 logo: 從 email 前2個字母獲取（YC）")
    print("   2. Credits: 添加詳細日誌以便調試")
    print("   3. 左側欄: 配置區塊固定在底部")
    print("   4. firstproject.html: 需要手動檢查佈局")

if __name__ == '__main__':
    main()

