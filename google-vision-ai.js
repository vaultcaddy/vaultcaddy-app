/**
 * Google Vision API 處理器
 * 作為Gemini API的備用方案，使用OCR + 文本分析
 */

class GoogleVisionAI {
    constructor() {
        this.config = window.VaultCaddyConfig?.apiConfig?.google;
        this.apiKey = this.config?.apiKey;
        this.endpoint = this.config?.endpoints?.vision;
        
        console.log('👁️ Google Vision AI 處理器初始化');
        
        if (!this.apiKey) {
            console.warn('⚠️ Google Vision API密鑰未設置');
        } else {
            console.log('✅ Google Vision API密鑰已載入');
        }
    }
    
    /**
     * 處理文檔
     */
    async processDocument(file, documentType = 'general') {
        const startTime = Date.now();
        
        try {
            if (!this.apiKey) {
                throw new Error('Google Vision API密鑰未設置');
            }
            
            console.log(`🚀 開始Vision AI處理: ${file.name} (${documentType})`);
            
            // 將文件轉換為base64
            const base64Data = await this.fileToBase64(file);
            
            // 構建請求
            const requestBody = {
                requests: [{
                    image: {
                        content: base64Data
                    },
                    features: [
                        {
                            type: 'TEXT_DETECTION',
                            maxResults: 1
                        },
                        {
                            type: 'DOCUMENT_TEXT_DETECTION',
                            maxResults: 1
                        }
                    ]
                }]
            };
            
            console.log('📡 調用Vision API...');
            
            const response = await fetch(`${this.endpoint}/images:annotate?key=${this.apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`Vision API錯誤: ${response.status} - ${errorData}`);
            }
            
            const result = await response.json();
            
            // 處理響應
            const extractedData = this.parseVisionResponse(result, documentType);
            
            console.log(`✅ Vision AI處理完成，耗時: ${Date.now() - startTime}ms`);
            
            return {
                success: true,
                data: extractedData,
                processingTime: Date.now() - startTime,
                engine: 'google-vision-ai'
            };
            
        } catch (error) {
            console.error('❌ Vision AI處理失敗:', error);
            throw error;
        }
    }
    
    /**
     * 解析Vision API響應
     */
    parseVisionResponse(response, documentType) {
        try {
            const annotations = response.responses[0];
            
            if (!annotations) {
                throw new Error('Vision API返回無效響應');
            }
            
            // 獲取文本
            const fullText = annotations.fullTextAnnotation?.text || '';
            const textAnnotations = annotations.textAnnotations || [];
            
            // 根據文檔類型解析
            switch (documentType) {
                case 'receipt':
                    return this.parseReceiptFromText(fullText);
                case 'invoice':
                    return this.parseInvoiceFromText(fullText);
                case 'bank_statement':
                    return this.parseBankStatementFromText(fullText);
                default:
                    return this.parseGeneralFromText(fullText, textAnnotations);
            }
            
        } catch (error) {
            console.error('解析Vision響應失敗:', error);
            throw new Error(`解析失敗: ${error.message}`);
        }
    }
    
    /**
     * 從文本解析收據數據
     */
    parseReceiptFromText(text) {
        const data = {
            type: 'receipt',
            merchant: '',
            date: '',
            total: '',
            items: [],
            raw_text: text
        };
        
        // 提取商家名稱（通常在第一行）
        const lines = text.split('\n').filter(line => line.trim());
        if (lines.length > 0) {
            data.merchant = lines[0].trim();
        }
        
        // 提取日期
        const datePattern = /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/;
        const dateMatch = text.match(datePattern);
        if (dateMatch) {
            data.date = dateMatch[1];
        }
        
        // 提取總金額
        const totalPatterns = [
            /總計[：:\s]*\$?([\d,]+\.?\d*)/i,
            /total[：:\s]*\$?([\d,]+\.?\d*)/i,
            /合計[：:\s]*\$?([\d,]+\.?\d*)/i
        ];
        
        for (const pattern of totalPatterns) {
            const match = text.match(pattern);
            if (match) {
                data.total = match[1];
                break;
            }
        }
        
        // 提取項目（簡單版本）
        const itemPattern = /(.+?)\s+\$?([\d,]+\.?\d*)/g;
        let match;
        while ((match = itemPattern.exec(text)) !== null) {
            const description = match[1].trim();
            const amount = match[2];
            
            // 過濾掉可能不是商品的行
            if (!description.match(/總計|total|合計|小計|税|tax/i) && description.length > 2) {
                data.items.push({
                    description: description,
                    amount: amount
                });
            }
        }
        
        return data;
    }
    
    /**
     * 從文本解析發票數據（增強版）
     */
    parseInvoiceFromText(text) {
        console.log('📋 開始解析發票文本...');
        console.log('   文本長度:', text.length, '字符');
        
        const data = {
            type: 'invoice',
            supplier: '',
            invoice_number: '',
            date: '',
            due_date: '',
            total: '',
            subtotal: '',
            tax: '',
            items: [],
            customer: '',
            payment_method: '',
            payment_status: 'Unpaid',
            raw_text: text
        };
        
        // 提取供應商名稱（第一行）
        const lines = text.split('\n').filter(line => line.trim());
        if (lines.length > 0) {
            data.supplier = lines[0].trim();
            console.log('   ✅ 供應商:', data.supplier);
        }
        
        // 提取發票號碼（多種格式）
        const invoicePatterns = [
            /發票[號编号]*[：:\s]*([A-Z0-9\/\-]+)/i,
            /invoice[：:\s#]*([A-Z0-9\/\-]+)/i,
            /INV[：:\s#]*([A-Z0-9\/\-]+)/i,
            /單號[：:\s]*([A-Z0-9\/\-]+)/i
        ];
        
        for (const pattern of invoicePatterns) {
            const match = text.match(pattern);
            if (match && match[1]) {
                data.invoice_number = match[1].trim();
                console.log('   ✅ 發票號碼:', data.invoice_number);
                break;
            }
        }
        
        // 提取所有日期（可能有多個）
        const allDates = [];
        const datePattern = /(\d{4}[\/\-年]\d{1,2}[\/\-月]\d{1,2}[日]?|\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/g;
        let dateMatch;
        while ((dateMatch = datePattern.exec(text)) !== null) {
            allDates.push(dateMatch[1]);
        }
        
        if (allDates.length > 0) {
            data.date = allDates[0]; // 第一個日期作為發票日期
            if (allDates.length > 1) {
                data.due_date = allDates[1]; // 第二個日期作為到期日
            }
            console.log('   ✅ 發票日期:', data.date);
            if (data.due_date) console.log('   ✅ 到期日:', data.due_date);
        }
        
        // 提取金額（多種格式）
        const amountPatterns = [
            { name: 'total', patterns: [/總[計額金][：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i, /total[：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i, /應付[：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i] },
            { name: 'subtotal', patterns: [/小計[：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i, /subtotal[：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i] },
            { name: 'tax', patterns: [/稅[額金][：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i, /tax[：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i, /GST[：:\s]*\$?\s*HKD?\s*([\d,]+\.?\d*)/i] }
        ];
        
        for (const { name, patterns } of amountPatterns) {
            for (const pattern of patterns) {
                const match = text.match(pattern);
                if (match && match[1]) {
                    data[name] = match[1].replace(/,/g, '');
                    console.log(`   ✅ ${name}:`, data[name]);
                    break;
                }
            }
        }
        
        // 如果沒找到總計，嘗試找最大的金額
        if (!data.total) {
            const allAmounts = [];
            const amountPattern = /\$?\s*HKD?\s*([\d,]+\.?\d{2})/g;
            let match;
            while ((match = amountPattern.exec(text)) !== null) {
                const amount = parseFloat(match[1].replace(/,/g, ''));
                if (amount > 0) {
                    allAmounts.push(amount);
                }
            }
            if (allAmounts.length > 0) {
                data.total = Math.max(...allAmounts).toString();
                console.log('   ⚠️ 推測總金額（最大值）:', data.total);
            }
        }
        
        // 提取客戶信息
        const customerPatterns = [
            /客戶[：:\s]*([^\n]+)/i,
            /customer[：:\s]*([^\n]+)/i,
            /收件人[：:\s]*([^\n]+)/i
        ];
        
        for (const pattern of customerPatterns) {
            const match = text.match(pattern);
            if (match && match[1]) {
                data.customer = match[1].trim();
                console.log('   ✅ 客戶:', data.customer);
                break;
            }
        }
        
        // 檢測付款方式
        const paymentPatterns = [
            { pattern: /現金|CASH/i, method: 'Cash' },
            { pattern: /支票|CHEQUE|CHECK/i, method: 'Cheque' },
            { pattern: /銀行轉帳|BANK TRANSFER/i, method: 'Bank Transfer' },
            { pattern: /信用卡|CREDIT CARD/i, method: 'Credit Card' }
        ];
        
        for (const { pattern, method } of paymentPatterns) {
            if (pattern.test(text)) {
                data.payment_method = method;
                console.log('   ✅ 付款方式:', data.payment_method);
                break;
            }
        }
        
        // 提取商品項目（簡化版）
        // 尋找表格式數據：數量 × 單價 = 金額
        const itemPattern = /(.{2,30}?)\s+(\d+)\s*[个個件箱]\s+[\d,]+\.?\d*\s+[\d,]+\.?\d*/g;
        let itemMatch;
        let itemCount = 0;
        
        while ((itemMatch = itemPattern.exec(text)) !== null && itemCount < 20) {
            const description = itemMatch[1].trim();
            const quantity = itemMatch[2];
            
            if (description.length > 2 && !description.match(/總計|合計|小計|稅/i)) {
                data.items.push({
                    description: description,
                    quantity: quantity
                });
                itemCount++;
            }
        }
        
        if (data.items.length > 0) {
            console.log('   ✅ 提取到', data.items.length, '個商品項目');
        }
        
        console.log('📋 發票解析完成');
        return data;
    }
    
    /**
     * 從文本解析銀行對帳單數據
     */
    parseBankStatementFromText(text) {
        const data = {
            type: 'bank_statement',
            account_number: '',
            statement_date: '',
            transactions: [],
            raw_text: text
        };
        
        // 提取帳戶號碼
        const accountPattern = /帳戶[號编号]*[：:\s]*([0-9\-]+)|account[：:\s#]*([0-9\-]+)/i;
        const accountMatch = text.match(accountPattern);
        if (accountMatch) {
            data.account_number = accountMatch[1] || accountMatch[2];
        }
        
        // 提取交易記錄
        const transactionPattern = /(\d{2}[\/\-]\d{2}[\/\-]\d{2,4})\s+(.+?)\s+([\-\+]?\$?[\d,]+\.?\d*)/g;
        let match;
        
        while ((match = transactionPattern.exec(text)) !== null) {
            data.transactions.push({
                date: match[1],
                description: match[2].trim(),
                amount: match[3]
            });
        }
        
        return data;
    }
    
    /**
     * 從文本解析通用數據
     */
    parseGeneralFromText(text, textAnnotations) {
        return {
            type: 'general',
            text: text,
            annotations: textAnnotations.map(annotation => ({
                text: annotation.description,
                confidence: annotation.score || 1.0
            })),
            raw_text: text
        };
    }
    
    /**
     * 文件轉base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = () => {
                const result = reader.result.toString();
                const base64 = result.split(',')[1]; // 移除data:mime/type;base64,前綴
                resolve(base64);
            };
            
            reader.onerror = (error) => {
                reject(new Error(`文件讀取失敗: ${error.message}`));
            };
            
            reader.readAsDataURL(file);
        });
    }
}

// 全局暴露
window.GoogleVisionAI = GoogleVisionAI;
window.googleVisionAI = new GoogleVisionAI();

console.log('👁️ Google Vision AI 模塊已載入');
