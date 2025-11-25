/**
 * VaultCaddy Language Manager
 * 
 * 功能：
 * - 管理中英文切換
 * - 動態翻譯頁面內容
 * - 保存用戶語言偏好
 * 
 * 使用方法：
 * 1. 在 HTML 中引入此文件
 * 2. 在需要翻譯的元素上添加 data-i18n="key"
 * 3. 調用 window.languageManager.setLanguage('en') 切換語言
 * 
 * 作用：幫助 AI 快速識別和翻譯頁面元素
 */

(function() {
    'use strict';

    // ============================================
    // 翻譯字典
    // ============================================
    
    const translations = {
        // 導航欄
        'nav.features': {
            'zh': '功能',
            'en': 'Features'
        },
        'nav.pricing': {
            'zh': '價錢',
            'en': 'Pricing'
        },
        'nav.billing': {
            'zh': '計費',
            'en': 'Billing'
        },
        'nav.account': {
            'zh': '帳戶',
            'en': 'Account'
        },
        'nav.dashboard': {
            'zh': '儀表板',
            'en': 'Dashboard'
        },
        'nav.logout': {
            'zh': '登出',
            'en': 'Logout'
        },
        'nav.login': {
            'zh': '登入',
            'en': 'Login'
        },
        'nav.credits': {
            'zh': 'Credits',
            'en': 'Credits'
        },

        // 首頁 Hero Section
        'hero.badge': {
            'zh': '超過 200+ 企業信賴',
            'en': 'Trusted by 200+ Businesses'
        },
        'hero.trust': {
            'zh': '超過 200+ 企業信賴',
            'en': 'Trusted by 200+ Businesses'
        },
        'hero.title1': {
            'zh': '針對香港銀行對帳單處理',
            'en': 'Hong Kong Bank Statement Processing'
        },
        'hero.title2': {
            'zh': '只需',
            'en': 'Only'
        },
        'hero.page': {
            'zh': '頁',
            'en': 'page'
        },
        'hero.subtitle1': {
            'zh': '專為會計師及小型公司設計的 AI 文檔處理平台',
            'en': 'AI Document Processing Platform Designed for Accountants and Small Businesses'
        },
        'hero.subtitle2': {
            'zh': '自動轉換 Excel/CSV/QuickBooks/Xero • 準確率 98% • 節省 90% 時間',
            'en': 'Auto-convert to Excel/CSV/QuickBooks/Xero • 98% Accuracy • Save 90% Time'
        },
        'hero.title': {
            'zh': '只需 HKD 0.5/頁 讓 AI 秒速幫你處理銀行對帳單',
            'en': 'Just HKD 0.5/page AI Processes Bank Statements in Seconds'
        },
        'hero.subtitle': {
            'zh': '香港市場性價比最高的 AI 銀行對帳單處理工具 自動轉換為 Excel/CSV/QuickBooks 格式 • 準確率 98% • 節省 90% 時間',
            'en': 'Hong Kong\'s Most Cost-Effective AI Bank Statement Processing Tool Auto-convert to Excel/CSV/QuickBooks • 98% Accuracy • Save 90% Time'
        },
        'hero.cta': {
            'zh': '免費開始',
            'en': 'Get Started Free'
        },
        'hero.cta_trial': {
            'zh': '免費試用 20 頁',
            'en': 'Free 20-Page Trial'
        },
        'hero.cta_pricing': {
            'zh': '了解收費',
            'en': 'View Pricing'
        },
        
        // 統計數據
        'stats.seconds': {
            'zh': '秒',
            'en': ' seconds'
        },
        'stats.time_desc': {
            'zh': '平均處理時間',
            'en': 'Average Processing Time'
        },
        'stats.accuracy': {
            'zh': '數據準確率',
            'en': 'Data Accuracy'
        },
        'stats.clients': {
            'zh': '企業客戶',
            'en': 'Business Clients'
        },
        
        // 功能區塊
        'features.badge': {
            'zh': '強大功能',
            'en': 'POWERFUL FEATURES'
        },
        'features.title': {
            'zh': '一站式 AI 文檔處理平台',
            'en': 'All-in-One AI Document Processing Platform'
        },
        'features.subtitle': {
            'zh': '支援發票、收據、銀行對賬單等多種財務文檔',
            'en': 'Supports invoices, receipts, bank statements and various financial documents'
        },
        'features.invoice_badge': {
            'zh': '智能發票收據處理',
            'en': 'Smart Invoice & Receipt Processing'
        },
        'features.invoice_title1': {
            'zh': '自動提取發票數據',
            'en': 'Auto Extract Invoice Data'
        },
        'features.invoice_title2': {
            'zh': '秒速完成分類歸檔',
            'en': 'Complete Classification in Seconds'
        },
        'features.ocr_title': {
            'zh': 'OCR 光學辨識技術',
            'en': 'OCR Recognition Technology'
        },
        'features.ocr_desc': {
            'zh': '準確擷取商家、日期、金額、稅項等關鍵資料',
            'en': 'Accurately extract merchant, date, amount, tax and other key data'
        },
        'features.classification_title': {
            'zh': '智能分類歸檔',
            'en': 'Smart Classification'
        },
        'features.classification_desc': {
            'zh': '自動識別發票類型並歸類到對應會計科目',
            'en': 'Auto-identify invoice types and categorize to accounting items'
        },
        'features.sync_title': {
            'zh': '即時同步到會計軟件',
            'en': 'Real-time Sync to Accounting Software'
        },
        'features.sync_desc': {
            'zh': '一鍵匯出QuickBooks、Xero 等主流平台格式',
            'en': 'Export to QuickBooks, Xero and other platforms with one click'
        },
        'features.bank_badge': {
            'zh': '銀行對賬單智能分析',
            'en': 'Smart Bank Statement Analysis'
        },
        'features.bank_title1': {
            'zh': '自動識別收支類別',
            'en': 'Auto-identify Income and Expenses'
        },
        'features.bank_title2': {
            'zh': '即時生成財務報表',
            'en': 'Generate Financial Reports Instantly'
        },
        'features.bank_category_title': {
            'zh': '智能交易分類',
            'en': 'Smart Transaction Classification'
        },
        'features.bank_category_desc': {
            'zh': '自動識別收入、支出、轉賬類別並歸類',
            'en': 'Auto-identify and categorize income, expenses, and transfers'
        },
        'features.bank_extract_title': {
            'zh': '精準數據提取',
            'en': 'Precise Data Extraction'
        },
        'features.bank_extract_desc': {
            'zh': '準確擷取日期、對方賬戶、金額等關鍵資料',
            'en': 'Accurately extract date, account, amount and other key data'
        },
        'features.bank_export_title': {
            'zh': '多格式匯出',
            'en': 'Multi-format Export'
        },
        'features.bank_export_desc': {
            'zh': '支援匯出到 Excel、CSV、QuickBooks、Xero 等',
            'en': 'Support export to Excel, CSV, QuickBooks, Xero and more'
        },
        
        // 為什麼選擇 VaultCaddy
        'why.badge': {
            'zh': '為什麼選擇 VaultCaddy',
            'en': 'WHY CHOOSE VAULTCADDY'
        },
        'why.title': {
            'zh': '專為香港會計師打造',
            'en': 'Designed for Hong Kong Accountants'
        },
        'why.subtitle': {
            'zh': '提升效率，降低成本，讓您專注於更有價值的工作',
            'en': 'Boost efficiency, reduce costs, and focus on more valuable work'
        },
        'why.speed_title': {
            'zh': '極速處理',
            'en': 'Lightning Fast'
        },
        'why.speed_desc1': {
            'zh': '平均 10 秒完成一份文檔',
            'en': 'Average 10 seconds per document'
        },
        'why.speed_desc2': {
            'zh': '批量處理更快更省時',
            'en': 'Batch processing saves even more time'
        },
        'why.speed_desc3': {
            'zh': '節省 90% 人工輸入時間',
            'en': 'Save 90% manual input time'
        },
        'why.accuracy_title': {
            'zh': '超高準確率',
            'en': 'Ultra High Accuracy'
        },
        'why.accuracy_desc1': {
            'zh': 'AI 辨識準確率達 98%',
            'en': '98% AI recognition accuracy'
        },
        'why.accuracy_desc2': {
            'zh': '自動驗證和校正錯誤',
            'en': 'Auto-verify and correct errors'
        },
        'why.accuracy_desc3': {
            'zh': '大幅降低人為失誤風險',
            'en': 'Greatly reduce human error risks'
        },
        'why.price_title': {
            'zh': '性價比最高',
            'en': 'Best Value'
        },
        'why.price_desc1': {
            'zh': '每頁只需 HKD 0.5',
            'en': 'Only HKD 0.5 per page'
        },
        'why.price_desc2': {
            'zh': '無隱藏收費',
            'en': 'No hidden fees'
        },
        'why.price_desc3': {
            'zh': '用多少付多少最靈活',
            'en': 'Pay as you go - most flexible'
        },
        
        // 上傳區塊
        'upload.title': {
            'zh': '選擇文檔類型並上傳文件',
            'en': 'Select Document Type and Upload Files'
        },
        'upload.drag': {
            'zh': '拖放PDF文件到這裡',
            'en': 'Drag and drop PDF files here'
        },
        'upload.or': {
            'zh': '或',
            'en': 'or'
        },
        'upload.browse': {
            'zh': '瀏覽',
            'en': 'Browse'
        },
        
        // 為什麼選擇我們
        'why.title': {
            'zh': '為什麼選擇 VaultCaddy？',
            'en': 'Why Choose VaultCaddy?'
        },
        'why.speed_title': {
            'zh': '⚡ 10 秒極速處理',
            'en': '⚡ 10-Second Processing'
        },
        'why.speed_desc': {
            'zh': '無需等待，立即完成銀行對帳單轉換',
            'en': 'Instant conversion, no waiting'
        },
        'why.price_title': {
            'zh': '💰 全港最低價',
            'en': '💰 Lowest Price in HK'
        },
        'why.price_desc': {
            'zh': 'HKD 0.5/頁，免費試用無需預約',
            'en': 'HKD 0.5/page, free trial without appointment'
        },
        'why.local_title': {
            'zh': '🎯 專為香港設計',
            'en': '🎯 Designed for Hong Kong'
        },
        'why.local_desc': {
            'zh': '支援匯豐、恆生、中銀等本地銀行格式',
            'en': 'Supports HSBC, Hang Seng, BOC and other local banks'
        },
        'why.secure_title': {
            'zh': '🔒 安全可靠',
            'en': '🔒 Secure & Reliable'
        },
        'why.secure_desc': {
            'zh': '銀行級加密，365天數據保留',
            'en': 'Bank-level encryption, 365-day data retention'
        },
        
        // 用戶下拉菜單
        'dropdown.credits': {
            'zh': 'Credits',
            'en': 'Credits'
        },
        'dropdown.account': {
            'zh': '帳戶',
            'en': 'Account'
        },
        'dropdown.billing': {
            'zh': '計費',
            'en': 'Billing'
        },
        'dropdown.logout': {
            'zh': '登出',
            'en': 'Logout'
        },

        // 定價頁面
        'pricing.badge': {
            'zh': '簡單透明的定價',
            'en': 'Simple, Transparent Pricing'
        },
        'pricing.title': {
            'zh': '輕鬆處理銀行對帳單',
            'en': 'Convert Bank Statements with Confidence'
        },
        'pricing.subtitle': {
            'zh': '與數千家企業一起，節省財務數據錄入的時間。無隱藏費用，隨時取消。',
            'en': 'Join thousands of businesses saving hours on financial data entry. No hidden fees, cancel anytime.'
        },
        'pricing.monthly': {
            'zh': '月費',
            'en': 'Monthly'
        },
        'pricing.yearly': {
            'zh': '年費',
            'en': 'Yearly'
        },
        'pricing.save': {
            'zh': '節省 20%',
            'en': 'Save 20%'
        },
        'pricing.suitable_for': {
            'zh': '適合會計師、企業和個人用戶',
            'en': 'Perfect for Accountants, Businesses, and Individuals'
        },
        'pricing.includes': {
            'zh': '包含',
            'en': 'Includes'
        },
        'pricing.cta': {
            'zh': '立即開始',
            'en': 'Get Started'
        },

        // 功能列表
        'feature.monthly_credits': {
            'zh': '每月 100 Credits',
            'en': '100 Credits/month'
        },
        'feature.yearly_credits': {
            'zh': '每年 1,200 Credits',
            'en': '1,200 Credits/year'
        },
        'feature.overage': {
            'zh': '超出後每頁 HKD $0.5',
            'en': 'HKD $0.5 per additional page'
        },
        'feature.batch_processing': {
            'zh': '批次處理無限制文件',
            'en': 'Unlimited Batch Processing'
        },
        'feature.one_click_convert': {
            'zh': '一鍵轉換所有文件',
            'en': 'One-Click File Conversion'
        },
        'feature.export': {
            'zh': 'Excel/CSV 匯出',
            'en': 'Excel/CSV Export'
        },
        'feature.quickbooks': {
            'zh': 'QuickBooks 整合',
            'en': 'QuickBooks Integration'
        },
        'feature.ai_processing': {
            'zh': '複合式 AI 處理',
            'en': 'Hybrid AI Processing'
        },
        'feature.languages': {
            'zh': '8 種語言支援',
            'en': '8 Languages Support'
        },
        'feature.email_support': {
            'zh': '電子郵件支援',
            'en': 'Email Support'
        },
        'feature.secure_upload': {
            'zh': '安全文件上傳',
            'en': 'Secure File Upload'
        },
        'feature.data_retention': {
            'zh': '365 天數據保留',
            'en': '365-Day Data Retention'
        },
        'feature.image_retention': {
            'zh': '30 天圖片保留',
            'en': '30-Day Image Retention'
        },

        // 計費頁面
        'billing.title': {
            'zh': '計費與積分',
            'en': 'Billing & Credits'
        },
        'billing.current_plan': {
            'zh': '當前方案',
            'en': 'Current Plan'
        },
        'billing.credits_remaining': {
            'zh': 'Credits 餘額',
            'en': 'Credits Remaining'
        },
        'billing.usage_history': {
            'zh': '使用記錄',
            'en': 'Usage History'
        },

        // 帳戶頁面
        'account.title': {
            'zh': '帳戶設定',
            'en': 'Account Settings'
        },
        'account.personal_info': {
            'zh': '個人資料',
            'en': 'Personal Information'
        },
        'account.email': {
            'zh': '電子郵件',
            'en': 'Email'
        },
        'account.display_name': {
            'zh': '顯示名稱',
            'en': 'Display Name'
        },
        'account.save': {
            'zh': '保存',
            'en': 'Save'
        },
        'account.cancel': {
            'zh': '取消',
            'en': 'Cancel'
        },

        // 儀表板
        'dashboard.title': {
            'zh': '儀表板',
            'en': 'Dashboard'
        },
        'dashboard.projects': {
            'zh': '項目',
            'en': 'Projects'
        },
        'dashboard.documents': {
            'zh': '文件',
            'en': 'Documents'
        },
        'dashboard.upload': {
            'zh': '上傳文件',
            'en': 'Upload Files'
        },
        'dashboard.export': {
            'zh': '匯出',
            'en': 'Export'
        },
        'dashboard.delete': {
            'zh': '刪除',
            'en': 'Delete'
        },

        // 通用
        'common.loading': {
            'zh': '載入中...',
            'en': 'Loading...'
        },
        'common.error': {
            'zh': '錯誤',
            'en': 'Error'
        },
        'common.success': {
            'zh': '成功',
            'en': 'Success'
        },
        'common.confirm': {
            'zh': '確認',
            'en': 'Confirm'
        },
        'common.back': {
            'zh': '返回',
            'en': 'Back'
        },

        // Email 驗證
        'email.verify_banner': {
            'zh': '🎁 立即驗證您的 email 即送 20 Credits 試用！',
            'en': '🎁 Verify your email now and get 20 free Credits!'
        },
        'email.verify_button': {
            'zh': '立即驗證',
            'en': 'Verify Now'
        },
        
        // 演示動畫
        'demo.invoice_title': {
            'zh': '🧾 智能發票處理',
            'en': '🧾 Smart Invoice Processing'
        },
        'demo.invoice_scanning': {
            'zh': '📄 發票掃描中...',
            'en': '📄 Scanning invoice...'
        },
        'demo.total': {
            'zh': '總計:',
            'en': 'Total:'
        },
        'demo.ai_analyzing': {
            'zh': '🤖 AI 分析中...',
            'en': '🤖 AI analyzing...'
        },
        'demo.auto_extract': {
            'zh': '✅ 自動擷取完成',
            'en': '✅ Auto-extraction complete'
        },
        'demo.upload_quickbooks': {
            'zh': '📊 已上傳至QuickBooks',
            'en': '📊 Uploaded to QuickBooks'
        },
        'demo.bank_title': {
            'zh': '🏦 銀行對賬單分析',
            'en': '🏦 Bank Statement Analysis'
        },
        'demo.bank_analyzing': {
            'zh': '🏛️ 對賬單分析中...',
            'en': '🏛️ Analyzing statement...'
        },
        'demo.analysis_complete': {
            'zh': '已分析完成',
            'en': 'Analysis complete'
        },
        'demo.auto_categorize': {
            'zh': '✅ 收支自動分類',
            'en': '✅ Auto-categorized'
        },
        'demo.save_time': {
            'zh': '📈 節省90%輸入時間',
            'en': '📈 Save 90% input time'
        },
        
        // 優勢展示
        'benefits.accurate': {
            'zh': '數據準確度大幅提升',
            'en': 'Greatly improved data accuracy'
        },
        'benefits.integrate': {
            'zh': '與主流會計軟件無縫對接，工作流程更順暢',
            'en': 'Seamless integration with mainstream accounting software'
        },
        'benefits.save_time': {
            'zh': '節省90%時間，專注業務發展',
            'en': 'Save 90% time, focus on business growth'
        },
        
        // 功能展示
        'features.invoice_title': {
            'zh': '功能一：智能發票收據處理',
            'en': 'Feature 1: Smart Invoice & Receipt Processing'
        },
        'features.ocr': {
            'zh': 'OCR技術',
            'en': 'OCR Technology'
        },
        'features.ocr_desc': {
            'zh': '準確擷取發票與收據資料',
            'en': 'Accurately extract invoice and receipt data'
        },
        'features.auto_classify': {
            'zh': '自動分類記錄',
            'en': 'Auto-classification'
        },
        'features.auto_classify_desc': {
            'zh': '智能歸類交易項目',
            'en': 'Smart categorization of transactions'
        },
        'features.realtime_sync': {
            'zh': '即時同步更新',
            'en': 'Real-time sync'
        },
        'features.realtime_sync_desc': {
            'zh': '數據實時同步至系統',
            'en': 'Data synced in real-time'
        },
        'features.efficient': {
            'zh': '大幅提升效率',
            'en': 'Greatly improved efficiency'
        },
        'features.efficient_desc': {
            'zh': '減少90%人手操作時間',
            'en': 'Reduce 90% manual operation time'
        },
        'features.bank_title': {
            'zh': '功能二：銀行月結單/對賬單智能分析',
            'en': 'Feature 2: Smart Bank Statement Analysis'
        },
        'features.extract_transactions': {
            'zh': '自動提取交易記錄',
            'en': 'Auto-extract transactions'
        },
        'features.extract_transactions_desc': {
            'zh': '精準識別收入支出明細',
            'en': 'Accurately identify income and expenses'
        },
        'features.analyze_income': {
            'zh': '分析收入來源',
            'en': 'Analyze income sources'
        },
        'features.analyze_income_desc': {
            'zh': '自動分類營業收入項目',
            'en': 'Auto-categorize revenue items'
        },
        'features.categorize_expenses': {
            'zh': '費用支出歸類',
            'en': 'Categorize expenses'
        },
        'features.categorize_expenses_desc': {
            'zh': '智能識別各項營運開支',
            'en': 'Smart identification of operating costs'
        },
        'features.export': {
            'zh': '轉賬記錄整理',
            'en': 'Export transaction records'
        },
        'features.export_desc': {
            'zh': '導出到Quickbook online，Xero online，MYOB等常用會計軟件',
            'en': 'Export to QuickBooks, Xero, MYOB and other accounting software'
        }
    };

    // ============================================
    // Language Manager 類
    // ============================================

    class LanguageManager {
        constructor() {
            this.currentLanguage = this.loadLanguage();
            this.translations = translations;
            console.log('✅ LanguageManager 初始化完成，當前語言:', this.currentLanguage);
        }

        /**
         * 從 localStorage 載入語言偏好
         */
        loadLanguage() {
            const saved = localStorage.getItem('vaultcaddy_language');
            return saved || 'zh'; // 默認中文
        }

        /**
         * 保存語言偏好到 localStorage
         */
        saveLanguage(language) {
            localStorage.setItem('vaultcaddy_language', language);
            console.log('💾 語言偏好已保存:', language);
        }

        /**
         * 設置語言並翻譯頁面
         */
        setLanguage(language) {
            if (language !== 'zh' && language !== 'en') {
                console.error('❌ 不支援的語言:', language);
                return;
            }

            console.log(`🌐 切換語言: ${this.currentLanguage} → ${language}`);
            this.currentLanguage = language;
            this.saveLanguage(language);
            this.translatePage();

            // 發送語言變更事件
            window.dispatchEvent(new CustomEvent('languageChanged', {
                detail: { language: language }
            }));
        }

        /**
         * 獲取翻譯
         */
        translate(key) {
            const translation = this.translations[key];
            if (!translation) {
                console.warn('⚠️ 翻譯 key 不存在:', key);
                return key;
            }
            return translation[this.currentLanguage] || translation['zh'] || key;
        }

        /**
         * 翻譯整個頁面
         */
        translatePage() {
            console.log('🔄 開始翻譯頁面...');
            console.log('📍 當前語言:', this.currentLanguage);
            
            // 查找所有帶有 data-i18n 屬性的元素
            const elements = document.querySelectorAll('[data-i18n]');
            console.log(`📝 找到 ${elements.length} 個需要翻譯的元素`);

            let successCount = 0;
            let failCount = 0;

            elements.forEach((element, index) => {
                const key = element.getAttribute('data-i18n');
                const translation = this.translate(key);
                const originalText = element.textContent;
                
                // 調試：顯示前 3 個翻譯
                if (index < 3) {
                    console.log(`🔍 [${index}] Key: ${key}`);
                    console.log(`   原文: ${originalText}`);
                    console.log(`   譯文: ${translation}`);
                }
                
                // 如果元素是 input，更新 placeholder
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    if (element.hasAttribute('placeholder')) {
                        element.placeholder = translation;
                    } else {
                        element.value = translation;
                    }
                    successCount++;
                } else {
                    // 否則更新 textContent
                    if (translation && translation !== key) {
                        element.textContent = translation;
                        successCount++;
                    } else {
                        failCount++;
                        if (index < 3) {
                            console.warn(`⚠️ 翻譯失敗: ${key}`);
                        }
                    }
                }
            });

            console.log(`✅ 頁面翻譯完成 - 成功: ${successCount}, 失敗: ${failCount}`);
        }

        /**
         * 獲取當前語言
         */
        getCurrentLanguage() {
            return this.currentLanguage;
        }

        /**
         * 檢查是否為英文
         */
        isEnglish() {
            return this.currentLanguage === 'en';
        }

        /**
         * 檢查是否為中文
         */
        isChinese() {
            return this.currentLanguage === 'zh';
        }
    }

    // ============================================
    // 全局暴露
    // ============================================

    window.LanguageManager = LanguageManager;
    window.languageManager = new LanguageManager();

    // 頁面載入完成後自動翻譯
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.languageManager.translatePage();
        });
    } else {
        window.languageManager.translatePage();
    }

    console.log('✅ LanguageManager 已全局暴露: window.languageManager');
})();

