# 🔍 發票 vs 銀行對帳單對比分析

## 您的觀察 100% 正確！

### **UI 結構完全一樣：**
- 左邊：PDF 預覽
- 右邊：提取的數據欄位
- **唯一不同：欄位名稱**

---

## 📊 **數據流對比**

### **發票（成功）：**

```
1. PDF 上傳
   ↓
2. Vision API OCR → 提取文本
   ↓
3. DeepSeek 分析 → 返回 JSON
   {
     "invoiceNumber": "INV-202510000232",
     "vendor": "惠原品味發展有限公司",
     "date": "2025/10/04",
     "total": 2666.60,
     "items": [
       {
         "description": "美國CAB PRIME為肝小排",
         "quantity": 1,
         "unitPrice": 67.00,
         "amount": 2666.60
       }
     ]
   }
   ↓
4. 保存到 Firestore
   {
     "processedData": {
       "invoiceNumber": "INV-202510000232",
       "vendor": "惠原品味發展有限公司",
       ...
     }
   }
   ↓
5. UI 顯示（document-detail-new.js）
   ✅ displayInvoiceContent(data)
   ✅ data.invoiceNumber → 顯示在 UI
   ✅ data.vendor → 顯示在 UI
   ✅ data.items → 顯示在表格
```

---

### **銀行對帳單（失敗）：**

```
1. PDF 上傳
   ↓
2. Vision API OCR → 提取文本
   ↓
3. DeepSeek 分析 → 返回 JSON
   {
     "bankName": "HANG SENG BANK",
     "accountNumber": "...",
     "closingBalance": 30188.66,
     "transactions": [
       {
         "date": "2025-03-22",
         "description": "B/F BALANCE",
         "amount": 1493.98,
         "balance": 1493.98
       },
       ...
     ]
   }
   ↓
4. cleanBankStatementData 清理數據
   ✅ 展平嵌套數組
   ✅ 確保 Firestore 兼容
   ↓
5. 保存到 Firestore
   {
     "processedData": {
       "bankName": "HANG SENG BANK",
       "accountNumber": "...",
       "closingBalance": 30188.66,
       "transactions": [...]  // ← 這裡有數據！
     }
   }
   ↓
6. UI 顯示（document-detail-new.js）
   ❌ displayBankStatementContent(data)
   ❌ data.bankName → 顯示 "—"
   ❌ data.accountNumber → 顯示 "—"
   ❌ data.transactions → 顯示 "共 0 筆交易"
```

---

## 🚨 **問題定位**

從圖1-2的日誌可以看到：
```
✅ 直接解析 JSON...
✅ 直接解析成功！
✅ 混合處理完成，總耗時: 65602ms
📊 性能統計：
   - 總交易數: 0  // ← 問題在這裡！
```

**關鍵發現：**
- `總交易數: 0` 在 `hybrid-vision-deepseek.js` 第 206 行
- 這意味著 `extractedData.transactions` 是空的或不存在

---

## 🔍 **可能的原因**

### **原因 1：DeepSeek 返回的數據結構不正確**

DeepSeek 可能返回了這樣的結構：
```json
{
  "confidence": 85,
  "document_type": "銀行對帳單",
  "bankName": "HANG SENG BANK",
  "accountNumber": "...",
  "closingBalance": 30188.66,
  "transactions": []  // ← 空數組！
}
```

或者：
```json
{
  "confidence": 85,
  "data": {  // ← 嵌套在 data 裡面
    "bankName": "HANG SENG BANK",
    "transactions": [...]
  }
}
```

---

### **原因 2：`cleanBankStatementData` 清理時丟失了數據**

讓我們檢查清理邏輯：

```javascript
cleanBankStatementData(data) {
    // 處理 transactions 字段
    let transactions = [];
    
    if (Array.isArray(data.transactions)) {
        transactions = data.transactions;
    } else if (Array.isArray(data.transaction)) {
        transactions = data.transaction;
    } else {
        // ← 如果都不是數組，transactions 就是空的！
        console.warn('⚠️ 找不到 transactions 字段');
    }
    
    // 清理交易記錄
    transactions = transactions.map((tx, index) => {
        // ...
    }).filter(tx => tx !== null);
    
    // 返回清理後的數據
    return {
        bankName: String(data.bankName || ''),
        transactions: transactions  // ← 可能是空數組
    };
}
```

---

## ✅ **解決方案**

### **方案 1：添加詳細日誌，查看 DeepSeek 返回的原始數據**

在 `hybrid-vision-deepseek.js` 第 206 行之前添加：

```javascript
console.log('🔍 提取的數據:', JSON.stringify(extractedData, null, 2));
console.log('🔍 transactions 字段:', extractedData.transactions);
console.log('🔍 transactions 類型:', typeof extractedData.transactions);
console.log('🔍 transactions 長度:', extractedData.transactions?.length);
```

### **方案 2：檢查 Firestore 中保存的數據**

在瀏覽器 Console 中運行：
```javascript
// 獲取文檔 ID（從 URL 中）
const params = new URLSearchParams(window.location.search);
const docId = params.get('id');
const projectId = params.get('project');

// 讀取 Firestore 數據
const doc = await window.simpleDataManager.getDocument(docId);
console.log('📊 Firestore 數據:', JSON.stringify(doc.processedData, null, 2));
```

### **方案 3：參考發票的做法**

發票成功的原因：
1. ✅ DeepSeek 返回的數據結構簡單
2. ✅ 沒有嵌套數組
3. ✅ 字段名稱一致

**我們應該：**
1. ✅ 確保 DeepSeek Prompt 返回正確的數據結構
2. ✅ 確保 `cleanBankStatementData` 不會丟失數據
3. ✅ 確保 UI 顯示邏輯正確

---

## 🚀 **立即實施**

**優先順序：**
1. ✅ 添加詳細日誌（查看 DeepSeek 返回的原始數據）
2. ✅ 檢查 Firestore 中保存的數據
3. ✅ 修復數據丟失問題

**您希望我立即實施哪個方案？** 🚀

