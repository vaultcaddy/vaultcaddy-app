# 🔧 數據映射問題修復

## 🚨 **問題診斷**

### **症狀：**
- ✅ AI 提取成功（狀態顯示「已完成」）
- ❌ 數據未顯示（銀行名稱、帳戶號碼、日期、餘額都是「—」或「$0.00」）
- ❌ 交易記錄顯示「無交易記錄」

---

## 🔍 **根本原因**

### **DeepSeek 返回的字段名（snake_case）：**
```json
{
  "bank_name": "恆生銀行",
  "account_number": "766-452064-882",
  "statement_period": "02/01/2025 to 03/22/2025",
  "opening_balance": 36188.66,
  "closing_balance": 36188.66,
  "transactions": [...]
}
```

### **顯示代碼期望的字段名（camelCase）：**
```javascript
const bankName = data.bankName || data.bank_name || ...
const accountNumber = data.accountNumber || data.account_number || ...
const statementDate = data.statementDate || data.statement_date || ...
```

### **問題：**
- DeepSeek Prompt 要求返回 `bank_name`（snake_case）
- 顯示代碼優先查找 `bankName`（camelCase）
- 雖然有 fallback（`data.bank_name`），但可能因為其他原因失敗

---

## ✅ **解決方案 1：統一使用 camelCase（推薦）**

### **修改 DeepSeek Prompt：**

**當前 Prompt（第 720-740 行）：**
```javascript
{
  "confidence": 0-100,
  "bank_name": "必須 - 銀行名稱",
  "account_holder": "戶主名稱",
  "account_number": "必須 - 賬戶號碼",
  "statement_period": "必須 - MM/DD/YYYY to MM/DD/YYYY",
  "opening_balance": 數字,
  "closing_balance": 必須 - 數字,
  "transactions": [...]
}
```

**修改為（camelCase）：**
```javascript
{
  "confidence": 0-100,
  "bankName": "必須 - 銀行名稱（如：恆生銀行、HANG SENG BANK）",
  "accountHolder": "戶主名稱（如：MR YEUNG CAVLIN）",
  "accountNumber": "必須 - 賬戶號碼（如：766-452064-882）",
  "statementDate": "必須 - 對帳單日期 YYYY-MM-DD（如：2025-03-22）",
  "statementPeriod": "對帳單期間（如：02/01/2025 to 03/22/2025）",
  "openingBalance": 數字,
  "closingBalance": 必須 - 數字,
  "transactions": [
    {
      "date": "必須 - YYYY-MM-DD",
      "description": "必須 - 交易描述",
      "type": "debit 或 credit",
      "amount": 數字,
      "balance": 數字
    }
  ],
  "currency": "HKD"
}
```

**關鍵改動：**
1. `bank_name` → `bankName`
2. `account_holder` → `accountHolder`
3. `account_number` → `accountNumber`
4. `statement_period` → `statementPeriod`
5. 添加 `statementDate`（單獨的日期字段）
6. `opening_balance` → `openingBalance`
7. `closing_balance` → `closingBalance`

---

## ✅ **解決方案 2：增強 Fallback 邏輯**

### **修改顯示代碼（document-detail-new.js）：**

**當前代碼（第 709-713 行）：**
```javascript
const bankName = data.bankName || data.bank_name || data.bank || '—';
const accountNumber = data.accountNumber || data.account_number || data.accountNo || '—';
const statementDate = data.statementDate || data.statement_date || data.date || '—';
const openingBalance = data.openingBalance || data.opening_balance || data.startBalance || 0;
const closingBalance = data.closingBalance || data.closing_balance || data.endBalance || data.finalBalance || 0;
```

**增強為：**
```javascript
// ✅ 提取銀行名稱（支持多種字段名稱）
const bankName = data.bankName || 
                 data.bank_name || 
                 data.bank || 
                 data.bankname ||
                 '—';

// ✅ 提取帳戶號碼
const accountNumber = data.accountNumber || 
                      data.account_number || 
                      data.accountNo || 
                      data.account_no ||
                      data.accountnum ||
                      '—';

// ✅ 提取對帳單日期（優先使用 statement_period 的結束日期）
let statementDate = data.statementDate || 
                    data.statement_date || 
                    data.date ||
                    data.statementdate ||
                    '';

// 如果沒有單獨的日期，從 statement_period 提取結束日期
if (!statementDate && data.statement_period) {
    const match = data.statement_period.match(/to\s+(\d{2}\/\d{2}\/\d{4})/);
    if (match) {
        // 轉換 MM/DD/YYYY 為 YYYY-MM-DD
        const [month, day, year] = match[1].split('/');
        statementDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    }
}

if (!statementDate) statementDate = '—';

// ✅ 提取餘額
const openingBalance = data.openingBalance || 
                       data.opening_balance || 
                       data.startBalance || 
                       data.start_balance ||
                       0;

const closingBalance = data.closingBalance || 
                       data.closing_balance || 
                       data.endBalance || 
                       data.end_balance ||
                       data.finalBalance ||
                       data.final_balance ||
                       0;

// ✅ 提取交易記錄
const transactions = data.transactions || 
                     data.transaction || 
                     data.items ||
                     [];

console.log('🔍 提取的數據:');
console.log('   銀行名稱:', bankName);
console.log('   帳戶號碼:', accountNumber);
console.log('   對帳單日期:', statementDate);
console.log('   期初餘額:', openingBalance);
console.log('   期末餘額:', closingBalance);
console.log('   交易數量:', transactions.length);
```

---

## 🎯 **推薦方案**

### **同時實施兩個方案：**

1. **修改 DeepSeek Prompt**（統一使用 camelCase）
   - 確保 AI 返回正確的字段名
   - 避免後續映射問題

2. **增強 Fallback 邏輯**（支持多種字段名）
   - 兼容舊數據
   - 處理 AI 可能的變化
   - 添加調試日誌

---

## 📊 **預期效果**

### **修復前：**
```
銀行名稱：—
帳戶號碼：—
對帳單日期：—
期末餘額：$0.00
交易記錄：無交易記錄
```

### **修復後：**
```
銀行名稱：恆生銀行
帳戶號碼：766-452064-882
對帳單日期：2025-03-22
期末餘額：$36,188.66
交易記錄：共 45 筆交易
```

---

## 🚀 **立即行動**

### **步驟 1：修改 DeepSeek Prompt**
- 文件：`hybrid-vision-deepseek.js`
- 位置：第 720-740 行
- 修改：所有 snake_case → camelCase

### **步驟 2：增強 Fallback 邏輯**
- 文件：`document-detail-new.js`
- 位置：第 709-753 行
- 添加：更多 fallback 選項 + 調試日誌

### **步驟 3：測試**
1. 重新上傳 3 頁 PDF
2. 觀察 Console 日誌
3. 確認數據正確顯示

---

## 📝 **調試技巧**

### **在 Console 中查看原始數據：**
```javascript
// 打開 document-detail-new.js
// 在 displayBankStatementContent 函數開頭添加：
console.log('📊 原始 processedData:', JSON.stringify(currentDocument.processedData, null, 2));
```

### **預期輸出：**
```json
{
  "bank_name": "恆生銀行",  // ← 如果是 snake_case，需要修改 Prompt
  "bankName": "恆生銀行",   // ← 如果是 camelCase，正確！
  ...
}
```

---

## 🎯 **總結**

**問題：** 字段名不匹配（snake_case vs camelCase）

**解決：**
1. 統一 DeepSeek Prompt 使用 camelCase
2. 增強 Fallback 邏輯支持多種字段名
3. 添加調試日誌確認數據

**預期：** 100% 數據正確顯示！

