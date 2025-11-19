# PDF 上傳 AI 處理失敗診斷

## 📅 日期
2025-11-19

---

## 🐛 問題描述

根據用戶提供的圖3-4截圖，PDF 上傳後出現以下錯誤：

```
AI 處理失敗: Error: AI 處理終止或超時
文檔 XxqMQrFFfMwDMdT3yjYq 內 Credits 已經消耗，無需重新處理
```

---

## 🔍 錯誤分析

### 錯誤 1：`AI 處理失敗: Error: AI 處理終止或超時`

**這是真正的錯誤**，表示 DeepSeek API 處理超時（180秒）。

**可能原因：**

1. **DeepSeek API 響應慢** ⭐⭐⭐⭐⭐
   - 即使文本只有 1818-2521 字符
   - 銀行對帳單可能有很多交易記錄
   - DeepSeek 需要生成大量 JSON 輸出
   - 輸出時間可能超過 180 秒

2. **網絡連接不穩定** ⭐⭐⭐⭐
   - Cloudflare Worker 與 DeepSeek API 之間的連接
   - 可能因網絡波動導致超時

3. **銀行對帳單複雜度高** ⭐⭐⭐
   - 用戶上傳的是 3 頁銀行對帳單
   - 可能包含數十甚至上百筆交易
   - DeepSeek 需要逐一提取和格式化

### 錯誤 2：`文檔 XxqMQrFFfMwDMdT3yjYq 內 Credits 已經消耗，無需重新處理`

**這不是錯誤！** 這是正常的日誌信息，表示：
- 文檔已經處理過（即使失敗）
- Credits 已經扣除（因為 OCR 已完成）
- 系統不會重新處理該文檔

---

## 📊 與之前成功案例的對比

### 為什麼之前成功，現在失敗？

**可能的差異：**

| 特徵 | 之前（成功） | 現在（失敗） |
|------|------------|------------|
| 文檔類型 | 發票 | 銀行對帳單 |
| 頁數 | 1-2 頁 | 3 頁 |
| 數據量 | 10-20 項明細 | 可能 50+ 筆交易 |
| 輸出 JSON 大小 | 較小 | 較大 |
| DeepSeek 處理時間 | < 60秒 | > 180秒 |

**關鍵發現：**
- 銀行對帳單的交易記錄比發票的項目明細多得多
- DeepSeek 需要生成更長的 JSON 輸出
- 更長的輸出需要更多時間

---

## 🛠️ 當前的超時處理邏輯

在 `hybrid-vision-deepseek.js` 的 `analyzeTextWithDeepSeek` 函數中：

```javascript
// 第 529-534 行
if (error.name === 'AbortError' || error.message.includes('aborted')) {
    console.error(`⏰ DeepSeek API 超時（180 秒），不再重試`);
    console.error(`   建議：文本可能太長或太複雜，需要分段處理`);
    throw new Error(`DeepSeek API 超時: 文本長度 ${text.length} 字符超過處理能力`);
}
```

**問題：**
- 當 DeepSeek 超時時，代碼立即拋出錯誤
- 不會觸發智能分段邏輯
- 用戶無法重試

---

## 💡 解決方案

### 方案 1：增加超時時間 ⭐⭐⭐

**優點：**
- 簡單直接
- 適用於大多數銀行對帳單

**缺點：**
- 用戶等待時間長
- 可能仍然超時

**實現：**
```javascript
// hybrid-vision-deepseek.js
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 300000); // 300秒 = 5分鐘
```

---

### 方案 2：優化 DeepSeek Prompt（減少輸出） ⭐⭐⭐⭐

**優點：**
- 減少 DeepSeek 輸出時間
- 減少 token 成本

**缺點：**
- 可能遺漏一些字段

**實現：**
```javascript
// 只提取關鍵字段
const systemPrompt = `
你是一個專業的銀行對帳單解析器。請提取以下字段：
- bankName: 銀行名稱
- accountNumber: 帳戶號碼
- statementPeriod: 對帳單期間
- openingBalance: 期初餘額
- closingBalance: 期末餘額
- transactions: 交易記錄（只包含 date, description, amount, balance）

不要包含任何其他字段或說明。
`;
```

---

### 方案 3：自動觸發智能分段 ⭐⭐⭐⭐⭐

**優點：**
- 自動處理超時
- 用戶無需干預
- 適用於任何大小的文檔

**缺點：**
- 實現複雜
- 需要測試

**實現：**
```javascript
// hybrid-vision-deepseek.js - analyzeTextWithDeepSeek
if (error.name === 'AbortError' || error.message.includes('aborted')) {
    console.warn(`⏰ DeepSeek API 超時，嘗試分段處理...`);
    
    // ✅ 不拋出錯誤，返回 null 以觸發分段
    return null;
}

// processMultiPageDocument
if (!extractedData) {
    console.warn(`⚠️ DeepSeek 處理失敗，嘗試智能分段...`);
    
    // 強制使用智能分段
    const coreContext = this.extractCoreContext(allText, documentType);
    const chunks = this.intelligentChunkingWithOverlap(allText, 5000, 500, coreContext);
    
    // 繼續處理分段...
}
```

---

### 方案 4：允許用戶手動重試 ⭐⭐⭐⭐

**優點：**
- 給用戶第二次機會
- 可能第二次會成功（網絡波動）

**缺點：**
- 需要 UI 改動
- 用戶體驗不佳

**實現：**
```javascript
// document-detail-new.js
if (doc.status === 'failed') {
    // 顯示「重試」按鈕
    `<button onclick="retryProcessing('${doc.id}')">重試處理</button>`
}

async function retryProcessing(docId) {
    // 重新處理文檔
    await window.hybridProcessor.processDocument(docId);
}
```

---

## 📝 推薦方案

**綜合方案（方案 2 + 方案 3）：**

1. **優化 Prompt** - 減少不必要的輸出字段
2. **自動分段** - 當超時時自動觸發智能分段
3. **增加超時** - 將超時從 180秒 增加到 240秒（4分鐘）

**實施步驟：**

1. 修改 `hybrid-vision-deepseek.js` 的 `analyzeTextWithDeepSeek`：
   ```javascript
   // 增加超時到 240秒
   const timeoutId = setTimeout(() => controller.abort(), 240000);
   
   // 超時時返回 null 而非拋出錯誤
   if (error.name === 'AbortError') {
       console.warn(`⏰ DeepSeek API 超時，將觸發分段處理`);
       return null;
   }
   ```

2. 修改 `processMultiPageDocument` 以自動處理 `null` 結果：
   ```javascript
   if (!extractedData) {
       console.warn(`⚠️ DeepSeek 處理失敗，自動分段處理...`);
       // 強制分段邏輯
   }
   ```

3. 優化銀行對帳單的 Prompt（已在之前的修復中完成）

---

## 🧪 測試計劃

1. **測試場景 1：小型銀行對帳單（1-2 頁，< 20 筆交易）**
   - ✅ 應該在 60 秒內完成
   - ✅ 不觸發分段

2. **測試場景 2：中型銀行對帳單（3-5 頁，20-50 筆交易）**
   - ⏱️ 可能需要 120-180 秒
   - ⚠️ 可能觸發分段

3. **測試場景 3：大型銀行對帳單（5+ 頁，50+ 筆交易）**
   - ⏱️ 必定觸發分段
   - ✅ 應該成功處理

---

## 🎯 下一步

1. ✅ 文檔已創建
2. ⏳ 等待用戶確認測試場景
3. ⏳ 實施推薦方案
4. ⏳ 測試並驗證

---

**狀態**: 診斷完成，等待實施  
**優先級**: 高  
**預計時間**: 30-45 分鐘

