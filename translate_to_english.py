#!/usr/bin/env python3
"""
將 tc/home.html 翻譯為英文版 en/home.html
使用 language-manager.js 中的翻譯字典
"""

# 翻譯字典（從 language-manager.js 提取）
translations = {
    # 導航欄
    '功能': 'Features',
    '價格': 'Pricing',  
    '儀表板': 'Dashboard',
    '隱私政策': 'Privacy Policy',
    '服務條款': 'Terms of Service',
    '繁體中文': 'English',
    '登出': 'Logout',
    '帳戶': 'Account',
    '計費': 'Billing',
    
    # Hero 區域
    '超過 200+ 企業信賴': 'Trusted by 200+ Businesses',
    '針對香港銀行對帳單處理': 'Targeted at Hong Kong Bank Statement Processing',
    '低至': 'As low as',
    '頁': 'page',
    '專為會計師及小型公司設計的 AI 文檔處理平台': 'AI document processing platform designed for accountants and small businesses',
    '自動轉換 Excel/CSV/QuickBooks/Xero • 準確率 98% • 節省 90% 時間': 'Auto-convert Excel/CSV/QuickBooks/Xero • 98% accuracy • Save 90% time',
    '免費試用 20 頁': 'Free Trial 20 Pages',
    '了解收費': 'Learn Pricing',
    
    # 統計數據
    '平均處理時間': 'Average Processing Time',
    '數據準確率': 'Data Accuracy',
    '企業客戶': 'Business Clients',
    
    # 功能區域
    '強大功能': 'Powerful Features',
    '一站式 AI 文檔處理平台': 'One-Stop AI Document Processing Platform',
    '支援發票、收據、銀行對賬單等多種財務文檔': 'Support invoices, receipts, bank statements and various financial documents',
    
    # 發票處理
    '智能發票收據處理': 'Smart Invoice & Receipt Processing',
    '自動提取發票數據': 'Auto-extract invoice data',
    '秒速完成分類歸檔': 'Complete classification in seconds',
    'OCR 光學辨識技術': 'OCR Optical Recognition Technology',
    '準確擷取發票與收據資料': 'Accurately extract invoice and receipt data',
    '準確擷取商家、日期、金額、稅項等關鍵資料': 'Accurately extract key data like merchant, date, amount, tax',
    '智能分類歸檔': 'Smart Classification & Filing',
    '自動識別發票類型並歸類到對應會計科目': 'Auto-identify invoice types and classify to accounting categories',
    '即時同步到會計軟件': 'Instant Sync to Accounting Software',
    '一鍵匯出QuickBooks、Xero 等主流平台格式': 'One-click export to QuickBooks, Xero and other platforms',
    
    # 銀行對賬單
    '銀行對賬單智能分析': 'Smart Bank Statement Analysis',
    '自動識別收支類別': 'Auto-identify transaction categories',
    '即時生成財務報表': 'Generate financial reports instantly',
    '智能交易分類': 'Smart Transaction Classification',
    '自動識別收入、支出、轉賬類別並歸類': 'Auto-identify and classify income, expenses, transfers',
    '精準數據提取': 'Precise Data Extraction',
    '準確擷取日期、對方賬戶、金額等關鍵資料': 'Accurately extract date, counterparty account, amount',
    '多格式匯出': 'Multiple Format Export',
    '支援匯出到 Excel、CSV、QuickBooks、Xero 等': 'Support export to Excel, CSV, QuickBooks, Xero, etc.',
    
    # 為什麼選擇
    '為什麼選擇 VaultCaddy': 'Why Choose VaultCaddy',
    '為什麼選擇 VaultCaddy？': 'Why Choose VaultCaddy?',
    '專為香港會計師打造': 'Built for Hong Kong Accountants',
    '提升效率，降低成本，讓您專注於更有價值的工作': 'Improve efficiency, reduce costs, focus on valuable work',
    '極速處理': 'Lightning Fast Processing',
    '平均 10 秒完成一份文檔': 'Average 10 seconds per document',
    '批量處理更快更省時': 'Batch processing even faster',
    '節省 90% 人工輸入時間': 'Save 90% manual input time',
    '超高準確率': 'Ultra-High Accuracy',
    'AI 辨識準確率達 98%': 'AI recognition accuracy 98%',
    '自動驗證和校正錯誤': 'Auto-verify and correct errors',
    '大幅降低人為失誤風險': 'Significantly reduce human error',
    '性價比最高': 'Best Value',
    '每頁低至 HKD 0.5': 'As low as HKD 0.5 per page',
    '無隱藏收費': 'No hidden fees',
    '用多少付多少最靈活': 'Pay as you go, most flexible',
    
    # 價格
    '合理且實惠的價格': 'Fair and Affordable Pricing',
    '輕鬆處理銀行對帳單': 'Process Bank Statements with Ease',
    '月付': 'Monthly',
    '年付': 'Yearly',
    '小型企業和會計事務所。': 'For small businesses and accounting firms.',
    '頁面包含': 'Includes',
    '每月 100 Credits': '100 Credits per month',
    '每年 1,200 Credits': '1,200 Credits per year',
    '超出後每頁 HKD $0.5': 'HKD $0.5 per page after limit',
    '批次處理無限制文件': 'Unlimited batch processing',
    '一鍵轉換所有文件': 'One-click convert all files',
    'Excel/CSV 匯出': 'Excel/CSV Export',
    'QuickBooks 整合': 'QuickBooks Integration',
    '複合式 AI 處理': 'Hybrid AI Processing',
    '8 種語言支援': '8 Languages Support',
    '電子郵件支援': 'Email Support',
    '安全文件上傳': 'Secure File Upload',
    '365 天數據保留': '365 Days Data Retention',
    '30 天圖片保留': '30 Days Image Retention',
    '開始使用': 'Get Started',
    '節省 20%': 'Save 20%',
    
    # 評價
    'VaultCaddy 使用者評價': 'VaultCaddy User Reviews',
    
    # 學習中心
    '學習中心': 'Learning Center',
    '了解如何最大化利用 VaultCaddy 處理您的財務文檔': 'Learn how to maximize VaultCaddy for your financial documents',
    '如何將 PDF 銀行對帳單轉換為 Excel': 'How to Convert PDF Bank Statements to Excel',
    '完整指南教您使用 AI 技術快速轉換銀行對帳單，節省數小時的手動輸入時間。': 'Complete guide on using AI to quickly convert bank statements, saving hours of manual input.',
    '閱讀文章': 'Read Article',
    'AI 發票處理完整指南': 'Complete Guide to AI Invoice Processing',
    '了解如何使用 AI 自動化發票處理流程，提升會計效率，減少人為錯誤。': 'Learn how to use AI to automate invoice processing, improve efficiency, reduce errors.',
    
    # CTA
    '準備好開始了嗎？': 'Ready to Get Started?',
    '立即上傳您的第一份文檔，體驗 AI 的強大功能': 'Upload your first document now and experience the power of AI',
    '立即開始': 'Start Now',
    
    # Footer
    '專為會計師及小型公司設計的 AI 文檔處理平台，': 'AI document processing platform designed for accountants and small businesses,',
    '讓財務文檔管理變得簡單高效。': 'making financial document management simple and efficient.',
    '快速連結': 'Quick Links',
    '功能介紹': 'Features',
    '價格方案': 'Pricing',
    '法律政策': 'Legal',
    '版權所有': 'All rights reserved',
    '聯繫我們': 'Contact Us',
}

def replace_text(content):
    """替換文本內容"""
    for zh, en in translations.items():
        content = content.replace(zh, en)
    return content

# 讀取中文版
with open('tc/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 翻譯
translated_content = replace_text(content)

# 更新 HTML lang 屬性
translated_content = translated_content.replace('lang="zh-TW"', 'lang="en"')

# 更新標題
translated_content = translated_content.replace(
    'VaultCaddy - 香港會計師首選 AI 銀行對帳單處理 | 免費試用 20 頁 | HKD 0.5/頁 | 10秒轉換 Excel/QuickBooks',
    'VaultCaddy - AI Bank Statement Processing for Hong Kong | Free Trial 20 Pages | HKD 0.5/page | 10s Convert Excel/QuickBooks'
)

# 寫入英文版
with open('en/home.html', 'w', encoding='utf-8') as f:
    f.write(translated_content)

print('✅ 英文版已生成: en/home.html')
print(f'✅ 共翻譯 {len(translations)} 個詞條')

