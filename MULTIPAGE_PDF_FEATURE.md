# 📄 多頁 PDF 處理功能

**實施日期：** 2025-11-14  
**功能：** 完整處理 PDF 所有頁面（不只第一頁）

---

## ✅ 功能概述

### 之前（只處理第一頁）❌
```
1. 上傳 3 頁 PDF
2. 只轉換第一頁為圖片
3. 只處理第一頁
4. ❌ 丟失第 2、3 頁的數據
5. ❌ Credits 可能計算不準確
```

### 現在（處理所有頁面）✅
```
1. 上傳 3 頁 PDF
2. 轉換所有 3 頁為圖片
3. 處理所有 3 頁
4. ✅ 合併所有頁面數據
5. ✅ Credits 按實際頁數扣除（3 Credits）
```

---

## 🔧 技術實現

### 1. 文件上傳階段 ✅

**修改：** 從單文件改為文件數組

```javascript
// ❌ 之前：只處理第一頁
let fileToProcess = file;
if (isPDF) {
    const imageFiles = await convertPDFToImages(file);
    fileToProcess = imageFiles[0]; // 只用第一頁
}

// ✅ 現在：處理所有頁面
let filesToProcess = [file];
if (isPDF) {
    const imageFiles = await convertPDFToImages(file);
    filesToProcess = imageFiles; // 所有頁面
    console.log(`📄 將處理所有 ${imageFiles.length} 頁`);
}
```

### 2. 並行上傳所有頁面 ✅

```javascript
// 使用 Promise.all 並行上傳
const uploadPromises = filesToProcess.map(f => 
    window.simpleDataManager.uploadFile(currentProjectId, f)
);
const imageUrls = await Promise.all(uploadPromises);
console.log(`✅ ${imageUrls.length} 個文件已上傳到 Storage`);
```

**優點：**
- ✅ 速度快（並行處理）
- ✅ 效率高

### 3. 文檔數據結構 ✅

```javascript
const docData = {
    name: file.name,
    pages: filesToProcess.length, // 實際頁數
    imageUrl: imageUrls[0], // 第一頁（向後兼容）
    imageUrls: imageUrls, // ✅ 所有頁面的 URL 數組
    originalFileType: file.type,
    isPDFConverted: isPDFConverted
};
```

### 4. Credits 扣除 ✅

```javascript
// 按實際頁數扣除
await window.creditsManager.deductCredits(filesToProcess.length);
console.log(`💰 已扣除 ${filesToProcess.length} Credits（${filesToProcess.length} 頁）`);
```

---

## 🤖 AI 處理流程

### 多頁處理函數

```javascript
async function processMultiPageFileWithAI(files, docId, documentType) {
    const processor = new window.HybridVisionDeepSeekProcessor();
    const allResults = [];
    
    // 1. 順序處理每一頁
    for (let i = 0; i < files.length; i++) {
        console.log(`📄 處理第 ${i + 1}/${files.length} 頁...`);
        
        // Vision API OCR + DeepSeek 分析
        const result = await processor.processDocument(files[i], documentType);
        allResults.push(result);
        
        // 2. 更新進度
        await updateDocument(docId, {
            status: 'processing',
            processingProgress: Math.round(((i + 1) / files.length) * 100)
        });
    }
    
    // 3. 合併結果
    const mergedData = mergeMultiPageResults(allResults, documentType);
    
    // 4. 完成
    await updateDocument(docId, {
        status: 'completed',
        processedData: mergedData,
        pageResults: allResults, // 保存每頁詳細結果
        processingProgress: 100
    });
}
```

**為什麼順序處理，不並行？**
- Vision API 有速率限制（每分鐘請求數）
- 避免超過配額
- 可以實時更新進度
- 更容易錯誤處理

---

## 📊 合併邏輯

### 1. 銀行對帳單 ✅

```javascript
function mergeBankStatementPages(results) {
    const allTransactions = [];
    let totalOpeningBalance = 0;
    let totalClosingBalance = 0;
    
    results.forEach((result, index) => {
        const data = result.data;
        
        // 合併所有交易記錄
        if (data.transactions) {
            allTransactions.push(...data.transactions);
        }
        
        // 第一頁的期初餘額
        if (index === 0 && data.opening_balance) {
            totalOpeningBalance = parseFloat(data.opening_balance);
        }
        
        // 最後一頁的期末餘額
        if (index === results.length - 1 && data.closing_balance) {
            totalClosingBalance = parseFloat(data.closing_balance);
        }
    });
    
    return {
        ...firstPage,
        transactions: allTransactions,
        opening_balance: totalOpeningBalance,
        closing_balance: totalClosingBalance,
        total_pages: results.length
    };
}
```

**合併規則：**
- ✅ 合併所有交易記錄
- ✅ 保留第一頁的期初餘額
- ✅ 保留最後一頁的期末餘額
- ✅ 保留第一頁的銀行名稱、帳號等基本信息

### 2. 發票/收據 ✅

```javascript
function mergeInvoiceReceiptPages(results) {
    const allItems = [];
    let totalAmount = 0;
    
    results.forEach(result => {
        const data = result.data;
        
        // 合併所有項目
        if (data.items) {
            allItems.push(...data.items);
        }
        
        // 累加總金額
        if (data.totalAmount) {
            totalAmount += parseFloat(data.totalAmount);
        }
    });
    
    return {
        ...firstPage,
        items: allItems,
        totalAmount: totalAmount,
        total_pages: results.length
    };
}
```

**合併規則：**
- ✅ 合併所有項目
- ✅ 累加總金額
- ✅ 保留第一頁的供應商、發票號等基本信息

### 3. 通用文檔 ✅

```javascript
function mergeGeneralPages(results) {
    const allText = results.map((r, i) => {
        const data = r.data;
        return `--- Page ${i + 1} ---\n${data.full_text || data.text || ''}`;
    }).join('\n\n');
    
    return {
        ...firstPage,
        full_text: allText,
        total_pages: results.length
    };
}
```

**合併規則：**
- ✅ 合併所有文本內容
- ✅ 標記頁碼（Page 1, Page 2, ...）
- ✅ 保留第一頁的元數據

---

## 📋 數據結構

### Firestore 文檔數據

```javascript
{
    // 基本信息
    name: "eStatementFile_20250829143359.pdf",
    fileName: "eStatementFile_20250829143359.pdf",
    fileSize: 123456,
    fileType: "image/jpeg", // 轉換後的類型
    documentType: "bank_statement",
    
    // 狀態
    status: "completed", // processing, completed, failed
    processingProgress: 100, // 0-100%
    
    // 頁數和 URL
    pages: 3,
    imageUrl: "https://...", // 第一頁（向後兼容）
    imageUrls: [ // ✅ 所有頁面
        "https://.../page-1.jpg",
        "https://.../page-2.jpg",
        "https://.../page-3.jpg"
    ],
    
    // PDF 標記
    originalFileType: "application/pdf",
    isPDFConverted: true,
    
    // 處理結果
    processedData: { // 合併後的數據
        bank_name: "香港銀行",
        account_number: "1234567890",
        transactions: [ /* 所有頁面的交易 */ ],
        opening_balance: 1000.00,
        closing_balance: 2000.00,
        total_pages: 3
    },
    
    pageResults: [ // ✅ 每頁的詳細結果
        { data: { /* 第 1 頁結果 */ } },
        { data: { /* 第 2 頁結果 */ } },
        { data: { /* 第 3 頁結果 */ } }
    ]
}
```

---

## 🧪 測試案例

### 測試 1：3 頁銀行對帳單 ✅

```
輸入：
- eStatementFile_20250829143359.pdf（3 頁）

預期輸出：
📄 檢測到 PDF 文件，開始轉換為圖片...
✅ PDF 轉換完成，生成 3 張圖片
📄 將處理所有 3 頁
📤 開始上傳 3 個文件...
✅ 3 個文件已上傳到 Storage
✅ 文檔記錄已創建
💰 已扣除 3 Credits（3 頁）
🤖 開始多頁 AI 處理: 3 頁
📄 處理第 1/3 頁... ✅
📄 處理第 2/3 頁... ✅
📄 處理第 3/3 頁... ✅
✅ 3 頁 AI 處理完成，開始合併結果...
✅ 多頁文檔狀態已更新

結果：
- 文檔狀態：已完成
- 總頁數：3
- 交易記錄：所有 3 頁的交易
- Credits 扣除：3
```

### 測試 2：1 頁發票 ✅

```
輸入：
- invoice.pdf（1 頁）

預期輸出：
📄 檢測到 PDF 文件，開始轉換為圖片...
✅ PDF 轉換完成，生成 1 張圖片
📄 將處理所有 1 頁
📤 開始上傳 1 個文件...
✅ 1 個文件已上傳到 Storage
💰 已扣除 1 Credits（1 頁）
🤖 開始多頁 AI 處理: 1 頁
📄 處理第 1/1 頁... ✅
✅ 1 頁 AI 處理完成，開始合併結果...
✅ 多頁文檔狀態已更新

結果：
- 文檔狀態：已完成
- 總頁數：1
- Credits 扣除：1
```

### 測試 3：圖片文件（非 PDF）✅

```
輸入：
- receipt.jpg

預期輸出：
（跳過 PDF 轉換）
📤 開始上傳 1 個文件...
✅ 1 個文件已上傳到 Storage
💰 已扣除 1 Credits（1 頁）
🤖 開始多頁 AI 處理: 1 頁
📄 處理第 1/1 頁... ✅
✅ 多頁文檔狀態已更新

結果：
- 正常處理（無轉換）
```

---

## 💡 用戶體驗

### 上傳進度顯示

```
1. 上傳中...
   └─ 正在轉換 PDF...（如果是 PDF）
   └─ 正在上傳文件...

2. 處理中...（X%）
   └─ 處理第 1/3 頁...（33%）
   └─ 處理第 2/3 頁...（67%）
   └─ 處理第 3/3 頁...（100%）

3. 已完成 ✅
   └─ 提取了 X 條交易記錄
```

### 文檔列表顯示

```
┌────────────────────────────────────────┐
│ 📄 eStatementFile_202508...pdf (3 頁)  │
│ 銀行對帳單 | 已完成 ✅                 │
│ 期末餘額: $2,000.00                    │
│ 交易記錄: 45 條                        │
└────────────────────────────────────────┘
```

---

## ⚠️ 注意事項

### 1. Vision API 速率限制

```
免費額度：1,000 requests/月
付費額度：1,800 requests/分鐘

建議：
- 順序處理頁面（不並行）
- 避免同時上傳多個大型 PDF
- 監控 API 使用量
```

### 2. Credits 計算

```
計算規則：
- 1 頁 = 1 Credit
- 3 頁 PDF = 3 Credits
- 失敗時退回所有 Credits

防止重複扣除：
✅ 使用 refundedDocuments Set 記錄
✅ 檢查文檔 ID 是否已退回
```

### 3. 處理時間

```
預估時間：
- Vision API OCR: ~2 秒/頁
- DeepSeek 分析: ~3 秒/頁
- 總計: ~5 秒/頁

3 頁 PDF 預估: ~15 秒
10 頁 PDF 預估: ~50 秒
```

---

## 🚀 未來改進

### 選項 1：並行 AI 處理 ⚡

```javascript
// 並行處理多頁（需要更高配額）
const promises = files.map(f => processor.processDocument(f, documentType));
const results = await Promise.all(promises);
```

**優點：** 速度更快  
**缺點：** 可能超過 API 配額

### 選項 2：後台任務隊列 📋

```javascript
// 使用 Cloud Functions + Task Queue
await addToQueue({
    docId: docId,
    imageUrls: imageUrls,
    documentType: documentType
});
```

**優點：** 不阻塞用戶  
**缺點：** 實施複雜度高

### 選項 3：智能分頁 🧠

```javascript
// 只處理包含內容的頁面
const validPages = await detectContentPages(imageFiles);
// 跳過空白頁
```

**優點：** 節省 Credits 和時間  
**缺點：** 需要額外的檢測邏輯

---

## 📊 性能對比

### 之前（只第一頁）

```
3 頁 PDF：
- 處理頁數：1 頁
- 處理時間：~5 秒
- Credits：3（按 PDF 頁數）
- 數據完整性：33%（只有 1/3）
```

### 現在（所有頁面）

```
3 頁 PDF：
- 處理頁數：3 頁
- 處理時間：~15 秒
- Credits：3（按實際頁數）
- 數據完整性：100%（所有頁面）
```

---

## ✅ 總結

### 關鍵改進

1. **數據完整性** ✅
   - 從 33% 提升到 100%（3 頁 PDF）
   - 不再丟失任何頁面數據

2. **Credits 準確性** ✅
   - 精確按實際處理頁數扣除
   - 失敗時正確退回

3. **用戶體驗** ✅
   - 一個 PDF = 一個文檔記錄
   - 實時進度顯示
   - 智能合併結果

4. **技術實現** ✅
   - 並行上傳（速度快）
   - 順序處理（避免配額）
   - 智能合併（根據類型）

---

**立即測試多頁 PDF 處理！** 🎉

上傳您的 3 頁銀行對帳單，體驗完整的數據提取！

