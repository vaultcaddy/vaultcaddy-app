# 🚨 為什麼發票成功但銀行對帳單失敗？

## 🔍 **關鍵發現**

從您的截圖分析：

```
✅ DeepSeek 回應長度: 9758 字符
✅ 直接解析成功！
✅ JSON 解析完成（使用方法 1）
✅ 混合處理完成，總耗時: 130761ms

❌ 更新文檔失敗: FirebaseError: Function DocumentReference.update() called with invalid data. 
   Nested arrays are not supported
```

---

## 💡 **根本原因**

### **1. 發票為什麼成功？**

**發票的數據結構簡單：**
```json
{
  "invoiceNumber": "INV-12345",
  "vendor": "Company A",
  "date": "2025-03-22",
  "total": 1000.00,
  "items": [
    {
      "description": "Item 1",
      "quantity": 1,
      "unitPrice": 100.00,
      "amount": 100.00
    }
  ]
}
```

**特點：**
- ✅ 只有 1 層數組（`items`）
- ✅ `items` 裡面的每個對象都是**簡單對象**（只有 string 和 number）
- ✅ **沒有嵌套數組**
- ✅ Firestore 完全兼容

---

### **2. 銀行對帳單為什麼失敗？**

**銀行對帳單的數據結構複雜：**
```json
{
  "bankName": "HANG SENG BANK",
  "transactions": [
    {
      "date": "2025-03-22",
      "description": "CREDIT INTEREST",
      "amount": 0.58,
      "items": [  // ← 嵌套數組！
        {"detail": "..."}
      ]
    },
    [  // ← 嵌套數組！
      {"date": "2025-03-23", ...}
    ]
  ]
}
```

**問題：**
- ❌ DeepSeek 可能返回**嵌套數組**
- ❌ Firestore **不支持嵌套數組**
- ❌ 保存時失敗

---

## 🔧 **為什麼 `cleanBankStatementData` 沒有被調用？**

### **保存流程：**

```javascript
// firstproject.html 第 2408-2417 行
const result = await processor.processMultiPageDocument(files, documentType);

// ✅ DeepSeek 返回數據
// ✅ cleanBankStatementData 在 hybrid-vision-deepseek.js 中被調用
// ✅ 數據已清理

// ❌ 但是！直接保存原始 result.extractedData，沒有使用清理後的數據
await window.simpleDataManager.updateDocument(currentProjectId, docId, {
    status: 'completed',
    processedData: result.extractedData,  // ← 這裡直接保存！
    rawText: result.rawText,
    confidence: result.confidence
});
```

**問題：**
- `result.extractedData` 是**已經清理過的數據**
- **但是**，DeepSeek 可能返回的數據有問題
- 或者清理函數沒有完全清理乾淨

---

## 🔬 **深入分析：為什麼清理沒有生效？**

### **檢查 `cleanBankStatementData` 調用流程：**

```javascript
// hybrid-vision-deepseek.js

// 1. processMultiPageDocument
const extractedData = this.mergeChunkedResults(pageResults.filter(r => r !== null), documentType);

// 2. mergeChunkedResults
if (results.length === 1) {
    if (this.isBankStatement(documentType)) {
        console.log('   這是銀行對帳單，調用 cleanBankStatementData');
        return this.cleanBankStatementData(result);  // ✅ 應該被調用
    }
}

// 3. cleanBankStatementData
cleanBankStatementData(data) {
    // 處理嵌套數組
    if (transactions.length > 0 && Array.isArray(transactions[0])) {
        console.warn('⚠️ 檢測到嵌套數組，正在展平...');
        transactions = transactions.flat();
    }
    
    // 清理交易記錄
    transactions = transactions.map((tx, index) => {
        if (Array.isArray(tx)) {
            console.warn(`⚠️ 交易 ${index + 1} 是數組，取第一個元素`);
            tx = tx[0] || {};
        }
        
        return {
            date: String(tx.date || ''),
            description: String(tx.description || ''),
            type: String(tx.type || ''),
            amount: parseFloat(tx.amount) || 0,
            balance: parseFloat(tx.balance) || 0
        };
    }).filter(tx => tx !== null);
}
```

---

## 🎯 **問題定位**

### **檢查清理日誌：**

從您的截圖，我看到：
```
✅ 混合處理完成，總耗時: 130761ms
📊 性能統計：
   - 頁數: 3
   - OCR 調用: 3 次（並行）
   - DeepSeek 調用: 1 次
   - 成功段數: 1
   - 總交易數: 0  // ← 問題在這裡！
```

**關鍵發現：**
- `總交易數: 0`
- **這意味著交易數據沒有被正確提取！**

---

## 🔍 **可能的原因**

### **原因 1：DeepSeek 返回的數據結構不正確**

DeepSeek 可能返回了這樣的結構：
```json
{
  "bankName": "HANG SENG BANK",
  "transactions": {  // ← 對象，不是數組！
    "items": [...]
  }
}
```

或者：
```json
{
  "bankName": "HANG SENG BANK",
  "transaction": [...]  // ← 字段名是 transaction（單數），不是 transactions
}
```

---

### **原因 2：`cleanBankStatementData` 沒有處理所有情況**

當前的 `cleanBankStatementData` 只處理：
1. 嵌套數組：`transactions[0]` 是數組
2. 單個交易是數組：`tx` 是數組

**但沒有處理：**
1. `transactions` 本身不是數組
2. `transactions` 是對象
3. `transactions` 是 `undefined`

---

## ✅ **解決方案**

### **方案 1：增強 `cleanBankStatementData` 函數**

```javascript
cleanBankStatementData(data) {
    console.log('   🧹 清理銀行對帳單數據...');
    console.log('   📝 原始數據:', JSON.stringify(data, null, 2));  // ← 添加日誌
    
    if (!data) {
        console.error('   ❌ 數據為空，無法清理');
        return null;
    }
    
    // ✅ 處理 transactions 字段的各種情況
    let transactions = [];
    
    // 情況 1：data.transactions 是數組
    if (Array.isArray(data.transactions)) {
        transactions = data.transactions;
    }
    // 情況 2：data.transaction 是數組（單數）
    else if (Array.isArray(data.transaction)) {
        console.warn('   ⚠️ 字段名是 transaction（單數），正在轉換...');
        transactions = data.transaction;
    }
    // 情況 3：data.transactions 是對象
    else if (data.transactions && typeof data.transactions === 'object') {
        console.warn('   ⚠️ transactions 是對象，正在提取...');
        // 嘗試從對象中提取數組
        if (Array.isArray(data.transactions.items)) {
            transactions = data.transactions.items;
        } else if (Array.isArray(data.transactions.list)) {
            transactions = data.transactions.list;
        } else {
            console.error('   ❌ transactions 對象中找不到數組');
        }
    }
    // 情況 4：完全沒有 transactions 字段
    else {
        console.warn('   ⚠️ 找不到 transactions 字段');
        console.warn('   📝 可用字段:', Object.keys(data));
    }
    
    console.log(`   📊 原始交易數量：${transactions.length}`);
    
    // ✅ 如果是嵌套數組，展平它
    if (transactions.length > 0 && Array.isArray(transactions[0])) {
        console.warn('   ⚠️ 檢測到嵌套數組，正在展平...');
        transactions = transactions.flat();
        console.log(`   ✅ 展平完成：${transactions.length} 筆交易`);
    }
    
    // ✅ 清理交易記錄
    transactions = transactions.map((tx, index) => {
        // 確保 tx 是對象，不是數組
        if (Array.isArray(tx)) {
            console.warn(`   ⚠️ 交易 ${index + 1} 是數組，取第一個元素:`, tx);
            tx = tx[0] || {};
        }
        
        // 確保 tx 是對象
        if (typeof tx !== 'object' || tx === null) {
            console.warn(`   ⚠️ 交易 ${index + 1} 不是對象，跳過:`, tx);
            return null;
        }
        
        // ✅ 確保沒有嵌套對象或數組
        const cleanTx = {
            date: String(tx.date || ''),
            description: String(tx.description || ''),
            type: String(tx.type || ''),
            amount: parseFloat(tx.amount) || 0,
            balance: parseFloat(tx.balance) || 0
        };
        
        // ✅ 檢查清理後的交易是否有嵌套
        Object.keys(cleanTx).forEach(key => {
            if (typeof cleanTx[key] === 'object') {
                console.warn(`   ⚠️ 交易 ${index + 1} 的 ${key} 是對象，轉為字符串`);
                cleanTx[key] = JSON.stringify(cleanTx[key]);
            }
        });
        
        return cleanTx;
    }).filter(tx => tx !== null); // 移除無效交易
    
    // 清理整個對象
    const cleanData = {
        bankName: String(data.bankName || ''),
        accountHolder: String(data.accountHolder || ''),
        accountNumber: String(data.accountNumber || ''),
        statementDate: String(data.statementDate || ''),
        statementPeriod: String(data.statementPeriod || ''),
        openingBalance: parseFloat(data.openingBalance) || 0,
        closingBalance: parseFloat(data.closingBalance) || 0,
        currency: String(data.currency || 'HKD'),
        transactions: transactions
    };
    
    console.log(`   ✅ 數據清理完成：${cleanData.transactions.length} 筆交易`);
    console.log('   📝 清理後數據:', JSON.stringify(cleanData, null, 2));  // ← 添加日誌
    
    return cleanData;
}
```

---

### **方案 2：在保存前再次清理**

```javascript
// firstproject.html 第 2408-2417 行
const result = await processor.processMultiPageDocument(files, documentType);

// ✅ 如果是銀行對帳單，再次清理數據
let processedData = result.extractedData;
if (documentType === 'bank_statement' || documentType === 'bank-statement') {
    console.log('🧹 保存前再次清理銀行對帳單數據...');
    processedData = cleanDataForFirestore(processedData);
}

await window.simpleDataManager.updateDocument(currentProjectId, docId, {
    status: 'completed',
    processedData: processedData,  // ← 使用清理後的數據
    rawText: result.rawText,
    confidence: result.confidence
});

// 清理函數
function cleanDataForFirestore(data) {
    if (!data) return data;
    
    // 遞歸清理對象
    function clean(obj) {
        if (Array.isArray(obj)) {
            // 展平嵌套數組
            const flattened = obj.flat();
            return flattened.map(item => clean(item));
        } else if (typeof obj === 'object' && obj !== null) {
            const cleaned = {};
            for (const key in obj) {
                const value = obj[key];
                if (Array.isArray(value)) {
                    cleaned[key] = clean(value);
                } else if (typeof value === 'object' && value !== null) {
                    // 不保存嵌套對象，轉為字符串
                    cleaned[key] = JSON.stringify(value);
                } else {
                    cleaned[key] = value;
                }
            }
            return cleaned;
        }
        return obj;
    }
    
    return clean(data);
}
```

---

## 🚀 **立即實施**

**優先順序：**
1. ✅ 增強 `cleanBankStatementData` 函數（添加詳細日誌）
2. ✅ 處理所有 transactions 字段的情況
3. ✅ 確保沒有嵌套對象或數組
4. ✅ 在保存前再次清理

**您希望我立即實施哪個方案？** 🚀

