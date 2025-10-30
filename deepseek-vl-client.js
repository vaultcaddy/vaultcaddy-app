/**
 * DeepSeek-VL Vision Client
 * 
 * 使用 Hugging Face Inference API 調用 DeepSeek-VL-7B-chat
 * 
 * 優勢：
 * - 真正的視覺理解（開源視覺語言模型）
 * - 在香港可用（Hugging Face 無區域限制）
 * - 成本低（~$0.001-0.002/張）
 * - 無需本地 GPU
 * 
 * 預期準確度：85-90%
 * 
 * @version 1.0.0
 * @updated 2025-10-28
 */

class DeepSeekVLClient {
    constructor() {
        // ✅ 使用 Cloudflare Worker 保護 Token
        // 🔄 使用 huggingface-proxy Worker
        this.workerUrl = 'https://huggingface-proxy.vaultcaddy.workers.dev';
        this.modelId = 'deepseek-ai/deepseek-vl-7b-chat';
        
        this.maxRetries = 3;
        this.retryDelay = 2000;
        
        console.log('🤖 DeepSeek-VL Client 初始化');
        console.log('   ✅ 模型:', this.modelId);
        console.log('   ✅ Worker URL:', this.workerUrl);
        console.log('   ✅ 支持格式: JPG, PNG');
        console.log('   💰 預估成本: ~$0.001-0.002/張');
        console.log('   🌏 香港可用: ✅');
        console.log('   🔒 Token 安全: 通過 Cloudflare Worker 保護');
    }
    
    /**
     * 處理文檔（圖片）
     */
    async processDocument(file, documentType = 'invoice') {
        const startTime = Date.now();
        console.log(`\n🚀 DeepSeek-VL 開始處理: ${file.name} (${documentType})`);
        
        try {
            // 1. 將文件轉換為 base64
            const base64Data = await this.fileToBase64(file);
            
            console.log('📸 文件信息:');
            console.log(`   類型: ${file.type}`);
            console.log(`   大小: ${(file.size / 1024).toFixed(2)} KB`);
            
            // 2. 生成 Prompt
            const prompt = this.generatePrompt(documentType);
            
            // 3. 構建請求（使用 Hugging Face 的標準格式）
            // DeepSeek-VL 使用 visual-question-answering 格式
            const requestBody = {
                model: this.modelId,  // 告訴 Worker 使用哪個模型
                inputs: {
                    image: `data:${file.type};base64,${base64Data}`,
                    question: prompt
                },
                parameters: {
                    max_length: 2048,
                    temperature: 0.1,
                    top_p: 0.9
                }
            };
            
            // 4. 調用 Cloudflare Worker（Worker 會調用 Hugging Face API）
            console.log('📤 發送請求到 Cloudflare Worker...');
            const response = await fetch(this.workerUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                
                // 如果模型正在加載，等待後重試
                if (response.status === 503 && errorData.error?.includes('loading')) {
                    const estimatedTime = errorData.estimated_time || 20;
                    console.log(`⏳ 模型正在加載，預計 ${estimatedTime} 秒後可用...`);
                    await this.sleep(estimatedTime * 1000);
                    return this.processDocument(file, documentType); // 重試
                }
                
                throw new Error(`Hugging Face API 錯誤: ${response.status} - ${errorData.error || JSON.stringify(errorData)}`);
            }
            
            const data = await response.json();
            console.log('📥 收到 DeepSeek-VL 響應');
            
            // 5. 解析響應
            let responseText;
            if (Array.isArray(data)) {
                responseText = data[0].generated_text || data[0].text;
            } else if (data.generated_text) {
                responseText = data.generated_text;
            } else {
                responseText = JSON.stringify(data);
            }
            
            console.log('📄 響應長度:', responseText.length, '字符');
            
            // 6. 解析 JSON
            let extractedData;
            try {
                // 嘗試直接解析
                extractedData = JSON.parse(responseText);
            } catch (parseError) {
                // 嘗試清理後解析（移除 markdown 代碼塊）
                const cleaned = responseText.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
                extractedData = JSON.parse(cleaned);
            }
            
            const processingTime = Date.now() - startTime;
            console.log(`✅ DeepSeek-VL 處理完成，耗時: ${processingTime}ms`);
            
            return {
                success: true,
                documentType: extractedData.document_type || documentType,
                confidence: extractedData.confidence_score || 85,
                extractedData: extractedData.extracted_data,
                processingTime: processingTime,
                processor: 'deepseek-vl'
            };
            
        } catch (error) {
            console.error('❌ DeepSeek-VL 處理失敗:', error);
            throw error;
        }
    }
    
    /**
     * 生成 Prompt（與 Claude 類似）
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

Return this exact JSON structure:

{
  "document_type": "invoice",
  "confidence_score": 0-100,
  "extracted_data": {
    "invoice_number": "string",
    "date": "YYYY-MM-DD",
    "due_date": "YYYY-MM-DD or empty string",
    "supplier": "string",
    "supplier_address": "string",
    "supplier_phone": "string",
    "supplier_email": "string",
    "customer": "string",
    "customer_address": "string",
    "customer_phone": "string",
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
}
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
     * 睡眠函數
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.DeepSeekVLClient = DeepSeekVLClient;
    window.deepseekVLClient = new DeepSeekVLClient();
    console.log('✅ DeepSeek-VL Client 模塊已載入');
}

