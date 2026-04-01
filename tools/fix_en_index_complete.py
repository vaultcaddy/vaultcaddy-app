#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整修复英文版首页的所有中文内容
Fix all Chinese content in English version homepage
"""

import re
import sys

def fix_en_index():
    """修复en/index.html中的所有中文内容"""
    
    file_path = 'en/index.html'
    
    print("🔍 读取文件:", file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计原始中文字符数
    chinese_chars_before = len(re.findall(r'[一-龥]', content))
    print(f"📊 发现 {chinese_chars_before} 个中文字符需要翻译")
    
    # ============================================
    # 第1部分：HTML/JavaScript注释翻译
    # ============================================
    print("\n🔄 翻译HTML和JavaScript注释...")
    
    comment_translations = {
        # HTML注释
        'CDN 版本 - compat': 'CDN version - compat',
        '🔥 Simplified system': '🔥 Simplified system',
        '💡 注意：卡片現在使用 inline styles, 不需要這些 CSS': '💡 Note: Cards now use inline styles, these CSS rules are not needed',
        '滑動動畫基礎設置': 'Slide animation base settings',
        '延遲動畫': 'Delayed animation',
        '從左滑入': 'Slide in from left',
        '從右滑入': 'Slide in from right',
        '縮放動畫': 'Scale animation',
        '創建 Intersection Observer': 'Create Intersection Observer',
        '增强型 Schema.org 结构化数据 - SEO优化': 'Enhanced Schema.org structured data - SEO optimization',
        'FAQ Schema - 常见问题（会在Google搜索结果展示）': 'FAQ Schema - Frequently Asked Questions (shown in Google search results)',
        'WebSite Schema - 网站搜索功能': 'WebSite Schema - website search function',
        'BreadcrumbList Schema - 面包屑导航': 'BreadcrumbList Schema - breadcrumb navigation',
        '资源提示 - 优化加载速度': 'Resource hints - optimize loading speed',
        '🌐 多语言数据互通系统': '🌐 Multilingual data synchronization system',
        '8折優惠橫幅': '20% discount banner',
        'Scroll Progress Bar - 阅读进度': 'Scroll Progress Bar - reading progress',
        '立即執行的頁面可見性腳本': 'Immediately executed page visibility script',
        '✅ 統一靜態導航欄（與 firstproject.html 完全一致）': '✅ Unified static navigation bar (identical to firstproject.html)',
        '漢堡菜單按鈕（僅手機顯示）': 'Hamburger menu button (mobile only)',
        '🌍 桌面版語言選擇器': '🌍 Desktop language selector',
        '初始狀態：不顯示任何內容, 由 JavaScript 動態更新': 'Initial state: no content displayed, dynamically updated by JavaScript',
        '手機側邊欄菜單': 'Mobile sidebar menu',
        '菜單項': 'Menu items',
        '🌍 手機版語言選擇器': '🌍 Mobile language selector',
        '側邊欄遮罩': 'Sidebar overlay',
        '用戶下拉菜單': 'User dropdown menu',
        '✅ index.html 動態更新用戶狀態': '✅ index.html dynamically updates user status',
        'index.html 初始化': 'index.html initialization',
        
        # JavaScript注释
        '立即執行的頁面可見性腳本': 'Immediately executed page visibility script',
        '檢查是否已登入': 'Check if logged in',
        '等待 initializeAuth 完成': 'Wait for initializeAuth to complete',
        '用戶已登入': 'User logged in',
        '未登入': 'Not logged in',
        '正在獲取用戶資料': 'Fetching user data',
        '用戶資料獲取成功': 'User data fetched successfully',
        '用戶資料獲取失敗': 'Failed to fetch user data',
        '頁面加載完成': 'Page loaded',
    }
    
    for chinese, english in comment_translations.items():
        content = content.replace(chinese, english)
    
    # ============================================
    # 第2部分：FAQ Schema 中文翻译
    # ============================================
    print("🔄 翻译FAQ Schema...")
    
    # FAQ问题1
    content = content.replace(
        '"name": "VaultCaddy 支援哪些銀行？"',
        '"name": "Which banks does VaultCaddy support?"'
    )
    content = content.replace(
        '"text": "VaultCaddy 支援香港所有主要銀行，包括匯豐銀行(HSBC)、恆生銀行(Hang Seng)、中國銀行香港(BOC HK)、渣打銀行(Standard Chartered)、東亞銀行(BEA)、星展銀行(DBS)等。支援商業戶口和個人戶口的對帳單。"',
        '"text": "VaultCaddy supports all major Hong Kong banks, including HSBC, Hang Seng Bank, Bank of China Hong Kong (BOC HK), Standard Chartered, Bank of East Asia (BEA), DBS Bank, etc. Supports both business and personal account statements."'
    )
    
    # FAQ问题2
    content = content.replace(
        '"name": "VaultCaddy 的收費是多少？"',
        '"name": "How much does VaultCaddy cost?"'
    )
    content = content.replace(
        '"text": "VaultCaddy 提供兩種方案：月付方案 HK$58/月，包含100頁免費處理，超出後每頁HK$0.5；年付方案 HK$552/年（相當於HK$46/月），同樣包含100頁免費處理。新用戶可免費試用20頁。使用優惠碼SAVE20可享首月8折優惠。"',
        '"text": "VaultCaddy offers two plans: Monthly plan at HK$58/month, including 100 pages free processing, additional pages at HK$0.5 each; Annual plan at HK$552/year (equivalent to HK$46/month), also including 100 pages free processing. New users can try 20 pages free. Use code SAVE20 for 20% off first month."'
    )
    
    # FAQ问题3
    content = content.replace(
        '"name": "VaultCaddy 的準確率如何？"',
        '"name": "What is VaultCaddy\'s accuracy rate?"'
    )
    content = content.replace(
        '"text": "VaultCaddy 使用專門訓練的AI模型，對香港銀行對帳單的識別準確率達98%以上。系統可自動識別日期、金額、交易描述、餘額等所有欄位，並支援人工修正。"',
        '"text": "VaultCaddy uses specially trained AI models with over 98% accuracy for Hong Kong bank statements. The system automatically recognizes all fields including dates, amounts, transaction descriptions, balances, and supports manual corrections."'
    )
    
    # FAQ问题4
    content = content.replace(
        '"name": "VaultCaddy 支援哪些會計軟件？"',
        '"name": "Which accounting software does VaultCaddy support?"'
    )
    content = content.replace(
        '"text": "VaultCaddy 支援QuickBooks、Xero、MYOB等主流會計軟件，也可匯出Excel (.xlsx)、CSV等通用格式。系統會自動將交易分類，方便直接匯入會計軟件。"',
        '"text": "VaultCaddy supports mainstream accounting software including QuickBooks, Xero, MYOB, and can export to universal formats like Excel (.xlsx) and CSV. The system automatically categorizes transactions for direct import into accounting software."'
    )
    
    # FAQ问题5
    content = content.replace(
        '"name": "處理一份對帳單需要多久？"',
        '"name": "How long does it take to process a statement?"'
    )
    content = content.replace(
        '"text": "VaultCaddy 平均處理一份銀行對帳單只需10秒，包括上傳、AI識別、分類和匯出。人工手動輸入同樣的對帳單平均需要2小時，VaultCaddy 可節省99.9%的時間。"',
        '"text": "VaultCaddy processes an average bank statement in just 10 seconds, including upload, AI recognition, categorization, and export. Manual input of the same statement typically takes 2 hours. VaultCaddy saves 99.9% of the time."'
    )
    
    # FAQ问题6
    content = content.replace(
        '"name": "VaultCaddy 的數據安全嗎？"',
        '"name": "Is VaultCaddy\'s data secure?"'
    )
    content = content.replace(
        '"text": "VaultCaddy 採用銀行級256位元加密技術，符合香港私隱條例。所有數據儲存在香港本地數據中心，並通過SOC 2安全認證。用戶可隨時刪除數據，我們不會將數據用於其他用途。"',
        '"text": "VaultCaddy uses bank-grade 256-bit encryption technology, compliant with Hong Kong privacy regulations. All data is stored in Hong Kong local data centers and SOC 2 security certified. Users can delete data at any time, and we do not use data for other purposes."'
    )
    
    # ============================================
    # 第3部分：WebSite Schema 描述翻译
    # ============================================
    print("🔄 翻译WebSite Schema...")
    
    content = content.replace(
        '"description": "AI銀行對帳單處理平台 - 香港專業版"',
        '"description": "AI Bank Statement Processing Platform - Hong Kong Professional Edition"'
    )
    
    # ============================================
    # 第4部分：BreadcrumbList Schema 翻译
    # ============================================
    print("🔄 翻译Breadcrumb...")
    
    content = content.replace(
        '"name": "首頁"',
        '"name": "Home"'
    )
    
    # ============================================
    # 第5部分：继续查找并翻译更多中文内容
    # ============================================
    print("🔄 翻译页面主体内容...")
    
    # 这里需要继续读取文件的其他部分来找到所有中文
    # 让我保存当前进度并继续
    
    # 统计翻译后的中文字符数
    chinese_chars_after = len(re.findall(r'[一-龥]', content))
    
    print(f"\n📊 翻译进度:")
    print(f"  翻译前: {chinese_chars_before} 个中文字符")
    print(f"  翻译后: {chinese_chars_after} 个中文字符")
    print(f"  已翻译: {chinese_chars_before - chinese_chars_after} 个字符")
    print(f"  剩余: {chinese_chars_after} 个字符需要继续翻译")
    
    # 保存当前进度
    print(f"\n💾 保存文件...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 第一阶段翻译完成！")
    print(f"⚠️  还需要继续翻译剩余的 {chinese_chars_after} 个中文字符")
    
    return chinese_chars_after

if __name__ == '__main__':
    try:
        remaining = fix_en_index()
        if remaining > 0:
            print(f"\n🔄 需要继续翻译...")
            sys.exit(1)  # 表示还需要继续
        else:
            print(f"\n🎉 所有翻译完成！")
            sys.exit(0)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

