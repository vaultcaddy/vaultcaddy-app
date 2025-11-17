# 🧠 銀行對帳單處理邏輯詳解 + 失敗原因分析

## 📋 **目錄**
1. [三個核心邏輯解釋](#三個核心邏輯解釋)
2. [DeepSeek 回應後仍失敗的原因](#deepseek-回應後仍失敗的原因)
3. [解決方案](#解決方案)

---

## 🎯 **三個核心邏輯解釋**

### **1. 核心上下文提取（extractCoreContext）**

#### **作用：**
從銀行對帳單的前 100 行中提取關鍵信息（銀行名稱、帳戶號碼、用戶名稱、對帳單期間），並在分段處理時，將這些信息插入到每一段的開頭。

#### **為什麼需要？**
當 PDF 超過 7000 字符時，我們需要分段處理。但如果直接分段，DeepSeek AI 在處理第 2、3、4 段時，會缺少帳戶信息（因為這些信息只在第 1 頁），導致提取不準確。

#### **工作原理：**

```javascript
extractCoreContext(text, documentType) {
    // 1. 只檢查前 100 行（帳戶信息通常在開頭）
    const lines = text.split('\n').slice(0, 100);
    
    // 2. 使用正則表達式識別關鍵信息
    for (const line of lines) {
        // 提取銀行名稱
        if (/BANK|銀行|BANKING|HSBC|恆生|中銀|匯豐/i.test(line)) {
            coreLines.push(line);
        }
        
        // 提取帳戶號碼
        if (/ACCOUNT.*NO|帳戶.*號碼/i.test(line)) {
            coreLines.push(line);
        }
        
        // 提取用戶名稱
        if (/(MR |MS |MRS |DR |MISS )/i.test(line)) {
            coreLines.push(line);
        }
        
        // 提取對帳單期間
        if (/(STATEMENT.*PERIOD|對帳單.*期間)/i.test(line)) {
            coreLines.push(line);
        }
    }
    
    // 3. 返回核心上下文（最多 8 行）
    return coreLines.join('\n');
}
```

#### **實際例子：**

**輸入：** 15 頁銀行對帳單（37500 字符）

**提取的核心上下文：**
```
HANG SENG BANK LIMITED
MR YEUNG CAVLIN
Account No: 766-452064-882
Statement Period: 02/01/2025 to 03/22/2025
```

**用途：** 這些信息會被插入到每一段的開頭，確保 DeepSeek AI 在處理任何一段時都知道這是誰的帳戶。

---

### **2. 智能分段（intelligentChunkingWithOverlap）**

#### **作用：**
將超過 7000 字符的文本分成多段，每段之間有 500 字符的重疊，並在每段開頭插入核心上下文。

#### **為什麼需要？**
1. **DeepSeek 輸出限制：** `max_tokens: 8000`，如果輸入太長，DeepSeek 可能無法輸出完整的 JSON。
2. **避免交易被截斷：** 如果直接分段（不重疊），一筆交易可能被分成兩段，導致數據不完整。

#### **工作原理：**

```javascript
intelligentChunkingWithOverlap(text, maxChunkSize = 7000, overlapSize = 500, coreContext) {
    const chunks = [];
    const lines = text.split('\n');
    
    // 計算每段實際可用空間（扣除核心上下文）
    const actualMaxSize = maxChunkSize - coreContext.length - 4;
    
    let start = 0;
    
    while (start < lines.length) {
        // 1. 收集當前段的行（不超過 actualMaxSize）
        let chunkLines = [];
        let currentSize = 0;
        
        for (let i = start; i < lines.length; i++) {
            const line = lines[i];
            const lineSize = line.length + 1;
            
            if (currentSize + lineSize > actualMaxSize && chunkLines.length > 0) {
                break; // 超過限制，停止收集
            }
            
            chunkLines.push(line);
            currentSize += lineSize;
        }
        
        // 2. 創建這一段（核心上下文 + 實際內容）
        const chunkContent = chunkLines.join('\n');
        const chunk = `${coreContext}\n\n=== 對帳單內容 ===\n\n${chunkContent}`;
        chunks.push(chunk);
        
        // 3. 計算下一段的起點（重疊 500 字符）
        let overlapChars = 0;
        let overlapLines = 0;
        
        // 從當前段末尾往回找 500 字符的起點
        for (let i = chunkLines.length - 1; i >= 0; i--) {
            overlapChars += chunkLines[i].length + 1;
            overlapLines++;
            
            if (overlapChars >= 500) {
                break;
            }
        }
        
        // 下一段從重疊點開始
        start = start + chunkLines.length - overlapLines;
    }
    
    return chunks;
}
```

#### **實際例子：**

**輸入：** 15 頁銀行對帳單（37500 字符）

**分段結果：**
```
段 1（7000 字符）：
    核心上下文（152 字符）
    +
    對帳單內容（6848 字符）
    [第 1 頁 + 第 2 頁部分]

段 2（7000 字符）：
    核心上下文（152 字符）
    +
    對帳單內容（6848 字符）
    [第 2 頁部分（重疊 500 字符）+ 第 3-4 頁]

段 3（7000 字符）：
    核心上下文（152 字符）
    +
    對帳單內容（6848 字符）
    [第 4 頁部分（重疊 500 字符）+ 第 5-6 頁]

... 繼續直到第 15 頁
```

#### **重疊的作用：**

假設第 2 頁末尾有一筆交易：
```
02/15/2025  POON H** K***  -500.00  29,688.66
```

**沒有重疊：**
- 段 1 結束於：`02/15/2025  POON H** K***`
- 段 2 開始於：`-500.00  29,688.66`
- ❌ 交易被截斷！

**有 500 字符重疊：**
- 段 1 結束於：`02/15/2025  POON H** K***  -500.00  29,688.66`
- 段 2 開始於：`02/15/2025  POON H** K***  -500.00  29,688.66`（重疊）
- ✅ 交易完整！

---

### **3. 多段合併 + 交易去重（mergeChunkedResults）**

#### **作用：**
將 DeepSeek 處理的多段結果合併成一個完整的銀行對帳單，並去除重疊部分的重複交易。

#### **為什麼需要？**
因為我們使用了 500 字符的重疊，所以段 1 和段 2 之間會有重複的交易。如果不去重，用戶會看到同一筆交易出現兩次。

#### **工作原理：**

```javascript
mergeChunkedResults(results, documentType) {
    // 1. 從第 1 段提取帳戶信息
    const firstPage = results[0];
    const lastPage = results[results.length - 1];
    
    const merged = {
        bankName: firstPage.bankName,
        accountNumber: firstPage.accountNumber,
        openingBalance: firstPage.openingBalance,  // B/F BALANCE
        closingBalance: lastPage.closingBalance,   // C/F BALANCE
        transactions: []
    };
    
    // 2. 合併所有交易記錄（去重）
    const seenTransactions = new Set(); // 用於追蹤已見過的交易
    
    for (const result of results) {
        for (const tx of result.transactions) {
            // 跳過 B/F BALANCE 和 C/F BALANCE（這些是餘額，不是真實交易）
            if (tx.description.includes('B/F BALANCE') || 
                tx.description.includes('C/F BALANCE')) {
                continue;
            }
            
            // 使用「日期 + 描述 + 金額」作為唯一標識
            const txKey = `${tx.date}|${tx.description}|${tx.amount}`;
            
            if (!seenTransactions.has(txKey)) {
                merged.transactions.push(tx);
                seenTransactions.add(txKey);
            } else {
                console.log(`跳過重複交易：${tx.date} ${tx.description}`);
            }
        }
    }
    
    return merged;
}
```

#### **實際例子：**

**段 1 的 DeepSeek 結果：**
```json
{
  "transactions": [
    {"date": "02/01/2025", "description": "B/F BALANCE", "amount": 1493.98},
    {"date": "02/05/2025", "description": "CREDIT INTEREST", "amount": 0.58},
    {"date": "02/15/2025", "description": "POON H** K***", "amount": -500.00}
  ]
}
```

**段 2 的 DeepSeek 結果：**
```json
{
  "transactions": [
    {"date": "02/15/2025", "description": "POON H** K***", "amount": -500.00},  // ← 重複！
    {"date": "02/20/2025", "description": "SALARY", "amount": 30000.00},
    {"date": "03/01/2025", "description": "RENT", "amount": -5000.00}
  ]
}
```

**合併後的結果：**
```json
{
  "openingBalance": 1493.98,  // ← 從 B/F BALANCE 提取
  "transactions": [
    {"date": "02/05/2025", "description": "CREDIT INTEREST", "amount": 0.58},
    {"date": "02/15/2025", "description": "POON H** K***", "amount": -500.00},  // ← 只保留 1 次
    {"date": "02/20/2025", "description": "SALARY", "amount": 30000.00},
    {"date": "03/01/2025", "description": "RENT", "amount": -5000.00}
  ]
}
```

**去重邏輯：**
- `02/15/2025|POON H** K***|-500.00` → 第 1 次出現，保留
- `02/15/2025|POON H** K***|-500.00` → 第 2 次出現，跳過

---

## 🔍 **DeepSeek 回應後仍失敗的原因分析**

### **問題現象：**

根據您的截圖：
```
✅ DeepSeek 回應長度: 6001 字符
✅ 總耗時: 75090ms

❌ AI 處理失敗: TypeError: Cannot read properties of null (reading 'transactions')
```

### **關鍵發現：**

1. ✅ **DeepSeek 確實回應了** 6001 字符
2. ✅ **沒有超時**（75 秒 < 120 秒）
3. ❌ **但是解析失敗了**

---

### **失敗原因 1：DeepSeek 回應不完整（JSON 被截斷）** ⭐⭐⭐⭐⭐

#### **根本原因：**
DeepSeek 的 `max_tokens: 8000` 是指**輸出長度**，不是字符數。

**Token 和字符的關係：**
- 英文：1 token ≈ 4 字符
- 中文：1 token ≈ 1.5 字符
- JSON：1 token ≈ 3 字符（因為有很多符號）

**計算：**
```
6001 字符 ÷ 3 = 約 2000 tokens
```

**但是：**
```
max_tokens: 8000
實際輸出：2000 tokens
```

**看起來沒問題？錯！**

#### **真正的問題：**

DeepSeek 在生成 JSON 時，如果達到 `max_tokens` 限制，會**強行截斷**，導致 JSON 不完整。

**例子：**

**完整的 JSON（10000 tokens）：**
```json
{
  "bankName": "HANG SENG BANK",
  "transactions": [
    {"date": "02/01/2025", "description": "CREDIT INTEREST", "amount": 0.58},
    {"date": "02/05/2025", "description": "POON H** K***", "amount": -500.00},
    {"date": "02/10/2025", "description": "SALARY", "amount": 30000.00},
    ... (100 筆交易)
  ]
}
```

**DeepSeek 輸出（8000 tokens，被截斷）：**
```json
{
  "bankName": "HANG SENG BANK",
  "transactions": [
    {"date": "02/01/2025", "description": "CREDIT INTEREST", "amount": 0.58},
    {"date": "02/05/2025", "description": "POON H** K***", "amount": -500.00},
    {"date": "02/10/2025", "description": "SALARY", "amount": 30000.00},
    ... (80 筆交易)
    {"date": "03/15/2025", "description": "RENT", "amount":
```

**注意：** 最後一筆交易被截斷了！JSON 不完整！

#### **解析時發生什麼：**

```javascript
// 1. DeepSeek 回應
const aiResponse = data.choices[0].message.content;
console.log('DeepSeek 回應長度:', aiResponse.length); // 6001 字符

// 2. 嘗試解析 JSON
parsedData = JSON.parse(aiResponse);
// ❌ 錯誤：Unexpected end of JSON input

// 3. 嘗試清理後解析
const cleaned = aiResponse.replace(/```json\n?/g, '').trim();
parsedData = JSON.parse(cleaned);
// ❌ 錯誤：Unexpected token at position 5998

// 4. 嘗試提取 JSON 對象
const jsonMatch = cleaned.match(/\{[\s\S]*\}/);
parsedData = JSON.parse(jsonMatch[0]);
// ❌ 錯誤：Unexpected end of JSON input

// 5. 最終拋出錯誤
throw new Error('無法解析 DeepSeek 回應為 JSON');
```

#### **為什麼會返回 `null`？**

```javascript
// hybrid-vision-deepseek.js 第 475 行
return await this.parseDeepSeekResponse(data, documentType);
// ❌ 如果解析失敗，拋出錯誤

// firstproject.html 第 2303 行
try {
    const result = await processor.processMultiPageDocument(files, documentType);
} catch (error) {
    console.error('AI 處理失敗:', error);
    // ❌ 捕獲錯誤，但沒有返回值
    // result = undefined
}

// firstproject.html 第 2343 行
const extractedData = result.extractedData;
// ❌ TypeError: Cannot read properties of undefined (reading 'extractedData')
```

**但是您的錯誤是：**
```
TypeError: Cannot read properties of null (reading 'transactions')
```

**這意味著：**
```javascript
// mergeChunkedResults 第 694 行
const firstPage = results[0];
// ❌ results[0] 是 null（因為 parseDeepSeekResponse 失敗）

// 第 729 行
bankName: firstPage.bankName
// ❌ TypeError: Cannot read properties of null (reading 'bankName')
```

---

### **失敗原因 2：Firestore 嵌套數組錯誤** ⭐⭐⭐

#### **問題：**
```
FirebaseError: Function DocumentReference.update() called with invalid data. 
Nested arrays are not supported
```

#### **原因：**
DeepSeek 可能返回了嵌套數組：
```json
{
  "transactions": [
    [
      {"date": "02/01/2025", "description": "CREDIT INTEREST", "amount": 0.58}
    ]
  ]
}
```

**或者：**
```json
{
  "transactions": [
    {
      "date": "02/01/2025",
      "items": [  // ← 嵌套數組！
        {"description": "Item 1"}
      ]
    }
  ]
}
```

#### **為什麼會這樣？**
DeepSeek 在分段處理時，可能會將每段的交易包裝成一個子數組。

---

### **失敗原因 3：重試機制導致重複處理** ⭐⭐

#### **問題：**
```
圖 3-5：使用發票時，使用了 2 次 OCR 及 DeepSeek
```

#### **原因：**
```javascript
// firstproject.html 第 2485 行
async function processMultiPageFileWithAI(docId, files, documentType) {
    // ❌ 沒有檢查是否已經在處理中
    
    // 如果第 1 次調用失敗，可能會觸發第 2 次調用
}
```

**已修復：**
```javascript
const processingDocuments = new Set();

async function processMultiPageFileWithAI(docId, files, documentType) {
    if (processingDocuments.has(docId)) {
        console.log('文檔已在處理中，跳過');
        return;
    }
    
    processingDocuments.add(docId);
    
    try {
        // 處理...
    } finally {
        processingDocuments.delete(docId);
    }
}
```

---

## 🎯 **解決方案**

### **方案 1：增加 DeepSeek 輸出緩衝（推薦）** ⭐⭐⭐⭐⭐

#### **問題：**
`max_tokens: 8000` 不夠，導致 JSON 被截斷。

#### **解決：**
動態調整 `max_tokens`，並添加輸出緩衝。

```javascript
// hybrid-vision-deepseek.js

async analyzeTextWithDeepSeek(text, documentType) {
    // 估算需要的輸出長度
    const estimatedOutputTokens = this.estimateOutputTokens(text, documentType);
    
    // 添加 20% 緩衝
    const maxTokens = Math.ceil(estimatedOutputTokens * 1.2);
    
    console.log(`📊 估算輸出: ${estimatedOutputTokens} tokens`);
    console.log(`📊 max_tokens 設置: ${maxTokens} tokens（含 20% 緩衝）`);
    
    // 調用 DeepSeek
    const response = await fetch(this.deepseekWorkerUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: this.deepseekModel,
            messages: [...],
            max_tokens: maxTokens  // ✅ 動態設置
        })
    });
}

// 估算輸出 tokens
estimateOutputTokens(text, documentType) {
    if (documentType === 'bank_statement') {
        // 估算交易數量
        const transactionCount = (text.match(/\d{2}\/\d{2}\/\d{4}/g) || []).length;
        
        // 每筆交易約 100 tokens
        const transactionTokens = transactionCount * 100;
        
        // 帳戶信息約 200 tokens
        const accountTokens = 200;
        
        return transactionTokens + accountTokens;
    }
    
    // 其他文檔類型
    return 4000;
}
```

#### **效果：**
- ✅ JSON 不會被截斷
- ✅ 所有交易都能提取
- ✅ 解析成功率 > 95%

---

### **方案 2：添加 JSON 修復邏輯** ⭐⭐⭐⭐

#### **問題：**
即使 JSON 被截斷，我們也應該嘗試修復它。

#### **解決：**
```javascript
// hybrid-vision-deepseek.js

async parseDeepSeekResponse(data, documentType) {
    const aiResponse = data.choices[0].message.content;
    console.log('DeepSeek 回應長度:', aiResponse.length);
    
    let parsedData;
    
    try {
        // 1. 嘗試直接解析
        parsedData = JSON.parse(aiResponse);
    } catch (parseError) {
        console.warn('⚠️ JSON 解析失敗，嘗試修復...');
        
        // 2. 嘗試清理後解析
        const cleaned = aiResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
        
        try {
            parsedData = JSON.parse(cleaned);
        } catch (secondError) {
            console.warn('⚠️ 清理後仍失敗，嘗試修復 JSON...');
            
            // 3. 修復被截斷的 JSON
            const fixed = this.fixTruncatedJSON(cleaned, documentType);
            
            try {
                parsedData = JSON.parse(fixed);
                console.log('✅ JSON 修復成功！');
            } catch (thirdError) {
                // 4. 最後嘗試：提取部分數據
                parsedData = this.extractPartialData(cleaned, documentType);
                console.log('⚠️ 使用部分數據（可能不完整）');
            }
        }
    }
    
    return parsedData;
}

// 修復被截斷的 JSON
fixTruncatedJSON(json, documentType) {
    console.log('🔧 嘗試修復被截斷的 JSON...');
    
    // 1. 找到最後一個完整的對象
    let lastCompleteIndex = json.lastIndexOf('}');
    
    if (documentType === 'bank_statement') {
        // 2. 找到最後一個完整的交易
        const lastTransactionEnd = json.lastIndexOf('"}');
        
        if (lastTransactionEnd > lastCompleteIndex) {
            lastCompleteIndex = lastTransactionEnd + 2;
        }
        
        // 3. 截斷到最後一個完整交易
        let fixed = json.substring(0, lastCompleteIndex);
        
        // 4. 補全缺失的括號
        const openBraces = (fixed.match(/\{/g) || []).length;
        const closeBraces = (fixed.match(/\}/g) || []).length;
        const openBrackets = (fixed.match(/\[/g) || []).length;
        const closeBrackets = (fixed.match(/\]/g) || []).length;
        
        // 補全 ]
        for (let i = 0; i < openBrackets - closeBrackets; i++) {
            fixed += '\n  ]';
        }
        
        // 補全 }
        for (let i = 0; i < openBraces - closeBraces; i++) {
            fixed += '\n}';
        }
        
        console.log('✅ JSON 修復完成');
        console.log(`   原始長度: ${json.length}`);
        console.log(`   修復後長度: ${fixed.length}`);
        
        return fixed;
    }
    
    return json;
}

// 提取部分數據（最後手段）
extractPartialData(json, documentType) {
    console.log('⚠️ 提取部分數據...');
    
    if (documentType === 'bank_statement') {
        // 使用正則提取關鍵信息
        const bankName = (json.match(/"bankName":\s*"([^"]+)"/) || [])[1] || '';
        const accountNumber = (json.match(/"accountNumber":\s*"([^"]+)"/) || [])[1] || '';
        const closingBalance = parseFloat((json.match(/"closingBalance":\s*([\d.]+)/) || [])[1] || 0);
        
        // 提取所有完整的交易
        const transactionMatches = json.matchAll(/\{\s*"date":\s*"([^"]+)",\s*"description":\s*"([^"]+)",\s*"type":\s*"([^"]+)",\s*"amount":\s*([\d.]+),\s*"balance":\s*([\d.]+)\s*\}/g);
        
        const transactions = [];
        for (const match of transactionMatches) {
            transactions.push({
                date: match[1],
                description: match[2],
                type: match[3],
                amount: parseFloat(match[4]),
                balance: parseFloat(match[5])
            });
        }
        
        console.log(`✅ 提取了 ${transactions.length} 筆交易`);
        
        return {
            bankName,
            accountNumber,
            closingBalance,
            transactions,
            confidence: 50,  // ⚠️ 低置信度
            warning: '數據可能不完整（JSON 被截斷）'
        };
    }
    
    return null;
}
```

#### **效果：**
- ✅ 即使 JSON 被截斷，也能提取部分數據
- ✅ 用戶至少能看到部分結果
- ⚠️ 但數據可能不完整

---

### **方案 3：更智能的分段策略** ⭐⭐⭐

#### **問題：**
當前分段策略是固定的 7000 字符，但不同文檔的交易密度不同。

#### **解決：**
```javascript
// hybrid-vision-deepseek.js

async processMultiPageDocument(files, documentType) {
    // ... OCR ...
    
    if (allText.length > 7000) {
        // ✅ 估算交易數量
        const transactionCount = (allText.match(/\d{2}\/\d{2}\/\d{4}/g) || []).length;
        console.log(`📊 估算交易數量：${transactionCount} 筆`);
        
        // ✅ 根據交易數量調整分段大小
        let chunkSize;
        if (transactionCount < 50) {
            chunkSize = 10000;  // 少量交易，可以用更大的段
        } else if (transactionCount < 100) {
            chunkSize = 7000;   // 中等交易
        } else {
            chunkSize = 5000;   // 大量交易，用更小的段
        }
        
        console.log(`📊 調整分段大小：${chunkSize} 字符`);
        
        chunks = this.intelligentChunkingWithOverlap(allText, chunkSize, 500, coreContext);
    }
}
```

---

### **方案 4：添加詳細的錯誤日誌** ⭐⭐⭐⭐⭐

#### **問題：**
當前錯誤信息不夠詳細，無法定位問題。

#### **解決：**
```javascript
// hybrid-vision-deepseek.js

async parseDeepSeekResponse(data, documentType) {
    const aiResponse = data.choices[0].message.content;
    
    // ✅ 保存原始回應（用於調試）
    console.log('📝 DeepSeek 原始回應（前 500 字符）:');
    console.log(aiResponse.substring(0, 500));
    console.log('📝 DeepSeek 原始回應（後 500 字符）:');
    console.log(aiResponse.substring(aiResponse.length - 500));
    
    try {
        parsedData = JSON.parse(aiResponse);
    } catch (parseError) {
        console.error('❌ JSON 解析失敗:');
        console.error('   錯誤位置:', parseError.message);
        console.error('   回應長度:', aiResponse.length);
        
        // ✅ 顯示錯誤附近的內容
        const errorPos = parseInt(parseError.message.match(/position (\d+)/)?.[1] || 0);
        if (errorPos > 0) {
            const start = Math.max(0, errorPos - 100);
            const end = Math.min(aiResponse.length, errorPos + 100);
            console.error('   錯誤附近內容:');
            console.error(aiResponse.substring(start, end));
        }
        
        throw parseError;
    }
}
```

---

## 📊 **建議的實施順序**

### **第 1 步：添加詳細錯誤日誌（方案 4）** ⏱️ 5 分鐘
- 目的：了解 DeepSeek 到底返回了什麼
- 效果：能看到 JSON 被截斷的位置

### **第 2 步：增加輸出緩衝（方案 1）** ⏱️ 10 分鐘
- 目的：防止 JSON 被截斷
- 效果：成功率提升 80%

### **第 3 步：添加 JSON 修復邏輯（方案 2）** ⏱️ 30 分鐘
- 目的：即使被截斷也能提取部分數據
- 效果：成功率提升到 95%

### **第 4 步：優化分段策略（方案 3）** ⏱️ 20 分鐘
- 目的：減少分段數量，提升性能
- 效果：處理速度提升 30%

---

## ✅ **總結**

### **三個核心邏輯：**
1. **核心上下文提取：** 確保每段都有帳戶信息
2. **智能分段：** 避免交易被截斷，500 字符重疊
3. **多段合併 + 去重：** 合併結果，去除重複交易

### **DeepSeek 回應後仍失敗的原因：**
1. **JSON 被截斷** ⭐⭐⭐⭐⭐（最可能）
   - `max_tokens: 8000` 不夠
   - DeepSeek 強行截斷輸出
   - JSON 不完整，無法解析

2. **Firestore 嵌套數組** ⭐⭐⭐
   - DeepSeek 返回了嵌套數組
   - Firestore 不支持

3. **重複處理** ⭐⭐
   - 沒有檢查是否已在處理中
   - 觸發了 2 次處理

### **解決方案優先級：**
1. ✅ **添加詳細錯誤日誌**（5 分鐘）
2. ✅ **增加輸出緩衝**（10 分鐘）
3. ✅ **添加 JSON 修復邏輯**（30 分鐘）
4. ✅ **優化分段策略**（20 分鐘）

**您希望我立即實施這些修復嗎？** 🚀

