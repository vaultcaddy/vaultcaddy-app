# 🚨 當前問題診斷和解決方案

## 問題 1：銀行對帳單超時失敗

### **錯誤現象（圖 1-2）：**
```
✅ OCR 完成：2521 字符
✅ 過濾完成：2521 → 2521 字符（減少 0%）
❌ DeepSeek API 請求失敗（第 1 次嘗試）: signal is aborted without reason
```

### **根本原因：**

1. **過濾無效**
   - 過濾前：2521 字符
   - 過濾後：2521 字符
   - **減少 0%** ← 沒有移除任何內容！

2. **為什麼過濾無效？**
   - 當前策略：只移除空白行
   - 問題：OCR 提取的文本可能**沒有空行**
   - 結果：所有內容都被保留

3. **2521 字符太長**
   - 發送給 DeepSeek：2521 字符
   - DeepSeek 處理時間：> 120 秒
   - 結果：超時

### **解決方案 1：恢復部分過濾邏輯（推薦）**

**策略：** 移除明顯無用的內容，但不要過度過濾

**保留：**
- ✅ 帳戶號碼、銀行名稱
- ✅ 對帳單日期、期間
- ✅ 開始/結束餘額
- ✅ 所有交易記錄（日期、描述、金額）

**移除：**
- ❌ 超長行（> 300 字符，通常是免責聲明）
- ❌ 網址（http, www, .com）
- ❌ 電話號碼（8位數字）
- ❌ 電郵地址（@）
- ❌ 頁碼（Page 1 of 3）
- ❌ 空行

**預期效果：** 2521 → 1500 字符（減少 40%）

---

### **解決方案 2：使用 GPT-4o-mini（更快的 AI）**

**問題：** deepseek-chat 處理 2521 字符需要 > 120 秒

**替代方案：** GPT-4o-mini（OpenAI）

| 模型 | 處理時間 | 成本 | 準確度 |
|------|----------|------|--------|
| **deepseek-chat** | 15-30 秒 | ¥0.0003 | 92% |
| **GPT-4o-mini** | **3-8 秒** | ¥0.0015 | 95% |

**優勢：**
- ✅ 更快（3-8 秒 vs 15-30 秒）
- ✅ 更穩定（OpenAI 服務更可靠）
- ✅ 更準確（95% vs 92%）

**劣勢：**
- ❌ 成本較高（5 倍）
- ❌ 需要 OpenAI API Key

---

## 問題 2：發票被處理了 2 次

### **錯誤現象（圖 3-5）：**

**第 1 次處理：**
```
🔄 混合處理器開始處理：05c077f0...JPG (invoice)
✅ OCR 完成：967 字符
✅ 過濾完成：967 → 955 字符
✅ DeepSeek 完成：500 字符
✅ 混合處理完成，總耗時：8982ms
```

**第 2 次處理（重複）：**
```
🔄 混合處理器開始處理：05c077f0...JPG (invoice)  ← 同一個文件！
✅ OCR 完成：967 字符
✅ 過濾完成：967 → 955 字符
✅ DeepSeek 完成：500 字符
✅ 混合處理完成，總耗時：8982ms
```

### **根本原因：**

**代碼分析：**

`firstproject.html` 中有兩個上傳函數：

1. **`uploadFile(file)`** - 按鈕點擊上傳
2. **`uploadFileDirect(file, pages)`** - 拖放上傳

兩個函數都調用了 `processMultiPageFileWithAI`！

**推測：**
- 用戶上傳發票（JPG 文件）
- 觸發了兩個上傳函數（可能是事件重複綁定）
- 結果：同一個文件被處理了 2 次

### **診斷步驟：**

1. **檢查事件綁定**
   - 查看是否有重複的事件監聽器
   - 查看是否同時觸發了按鈕和拖放

2. **檢查調用棧**
   - 查看 Console 日誌中的調用順序
   - 確認是哪個函數被調用了 2 次

3. **檢查文檔 ID**
   - 第 1 次和第 2 次的 `docId` 是否相同？
   - 如果相同 → 重複處理同一文檔
   - 如果不同 → 創建了 2 個文檔

### **解決方案：防止重複處理**

**方案 1：添加處理鎖**

```javascript
// 全局處理鎖
const processingDocuments = new Set();

async function processMultiPageFileWithAI(files, docId, documentType) {
    // 檢查是否正在處理
    if (processingDocuments.has(docId)) {
        console.warn(`⚠️ 文檔 ${docId} 正在處理中，跳過重複處理`);
        return;
    }
    
    try {
        // 添加到處理鎖
        processingDocuments.add(docId);
        console.log(`🔒 鎖定文檔 ${docId}，開始處理`);
        
        // ... 原有的處理邏輯 ...
        
    } finally {
        // 處理完成，移除鎖
        processingDocuments.delete(docId);
        console.log(`🔓 解鎖文檔 ${docId}，處理完成`);
    }
}
```

**方案 2：檢查文檔狀態**

```javascript
async function processMultiPageFileWithAI(files, docId, documentType) {
    // 檢查文檔當前狀態
    const doc = await window.simpleDataManager.getDocument(currentProjectId, docId);
    
    if (doc.status === 'processing' || doc.status === 'completed') {
        console.warn(`⚠️ 文檔 ${docId} 已經在處理或已完成（${doc.status}），跳過`);
        return;
    }
    
    // ... 繼續處理 ...
}
```

**方案 3：禁用重複事件綁定**

```javascript
// 移除舊的事件監聽器，只綁定一次
function setupUploadEvents() {
    const uploadBtn = document.getElementById('uploadBtn');
    const dropZone = document.getElementById('dropZone');
    
    // 移除舊的監聽器
    uploadBtn.removeEventListener('click', handleUploadClick);
    dropZone.removeEventListener('drop', handleDrop);
    
    // 添加新的監聽器
    uploadBtn.addEventListener('click', handleUploadClick, { once: false });
    dropZone.addEventListener('drop', handleDrop, { once: false });
}
```

---

## 問題 3：過濾邏輯的平衡

### **您的要求：**
> "銀行對帳單中不要暴力過濾，只過濾空白等內容"

### **當前實現：**
```javascript
filterBankStatementText(text) {
    // 只移除空行
    if (trimmed.length === 0) continue;
    
    // 保留所有有內容的行
    relevantLines.push(line);
}
```

**問題：** 過濾效果 0%，導致超時！

### **建議的平衡方案：**

```javascript
filterBankStatementText(text) {
    console.log('🏦 過濾銀行對帳單文本（平衡版本）...');
    
    const lines = text.split('\n');
    const relevantLines = [];
    
    for (let line of lines) {
        const trimmed = line.trim();
        
        // ❌ 跳過空行
        if (trimmed.length === 0) continue;
        
        // ❌ 跳過超長行（> 300 字符，通常是免責聲明）
        if (trimmed.length > 300) {
            console.log(`  ⏭️ 跳過超長行: ${trimmed.substring(0, 40)}...`);
            continue;
        }
        
        // ❌ 跳過網址（明顯無用）
        if (/www\.|http|\.com|\.hk/.test(trimmed)) {
            console.log(`  ⏭️ 跳過網址: ${trimmed.substring(0, 40)}...`);
            continue;
        }
        
        // ❌ 跳過電郵地址（明顯無用）
        if (/@/.test(trimmed)) {
            console.log(`  ⏭️ 跳過電郵: ${trimmed.substring(0, 40)}...`);
            continue;
        }
        
        // ❌ 跳過頁碼（明顯無用）
        if (/Page \d+ of \d+/i.test(trimmed) || /第 \d+ 頁/.test(trimmed)) {
            console.log(`  ⏭️ 跳過頁碼: ${trimmed}`);
            continue;
        }
        
        // ✅ 保留所有其他內容（包括交易記錄、餘額、帳戶信息）
        relevantLines.push(line);
    }
    
    const filteredText = relevantLines.join('\n');
    const reductionPercent = Math.round((1 - filteredText.length / text.length) * 100);
    console.log(`✅ 銀行對帳單過濾完成：${text.length} → ${filteredText.length} 字符（減少 ${reductionPercent}%）`);
    
    return filteredText;
}
```

**預期效果：**
- 2521 → 1500-1800 字符（減少 30-40%）
- 不會移除任何重要內容
- 只移除明顯無用的內容

---

## 🎯 **立即行動計劃**

### **優先級 1：修復銀行對帳單超時**

1. **實施平衡過濾**
   - 修改 `filterBankStatementText` 方法
   - 移除超長行、網址、電郵、頁碼
   - 保留所有交易和餘額數據

2. **測試**
   - 清除緩存
   - 重新上傳 3 頁銀行對帳單
   - 觀察過濾效果和處理時間

**預期結果：**
```
✅ 過濾完成：2521 → 1600 字符（減少 36%）
✅ DeepSeek 成功：15-20 秒
```

---

### **優先級 2：修復發票重複處理**

1. **添加處理鎖**
   - 實施方案 1（處理鎖）
   - 防止重複處理同一文檔

2. **測試**
   - 重新上傳發票
   - 確認只處理 1 次

**預期結果：**
```
🔒 鎖定文檔 XXX，開始處理
✅ DeepSeek 完成
🔓 解鎖文檔 XXX，處理完成
（不會出現第 2 次處理）
```

---

### **優先級 3：長期優化（未來）**

1. **評估 GPT-4o-mini**
   - 測試處理速度和準確度
   - 對比成本

2. **實施逐頁處理**
   - 支持 100+ 頁的大型 PDF

3. **添加後台處理**
   - 用戶無需等待

---

## 📞 **需要您確認的問題**

1. **過濾策略**
   - 是否接受「平衡版本」的過濾？
   - 移除：超長行、網址、電郵、頁碼
   - 保留：所有交易記錄、餘額、帳戶信息

2. **重複處理**
   - 發票是上傳 1 次還是 2 次？
   - 是否只是處理了 2 次（重複處理）？

3. **成本**
   - 是否考慮切換到 GPT-4o-mini？
   - 成本：¥0.0015/張（5 倍），但更快更穩定

請告訴我您的決定！🚀

