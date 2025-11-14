# 🏦 銀行對帳單優化方案

## 📋 問題分析

### 問題 1：銀行對帳單處理失敗

**當前狀態：**
- ❌ 圖1：銀行對帳單（eStatementFile_20250829143359.pdf）處理失敗
- ✅ 圖2-3：收據處理成功

**原因分析：**
1. 銀行對帳單格式複雜（表格、多頁、混合內容）
2. AI 提示詞不適合銀行對帳單
3. OCR 提取困難（表格結構）

---

### 問題 2：目錄設計

**您的建議：** 根據文檔類型動態調整目錄名稱 ✅

**示例：**
- **發票/收據：** 供應商/來源
- **銀行對帳單：** Balance Info

**實施方案：** 動態顯示欄位名稱

---

## 🎯 解決方案

### 方案 1：參考 LedgerBox 的銀行對帳單 UI

**LedgerBox 的設計（圖4-5）：**

```
左側：PDF 預覽（可翻頁 1 of 3）
右側：
  ├── Reconciliation Status（0 of 14 transactions reconciled）
  ├── Bank Statement Details & Notes
  │   ├── Statement Period: 02/01/2025 to 03/22/2025
  │   ├── Balance Info: Start $121,080.49, End $30,188.66
  │   └── Status: Success / Review
  │
  └── Transactions（14 transactions）
      ├── Show Unreconciled / Toggle All
      ├── Date | Description | Amount | Balance
      ├── 02/22/2025 | B/F BALANCE | 0 | 1493.98
      ├── 02/26/2025 | CREDIT INTEREST | 2.61 | 1496.59
      └── ... (更多交易)
```

**關鍵特點：**
1. ✅ 清晰的期間顯示（Statement Period）
2. ✅ 期初/期末餘額（Balance Info）
3. ✅ 交易列表（可勾選、可搜索）
4. ✅ Reconciliation 狀態

---

### 方案 2：優化我們的銀行對帳單 UI

**當前 UI（收據/發票）：**
```
左側：PDF 預覽
右側：
  ├── 發票詳情
  │   ├── 發票號碼
  │   ├── 日期
  │   ├── 供應商
  │   └── 總金額
  │
  └── 項目明細（可編輯）
```

**優化後 UI（銀行對帳單）：**
```
左側：PDF 預覽（支持翻頁）
右側：
  ├── 銀行對帳單詳情
  │   ├── 銀行名稱：恆生銀行
  │   ├── 賬戶號碼：766-452064-882
  │   ├── 賬戶名稱：MR YEUNG CAVLIN
  │   ├── 對帳單期間：02/01/2025 - 03/22/2025
  │   ├── 期初餘額：$121,080.49
  │   ├── 期末餘額：$30,188.66
  │   └── 交易數量：14 筆
  │
  └── 交易記錄（可編輯）
      ├── 日期 | 描述 | 類型 | 金額 | 餘額
      ├── 02/22/2025 | B/F BALANCE | Debit | 0 | 1493.98
      ├── 02/26/2025 | CREDIT INTEREST | Credit | 2.61 | 1496.59
      └── ... (更多交易)
```

---

### 方案 3：動態調整目錄名稱

**實施方案：** 根據文檔類型動態顯示欄位

#### 選項 A：使用統一欄位名（推薦）

**優點：**
- ✅ 簡化 UI 設計
- ✅ 減少用戶困惑
- ✅ 易於維護

**實施：**

| 欄位名稱 | 發票/收據 | 銀行對帳單 | 通用文檔 |
|---------|---------|-----------|---------|
| **供應商/來源** | 供應商名稱 | 銀行名稱 | 來源 |
| **編號** | 發票號/收據號 | 賬戶號碼 | 文檔編號 |
| **日期** | 發票日期 | 對帳單期間 | 文檔日期 |
| **金額** | 總金額 | 期末餘額 | 金額 |

**示例（圖1 的表格）：**

**發票/收據：**
```
文檔名稱 | 類型 | 供應商/來源 | 金額 | 日期 | 狀態
ae2eb358... | 發票 | 美亞食品貿易有限公司 | $5,383.40 | 2025-11-01 | 已完成
```

**銀行對帳單：**
```
文檔名稱 | 類型 | 供應商/來源 | 金額 | 日期 | 狀態
eStatementFile... | 銀行對帳單 | 恆生銀行 | $30,188.66 | 02/01-03/22 | 失敗
```

---

#### 選項 B：使用動態欄位名（您的建議）

**優點：**
- ✅ 更精確的欄位名稱
- ✅ 專業性更強

**缺點：**
- ⚠️ UI 需要動態調整
- ⚠️ 開發複雜度增加

**實施：**

```javascript
// 根據文檔類型動態調整表頭
function getColumnHeaders(documentType) {
    switch(documentType) {
        case 'invoice':
        case 'receipt':
            return {
                col1: '文檔名稱',
                col2: '類型',
                col3: '供應商/來源',
                col4: '金額',
                col5: '日期',
                col6: '狀態'
            };
        case 'bank_statement':
            return {
                col1: '文檔名稱',
                col2: '類型',
                col3: '銀行名稱',
                col4: '期末餘額',
                col5: '對帳單期間',
                col6: '狀態'
            };
        default:
            return {
                col1: '文檔名稱',
                col2: '類型',
                col3: '來源',
                col4: '金額',
                col5: '日期',
                col6: '狀態'
            };
    }
}
```

---

## 💻 實施代碼

### 步驟 1：優化銀行對帳單 AI 提示詞

修改 `hybrid-vision-deepseek-optimized.js`：

```javascript
generateOptimizedSystemPrompt(documentType) {
    const base = 'Extract data from OCR text. Return JSON only, no markdown.';
    
    const fields = {
        invoice: '{inv_no,date,supplier,customer,total,tax,items:[{desc,qty,price}]}',
        receipt: '{merchant,date,total,tax,items:[{desc,price}],payment}',
        // 優化銀行對帳單提示詞（更詳細）
        statement: `{
            bank: "bank name",
            account: "account number",
            account_name: "account holder name",
            period: "statement period (from - to)",
            opening_balance: number,
            closing_balance: number,
            transactions: [{
                date: "YYYY-MM-DD",
                description: "transaction description",
                type: "debit/credit",
                amount: number,
                balance: number
            }]
        }`,
        general: '{type,title,date,entities,amounts,summary}'
    };
    
    // 銀行對帳單特殊處理
    if (documentType === 'statement' || documentType === 'bank_statements') {
        return `${base}\n\nExtract bank statement data from OCR text.\n\nRequired fields:\n${fields.statement}\n\nImportant:\n- Extract ALL transactions from the statement\n- Include opening and closing balance\n- Capture account number and bank name\n- Format dates as YYYY-MM-DD\n- Amount should be positive for credits, negative for debits`;
    }
    
    return `${base}\nSchema: ${fields[documentType] || fields.general}`;
}

// 清理 OCR 文本時保留表格結構
cleanOcrText(rawText) {
    if (!rawText) return '';
    
    let cleaned = rawText
        // 保留表格結構（不完全移除換行）
        .replace(/\s+/g, ' ')
        .replace(/(\r\n|\n|\r){5,}/g, '\n\n')  // 只移除多於 4 個的換行
        .trim();
    
    // 對於銀行對帳單，保留更多內容
    const maxLength = this.documentType === 'statement' ? 5000 : 3000;
    
    if (cleaned.length > maxLength) {
        console.warn(`⚠️ OCR 文本過長，截斷到 ${maxLength} 字符`);
        cleaned = cleaned.slice(0, maxLength) + '...';
    }
    
    return cleaned;
}
```

---

### 步驟 2：創建銀行對帳單專用 UI 組件

創建 `document-detail-statement.html` 或在現有 `document-detail.html` 中添加：

```html
<!-- 銀行對帳單專用顯示 -->
<div id="statementDetails" style="display: none;">
    <h3>銀行對帳單詳情</h3>
    
    <!-- 基本信息 -->
    <div class="statement-info">
        <div class="info-row">
            <label>銀行名稱：</label>
            <span id="bankName"></span>
        </div>
        <div class="info-row">
            <label>賬戶號碼：</label>
            <span id="accountNumber"></span>
        </div>
        <div class="info-row">
            <label>賬戶名稱：</label>
            <span id="accountName"></span>
        </div>
        <div class="info-row">
            <label>對帳單期間：</label>
            <span id="statementPeriod"></span>
        </div>
        <div class="info-row">
            <label>期初餘額：</label>
            <span id="openingBalance" class="amount"></span>
        </div>
        <div class="info-row">
            <label>期末餘額：</label>
            <span id="closingBalance" class="amount"></span>
        </div>
        <div class="info-row">
            <label>交易數量：</label>
            <span id="transactionCount"></span>
        </div>
    </div>
    
    <!-- 交易記錄表格 -->
    <h4>交易記錄</h4>
    <table class="transactions-table">
        <thead>
            <tr>
                <th>日期</th>
                <th>描述</th>
                <th>類型</th>
                <th>金額</th>
                <th>餘額</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody id="transactionsTableBody">
            <!-- 動態填充 -->
        </tbody>
    </table>
</div>

<style>
.statement-info {
    background: #f9fafb;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
}

.info-row {
    display: flex;
    padding: 0.5rem 0;
    border-bottom: 1px solid #e5e7eb;
}

.info-row label {
    font-weight: 500;
    width: 150px;
    color: #374151;
}

.info-row span {
    flex: 1;
    color: #6b7280;
}

.amount {
    font-weight: 600;
    color: #10b981;
}

.transactions-table {
    width: 100%;
    border-collapse: collapse;
}

.transactions-table th {
    background: #f3f4f6;
    padding: 0.75rem;
    text-align: left;
    font-weight: 500;
    border-bottom: 2px solid #d1d5db;
}

.transactions-table td {
    padding: 0.75rem;
    border-bottom: 1px solid #e5e7eb;
}

.transactions-table tr:hover {
    background: #f9fafb;
}
</style>
```

---

### 步驟 3：動態調整項目列表欄位

修改 `firstproject.html` 的 `renderDocuments()` 函數：

```javascript
function renderDocuments(docs) {
    const tbody = document.getElementById('documentsTableBody');
    if (!tbody) return;
    
    // 檢查是否所有文檔都是同一類型
    const types = [...new Set(docs.map(doc => doc.type))];
    const isSingleType = types.length === 1;
    
    // 動態調整表頭
    if (isSingleType && types[0] === 'bank_statements') {
        // 銀行對帳單專用表頭
        updateTableHeaders({
            col3: '銀行名稱',
            col4: '期末餘額',
            col5: '對帳單期間'
        });
    } else {
        // 默認表頭
        updateTableHeaders({
            col3: '供應商/來源',
            col4: '金額',
            col5: '日期'
        });
    }
    
    // 渲染文檔行
    tbody.innerHTML = docs.map(doc => {
        const data = doc.processedData || {};
        
        // 根據文檔類型提取不同欄位
        let col3Value, col4Value, col5Value;
        
        if (doc.type === 'bank_statements') {
            col3Value = data.bank_name || data.bank || '-';
            col4Value = data.closing_balance || data.closingBalance || '-';
            col5Value = data.statement_period || data.period || '-';
        } else {
            col3Value = data.supplier || data.vendor || data.merchantName || data.source || '-';
            col4Value = data.total || data.totalAmount || data.amount || '-';
            col5Value = data.date || data.invoiceDate || data.transactionDate || '-';
        }
        
        return `
            <tr onclick="viewDocument('${doc.id}')">
                <td><input type="checkbox" data-doc-id="${doc.id}" onclick="event.stopPropagation(); toggleDocumentSelection('${doc.id}', event);"></td>
                <td>${doc.fileName || doc.name}</td>
                <td>${getDocumentTypeLabel(doc.type)}</td>
                <td>${col3Value}</td>
                <td>${col4Value}</td>
                <td>${col5Value}</td>
                <td>${getStatusBadge(doc.status)}</td>
                <td>${doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : ''}</td>
                <td>
                    <button onclick="event.stopPropagation(); deleteDocument('${doc.id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

function updateTableHeaders(headers) {
    // 更新表頭欄位名稱
    const headerRow = document.querySelector('#documentsTable thead tr');
    if (!headerRow) return;
    
    const ths = headerRow.querySelectorAll('th');
    if (headers.col3) ths[3].textContent = headers.col3;
    if (headers.col4) ths[4].textContent = headers.col4;
    if (headers.col5) ths[5].textContent = headers.col5;
}
```

---

## 🎯 推薦方案

### 我的建議：選項 A（統一欄位名）

**原因：**
1. ✅ 簡化實施（減少開發時間）
2. ✅ 用戶體驗一致（減少混淆）
3. ✅ 易於維護（單一代碼路徑）
4. ✅ 「供應商/來源」可以涵蓋所有情況：
   - 發票 → 供應商
   - 收據 → 商家
   - 銀行對帳單 → 銀行
   - 通用文檔 → 來源

**但是，如果您想要更專業的顯示：**
- 可以在**詳情頁**使用專業術語
- 在**列表頁**使用統一術語

**示例：**
```
列表頁（統一）：
文檔名稱 | 類型 | 供應商/來源 | 金額 | 日期

詳情頁（專業）：
- 發票：供應商名稱、客戶名稱、發票號碼
- 收據：商家名稱、付款方式、收據號碼
- 銀行對帳單：銀行名稱、賬戶號碼、對帳單期間
```

---

## 📋 實施清單

### 高優先級（今天）

- [ ] **1. 優化銀行對帳單 AI 提示詞**
  - 修改 `hybrid-vision-deepseek-optimized.js`
  - 添加詳細的銀行對帳單提示詞
  - 保留更多 OCR 文本（5000 字符）

- [ ] **2. 測試銀行對帳單處理**
  - 重新上傳圖6-8 的 PDF
  - 檢查提取結果
  - 驗證交易記錄

---

### 中優先級（本週）

- [ ] **3. 實施銀行對帳單 UI**
  - 創建專用顯示組件
  - 顯示期初/期末餘額
  - 顯示交易列表

- [ ] **4. 決定欄位命名方案**
  - 選項 A：統一欄位名（推薦）
  - 選項 B：動態欄位名（您的建議）

---

## 💡 您的決定

**請告訴我：**

1. **欄位命名方案：**
   - 🔴 選項 A：統一使用「供應商/來源」（推薦）
   - 🟡 選項 B：根據類型動態調整（例如「銀行名稱」）

2. **優先級：**
   - 先修復銀行對帳單處理？
   - 先實施 UI 改進？
   - 還是兩者同時進行？

請告訴我您的選擇，我會立即實施！🚀

