/**
 * SmartDoc Parser - AI服務整合模塊
 * 整合Google Vision API + AWS Textract + Azure Form Recognizer
 */

class AIDocumentProcessor {
    constructor() {
        this.services = {
            googleVision: new GoogleVisionService(),
            awsTextract: new AWSTextractService(),
            azureFormRecognizer: new AzureFormRecognizerService()
        };
        
        this.processingQueue = [];
        this.isProcessing = false;
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
     * 處理文檔
     */
    async processDocument(file, documentType, options = {}) {
        try {
            const route = this.routeDocument(file, documentType);
            const startTime = Date.now();
            
            // 顯示處理狀態
            this.showProcessingStatus(file.name, documentType);
            
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
                this.showSuccessStatus(file.name, processingTime, outputFormats);
                
                return {
                    success: true,
                    data: processedData,
                    formats: outputFormats,
                    metadata: {
                        documentType,
                        processingTime,
                        service: route.primary,
                        confidence: result.confidence || 0.95
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
}

/**
 * Google Vision Service
 */
class GoogleVisionService {
    constructor() {
        this.apiKey = process.env.GOOGLE_VISION_API_KEY;
        this.endpoint = 'https://vision.googleapis.com/v1/images:annotate';
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
        
        const response = await fetch(`${this.endpoint}?key=${this.apiKey}`, {
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
