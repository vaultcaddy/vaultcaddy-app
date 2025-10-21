/**
 * Gemini Worker Client
 * 通過 Cloudflare Worker 調用 Gemini API（繞過 CORS）
 */

class GeminiWorkerClient {
    constructor(workerUrl) {
        // Cloudflare Worker URL
        this.workerUrl = workerUrl || 'https://gemini-proxy.vaultcaddy.workers.dev/v1beta/models/gemini-1.5-flash-latest:generateContent';
        this.maxRetries = 3;
        this.retryDelay = 2000; // 2 seconds
        
        console.log('🤖 Gemini Worker Client 初始化');
        console.log('   Worker URL:', this.workerUrl);
    }
    
    /**
     * 處理文檔（主方法）
     */
    async processDocument(file, documentType = 'invoice') {
        const startTime = Date.now();
        
        console.log(`🚀 開始處理文檔: ${file.name} (${documentType})`);
        console.log(`   文件大小: ${file.size} bytes`);
        
        try {
            // 驗證文件
            this.validateFile(file);
            
            // 將文件轉換為 base64
            const base64Data = await this.fileToBase64(file);
            
            // 生成提示詞
            const prompt = this.generatePrompt(documentType);
            
            // 調用 Gemini API（通過 Worker）
            const result = await this.callGeminiViaWorker(base64Data, file.type, prompt);
            
            const processingTime = Date.now() - startTime;
            console.log(`✅ 處理完成，耗時: ${processingTime}ms`);
            
            return {
                success: true,
                data: result,
                processingTime: processingTime,
                engine: 'gemini-via-worker'
            };
            
        } catch (error) {
            console.error('❌ 處理失敗:', error);
            return {
                success: false,
                error: error.message,
                processingTime: Date.now() - startTime,
                engine: 'gemini-via-worker'
            };
        }
    }
    
    /**
     * 通過 Worker 調用 Gemini API
     */
    async callGeminiViaWorker(base64Data, mimeType, prompt) {
        let lastError = null;
        
        for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
            try {
                console.log(`🔄 嘗試 ${attempt}/${this.maxRetries}...`);
                
                // 構建請求體
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
                        temperature: 0.1,  // 低溫度 = 更準確、更一致的輸出
                        topK: 40,
                        topP: 0.95,
                        maxOutputTokens: 4096,  // 增加到 4096 以支持更多商品項目
                    }
                };
                
                // 調用 Worker
                const response = await fetch(this.workerUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody)
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(`Worker 響應錯誤: ${response.status} - ${JSON.stringify(errorData)}`);
                }
                
                const data = await response.json();
                
                // 解析 Gemini 響應
                const extractedData = this.parseGeminiResponse(data);
                
                return extractedData;
                
            } catch (error) {
                console.warn(`⚠️ 嘗試 ${attempt} 失敗:`, error.message);
                lastError = error;
                
                if (attempt < this.maxRetries) {
                    console.log(`   等待 ${this.retryDelay}ms 後重試...`);
                    await new Promise(resolve => setTimeout(resolve, this.retryDelay));
                }
            }
        }
        
        throw new Error(`所有重試失敗: ${lastError.message}`);
    }
    
    /**
     * 解析 Gemini 響應
     */
    parseGeminiResponse(response) {
        try {
            // Gemini 響應格式：
            // { candidates: [{ content: { parts: [{ text: "..." }] } }] }
            
            if (!response.candidates || response.candidates.length === 0) {
                throw new Error('Gemini 響應格式無效：沒有 candidates');
            }
            
            const candidate = response.candidates[0];
            const text = candidate.content?.parts?.[0]?.text;
            
            if (!text) {
                throw new Error('Gemini 響應格式無效：沒有文本內容');
            }
            
            console.log('📝 Gemini 返回的文本長度:', text.length);
            
            // 嘗試解析 JSON
            let jsonData;
            
            // 移除 markdown 代碼塊標記（如果有）
            const cleanedText = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
            
            try {
                jsonData = JSON.parse(cleanedText);
            } catch (e) {
                console.warn('⚠️ JSON 解析失敗，嘗試提取 JSON 部分...');
                
                // 嘗試從文本中提取 JSON
                const jsonMatch = cleanedText.match(/\{[\s\S]*\}/);
                if (jsonMatch) {
                    jsonData = JSON.parse(jsonMatch[0]);
                } else {
                    throw new Error('無法從 Gemini 響應中提取 JSON 數據');
                }
            }
            
            console.log('✅ JSON 解析成功');
            return jsonData;
            
        } catch (error) {
            console.error('❌ 解析 Gemini 響應失敗:', error);
            throw new Error(`解析失敗: ${error.message}`);
        }
    }
    
    /**
     * 生成提示詞（根據文檔類型）
     */
    generatePrompt(documentType) {
        const prompts = {
            invoice: `你是一個專業的發票數據提取專家。請仔細分析這張發票圖片，並提取所有可見信息。

**重要提示**：
- 這是一張中文發票，可能包含繁體中文、簡體中文或英文
- 發票號碼通常在頂部，格式可能是：Invoice No.、發票編號、單號、No. 等
- 日期格式可能是：2025-10-01、2025/10/01、01/10/2025、2025年10月1日 等
- 商品項目通常在表格中，包含：品名、數量、單價、金額等列
- 小計、稅額、總額通常在底部
- 請提取**所有可見的商品項目**，不要只提取第一個

請以 JSON 格式返回，格式如下：

{
  "type": "invoice",
  "supplier": "供應商名稱（公司全名）",
  "invoice_number": "發票號碼（完整號碼）",
  "date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "customer": "客戶名稱（公司全名）",
  "subtotal": 1234.56,
  "tax": 123.45,
  "total": 1358.01,
  "currency": "HKD",
  "payment_method": "Cash",
  "payment_status": "Unpaid",
  "items": [
    {
      "description": "商品名稱/描述",
      "quantity": 10,
      "unit_price": 123.45,
      "amount": 1234.56
    }
  ]
}

**CRITICAL RULES**（必須遵守）：
1. ✅ 返回純 JSON，絕對不要包含 markdown 標記（如 \`\`\`json）
2. ✅ 所有金額必須是**純數字**（例如：1407.28，不要：HKD $1407.28、$1,407.28）
3. ✅ 日期必須轉換為 YYYY-MM-DD 格式（例如：2025-10-01）
4. ✅ 如果某個字段找不到，使用空字符串 "" 或 0（金額）
5. ✅ **必須提取所有可見的商品項目**（不要只提取第一個）
6. ✅ 仔細查看圖片中的所有文字，包括：
   - 頂部區域：發票號碼、日期
   - 中間表格：所有商品項目（逐行提取）
   - 底部區域：小計、稅額、總額
7. ✅ quantity 和 unit_price 必須是數字
8. ✅ 如果發票上有多個金額，總額通常是最大的那個
9. ✅ 小計 + 稅額 = 總額（請驗證數學關係）

**數據提取優先級**：
1. 總額 (total) - 最重要
2. 供應商名稱 (supplier) - 第二重要
3. 發票號碼 (invoice_number) - 第三重要
4. 日期 (date) - 第四重要
5. 商品項目 (items) - 必須提取所有
6. 客戶名稱 (customer)
7. 小計 (subtotal)、稅額 (tax)
8. 付款方式 (payment_method)

請開始分析！`,

            receipt: `你是一個專業的收據數據提取專家。請分析這張收據圖片，並提取以下信息：

請以 JSON 格式返回，格式如下：

{
  "type": "receipt",
  "merchant": "商家名稱",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "receipt_number": "收據號碼",
  "subtotal": "小計金額（數字）",
  "tax": "稅額（數字）",
  "tip": "小費（數字）",
  "total": "總金額（數字）",
  "currency": "HKD",
  "payment_method": "付款方式",
  "items": [
    {
      "description": "商品描述",
      "quantity": "數量",
      "amount": "金額"
    }
  ]
}

CRITICAL RULES:
1. 返回純 JSON，不要包含任何 markdown 標記
2. 所有金額必須是數字（不要包含貨幣符號或逗號）
3. 如果某個字段找不到，使用空字符串 ""`,

            bank_statement: `你是一個專業的銀行對帳單數據提取專家。請分析這張銀行對帳單圖片，並提取以下信息：

請以 JSON 格式返回，格式如下：

{
  "type": "bank_statement",
  "bank_name": "銀行名稱",
  "account_holder": "帳戶持有人",
  "account_number": "帳戶號碼（後4位）",
  "statement_period_start": "YYYY-MM-DD",
  "statement_period_end": "YYYY-MM-DD",
  "opening_balance": "期初餘額（數字）",
  "closing_balance": "期末餘額（數字）",
  "currency": "HKD",
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "交易描述",
      "amount": "金額（正數為收入，負數為支出）",
      "balance": "餘額"
    }
  ]
}

CRITICAL RULES:
1. 返回純 JSON，不要包含任何 markdown 標記
2. 所有金額必須是數字
3. 交易金額：收入為正數，支出為負數
4. 提取所有可見的交易記錄`
        };
        
        return prompts[documentType] || prompts.invoice;
    }
    
    /**
     * 驗證文件
     */
    validateFile(file) {
        const maxSize = 20 * 1024 * 1024; // 20MB
        const supportedTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
        
        if (file.size > maxSize) {
            throw new Error(`文件太大：${(file.size / 1024 / 1024).toFixed(2)}MB（最大 20MB）`);
        }
        
        if (!supportedTypes.includes(file.type)) {
            throw new Error(`不支持的文件類型：${file.type}`);
        }
    }
    
    /**
     * 文件轉 base64
     */
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = () => {
                const result = reader.result.toString();
                const base64 = result.split(',')[1]; // 移除 data:mime/type;base64, 前綴
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
window.GeminiWorkerClient = GeminiWorkerClient;

console.log('🤖 Gemini Worker Client 模塊已載入');

