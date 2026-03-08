#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. 修复 en/firstproject.html 的日期筛选器设计，使其与中文版一致
2. 创建 en/document-detail.html 英文版页面
"""

import shutil
import re

def fix_en_firstproject_date_filter():
    """修复英文版 firstproject.html 的日期筛选器设计"""
    en_file = '/Users/cavlinyeung/ai-bank-parser/en/firstproject.html'
    
    with open(en_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到并替换旧的日期筛选器代码
    old_filter_pattern = r'<div class="filter-section".*?</div>\s*</div>\s*</div>\s*<div class="table-container"'
    
    # 新的日期筛选器HTML（与中文版一致的设计）
    new_filter_html = '''<!-- 📅 日期篩選器 -->
                <div class="date-filter-container" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- 日期篩選標題 -->
                    <div class="date-filter-header" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="color: white; font-size: 1rem; font-weight: 600; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
                            <i class="fas fa-filter"></i>
                            <span>Date Filter</span>
                        </h3>
                        <button onclick="toggleDateFilter()" style="background: rgba(255,255,255,0.2); color: white; border: none; padding: 0.25rem 0.75rem; border-radius: 6px; cursor: pointer; font-size: 0.875rem; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">
                            <i class="fas fa-chevron-down" id="filter-toggle-icon"></i>
                        </button>
                    </div>
                    
                    <!-- 日期篩選內容 -->
                    <div class="date-filter-content" id="date-filter-content" style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <!-- 日期範圍 -->
                        <div class="date-filter-group" style="flex: 1; min-width: 200px;">
                            <label style="display: block; font-size: 0.875rem; font-weight: 600; color: white; margin-bottom: 0.5rem;">
                                <i class="fas fa-calendar-alt" style="margin-right: 0.5rem;"></i>
                                Date Range
                            </label>
                            <div class="date-filter-inputs" style="display: flex; gap: 0.5rem; align-items: center;">
                                <input type="date" id="date-from" style="flex: 1; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem;" placeholder="Start Date">
                                <span style="color: white;">to</span>
                                <input type="date" id="date-to" style="flex: 1; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem;" placeholder="End Date">
                            </div>
                        </div>
                        
                        <!-- Upload Date Range -->
                        <div class="date-filter-group" style="flex: 1; min-width: 200px;">
                            <label style="display: block; font-size: 0.875rem; font-weight: 600; color: white; margin-bottom: 0.5rem;">
                                <i class="fas fa-upload" style="margin-right: 0.5rem;"></i>
                                Upload Date Range
                            </label>
                            <div class="date-filter-inputs" style="display: flex; gap: 0.5rem; align-items: center;">
                                <input type="date" id="upload-date-from" style="flex: 1; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem;" placeholder="Start Date">
                                <span style="color: white;">to</span>
                                <input type="date" id="upload-date-to" style="flex: 1; padding: 0.5rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem;" placeholder="End Date">
                            </div>
                        </div>
                        
                        <!-- Clear Button -->
                        <div class="date-filter-clear-btn" style="align-self: flex-end;">
                            <button onclick="clearDateFilters()" style="padding: 0.5rem 1rem; background: rgba(255,255,255,0.9); color: #667eea; border: none; border-radius: 6px; font-size: 0.875rem; font-weight: 600; cursor: pointer; white-space: nowrap; transition: all 0.2s;" onmouseover="this.style.background='white'" onmouseout="this.style.background='rgba(255,255,255,0.9)'">
                                <i class="fas fa-times" style="margin-right: 0.5rem;"></i>
                                Clear Filter
                            </button>
                        </div>
                    </div> <!-- Close date-filter-content -->
                </div>
                
                <!-- Document Table -->
                <div class="table-container"'''
    
    # 使用正则表达式替换
    content = re.sub(old_filter_pattern, new_filter_html, content, flags=re.DOTALL)
    
    with open(en_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/firstproject.html 日期筛选器设计已修复")

def create_en_document_detail():
    """创建英文版 document-detail.html"""
    cn_file = '/Users/cavlinyeung/ai-bank-parser/document-detail.html'
    en_file = '/Users/cavlinyeung/ai-bank-parser/en/document-detail.html'
    
    # 复制中文版文件
    shutil.copy(cn_file, en_file)
    
    with open(en_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 翻译所有用户可见的文本
    translations = {
        # HTML lang
        'lang="zh-TW"': 'lang="en"',
        
        # 页面标题
        '<title>文檔詳情 - VaultCaddy</title>': '<title>Document Details - VaultCaddy</title>',
        
        # 脚本路径 - 更新为相对路径
        'src="disable-console-safe.js"': 'src="../disable-console-safe.js"',
        'href="styles.css"': 'href="../styles.css"',
        'href="dashboard.css"': 'href="../dashboard.css"',
        'href="pages.css"': 'href="../pages.css"',
        'href="editable-table.css"': 'href="../editable-table.css"',
        'src="config.js"': 'src="../config.js"',
        'src="translations.js"': 'src="../translations.js"',
        'src="firebase-config.js': 'src="../firebase-config.js',
        'src="simple-auth.js': 'src="../simple-auth.js',
        'src="user-profile-manager.js': 'src="../user-profile-manager.js',
        'src="simple-data-manager.js': 'src="../simple-data-manager.js',
        'src="navbar-interactions.js': 'src="../navbar-interactions.js',
        'src="navbar-component.js': 'src="../navbar-component.js',
        'src="sidebar-component.js': 'src="../sidebar-component.js',
        'src="export-manager.js': 'src="../export-manager.js',
        
        # 按钮和操作
        '確定要刪除此文檔嗎？此操作無法撤銷。': 'Are you sure you want to delete this document? This action cannot be undone.',
        '無法獲取文檔信息': 'Unable to get document information',
        '文檔已成功刪除': 'Document deleted successfully',
        '無法連接到數據庫': 'Unable to connect to database',
        '返回儀表板': 'Back to Dashboard',
        '載入中...': 'Loading...',
        'Saved': 'Saved',
        'Export': 'Export',
        'Delete': 'Delete',
        '載入文檔中...': 'Loading document...',
        
        # 银行对账单详情
        'Bank Statement Details & Notes': 'Bank Statement Details & Notes',
        'Transactions': 'Transactions',
        'Show Unreconciled': 'Show Unreconciled',
        'Toggle All': 'Toggle All',
        'Add Item': 'Add Item',
        'Showing 0 to 0 of 0 transactions': 'Showing 0 to 0 of 0 transactions',
        
        # 表格标题
        'Date': 'Date',
        'Description': 'Description',
        'Amount': 'Amount',
        'Balance': 'Balance',
        'Actions': 'Actions',
        '載入交易記錄中...': 'Loading transactions...',
        
        # 导航
        '上一頁': 'Previous',
        '下一頁': 'Next',
        '首頁': 'Home',
        '功能': 'Features',
        '價格': 'Pricing',
        '學習中心': 'Learning Center',
        '儀表板': 'Dashboard',
        
        # 其他
        '繁體中文': 'English',
        '搜尋文檔名稱...': 'Search documents...',
        '管理': 'Manage',
        '帳戶': 'Account',
        '計費': 'Billing',
        '登出': 'Logout',
    }
    
    for cn_text, en_text in translations.items():
        content = content.replace(cn_text, en_text)
    
    with open(en_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/document-detail.html 已创建并翻译")

if __name__ == '__main__':
    print("开始修复英文版页面...")
    print()
    
    # 1. 修复 en/firstproject.html 的日期筛选器
    fix_en_firstproject_date_filter()
    
    # 2. 创建 en/document-detail.html
    create_en_document_detail()
    
    print()
    print("=" * 50)
    print("✅ 修复完成！")
    print()
    print("完成内容：")
    print("1. en/firstproject.html:")
    print("   - 日期筛选器设计已更新为与中文版一致")
    print("   - 添加了渐变背景和图标")
    print("   - 改进了按钮样式")
    print()
    print("2. en/document-detail.html:")
    print("   - 已创建英文版页面")
    print("   - 所有用户可见文本已翻译")
    print("   - 脚本路径已更新为相对路径")

