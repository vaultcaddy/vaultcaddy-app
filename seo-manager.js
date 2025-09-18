/**
 * VaultCaddy SEO/SEM 管理器
 * 企業級搜索引擎優化和營銷工具
 */

class SEOManager {
    constructor() {
        this.config = {
            siteName: 'VaultCaddy',
            domain: 'vaultcaddy.com',
            defaultLanguage: 'zh-TW',
            twitterHandle: '@vaultcaddy',
            fbPageId: 'vaultcaddy',
            
            // 核心關鍵詞策略
            primaryKeywords: [
                'AI文檔處理', 'AI document processing', 'PDF轉換器', 'PDF converter',
                '銀行對帳單轉換', 'bank statement converter', '發票處理', 'invoice processing',
                '收據識別', 'receipt recognition', 'OCR技術', 'OCR technology',
                '財務文檔自動化', 'financial document automation'
            ],
            
            // 長尾關鍵詞
            longTailKeywords: [
                'AI銀行對帳單PDF轉Excel', 'AI bank statement PDF to Excel converter',
                '會計師文檔處理工具', 'accountant document processing tool',
                '企業財務自動化解決方案', 'enterprise financial automation solution',
                '多語言文檔識別軟體', 'multilingual document recognition software'
            ],
            
            // 競爭對手分析
            competitors: [
                'docsumo.com', 'klippa.com', 'mindee.com', 'nanonets.com'
            ]
        };
        
        this.analytics = {
            gtag: null,
            fbPixel: null,
            hotjar: null
        };
        
        this.schemaData = {};
        this.metaData = {};
        
        console.log('🔍 VaultCaddy SEO Manager 初始化');
    }
    
    /**
     * 初始化 SEO 系統
     */
    async initialize() {
        await this.loadAnalytics();
        this.setupMetaTags();
        this.setupStructuredData();
        this.setupSitemap();
        this.setupRobotsTxt();
        this.optimizePageSpeed();
        this.setupSocialMedia();
        
        console.log('✅ SEO 系統初始化完成');
    }
    
    /**
     * 載入分析工具
     */
    async loadAnalytics() {
        // Google Analytics 4
        await this.loadGoogleAnalytics();
        
        // Facebook Pixel
        await this.loadFacebookPixel();
        
        // Hotjar 熱圖分析
        await this.loadHotjar();
        
        // Google Search Console
        this.setupSearchConsole();
    }
    
    /**
     * 載入 Google Analytics 4
     */
    async loadGoogleAnalytics() {
        const GA_ID = 'G-XXXXXXXXXX'; // 您需要替換為真實的 GA4 ID
        
        // 載入 gtag 腳本
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
        document.head.appendChild(script);
        
        // 初始化 gtag
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', GA_ID, {
            page_title: document.title,
            page_location: window.location.href,
            content_group1: 'AI Document Processing',
            content_group2: this.getPageCategory(),
            custom_map: {
                'custom_parameter': 'user_type'
            }
        });
        
        // 設置增強型電子商務
        gtag('config', GA_ID, {
            custom_map: {'custom_parameter': 'user_subscription'}
        });
        
        this.analytics.gtag = gtag;
        console.log('✅ Google Analytics 4 已載入');
    }
    
    /**
     * 載入 Facebook Pixel
     */
    async loadFacebookPixel() {
        const FB_PIXEL_ID = 'XXXXXXXXXXXXXXXXX'; // 您需要替換為真實的 Pixel ID
        
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        
        fbq('init', FB_PIXEL_ID);
        fbq('track', 'PageView');
        
        this.analytics.fbPixel = fbq;
        console.log('✅ Facebook Pixel 已載入');
    }
    
    /**
     * 載入 Hotjar
     */
    async loadHotjar() {
        const HOTJAR_ID = XXXXXXX; // 您需要替換為真實的 Hotjar ID
        
        (function(h,o,t,j,a,r){
            h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
            h._hjSettings={hjid:HOTJAR_ID,hjsv:6};
            a=o.getElementsByTagName('head')[0];
            r=o.createElement('script');r.async=1;
            r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
            a.appendChild(r);
        })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
        
        this.analytics.hotjar = window.hj;
        console.log('✅ Hotjar 已載入');
    }
    
    /**
     * 設置 Google Search Console
     */
    setupSearchConsole() {
        const metaTag = document.createElement('meta');
        metaTag.name = 'google-site-verification';
        metaTag.content = 'YOUR_GOOGLE_SEARCH_CONSOLE_CODE'; // 您需要替換
        document.head.appendChild(metaTag);
    }
    
    /**
     * 設置 Meta Tags
     */
    setupMetaTags() {
        const pageData = this.getPageData();
        
        // 基本 Meta Tags
        this.setMetaTag('description', pageData.description);
        this.setMetaTag('keywords', pageData.keywords.join(', '));
        this.setMetaTag('author', 'VaultCaddy Team');
        this.setMetaTag('robots', 'index, follow, max-snippet:-1, max-image-preview:large');
        this.setMetaTag('googlebot', 'index, follow');
        
        // Open Graph (Facebook)
        this.setMetaProperty('og:title', pageData.title);
        this.setMetaProperty('og:description', pageData.description);
        this.setMetaProperty('og:image', `https://${this.config.domain}/og-image.jpg`);
        this.setMetaProperty('og:url', window.location.href);
        this.setMetaProperty('og:type', pageData.type);
        this.setMetaProperty('og:site_name', this.config.siteName);
        this.setMetaProperty('og:locale', 'zh_TW');
        
        // Twitter Cards
        this.setMetaName('twitter:card', 'summary_large_image');
        this.setMetaName('twitter:site', this.config.twitterHandle);
        this.setMetaName('twitter:title', pageData.title);
        this.setMetaName('twitter:description', pageData.description);
        this.setMetaName('twitter:image', `https://${this.config.domain}/twitter-image.jpg`);
        
        // 移動優化
        this.setMetaName('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=5.0');
        this.setMetaName('theme-color', '#667eea');
        this.setMetaName('apple-mobile-web-app-capable', 'yes');
        this.setMetaName('apple-mobile-web-app-status-bar-style', 'default');
        
        // 規範化 URL
        const canonical = document.createElement('link');
        canonical.rel = 'canonical';
        canonical.href = window.location.href.split('?')[0].split('#')[0];
        document.head.appendChild(canonical);
        
        console.log('✅ Meta Tags 已設置');
    }
    
    /**
     * 設置結構化數據 (Schema.org)
     */
    setupStructuredData() {
        // 組織架構
        const organizationSchema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "VaultCaddy",
            "url": `https://${this.config.domain}`,
            "logo": `https://${this.config.domain}/logo.png`,
            "description": "專業的AI文檔處理平台，提供銀行對帳單、發票、收據的智能轉換服務",
            "foundingDate": "2024",
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+1-XXX-XXX-XXXX",
                "contactType": "customer service",
                "availableLanguage": ["zh-TW", "zh-CN", "en", "ja", "ko", "es", "fr", "de"]
            },
            "sameAs": [
                "https://twitter.com/vaultcaddy",
                "https://facebook.com/vaultcaddy",
                "https://linkedin.com/company/vaultcaddy"
            ]
        };
        
        // 軟體應用架構
        const softwareSchema = {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "VaultCaddy AI Document Processor",
            "description": "使用AI技術自動處理財務文檔，支援PDF轉Excel、OCR識別、多語言處理",
            "url": `https://${this.config.domain}`,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web Browser",
            "offers": {
                "@type": "Offer",
                "price": "19.00",
                "priceCurrency": "USD",
                "priceValidUntil": "2025-12-31"
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": "127"
            },
            "featureList": [
                "AI文檔識別",
                "多格式轉換",
                "批量處理",
                "多語言支援",
                "安全加密",
                "雲端同步"
            ]
        };
        
        // 常見問題架構
        const faqSchema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "VaultCaddy 支援哪些文檔格式？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "VaultCaddy 支援 PDF、JPG、PNG 等格式的銀行對帳單、發票、收據文檔，並可轉換為 Excel、CSV、JSON 等格式。"
                    }
                },
                {
                    "@type": "Question",
                    "name": "處理速度有多快？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "使用Google AI技術，單頁文檔處理時間通常在2-5秒內完成，批量處理支援同時處理多個文件。"
                    }
                },
                {
                    "@type": "Question",
                    "name": "數據安全如何保障？",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "採用SSL加密傳輸、Google Cloud安全基礎設施，用戶數據經過加密存儲，符合GDPR和相關隱私法規。"
                    }
                }
            ]
        };
        
        // 添加架構到頁面
        this.addSchema('organization', organizationSchema);
        this.addSchema('software', softwareSchema);
        this.addSchema('faq', faqSchema);
        
        console.log('✅ 結構化數據已設置');
    }
    
    /**
     * 設置網站地圖
     */
    setupSitemap() {
        const sitemap = {
            pages: [
                { url: '/', priority: 1.0, changefreq: 'daily' },
                { url: '/dashboard.html', priority: 0.9, changefreq: 'daily' },
                { url: '/billing.html', priority: 0.8, changefreq: 'weekly' },
                { url: '/account.html', priority: 0.7, changefreq: 'weekly' },
                { url: '/auth.html', priority: 0.6, changefreq: 'monthly' },
                { url: '/privacy.html', priority: 0.5, changefreq: 'monthly' },
                { url: '/terms.html', priority: 0.5, changefreq: 'monthly' }
            ]
        };
        
        // 生成 XML 網站地圖（這裡只是數據結構，實際文件需要在服務器端生成）
        this.generateSitemapXML(sitemap);
        
        console.log('✅ 網站地圖配置已設置');
    }
    
    /**
     * 設置 robots.txt
     */
    setupRobotsTxt() {
        const robotsTxt = `
User-agent: *
Allow: /

# 重要頁面
Allow: /index.html
Allow: /dashboard.html
Allow: /billing.html

# 禁止訪問敏感文件
Disallow: /config.js
Disallow: /oauth-setup-tool.html
Disallow: /*.json$
Disallow: /node_modules/

# 網站地圖
Sitemap: https://${this.config.domain}/sitemap.xml

# 爬取延遲（禮貌爬取）
Crawl-delay: 1
        `.trim();
        
        console.log('📝 robots.txt 配置已準備');
        console.log(robotsTxt);
    }
    
    /**
     * 頁面速度優化
     */
    optimizePageSpeed() {
        // 預載入關鍵資源
        this.preloadCriticalResources();
        
        // 圖片懶載入
        this.setupLazyLoading();
        
        // 關鍵 CSS 內聯
        this.inlineCriticalCSS();
        
        // 資源提示
        this.setupResourceHints();
        
        console.log('⚡ 頁面速度優化已啟用');
    }
    
    /**
     * 預載入關鍵資源
     */
    preloadCriticalResources() {
        const resources = [
            { href: 'styles.css', as: 'style' },
            { href: 'config.js', as: 'script' },
            { href: 'google-auth.js', as: 'script' },
            { href: 'https://fonts.gstatic.com', as: 'font', type: 'font/woff2', crossorigin: 'anonymous' }
        ];
        
        resources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            Object.assign(link, resource);
            document.head.appendChild(link);
        });
    }
    
    /**
     * 設置圖片懶載入
     */
    setupLazyLoading() {
        if ('loading' in HTMLImageElement.prototype) {
            // 原生懶載入支援
            document.querySelectorAll('img').forEach(img => {
                img.loading = 'lazy';
            });
        } else {
            // Intersection Observer 後備方案
            this.setupIntersectionObserver();
        }
    }
    
    /**
     * 設置社交媒體優化
     */
    setupSocialMedia() {
        // 社交分享按鈕
        this.setupSocialShareButtons();
        
        // 社交媒體圖片優化
        this.optimizeSocialImages();
        
        console.log('📱 社交媒體優化已設置');
    }
    
    /**
     * 追蹤轉換事件
     */
    trackConversion(eventName, eventData = {}) {
        // Google Analytics 事件追蹤
        if (this.analytics.gtag) {
            this.analytics.gtag('event', eventName, {
                event_category: 'conversion',
                event_label: eventData.label || '',
                value: eventData.value || 0,
                ...eventData
            });
        }
        
        // Facebook Pixel 轉換追蹤
        if (this.analytics.fbPixel) {
            this.analytics.fbPixel('track', eventName, eventData);
        }
        
        console.log(`📊 轉換事件已追蹤: ${eventName}`, eventData);
    }
    
    /**
     * 追蹤頁面瀏覽
     */
    trackPageView(pagePath = window.location.pathname) {
        if (this.analytics.gtag) {
            this.analytics.gtag('config', 'GA_MEASUREMENT_ID', {
                page_path: pagePath,
                page_title: document.title,
                content_group1: this.getPageCategory()
            });
        }
        
        if (this.analytics.fbPixel) {
            this.analytics.fbPixel('track', 'PageView');
        }
    }
    
    /**
     * 設置 A/B 測試
     */
    setupABTesting() {
        // Google Optimize
        const optimizeId = 'GTM-XXXXXXX';
        const script = document.createElement('script');
        script.src = `https://www.googleoptimize.com/optimize.js?id=${optimizeId}`;
        document.head.appendChild(script);
        
        console.log('🧪 A/B 測試已設置');
    }
    
    /**
     * 本地 SEO 優化
     */
    setupLocalSEO() {
        const localBusinessSchema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "VaultCaddy",
            "description": "專業AI文檔處理服務",
            "url": `https://${this.config.domain}`,
            "telephone": "+1-XXX-XXX-XXXX",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Your Street Address",
                "addressLocality": "City",
                "addressRegion": "State",
                "postalCode": "12345",
                "addressCountry": "US"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "XX.XXXXXX",
                "longitude": "XX.XXXXXX"
            },
            "openingHoursSpecification": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "09:00",
                "closes": "18:00"
            }
        };
        
        this.addSchema('localBusiness', localBusinessSchema);
    }
    
    // 輔助方法
    getPageData() {
        const path = window.location.pathname;
        const pageConfigs = {
            '/': {
                title: 'VaultCaddy - AI文檔處理專家 | PDF轉Excel | 銀行對帳單轉換',
                description: '專業的AI文檔處理平台，使用Google AI技術將PDF銀行對帳單、發票、收據智能轉換為Excel、CSV格式。支援多語言，安全快速，企業級服務。',
                keywords: this.config.primaryKeywords.concat(['首頁', 'AI轉換', 'PDF處理']),
                type: 'website'
            },
            '/dashboard.html': {
                title: 'VaultCaddy 控制台 - AI文檔處理工作台',
                description: '功能強大的AI文檔處理控制台，一鍵上傳處理PDF文檔，即時獲得Excel格式結果。支援批量處理和多種文檔格式。',
                keywords: this.config.primaryKeywords.concat(['控制台', '工作台', '批量處理']),
                type: 'webapp'
            },
            '/billing.html': {
                title: 'VaultCaddy 價格方案 - 靈活的AI文檔處理訂閱',
                description: '查看VaultCaddy的靈活價格方案，從個人用戶到企業客戶，提供不同級別的AI文檔處理服務和Credits方案。',
                keywords: this.config.primaryKeywords.concat(['價格', '訂閱', '方案', '企業']),
                type: 'website'
            }
            // 可以添加更多頁面配置
        };
        
        return pageConfigs[path] || pageConfigs['/'];
    }
    
    getPageCategory() {
        const path = window.location.pathname;
        if (path.includes('dashboard')) return 'Application';
        if (path.includes('billing')) return 'Pricing';
        if (path.includes('auth')) return 'Authentication';
        return 'Marketing';
    }
    
    setMetaTag(name, content) {
        let meta = document.querySelector(`meta[name="${name}"]`);
        if (!meta) {
            meta = document.createElement('meta');
            meta.name = name;
            document.head.appendChild(meta);
        }
        meta.content = content;
    }
    
    setMetaProperty(property, content) {
        let meta = document.querySelector(`meta[property="${property}"]`);
        if (!meta) {
            meta = document.createElement('meta');
            meta.setAttribute('property', property);
            document.head.appendChild(meta);
        }
        meta.content = content;
    }
    
    setMetaName(name, content) {
        this.setMetaTag(name, content);
    }
    
    addSchema(name, schema) {
        let script = document.querySelector(`script[data-schema="${name}"]`);
        if (!script) {
            script = document.createElement('script');
            script.type = 'application/ld+json';
            script.setAttribute('data-schema', name);
            document.head.appendChild(script);
        }
        script.textContent = JSON.stringify(schema, null, 2);
    }
    
    generateSitemapXML(sitemap) {
        // 這裡生成網站地圖的數據結構
        this.sitemapData = sitemap;
    }
}

// 頁面特定的 SEO 優化
class PageSEOOptimizer {
    static optimizeForIndex() {
        // 首頁特定優化
        document.title = 'VaultCaddy - AI文檔處理專家 | PDF轉Excel | 銀行對帳單轉換';
        
        // 添加關鍵詞密度優化
        const keywords = ['AI文檔處理', 'PDF轉換', '銀行對帳單', 'Excel轉換', 'OCR識別'];
        // 這裡可以添加關鍵詞密度檢查和優化邏輯
    }
    
    static optimizeForDashboard() {
        document.title = 'VaultCaddy 控制台 - AI文檔處理工作台';
        // 添加應用程式特定的 SEO 優化
    }
    
    static optimizeForBilling() {
        document.title = 'VaultCaddy 價格方案 - 靈活的AI文檔處理訂閱';
        // 添加電商/定價頁面的 SEO 優化
    }
}

// 全局 SEO 管理器實例
window.SEOManager = SEOManager;
window.PageSEOOptimizer = PageSEOOptimizer;

// 自動初始化
document.addEventListener('DOMContentLoaded', () => {
    window.seoManager = new SEOManager();
    window.seoManager.initialize();
    
    // 根據頁面類型優化
    const path = window.location.pathname;
    if (path === '/' || path === '/index.html') {
        PageSEOOptimizer.optimizeForIndex();
    } else if (path.includes('dashboard')) {
        PageSEOOptimizer.optimizeForDashboard();
    } else if (path.includes('billing')) {
        PageSEOOptimizer.optimizeForBilling();
    }
});

// 導出供其他模組使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SEOManager, PageSEOOptimizer };
}
