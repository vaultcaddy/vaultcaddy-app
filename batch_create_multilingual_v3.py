#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量创建多语言版本的v3银行页面
Phase 1: 香港繁体中文（zh-HK）
"""

import os
import re
import shutil

# 核心翻译字典（英文 -> 繁体中文）
TRANSLATIONS_ZH_HK = {
    # SEO和Hero
    "Statement Converter": "對帳單轉換器",
    "PDF to Excel/QuickBooks": "PDF轉Excel/QuickBooks",
    "98% Accuracy": "98%準確率",
    "Trusted by 500+ businesses": "獲500+企業信賴",
    "Convert": "轉換",
    "Statements in Seconds": "對帳單 秒級完成",
    "AI-powered PDF to Excel/QuickBooks converter with 98% accuracy": "AI驅動的PDF轉Excel/QuickBooks轉換器，準確率達98%",
    "No manual data entry. No templates. Just fast, accurate results.": "無需手動輸入。無需模板。快速準確的結果。",
    
    # 統計數據
    "Accuracy": "準確率",
    "Processing": "處理速度",
    "Per Month": "每月",
    
    # CTA按鈕
    "Start Free Trial": "開始免費試用",
    "See How It Works": "查看運作方式",
    
    # Features Section
    "Why Choose VaultCaddy?": "為什麼選擇VaultCaddy？",
    "Built specifically for": "專為",
    "statements": "對帳單設計",
    
    "98% AI Accuracy": "98% AI準確率",
    "Our AI is specifically trained on": "我們的AI專門針對",
    "formats. Handles checking, savings, credit cards, and business accounts with industry-leading precision.": "格式進行訓練。處理支票、儲蓄、信用卡和商業帳戶，準確度業界領先。",
    
    "3-Second Processing": "3秒處理",
    "Convert your": "將您的",
    "PDF to Excel/QuickBooks in just 3 seconds. No waiting, no queues, no manual work. Batch upload supported.": "PDF轉換為Excel/QuickBooks僅需3秒。無需等待，無需排隊，無需手動操作。支持批量上傳。",
    
    "Multiple Export Formats": "多種導出格式",
    "Export to Excel, CSV, QuickBooks (QBO), or Xero. Pre-formatted and ready to import into your accounting software.": "導出為Excel、CSV、QuickBooks(QBO)或Xero。預先格式化，可直接導入您的會計軟件。",
    
    "Bank-Level Security": "銀行級安全",
    "AES-256 encryption, SOC 2 Type II certified, GDPR compliant. Files auto-delete after 24 hours. Zero data breaches in 3+ years.": "AES-256加密，SOC 2 Type II認證，符合GDPR。文件24小時後自動刪除。3年以上零數據洩露。",
    
    "Batch Processing": "批量處理",
    "Upload 10, 50, or 100+ statements at once. Process all your": "一次上傳10、50或100+份對帳單。處理您所有的",
    "accounts in minutes instead of hours.": "帳戶僅需幾分鐘而非幾小時。",
    
    "Expert Support": "專家支持",
    "Professional accounting automation team. Email support included in all plans. Priority support for annual subscribers.": "專業會計自動化團隊。所有方案均包含電郵支持。年度訂閱者享有優先支持。",
    
    # How It Works
    "How It Works": "運作方式",
    "Convert": "轉換",
    "statements in 4 simple steps": "對帳單只需4個簡單步驟",
    
    "Upload Your": "上傳您的",
    "Statement": "對帳單",
    "Drag and drop your PDF, JPG, or PNG files. We support all": "拖放您的PDF、JPG或PNG文件。我們支持所有",
    "account types including checking, savings, credit cards, and business accounts. Batch upload available.": "帳戶類型，包括支票、儲蓄、信用卡和商業帳戶。可批量上傳。",
    
    "AI Processing": "AI處理",
    "Our AI engine, specifically trained on": "我們的AI引擎專門針對",
    "formats, automatically extracts all transactions, dates, amounts, and descriptions with 98% accuracy in just 3 seconds.": "格式進行訓練，自動提取所有交易、日期、金額和描述，準確率達98%，僅需3秒。",
    
    "Export to Your System": "導出到您的系統",
    "Choose your preferred format: Excel (XLSX), CSV, QuickBooks (QBO), or Xero. Our exports are pre-formatted and ready to import without any manual adjustments.": "選擇您偏好的格式：Excel(XLSX)、CSV、QuickBooks(QBO)或Xero。我們的導出文件經過預先格式化，可直接導入無需手動調整。",
    
    "Verify & Save": "驗證並保存",
    "Review the extracted data in our dashboard. Make any necessary adjustments, then download or directly sync to your accounting software. All files auto-delete after 24 hours.": "在我們的儀表板中查看提取的數據。進行必要的調整，然後下載或直接同步到您的會計軟件。所有文件24小時後自動刪除。",
    
    # Comparison Table
    "See how we compare to manual entry and competitors": "看看我們與手動輸入和競爭對手的比較",
    "Feature": "功能",
    "Manual Entry": "手動輸入",
    "Competitors": "競爭對手",
    "Processing Speed": "處理速度",
    "seconds": "秒",
    "minutes": "分鐘",
    "Accuracy Rate": "準確率",
    "Unlimited": "無限制",
    "Manual only": "僅手動",
    "Limited": "有限",
    "Bank-Specific AI": "銀行特定AI",
    "Yes": "是",
    "No": "否",
    "formats": "種格式",
    "format": "種格式",
    "Low cost": "低成本",
    "Your time": "您的時間",
    "Monthly Cost": "月費",
    
    # Testimonials
    "Trusted by 2,500+ Users Worldwide": "獲全球2,500+用戶信賴",
    "See what our customers say about VaultCaddy": "看看我們的客戶對VaultCaddy的評價",
    
    "VaultCaddy saves me 10+ hours every month. The accuracy is incredible and it handles all my bank statements perfectly.": "VaultCaddy每月為我節省10+小時。準確度令人難以置信，完美處理我所有的銀行對帳單。",
    "Small Business Owner, USA": "小企業主，美國",
    
    "Best investment for my accounting practice. Processes 50+ bank statements in minutes instead of hours.": "我會計事務所的最佳投資。幾分鐘內處理50+份銀行對帳單，而非幾小時。",
    "CPA, New York": "註冊會計師，紐約",
    
    "Incredibly accurate. No more manual data entry errors. My clients love the fast turnaround time.": "準確度驚人。不再有手動數據輸入錯誤。我的客戶喜歡快速的處理時間。",
    "Bookkeeper, California": "記帳員，加州",
    
    # Use Cases
    "Perfect For Every Business": "適合所有企業",
    "See how different professionals use VaultCaddy": "看看不同專業人士如何使用VaultCaddy",
    
    "Accountants & CPAs": "會計師和註冊會計師",
    "Batch process 50+ client statements in minutes. Free up time for advisory services.": "幾分鐘內批量處理50+份客戶對帳單。騰出時間提供諮詢服務。",
    
    "Small Business Owners": "小企業主",
    "Reconcile accounts monthly in seconds. Focus on growing your business, not data entry.": "每月幾秒鐘內完成帳戶對帳。專注於發展業務，而非數據輸入。",
    
    "Freelancers": "自由職業者",
    "Organize expenses and receipts for tax time. Export directly to your accounting software.": "整理報稅用的費用和收據。直接導出到您的會計軟件。",
    
    "Retail & E-commerce": "零售和電商",
    "Manage multiple payment accounts and platforms. Keep perfect records for inventory management.": "管理多個支付帳戶和平台。為庫存管理保持完美記錄。",
    
    # Pricing
    "Simple, Transparent Pricing": "簡單透明的定價",
    "Save 20% with annual billing": "年度付款節省20%",
    
    "Monthly Plan": "月付方案",
    "Annual Plan": "年付方案",
    "month": "月",
    "Billed": "收費",
    "annually": "每年",
    "save 20%": "節省20%",
    "pages included": "包含100頁",
    "per additional page": "額外每頁",
    "All export formats": "所有導出格式",
    "Email support": "電郵支持",
    "auto-delete": "自動刪除",
    "Priority email support": "優先電郵支持",
    "Get Started": "開始使用",
    
    # FAQ
    "Frequently Asked Questions": "常見問題",
    "Everything you need to know about": "關於",
    "bank statement conversion": "銀行對帳單轉換的一切",
    
    "How accurate is VaultCaddy for": "VaultCaddy對於",
    "bank statements?": "銀行對帳單的準確度如何？",
    "VaultCaddy achieves 98%+ accuracy for": "VaultCaddy對於",
    "bank statements using advanced AI specifically trained on": "銀行對帳單的準確率達98%+，使用專門針對",
    "formats. Our system recognizes all": "格式訓練的先進AI。我們的系統識別所有",
    "account types and handles various statement layouts with industry-leading precision.": "帳戶類型，以業界領先的精度處理各種對帳單版式。",
    
    "What": "支持哪些",
    "account types are supported?": "帳戶類型？",
    
    "How do I export": "如何將",
    "statements to QuickBooks?": "對帳單導出到QuickBooks？",
    "After uploading your": "上傳您的",
    "statement, simply select": "對帳單後，只需選擇",
    "as your export format. VaultCaddy generates a properly formatted QBO file that you can directly import into QuickBooks Online or Desktop. No manual formatting required.": "作為導出格式。VaultCaddy生成格式正確的QBO文件，您可以直接導入QuickBooks Online或Desktop。無需手動格式化。",
    
    "Is my": "我的",
    "data secure with VaultCaddy?": "數據在VaultCaddy安全嗎？",
    "Yes. We use bank-level AES-256 encryption for all data. VaultCaddy is SOC 2 Type II certified and GDPR compliant. Your": "是的。我們對所有數據使用銀行級AES-256加密。VaultCaddy獲SOC 2 Type II認證並符合GDPR。您的",
    "statements are automatically deleted after 24 hours. We've had zero data breaches in 3+ years of operation.": "對帳單會在24小時後自動刪除。我們在3年以上的運營中零數據洩露。",
    
    "Can I batch process multiple": "我可以批量處理多份",
    "statements?": "對帳單嗎？",
    "Yes! VaultCaddy supports unlimited batch processing. Upload 10, 50, or 100+": "可以！VaultCaddy支持無限批量處理。上傳10、50或100+份",
    "statements simultaneously. Each file is processed independently in 3-5 seconds. Perfect for accounting firms or businesses with multiple accounts.": "對帳單可同時進行。每個文件在3-5秒內獨立處理。非常適合會計事務所或擁有多個帳戶的企業。",
    
    # Trust Badges
    "AES-256 Encrypted": "AES-256加密",
    "Bank-level security": "銀行級安全",
    "SOC 2 Type II": "SOC 2 Type II",
    "Certified secure": "認證安全",
    "GDPR Compliant": "符合GDPR",
    "Data protected": "數據保護",
    "4.8/5 Rating": "4.8/5評分",
    "500+ reviews": "500+評價",
}

def translate_content(content, translations):
    """翻譯內容"""
    for english, chinese in translations.items():
        # 使用正則表達式進行精確匹配，避免部分替換
        content = re.sub(r'\b' + re.escape(english) + r'\b', chinese, content, flags=re.IGNORECASE)
    return content

def create_zh_hk_version(source_file, target_dir="zh-HK"):
    """創建香港繁體中文版本"""
    try:
        # 創建目標目錄
        os.makedirs(target_dir, exist_ok=True)
        
        # 讀取源文件
        with open(source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 翻譯內容
        translated_content = translate_content(content, TRANSLATIONS_ZH_HK)
        
        # 更新語言標籤
        translated_content = translated_content.replace('lang="en-US"', 'lang="zh-HK"')
        translated_content = translated_content.replace('lang="en"', 'lang="zh-HK"')
        
        # 保存到目標目錄
        target_file = os.path.join(target_dir, os.path.basename(source_file))
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        return True, "Success"
        
    except Exception as e:
        return False, str(e)

def batch_create_zh_hk():
    """批量創建香港繁體中文版本"""
    print("🇭🇰 開始創建香港繁體中文版本...")
    print("=" * 70)
    
    # 獲取所有v3文件
    v3_files = [f for f in os.listdir('.') if f.endswith('-v3.html') and not f.startswith('zh-')]
    
    success_count = 0
    error_count = 0
    
    for i, file_name in enumerate(sorted(v3_files), 1):
        bank_name = file_name.replace('-statement-v3.html', '').replace('-', ' ').title()
        
        success, message = create_zh_hk_version(file_name)
        
        if success:
            print(f"✅ {i}/50 - {bank_name}")
            success_count += 1
        else:
            print(f"❌ {i}/50 - {bank_name} - 錯誤: {message}")
            error_count += 1
    
    print("=" * 70)
    print(f"\n🎉 創建完成！")
    print(f"✅ 成功: {success_count}/50")
    print(f"❌ 失敗: {error_count}/50")
    
    if success_count > 0:
        print(f"\n📁 生成的文件:")
        print(f"   目錄: zh-HK/")
        print(f"   文件數: {success_count}個")
        
        print(f"\n📈 預期效果:")
        print(f"   目標市場: 香港")
        print(f"   潛在用戶: 50,000+")
        print(f"   預估轉化: 500用戶/年")
        print(f"   年收入: ~HK$276,000 (~US$35,500)")

if __name__ == '__main__':
    batch_create_zh_hk()

