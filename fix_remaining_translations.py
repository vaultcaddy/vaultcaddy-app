#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复英文页面中遗漏的翻译
"""

import re

def fix_en_account():
    """修复 en/account.html 中遗漏的中文"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/account.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 主标题
    content = content.replace('<h1>Account設定</h1>', '<h1>Account Settings</h1>')
    content = content.replace('<p>Manage您的Profile和AccountPreferences</p>', 
                            '<p>Manage your profile and account preferences</p>')
    
    # 密码部分的输入框
    content = content.replace('目前Password', 'Current Password')
    content = content.replace('輸入目前Password', 'Enter current password')
    content = content.replace('輸入新Password', 'Enter new password')
    content = content.replace('再次輸入新Password', 'Re-enter new password')
    content = content.replace('更新Password', 'Update Password')
    content = content.replace('Password至少需要 8 個字元', 'Password must be at least 8 characters')
    
    # Preferences 部分
    content = content.replace('儲存Preferences', 'Save Preferences')
    
    # 购买历史表格
    content = content.replace('<th>期</th>', '<th>Date</th>')
    
    # Danger Zone
    content = content.replace(
        '刪除您的Account將永久移除所有資料，包括項目、文檔和設定。此操作無法復原。',
        'Deleting your account will permanently remove all data, including projects, documents, and settings. This action cannot be undone.'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/account.html 遗漏翻译已修复")

def fix_sidebar_and_menu():
    """修复所有英文页面的左侧栏和会员菜单"""
    files = [
        '/Users/cavlinyeung/ai-bank-parser/en/dashboard.html',
        '/Users/cavlinyeung/ai-bank-parser/en/account.html',
        '/Users/cavlinyeung/ai-bank-parser/en/billing.html',
        '/Users/cavlinyeung/ai-bank-parser/en/firstproject.html'
    ]
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 会员菜单（图1）
            # Credits: -60 后面的邮箱地址下方的菜单项
            content = re.sub(r'<i class="fas fa-user"></i>\s*帳戶', 
                           '<i class="fas fa-user"></i> Account', content)
            content = re.sub(r'<i class="fas fa-credit-card"></i>\s*計費', 
                           '<i class="fas fa-credit-card"></i> Billing', content)
            content = re.sub(r'<i class="fas fa-sign-out-alt"></i>\s*登出', 
                           '<i class="fas fa-sign-out-alt"></i> Logout', content)
            
            # 左侧栏 - 搜索框
            content = content.replace('搜尋文檔名稱...', 'Search documents...')
            
            # 左侧栏 - 管理部分
            content = content.replace('<div class="sidebar-header">管理</div>', 
                                    '<div class="sidebar-header">Manage</div>')
            
            # 左侧栏 - 菜单项（如果还有中文）
            content = re.sub(r'>\s*帳戶\s*<', '>Account<', content)
            content = re.sub(r'>\s*計費\s*<', '>Billing<', content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {file_path.split('/')[-1]} 左侧栏和会员菜单已修复")
        except FileNotFoundError:
            print(f"⚠️ 文件未找到: {file_path}")

def add_date_filters_to_en_firstproject():
    """在英文版 firstproject.html 中添加日期筛选功能"""
    en_file = '/Users/cavlinyeung/ai-bank-parser/en/firstproject.html'
    cn_file = '/Users/cavlinyeung/ai-bank-parser/firstproject.html'
    
    # 读取中文版获取日期筛选的HTML结构
    with open(cn_file, 'r', encoding='utf-8') as f:
        cn_content = f.read()
    
    # 读取英文版
    with open(en_file, 'r', encoding='utf-8') as f:
        en_content = f.read()
    
    # 查找中文版中的日期筛选部分
    # 通常在表格上方，包含 "日期篩選" 的部分
    date_filter_pattern = r'(<div[^>]*class="[^"]*date-filter[^"]*"[^>]*>.*?</div>)'
    
    # 如果英文版没有日期筛选，我们需要从中文版复制并翻译
    if '日期範圍' not in en_content:
        # 查找插入位置（通常在表格之前）
        # 查找 Upload files Export Delete 按钮组之后的位置
        
        date_filter_html = '''
                <!-- 日期筛选器 -->
                <div class="filter-section" style="margin-bottom: 1rem; padding: 1rem; background: #f9fafb; border-radius: 8px; display: flex; gap: 1rem; align-items: end; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 200px;">
                        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #374151;">Date Range</label>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <input type="date" id="filter-date-from" class="form-input" style="flex: 1;">
                            <span style="color: #6b7280;">to</span>
                            <input type="date" id="filter-date-to" class="form-input" style="flex: 1;">
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.875rem; font-weight: 500; color: #374151;">Upload Date Range</label>
                        <div style="display: flex; gap: 0.5rem; align-items: center;">
                            <input type="date" id="filter-upload-from" class="form-input" style="flex: 1;">
                            <span style="color: #6b7280;">to</span>
                            <input type="date" id="filter-upload-to" class="form-input" style="flex: 1;">
                        </div>
                    </div>
                    <div>
                        <button onclick="applyFilters()" class="btn btn-primary" style="white-space: nowrap;">Apply Filter</button>
                        <button onclick="clearFilters()" class="btn btn-secondary" style="white-space: nowrap; margin-left: 0.5rem;">Clear Filter</button>
                    </div>
                </div>
'''
        
        # 找到表格容器之前插入
        table_start = en_content.find('<div class="table-container"')
        if table_start > 0:
            # 在表格容器之前插入日期筛选器
            en_content = en_content[:table_start] + date_filter_html + '\n                ' + en_content[table_start:]
            
            with open(en_file, 'w', encoding='utf-8') as f:
                f.write(en_content)
            
            print("✅ en/firstproject.html 日期筛选功能已添加")
        else:
            print("⚠️ 未找到表格容器位置，无法添加日期筛选器")
    else:
        print("ℹ️ en/firstproject.html 已包含日期筛选功能")

if __name__ == '__main__':
    print("开始修复英文页面遗漏的翻译...")
    print()
    
    # 1. 修复 account.html 中的遗漏翻译
    fix_en_account()
    
    # 2. 修复所有页面的左侧栏和会员菜单
    fix_sidebar_and_menu()
    
    # 3. 添加日期筛选功能到英文版 firstproject.html
    add_date_filters_to_en_firstproject()
    
    print()
    print("=" * 50)
    print("✅ 所有遗漏的翻译已修复！")
    print()
    print("修复内容：")
    print("1. en/account.html:")
    print("   - Account設定 → Account Settings")
    print("   - Manage您的Profile... → Manage your profile...")
    print("   - 所有输入框 placeholder 已翻译")
    print("   - 儲存Preferences → Save Preferences")
    print("   - 期 → Date")
    print("   - 刪除您的Account... → Deleting your account...")
    print()
    print("2. 所有英文页面:")
    print("   - 会员菜单：帳戶/計費/登出 → Account/Billing/Logout")
    print("   - 左侧栏：管理 → Manage")
    print()
    print("3. en/firstproject.html:")
    print("   - 添加日期筛选功能（Date Range & Upload Date Range）")

