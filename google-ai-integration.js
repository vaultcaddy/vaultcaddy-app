/**
 * Google Cloud AI 整合模組
 * 使用 Google Gemini API 進行真實的文檔數據提取
 */

class GoogleAIProcessor {
    constructor() {
        this.apiKey = null;
        this.model = 'gemini-1.5-flash'; // 使用穩定的模型版本
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
        // 從 VaultCaddyConfig 獲取 API 密鑰和配置
        const config = window.VaultCaddyConfig?.apiConfig?.googleAI;
        
        if (config) {
            this.apiKey = config.apiKey;
            this.model = config.model || this.model;
            
            // 使用配置中的端點
            if (config.endpoint) {
                this.apiEndpoint = `${config.endpoint}/${this.model}:generateContent`;
            }
            
            // 保存備用端點
            this.fallbackEndpoints = config.fallbackEndpoints || [];
        } else {
            // 備用：嘗試舊的配置格式
            this.apiKey = window.config?.googleAI?.apiKey;
        }
        
        if (!this.apiKey || this.apiKey === 'demo-key') {
            console.warn('⚠️ Google AI API密鑰未設置，將使用模擬數據');
            console.info('💡 請設置 API Key: localStorage.setItem("google_ai_api_key", "your-key")');
        } else {
            console.log('🤖 Google AI處理器已初始化');
            console.log('   模型:', this.model);
            console.log('   端點:', this.apiEndpoint);
        }
    }
    
    /**
     * 處理文件並提取數據（帶重試機制）
     */
    async processDocument(file, documentType, options = {}) {
        const maxRetries = options.maxRetries || 3;
        const retryDelay = options.retryDelay || 2000;
        
        console.log(`🚀 開始處理文檔: ${file.name} (${documentType})`);
        console.log(`   最大重試次數: ${maxRetries}`);
        
        // 驗證文件
        const fileValidation = this.validateFileWithDetails(file);
        if (!fileValidation.isValid) {
            const error = new Error(fileValidation.error);
            error.code = 'FILE_VALIDATION_ERROR';
            error.details = fileValidation;
            throw error;
        }
        
        // 如果沒有API密鑰，使用模擬數據
        if (!this.apiKey || this.apiKey === 'demo-key') {
            console.log('🎭 使用模擬數據處理');
            return await this.generateMockData(file, documentType);
        }
        
        let lastError = null;
        
        // 重試循環
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                console.log(`🔄 嘗試 ${attempt}/${maxRetries}...`);
                
                // 將文件轉換為base64
                const base64Data = await this.fileToBase64(file);
                
                // 生成提示詞
                const prompt = this.generatePrompt(documentType);
                
                // 調用Google AI API
                const extractedData = await this.callGoogleAI(base64Data, file.type, prompt);
                
                // 處理和驗證返回的數據
                const processedData = this.processAIResponse(extractedData, documentType);
                
                // 檢查數據質量
                const qualityCheck = this.checkDataQuality(processedData, documentType);
                
                if (qualityCheck.isAcceptable) {
                    console.log('✅ Google AI處理完成');
                    console.log(`   信心分數: ${processedData.extractedFields.confidenceScore || 'N/A'}%`);
                    console.log(`   數據完整性: ${processedData.extractedFields.validationStatus?.completeness || 'N/A'}`);
                    
                    return {
                        ...processedData,
                        success: true,
                        attempts: attempt,
                        qualityScore: qualityCheck.score
                    };
                } else {
                    // 數據質量不佳，但不是最後一次嘗試
                    if (attempt < maxRetries) {
                        console.warn(`⚠️ 數據質量不佳 (${qualityCheck.score}%)，重試...`);
                        lastError = new Error(`數據質量不佳: ${qualityCheck.issues.join(', ')}`);
                        await new Promise(resolve => setTimeout(resolve, retryDelay));
                        continue;
                    } else {
                        // 最後一次嘗試，返回低質量數據並標記
                        console.warn(`⚠️ 達到最大重試次數，返回低質量數據`);
                        return {
                            ...processedData,
                            success: true,
                            lowQuality: true,
                            attempts: attempt,
                            qualityScore: qualityCheck.score,
                            qualityIssues: qualityCheck.issues
                        };
                    }
                }
                
            } catch (error) {
                console.error(`❌ 嘗試 ${attempt}/${maxRetries} 失敗:`, error.message);
                lastError = this.enhanceError(error, file, documentType, attempt);
                
                // 如果不是最後一次嘗試，等待後重試
                if (attempt < maxRetries) {
                    const delay = retryDelay * attempt; // 指數退避
                    console.log(`⏳ 等待 ${delay}ms 後重試...`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                } else {
                    // 最後一次嘗試失敗，拋出增強的錯誤
                    console.error('❌ 所有重試均失敗');
                    throw lastError;
                }
            }
        }
        
        // 如果所有重試都失敗，拋出最後的錯誤
        throw lastError || new Error('處理失敗，原因未知');
    }
    
    /**
     * 增強的文件驗證（返回詳細信息）
     */
    validateFileWithDetails(file) {
        const result = {
            isValid: true,
            error: null,
            warnings: []
        };
        
        // 檢查文件大小（20MB限制）
        const maxSize = 20 * 1024 * 1024;
        if (file.size > maxSize) {
            result.isValid = false;
            result.error = `文件過大: ${(file.size / 1024 / 1024).toFixed(2)}MB (最大 20MB)`;
            return result;
        }
        
        // 檢查文件類型
        const supportedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp', 'application/pdf'];
        if (!supportedTypes.includes(file.type)) {
            result.isValid = false;
            result.error = `不支持的文件類型: ${file.type}。支持的類型: JPG, PNG, GIF, WEBP, PDF`;
            return result;
        }
        
        // 警告：大文件可能處理較慢
        if (file.size > 5 * 1024 * 1024) {
            result.warnings.push(`文件較大 (${(file.size / 1024 / 1024).toFixed(2)}MB)，處理可能需要更長時間`);
        }
        
        return result;
    }
    
    /**
     * 檢查數據質量
     */
    checkDataQuality(processedData, documentType) {
        const extractedFields = processedData.extractedFields || {};
        const confidenceScore = extractedFields.confidenceScore || 0;
        const validationStatus = extractedFields.validationStatus || {};
        
        const issues = [];
        let score = confidenceScore;
        
        // 信心分數太低
        if (confidenceScore < 50) {
            issues.push(`信心分數過低 (${confidenceScore}%)`);
        }
        
        // 驗證失敗
        if (validationStatus.isValid === false) {
            issues.push(`驗證失敗: ${validationStatus.issues?.join(', ') || '未知錯誤'}`);
            score = Math.min(score, 40);
        }
        
        // 數據不完整
        if (validationStatus.completeness === 'Incomplete') {
            issues.push('數據不完整');
            score = Math.min(score, 60);
        }
        
        return {
            isAcceptable: score >= 50 && issues.length <= 2,
            score: score,
            issues: issues
        };
    }
    
    /**
     * 增強錯誤信息
     */
    enhanceError(error, file, documentType, attempt) {
        const enhancedError = new Error(error.message);
        enhancedError.originalError = error;
        enhancedError.fileName = file.name;
        enhancedError.fileSize = file.size;
        enhancedError.fileType = file.type;
        enhancedError.documentType = documentType;
        enhancedError.attempt = attempt;
        enhancedError.timestamp = new Date().toISOString();
        
        // 根據錯誤類型添加用戶友好的消息
        if (error.message.includes('API key not valid')) {
            enhancedError.code = 'INVALID_API_KEY';
            enhancedError.userMessage = 'API 密鑰無效，請檢查配置';
            enhancedError.suggestion = '請在 config.js 中設置有效的 Google AI API 密鑰';
        } else if (error.message.includes('location is not supported')) {
            enhancedError.code = 'REGION_NOT_SUPPORTED';
            enhancedError.userMessage = 'API 在當前地區不可用';
            enhancedError.suggestion = '正在嘗試備用端點...';
        } else if (error.message.includes('quota')) {
            enhancedError.code = 'QUOTA_EXCEEDED';
            enhancedError.userMessage = 'API 配額已用盡';
            enhancedError.suggestion = '請稍後再試或升級 API 計劃';
        } else if (error.message.includes('timeout')) {
            enhancedError.code = 'TIMEOUT';
            enhancedError.userMessage = '請求超時';
            enhancedError.suggestion = '文件可能過大或網絡連接不穩定';
        } else if (error.message.includes('JSON')) {
            enhancedError.code = 'INVALID_RESPONSE';
            enhancedError.userMessage = 'AI 返回的數據格式無效';
            enhancedError.suggestion = '正在重試以獲取有效數據...';
        } else {
            enhancedError.code = 'UNKNOWN_ERROR';
            enhancedError.userMessage = '處理失敗';
            enhancedError.suggestion = '請重試或聯繫技術支持';
        }
        
        return enhancedError;
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
You are an expert bank statement data extraction AI. Analyze this bank statement image and extract ALL information into a valid JSON object.

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanations
2. Extract ACTUAL data from the image - do not use placeholder text
3. All amounts must be pure numbers (no currency symbols, no commas)
4. All dates must be in YYYY-MM-DD format
5. Extract ALL transactions from the statement

REQUIRED JSON STRUCTURE:
{
  "documentType": "Bank Statement",
  "bankName": "actual bank name (e.g., HSBC, 匯豐銀行, Hang Seng Bank, 恒生銀行)",
  "accountHolder": "actual account holder name",
  "accountNumber": "actual account number (last 4 digits if masked)",
  "accountType": "Savings or Current or Credit Card",
  "currency": "HKD or USD or CNY",
  "statementPeriod": {
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD"
  },
  "balances": {
    "openingBalance": actual_number,
    "closingBalance": actual_number,
    "availableBalance": actual_number_or_null
  },
  "summary": {
    "totalDeposits": actual_number,
    "totalWithdrawals": actual_number,
    "numberOfTransactions": actual_number
  },
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "actual transaction description",
      "reference": "reference number or null",
      "debit": actual_number_or_0,
      "credit": actual_number_or_0,
      "balance": actual_number,
      "type": "Deposit or Withdrawal or Transfer or Fee or Interest"
    }
  ]
}

EXTRACTION GUIDELINES:
- Bank name is usually at the top (匯豐/HSBC, 恒生/Hang Seng, 中銀/Bank of China)
- Account holder name may be labeled as 客戶姓名/Account Holder/Name
- Account number may be partially masked (e.g., ****1234)
- Statement period: look for 結單期/Statement Period/From...To...
- Opening balance: 期初結餘/Opening Balance/Previous Balance
- Closing balance: 期末結餘/Closing Balance/Current Balance
- Transactions table columns: 日期/Date, 交易描述/Description, 支出/Debit, 存入/Credit, 結餘/Balance
- Extract ALL transaction rows from the table
- For amounts: positive = credit/deposit, negative = debit/withdrawal

HONG KONG BANK FORMATS:
- HSBC (匯豐銀行): Look for red/white logo
- Hang Seng Bank (恒生銀行): Look for blue logo
- Bank of China (中國銀行): Look for red logo
- Standard Chartered (渣打銀行): Look for blue/green logo

Extract the ACTUAL data from this bank statement image and return ONLY the JSON object.
            `,
            
            'invoice': `
You are an expert invoice data extraction AI. Analyze this invoice image and extract ALL information into a valid JSON object.

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanations
2. Extract ACTUAL data from the image - do not use placeholder text
3. All amounts must be pure numbers (no currency symbols like $, HKD)
4. All dates must be in YYYY-MM-DD format
5. If a field cannot be found, use null or empty string ""

REQUIRED JSON STRUCTURE:
{
  "documentType": "Invoice",
  "invoiceNumber": "actual invoice number from image",
  "issueDate": "YYYY-MM-DD",
  "deliveryDate": "YYYY-MM-DD or null",
  "dueDate": "YYYY-MM-DD or null",
  "vendor": {
    "name": "actual vendor company name",
    "address": "actual vendor address",
    "phone": "actual phone number",
    "email": "email or null",
    "taxId": "tax ID or null",
    "companyRegNo": "company registration number or null"
  },
  "customer": {
    "name": "actual customer name",
    "address": "actual customer address",
    "phone": "actual customer phone",
    "email": "email or null"
  },
  "lineItems": [
    {
      "itemCode": "actual item code from invoice",
      "description": "actual product description",
      "quantity": actual_number,
      "unit": "actual unit (件/箱/支/etc)",
      "unitPrice": actual_number,
      "amount": actual_number
    }
  ],
  "subtotal": actual_number,
  "discount": actual_number_or_0,
  "discountPercent": actual_number_or_0,
  "taxAmount": actual_number_or_0,
  "taxRate": actual_number_or_0,
  "totalAmount": actual_number,
  "currency": "HKD or USD or CNY",
  "paymentMethod": "CASH or Credit Card or Bank Transfer or C.O.D",
  "paymentTerms": "Net 30 or C.O.D or null",
  "paymentStatus": "Paid or Unpaid",
  "notes": "any notes or empty string"
}

EXTRACTION GUIDELINES:
- Look for invoice number near the top (發票號碼/INVOICE)
- Vendor info is usually at the top left (FROM/供應商)
- Customer info is usually at the top right (TO/客戶/BILL TO)
- Line items are in a table format with columns for item code, description, quantity, price
- Look for keywords: 小計/Subtotal, 折扣/Discount, 總計/Total, 合計/Grand Total
- Payment method keywords: CASH, 現金, C.O.D, 貨到付款, Credit Card, 信用卡
- Extract ALL line items from the table, not just the first one

EXAMPLE (for reference only - extract ACTUAL data):
If invoice shows "200602" as invoice number, return "invoiceNumber": "200602"
If date shows "2025-09-25", return "issueDate": "2025-09-25"
If total shows "$1,250.00", return "totalAmount": 1250.00
If item shows "01301 - 雀巢咖啡 × 2件 = $250", extract as:
{
  "itemCode": "01301",
  "description": "雀巢咖啡",
  "quantity": 2,
  "unit": "件",
  "unitPrice": 125.00,
  "amount": 250.00
}

Now extract the ACTUAL data from this invoice image and return ONLY the JSON object.
            `,
            
            'receipt': `
You are an expert receipt data extraction AI. Analyze this receipt image and extract ALL information into a valid JSON object.

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanations
2. Extract ACTUAL data from the image - do not use placeholder text
3. All amounts must be pure numbers (no currency symbols)
4. All dates must be in YYYY-MM-DD format
5. If a field cannot be found, use null or 0

REQUIRED JSON STRUCTURE:
{
  "documentType": "Receipt",
  "receiptNumber": "actual receipt number or null",
  "date": "YYYY-MM-DD",
  "merchant": {
    "name": "actual merchant/store name",
    "address": "actual address or null",
    "phone": "actual phone or null"
  },
  "items": [
    {
      "name": "actual item name",
      "quantity": actual_number,
      "unitPrice": actual_number,
      "amount": actual_number
    }
  ],
  "subtotal": actual_number,
  "taxAmount": actual_number_or_0,
  "tipAmount": actual_number_or_0,
  "totalAmount": actual_number,
  "currency": "HKD or USD or CNY",
  "paymentMethod": "Cash or Credit Card or Debit Card or Mobile Payment"
}

EXTRACTION GUIDELINES:
- Look for merchant name at the top (店名/商家)
- Receipt number may be labeled as 收據號/Receipt No/單號
- Items are usually in a list with name, quantity, and price
- Look for: 小計/Subtotal, 稅/Tax, 小費/Tip, 總計/Total
- Payment method: 現金/Cash, 信用卡/Credit Card, 八達通/Octopus, 支付寶/Alipay

Extract the ACTUAL data from this receipt image and return ONLY the JSON object.
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
        console.log('   模型:', this.model);
        console.log('   API Key:', this.apiKey ? (this.apiKey.substring(0, 10) + '...') : '未設置');
        
        // 構建端點列表（每個端點都需要加上模型路徑）
        const baseEndpoints = [
            this.apiEndpoint,
            ...(this.fallbackEndpoints || [])
        ];
        
        // 如果端點已經包含完整路徑（包含 :generateContent），直接使用
        // 否則添加模型路徑
        const endpoints = baseEndpoints.map(endpoint => {
            if (endpoint.includes(':generateContent')) {
                return endpoint;
            } else {
                return `${endpoint}/${this.model}:generateContent`;
            }
        });
        
        console.log('   嘗試的端點:', endpoints);
        
        let lastError = null;
        
        for (let i = 0; i < endpoints.length; i++) {
            const endpoint = endpoints[i];
            const apiUrl = `${endpoint}?key=${this.apiKey}`;
            
            console.log(`🔄 嘗試端點 ${i + 1}/${endpoints.length}:`);
            console.log(`   ${endpoint.replace(this.apiKey, '***')}`);
            
            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody)
                });
                
                if (response.ok) {
                    console.log(`✅ 端點 ${endpoint} 成功響應`);
                    const data = await response.json();
                    
                    if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
                        throw new Error('Google AI API返回無效響應');
                    }
                    
                    const textContent = data.candidates[0].content.parts[0].text;
                    console.log('📄 AI響應:', textContent.substring(0, 200) + '...');
                    
                    return textContent;
                } else {
                    const errorData = await response.json();
                    const errorMsg = `${response.status} - ${errorData.error?.message || 'Unknown error'}`;
                    console.warn(`⚠️ 端點 ${endpoint} 失敗: ${errorMsg}`);
                    lastError = new Error(`Google AI API錯誤: ${errorMsg}`);
                    
                    // 如果是地理限制錯誤，繼續嘗試下一個端點
                    if (errorData.error?.message?.includes('location is not supported')) {
                        continue;
                    }
                    // 其他錯誤也繼續嘗試
                }
            } catch (error) {
                console.warn(`⚠️ 端點 ${endpoint} 網絡錯誤:`, error.message);
                lastError = error;
            }
        }
        
        // 所有端點都失敗
        throw lastError || new Error('所有API端點都無法訪問');
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
        console.log('🧹 清理銀行對帳單數據...');
        
        // 確保 balances 對象存在
        if (!data.balances) {
            data.balances = {
                openingBalance: 0,
                closingBalance: 0,
                availableBalance: null
            };
        } else {
            data.balances.openingBalance = parseFloat(data.balances.openingBalance) || 0;
            data.balances.closingBalance = parseFloat(data.balances.closingBalance) || 0;
            if (data.balances.availableBalance !== null) {
                data.balances.availableBalance = parseFloat(data.balances.availableBalance) || 0;
            }
        }
        
        // 確保 summary 對象存在
        if (!data.summary) {
            data.summary = {
                totalDeposits: 0,
                totalWithdrawals: 0,
                numberOfTransactions: 0
            };
        } else {
            data.summary.totalDeposits = parseFloat(data.summary.totalDeposits) || 0;
            data.summary.totalWithdrawals = parseFloat(data.summary.totalWithdrawals) || 0;
            data.summary.numberOfTransactions = parseInt(data.summary.numberOfTransactions) || 0;
        }
        
        // 清理交易數據
        if (data.transactions && Array.isArray(data.transactions)) {
            data.transactions = data.transactions.map(transaction => ({
                date: this.validateDate(transaction.date),
                description: transaction.description || '',
                reference: transaction.reference || null,
                debit: parseFloat(transaction.debit) || 0,
                credit: parseFloat(transaction.credit) || 0,
                balance: parseFloat(transaction.balance) || 0,
                type: transaction.type || 'Unknown'
            }));
        } else {
            data.transactions = [];
        }
        
        // 驗證日期
        if (data.statementPeriod) {
            if (data.statementPeriod.startDate) {
                data.statementPeriod.startDate = this.validateDate(data.statementPeriod.startDate);
            }
            if (data.statementPeriod.endDate) {
                data.statementPeriod.endDate = this.validateDate(data.statementPeriod.endDate);
            }
        }
        
        // 添加對帳信息
        data.reconciliation = {
            totalTransactions: data.transactions.length,
            reconciledTransactions: 0,
            completionPercentage: 0
        };
        
        // 計算信心分數
        data.confidenceScore = this.calculateBankStatementConfidence(data);
        
        // 添加驗證狀態
        data.validationStatus = this.validateBankStatementData(data);
        
        console.log('✅ 銀行對帳單數據清理完成');
        console.log('   信心分數:', data.confidenceScore);
        console.log('   驗證狀態:', data.validationStatus);
        
        return data;
    }
    
    /**
     * 計算銀行對帳單數據的信心分數 (0-100)
     */
    calculateBankStatementConfidence(data) {
        let score = 0;
        let maxScore = 0;
        
        // 銀行名稱 (10分)
        maxScore += 10;
        if (data.bankName && data.bankName.length > 0) {
            score += 10;
        }
        
        // 帳戶信息 (20分)
        maxScore += 20;
        if (data.accountHolder && data.accountHolder.length > 0) {
            score += 10;
        }
        if (data.accountNumber && data.accountNumber.length > 0) {
            score += 10;
        }
        
        // 對帳期間 (15分)
        maxScore += 15;
        if (data.statementPeriod?.startDate) {
            score += 7;
        }
        if (data.statementPeriod?.endDate) {
            score += 8;
        }
        
        // 餘額信息 (20分)
        maxScore += 20;
        if (data.balances?.openingBalance !== undefined && data.balances.openingBalance !== null) {
            score += 10;
        }
        if (data.balances?.closingBalance !== undefined && data.balances.closingBalance !== null) {
            score += 10;
        }
        
        // 交易記錄 (35分)
        maxScore += 35;
        if (data.transactions && data.transactions.length > 0) {
            score += 20;
            // 檢查交易記錄的完整性
            const completeTransactions = data.transactions.filter(t => 
                t.date && t.description && (t.debit > 0 || t.credit > 0)
            );
            if (completeTransactions.length === data.transactions.length) {
                score += 15;
            } else if (completeTransactions.length > data.transactions.length * 0.8) {
                score += 10;
            }
        }
        
        // 計算百分比
        const percentage = Math.round((score / maxScore) * 100);
        console.log(`📊 信心分數計算: ${score}/${maxScore} = ${percentage}%`);
        
        return percentage;
    }
    
    /**
     * 驗證銀行對帳單數據完整性
     */
    validateBankStatementData(data) {
        const issues = [];
        
        // 必填字段檢查
        if (!data.bankName || data.bankName.length === 0) {
            issues.push('缺少銀行名稱');
        }
        
        if (!data.accountHolder || data.accountHolder.length === 0) {
            issues.push('缺少帳戶持有人');
        }
        
        if (!data.accountNumber || data.accountNumber.length === 0) {
            issues.push('缺少帳戶號碼');
        }
        
        if (!data.statementPeriod?.startDate || !data.statementPeriod?.endDate) {
            issues.push('缺少對帳期間');
        }
        
        if (!data.transactions || data.transactions.length === 0) {
            issues.push('缺少交易記錄');
        }
        
        // 餘額一致性檢查
        if (data.transactions && data.transactions.length > 0 && data.balances) {
            const lastTransaction = data.transactions[data.transactions.length - 1];
            if (lastTransaction.balance && data.balances.closingBalance) {
                const difference = Math.abs(lastTransaction.balance - data.balances.closingBalance);
                if (difference > 0.01) { // 允許 0.01 的誤差
                    issues.push(`期末餘額不匹配 (最後交易餘額: ${lastTransaction.balance.toFixed(2)}, 期末餘額: ${data.balances.closingBalance.toFixed(2)})`);
                }
            }
        }
        
        return {
            isValid: issues.length === 0,
            issues: issues,
            completeness: issues.length === 0 ? 'Complete' : (issues.length <= 2 ? 'Partial' : 'Incomplete')
        };
    }
    
    /**
     * 清理發票數據
     */
    cleanInvoiceData(data) {
        console.log('🧹 清理發票數據...');
        
        // 確保金額字段是數字類型
        const amountFields = ['subtotal', 'discount', 'discountPercent', 'taxAmount', 'taxRate', 'totalAmount'];
        amountFields.forEach(field => {
            if (data[field] !== undefined && data[field] !== null) {
                const value = parseFloat(String(data[field]).replace(/[^0-9.-]/g, ''));
                data[field] = isNaN(value) ? 0 : value;
            } else {
                data[field] = 0;
            }
        });
        
        // 清理行項目
        if (data.lineItems && Array.isArray(data.lineItems)) {
            data.lineItems = data.lineItems.map(item => ({
                itemCode: item.itemCode || '',
                description: item.description || '',
                quantity: parseFloat(item.quantity) || 0,
                unit: item.unit || '',
                unitPrice: parseFloat(item.unitPrice) || 0,
                amount: parseFloat(item.amount) || 0
            }));
        } else {
            data.lineItems = [];
        }
        
        // 驗證日期
        if (data.issueDate) {
            data.issueDate = this.validateDate(data.issueDate);
        }
        if (data.deliveryDate) {
            data.deliveryDate = this.validateDate(data.deliveryDate);
        }
        if (data.dueDate) {
            data.dueDate = this.validateDate(data.dueDate);
        }
        
        // 確保 vendor 和 customer 對象存在
        if (!data.vendor) {
            data.vendor = { name: '', address: '', phone: '', email: null };
        }
        if (!data.customer) {
            data.customer = { name: '', address: '', phone: '', email: null };
        }
        
        // 計算信心分數
        data.confidenceScore = this.calculateInvoiceConfidence(data);
        
        // 添加驗證狀態
        data.validationStatus = this.validateInvoiceData(data);
        
        console.log('✅ 發票數據清理完成');
        console.log('   信心分數:', data.confidenceScore);
        console.log('   驗證狀態:', data.validationStatus);
        
        return data;
    }
    
    /**
     * 計算發票數據的信心分數 (0-100)
     */
    calculateInvoiceConfidence(data) {
        let score = 0;
        let maxScore = 0;
        
        // 發票號碼 (10分)
        maxScore += 10;
        if (data.invoiceNumber && data.invoiceNumber.length > 0) {
            score += 10;
        }
        
        // 日期 (10分)
        maxScore += 10;
        if (data.issueDate) {
            score += 10;
        }
        
        // 供應商信息 (20分)
        maxScore += 20;
        if (data.vendor?.name && data.vendor.name.length > 0) {
            score += 10;
        }
        if (data.vendor?.address && data.vendor.address.length > 0) {
            score += 5;
        }
        if (data.vendor?.phone && data.vendor.phone.length > 0) {
            score += 5;
        }
        
        // 客戶信息 (15分)
        maxScore += 15;
        if (data.customer?.name && data.customer.name.length > 0) {
            score += 10;
        }
        if (data.customer?.address && data.customer.address.length > 0) {
            score += 5;
        }
        
        // 行項目 (25分)
        maxScore += 25;
        if (data.lineItems && data.lineItems.length > 0) {
            score += 15;
            // 檢查行項目的完整性
            const completeItems = data.lineItems.filter(item => 
                item.description && item.quantity > 0 && item.amount > 0
            );
            if (completeItems.length === data.lineItems.length) {
                score += 10;
            }
        }
        
        // 金額信息 (20分)
        maxScore += 20;
        if (data.totalAmount && data.totalAmount > 0) {
            score += 10;
        }
        if (data.subtotal && data.subtotal > 0) {
            score += 5;
        }
        if (data.currency && data.currency.length > 0) {
            score += 5;
        }
        
        // 計算百分比
        const percentage = Math.round((score / maxScore) * 100);
        console.log(`📊 信心分數計算: ${score}/${maxScore} = ${percentage}%`);
        
        return percentage;
    }
    
    /**
     * 驗證發票數據完整性
     */
    validateInvoiceData(data) {
        const issues = [];
        
        // 必填字段檢查
        if (!data.invoiceNumber || data.invoiceNumber.length === 0) {
            issues.push('缺少發票號碼');
        }
        
        if (!data.issueDate) {
            issues.push('缺少發票日期');
        }
        
        if (!data.vendor?.name || data.vendor.name.length === 0) {
            issues.push('缺少供應商名稱');
        }
        
        if (!data.customer?.name || data.customer.name.length === 0) {
            issues.push('缺少客戶名稱');
        }
        
        if (!data.lineItems || data.lineItems.length === 0) {
            issues.push('缺少商品項目');
        }
        
        if (!data.totalAmount || data.totalAmount <= 0) {
            issues.push('缺少總金額或金額無效');
        }
        
        // 金額一致性檢查
        if (data.lineItems && data.lineItems.length > 0 && data.subtotal > 0) {
            const calculatedSubtotal = data.lineItems.reduce((sum, item) => sum + (item.amount || 0), 0);
            const difference = Math.abs(calculatedSubtotal - data.subtotal);
            if (difference > 0.01) { // 允許 0.01 的誤差
                issues.push(`小計金額不匹配 (計算值: ${calculatedSubtotal.toFixed(2)}, 提取值: ${data.subtotal.toFixed(2)})`);
            }
        }
        
        return {
            isValid: issues.length === 0,
            issues: issues,
            completeness: issues.length === 0 ? 'Complete' : (issues.length <= 2 ? 'Partial' : 'Incomplete')
        };
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
