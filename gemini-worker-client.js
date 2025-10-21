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
            invoice: `你是一個專業的發票數據提取專家。請**逐字逐句**仔細分析這張發票圖片，提取所有可見信息。

🔍 **第一步：識別發票結構**
1. 查看**最頂部**：找到發票號碼（通常在左上角或右上角）
   - 格式可能是：FI25093602、INV-001、No.12345 等
2. 查看**公司信息區域**：
   - 供應商名稱（通常在左上角，公司 Logo 附近）
   - 客戶名稱（通常在中間或右側，標註為 CUSTOMER、客戶、收件人 等）
3. 查看**日期信息**：
   - 發票日期：DATE、日期、2025年10月1日、2025-10-17 等
   - 到期日：DUE DATE、到期日 等

🔍 **第二步：提取表格數據**（最重要！）
表格通常有以下列（從左到右）：
- CODE NO / 代碼
- DESCRIPTION / 品名 / 描述
- QTY / 數量
- UNIT PRICE / 單價
- DS % / 折扣
- AMOUNT / 金額

**重要**：
- ✅ 請**逐行**閱讀表格，提取**每一行**的商品信息
- ✅ 不要跳過任何一行
- ✅ 即使有些文字被遮擋（如 CREDIT 標記），也要提取可見部分
- ✅ 商品描述可能很長（如：Premium Thai Hom Mali Rice (Golden Phoenix) 2...）

🔍 **第三步：提取金額信息**（在底部）
- 查找：SUBTOTAL、小計、NET TOTALS
- 查找：TAX、稅額、GST
- 查找：TOTAL、總計、合計

---

📋 **JSON 格式要求**：

{
  "type": "invoice",
  "supplier": "供應商完整名稱",
  "invoice_number": "完整發票號碼",
  "date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "customer": "客戶完整名稱",
  "subtotal": 1234.56,
  "tax": 0,
  "total": 1234.56,
  "currency": "HKD",
  "payment_method": "",
  "payment_status": "Unpaid",
  "items": [
    {
      "code": "H01-7",
      "description": "Rice Noodles (Ann Moon) 14KG",
      "quantity": 1,
      "unit_price": 54.00,
      "discount_percent": 0,
      "amount": 54.00
    },
    {
      "code": "C001",
      "description": "Korean Granulated White Sugar 30kg",
      "quantity": 1,
      "unit_price": 198.00,
      "discount_percent": 0,
      "amount": 198.00
    }
  ]
}

---

⚠️ **CRITICAL RULES**（必須嚴格遵守）：

1. ✅ **返回純 JSON**：不要包含 \`\`\`json 或任何 markdown 標記
2. ✅ **所有金額必須是純數字**：
   - ✅ 正確：1407.28
   - ❌ 錯誤：HKD $1407.28、$1,407.28、1407
3. ✅ **日期格式統一為 YYYY-MM-DD**：
   - ✅ 正確：2025-10-17
   - ❌ 錯誤：2025年10月17日、17/10/2025
4. ✅ **提取所有表格行**：
   - 如果表格有 5 行商品，items 數組必須有 5 個對象
   - 不要只提取第一行！
5. ✅ **商品描述要完整**：
   - ✅ 正確："Premium Thai Hom Mali Rice (Golden Phoenix) 25KG"
   - ❌ 錯誤："AMOUNT"、"Rice"
6. ✅ **quantity 和 unit_price 必須是數字**：
   - ✅ 正確：1、2.0、54.00
   - ❌ 錯誤："1件"、"54元"
7. ✅ **如果字段找不到**：
   - 文字字段：使用 ""
   - 金額字段：使用 0
8. ✅ **驗證數學關係**：
   - 每行：quantity × unit_price = amount
   - 總額：所有 amount 相加 ≈ total

---

🎯 **提取優先級**：
1. 🥇 **total**（總額）- 最重要
2. 🥈 **items**（商品列表）- 必須全部提取
3. 🥉 **invoice_number**（發票號碼）
4. **supplier**（供應商）
5. **date**（日期）
6. **customer**（客戶）
7. **subtotal**、**tax**

---

現在請開始逐字分析這張發票！`,

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

