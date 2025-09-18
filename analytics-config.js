/**
 * VaultCaddy 分析配置
 * 統一管理所有分析和追蹤工具
 */

// Google Analytics 4 配置
const GA4_CONFIG = {
    // 您需要在 Google Analytics 中創建這個
    measurementId: 'G-XXXXXXXXXX', // 替換為您的 GA4 Measurement ID
    
    // 自定義事件配置
    events: {
        // 轉換事件
        document_upload: 'document_upload',
        document_processed: 'document_processed',
        credits_purchased: 'credits_purchased',
        subscription_started: 'subscription_started',
        
        // 用戶行為事件
        google_signin: 'google_signin',
        feature_demo: 'feature_demo',
        pricing_viewed: 'pricing_viewed',
        contact_form: 'contact_form',
        
        // 技術事件
        api_error: 'api_error',
        processing_time: 'processing_time',
        file_type_processed: 'file_type_processed'
    },
    
    // 自定義維度
    customDimensions: {
        user_subscription_type: 'custom_parameter_1',
        document_type: 'custom_parameter_2',
        processing_language: 'custom_parameter_3',
        feature_usage: 'custom_parameter_4'
    }
};

// Facebook Pixel 配置
const FACEBOOK_PIXEL_CONFIG = {
    pixelId: 'XXXXXXXXXXXXXXXXX', // 替換為您的 Facebook Pixel ID
    
    // 標準事件
    events: {
        ViewContent: 'ViewContent',
        InitiateCheckout: 'InitiateCheckout',
        Purchase: 'Purchase',
        Lead: 'Lead',
        CompleteRegistration: 'CompleteRegistration',
        AddToCart: 'AddToCart'
    }
};

// Hotjar 配置
const HOTJAR_CONFIG = {
    siteId: XXXXXXX, // 替換為您的 Hotjar Site ID
    version: 6
};

// Google Tag Manager 配置
const GTM_CONFIG = {
    containerId: 'GTM-XXXXXXX' // 替換為您的 GTM Container ID
};

// Microsoft Clarity 配置
const CLARITY_CONFIG = {
    projectId: 'XXXXXXXXXX' // 替換為您的 Clarity Project ID
};

/**
 * 統一分析管理器
 */
class AnalyticsManager {
    constructor() {
        this.isInitialized = false;
        this.enabledServices = {
            ga4: true,
            facebook: true,
            hotjar: true,
            gtm: false, // 可選
            clarity: false // 可選
        };
        
        this.userProperties = {};
        this.sessionData = {};
        
        console.log('📊 Analytics Manager 初始化');
    }
    
    /**
     * 初始化所有分析服務
     */
    async initialize() {
        if (this.isInitialized) return;
        
        try {
            // 載入 Google Analytics 4
            if (this.enabledServices.ga4) {
                await this.initializeGA4();
            }
            
            // 載入 Facebook Pixel
            if (this.enabledServices.facebook) {
                await this.initializeFacebookPixel();
            }
            
            // 載入 Hotjar
            if (this.enabledServices.hotjar) {
                await this.initializeHotjar();
            }
            
            // 載入 Google Tag Manager（可選）
            if (this.enabledServices.gtm) {
                await this.initializeGTM();
            }
            
            // 載入 Microsoft Clarity（可選）
            if (this.enabledServices.clarity) {
                await this.initializeClarity();
            }
            
            // 設置用戶屬性
            this.setupUserProperties();
            
            // 開始會話追蹤
            this.startSession();
            
            this.isInitialized = true;
            console.log('✅ 所有分析服務初始化完成');
            
        } catch (error) {
            console.error('❌ 分析服務初始化失敗:', error);
        }
    }
    
    /**
     * 初始化 Google Analytics 4
     */
    async initializeGA4() {
        // 載入 gtag 腳本
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${GA4_CONFIG.measurementId}`;
        document.head.appendChild(script);
        
        // 等待腳本載入
        await new Promise(resolve => {
            script.onload = resolve;
        });
        
        // 初始化 gtag
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        window.gtag = gtag;
        
        gtag('js', new Date());
        gtag('config', GA4_CONFIG.measurementId, {
            // 增強型測量
            enhanced_measurements: {
                scrolls: true,
                outbound_clicks: true,
                site_search: true,
                video_engagement: true,
                file_downloads: true
            },
            
            // 自定義配置
            page_title: document.title,
            page_location: window.location.href,
            content_group1: this.getContentGroup(),
            
            // 用戶 ID（如果已登入）
            user_id: this.getUserId(),
            
            // 自定義參數
            custom_map: GA4_CONFIG.customDimensions
        });
        
        console.log('✅ Google Analytics 4 已初始化');
    }
    
    /**
     * 初始化 Facebook Pixel
     */
    async initializeFacebookPixel() {
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        
        fbq('init', FACEBOOK_PIXEL_CONFIG.pixelId);
        fbq('track', 'PageView');
        
        // 設置自動追蹤
        fbq('track', 'ViewContent', {
            content_type: 'website',
            content_ids: [window.location.pathname]
        });
        
        window.fbq = fbq;
        console.log('✅ Facebook Pixel 已初始化');
    }
    
    /**
     * 初始化 Hotjar
     */
    async initializeHotjar() {
        (function(h,o,t,j,a,r){
            h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
            h._hjSettings={hjid:HOTJAR_CONFIG.siteId,hjsv:HOTJAR_CONFIG.version};
            a=o.getElementsByTagName('head')[0];
            r=o.createElement('script');r.async=1;
            r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
            a.appendChild(r);
        })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
        
        console.log('✅ Hotjar 已初始化');
    }
    
    /**
     * 追蹤事件
     */
    trackEvent(eventName, parameters = {}) {
        try {
            // Google Analytics 4
            if (window.gtag && this.enabledServices.ga4) {
                gtag('event', eventName, {
                    event_category: parameters.category || 'engagement',
                    event_label: parameters.label || '',
                    value: parameters.value || 0,
                    ...parameters
                });
            }
            
            // Facebook Pixel
            if (window.fbq && this.enabledServices.facebook) {
                const fbEventName = this.mapToFacebookEvent(eventName);
                if (fbEventName) {
                    fbq('track', fbEventName, parameters);
                }
            }
            
            console.log(`📊 事件已追蹤: ${eventName}`, parameters);
            
        } catch (error) {
            console.error('事件追蹤失敗:', error);
        }
    }
    
    /**
     * 追蹤頁面瀏覽
     */
    trackPageView(pagePath = window.location.pathname, pageTitle = document.title) {
        try {
            // Google Analytics 4
            if (window.gtag && this.enabledServices.ga4) {
                gtag('config', GA4_CONFIG.measurementId, {
                    page_path: pagePath,
                    page_title: pageTitle,
                    content_group1: this.getContentGroup()
                });
            }
            
            // Facebook Pixel
            if (window.fbq && this.enabledServices.facebook) {
                fbq('track', 'PageView');
            }
            
            console.log(`📄 頁面瀏覽已追蹤: ${pagePath}`);
            
        } catch (error) {
            console.error('頁面追蹤失敗:', error);
        }
    }
    
    /**
     * 追蹤轉換事件
     */
    trackConversion(conversionType, value = 0, currency = 'USD', parameters = {}) {
        const eventData = {
            currency: currency,
            value: value,
            transaction_id: this.generateTransactionId(),
            ...parameters
        };
        
        switch (conversionType) {
            case 'subscription':
                this.trackEvent('purchase', {
                    ...eventData,
                    item_category: 'subscription',
                    item_name: parameters.plan_name || 'Unknown Plan'
                });
                break;
                
            case 'credits_purchase':
                this.trackEvent('purchase', {
                    ...eventData,
                    item_category: 'credits',
                    item_name: `${parameters.credits_amount} Credits`
                });
                break;
                
            case 'document_processed':
                this.trackEvent('document_processed', {
                    ...eventData,
                    document_type: parameters.document_type || 'unknown',
                    processing_time: parameters.processing_time || 0
                });
                break;
                
            case 'signup':
                this.trackEvent('sign_up', {
                    method: parameters.method || 'email'
                });
                break;
                
            case 'login':
                this.trackEvent('login', {
                    method: parameters.method || 'email'
                });
                break;
        }
    }
    
    /**
     * 設置用戶屬性
     */
    setUserProperties(properties) {
        this.userProperties = { ...this.userProperties, ...properties };
        
        // Google Analytics 4
        if (window.gtag && this.enabledServices.ga4) {
            gtag('config', GA4_CONFIG.measurementId, {
                custom_map: properties
            });
        }
        
        // Facebook Pixel
        if (window.fbq && this.enabledServices.facebook) {
            fbq('track', 'CustomizeProduct', properties);
        }
    }
    
    /**
     * 設置用戶 ID
     */
    setUserId(userId) {
        if (window.gtag && this.enabledServices.ga4) {
            gtag('config', GA4_CONFIG.measurementId, {
                user_id: userId
            });
        }
        
        // 存儲用戶 ID
        this.userProperties.user_id = userId;
    }
    
    /**
     * 開始會話追蹤
     */
    startSession() {
        this.sessionData = {
            start_time: Date.now(),
            page_views: 0,
            events: 0,
            user_agent: navigator.userAgent,
            screen_resolution: `${screen.width}x${screen.height}`,
            language: navigator.language
        };
        
        // 追蹤會話開始
        this.trackEvent('session_start', {
            session_id: this.generateSessionId()
        });
    }
    
    /**
     * 追蹤 A/B 測試
     */
    trackExperiment(experimentId, variantId) {
        this.trackEvent('experiment_impression', {
            experiment_id: experimentId,
            variant_id: variantId
        });
    }
    
    /**
     * 追蹤性能指標
     */
    trackPerformance() {
        if ('performance' in window) {
            const navigation = performance.getEntriesByType('navigation')[0];
            const paint = performance.getEntriesByType('paint');
            
            const performanceData = {
                page_load_time: Math.round(navigation.loadEventEnd - navigation.fetchStart),
                dom_content_loaded: Math.round(navigation.domContentLoadedEventEnd - navigation.fetchStart),
                first_contentful_paint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
                largest_contentful_paint: 0 // 需要 Web Vitals 庫
            };
            
            this.trackEvent('page_performance', performanceData);
        }
    }
    
    // 輔助方法
    getContentGroup() {
        const path = window.location.pathname;
        if (path.includes('dashboard')) return 'Application';
        if (path.includes('billing')) return 'Pricing';
        if (path.includes('auth')) return 'Authentication';
        return 'Marketing';
    }
    
    getUserId() {
        // 從 Google Auth 或其他認證系統獲取用戶 ID
        if (window.googleAuth && window.googleAuth.isLoggedIn()) {
            return window.googleAuth.getCurrentUser()?.uid;
        }
        return null;
    }
    
    mapToFacebookEvent(eventName) {
        const mapping = {
            'document_upload': 'InitiateCheckout',
            'document_processed': 'Purchase',
            'credits_purchased': 'Purchase',
            'subscription_started': 'Subscribe',
            'google_signin': 'CompleteRegistration',
            'contact_form': 'Lead'
        };
        
        return mapping[eventName] || null;
    }
    
    generateTransactionId() {
        return 'txn_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    generateSessionId() {
        return 'ses_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
}

// 全局實例
window.AnalyticsManager = AnalyticsManager;

// 自動初始化
document.addEventListener('DOMContentLoaded', () => {
    window.analyticsManager = new AnalyticsManager();
    window.analyticsManager.initialize();
    
    // 追蹤頁面載入性能
    window.addEventListener('load', () => {
        setTimeout(() => {
            window.analyticsManager.trackPerformance();
        }, 1000);
    });
});

// 導出配置供其他模組使用
window.ANALYTICS_CONFIG = {
    GA4_CONFIG,
    FACEBOOK_PIXEL_CONFIG,
    HOTJAR_CONFIG,
    GTM_CONFIG,
    CLARITY_CONFIG
};
