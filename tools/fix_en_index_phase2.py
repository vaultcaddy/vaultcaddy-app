#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第二阶段：翻译JavaScript代码中的中文注释和console.log
"""

import re

def fix_en_index_phase2():
    """修复JavaScript中的所有中文"""
    
    file_path = 'en/index.html'
    
    print("🔍 Phase 2: 翻译JavaScript内容...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符")
    
    # ============================================
    # JavaScript 注释和 console.log 翻译
    # ============================================
    
    js_translations = {
        # 用户菜单相关
        '更新下拉菜單內容': 'Update dropdown menu content',
        '點擊外部關閉下拉菜單': 'Close dropdown menu when clicking outside',
        'Logout功能': 'Logout functionality',
        'Logout失敗': 'Logout failed',
        '🔥 與 dashboard.html 完全相同的更新方式': '🔥 Same update method as dashboard.html',
        '✅ 已登入：顯示用戶頭像': '✅ Logged in: Show user avatar',
        '🔥 從 Firestore 獲取 displayName 和 credits': '🔥 Fetch displayName and credits from Firestore',
        '✅ index.html 獲取 Credits': '✅ index.html fetched Credits',
        '⚠️ 無法從 Firestore 獲取用戶資料': '⚠️ Unable to fetch user data from Firestore',
        '⏳ SimpleDataManager 尚未初始化, 等待中...': '⏳ SimpleDataManager not yet initialized, waiting...',
        '延遲重試': 'Delayed retry',
        '✅ 延遲獲取 Credits': '✅ Delayed fetch Credits',
        '❌ 延遲獲取失敗': '❌ Delayed fetch failed',
        '👤 用戶首字母': '👤 User initial',
        '🔥 已登入：顯示頭像和下拉菜單': '🔥 Logged in: Show avatar and dropdown menu',
        '✅ Not logged in：顯示登入按鈕': '✅ Not logged in: Show login button',
        '登入': 'Login',
        '❌ Cannot update user menu': '❌ Cannot update user menu',
        
        # 初始化相關
        '🔥 優化：只在 SimpleAuth 初始化後才更新（刪除立即調用）': '🔥 Optimization: Only update after SimpleAuth initialization (remove immediate call)',
        'SimpleAuth 尚未初始化': 'SimpleAuth not yet initialized',
        '監聽 Firebase 和 Auth 事件': 'Listen to Firebase and Auth events',
        '延遲檢查（等待 SimpleAuth 初始化完成）': 'Delayed check (waiting for SimpleAuth initialization)',
        '0.5s後首次檢查': 'First check after 0.5s',
        '1s後再次檢查': 'Check again after 1s',
        '2s後最終確認': 'Final confirmation after 2s',
        '暴露 toggleDropdown 到全局': 'Expose toggleDropdown to global scope',
        
        # 手机版样式相关
        '🔥 手機版強制修改樣式（解決CSS無法覆蓋內聯樣式的問題）': '🔥 Force mobile styles (solve CSS inline style override issue)',
        '僅在手機版執行': 'Execute on mobile only',
        '🔥 強制應用手機版樣式': '🔥 Force apply mobile styles',
        '價值卡片（Ultra-Fast Processing、超高準確率、性價比最高）': 'Value cards (Ultra-Fast Processing, Highest Accuracy, Best Cost Performance)',
        '修改圖標容器': 'Modify icon container',
        '修改標題': 'Modify title',
        '修改段落': 'Modify paragraph',
        '功能組優化（手機版）- 使用更精確的選擇器': 'Feature group optimization (mobile) - use more precise selectors',
        '🔍 找到': '🔍 Found',
        '個功能組容器': ' feature group containers',
        '找到 grid 容器並改為垂直排列': 'Found grid container and change to vertical layout',
        '✅ 功能組': '✅ Feature group',
        'grid 已改為垂直排列': 'grid changed to vertical layout',
        '徽章置中（找到所有帶有 feature-badge 類的元素）': 'Center badges (find all elements with feature-badge class)',
        '找到': 'Found',
        '個徽章': ' badges',
        '恢復原始大小': 'Restore original size',
        '恢復原始內距': 'Restore original padding',
        '標題置中': 'Center title',
        '個標題': ' titles',
        '減少所有 flex 容器的間距（OCR、智能分類、即時同步等）': 'Reduce spacing of all flex containers (OCR, Smart Classification, Real-time Sync, etc.)',
        '個描述 flex 容器': ' description flex containers',
        '所有描述段落間距都減少 30pt（再減小 10pt）': 'All description paragraph spacing reduced by 30pt (reduced by 10pt more)',
        '已優化完成': 'optimization complete',
        '卡片與上方文字間距減少 20pt': 'Card top margin reduced by 20pt',
        
        # 更多常见中文
        '頁面載入完成': 'Page loaded',
        '初始化完成': 'Initialization complete',
        '初始化失敗': 'Initialization failed',
        '資料載入中': 'Loading data',
        '資料載入完成': 'Data loaded',
        '資料載入失敗': 'Data loading failed',
        '用戶資料': 'User data',
        '獲取失敗': 'Fetch failed',
        '獲取成功': 'Fetch successful',
        '請求失敗': 'Request failed',
        '請求成功': 'Request successful',
        '錯誤': 'Error',
        '警告': 'Warning',
        '成功': 'Success',
        '失敗': 'Failed',
        '載入中': 'Loading',
        '處理中': 'Processing',
        '完成': 'Complete',
        '取消': 'Cancel',
        '確認': 'Confirm',
        '關閉': 'Close',
        '開啟': 'Open',
        '保存': 'Save',
        '刪除': 'Delete',
        '編輯': 'Edit',
        '新增': 'Add',
        '查詢': 'Search',
        '篩選': 'Filter',
        '排序': 'Sort',
        '上傳': 'Upload',
        '下載': 'Download',
        '匯出': 'Export',
        '匯入': 'Import',
        '提交': 'Submit',
        '重設': 'Reset',
        '返回': 'Back',
        '下一步': 'Next',
        '上一步': 'Previous',
        '繼續': 'Continue',
        '跳過': 'Skip',
        '了解更多': 'Learn More',
        '查看詳情': 'View Details',
        '立即開始': 'Get Started',
        '免費試用': 'Free Trial',
        '立即註冊': 'Sign Up Now',
        '已經有帳戶': 'Already have an account',
        '還沒有帳戶': "Don't have an account",
        '忘記密碼': 'Forgot Password',
        '重設密碼': 'Reset Password',
        '變更密碼': 'Change Password',
        '個人資料': 'Profile',
        '帳戶設定': 'Account Settings',
        '通知設定': 'Notification Settings',
        '隱私設定': 'Privacy Settings',
        '安全設定': 'Security Settings',
        '語言設定': 'Language Settings',
        '主題設定': 'Theme Settings',
        '偏好設定': 'Preferences',
        '使用條款': 'Terms of Service',
        '隱私政策': 'Privacy Policy',
        '關於我們': 'About Us',
        '聯絡我們': 'Contact Us',
        '常見問題': 'FAQ',
        '幫助中心': 'Help Center',
        '技術支援': 'Technical Support',
        '客戶服務': 'Customer Service',
    }
    
    print(f"🔄 翻译 {len(js_translations)} 个常见词组...")
    
    # 按长度排序，先替换长的，避免部分匹配
    sorted_translations = sorted(js_translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for chinese, english in sorted_translations:
        content = content.replace(chinese, english)
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 Phase 2 翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    print(f"  剩余: {chinese_chars_after} 个字符")
    
    # 保存文件
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if chinese_chars_after > 0:
        print(f"⚠️  还需要继续翻译剩余的 {chinese_chars_after} 个中文字符")
        return chinese_chars_after
    else:
        print(f"🎉 Phase 2 完成！")
        return 0

if __name__ == '__main__':
    remaining = fix_en_index_phase2()
    print(f"\n{'='*60}")
    if remaining > 0:
        print(f"🔄 需要Phase 3继续翻译...")
    else:
        print(f"✅ 所有JavaScript翻译完成！")

