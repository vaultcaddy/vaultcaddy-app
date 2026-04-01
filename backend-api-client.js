/**
 * Backend API Client - 调用Python后端的银行对账单提取API
 * 
 * 使用方法：
 * 1. 启动Python后端：python backend/bank_statement_extractor.py
 * 2. 在前端调用：const result = await BackendAPIClient.extract(file);
 * 
 * @version 1.0.0
 * @date 2026-02-02
 */

class BackendAPIClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }
    
    /**
     * 提取银行对账单数据
     * 
     * @param {File} file - PDF文件
     * @param {string} bankKey - 银行配置键（可选，如 "zh_hangseng"）
     * @returns {Promise<Object>} 提取的数据
     */
    async extract(file, bankKey = null) {
        const formData = new FormData();
        formData.append('file', file);
        
        if (bankKey) {
            formData.append('bank_key', bankKey);
        }
        
        try {
            const response = await fetch(`${this.baseURL}/api/extract`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP ${response.status}`);
            }
            
            const data = await response.json();
            console.log('✅ 后端提取成功:', data);
            
            return {
                success: true,
                extractedData: data,
                method: 'backend-paddleocr'
            };
        } catch (error) {
            console.error('❌ 后端提取失败:', error);
            throw error;
        }
    }
    
    /**
     * 获取支持的银行列表
     * 
     * @returns {Promise<Array>} 银行列表
     */
    async getSupportedBanks() {
        try {
            const response = await fetch(`${this.baseURL}/api/banks`);
            const data = await response.json();
            return data.banks;
        } catch (error) {
            console.error('❌ 获取银行列表失败:', error);
            return [];
        }
    }
    
    /**
     * 健康检查
     * 
     * @returns {Promise<Object>} 健康状态
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch (error) {
            console.error('❌ 健康检查失败:', error);
            return { status: 'unhealthy', error: error.message };
        }
    }
}

// 导出为全局变量（浏览器环境）
if (typeof window !== 'undefined') {
    window.BackendAPIClient = BackendAPIClient;
}

// 导出为模块（Node.js环境）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BackendAPIClient;
}

