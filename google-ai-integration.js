/**
 * Google Cloud AI 整合模組
 * 使用 Google Gemini API 進行真實的文檔數據提取
 */

class GoogleAIProcessor {
    constructor() {
        this.apiKey = null;
        this.apiEndpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';
        this.maxFileSize = 20 * 1024 * 1024; // 20MB
        this.supportedMimeTypes = [
            'application/pdf',
            'image/jpeg',
            'image/png',
            'image/webp',
            'text/plain'
        ];
        
        this.init();
    }
    
    init() {
        // 從配置中獲取API密鑰
        this.apiKey = window.config?.googleAI?.apiKey;
        
        if (!this.apiKey || this.apiKey === 'demo-key') {
            console.warn('⚠️ Google AI API密鑰未設置，將使用模擬數據');
        } else {
            console.log('🤖 Google AI處理器已初始化');
        }
    }
    
    /**
     * 處理文件並提取數據
     */
    async processDocument(file, documentType) {
        console.log(`🚀 開始處理文檔: ${file.name} (${documentType})`);
        
        // 驗證文件
        if (!this.validateFile(file)) {
            throw new Error('文件格式不支援或文件過大');
        }
        
        // 如果沒有API密鑰，使用模擬數據
        if (!this.apiKey || this.apiKey === 'demo-key') {
            console.log('🎭 使用模擬數據處理');
            return await this.generateMockData(file, documentType);
        }
        
        try {
            // 將文件轉換為base64
            const base64Data = await this.fileToBase64(file);
            
            // 生成提示詞
            const prompt = this.generatePrompt(documentType);
            
            // 調用Google AI API
            const extractedData = await this.callGoogleAI(base64Data, file.type, prompt);
            
            // 處理和驗證返回的數據
            const processedData = this.processAIResponse(extractedData, documentType);
            
            console.log('✅ Google AI處理完成');
            return processedData;
            
        } catch (error) {
            console.error('❌ Google AI處理失敗:', error);
            
            // 如果API調用失敗，回退到模擬數據
            console.log('🔄 回退到模擬數據');
            return await this.generateMockData(file, documentType);
        }
    }
    
    /**
     * 驗證文件
     */
    validateFile(file) {
        // 檢查文件大小
        if (file.size > this.maxFileSize) {
            console.error(`文件過大: ${file.size} bytes > ${this.maxFileSize} bytes`);
            return false;
        }
        
        // 檢查MIME類型
        if (!this.supportedMimeTypes.includes(file.type)) {
            console.error(`不支援的文件類型: ${file.type}`);
            return false;
        }
        
        return true;
    }
    
    /**
     * 將文件轉換為base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            // 驗證文件
            if (!file) {
                reject(new Error('文件不存在'));
                return;
            }
            
            if (file.size === 0) {
                reject(new Error('文件為空'));
                return;
            }
            
            const reader = new FileReader();
            
            // 設置超時
            const timeout = setTimeout(() => {
                reject(new Error('文件讀取超時'));
            }, 30000);
            
            reader.onload = () => {
                clearTimeout(timeout);
                try {
                    if (!reader.result) {
                        reject(new Error('文件讀取結果為空'));
                        return;
                    }
                    
                    // 移除data:mime/type;base64,前綴
                    const result = reader.result.toString();
                    const commaIndex = result.indexOf(',');
                    
                    if (commaIndex === -1) {
                        reject(new Error('無效的base64格式'));
                        return;
                    }
                    
                    const base64 = result.substring(commaIndex + 1);
                    
                    if (!base64) {
                        reject(new Error('base64數據為空'));
                        return;
                    }
                    
                    resolve(base64);
                } catch (error) {
                    clearTimeout(timeout);
                    reject(new Error(`base64轉換失敗: ${error.message}`));
                }
            };
            
            reader.onerror = (error) => {
                clearTimeout(timeout);
                reject(new Error(`文件讀取失敗: ${error.message || '未知錯誤'}`));
            };
            
            try {
                reader.readAsDataURL(file);
            } catch (error) {
                clearTimeout(timeout);
                reject(new Error(`開始讀取文件失敗: ${error.message}`));
            }
        });
    }
    
    /**
     * 生成針對不同文檔類型的提示詞
     */
    generatePrompt(documentType) {
        const prompts = {
            'bank-statement': `
請分析這份銀行對帳單並提取以下信息，以JSON格式返回：

{
  "accountInfo": {
    "accountHolder": "帳戶持有人姓名",
    "accountNumber": "帳戶號碼",
    "bankCode": "銀行代碼",
    "branch": "分行名稱"
  },
  "statementPeriod": {
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD"
  },
  "financialPosition": {
    "deposits": 存款金額(數字),
    "personalLoans": 個人貸款金額(數字，負數),
    "creditCards": 信用卡欠款(數字，負數),
    "netPosition": 淨額(數字)
  },
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "交易描述",
      "amount": 交易金額(數字，正數為收入，負數為支出),
      "balance": 餘額(數字),
      "type": "交易類型(credit/debit/balance/deposit)"
    }
  ]
}

請確保所有金額都是數字格式，日期都是YYYY-MM-DD格式。如果某些信息無法提取，請設為null。
            `,
            
            'invoice': `
請分析這份發票並提取以下信息，以JSON格式返回：

{
  "invoiceNumber": "發票號碼",
  "issueDate": "YYYY-MM-DD",
  "dueDate": "YYYY-MM-DD",
  "vendor": "供應商名稱",
  "customer": "客戶名稱",
  "totalAmount": 總金額(數字),
  "taxAmount": 稅額(數字),
  "currency": "貨幣代碼",
  "lineItems": [
    {
      "description": "項目描述",
      "quantity": 數量(數字),
      "unitPrice": 單價(數字),
      "totalPrice": 總價(數字)
    }
  ]
}

請確保所有金額都是數字格式，日期都是YYYY-MM-DD格式。
            `,
            
            'receipt': `
請分析這份收據並提取以下信息，以JSON格式返回：

{
  "receiptNumber": "收據號碼",
  "date": "YYYY-MM-DD",
  "merchant": "商家名稱",
  "totalAmount": 總金額(數字),
  "taxAmount": 稅額(數字),
  "paymentMethod": "付款方式",
  "currency": "貨幣代碼",
  "items": [
    {
      "name": "商品名稱",
      "quantity": 數量(數字),
      "price": 價格(數字)
    }
  ]
}

請確保所有金額都是數字格式，日期都是YYYY-MM-DD格式。
            `,
            
            'general': `
請分析這份文檔並提取關鍵信息，以JSON格式返回：

{
  "documentType": "文檔類型",
  "title": "文檔標題",
  "date": "YYYY-MM-DD",
  "content": "主要內容摘要",
  "keyInformation": ["關鍵信息1", "關鍵信息2", "關鍵信息3"],
  "entities": {
    "persons": ["人名"],
    "organizations": ["機構名"],
    "locations": ["地點"],
    "dates": ["重要日期"],
    "amounts": ["金額"]
  }
}

請提取文檔中的關鍵信息和實體。
            `
        };
        
        return prompts[documentType] || prompts['general'];
    }
    
    /**
     * 調用Google AI API
     */
    async callGoogleAI(base64Data, mimeType, prompt) {
        const requestBody = {
            contents: [{
                parts: [
                    {
                        text: prompt
                    },
                    {
                        inline_data: {
                            mime_type: mimeType,
                            data: base64Data
                        }
                    }
                ]
            }],
            generationConfig: {
                temperature: 0.1,
                topK: 32,
                topP: 1,
                maxOutputTokens: 4096,
            }
        };
        
        console.log('📡 調用Google AI API...');
        
        const response = await fetch(`${this.apiEndpoint}?key=${this.apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Google AI API錯誤: ${response.status} - ${errorData.error?.message || 'Unknown error'}`);
        }
        
        const data = await response.json();
        
        if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
            throw new Error('Google AI API返回無效響應');
        }
        
        const textContent = data.candidates[0].content.parts[0].text;
        console.log('📄 AI響應:', textContent.substring(0, 200) + '...');
        
        return textContent;
    }
    
    /**
     * 處理AI響應
     */
    processAIResponse(aiResponse, documentType) {
        try {
            // 嘗試從響應中提取JSON
            const jsonMatch = aiResponse.match(/\{[\s\S]*\}/);
            if (!jsonMatch) {
                throw new Error('AI響應中未找到有效的JSON');
            }
            
            const extractedData = JSON.parse(jsonMatch[0]);
            
            // 驗證和清理數據
            const cleanedData = this.validateAndCleanData(extractedData, documentType);
            
            return {
                documentType: documentType,
                extractedFields: cleanedData,
                aiProcessed: true,
                processedAt: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ 處理AI響應失敗:', error);
            throw new Error(`AI響應處理失敗: ${error.message}`);
        }
    }
    
    /**
     * 驗證和清理數據
     */
    validateAndCleanData(data, documentType) {
        // 根據文檔類型進行特定的驗證和清理
        switch (documentType) {
            case 'bank-statement':
                return this.cleanBankStatementData(data);
            case 'invoice':
                return this.cleanInvoiceData(data);
            case 'receipt':
                return this.cleanReceiptData(data);
            default:
                return data;
        }
    }
    
    /**
     * 清理銀行對帳單數據
     */
    cleanBankStatementData(data) {
        // 確保數字字段是數字類型
        if (data.financialPosition) {
            ['deposits', 'personalLoans', 'creditCards', 'netPosition'].forEach(field => {
                if (data.financialPosition[field] !== null) {
                    data.financialPosition[field] = parseFloat(data.financialPosition[field]) || 0;
                }
            });
        }
        
        // 清理交易數據
        if (data.transactions && Array.isArray(data.transactions)) {
            data.transactions = data.transactions.map(transaction => ({
                ...transaction,
                amount: parseFloat(transaction.amount) || 0,
                balance: parseFloat(transaction.balance) || 0,
                date: this.validateDate(transaction.date)
            }));
        }
        
        // 添加對帳信息
        data.reconciliation = {
            totalTransactions: data.transactions ? data.transactions.length : 0,
            reconciledTransactions: 0,
            completionPercentage: 0
        };
        
        return data;
    }
    
    /**
     * 清理發票數據
     */
    cleanInvoiceData(data) {
        // 確保金額字段是數字類型
        ['totalAmount', 'taxAmount'].forEach(field => {
            if (data[field] !== null) {
                data[field] = parseFloat(data[field]) || 0;
            }
        });
        
        // 清理行項目
        if (data.lineItems && Array.isArray(data.lineItems)) {
            data.lineItems = data.lineItems.map(item => ({
                ...item,
                quantity: parseFloat(item.quantity) || 0,
                unitPrice: parseFloat(item.unitPrice) || 0,
                totalPrice: parseFloat(item.totalPrice) || 0
            }));
        }
        
        return data;
    }
    
    /**
     * 清理收據數據
     */
    cleanReceiptData(data) {
        // 確保金額字段是數字類型
        ['totalAmount', 'taxAmount'].forEach(field => {
            if (data[field] !== null) {
                data[field] = parseFloat(data[field]) || 0;
            }
        });
        
        // 清理商品項目
        if (data.items && Array.isArray(data.items)) {
            data.items = data.items.map(item => ({
                ...item,
                quantity: parseFloat(item.quantity) || 0,
                price: parseFloat(item.price) || 0
            }));
        }
        
        return data;
    }
    
    /**
     * 驗證日期格式
     */
    validateDate(dateString) {
        if (!dateString) return null;
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            return null;
        }
        
        return date.toISOString().split('T')[0]; // YYYY-MM-DD格式
    }
    
    /**
     * 生成模擬數據（當API不可用時使用）
     */
    async generateMockData(file, documentType) {
        // 模擬處理時間
        await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 3000));
        
        const mockData = {
            documentType: documentType,
            aiProcessed: false,
            processedAt: new Date().toISOString()
        };
        
        switch (documentType) {
            case 'bank-statement':
                mockData.extractedFields = {
                    accountInfo: {
                        accountHolder: 'DEMO USER',
                        accountNumber: '****1234',
                        bankCode: '024',
                        branch: 'DEMO BRANCH'
                    },
                    statementPeriod: {
                        startDate: '2025-01-01',
                        endDate: '2025-01-31'
                    },
                    financialPosition: {
                        deposits: 50000.00,
                        personalLoans: -25000.00,
                        creditCards: -5000.00,
                        netPosition: 20000.00
                    },
                    transactions: [
                        {
                            date: '2025-01-15',
                            description: 'SALARY DEPOSIT',
                            amount: 30000.00,
                            balance: 50000.00,
                            type: 'credit'
                        },
                        {
                            date: '2025-01-20',
                            description: 'GROCERY SHOPPING',
                            amount: -500.00,
                            balance: 49500.00,
                            type: 'debit'
                        }
                    ],
                    reconciliation: {
                        totalTransactions: 2,
                        reconciledTransactions: 0,
                        completionPercentage: 0
                    }
                };
                break;
                
            case 'invoice':
                mockData.extractedFields = {
                    invoiceNumber: 'INV-2025-001',
                    issueDate: '2025-01-15',
                    dueDate: '2025-02-15',
                    vendor: 'Demo Vendor Ltd.',
                    customer: 'Demo Customer',
                    totalAmount: 1200.00,
                    taxAmount: 120.00,
                    currency: 'USD',
                    lineItems: [
                        {
                            description: 'Professional Services',
                            quantity: 10,
                            unitPrice: 100.00,
                            totalPrice: 1000.00
                        }
                    ]
                };
                break;
                
            case 'receipt':
                mockData.extractedFields = {
                    receiptNumber: 'RCP-001',
                    date: '2025-01-15',
                    merchant: 'Demo Store',
                    totalAmount: 45.99,
                    taxAmount: 4.59,
                    paymentMethod: 'Credit Card',
                    currency: 'USD',
                    items: [
                        {
                            name: 'Office Supplies',
                            quantity: 2,
                            price: 22.99
                        }
                    ]
                };
                break;
                
            default:
                mockData.extractedFields = {
                    documentType: 'General Document',
                    title: file.name,
                    date: new Date().toISOString().split('T')[0],
                    content: 'This is a demo document processed with mock data.',
                    keyInformation: ['Demo information 1', 'Demo information 2'],
                    entities: {
                        persons: ['Demo Person'],
                        organizations: ['Demo Organization'],
                        locations: ['Demo Location'],
                        dates: [new Date().toISOString().split('T')[0]],
                        amounts: ['$1000']
                    }
                };
        }
        
        return mockData;
    }
}

// 將類別暴露到全域範圍
window.GoogleAIProcessor = GoogleAIProcessor;

// 創建全域實例
window.googleAIProcessor = new GoogleAIProcessor();

console.log('🤖 Google AI處理器已載入');
