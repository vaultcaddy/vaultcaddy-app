/**
 * Google Document AI 處理器
 * 專門為文檔處理設計，更穩定且無地理限制
 */

class GoogleDocumentAI {
    constructor() {
        this.config = window.VaultCaddyConfig?.apiConfig?.documentAI;
        this.apiKey = this.config?.apiKey;
        this.projectId = this.config?.projectId;
        this.location = this.config?.location || 'us';
        this.endpoint = this.config?.endpoint;
        
        console.log('📄 Google Document AI 處理器初始化');
        
        if (!this.apiKey) {
            console.warn('⚠️ Google Document AI API密鑰未設置');
        } else {
            console.log('✅ Google Document AI API密鑰已載入');
        }
    }
    
    /**
     * 處理文檔
     */
    async processDocument(file, documentType = 'general') {
        const startTime = Date.now();
        
        try {
            if (!this.apiKey) {
                throw new Error('Google Document AI API密鑰未設置');
            }
            
            console.log(`🚀 開始Document AI處理: ${file.name} (${documentType})`);
            
            // 將文件轉換為base64
            const base64Data = await this.fileToBase64(file);
            
            // 構建請求
            const requestBody = {
                rawDocument: {
                    content: base64Data,
                    mimeType: file.type
                }
            };
            
            // 選擇處理器
            const processorName = this.getProcessorName(documentType);
            const url = `${this.endpoint}/${processorName}:process`;
            
            console.log('📡 調用Document AI API...');
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json',
                    'x-goog-user-project': this.projectId
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`Document AI API錯誤: ${response.status} - ${errorData}`);
            }
            
            const result = await response.json();
            
            // 處理響應
            const extractedData = this.parseDocumentAIResponse(result, documentType);
            
            console.log(`✅ Document AI處理完成，耗時: ${Date.now() - startTime}ms`);
            
            return {
                success: true,
                data: extractedData,
                processingTime: Date.now() - startTime,
                engine: 'google-document-ai'
            };
            
        } catch (error) {
            console.error('❌ Document AI處理失敗:', error);
            throw error;
        }
    }
    
    /**
     * 獲取處理器名稱
     */
    getProcessorName(documentType) {
        const processors = this.config?.processors;
        
        switch (documentType) {
            case 'invoice':
                return processors?.invoice || `projects/${this.projectId}/locations/${this.location}/processors/invoice`;
            case 'receipt':
                return processors?.receipt || `projects/${this.projectId}/locations/${this.location}/processors/receipt`;
            case 'bank_statement':
                return processors?.general || `projects/${this.projectId}/locations/${this.location}/processors/general`;
            default:
                return processors?.general || `projects/${this.projectId}/locations/${this.location}/processors/general`;
        }
    }
    
    /**
     * 解析Document AI響應
     */
    parseDocumentAIResponse(response, documentType) {
        try {
            const document = response.document;
            
            if (!document) {
                throw new Error('Document AI返回無效響應');
            }
            
            // 提取文本
            const text = document.text || '';
            
            // 提取實體
            const entities = document.entities || [];
            
            // 根據文檔類型解析
            switch (documentType) {
                case 'receipt':
                    return this.parseReceiptData(entities, text);
                case 'invoice':
                    return this.parseInvoiceData(entities, text);
                case 'bank_statement':
                    return this.parseBankStatementData(entities, text);
                default:
                    return this.parseGeneralData(entities, text);
            }
            
        } catch (error) {
            console.error('解析Document AI響應失敗:', error);
            throw new Error(`解析失敗: ${error.message}`);
        }
    }
    
    /**
     * 解析收據數據
     */
    parseReceiptData(entities, text) {
        const data = {
            type: 'receipt',
            merchant: '',
            date: '',
            total: '',
            items: [],
            raw_text: text
        };
        
        entities.forEach(entity => {
            switch (entity.type) {
                case 'supplier_name':
                    data.merchant = entity.mentionText || '';
                    break;
                case 'invoice_date':
                case 'receipt_date':
                    data.date = entity.mentionText || '';
                    break;
                case 'total_amount':
                    data.total = entity.mentionText || '';
                    break;
                case 'line_item':
                    if (entity.properties) {
                        const item = {};
                        entity.properties.forEach(prop => {
                            if (prop.type === 'line_item/description') {
                                item.description = prop.mentionText;
                            } else if (prop.type === 'line_item/amount') {
                                item.amount = prop.mentionText;
                            }
                        });
                        if (item.description || item.amount) {
                            data.items.push(item);
                        }
                    }
                    break;
            }
        });
        
        return data;
    }
    
    /**
     * 解析發票數據
     */
    parseInvoiceData(entities, text) {
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
        
        entities.forEach(entity => {
            switch (entity.type) {
                case 'supplier_name':
                    data.supplier = entity.mentionText || '';
                    break;
                case 'invoice_id':
                    data.invoice_number = entity.mentionText || '';
                    break;
                case 'invoice_date':
                    data.date = entity.mentionText || '';
                    break;
                case 'due_date':
                    data.due_date = entity.mentionText || '';
                    break;
                case 'total_amount':
                    data.total = entity.mentionText || '';
                    break;
            }
        });
        
        return data;
    }
    
    /**
     * 解析銀行對帳單數據
     */
    parseBankStatementData(entities, text) {
        const data = {
            type: 'bank_statement',
            account_number: '',
            statement_date: '',
            transactions: [],
            raw_text: text
        };
        
        // 使用正則表達式提取交易記錄
        const transactionPattern = /(\d{2}\/\d{2}\/\d{4})\s+(.+?)\s+([\-\+]?\$?[\d,]+\.?\d*)/g;
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
     * 解析通用數據
     */
    parseGeneralData(entities, text) {
        const data = {
            type: 'general',
            extracted_fields: {},
            raw_text: text
        };
        
        entities.forEach(entity => {
            data.extracted_fields[entity.type] = entity.mentionText || '';
        });
        
        return data;
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
window.GoogleDocumentAI = GoogleDocumentAI;
window.googleDocumentAI = new GoogleDocumentAI();

console.log('📄 Google Document AI 模塊已載入');
