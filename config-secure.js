/**
 * VaultCaddy 安全配置管理
 * 安全地載入和管理API密鑰
 */

class SecureConfig {
    constructor() {
        this.config = {};
        this.loadConfiguration();
    }

    /**
     * 安全載入配置
     */
    loadConfiguration() {
        // 嘗試從多個來源載入配置
        try {
            // 1. 環境變數（生產環境推薦）
            this.loadFromEnvironment();
            
            // 2. 如果是開發環境，嘗試載入 .env 文件
            if (this.isDevelopment()) {
                this.loadFromDotEnv();
            }
            
            // 3. 驗證必要的配置
            this.validateConfiguration();
            
        } catch (error) {
            console.error('配置載入失敗:', error.message);
            throw error;
        }
    }

    /**
     * 從環境變數載入
     */
    loadFromEnvironment() {
        this.config = {
            // Google Cloud
            googleCloud: {
                projectId: process.env.GOOGLE_CLOUD_PROJECT_ID,
                apiKey: process.env.GOOGLE_CLOUD_API_KEY,
                credentialsPath: process.env.GOOGLE_APPLICATION_CREDENTIALS,
                processors: {
                    bankStatement: process.env.BANK_STATEMENT_PROCESSOR_ID,
                    invoice: process.env.INVOICE_PROCESSOR_ID,
                    receipt: process.env.RECEIPT_PROCESSOR_ID,
                    general: process.env.GENERAL_PROCESSOR_ID
                }
            },
            
            // Azure Form Recognizer
            azure: {
                endpoint: process.env.AZURE_FORM_RECOGNIZER_ENDPOINT,
                apiKey: process.env.AZURE_FORM_RECOGNIZER_KEY
            },
            
            // AWS (可選)
            aws: {
                accessKeyId: process.env.AWS_ACCESS_KEY_ID,
                secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
                region: process.env.AWS_REGION || 'us-east-1'
            },
            
            // 應用設定
            app: {
                nodeEnv: process.env.NODE_ENV || 'development',
                port: process.env.PORT || 3000
            }
        };
    }

    /**
     * 從 .env 文件載入（僅開發環境）
     */
    loadFromDotEnv() {
        try {
            // 如果在瀏覽器環境，跳過
            if (typeof window !== 'undefined') {
                console.warn('瀏覽器環境：API密鑰應由後端服務提供');
                return;
            }

            // Node.js 環境中載入 dotenv
            const dotenv = require('dotenv');
            const result = dotenv.config();
            
            if (result.error) {
                console.warn('.env 文件未找到，使用環境變數');
            } else {
                console.log('✅ .env 文件載入成功');
                this.loadFromEnvironment(); // 重新載入環境變數
            }
        } catch (error) {
            console.warn('dotenv 未安裝，請安裝: npm install dotenv');
        }
    }

    /**
     * 驗證配置完整性
     */
    validateConfiguration() {
        const requiredFields = [
            'googleCloud.projectId',
            'googleCloud.apiKey'
        ];

        const missingFields = requiredFields.filter(field => {
            return !this.getNestedValue(this.config, field);
        });

        if (missingFields.length > 0) {
            throw new Error(`缺少必要的配置項目: ${missingFields.join(', ')}`);
        }

        // 檢查Google Cloud認證
        if (!this.config.googleCloud.credentialsPath && !this.config.googleCloud.apiKey) {
            throw new Error('需要設定 GOOGLE_APPLICATION_CREDENTIALS 或 GOOGLE_CLOUD_API_KEY');
        }

        console.log('✅ 配置驗證通過');
    }

    /**
     * 取得嵌套的配置值
     */
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => current && current[key], obj);
    }

    /**
     * 是否為開發環境
     */
    isDevelopment() {
        return this.config.app?.nodeEnv === 'development' || 
               process.env.NODE_ENV === 'development' ||
               (!process.env.NODE_ENV && typeof window === 'undefined');
    }

    /**
     * 取得Google Cloud配置
     */
    getGoogleCloudConfig() {
        return {
            projectId: this.config.googleCloud.projectId,
            keyFilename: this.config.googleCloud.credentialsPath,
            apiKey: this.config.googleCloud.apiKey,
            location: 'us', // 或 'eu'
            processors: this.config.googleCloud.processors
        };
    }

    /**
     * 取得Azure配置
     */
    getAzureConfig() {
        return {
            endpoint: this.config.azure.endpoint,
            apiKey: this.config.azure.apiKey
        };
    }

    /**
     * 取得AWS配置
     */
    getAWSConfig() {
        return {
            accessKeyId: this.config.aws.accessKeyId,
            secretAccessKey: this.config.aws.secretAccessKey,
            region: this.config.aws.region
        };
    }

    /**
     * 檢查服務是否可用
     */
    isServiceAvailable(service) {
        switch (service) {
            case 'googleCloud':
                return !!(this.config.googleCloud.projectId && 
                         (this.config.googleCloud.apiKey || this.config.googleCloud.credentialsPath));
            
            case 'azure':
                return !!(this.config.azure.endpoint && this.config.azure.apiKey);
            
            case 'aws':
                return !!(this.config.aws.accessKeyId && this.config.aws.secretAccessKey);
            
            default:
                return false;
        }
    }

    /**
     * 取得可用的服務列表
     */
    getAvailableServices() {
        const services = ['googleCloud', 'azure', 'aws'];
        return services.filter(service => this.isServiceAvailable(service));
    }

    /**
     * 遮蔽敏感信息用於日誌
     */
    getSafeConfigForLogging() {
        const safeConfig = JSON.parse(JSON.stringify(this.config));
        
        // 遮蔽API密鑰
        if (safeConfig.googleCloud?.apiKey) {
            safeConfig.googleCloud.apiKey = this.maskKey(safeConfig.googleCloud.apiKey);
        }
        if (safeConfig.azure?.apiKey) {
            safeConfig.azure.apiKey = this.maskKey(safeConfig.azure.apiKey);
        }
        if (safeConfig.aws?.secretAccessKey) {
            safeConfig.aws.secretAccessKey = this.maskKey(safeConfig.aws.secretAccessKey);
        }

        return safeConfig;
    }

    /**
     * 遮蔽密鑰
     */
    maskKey(key) {
        if (!key || key.length < 8) return '***';
        return key.substring(0, 4) + '***' + key.substring(key.length - 4);
    }
}

// 單例實例
let configInstance = null;

/**
 * 取得配置實例
 */
function getSecureConfig() {
    if (!configInstance) {
        configInstance = new SecureConfig();
    }
    return configInstance;
}

// 匯出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { SecureConfig, getSecureConfig };
} else {
    window.SecureConfig = SecureConfig;
    window.getSecureConfig = getSecureConfig;
}

