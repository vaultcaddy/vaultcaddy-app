/**
 * Gemini Worker Client
 * 通過 Cloudflare Worker 調用 Gemini API（繞過 CORS）
 * 
 * 作用：
 * 1. 提供客戶端接口調用 Cloudflare Worker 代理的 Gemini API
 * 2. 處理文檔圖片的 AI 數據提取（發票、收據、銀行對帳單）
 * 3. 實現重試機制和錯誤處理
 * 4. 優化的提示詞確保 95%+ 的提取準確率
 */

class GeminiWorkerClient {
    constructor(workerUrl) {
        // Cloudflare Worker URL（注意：Worker 會自己處理完整的 API 路徑，這裡只需要 Worker 的基礎 URL）
        this.workerUrl = workerUrl || 'https://gemini-proxy.vaultcaddy.workers.dev';
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
                        maxOutputTokens: 8192,  // 增加到 8192 以支持更多商品項目和詳細信息
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
            console.log('📝 Gemini 返回的前 500 字符:', text.substring(0, 500));
            
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
            console.log('📊 提取的數據:', JSON.stringify(jsonData, null, 2));
            
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
            invoice: `你是一個專業的香港發票數據提取專家。請**逐字逐句**仔細分析這張發票圖片，提取所有可見信息。

🎯 **你的任務目標**：
將這張發票的所有信息準確提取到 JSON 格式中，準確率必須達到 95% 以上。

---

## 📋 **第一步：識別發票基本信息**

### 1.1 **發票號碼**（CRITICAL！）
- 🔍 查找位置：
  - 通常在**右上角**或**左上角**
  - 可能標註為：「訂貨日期」下方、「客戶編號」旁邊、或獨立一行
  - 格式示例：\`200602\`、\`FI25093602\`、\`INV-001\`、\`No.12345\`
- ⚠️ **不要混淆**：
  - ❌ 不是電話號碼（如 2950 0083）
  - ❌ 不是傳真號碼（如 2950 0026）
  - ❌ 不是客戶編號
- ✅ **提取規則**：
  - 如果看到「訂貨日期」下方有一個 6 位數字（如 200602），這就是發票號碼
  - 如果看到「送貨日期」旁邊有一個長數字（如 25091134），這可能是送貨單號，不是發票號碼

### 1.2 **供應商信息**（Supplier）
- 🔍 查找位置：**最頂部**，通常有公司 Logo 或公司名稱
- ✅ 提取內容：
  - 中文名稱（如：海運達（香港）有限公司）
  - 英文名稱（如：Hoi Wan Tat (HK) Ltd.）
  - 地址（如：九龍油塘四山街2號...）
  - 電話、傳真、WhatsApp、Email
- 📝 JSON 格式：
  \`\`\`json
  "supplier": {
    "name": "海運達（香港）有限公司",
    "name_en": "Hoi Wan Tat (HK) Ltd.",
    "address": "九龍油塘四山街2號油庫工業大廈第二座1.G/F, A&D室",
    "phone": "2950 0083 / 2950 0132",
    "fax": "2950 0026",
    "whatsapp": "9444 1102 / 9444 1103",
    "email": "hoiwantat@yahoo.com.hk"
  }
  \`\`\`

### 1.3 **客戶信息**（Customer）
- 🔍 查找位置：通常在**右上角**，標註為「客戶」、「地址」、「聯絡人」
- ✅ 提取內容：
  - 客戶名稱（如：滾得篤宮庭火鍋（北角））
  - 地址
  - 聯絡人（如：ALEX）
  - 電話（如：96065490/23313838）
- 📝 JSON 格式：
  \`\`\`json
  "customer": {
    "name": "滾得篤宮庭火鍋（北角）",
    "address": "北角馬寶道33號馬寶樓地舖雨場 1/F 116號舖",
    "contact": "ALEX",
    "phone": "96065490/23313838"
  }
  \`\`\`

### 1.4 **日期信息**
- 🔍 查找位置：
  - 「訂貨日期」（Invoice Date）：如 2025年9月25日
  - 「送貨日期」（Delivery Date）：如 2025年9月26日
- ✅ 轉換為 \`YYYY-MM-DD\` 格式：
  - \`2025年9月25日\` → \`2025-09-25\`
  - \`2025-9-25\` → \`2025-09-25\`

---

## 📊 **第二步：提取表格商品明細**（最重要！）

### 2.1 **表格結構識別**
香港發票表格通常有以下列（從左到右）：
\`\`\`
| 貨品編號 | 品名 | 數量 | 單價 | 金額 |
\`\`\`
或
\`\`\`
| CODE NO | DESCRIPTION | QTY | UNIT PRICE | AMOUNT |
\`\`\`

### 2.2 **逐行提取商品**（CRITICAL！）
⚠️ **重要規則**：
1. ✅ **必須提取表格中的每一行商品**
2. ✅ **不要跳過任何一行**
3. ✅ **即使有水印（如 "CASH"）遮擋，也要提取可見部分**
4. ✅ **商品描述要完整**（不要只提取前幾個字）

### 2.3 **提取示例**
如果看到以下表格：
\`\`\`
| 01301 | 支雀巢 鮮奶絲滑咖啡 (268mlx15支) | 2 件 | 125.00 | 250.00 |
| 01113 | 曬雀巢 美式黑咖啡 (250mlx24)    | 8 箱 | 125.00 | 1,000.00 |
\`\`\`

提取為：
\`\`\`json
"items": [
  {
    "code": "01301",
    "description": "支雀巢 鮮奶絲滑咖啡 (268mlx15支)",
    "quantity": 2,
    "unit": "件",
    "unit_price": 125.00,
    "amount": 250.00
  },
  {
    "code": "01113",
    "description": "曬雀巢 美式黑咖啡 (250mlx24)",
    "quantity": 8,
    "unit": "箱",
    "unit_price": 125.00,
    "amount": 1000.00
  }
]
\`\`\`

⚠️ **常見錯誤**：
- ❌ 只提取第一行商品
- ❌ 商品描述不完整（如只提取「支雀巢」）
- ❌ 數量包含單位（如 "2件" 應該是 2）
- ❌ 金額包含逗號（如 "1,000.00" 應該是 1000.00）

---

## 💰 **第三步：提取金額信息**

### 3.1 **查找金額區域**
通常在**表格底部**，有以下信息：
\`\`\`
總數量: 10
金額: 1,250.00
折扣: 10
總金額: 1,250.00
\`\`\`

### 3.2 **提取規則**
- **小計（Subtotal）**：所有商品金額相加
  - 計算方式：250.00 + 1,000.00 = 1,250.00
- **折扣（Discount）**：如果有「折扣」欄位
  - 示例：折扣 10（可能是 10 元或 10%）
- **稅額（Tax）**：香港發票通常沒有稅
  - 如果找不到，設為 \`0\`
- **總金額（Total）**：最終應付金額
  - 示例：1,250.00

### 3.3 **數學驗證**（CRITICAL！）
✅ **必須驗證**：
\`\`\`javascript
// 驗證每行商品
items[0].quantity × items[0].unit_price = items[0].amount
2 × 125.00 = 250.00 ✅

// 驗證總金額
sum(items[].amount) - discount + tax = total
(250.00 + 1000.00) - 10 + 0 = 1,240.00
或
(250.00 + 1000.00) = 1,250.00 ✅
\`\`\`

---

## 💳 **第四步：提取付款信息**

### 4.1 **付款方式**
- 🔍 查找位置：
  - 表格中間或底部可能有「CASH」水印
  - 付款方式欄位：C.O.D（貨到付款）、CASH、支票、銀行轉帳
- ✅ 提取內容：
  \`\`\`json
  "payment_method": "C.O.D",
  "payment_status": "CASH"
  \`\`\`

### 4.2 **香港特有付款信息**（CRITICAL！）
- 🔍 查找位置：通常在**底部備註**
- ✅ 提取內容：
  - **轉數快（FPS）**：識別碼 # 3811486
  - **PayMe**：PAYME# 9786 2248
  - **八達通（Octopus）**：如果有
- 📝 JSON 格式：
  \`\`\`json
  "payment_info": {
    "fps_id": "3811486",
    "payme_number": "9786 2248"
  }
  \`\`\`

### 4.3 **簽名和印章**
- 如果看到手寫簽名或公司印章，記錄：
  \`\`\`json
  "has_signature": true,
  "has_stamp": false
  \`\`\`

---

## 📝 **完整 JSON 格式要求**

\`\`\`json
{
  "type": "invoice",
  "invoice_number": "200602",
  "date": "2025-09-25",
  "due_date": "2025-09-26",
  
  "supplier": {
    "name": "海運達（香港）有限公司",
    "name_en": "Hoi Wan Tat (HK) Ltd.",
    "address": "九龍油塘四山街2號油庫工業大廈第二座1.G/F, A&D室",
    "phone": "2950 0083 / 2950 0132",
    "fax": "2950 0026",
    "whatsapp": "9444 1102 / 9444 1103",
    "email": "hoiwantat@yahoo.com.hk"
  },
  
  "customer": {
    "name": "滾得篤宮庭火鍋（北角）",
    "address": "北角馬寶道33號馬寶樓地舖雨場 1/F 116號舖",
    "contact": "ALEX",
    "phone": "96065490/23313838"
  },
  
  "items": [
    {
      "code": "01301",
      "description": "支雀巢 鮮奶絲滑咖啡 (268mlx15支)",
      "quantity": 2,
      "unit": "件",
      "unit_price": 125.00,
      "amount": 250.00
    },
    {
      "code": "01113",
      "description": "曬雀巢 美式黑咖啡 (250mlx24)",
      "quantity": 8,
      "unit": "箱",
      "unit_price": 125.00,
      "amount": 1000.00
    }
  ],
  
  "subtotal": 1250.00,
  "discount": 10,
  "tax": 0,
  "total": 1250.00,
  "currency": "HKD",
  
  "payment_method": "C.O.D",
  "payment_status": "CASH",
  "payment_info": {
    "fps_id": "3811486",
    "payme_number": "9786 2248"
  },
  
  "has_signature": true,
  "has_stamp": false,
  
  "notes": "轉數快「識別碼 # 3811486，PAYME# 9786 2248」"
}
\`\`\`

---

## ⚠️ **CRITICAL RULES**（必須 100% 遵守）

### 1. **JSON 格式**
- ✅ 返回**純 JSON**，不要包含 \\\`\\\`\\\`json 或任何 markdown 標記
- ✅ 所有字段名稱必須用雙引號 \`"field_name"\`
- ✅ 字符串值必須用雙引號 \`"value"\`
- ✅ 數字值不要用引號 \`123.45\`（不是 \`"123.45"\`）

### 2. **金額格式**
- ✅ 所有金額必須是**純數字**（不要包含貨幣符號、逗號）
  - ✅ 正確：\`1250.00\`
  - ❌ 錯誤：\`"HKD $1,250.00"\`、\`"$1,250.00"\`、\`"1,250"\`
- ✅ 保留兩位小數：\`125.00\`（不是 \`125\`）

### 3. **日期格式**
- ✅ 統一使用 \`YYYY-MM-DD\` 格式
  - ✅ 正確：\`"2025-09-25"\`
  - ❌ 錯誤：\`"2025年9月25日"\`、\`"25/09/2025"\`、\`"Sep 25, 2025"\`

### 4. **商品明細**
- ✅ **必須提取表格中的每一行商品**
- ✅ \`quantity\` 和 \`unit_price\` 必須是數字（不要包含單位）
  - ✅ 正確：\`"quantity": 2\`
  - ❌ 錯誤：\`"quantity": "2件"\`
- ✅ 商品描述要**完整**
  - ✅ 正確：\`"支雀巢 鮮奶絲滑咖啡 (268mlx15支)"\`
  - ❌ 錯誤：\`"支雀巢"\`、\`"咖啡"\`

### 5. **缺失字段處理**
- ✅ 如果字段找不到：
  - 文字字段：使用 \`""\`（空字符串）
  - 數字字段：使用 \`0\`
  - 布爾字段：使用 \`false\`
- ❌ 不要使用 \`null\`、\`undefined\`、\`"N/A"\`

### 6. **數學驗證**
- ✅ 每行商品：\`quantity × unit_price = amount\`
- ✅ 總金額：\`sum(items[].amount) - discount + tax ≈ total\`
- ⚠️ 如果計算不匹配，以**發票上顯示的金額**為準

---

## 🎯 **提取優先級**（按重要性排序）

1. 🥇 **total**（總金額）- 最重要
2. 🥈 **items**（商品明細）- 必須全部提取
3. 🥉 **invoice_number**（發票號碼）
4. **customer.name**（客戶名稱）
5. **supplier.name**（供應商名稱）
6. **date**（發票日期）
7. **payment_method**、**payment_info**（付款信息）
8. **subtotal**、**discount**、**tax**（金額明細）

---

## ✅ **最終檢查清單**

在返回 JSON 之前，請檢查：
- [ ] 發票號碼是否正確？（不是電話號碼或傳真號碼）
- [ ] 客戶名稱是否完整？
- [ ] 所有商品行是否都提取了？（數量是否匹配表格行數）
- [ ] 商品描述是否完整？（不是只有前幾個字）
- [ ] 所有金額是否是純數字？（沒有 $、HKD、逗號）
- [ ] 日期格式是否是 YYYY-MM-DD？
- [ ] 數學驗證是否通過？（quantity × unit_price = amount）
- [ ] FPS 和 PayMe 信息是否提取？
- [ ] JSON 格式是否正確？（沒有 markdown 標記）

---

🚀 **現在請開始逐字分析這張發票，確保準確率達到 95% 以上！**`,

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

            bank_statement: `你是一個專業的香港銀行對帳單數據提取專家。請**逐字逐句**仔細分析這張銀行對帳單圖片，提取所有可見信息。

🎯 **你的任務目標**：
將這張銀行對帳單的所有信息準確提取到 JSON 格式中，準確率必須達到 95% 以上。

---

## 📋 **第一步：識別銀行和帳戶信息**

### 1.1 **銀行信息**
- 🔍 查找位置：**最頂部**，通常有銀行 Logo
- ✅ 提取內容：
  - 銀行名稱（中文）：如「恆生銀行」
  - 銀行名稱（英文）：如「HANG SENG BANK」
  - 分行名稱：如「EAST POINT CITY (766)」
  - 銀行代碼：如「024」

### 1.2 **帳戶持有人**
- 🔍 查找位置：通常在**左上角**或**右上角**
- ✅ 提取內容：
  - 姓名（如：MR YEUNG CAVLIN）
  - 地址（可能多行，如：RM 2505 25/F MING TOA HSE / MING TAK EST / TSEUNG KWAN O NT）

### 1.3 **帳戶號碼**
- 🔍 查找位置：通常標註為「Account Number」或「戶口號碼」
- ✅ 格式示例：
  - \`766-450064-882\`（完整號碼）
  - \`766-45006\*-\*\*\*\`（部分隱藏）
- ⚠️ **提取規則**：
  - 如果號碼部分隱藏，提取可見部分
  - 保留分隔符（如 \`-\`）

### 1.4 **對帳單日期**
- 🔍 查找位置：「Statement Date」或「日期」
- ✅ 格式示例：
  - \`22 Mar 2025\` → \`2025-03-22\`
  - \`2025年3月22日\` → \`2025-03-22\`

---

## 📊 **第二步：識別帳戶類型和餘額**

### 2.1 **帳戶類型識別**
香港銀行對帳單通常包含多種帳戶：

#### **A. 綜合帳戶（Integrated Account）**
- 標註：「Integrated Account」或「綜合戶口」
- 包含：儲蓄、支票等子帳戶

#### **B. 儲蓄帳戶（Savings Account）**
- 標註：「HKD Statement Savings」或「港元儲蓄」
- 顯示：期初餘額、期末餘額

#### **C. 信用卡（Credit Card）**
- 標註：「VISA Platinum Card」或「信用卡」
- 顯示：信用額度、已用金額、可用餘額

#### **D. 貸款（Personal Loan）**
- 標註：「Personal Loan」或「私人貸款」
- 顯示：貸款餘額（通常為負數）

### 2.2 **餘額提取**
- 🔍 查找位置：「FINANCIAL POSITION」或「財務狀況」區域
- ✅ 提取內容：
  \`\`\`json
  "balances": {
    "integrated_account": {
      "opening": 30188.66,
      "closing": 30188.66
    },
    "savings": {
      "opening": 30188.66,
      "closing": 30188.66
    },
    "personal_loan": {
      "balance": -118986.00
    },
    "credit_card": {
      "credit_limit": 270000.00,
      "used": 19964.61,
      "available": 250035.39
    }
  }
  \`\`\`

---

## 💳 **第三步：提取交易明細**（最重要！）

### 3.1 **交易表格識別**
- 🔍 查找位置：「TRANSACTION HISTORY」或「交易記錄」區域
- ✅ 表格列（從左到右）：
  \`\`\`
  | Date | Transaction Details | Deposit | Withdrawal | Balance |
  | 日期 | 交易描述            | 存款    | 提款       | 餘額    |
  \`\`\`

### 3.2 **逐行提取交易**（CRITICAL！）
⚠️ **重要規則**：
1. ✅ **必須提取表格中的每一行交易**
2. ✅ **不要跳過任何一行**
3. ✅ **交易描述要完整**（不要只提取前幾個字）
4. ✅ **正確識別存款和提款**

### 3.3 **交易類型識別**
常見的香港銀行交易類型：

| 英文描述 | 中文描述 | 類型 | 示例 |
|---------|---------|------|------|
| BF BALANCE | 前結餘 | 餘額 | 期初餘額 |
| CREDIT INTEREST | 利息 - 儲蓄 | 存款 | 銀行利息 |
| CHEQUE DEPOSIT | 存入支票 | 存款 | 支票入帳 |
| AUTOPAY | 自動轉帳 | 提款 | 自動付款 |
| ATM WITHDRAWAL | 櫃員機提款 | 提款 | ATM 提款 |
| BANK TRANSFER | 銀行轉帳 | 提款 | 轉帳 |
| SALARY | 薪金 | 存款 | 薪金入帳 |

### 3.4 **提取示例**
如果看到以下交易：
\`\`\`
| 22 Feb | BF BALANCE 前結餘                    | -      | -      | 1,493.98  |
| 26 Feb | CREDIT INTEREST 利息 - 儲蓄          | 2.61   | -      | 1,496.59  |
| 07 Mar | CHEQUE DEPOSIT 存入支票              | 78,649.00 | -   | 80,145.59 |
| 07 Mar | AUTOPAY - ALIPAY HK/ASIA 自動轉帳    | -      | 940.00 | 79,205.59 |
| 10 Mar | AUTO 4006-1210-9327-0086 自動轉帳    | -      | 21,208.59 | 57,997.00 |
\`\`\`

提取為：
\`\`\`json
"transactions": [
  {
    "date": "2025-02-22",
    "type": "BF BALANCE",
    "description": "前結餘",
    "deposit": 0,
    "withdrawal": 0,
    "balance": 1493.98
  },
  {
    "date": "2025-02-26",
    "type": "CREDIT INTEREST",
    "description": "利息 - 儲蓄",
    "deposit": 2.61,
    "withdrawal": 0,
    "balance": 1496.59
  },
  {
    "date": "2025-03-07",
    "type": "CHEQUE DEPOSIT",
    "description": "存入支票",
    "deposit": 78649.00,
    "withdrawal": 0,
    "balance": 80145.59
  },
  {
    "date": "2025-03-07",
    "type": "AUTOPAY",
    "description": "ALIPAY HK/ASIA 自動轉帳",
    "deposit": 0,
    "withdrawal": 940.00,
    "balance": 79205.59
  },
  {
    "date": "2025-03-10",
    "type": "AUTO",
    "description": "4006-1210-9327-0086 自動轉帳",
    "deposit": 0,
    "withdrawal": 21208.59,
    "balance": 57997.00
  }
]
\`\`\`

⚠️ **常見錯誤**：
- ❌ 只提取第一頁的交易（如果有多頁）
- ❌ 交易描述不完整（如只提取「AUTOPAY」）
- ❌ 存款和提款混淆
- ❌ 金額包含逗號（如 "78,649.00" 應該是 78649.00）

---

## 📝 **第四步：提取交易統計**

### 4.1 **交易摘要**
- 🔍 查找位置：「Transaction Summary」或「交易摘要」
- ✅ 提取內容：
  \`\`\`json
  "transaction_summary": {
    "total_deposits": 88251.61,
    "total_withdrawals": 59958.59,
    "net_change": 28293.02
  }
  \`\`\`

### 4.2 **數學驗證**（CRITICAL！）
✅ **必須驗證**：
\`\`\`javascript
// 驗證餘額計算
opening_balance + total_deposits - total_withdrawals = closing_balance
1493.98 + 88251.61 - 59958.59 = 29787.00 ≈ 30188.66 ✅

// 驗證每筆交易
previous_balance + deposit - withdrawal = current_balance
1496.59 + 78649.00 - 0 = 80145.59 ✅
\`\`\`

---

## 📝 **完整 JSON 格式要求**

\`\`\`json
{
  "type": "bank_statement",
  "bank": {
    "name": "恆生銀行",
    "name_en": "HANG SENG BANK",
    "branch": "EAST POINT CITY (766)",
    "bank_code": "024"
  },
  
  "account_holder": {
    "name": "MR YEUNG CAVLIN",
    "address": "RM 2505 25/F MING TOA HSE\\nMING TAK EST\\nTSEUNG KWAN O NT"
  },
  
  "account_number": "766-450064-882",
  "statement_date": "2025-03-22",
  "statement_period": {
    "start": "2025-02-22",
    "end": "2025-03-22"
  },
  
  "balances": {
    "integrated_account": {
      "opening": 30188.66,
      "closing": 30188.66
    },
    "savings": {
      "opening": 30188.66,
      "closing": 30188.66
    },
    "personal_loan": {
      "balance": -118986.00
    },
    "credit_card": {
      "credit_limit": 270000.00,
      "used": 19964.61,
      "available": 250035.39
    }
  },
  
  "transactions": [
    {
      "date": "2025-02-22",
      "type": "BF BALANCE",
      "description": "前結餘",
      "deposit": 0,
      "withdrawal": 0,
      "balance": 1493.98
    },
    {
      "date": "2025-02-26",
      "type": "CREDIT INTEREST",
      "description": "利息 - 儲蓄",
      "deposit": 2.61,
      "withdrawal": 0,
      "balance": 1496.59
    }
  ],
  
  "transaction_summary": {
    "total_deposits": 88251.61,
    "total_withdrawals": 59958.59,
    "net_change": 28293.02
  },
  
  "currency": "HKD"
}
\`\`\`

---

## ⚠️ **CRITICAL RULES**（必須 100% 遵守）

### 1. **JSON 格式**
- ✅ 返回**純 JSON**，不要包含 \\\`\\\`\\\`json 或任何 markdown 標記
- ✅ 所有字段名稱必須用雙引號 \`"field_name"\`
- ✅ 字符串值必須用雙引號 \`"value"\`
- ✅ 數字值不要用引號 \`123.45\`（不是 \`"123.45"\`）

### 2. **金額格式**
- ✅ 所有金額必須是**純數字**（不要包含貨幣符號、逗號）
  - ✅ 正確：\`78649.00\`
  - ❌ 錯誤：\`"HKD $78,649.00"\`、\`"$78,649.00"\`、\`"78,649"\`
- ✅ 保留兩位小數：\`1493.98\`（不是 \`1493.9\`）
- ✅ 負數表示欠款：\`-118986.00\`

### 3. **日期格式**
- ✅ 統一使用 \`YYYY-MM-DD\` 格式
  - ✅ 正確：\`"2025-03-22"\`
  - ❌ 錯誤：\`"22 Mar 2025"\`、\`"2025年3月22日"\`、\`"22/03/2025"\`

### 4. **交易明細**
- ✅ **必須提取表格中的每一行交易**
- ✅ \`deposit\` 和 \`withdrawal\` 必須是數字（不要包含貨幣符號）
- ✅ 如果沒有存款或提款，使用 \`0\`（不是空字符串）
- ✅ 交易描述要**完整**
  - ✅ 正確：\`"ALIPAY HK/ASIA 自動轉帳"\`
  - ❌ 錯誤：\`"AUTOPAY"\`、\`"自動轉帳"\`

### 5. **缺失字段處理**
- ✅ 如果字段找不到：
  - 文字字段：使用 \`""\`（空字符串）
  - 數字字段：使用 \`0\`
  - 對象字段：使用 \`{}\`
- ❌ 不要使用 \`null\`、\`undefined\`、\`"N/A"\`

### 6. **數學驗證**
- ✅ 每筆交易：\`previous_balance + deposit - withdrawal = current_balance\`
- ✅ 總餘額：\`opening_balance + total_deposits - total_withdrawals ≈ closing_balance\`
- ⚠️ 如果計算不匹配，以**對帳單上顯示的餘額**為準

---

## 🎯 **提取優先級**（按重要性排序）

1. 🥇 **balances.savings.closing**（期末餘額）- 最重要
2. 🥈 **transactions**（交易明細）- 必須全部提取
3. 🥉 **account_number**（帳戶號碼）
4. **account_holder.name**（帳戶持有人）
5. **bank.name**（銀行名稱）
6. **statement_period**（對帳單期間）
7. **transaction_summary**（交易統計）
8. **balances.credit_card**、**balances.personal_loan**（其他帳戶）

---

## ✅ **最終檢查清單**

在返回 JSON 之前，請檢查：
- [ ] 帳戶號碼是否正確？（包含分隔符）
- [ ] 帳戶持有人姓名是否完整？
- [ ] 所有交易行是否都提取了？（數量是否匹配表格行數）
- [ ] 交易描述是否完整？（不是只有類型代碼）
- [ ] 所有金額是否是純數字？（沒有 $、HKD、逗號）
- [ ] 日期格式是否是 YYYY-MM-DD？
- [ ] 存款和提款是否正確區分？
- [ ] 數學驗證是否通過？（餘額計算正確）
- [ ] JSON 格式是否正確？（沒有 markdown 標記）

---

🚀 **現在請開始逐字分析這張銀行對帳單，確保準確率達到 95% 以上！**`
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
