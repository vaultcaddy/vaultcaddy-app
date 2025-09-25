/**
 * VaultCaddy 生產環境配置
 */

// 環境檢測
const isProduction = window.location.hostname === 'vaultcaddy.com' || 
                    window.location.hostname === 'www.vaultcaddy.com';
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.protocol === 'file:';

// 基礎配置
window.VAULTCADDY_CONFIG = {
    // 環境設定
    environment: isProduction ? 'production' : (isDevelopment ? 'development' : 'staging'),
    
    // API 端點
    api: {
        baseUrl: isProduction 
            ? 'https://api.vaultcaddy.com/v1' 
            : 'http://localhost:3000/api/v1',
        timeout: 30000,
        retries: 3
    },
    
    // AI 服務配置
    ai: {
        googleApiKey: isProduction 
            ? 'PLACEHOLDER_FOR_PRODUCTION' 
            : 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug',
        model: 'gemini-pro-vision',
        maxFileSize: 10 * 1024 * 1024,
        supportedFormats: ['pdf', 'jpg', 'jpeg', 'png']
    },
    
    // 認證配置
    auth: {
        googleClientId: isProduction 
            ? 'PLACEHOLDER_FOR_PRODUCTION'
            : 'your-dev-client-id',
        jwtSecret: 'PLACEHOLDER_FOR_PRODUCTION',
        tokenExpiry: 24 * 60 * 60 * 1000,
        sessionTimeout: 30 * 60 * 1000
    },
    
    // 支付配置
    payment: {
        stripePublicKey: isProduction 
            ? 'PLACEHOLDER_FOR_PRODUCTION'
            : 'pk_test_your_dev_key',
        currency: 'USD',
        locale: 'auto'
    },
    
    // 功能開關
    features: {
        realTimeProcessing: isProduction,
        googleAuth: true,
        stripePayments: isProduction,
        analytics: isProduction,
        errorReporting: isProduction,
        mockMode: !isProduction
    },
    
    // Credits 系統
    credits: {
        freeAllowance: 10,
        processingCost: {
            'bank-statement': 2,
            'invoice': 1,
            'receipt': 1,
            'general': 2
        }
    }
};

// 配置載入完成事件
document.addEventListener('DOMContentLoaded', () => {
    console.log(`🔧 VaultCaddy 配置已載入 (${window.VAULTCADDY_CONFIG.environment})`);
    
    window.dispatchEvent(new CustomEvent('configLoaded', { 
        detail: { config: window.VAULTCADDY_CONFIG } 
    }));
});

// 公開工具函數
window.getConfig = (path) => {
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

window.isProduction = () => window.VAULTCADDY_CONFIG.environment === 'production';
window.isDevelopment = () => window.VAULTCADDY_CONFIG.environment === 'development';
window.isMockMode = () => window.VAULTCADDY_CONFIG.features.mockMode;
