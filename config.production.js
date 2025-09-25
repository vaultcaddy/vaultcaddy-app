/**
 * VaultCaddy 生產環境配置
 * 用於管理 API 金鑰和環境設定
 */

// 環境檢測
const isProduction = window.location.hostname === 'vaultcaddy.com' || 
                    window.location.hostname === 'www.vaultcaddy.com';
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.protocol === 'file:';

// VaultCaddy 配置對象
window.VAULTCADDY_CONFIG = {
    // 環境資訊
    environment: isProduction ? 'production' : (isDevelopment ? 'development' : 'staging'),
    isProduction: isProduction,
    isDevelopment: isDevelopment,
    
    // API 端點配置
    api: {
        baseUrl: isProduction 
            ? 'https://api.vaultcaddy.com/v1' 
            : 'http://localhost:3000/api/v1',
        timeout: 30000,
        retries: 3
    },
    
    // Google AI 服務配置
    ai: {
        // 這裡將被 quick-api-setup.sh 腳本替換
        googleApiKey: isProduction 
            ? 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug' 
            : 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug',
        model: 'gemini-pro',
        visionModel: 'gemini-pro-vision',
        maxFileSize: 10 * 1024 * 1024, // 10MB
        supportedFormats: ['pdf', 'jpg', 'jpeg', 'png'],
        timeout: 60000
    },
    
    // Google OAuth 配置
    auth: {
        // 這裡將被 quick-api-setup.sh 腳本替換
        googleClientId: isProduction 
            ? '672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com'
            : '672279750239-u41ov9g2no1l2vh5j9h1679phggq0gko.apps.googleusercontent.com',
        jwtSecret: 'vaultcaddy-jwt-secret-' + Date.now(),
        tokenExpiry: 24 * 60 * 60 * 1000, // 24 小時
        sessionTimeout: 30 * 60 * 1000 // 30 分鐘
    },
    
    // Stripe 支付配置
    payment: {
        stripePublicKey: isProduction 
            ? 'pk_live_your_production_key'
            : 'pk_test_your_dev_key',
        currency: 'USD',
        locale: 'auto'
    },
    
    // 功能開關
    features: {
        realTimeProcessing: isProduction,
        googleAuth: true,
        stripePayments: false, // 暫時關閉，等待 Stripe 設置
        analytics: isProduction,
        errorReporting: isProduction,
        mockMode: !isProduction,
        debugMode: isDevelopment
    },
    
    // Credits 系統配置
    credits: {
        freeAllowance: 10,
        processingCost: {
            'bank-statement': 2,
            'invoice': 1,
            'receipt': 1,
            'general-document': 2
        },
        maxDailyProcessing: 50
    },
    
    // UI 配置
    ui: {
        language: 'zh-TW',
        theme: 'auto',
        animations: true,
        notifications: true
    }
};

// 配置驗證
function validateConfig() {
    const config = window.VAULTCADDY_CONFIG;
    const errors = [];
    
    // 檢查必要的 API 金鑰
    if (config.isProduction) {
        if (!config.ai.googleApiKey || config.ai.googleApiKey === 'PLACEHOLDER_FOR_PRODUCTION') {
            errors.push('生產環境缺少 Google AI API Key');
        }
        
        if (!config.auth.googleClientId || config.auth.googleClientId === 'your-production-client-id') {
            errors.push('生產環境缺少 Google OAuth Client ID');
        }
    }
    
    return errors;
}

// 配置載入完成處理
document.addEventListener('DOMContentLoaded', () => {
    const config = window.VAULTCADDY_CONFIG;
    const errors = validateConfig();
    
    console.log(`🔧 VaultCaddy 配置已載入 (${config.environment})`);
    
    if (errors.length > 0) {
        console.warn('⚠️ 配置問題:', errors);
        if (config.isProduction) {
            console.error('🚨 生產環境配置不完整，某些功能可能無法正常工作');
        }
    }
    
    // 觸發配置載入事件
    window.dispatchEvent(new CustomEvent('vaultcaddyConfigLoaded', { 
        detail: { config: config, errors: errors } 
    }));
});

// 公開工具函數
window.getVaultCaddyConfig = (path) => {
    const parts = path.split('.');
    let value = window.VAULTCADDY_CONFIG;
    
    for (const part of parts) {
        if (value && typeof value === 'object' && part in value) {
            value = value[part];
        } else {
            return undefined;
        }
    }
    
    return value;
};

// 環境檢測函數
window.VaultCaddy = {
    isProduction: () => window.VAULTCADDY_CONFIG.isProduction,
    isDevelopment: () => window.VAULTCADDY_CONFIG.isDevelopment,
    isMockMode: () => window.VAULTCADDY_CONFIG.features.mockMode,
    getApiKey: () => window.VAULTCADDY_CONFIG.ai.googleApiKey,
    getClientId: () => window.VAULTCADDY_CONFIG.auth.googleClientId,
    getConfig: window.getVaultCaddyConfig
};

// 兼容性支持（為了向後兼容舊代碼）
window.appConfig = window.VAULTCADDY_CONFIG;