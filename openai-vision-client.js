/**
 * OpenAI GPT-4 Vision 客戶端
 * 用於處理文檔圖片的 AI 數據提取
 */

class OpenAIVisionClient {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.apiEndpoint = 'https://api.openai.com/v1/chat/completions';
        this.model = 'gpt-4-vision-preview'; // GPT-4 Vision 模型
        this.maxRetries = 3;
        this.retryDelay = 2000; // 2 seconds
        
        console.log('🤖 OpenAI Vision Client 初始化');
        console.log('   ✅ Model:', this.model);
    }

    /**
     * 生成文檔提取提示詞
     */
    generatePrompt(documentType) {
        const prompts = {
            invoice: `你是一個專業的發票數據提取專家。請仔細分析這張發票圖片，並提取以下信息：

**CRITICAL RULES:**
1. 提取 **所有** 行項目（line items），不要遺漏任何一項
2. 確保 subtotal + tax = total（數學驗證）
3. 如果找不到某個字段，使用 null，不要猜測
4. 所有金額必須是數字，不要包含貨幣符號
5. 日期格式：YYYY-MM-DD
6. 返回純 JSON，不要包含任何其他文字

**必須提取的字段：**
{
  "invoice_number": "發票號碼",
  "invoice_date": "發票日期 (YYYY-MM-DD)",
  "due_date": "到期日期 (YYYY-MM-DD)",
  "supplier": {
    "name": "供應商名稱",
    "address": "供應商地址",
    "phone": "電話",
    "email": "電子郵件"
  },
  "customer": {
    "name": "客戶名稱",
    "address": "客戶地址",
    "phone": "電話",
    "email": "電子郵件"
  },
  "items": [
    {
      "description": "商品描述",
      "quantity": 數量,
      "unit_price": 單價,
      "amount": 金額
    }
  ],
  "subtotal": 小計,
  "tax": 稅額,
  "total": 總額,
  "payment_method": "付款方式",
  "notes": "備註"
}

**重要提示：**
- 提取 **所有** 行項目，不要遺漏
- 確保數學計算正確：subtotal + tax = total
- 所有金額必須是數字（不要包含 $, HKD 等符號）
- 如果找不到某個字段，使用 null

請返回純 JSON 格式的數據。`,

            receipt: `你是一個專業的收據數據提取專家。請仔細分析這張收據圖片，並提取以下信息：

**CRITICAL RULES:**
1. 提取 **所有** 商品項目，不要遺漏任何一項
2. 確保 subtotal + tax = total（數學驗證）
3. 如果找不到某個字段，使用 null，不要猜測
4. 所有金額必須是數字，不要包含貨幣符號
5. 日期格式：YYYY-MM-DD
6. 返回純 JSON，不要包含任何其他文字

**必須提取的字段：**
{
  "receipt_number": "收據號碼",
  "date": "日期 (YYYY-MM-DD)",
  "time": "時間 (HH:MM)",
  "merchant": {
    "name": "商家名稱",
    "address": "商家地址",
    "phone": "電話"
  },
  "items": [
    {
      "description": "商品描述",
      "quantity": 數量,
      "unit_price": 單價,
      "amount": 金額
    }
  ],
  "subtotal": 小計,
  "tax": 稅額,
  "total": 總額,
  "payment_method": "付款方式",
  "card_last4": "卡號後4位"
}

請返回純 JSON 格式的數據。`,

            'bank-statement': `你是一個專業的銀行對帳單數據提取專家。請仔細分析這張銀行對帳單圖片，並提取以下信息：

**CRITICAL RULES:**
1. 提取 **所有** 交易記錄，不要遺漏任何一項
2. 確保 opening_balance + total_deposits - total_withdrawals = closing_balance
3. 如果找不到某個字段，使用 null，不要猜測
4. 所有金額必須是數字，不要包含貨幣符號
5. 日期格式：YYYY-MM-DD
6. 返回純 JSON，不要包含任何其他文字

**必須提取的字段：**
{
  "bank_name": "銀行名稱",
  "account_holder": "帳戶持有人",
  "account_number": "帳戶號碼",
  "statement_period": {
    "from": "起始日期 (YYYY-MM-DD)",
    "to": "結束日期 (YYYY-MM-DD)"
  },
  "opening_balance": 期初餘額,
  "closing_balance": 期末餘額,
  "transactions": [
    {
      "date": "交易日期 (YYYY-MM-DD)",
      "description": "交易描述",
      "amount": 金額,
      "type": "debit 或 credit",
      "balance": 餘額
    }
  ],
  "total_deposits": 總存款,
  "total_withdrawals": 總取款
}

請返回純 JSON 格式的數據。`,

            general: `你是一個專業的文檔數據提取專家。請仔細分析這張文檔圖片，並提取以下信息：

**CRITICAL RULES:**
1. 提取文檔中的所有關鍵信息
2. 如果找不到某個字段，使用 null，不要猜測
3. 返回純 JSON，不要包含任何其他文字

**必須提取的字段：**
{
  "document_type": "文檔類型",
  "document_number": "文檔編號",
  "date": "日期 (YYYY-MM-DD)",
  "parties": [
    {
      "name": "相關方名稱",
      "role": "角色（例如：發送方、接收方）",
      "contact": "聯繫方式"
    }
  ],
  "key_information": {
    "field1": "值1",
    "field2": "值2"
  },
  "notes": "備註"
}

請返回純 JSON 格式的數據。`
        };

        return prompts[documentType] || prompts.general;
    }

    /**
     * 將圖片轉換為 Base64
     */
    async imageToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                // 移除 data:image/...;base64, 前綴
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    /**
     * 處理文檔圖片
     */
    async processDocument(file, documentType = 'invoice') {
        console.log('🔄 OpenAI Vision 開始處理文檔...');
        console.log('   文檔類型:', documentType);
        console.log('   文件名:', file.name);

        try {
            // 將圖片轉換為 Base64
            const base64Image = await this.imageToBase64(file);
            console.log('   ✅ 圖片已轉換為 Base64');

            // 生成提示詞
            const prompt = this.generatePrompt(documentType);

            // 構建請求
            const requestBody = {
                model: this.model,
                messages: [
                    {
                        role: 'user',
                        content: [
                            {
                                type: 'text',
                                text: prompt
                            },
                            {
                                type: 'image_url',
                                image_url: {
                                    url: `data:image/jpeg;base64,${base64Image}`,
                                    detail: 'high' // 高解析度分析
                                }
                            }
                        ]
                    }
                ],
                max_tokens: 4096,
                temperature: 0.1 // 低溫度，確保輸出穩定
            };

            // 發送請求
            const response = await this.sendRequest(requestBody);

            console.log('   ✅ OpenAI Vision 處理完成');
            return response;

        } catch (error) {
            console.error('   ❌ OpenAI Vision 處理失敗:', error);
            throw error;
        }
    }

    /**
     * 發送請求到 OpenAI API
     */
    async sendRequest(requestBody, retryCount = 0) {
        try {
            console.log(`   📤 發送請求到 OpenAI API (嘗試 ${retryCount + 1}/${this.maxRetries})`);

            const response = await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.apiKey}`
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`OpenAI API 錯誤: ${errorData.error?.message || response.statusText}`);
            }

            const data = await response.json();
            
            // 提取 AI 返回的內容
            const content = data.choices[0].message.content;
            console.log('   📥 收到 OpenAI 響應');

            // 解析 JSON
            const jsonMatch = content.match(/\{[\s\S]*\}/);
            if (!jsonMatch) {
                throw new Error('無法從 AI 響應中提取 JSON 數據');
            }

            const extractedData = JSON.parse(jsonMatch[0]);
            console.log('   ✅ 數據提取成功');

            return {
                success: true,
                data: extractedData,
                rawResponse: content
            };

        } catch (error) {
            console.error(`   ❌ 請求失敗 (嘗試 ${retryCount + 1}/${this.maxRetries}):`, error);

            // 重試邏輯
            if (retryCount < this.maxRetries - 1) {
                console.log(`   ⏳ ${this.retryDelay / 1000} 秒後重試...`);
                await new Promise(resolve => setTimeout(resolve, this.retryDelay));
                return this.sendRequest(requestBody, retryCount + 1);
            }

            throw error;
        }
    }
}

// 將類別暴露到全局作用域
window.OpenAIVisionClient = OpenAIVisionClient;

console.log('✅ OpenAI Vision Client 已載入');

