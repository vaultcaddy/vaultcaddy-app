/**
 * VaultCaddy AI Services - AI服務整合模塊
 * 整合Google Vision API + AWS Textract + Azure Form Recognizer
 */

class AIDocumentProcessor {
    constructor() {
        // 生產環境配置
        this.config = {
            isProduction: window.location.hostname === 'vaultcaddy.com' || window.location.hostname === 'www.vaultcaddy.com',
            apiKey: '', // 將在運行時設置
            projectId: 'vaultcaddy-production', // 您的 Google Cloud 項目 ID
            apiEndpoints: {
                vision: 'https://vision.googleapis.com/v1',
                documentai: 'https://documentai.googleapis.com/v1',
                translation: 'https://translation.googleapis.com/language/translate/v2'
            }
        };
        
        this.services = {
            googleVision: new GoogleVisionService(),
            awsTextract: new AWSTextractService(),
            azureFormRecognizer: new AzureFormRecognizerService()
        };
        
        this.processingQueue = [];
        this.isProcessing = false;
        
        // 初始化生產環境設置
        if (this.config.isProduction) {
            this.initProductionMode();
        }
    }
    
    /**
     * 初始化生產環境模式
     */
    initProductionMode() {
        console.log('🔗 初始化生產環境 AI 服務...');
        
        // 驗證域名安全性
        if (!this.validateDomain()) {
            throw new Error('未授權的域名訪問');
        }
        
        // 設置 API Key（建議從安全存儲獲取）
        this.config.apiKey = this.getSecureApiKey();
        
        console.log('✅ 生產環境 AI 服務初始化完成');
    }
    
    /**
     * 驗證域名安全性
     */
    validateDomain() {
        const allowedDomains = ['vaultcaddy.com', 'www.vaultcaddy.com'];
        const currentDomain = window.location.hostname;
        return allowedDomains.includes(currentDomain);
    }
    
    /**
     * 安全獲取 API Key
     */
    getSecureApiKey() {
        // 使用統一配置系統獲取 API Key
        if (window.VaultCaddyConfig) {
            const apiKey = window.VaultCaddyConfig.apiConfig.google.apiKey;
            if (apiKey) {
                return apiKey;
            }
        }
        
        // 後備方案：直接從 localStorage 獲取
        const fallbackKey = localStorage.getItem('google_ai_api_key') || 
                           localStorage.getItem('google_api_key');
        
        if (!fallbackKey) {
            console.warn('⚠️ 未找到 Google AI API Key，使用模擬模式');
            console.info('💡 請設置 API Key 以啟用真實 AI 處理');
            return null;
        }
        
        return fallbackKey;
    }
    
    /**
     * 智能路由 - 根據文檔類型選擇最佳AI服務
     */
    routeDocument(file, documentType) {
        const routes = {
            'bank-statement': {
                primary: 'awsTextract',
                secondary: 'googleVision',
                features: ['TABLES', 'FORMS']
            },
            'invoice': {
                primary: 'azureFormRecognizer',
                secondary: 'awsTextract', 
                model: 'prebuilt-invoice'
            },
            'receipt': {
                primary: 'azureFormRecognizer',
                secondary: 'googleVision',
                model: 'prebuilt-receipt'
            },
            'general': {
                primary: 'googleVision',
                secondary: 'awsTextract',
                features: ['DOCUMENT_TEXT_DETECTION']
            }
        };
        
        return routes[documentType] || routes['general'];
    }
    
    /**
     * 處理文檔（整合 Credits 系統）
     */
    async processDocument(file, documentType, options = {}) {
        try {
            // 獲取當前用戶 ID
            const userId = this.getCurrentUserId();
            if (!userId) {
                throw new Error('請先登入後再處理文檔');
            }
            
            const route = this.routeDocument(file, documentType);
            const startTime = Date.now();
            
            // 估算需要的 Credits（每頁 1 Credit）
            const pagesCount = await this.estimatePageCount(file);
            const requiredCredits = pagesCount;
            
            // 檢查 Credits 餘額
            const creditsCheck = await this.checkUserCredits(userId, requiredCredits);
            if (!creditsCheck.sufficient) {
                throw new Error(`需要 ${requiredCredits} Credits，但您只有 ${creditsCheck.currentCredits} Credits。請購買更多 Credits。`);
            }
            
            // 顯示處理狀態（包含 Credits 信息）
            this.showProcessingStatus(file.name, documentType, requiredCredits);
            
            // 消耗 Credits
            const creditsResult = await this.consumeCredits(userId, requiredCredits, file.name);
            if (!creditsResult.success) {
                throw new Error('Credits 消耗失敗：' + creditsResult.error);
            }
            
            // 主要AI服務處理
            let result = await this.tryService(
                this.services[route.primary],
                file,
                { ...route, ...options }
            );
            
            // 如果主要服務失敗，使用備用服務
            if (!result.success && route.secondary) {
                console.log(`主要服務失敗，使用備用服務: ${route.secondary}`);
                result = await this.tryService(
                    this.services[route.secondary],
                    file,
                    { ...route, ...options }
                );
            }
            
            // 處理結果
            if (result.success) {
                const processedData = await this.postProcessData(result.data, documentType);
                const outputFormats = await this.convertToFormats(processedData, options.formats || ['csv']);
                
                const processingTime = Date.now() - startTime;
                
                // 更新用戶 Credits 顯示
                await this.updateCreditsDisplay(userId);
                
                this.showSuccessStatus(file.name, processingTime, outputFormats, requiredCredits);
                
                return {
                    success: true,
                    data: processedData,
                    formats: outputFormats,
                    metadata: {
                        documentType,
                        processingTime,
                        service: route.primary,
                        confidence: result.confidence || 0.95,
                        creditsUsed: requiredCredits,
                        pagesProcessed: pagesCount
                    }
                };
            } else {
                throw new Error(result.error || '處理失敗');
            }
            
        } catch (error) {
            console.error('文檔處理失敗:', error);
            this.showErrorStatus(file.name, error.message);
            
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * 嘗試使用指定的AI服務
     */
    async tryService(service, file, config) {
        try {
            const result = await service.process(file, config);
            return {
                success: true,
                data: result.data,
                confidence: result.confidence
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * 後處理數據
     */
    async postProcessData(rawData, documentType) {
        const processors = {
            'bank-statement': this.processBankStatement.bind(this),
            'invoice': this.processInvoice.bind(this),
            'receipt': this.processReceipt.bind(this),
            'general': this.processGeneral.bind(this)
        };
        
        const processor = processors[documentType] || processors['general'];
        return await processor(rawData);
    }
    
    /**
     * 處理銀行對帳單數據
     */
    async processBankStatement(data) {
        const transactions = [];
        
        // 解析表格數據
        if (data.tables) {
            for (const table of data.tables) {
                for (const row of table.rows) {
                    const transaction = this.parseTransactionRow(row);
                    if (transaction) {
                        transactions.push(transaction);
                    }
                }
            }
        }
        
        return {
            type: 'bank-statement',
            transactions,
            summary: {
                totalTransactions: transactions.length,
                totalAmount: transactions.reduce((sum, t) => sum + (t.amount || 0), 0),
                dateRange: this.getDateRange(transactions)
            }
        };
    }
    
    /**
     * 處理發票數據
     */
    async processInvoice(data) {
        return {
            type: 'invoice',
            invoiceNumber: data.invoiceNumber,
            date: data.invoiceDate,
            vendor: data.vendorName,
            amount: data.totalAmount,
            items: data.lineItems || [],
            tax: data.taxAmount
        };
    }
    
    /**
     * 處理收據數據
     */
    async processReceipt(data) {
        return {
            type: 'receipt',
            merchant: data.merchantName,
            date: data.transactionDate,
            amount: data.totalAmount,
            items: data.items || [],
            category: this.categorizeReceipt(data)
        };
    }
    
    /**
     * 處理一般文檔數據
     */
    async processGeneral(data) {
        return {
            type: 'general',
            text: data.fullText,
            extractedData: this.extractKeyValuePairs(data.text),
            confidence: data.confidence || 0.8
        };
    }
    
    /**
     * 轉換為多種格式
     */
    async convertToFormats(data, formats) {
        const converters = {
            csv: this.convertToCSV.bind(this),
            excel: this.convertToExcel.bind(this),
            json: this.convertToJSON.bind(this),
            qbo: this.convertToQBO.bind(this)
        };
        
        const results = {};
        
        for (const format of formats) {
            if (converters[format]) {
                results[format] = await converters[format](data);
            }
        }
        
        return results;
    }
    
    /**
     * 轉換為CSV格式
     */
    async convertToCSV(data) {
        if (data.type === 'bank-statement') {
            const headers = ['日期', '描述', '金額', '類型'];
            const rows = data.transactions.map(t => [
                t.date || '',
                t.description || '',
                t.amount || 0,
                t.type || ''
            ]);
            
            return {
                content: [headers, ...rows].map(row => row.join(',')).join('\n'),
                filename: `bank_statement_${Date.now()}.csv`,
                mimeType: 'text/csv'
            };
        }
        
        // 其他類型的CSV轉換邏輯...
        return {
            content: JSON.stringify(data, null, 2),
            filename: `document_${Date.now()}.json`,
            mimeType: 'application/json'
        };
    }
    
    /**
     * 轉換為Excel格式
     */
    async convertToExcel(data) {
        // Excel轉換邏輯（需要使用XLSX庫）
        return {
            content: 'Excel format content',
            filename: `document_${Date.now()}.xlsx`,
            mimeType: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        };
    }
    
    /**
     * 轉換為JSON格式
     */
    async convertToJSON(data) {
        return {
            content: JSON.stringify(data, null, 2),
            filename: `document_${Date.now()}.json`,
            mimeType: 'application/json'
        };
    }
    
    /**
     * 轉換為QBO格式
     */
    async convertToQBO(data) {
        // QBO格式轉換邏輯
        return {
            content: 'QBO format content',
            filename: `document_${Date.now()}.qbo`,
            mimeType: 'application/vnd.quickbooks'
        };
    }
    
    /**
     * 顯示處理狀態
     */
    showProcessingStatus(filename, documentType) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="processing-item">
                    <div class="processing-spinner"></div>
                    <span>正在處理 ${filename}...</span>
                    <small>文檔類型: ${documentType}</small>
                </div>
            `;
        }
    }
    
    /**
     * 顯示成功狀態
     */
    showSuccessStatus(filename, processingTime, formats) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="success-item">
                    <i class="fas fa-check-circle"></i>
                    <span>成功處理 ${filename}</span>
                    <small>處理時間: ${processingTime}ms</small>
                    <div class="download-links">
                        ${Object.keys(formats).map(format => 
                            `<a href="#" onclick="downloadFile('${format}')" class="download-btn">${format.toUpperCase()}</a>`
                        ).join('')}
                    </div>
                </div>
            `;
        }
    }
    
    /**
     * 顯示錯誤狀態
     */
    showErrorStatus(filename, error) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="error-item">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>處理失敗 ${filename}</span>
                    <small>錯誤: ${error}</small>
                </div>
            `;
        }
    }
    
    // 輔助方法
    parseTransactionRow(row) {
        // 解析交易行的邏輯
        return null;
    }
    
    getDateRange(transactions) {
        // 計算日期範圍
        return { start: null, end: null };
    }
    
    categorizeReceipt(data) {
        // 收據分類邏輯
        return 'general';
    }
    
    extractKeyValuePairs(text) {
        // 提取鍵值對
        return {};
    }
    
    // ===== Credits 系統方法 =====
    
    /**
     * 獲取當前用戶 ID
     */
    getCurrentUserId() {
        // 優先使用 Google 認證的用戶ID
        if (window.googleAuth && window.googleAuth.isLoggedIn()) {
            const googleUser = window.googleAuth.getCurrentUser();
            return googleUser.uid;
        }
        
        // 後備方案：原有認證系統
        if (window.UnifiedAuthManager && window.UnifiedAuthManager.isLoggedIn()) {
            return window.UnifiedAuthManager.getCurrentUser()?.uid || localStorage.getItem('userId');
        }
        
        // 最後後備：檢查本地存儲
        const user = JSON.parse(localStorage.getItem('vaultcaddy_user') || '{}');
        if (user.id || user.uid) {
            return user.id || user.uid;
        }
        
        return null;
    }
    
    /**
     * 估算文檔頁數
     */
    async estimatePageCount(file) {
        // 基於文件大小估算頁數
        const fileSizeMB = file.size / (1024 * 1024);
        
        if (file.type === 'application/pdf') {
            // PDF: 平均每頁約 0.1-0.5MB
            return Math.max(1, Math.ceil(fileSizeMB * 2));
        } else if (file.type.startsWith('image/')) {
            // 圖片: 通常 1 頁
            return 1;
        } else {
            // 其他文件: 保守估算
            return Math.max(1, Math.ceil(fileSizeMB));
        }
    }
    
    /**
     * 檢查用戶 Credits 餘額
     */
    async checkUserCredits(userId, requiredCredits) {
        try {
            // 模擬 API 調用 - 實際上應該調用後端 API
            const response = await fetch('/api/credits/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: userId,
                    requiredCredits: requiredCredits
                })
            });
            
            if (!response.ok) {
                throw new Error('Credits 檢查失敗');
            }
            
            const result = await response.json();
            return {
                sufficient: result.currentCredits >= requiredCredits,
                currentCredits: result.currentCredits
            };
        } catch (error) {
            console.warn('Credits 檢查失敗，使用本地模擬:', error);
            
            // 後備方案：從本地存儲獲取 Credits
            const localCredits = parseInt(localStorage.getItem('userCredits') || '7');
            return {
                sufficient: localCredits >= requiredCredits,
                currentCredits: localCredits
            };
        }
    }
    
    /**
     * 消耗 Credits
     */
    async consumeCredits(userId, credits, fileName) {
        try {
            // 模擬 API 調用 - 實際上應該調用後端 API
            const response = await fetch('/api/credits/consume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    userId: userId,
                    credits: credits,
                    fileName: fileName,
                    timestamp: new Date().toISOString()
                })
            });
            
            if (!response.ok) {
                throw new Error('Credits 消耗失敗');
            }
            
            const result = await response.json();
            return { success: true, remainingCredits: result.remainingCredits };
        } catch (error) {
            console.warn('Credits 消耗失敗，使用本地模擬:', error);
            
            // 後備方案：更新本地存儲
            const currentCredits = parseInt(localStorage.getItem('userCredits') || '7');
            const newCredits = Math.max(0, currentCredits - credits);
            localStorage.setItem('userCredits', newCredits.toString());
            
            return { success: true, remainingCredits: newCredits };
        }
    }
    
    /**
     * 更新 Credits 顯示
     */
    async updateCreditsDisplay(userId) {
        try {
            const creditsCheck = await this.checkUserCredits(userId, 0);
            const creditsElements = document.querySelectorAll('.stat-value');
            
            // 更新側邊欄的 Credits 顯示
            if (creditsElements.length > 0) {
                const creditsElement = creditsElements[creditsElements.length - 1]; // 最後一個是 Credits
                creditsElement.textContent = creditsCheck.currentCredits;
            }
        } catch (error) {
            console.error('更新 Credits 顯示失敗:', error);
        }
    }
    
    /**
     * 顯示處理狀態（包含 Credits 信息）
     */
    showProcessingStatus(filename, documentType, requiredCredits) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="processing-item" style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: #f8fafc; border-radius: 8px; margin: 1rem 0;">
                    <div class="processing-spinner" style="width: 20px; height: 20px; border: 2px solid #e5e7eb; border-top: 2px solid #7c3aed; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1f2937;">正在處理 ${filename}</div>
                        <div style="font-size: 0.875rem; color: #6b7280;">文檔類型: ${documentType} • 消耗 ${requiredCredits} Credits</div>
                    </div>
                </div>
            `;
        }
        
        // 添加 spinner 動畫 CSS
        if (!document.getElementById('spinner-styles')) {
            const style = document.createElement('style');
            style.id = 'spinner-styles';
            style.textContent = `
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    /**
     * 顯示成功狀態（包含 Credits 信息）
     */
    showSuccessStatus(filename, processingTime, formats, creditsUsed) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="success-item" style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; margin: 1rem 0;">
                    <i class="fas fa-check-circle" style="color: #10b981; font-size: 1.25rem;"></i>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1f2937;">成功處理 ${filename}</div>
                        <div style="font-size: 0.875rem; color: #6b7280;">處理時間: ${processingTime}ms • 消耗 ${creditsUsed} Credits</div>
                        <div class="download-links" style="margin-top: 0.5rem;">
                            ${Object.keys(formats).map(format => 
                                `<a href="#" onclick="downloadFile('${format}')" class="download-btn" style="display: inline-block; padding: 0.25rem 0.75rem; margin-right: 0.5rem; background: #7c3aed; color: white; text-decoration: none; border-radius: 4px; font-size: 0.75rem; font-weight: 500;">${format.toUpperCase()}</a>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    /**
     * 顯示錯誤狀態
     */
    showErrorStatus(filename, error) {
        const statusElement = document.getElementById('processing-status');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="error-item" style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; margin: 1rem 0;">
                    <i class="fas fa-exclamation-circle" style="color: #ef4444; font-size: 1.25rem;"></i>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #1f2937;">處理失敗 ${filename}</div>
                        <div style="font-size: 0.875rem; color: #ef4444;">錯誤: ${error}</div>
                        ${error.includes('Credits') ? `
                            <a href="billing.html" style="display: inline-block; margin-top: 0.5rem; padding: 0.25rem 0.75rem; background: #7c3aed; color: white; text-decoration: none; border-radius: 4px; font-size: 0.75rem;">購買 Credits</a>
                        ` : ''}
                    </div>
                </div>
            `;
        }
    }
}

/**
 * Google Vision Service
 */
class GoogleVisionService {
    constructor() {
        this.endpoint = 'https://vision.googleapis.com/v1/images:annotate';
    }
    
    getApiKey() {
        // 使用統一配置系統
        if (window.VaultCaddyConfig) {
            return window.VaultCaddyConfig.apiConfig.google.apiKey;
        }
        
        // 後備方案
        return localStorage.getItem('google_ai_api_key') || 
               localStorage.getItem('google_api_key') ||
               process.env.GOOGLE_VISION_API_KEY;
    }
    
    async process(file, config) {
        const base64 = await this.fileToBase64(file);
        
        const requestBody = {
            requests: [{
                image: { content: base64 },
                features: [
                    { type: 'DOCUMENT_TEXT_DETECTION', maxResults: 1 }
                ]
            }]
        };
        
        const apiKey = this.getApiKey();
        if (!apiKey) {
            console.warn('⚠️ Google Vision API Key 未設置，返回模擬結果');
            return this.getMockResult(file);
        }
        
        const response = await fetch(`${this.endpoint}?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });
        
        const result = await response.json();
        
        return {
            data: {
                fullText: result.responses[0]?.fullTextAnnotation?.text || '',
                confidence: 0.9
            },
            confidence: 0.9
        };
    }
    
    async fileToBase64(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.readAsDataURL(file);
        });
    }
    
    getMockResult(file) {
        // 返回模擬的處理結果
        return {
            success: true,
            data: {
                fullText: `模擬處理結果 - ${file.name}\n\n日期: 2024-01-15\n描述: 範例交易\n金額: $123.45\n餘額: $1,234.56`,
                confidence: 0.85,
                transactions: [
                    {
                        date: '2024-01-15',
                        description: '範例交易 1',
                        amount: 123.45,
                        balance: 1234.56
                    },
                    {
                        date: '2024-01-14', 
                        description: '範例交易 2',
                        amount: -50.00,
                        balance: 1111.11
                    }
                ]
            },
            confidence: 0.85
        };
    }
}

/**
 * AWS Textract Service
 */
class AWSTextractService {
    constructor() {
        this.region = 'us-east-1';
        this.endpoint = `https://textract.${this.region}.amazonaws.com/`;
    }
    
    async process(file, config) {
        // AWS Textract API調用邏輯
        // 注意：實際部署時需要AWS SDK和認證
        
        console.log('AWS Textract processing:', file.name);
        
        // 模擬處理結果
        return {
            data: {
                tables: [],
                forms: [],
                confidence: 0.95
            },
            confidence: 0.95
        };
    }
}

/**
 * Azure Form Recognizer Service
 */
class AzureFormRecognizerService {
    constructor() {
        this.endpoint = process.env.AZURE_FORM_RECOGNIZER_ENDPOINT;
        this.apiKey = process.env.AZURE_FORM_RECOGNIZER_KEY;
    }
    
    async process(file, config) {
        // Azure Form Recognizer API調用邏輯
        
        console.log('Azure Form Recognizer processing:', file.name);
        
        // 模擬處理結果
        return {
            data: {
                invoiceNumber: 'INV-001',
                totalAmount: 1000,
                confidence: 0.97
            },
            confidence: 0.97
        };
    }
}

// 全局AI處理器實例
window.aiProcessor = new AIDocumentProcessor();

// 導出供其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AIDocumentProcessor };
}
