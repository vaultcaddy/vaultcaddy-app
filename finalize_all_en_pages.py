#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完成所有英文页面的最终英文化修改
"""

import re

def update_en_index():
    """更新 en/index.html"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. QuickBooks 整合 -> QuickBooks Integration
    content = content.replace('QuickBooks 整合', 'QuickBooks Integration')
    
    # 2. 365 Days Data Retention -> Data Retention
    content = content.replace('365 Days Data Retention', 'Data Retention')
    
    # 3. 30 Days Image Backup -> Image Backup
    content = content.replace('30 Days Image Backup', 'Image Backup')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/index.html 更新完成")

def update_en_dashboard():
    """更新 en/dashboard.html"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/dashboard.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 导航栏
    content = content.replace('功能', 'Features')
    content = content.replace('價格', 'Pricing')
    content = content.replace('學習中心', 'Learning Center')
    content = content.replace('儀表板', 'Dashboard')
    
    # Email 验证横幅
    content = content.replace('🎁\n立即驗證您的 email 即送 20 Credits 試用！', '🎁\nVerify your email now and get 20 Credits free trial!')
    content = content.replace('立即驗證', 'Verify Now')
    
    # 左侧栏
    content = content.replace('管理', 'Manage')
    content = content.replace('帳戶', 'Account')
    content = content.replace('計費', 'Billing')
    
    # 主内容区
    content = content.replace('搜尋文檔名稱...', 'Search documents...')
    content = content.replace('project', 'Project')
    content = content.replace('創建', 'Create')
    content = content.replace('Name', 'Name')
    content = content.replace('Last modified', 'Last Modified')
    content = content.replace('Created', 'Created')
    content = content.replace('Actions', 'Actions')
    content = content.replace('No projects yet Create your first project to get started', 'No projects yet. Create your first project to get started.')
    
    # 对话框
    content = content.replace('Create New Project', 'Create New Project')
    content = content.replace('Project Name', 'Project Name')
    content = content.replace('Cancel', 'Cancel')
    content = content.replace('刪除項目', 'Delete Project')
    content = content.replace('是否刪除文件夾', 'Delete folder')
    content = content.replace('？', '?')
    content = content.replace('刪除後無法復原文件夾及當中內容。', 'This action cannot be undone. All contents will be permanently deleted.')
    content = content.replace('請輸入項目名稱以確認刪除', 'Enter project name to confirm deletion')
    content = content.replace('取消', 'Cancel')
    content = content.replace('是', 'Yes')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/dashboard.html 更新完成")

def update_en_firstproject():
    """更新 en/firstproject.html"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/firstproject.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 导航栏（同 dashboard）
    content = content.replace('功能', 'Features')
    content = content.replace('價格', 'Pricing')
    content = content.replace('學習中心', 'Learning Center')
    content = content.replace('儀表板', 'Dashboard')
    
    # Email 验证横幅
    content = content.replace('🎁\n立即驗證您的 email 即送 20 Credits 試用！', '🎁\nVerify your email now and get 20 Credits free trial!')
    content = content.replace('立即驗證', 'Verify Now')
    
    # 左侧栏
    content = content.replace('管理', 'Manage')
    content = content.replace('帳戶', 'Account')
    content = content.replace('計費', 'Billing')
    
    # 文档类型选择
    content = content.replace('選擇文檔類型', 'Select Document Type')
    content = content.replace('銀行對帳單', 'Bank Statement')
    content = content.replace('將銀行對帳單轉換為 Excel 和 CSV 格式', 'Convert bank statements to Excel and CSV format')
    content = content.replace('Invoice', 'Invoice')
    content = content.replace('發票', 'Invoice')
    content = content.replace('提取編號、日期、項目明細、價格和供應商信息', 'Extract number, date, items, prices and vendor information')
    
    # 上传区域
    content = content.replace('拖放文件到此處或點擊上傳', 'Drag and drop files here or click to upload')
    content = content.replace('支援 PDF、JPG、PNG 格式 (最大 10MB)｜✨ 支持批量上傳', 'Supports PDF, JPG, PNG formats (max 10MB) | ✨ Batch upload supported')
    content = content.replace('文件上傳', 'File Upload')
    content = content.replace('AI 分析', 'AI Analysis')
    content = content.replace('數據提取', 'Data Extraction')
    content = content.replace('雲端存儲', 'Cloud Storage')
    content = content.replace('處理進度', 'Processing Progress')
    
    # 表格标题
    content = content.replace('Document Name', 'Document Name')
    content = content.replace('Type', 'Type')
    content = content.replace('Status', 'Status')
    content = content.replace('Vendor/Source/Bank', 'Vendor/Source/Bank')
    content = content.replace('Amount', 'Amount')
    content = content.replace('Date', 'Date')
    content = content.replace('Upload Date', 'Upload Date')
    content = content.replace('Actions', 'Actions')
    content = content.replace('文檔名稱', 'Document Name')
    content = content.replace('類型', 'Type')
    content = content.replace('狀態', 'Status')
    content = content.replace('供應商/來源/銀行', 'Vendor/Source/Bank')
    content = content.replace('金額', 'Amount')
    content = content.replace('日期', 'Date')
    content = content.replace('上傳日期', 'Upload Date')
    content = content.replace('操作', 'Actions')
    
    # Status 状态
    content = content.replace('已完成', 'Completed')
    content = content.replace('處理中', 'Processing')
    content = content.replace('失敗', 'Failed')
    content = content.replace('等待中', 'Pending')
    
    # 按钮和统计
    content = content.replace('Upload files', 'Upload Files')
    content = content.replace('Export', 'Export')
    content = content.replace('Delete', 'Delete')
    content = content.replace('共 13 張發票', '13 invoices total')
    content = content.replace('共', '')
    content = content.replace('張發票', ' invoices total')
    content = content.replace('張', '')
    content = content.replace('發票', 'invoices')
    
    # 筛选器
    content = content.replace('日期篩選', 'Date Filter')
    content = content.replace('日期範圍', 'Date Range')
    content = content.replace('至', 'to')
    content = content.replace('上傳日期範圍', 'Upload Date Range')
    content = content.replace('清除篩選', 'Clear Filter')
    
    # 其他
    content = content.replace('No results.', 'No results.')
    content = content.replace('Rows per page', 'Rows per page')
    content = content.replace('Page 1 of 0', 'Page 1 of 0')
    content = content.replace('創建新項目', 'Create New Project')
    content = content.replace('輸入項目名稱以創建新的文檔項目', 'Enter project name to create a new document project')
    content = content.replace('項目名稱', 'Project Name')
    content = content.replace('取消', 'Cancel')
    content = content.replace('創建', 'Create')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/firstproject.html 更新完成")

def update_en_account():
    """更新 en/account.html"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/account.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 导航栏
    content = content.replace('功能', 'Features')
    content = content.replace('價格', 'Pricing')
    content = content.replace('學習中心', 'Learning Center')
    content = content.replace('儀表板', 'Dashboard')
    
    # 左侧栏
    content = content.replace('管理', 'Manage')
    content = content.replace('帳戶', 'Account')
    content = content.replace('計費', 'Billing')
    
    # 主标题
    content = content.replace('帳戶設定', 'Account Settings')
    content = content.replace('管理您的個人資料和帳戶偏好設定', 'Manage your personal information and account preferences')
    
    # 个人资料部分
    content = content.replace('個人資料', 'Profile')
    content = content.replace('目前計劃', 'Current Plan')
    content = content.replace('Basic Plan', 'Basic Plan')
    content = content.replace('Free Plan', 'Free Plan')
    content = content.replace('Pro Plan', 'Pro Plan')
    content = content.replace('升級計劃', 'Upgrade Plan')
    
    # Credits 部分
    content = content.replace('Credits Usage', 'Credits Usage')
    content = content.replace('每處理 1 頁文檔消耗 1 個 Credit。', 'Each page processed consumes 1 Credit.')
    content = content.replace('重置日期：', 'Reset Date: ')
    content = content.replace('年', '')
    content = content.replace('月', '/')
    content = content.replace('日', '')
    content = content.replace('購買 Credits', 'Purchase Credits')
    content = content.replace('查看記錄', 'View History')
    
    # 密码部分
    content = content.replace('密碼', 'Password')
    content = content.replace('目前密碼', 'Current Password')
    content = content.replace('New Password', 'New Password')
    content = content.replace('密碼至少需要 8 個字元', 'Password must be at least 8 characters')
    content = content.replace('Confirm New Password', 'Confirm New Password')
    content = content.replace('更新密碼', 'Update Password')
    
    # 偏好设置
    content = content.replace('偏好設定', 'Preferences')
    content = content.replace('Language', 'Language')
    content = content.replace('繁體中文', 'Traditional Chinese')
    content = content.replace('English', 'English')
    content = content.replace('時區', 'Timezone')
    content = content.replace('台北 (GMT+8)', 'Taipei (GMT+8)')
    content = content.replace('香港 (GMT+8)', 'Hong Kong (GMT+8)')
    content = content.replace('UTC (GMT+0)', 'UTC (GMT+0)')
    content = content.replace('儲存偏好設定', 'Save Preferences')
    
    # 购买历史
    content = content.replace('Purchase History', 'Purchase History')
    content = content.replace('所有記錄', 'All Records')
    content = content.replace('2025年11月', 'November 2025')
    content = content.replace('2025年10月', 'October 2025')
    content = content.replace('日期', 'Date')
    content = content.replace('Description', 'Description')
    content = content.replace('Credits', 'Credits')
    content = content.replace('載入記錄中...', 'Loading records...')
    content = content.replace('文件轉換', 'Document Conversion')
    content = content.replace('VaultCaddy Monthly', 'VaultCaddy Monthly')
    content = content.replace('VaultCaddy Yearly', 'VaultCaddy Yearly')
    
    # 危险区域
    content = content.replace('危險區域', 'Danger Zone')
    content = content.replace('刪除您的帳戶將永久移除所有資料，包括項目、文檔和設定。此操作無法復原。', 
                            'Deleting your account will permanently remove all data, including projects, documents, and settings. This action cannot be undone.')
    content = content.replace('Delete Account', 'Delete Account')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/account.html 更新完成")

if __name__ == '__main__':
    print("开始更新所有英文页面...")
    print()
    
    update_en_index()
    update_en_dashboard()
    update_en_firstproject()
    update_en_account()
    
    print()
    print("=" * 50)
    print("✅ 所有页面英文化完成！")
    print()
    print("修改摘要：")
    print("1. en/index.html:")
    print("   - QuickBooks 整合 → QuickBooks Integration")
    print("   - 365 Days Data Retention → Data Retention")
    print("   - 30 Days Image Backup → Image Backup")
    print()
    print("2. en/dashboard.html:")
    print("   - 导航栏完全英文化")
    print("   - Email 验证横幅英文化")
    print("   - 左侧栏和主内容区英文化")
    print()
    print("3. en/firstproject.html:")
    print("   - 导航栏和左侧栏英文化")
    print("   - 文档类型选择英文化")
    print("   - 表格和状态英文化")
    print("   - '共 X 張發票' → 'X invoices total'")
    print()
    print("4. en/account.html:")
    print("   - 所有界面元素完全英文化")
    print("   - 包括导航栏、左侧栏、设置项等")

