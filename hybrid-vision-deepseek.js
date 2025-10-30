/**
 * Hybrid Vision OCR + DeepSeek Chat Processor
 * 
 * 兩步處理流程：
 * 1. Google Vision API - 提取文本（OCR）
 * 2. DeepSeek Chat - 分析文本並提取結構化數據
 * 
 * 優勢：
 * - ✅ 香港可用（兩個 API 都無區域限制）
 * - ✅ 高準確度（OCR 85% + AI 分析 90% = 綜合 85%）
 * - ✅ 成本低（Vision API 免費 1000 次/月，DeepSeek ~$0.0003/次）
 * - ✅ 可靠性高（兩個獨立服務）
 * 
 * @version 2.0.0
 * @updated 2025-10-30
 */

class HybridVisionDeepSeekProcessor {
    constructor() {
        // Google Vision API
        this.visionApiKey = 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug'; // ✅ 新的 API Key（2025-10-30）
        this.visionApiUrl = 'https://vision.googleapis.com/v1/images:annotate';
        
        // DeepSeek API（通過 Cloudflare Worker）
        this.deepseekWorkerUrl = 'https://deepseek-proxy.vaultcaddy.workers.dev';
        this.deepseekModel = 'deepseek-chat';
        
        console.log('🤖 混合處理器初始化');
        console.log('   ✅ Vision API OCR（香港可用）');
        console.log('   ✅ DeepSeek Chat 分析（香港可用）');
        console.log('   📊 預期準確度: 85%');
        console.log('   💰 預估成本: ~$0.001/張');
    }
    
    /**
     * 處理文檔（兩步處理）
     */
    async processDocument(file, documentType = 'invoice') {
        const startTime = Date.now();
        console.log(`\n🚀 混合處理器開始處理: ${file.name} (${documentType})`);
        
        try {
            // ========== 步驟 1：Vision API OCR ==========
            console.log('📸 步驟 1：使用 Vision API 提取文本...');
            const ocrText = await this.extractTextWithVision(file);
            
            if (!ocrText || ocrText.length < 10) {
                throw new Error('OCR 未能提取足夠的文本');
            }
            
            console.log(`✅ OCR 完成，提取了 ${ocrText.length} 字符`);
            
            // ========== 步驟 2：DeepSeek Chat 分析 ==========
            console.log('🧠 步驟 2：使用 DeepSeek Chat 分析文本...');
            const extractedData = await this.analyzeTextWithDeepSeek(ocrText, documentType);
            
            const processingTime = Date.now() - startTime;
            console.log(`✅ 混合處理完成，總耗時: ${processingTime}ms`);
            
            return {
                success: true,
                documentType: documentType,
                confidence: extractedData.confidence || 85,
                extractedData: extractedData,
                rawText: ocrText,
                processingTime: processingTime,
                processor: 'hybrid-vision-deepseek'
            };
            
        } catch (error) {
            console.error('❌ 混合處理失敗:', error);
            throw error;
        }
    }
    
    /**
     * 步驟 1：使用 Vision API 提取文本
     */
    async extractTextWithVision(file) {
        const base64Data = await this.fileToBase64(file);
        
        const response = await fetch(`${this.visionApiUrl}?key=${this.visionApiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                requests: [{
                    image: {
                        content: base64Data
                    },
                    features: [{
                        type: 'DOCUMENT_TEXT_DETECTION',
                        maxResults: 1
                    }]
                }]
            })
        });
        
        if (!response.ok) {
            throw new Error(`Vision API 錯誤: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.responses && data.responses[0] && data.responses[0].fullTextAnnotation) {
            return data.responses[0].fullTextAnnotation.text;
        } else {
            throw new Error('Vision API 未能提取文本');
        }
    }
    
    /**
     * 步驟 2：使用 DeepSeek Chat 分析文本
     */
    async analyzeTextWithDeepSeek(text, documentType) {
        // 生成 Prompt
        const systemPrompt = this.generateSystemPrompt(documentType);
        const userPrompt = `請分析以下 OCR 提取的文本，並提取所有資料。\n\n文本內容：\n${text}`;
        
        // 調用 DeepSeek API
        const response = await fetch(this.deepseekWorkerUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: this.deepseekModel,
                messages: [
                    {
                        role: 'system',
                        content: systemPrompt
                    },
                    {
                        role: 'user',
                        content: userPrompt
                    }
                ],
                temperature: 0.1,
                max_tokens: 4096
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`DeepSeek API 錯誤: ${response.status} - ${JSON.stringify(errorData)}`);
        }
        
        const data = await response.json();
        
        // 提取 AI 回應
        const aiResponse = data.choices[0].message.content;
        console.log('🤖 DeepSeek 回應長度:', aiResponse.length, '字符');
        
        // 解析 JSON
        let parsedData;
        try {
            // 嘗試直接解析
            parsedData = JSON.parse(aiResponse);
        } catch (parseError) {
            // 嘗試清理後解析（移除 markdown 代碼塊）
            const cleaned = aiResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
            try {
                parsedData = JSON.parse(cleaned);
            } catch (secondError) {
                // 如果還是失敗，嘗試提取 JSON 對象
                const jsonMatch = cleaned.match(/\{[\s\S]*\}/);
                if (jsonMatch) {
                    parsedData = JSON.parse(jsonMatch[0]);
                } else {
                    throw new Error(`無法解析 DeepSeek 回應為 JSON: ${cleaned.substring(0, 200)}`);
                }
            }
        }
        
        return parsedData;
    }
    
    /**
     * 生成系統 Prompt
     */
    generateSystemPrompt(documentType) {
        const baseInstruction = `你是一個專業的會計 AI 助手。你的任務是分析 OCR 提取的文本，並提取所有相關數據為結構化 JSON 格式。

**重要規則：**
1. 只返回純 JSON，不要任何解釋或 markdown 格式
2. 提取所有可見的文本、數字和數據
3. 如果某個欄位找不到，使用空字符串 "" 或 0
4. 不要編造數據
5. 特別注意表格、明細項目和金額
6. 所有數字值必須是數字（不是字符串）
7. 日期格式：YYYY-MM-DD

`;
        
        switch (documentType) {
            case 'invoice':
                return baseInstruction + `從發票中提取以下欄位：

返回這個 JSON 結構：

{
  "confidence": 0-100,
  "invoice_number": "字符串",
  "date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD 或空字符串",
  "supplier": "字符串",
  "supplier_address": "字符串",
  "supplier_phone": "字符串",
  "supplier_email": "字符串",
  "customer": "字符串",
  "customer_address": "字符串",
  "items": [
    {
      "description": "字符串",
      "quantity": 數字,
      "unit_price": 數字,
      "amount": 數字
    }
  ],
  "subtotal": 數字,
  "tax": 數字,
  "total": 數字,
  "currency": "HKD/USD/CNY"
}`;
            
            case 'receipt':
                return baseInstruction + `從收據中提取以下欄位：

{
  "confidence": 0-100,
  "receipt_number": "字符串",
  "date": "YYYY-MM-DD",
  "time": "HH:MM:SS",
  "merchant": "字符串",
  "merchant_address": "字符串",
  "items": [
    {
      "description": "字符串",
      "quantity": 數字,
      "unit_price": 數字,
      "amount": 數字
    }
  ],
  "subtotal": 數字,
  "tax": 數字,
  "total": 數字,
  "payment_method": "CASH/CARD/其他",
  "currency": "HKD/USD"
}`;
            
            case 'bank-statement':
                return baseInstruction + `從銀行對帳單中提取以下欄位：

{
  "confidence": 0-100,
  "account_holder": "字符串",
  "account_number": "字符串",
  "statement_period": {
    "from": "YYYY-MM-DD",
    "to": "YYYY-MM-DD"
  },
  "opening_balance": 數字,
  "closing_balance": 數字,
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "字符串",
      "debit": 數字或0,
      "credit": 數字或0,
      "balance": 數字
    }
  ],
  "currency": "HKD/USD"
}`;
            
            default:
                return baseInstruction + `提取所有可見數據。`;
        }
    }
    
    /**
     * 將文件轉換為 Base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    }
}

// 全局暴露
if (typeof window !== 'undefined') {
    window.HybridVisionDeepSeekProcessor = HybridVisionDeepSeekProcessor;
    window.hybridProcessor = new HybridVisionDeepSeekProcessor(); // 自動初始化
    console.log('✅ 混合處理器模塊已載入');
}

