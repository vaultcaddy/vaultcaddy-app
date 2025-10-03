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
     * 從文本解析發票數據
     */
    parseInvoiceFromText(text) {
        const data = {
            type: 'invoice',
            supplier: '',
            invoice_number: '',
            date: '',
            due_date: '',
            total: '',
            items: [],
            raw_text: text
        };
        
        // 提取供應商名稱
        const lines = text.split('\n').filter(line => line.trim());
        if (lines.length > 0) {
            data.supplier = lines[0].trim();
        }
        
        // 提取發票號碼
        const invoicePattern = /發票[號编号]*[：:\s]*([A-Z0-9\-]+)|invoice[：:\s#]*([A-Z0-9\-]+)/i;
        const invoiceMatch = text.match(invoicePattern);
        if (invoiceMatch) {
            data.invoice_number = invoiceMatch[1] || invoiceMatch[2];
        }
        
        // 提取日期
        const datePattern = /(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/;
        const dateMatch = text.match(datePattern);
        if (dateMatch) {
            data.date = dateMatch[1];
        }
        
        // 提取總金額
        const totalPattern = /總計[：:\s]*\$?([\d,]+\.?\d*)|total[：:\s]*\$?([\d,]+\.?\d*)/i;
        const totalMatch = text.match(totalPattern);
        if (totalMatch) {
            data.total = totalMatch[1] || totalMatch[2];
        }
        
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
