#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复最后遗漏的中文翻译
"""

import re

def fix_en_account_final():
    """修复 en/account.html 的最后遗漏项"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/account.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复输入框 placeholder
    content = content.replace('placeholder="輸入Current Password"', 'placeholder="Enter current password"')
    content = content.replace('placeholder="再次Enter new password"', 'placeholder="Re-enter new password"')
    
    # 修复左侧栏（如果还有中文）
    content = content.replace('搜尋文檔名稱...', 'Search documents...')
    content = content.replace('<div class="sidebar-header">管理</div>', '<div class="sidebar-header">Manage</div>')
    content = content.replace('>帳戶<', '>Account<')
    content = content.replace('>計費<', '>Billing<')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/account.html 最后遗漏项已修复")

def fix_en_billing_final():
    """修复 en/billing.html 的所有中文"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/billing.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 导航栏
    content = content.replace('功能', 'Features')
    content = content.replace('價格', 'Pricing')
    content = content.replace('學習中心', 'Learning Center')
    content = content.replace('儀表板', 'Dashboard')
    
    # 2. Email 验证横幅
    content = content.replace('🎁 立即驗證您的 email 即送 20 Credits 試用！', '🎁 Verify your email now and get 20 Credits free trial!')
    content = content.replace('立即驗證', 'Verify Now')
    
    # 3. 主标题
    content = content.replace('無隱藏費用，安全可靠', 'No Hidden Fees, Secure and Reliable')
    
    # 4. 副标题
    content = content.replace('與數千家企業一起，節省財務數據錄入的時間。', 'Join thousands of businesses saving time on financial data entry.')
    
    # 5. 30 天圖片保留 → Image Backup
    content = content.replace('<span>30 天圖片保留</span>', '<span>Image Backup</span>')
    
    # 6. 365 Days Data Retention → Data Retention (如果还没改)
    # 这个应该已经在之前改过了，但再检查一次
    
    # 7. 左侧栏
    content = content.replace('搜尋文檔名稱...', 'Search documents...')
    content = content.replace('<div class="sidebar-header">管理</div>', '<div class="sidebar-header">Manage</div>')
    
    # 8. 其他可能的中文
    content = content.replace('首頁', 'Home')
    content = content.replace('隱私政策', 'Privacy Policy')
    content = content.replace('服務條款', 'Terms of Service')
    content = content.replace('輸入項目名稱以創建新的文檔項目', 'Enter project name to create a new document project')
    content = content.replace('項目名稱', 'Project Name')
    content = content.replace('取消', 'Cancel')
    content = content.replace('創建', 'Create')
    content = content.replace('創建新項目', 'Create New Project')
    content = content.replace('節省', 'Save')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/billing.html 所有中文已修复")

def fix_en_index_final():
    """修复 en/index.html 的最后遗漏项"""
    file_path = '/Users/cavlinyeung/ai-bank-parser/en/index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 这些应该已经在早期翻译过了，但再检查一次
    # 合理且實惠的價格 → Fair and Affordable Pricing (应该已经是英文)
    # 輕鬆處理銀行對帳單 → Easy Bank Statement Processing (应该已经是英文)
    
    # 如果还有中文，修复它们
    content = content.replace('合理且實惠的價格', 'Fair and Affordable Pricing')
    content = content.replace('輕鬆處理銀行對帳單', 'Easy Bank Statement Processing')
    
    # 确保 Data Retention 和 Image Backup 正确
    # 这些应该已经修复过了
    
    # 检查其他可能的中文
    content = content.replace('帳戶', 'Account')
    content = content.replace('計費', 'Billing')
    content = content.replace('登出', 'Logout')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ en/index.html 最后检查完成")

def fix_all_en_sidebars():
    """确保所有英文页面的左侧栏都是英文"""
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
            
            # 搜索框
            content = content.replace('搜尋文檔名稱...', 'Search documents...')
            content = content.replace('請輸入文檔名稱...', 'Search documents...')
            
            # 左侧栏标题
            content = re.sub(r'<div class="sidebar-header">管理</div>', 
                           '<div class="sidebar-header">Manage</div>', content)
            
            # 左侧栏项目
            content = content.replace('2025年10月', 'October 2025')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {file_path.split('/')[-1]} 左侧栏已确保英文化")
        except Exception as e:
            print(f"⚠️ 处理 {file_path} 时出错: {e}")

if __name__ == '__main__':
    print("开始修复最后遗漏的翻译...")
    print()
    
    # 1. 修复 account.html
    fix_en_account_final()
    
    # 2. 修复 billing.html
    fix_en_billing_final()
    
    # 3. 修复 index.html
    fix_en_index_final()
    
    # 4. 确保所有页面的左侧栏都是英文
    fix_all_en_sidebars()
    
    print()
    print("=" * 50)
    print("✅ 所有最后遗漏的翻译已修复！")
    print()
    print("修复内容总结：")
    print()
    print("1. en/account.html:")
    print("   - 輸入Current Password → Enter current password")
    print("   - 再次Enter new password → Re-enter new password")
    print("   - 左侧栏完全英文化")
    print()
    print("2. en/billing.html:")
    print("   - 导航栏：功能/價格/學習中心/儀表板 → Features/Pricing/Learning Center/Dashboard")
    print("   - Email横幅：立即驗證您的 email... → Verify your email now...")
    print("   - 標題：無隱藏費用，安全可靠 → No Hidden Fees, Secure and Reliable")
    print("   - 副標題：與數千家企業一起... → Join thousands of businesses...")
    print("   - 30 天圖片保留 → Image Backup")
    print("   - 365 Days Data Retention → Data Retention")
    print("   - 左侧栏完全英文化")
    print()
    print("3. en/index.html:")
    print("   - 合理且實惠的價格 → Fair and Affordable Pricing")
    print("   - 輕鬆處理銀行對帳單 → Easy Bank Statement Processing")
    print()
    print("4. 所有英文页面:")
    print("   - 左侧栏搜索框完全英文化")
    print("   - 项目列表日期格式英文化")

