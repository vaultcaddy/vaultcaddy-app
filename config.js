/**
 * VaultCaddy 配置文件 - API Keys 和環境設置
 * 注意：生產環境中的 API Keys 應該通過安全的方式管理
 */

class VaultCaddyConfig {
    constructor() {
        this.isDevelopment = window.location.hostname === 'localhost' || 
                           window.location.hostname === '127.0.0.1' ||
                           window.location.protocol === 'file:';
        
        this.isProduction = window.location.hostname === 'vaultcaddy.com' || 
                          window.location.hostname === 'www.vaultcaddy.com';
        
        this.environment = this.isProduction ? 'production' : 'development';
        
        // API 配置
        this.apiConfig = {
            google: {
                // 生產環境的 API Key（應該來自安全的來源）
                apiKey: this.getGoogleApiKey(),
                projectId: 'vaultcaddy-production',
                endpoints: {
                    vision: 'https://vision.googleapis.com/v1',
                    documentai: 'https://documentai.googleapis.com/v1',
                    translation: 'https://translation.googleapis.com/language/translate/v2'
                }
            },
            documentAI: {
                // Google Document AI 配置 (更穩定，無地理限制)
                apiKey: this.getGoogleApiKey(),
                projectId: 'vaultcaddy-production',
                location: 'us', // 或 'eu'
                endpoint: 'https://documentai.googleapis.com/v1',
                processors: {
                    general: 'projects/vaultcaddy-production/locations/us/processors/general',
                    invoice: 'projects/vaultcaddy-production/locations/us/processors/invoice',
                    receipt: 'projects/vaultcaddy-production/locations/us/processors/receipt'
                }
            },
            googleAI: {
                // Google Gemini API 配置
                apiKey: this.getGoogleApiKey(),
                model: 'gemini-1.5-flash',
                endpoint: 'https://asia-southeast1-generativelanguage.googleapis.com/v1beta/models',
                fallbackEndpoints: [
                    'https://us-central1-generativelanguage.googleapis.com/v1beta/models',
                    'https://europe-west1-generativelanguage.googleapis.com/v1beta/models',
                    'https://generativelanguage.googleapis.com/v1beta/models'
                ],
                maxFileSize: 20 * 1024 * 1024, // 20MB
                supportedMimeTypes: [
                    'application/pdf',
                    'image/jpeg',
                    'image/png',
                    'image/webp',
                    'text/plain'
                ]
            },
            googleCloud: {
                // Google Cloud Storage 配置
                apiKey: this.getGoogleCloudApiKey(),
                projectId: 'vaultcaddy-production',
                bucketName: 'vaultcaddy-documents',
                endpoints: {
                    storage: 'https://storage.googleapis.com/storage/v1',
                    upload: 'https://storage.googleapis.com/upload/storage/v1'
                }
            },
            stripe: {
                publishableKey: this.isProduction ? 
                    'pk_live_your_live_key' : 
                    'pk_test_your_test_key'
            }
        };
        
        console.log(`🔧 VaultCaddy Config 初始化: ${this.environment} 環境`);
    }
    
    /**
     * 安全獲取 Google API Key
     */
    getGoogleApiKey() {
        if (this.isProduction) {
            // 生產環境：從安全的環境變量或API獲取
            // 這裡需要您設置實際的 Google AI API Key
            const productionKey = this.getSecureApiKey();
            if (productionKey) {
                return productionKey;
            }
            
            // 臨時警告：需要設置生產環境 API Key
            console.warn('⚠️ 生產環境缺少 Google AI API Key');
            return null;
        } else {
            // 開發環境：從 localStorage 或環境變量獲取
            const devKey = localStorage.getItem('google_ai_api_key') || 
                          localStorage.getItem('google_api_key');
            
            if (!devKey) {
                console.warn('⚠️ 開發環境缺少 Google AI API Key');
                console.info('💡 請在瀏覽器控制台中設置：localStorage.setItem("google_ai_api_key", "your-api-key")');
            }
            
            return devKey;
        }
    }
    
    /**
     * 從安全來源獲取 API Key（生產環境）
     */
    getSecureApiKey() {
        // 生產環境 API Key (vaultcaddy.com)
        if (this.isProduction) {
            return 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug';
        }
        
        // 方法 1：從 meta tag 獲取（由服務器端設置）
        const metaKey = document.querySelector('meta[name="google-ai-api-key"]');
        if (metaKey) {
            return metaKey.getAttribute('content');
        }
        
        // 方法 2：從 window 全局變量獲取（由服務器端注入）
        if (window.GOOGLE_AI_API_KEY) {
            return window.GOOGLE_AI_API_KEY;
        }
        
        // 方法 3：從環境變量獲取（Node.js 環境）
        if (typeof process !== 'undefined' && process.env) {
            return process.env.GOOGLE_AI_API_KEY;
        }
        
        return null;
    }
    
    /**
     * 獲取 Google Cloud API Key
     */
    getGoogleCloudApiKey() {
        if (this.isProduction) {
            // 生產環境使用相同的API Key（Google Cloud和AI共用）
            return this.getSecureApiKey();
        } else {
            // 開發環境從localStorage獲取
            const devKey = localStorage.getItem('google_cloud_api_key') || 
                          localStorage.getItem('google_api_key');
            
            if (!devKey) {
                console.warn('⚠️ 開發環境缺少 Google Cloud API Key');
                console.info('💡 請在瀏覽器控制台中設置：localStorage.setItem("google_cloud_api_key", "your-api-key")');
            }
            
            return devKey;
        }
    }
    
    /**
     * 驗證 API Key 是否有效
     */
    async validateApiKey(apiKey) {
        if (!apiKey) return false;
        
        try {
            // 簡單的 API Key 格式驗證
            if (!apiKey.startsWith('AIza') || apiKey.length < 20) {
                return false;
            }
            
            // 可選：實際調用 API 驗證
            // const response = await fetch(`${this.apiConfig.google.endpoints.vision}/models?key=${apiKey}`);
            // return response.ok;
            
            return true;
        } catch (error) {
            console.error('API Key 驗證失敗:', error);
            return false;
        }
    }
    
    /**
     * 初始化 API Keys
     */
    async initializeApiKeys() {
        const googleApiKey = this.apiConfig.google.apiKey;
        
        if (googleApiKey) {
            const isValid = await this.validateApiKey(googleApiKey);
            if (isValid) {
                console.log('✅ Google AI API Key 已驗證');
                return true;
            } else {
                console.error('❌ Google AI API Key 無效');
                return false;
            }
        } else {
            console.warn('⚠️ 未找到 Google AI API Key');
            this.showApiKeySetupInstructions();
            return false;
        }
    }
    
    /**
     * 顯示 API Key 設置說明（已禁用弹窗）
     */
    showApiKeySetupInstructions() {
        if (this.isDevelopment) {
            console.group('🔑 Google AI API Key 設置說明');
            console.log('1. 前往 Google Cloud Console: https://console.cloud.google.com/');
            console.log('2. 啟用 AI Platform API 和 Vision API');
            console.log('3. 創建 API Key');
            console.log('4. 在控制台執行：localStorage.setItem("google_ai_api_key", "您的API Key")');
            console.log('5. 重新載入頁面');
            console.groupEnd();
        }
    }
    
    /**
     * 獲取當前配置
     */
    getConfig() {
        return {
            environment: this.environment,
            isProduction: this.isProduction,
            isDevelopment: this.isDevelopment,
            apiConfig: this.apiConfig
        };
    }
}

// 全局配置實例
window.VaultCaddyConfig = new VaultCaddyConfig();

// 自動初始化
document.addEventListener('DOMContentLoaded', async () => {
    await window.VaultCaddyConfig.initializeApiKeys();
});
