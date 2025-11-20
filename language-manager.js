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
        'hero.title': {
            'zh': 'AI 驅動的財務文件處理',
            'en': 'AI-Powered Financial Document Processing'
        },
        'hero.subtitle': {
            'zh': '香港市場性價比最高的 AI 銀行對帳單處理工具',
            'en': 'Hong Kong\'s Most Cost-Effective AI Bank Statement Processing Tool'
        },
        'hero.slogan': {
            'zh': '只需 HKD 0.5/頁，讓 AI 秒速幫你處理銀行對帳單',
            'en': 'Process Bank Statements with AI at Just HKD 0.5/page'
        },
        'hero.cta': {
            'zh': '免費開始',
            'en': 'Get Started Free'
        },

        // 定價頁面
        'pricing.title': {
            'zh': '簡單透明的定價',
            'en': 'Simple, Transparent Pricing'
        },
        'pricing.subtitle': {
            'zh': '輕鬆處理銀行對帳單',
            'en': 'Convert Bank Statements with Confidence'
        },
        'pricing.description': {
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
            
            // 查找所有帶有 data-i18n 屬性的元素
            const elements = document.querySelectorAll('[data-i18n]');
            console.log(`📝 找到 ${elements.length} 個需要翻譯的元素`);

            elements.forEach(element => {
                const key = element.getAttribute('data-i18n');
                const translation = this.translate(key);
                
                // 如果元素是 input，更新 placeholder
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    if (element.hasAttribute('placeholder')) {
                        element.placeholder = translation;
                    } else {
                        element.value = translation;
                    }
                } else {
                    // 否則更新 textContent
                    element.textContent = translation;
                }
            });

            console.log('✅ 頁面翻譯完成');
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

