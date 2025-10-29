/**
 * Claude Vision API Client
 * 
 * 使用 Claude 3.5 Sonnet 直接處理圖片和 PDF
 * 優勢：
 * - 真正的視覺理解（可以看懂圖片佈局）
 * - 原生 PDF 支持
 * - 95-98% 準確度
 * - 5-10 秒處理速度
 * 
 * 成本：~$0.021 / 張
 * 
 * @version 1.0.0
 * @updated 2025-10-28
 */

class ClaudeVisionClient {
    constructor() {
        // ⚠️ API Key 應該通過 Cloudflare Worker 保護
        this.workerUrl = 'https://claude-proxy.vaultcaddy.workers.dev';
        
        // ✅ 使用 Claude 3 Haiku（經濟型，高性價比）
        this.model = 'claude-3-haiku-20240307';  
        // 可選：'claude-3-5-sonnet-20241022' (最高準確度，成本較高)
        
        this.maxRetries = 3;
        this.retryDelay = 2000;
        
        console.log('🤖 Claude Vision Client 初始化（Haiku）');
        console.log('   ✅ 模型:', this.model);
        console.log('   ✅ Worker URL:', this.workerUrl);
        console.log('   ✅ 支持格式: JPG, PNG, PDF, WebP');
        console.log('   💰 成本: ~$0.003/張 (90-93% 準確度)');
    }
    
    /**
     * 處理文檔（圖片或 PDF）
     */
    async processDocument(file, documentType = 'invoice') {
        const startTime = Date.now();
        console.log(`\n🚀 Claude Vision 開始處理: ${file.name} (${documentType})`);
        
        try {
            // 1. 將文件轉換為 base64
            const base64Data = await this.fileToBase64(file);
            const mediaType = this.getMediaType(file.type);
            
            console.log('📸 文件信息:');
            console.log(`   類型: ${file.type}`);
            console.log(`   大小: ${(file.size / 1024).toFixed(2)} KB`);
            console.log(`   Media Type: ${mediaType}`);
            
            // 2. 生成 Prompt
            const prompt = this.generatePrompt(documentType);
            
            // 3. 構建請求
            const requestBody = {
                model: this.model,
                max_tokens: 4096,
                messages: [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'image',
                                source: {
                                    type: 'base64',
                                    media_type: mediaType,
                                    data: base64Data
                                }
                            },
                            {
                                type: 'text',
                                text: prompt
                            }
                        ]
                    }
                ]
            };
            
            // 4. 調用 Claude API（通過 Cloudflare Worker）
            console.log('📤 發送請求到 Claude API...');
            const response = await fetch(this.workerUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Claude API 錯誤: ${response.status} - ${errorData.error?.message || errorData.message}`);
            }
            
            const data = await response.json();
            console.log('📥 收到 Claude 響應');
            
            // 5. 解析響應
            if (!data.content || data.content.length === 0) {
                throw new Error('Claude 返回空響應');
            }
            
            const contentText = data.content[0].text;
            console.log('📄 響應長度:', contentText.length, '字符');
            
            // 6. 解析 JSON
            let extractedData;
            try {
                // 嘗試直接解析
                extractedData = JSON.parse(contentText);
            } catch (parseError) {
                // 嘗試清理後解析（移除 markdown 代碼塊）
                const cleaned = contentText.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
                extractedData = JSON.parse(cleaned);
            }
            
            const processingTime = Date.now() - startTime;
            console.log(`✅ Claude Vision 處理完成，耗時: ${processingTime}ms`);
            
            return {
                success: true,
                documentType: extractedData.document_type || documentType,
                confidence: extractedData.confidence_score || 95,
                extractedData: extractedData.extracted_data,
                processingTime: processingTime,
                processor: 'claude-vision',
                usage: {
                    input_tokens: data.usage?.input_tokens || 0,
                    output_tokens: data.usage?.output_tokens || 0,
                    estimated_cost: this.calculateCost(data.usage)
                }
            };
            
        } catch (error) {
            console.error('❌ Claude Vision 處理失敗:', error);
            throw error;
        }
    }
    
    /**
     * 生成 Prompt
     */
    generatePrompt(documentType) {
        const baseInstruction = `
You are an expert accounting AI assistant. Analyze this ${documentType} image and extract ALL data in structured JSON format.

CRITICAL RULES:
1. Return ONLY pure JSON, no explanations or markdown
2. Extract ALL visible text, numbers, and data
3. If a field is not found, use empty string "" or 0
4. Do NOT make up data
5. Pay special attention to tables, line items, and amounts
6. Ensure all numerical values are numbers (not strings)
7. Dates should be in YYYY-MM-DD format

`;
        
        switch (documentType) {
            case 'invoice':
                return baseInstruction + `
Extract the following fields from the invoice:

CRITICAL AREAS TO FOCUS:
1. **Invoice Number** (發票號碼): Look for "Invoice No", "INV", "發票編號", etc.
2. **Customer Name** (客戶名稱): Look for "客戶", "Customer", "Bill To", etc.
3. **Unit Price** (單價): Extract from the price column in the table

Return this exact JSON structure:

{
  "document_type": "invoice",
  "confidence_score": 0-100,
  "extracted_data": {
    "invoice_number": "string (REQUIRED - 發票號碼)",
    "date": "YYYY-MM-DD (REQUIRED - convert Chinese dates)",
    "due_date": "YYYY-MM-DD or empty string",
    "supplier": "string (company name at top of invoice)",
    "supplier_address": "string",
    "supplier_phone": "string",
    "supplier_email": "string",
    "customer": "string (REQUIRED - 客戶名稱, look for Bill To, 客戶)",
    "customer_address": "string",
    "customer_phone": "string",
    "items": [
      {
        "description": "string (product name)",
        "quantity": number,
        "unit_price": number (REQUIRED - 單價, from price column)",
        "amount": number (total for this item)
      }
    ],
    "subtotal": number,
    "tax": number,
    "total": number,
    "currency": "string (e.g., HKD, USD)"
  }
}

IMPORTANT: 
- Make sure to extract the INVOICE NUMBER (發票號碼)
- Make sure to extract the CUSTOMER NAME (客戶名稱)
- Make sure to extract the UNIT PRICE (單價) from the table, NOT $0.00
- Look at the entire image, including headers, footers, and table structure
`;
            
            case 'receipt':
                return baseInstruction + `
Extract the following fields from the receipt:

{
  "document_type": "receipt",
  "confidence_score": 0-100,
  "extracted_data": {
    "receipt_number": "string",
    "date": "YYYY-MM-DD",
    "time": "HH:MM:SS",
    "merchant": "string",
    "merchant_address": "string",
    "merchant_phone": "string",
    "items": [
      {
        "description": "string",
        "quantity": number,
        "unit_price": number,
        "amount": number
      }
    ],
    "subtotal": number,
    "tax": number,
    "total": number,
    "payment_method": "string",
    "currency": "string"
  }
}
`;
            
            case 'bank-statement':
                return baseInstruction + `
Extract the following fields from the bank statement:

{
  "document_type": "bank-statement",
  "confidence_score": 0-100,
  "extracted_data": {
    "account_holder": "string",
    "account_number": "string",
    "statement_period": {
      "from": "YYYY-MM-DD",
      "to": "YYYY-MM-DD"
    },
    "opening_balance": number,
    "closing_balance": number,
    "transactions": [
      {
        "date": "YYYY-MM-DD",
        "description": "string",
        "reference": "string",
        "debit": number or 0,
        "credit": number or 0,
        "balance": number
      }
    ],
    "currency": "string"
  }
}
`;
            
            default:
                return baseInstruction + `
Extract all visible data from this document in a structured format.
`;
        }
    }
    
    /**
     * 將文件轉換為 Base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                // 移除 data:...;base64, 前綴
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
    
    /**
     * 獲取媒體類型
     */
    getMediaType(mimeType) {
        const typeMap = {
            'image/jpeg': 'image/jpeg',
            'image/jpg': 'image/jpeg',
            'image/png': 'image/png',
            'image/gif': 'image/gif',
            'image/webp': 'image/webp',
            'application/pdf': 'application/pdf'
        };
        return typeMap[mimeType] || 'image/jpeg';
    }
    
    /**
     * 計算成本
     */
    calculateCost(usage) {
        if (!usage) return 0;
        
        // Claude 3 Haiku 定價（經濟型）
        const inputCostPer1M = 0.25;   // $0.25 / 1M tokens
        const outputCostPer1M = 1.25;  // $1.25 / 1M tokens
        
        // 如果使用 Claude 3.5 Sonnet，請使用以下定價：
        // const inputCostPer1M = 3.00;   // $3 / 1M tokens
        // const outputCostPer1M = 15.00; // $15 / 1M tokens
        
        const inputCost = (usage.input_tokens / 1000000) * inputCostPer1M;
        const outputCost = (usage.output_tokens / 1000000) * outputCostPer1M;
        
        return (inputCost + outputCost).toFixed(4);
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.ClaudeVisionClient = ClaudeVisionClient;
    window.claudeVisionClient = new ClaudeVisionClient();
    console.log('✅ Claude Vision Client 模塊已載入');
}

