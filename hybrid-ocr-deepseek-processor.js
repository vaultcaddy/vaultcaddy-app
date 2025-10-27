/**
 * 混合處理器：Vision API OCR + DeepSeek 文本處理
 * 
 * 工作流程：
 * 1. 使用 Vision API 進行 OCR（提取圖片中的文本）
 * 2. 將提取的文本發送給 DeepSeek 進行結構化處理
 * 3. 返回結構化的數據
 * 
 * 優勢：
 * - 準確度高（85-95%）
 * - 成本低（$1.64 / 1000 張）
 * - 在香港可用
 * - 結合 Vision API 的 OCR 能力和 DeepSeek 的文本理解能力
 */

class HybridOCRDeepSeekProcessor {
    constructor() {
        this.visionAI = window.googleVisionAI;
        this.deepseekWorkerUrl = 'https://deepseek-proxy.vaultcaddy.workers.dev';
        this.deepseekModel = 'deepseek-chat'; // 純文本模型
        
        console.log('🔄 混合處理器初始化（OCR + DeepSeek）');
        console.log('   ✅ Vision API:', this.visionAI ? '可用' : '不可用');
        console.log('   ✅ DeepSeek Worker:', this.deepseekWorkerUrl);
    }
    
    /**
     * 處理文檔
     */
    async processDocument(file, documentType = 'general') {
        const startTime = Date.now();
        console.log(`\n🚀 混合處理器開始處理: ${file.name} (${documentType})`);
        
        try {
            // ========== 步驟 1：使用 Vision API 提取文本 ==========
            console.log('📸 步驟 1/2: 使用 Vision API 進行 OCR...');
            const ocrStartTime = Date.now();
            
            const ocrText = await this.extractTextWithVisionAPI(file);
            
            console.log(`✅ OCR 完成，耗時: ${Date.now() - ocrStartTime}ms`);
            console.log(`📄 提取的文本長度: ${ocrText.length} 字符`);
            console.log(`📄 文本預覽: ${ocrText.substring(0, 200)}...`);
            
            // ========== 步驟 2：使用 DeepSeek 處理文本 ==========
            console.log('\n🤖 步驟 2/2: 使用 DeepSeek 處理文本...');
            const deepseekStartTime = Date.now();
            
            const structuredData = await this.processTextWithDeepSeek(ocrText, documentType);
            
            console.log(`✅ DeepSeek 處理完成，耗時: ${Date.now() - deepseekStartTime}ms`);
            console.log(`\n🎉 混合處理完成，總耗時: ${Date.now() - startTime}ms`);
            
            return {
                success: true,
                documentType: structuredData.document_type || documentType,
                confidence: structuredData.confidence_score || 85,
                extractedData: structuredData.extracted_data,
                ocrText: ocrText, // 保留原始 OCR 文本供調試
                processingTime: {
                    ocr: Date.now() - ocrStartTime,
                    deepseek: Date.now() - deepseekStartTime,
                    total: Date.now() - startTime
                },
                processor: 'hybrid-ocr-deepseek'
            };
            
        } catch (error) {
            console.error('❌ 混合處理器失敗:', error);
            throw error;
        }
    }
    
    /**
     * 使用 Vision API 提取文本
     */
    async extractTextWithVisionAPI(file) {
        if (!this.visionAI) {
            throw new Error('Vision API 不可用');
        }
        
        // 將文件轉換為 base64
        const base64Data = await this.fileToBase64(file);
        
        // 調用 Vision API
        const config = window.VaultCaddyConfig?.apiConfig?.google;
        const apiKey = config?.apiKey;
        const endpoint = config?.endpoints?.vision;
        
        if (!apiKey) {
            throw new Error('Google Vision API 密鑰未設置');
        }
        
        const requestBody = {
            requests: [{
                image: {
                    content: base64Data
                },
                features: [
                    {
                        type: 'DOCUMENT_TEXT_DETECTION', // 使用文檔文本檢測（更適合文檔）
                        maxResults: 1
                    }
                ]
            }]
        };
        
        const response = await fetch(`${endpoint}/images:annotate?key=${apiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.text();
            throw new Error(`Vision API 錯誤: ${response.status} - ${errorData}`);
        }
        
        const result = await response.json();
        
        // 提取文本
        const annotations = result.responses[0];
        if (!annotations || !annotations.fullTextAnnotation) {
            throw new Error('Vision API 未能提取文本');
        }
        
        return annotations.fullTextAnnotation.text;
    }
    
    /**
     * 使用 DeepSeek 處理文本
     */
    async processTextWithDeepSeek(text, documentType) {
        const prompt = this.generatePrompt(text, documentType);
        
        const requestBody = {
            model: this.deepseekModel,
            messages: [
                {
                    role: 'system',
                    content: 'You are an expert accounting AI assistant specialized in extracting structured data from financial documents. You will receive OCR-extracted text and must parse it into structured JSON format.'
                },
                {
                    role: 'user',
                    content: prompt
                }
            ],
            max_tokens: 4000,
            temperature: 0.1 // 低溫度以獲得更準確的輸出
        };
        
        const response = await fetch(this.deepseekWorkerUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`DeepSeek API 錯誤: ${response.status} - ${errorData.error?.message || errorData.message}`);
        }
        
        const data = await response.json();
        
        if (!data.choices || data.choices.length === 0 || !data.choices[0].message) {
            throw new Error('DeepSeek API 返回無效響應');
        }
        
        const content = data.choices[0].message.content;
        
        // 解析 JSON
        let parsedData;
        try {
            parsedData = JSON.parse(content);
        } catch (jsonError) {
            // 嘗試清理響應（移除 markdown 代碼塊）
            const cleaned = content.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
            parsedData = JSON.parse(cleaned);
        }
        
        return parsedData;
    }
    
    /**
     * 生成 DeepSeek 提示詞
     */
    generatePrompt(ocrText, documentType) {
        const baseInstruction = `
I have extracted the following text from a ${documentType} image using OCR:

---
${ocrText}
---

Please analyze this text and extract structured data in JSON format.

CRITICAL RULES:
1. Return ONLY pure JSON, no explanations or markdown
2. If a field is not found, use empty string "" or 0
3. Do NOT make up data
4. Ensure all numerical values are numbers (not strings)
5. Dates should be in YYYY-MM-DD format

`;
        
        switch (documentType) {
            case 'invoice':
                return baseInstruction + `
Extract the following fields:

{
  "document_type": "invoice",
  "confidence_score": 0-100,
  "extracted_data": {
    "invoice_number": "string",
    "date": "YYYY-MM-DD",
    "due_date": "YYYY-MM-DD",
    "supplier": {
      "name": "string",
      "address": "string",
      "phone": "string",
      "email": "string"
    },
    "customer": {
      "name": "string",
      "address": "string",
      "phone": "string"
    },
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
    "currency": "string (e.g., HKD, USD)"
  }
}`;
            
            case 'receipt':
                return baseInstruction + `
Extract the following fields:

{
  "document_type": "receipt",
  "confidence_score": 0-100,
  "extracted_data": {
    "transaction_id": "string",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "merchant": {
      "name": "string",
      "address": "string",
      "phone": "string"
    },
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
    "currency": "string",
    "payment_method": "string"
  }
}`;
            
            case 'bank_statement':
                return baseInstruction + `
Extract the following fields:

{
  "document_type": "bank_statement",
  "confidence_score": 0-100,
  "extracted_data": {
    "bank": {
      "name": "string",
      "address": "string"
    },
    "account_number": "string",
    "account_holder": {
      "name": "string"
    },
    "statement_period": {
      "from": "YYYY-MM-DD",
      "to": "YYYY-MM-DD"
    },
    "opening_balance": number,
    "closing_balance": number,
    "currency": "string",
    "transactions": [
      {
        "date": "YYYY-MM-DD",
        "description": "string",
        "type": "credit or debit",
        "amount": number,
        "balance": number
      }
    ]
  }
}`;
            
            default:
                return baseInstruction + `
Extract key information and return in this format:

{
  "document_type": "general",
  "confidence_score": 0-100,
  "extracted_data": {
    "summary": "string",
    "key_entities": [
      {
        "type": "string (e.g., Person, Organization, Date, Amount)",
        "value": "string"
      }
    ]
  }
}`;
        }
    }
    
    /**
     * 將文件轉換為 Base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]); // 只取 Base64 部分
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.HybridOCRDeepSeekProcessor = HybridOCRDeepSeekProcessor;
    console.log('✅ HybridOCRDeepSeekProcessor 已載入');
}

