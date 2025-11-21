# 🚀 Export 功能優化計劃

**日期**: 2025-11-21  
**目標**: 統一和優化 Export 功能

---

## 📋 需求總結

### 1️⃣ 統一 Export 菜單
- ✅ `firstproject.html` 和 `document-detail.html` 使用相同的 Export 菜單
- ✅ 支援所有格式：CSV（通用）、銀行對帳單、發票、QuickBooks

### 2️⃣ 只導出選中的文件
- ✅ 用戶選中 2 個文件 → Export 按鈕顯示 "Export 2"
- ✅ 點擊後只導出這 2 個文件
- ✅ 未選中時 → 導出所有文件

### 3️⃣ 按類型自動分組導出
- ✅ 選中：1個銀行對帳單 + 2個發票
- ✅ 自動生成 2 個 CSV:
  - `BankStatement_2025-11-21.csv`（1個銀行對帳單）
  - `Invoice_2025-11-21.csv`（2個發票）

### 4️⃣ 動態 Export 菜單
- ✅ 根據選中文件的類型，動態顯示相關選項
- ✅ 只選銀行對帳單 → 只顯示銀行對帳單選項
- ✅ 只選發票 → 只顯示發票選項
- ✅ 混合選擇 → 顯示所有相關選項

### 5️⃣ 發票 Export 選項
- ✅ 標準 CSV（總數）：快速對帳
- ✅ 完整交易數據 CSV：詳細記錄

---

## 🎨 Export 菜單設計

### 當前設計（firstproject.html）

```
Export
├─ CSV（通用）
│  └─ 所有文檔類型
├─ 銀行對帳單
│  ├─ 標準 CSV（完整欄位格式）
│  ├─ Xero CSV（官方最小格式）
│  └─ QuickBooks CSV（官方最小格式）
└─ QuickBooks
   ├─ IIF（QuickBooks Desktop）
   └─ QBO（QuickBooks Online）
```

### 新設計（動態菜單）

**場景 1**: 選中 2 個銀行對帳單
```
Export 2
├─ CSV（通用）
├─ 銀行對帳單
│  ├─ 標準 CSV
│  ├─ Xero CSV
│  └─ QuickBooks CSV
└─ QuickBooks
   ├─ IIF
   └─ QBO
```

**場景 2**: 選中 2 個發票
```
Export 2
├─ CSV（通用）
└─ 發票
   ├─ 標準 CSV（總數）
   └─ 完整交易數據 CSV
```

**場景 3**: 選中 1 個銀行對帳單 + 2 個發票
```
Export 3
├─ CSV（通用）
├─ 銀行對帳單
│  ├─ 標準 CSV
│  ├─ Xero CSV
│  └─ QuickBooks CSV
└─ 發票
   ├─ 標準 CSV（總數）
   └─ 完整交易數據 CSV
```

---

## 🛠️ 技術實施

### 步驟 1: 更新 Export 按鈕邏輯

**修改文件**: `firstproject.html`

**功能**: 
- 檢測選中文件數量
- 動態更新按鈕文字

```javascript
function updateExportButton() {
    const selectedDocs = Array.from(window.selectedDocuments || new Set());
    const exportBtn = document.querySelector('[onclick*="toggleExportMenu"]');
    
    if (!exportBtn) return;
    
    if (selectedDocs.length > 0) {
        exportBtn.innerHTML = `<i class="fas fa-download"></i> Export ${selectedDocs.length}`;
    } else {
        exportBtn.innerHTML = `<i class="fas fa-download"></i> Export`;
    }
}
```

---

### 步驟 2: 實施動態 Export 菜單

**修改文件**: `firstproject.html`

**功能**: 
- 根據選中文件類型，動態生成菜單

```javascript
function generateExportMenu() {
    const selectedDocs = Array.from(window.selectedDocuments || new Set());
    
    // 如果沒有選中，使用所有文檔
    const docsToCheck = selectedDocs.length > 0 
        ? allDocuments.filter(doc => selectedDocs.includes(doc.id))
        : allDocuments;
    
    // 檢測文檔類型
    const hasBankStatements = docsToCheck.some(doc => 
        doc.documentType === 'bank_statement' || doc.documentType === 'bank_statements'
    );
    const hasInvoices = docsToCheck.some(doc => 
        doc.documentType === 'invoice' || doc.documentType === 'invoices'
    );
    
    // 動態生成菜單
    let menuHTML = `
        <button onclick="exportDocuments('csv')" class="export-menu-item">
            <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
            <div>
                <div style="font-weight: 500;">CSV（通用）</div>
                <div style="font-size: 0.75rem; color: #6b7280;">所有文檔類型</div>
            </div>
        </button>
    `;
    
    if (hasBankStatements) {
        menuHTML += `
            <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase;">銀行對帳單</div>
            <button onclick="exportDocuments('bank_statement_csv')" class="export-menu-item">
                <i class="fas fa-file-csv" style="color: #10b981; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">標準 CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">完整欄位格式</div>
                </div>
            </button>
            <button onclick="exportDocuments('xero_csv')" class="export-menu-item">
                <i class="fas fa-file-csv" style="color: #2563eb; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">Xero CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">官方最小格式</div>
                </div>
            </button>
            <button onclick="exportDocuments('quickbooks_csv')" class="export-menu-item">
                <i class="fas fa-file-csv" style="color: #059669; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">QuickBooks CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">官方最小格式</div>
                </div>
            </button>
        `;
    }
    
    if (hasInvoices) {
        menuHTML += `
            <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase;">發票</div>
            <button onclick="exportDocuments('invoice_summary_csv')" class="export-menu-item">
                <i class="fas fa-file-csv" style="color: #f59e0b; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">標準 CSV（總數）</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">快速對帳</div>
                </div>
            </button>
            <button onclick="exportDocuments('invoice_detailed_csv')" class="export-menu-item">
                <i class="fas fa-file-csv" style="color: #f59e0b; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">完整交易數據 CSV</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">詳細記錄</div>
                </div>
            </button>
        `;
    }
    
    if (hasBankStatements) {
        menuHTML += `
            <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase;">QUICKBOOKS</div>
            <button onclick="exportDocuments('iif')" class="export-menu-item">
                <i class="fas fa-file" style="color: #2563eb; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">IIF</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">QuickBooks Desktop</div>
                </div>
            </button>
            <button onclick="exportDocuments('qbo')" class="export-menu-item">
                <i class="fas fa-cloud" style="color: #2563eb; width: 20px;"></i>
                <div>
                    <div style="font-weight: 500;">QBO</div>
                    <div style="font-size: 0.75rem; color: #6b7280;">QuickBooks Online</div>
                </div>
            </button>
        `;
    }
    
    return menuHTML;
}
```

---

### 步驟 3: 按類型分組導出

**修改文件**: `firstproject.html`

**功能**: 
- 自動按文檔類型分組
- 生成多個 CSV 文件

```javascript
window.exportDocuments = async function(format) {
    console.log('📤 開始導出:', format);
    
    try {
        // 獲取要導出的文檔
        const selectedDocs = Array.from(window.selectedDocuments || new Set());
        let docsToExport;
        
        if (selectedDocs.length > 0) {
            docsToExport = allDocuments.filter(doc => 
                selectedDocs.includes(doc.id) && 
                doc.status === 'completed' && 
                doc.processedData
            );
        } else {
            docsToExport = allDocuments.filter(doc => 
                doc.status === 'completed' && doc.processedData
            );
        }
        
        if (docsToExport.length === 0) {
            alert('沒有可導出的文檔');
            return;
        }
        
        // 按類型分組
        const groupedDocs = {
            bank_statements: [],
            invoices: [],
            receipts: [],
            general: []
        };
        
        docsToExport.forEach(doc => {
            if (doc.documentType === 'bank_statement' || doc.documentType === 'bank_statements') {
                groupedDocs.bank_statements.push(doc);
            } else if (doc.documentType === 'invoice' || doc.documentType === 'invoices') {
                groupedDocs.invoices.push(doc);
            } else if (doc.documentType === 'receipt' || doc.documentType === 'receipts') {
                groupedDocs.receipts.push(doc);
            } else {
                groupedDocs.general.push(doc);
            }
        });
        
        // 根據格式導出
        switch(format) {
            case 'bank_statement_csv':
            case 'xero_csv':
            case 'quickbooks_csv':
                // 只導出銀行對帳單
                if (groupedDocs.bank_statements.length > 0) {
                    exportByType(groupedDocs.bank_statements, format);
                }
                break;
                
            case 'invoice_summary_csv':
            case 'invoice_detailed_csv':
                // 只導出發票
                if (groupedDocs.invoices.length > 0) {
                    exportByType(groupedDocs.invoices, format);
                }
                break;
                
            case 'csv':
                // 導出所有類型，按類型分組
                if (groupedDocs.bank_statements.length > 0) {
                    exportByType(groupedDocs.bank_statements, 'bank_statement_csv');
                }
                if (groupedDocs.invoices.length > 0) {
                    exportByType(groupedDocs.invoices, 'invoice_summary_csv');
                }
                if (groupedDocs.receipts.length > 0) {
                    exportByType(groupedDocs.receipts, 'receipt_csv');
                }
                if (groupedDocs.general.length > 0) {
                    exportByType(groupedDocs.general, 'general_csv');
                }
                break;
                
            default:
                // 其他格式
                exportByType(docsToExport, format);
        }
        
    } catch (error) {
        console.error('❌ 導出失敗:', error);
        alert('導出失敗: ' + error.message);
    }
};

function exportByType(docs, format) {
    // 實際導出邏輯
    console.log(`📋 導出 ${docs.length} 個文檔，格式: ${format}`);
    
    let exportContent = '';
    let fileName = '';
    let mimeType = '';
    
    // ... 根據 format 生成不同的導出內容 ...
    
    // 下載文件
    const blob = new Blob([exportContent], { type: mimeType });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}
```

---

### 步驟 4: 新增發票 Export 函數

**新建文件**: `invoice-export.js`

**功能**: 
- 生成發票總數 CSV
- 生成發票詳細交易數據 CSV

```javascript
/**
 * VaultCaddy Invoice Export Module
 * 
 * 功能：
 * - 生成發票總數 CSV（快速對帳）
 * - 生成發票詳細交易數據 CSV（詳細記錄）
 * 
 * 作用：幫助用戶快速導出發票數據
 */

(function() {
    'use strict';
    
    /**
     * 生成發票總數 CSV
     */
    function generateInvoiceSummaryCSV(invoices) {
        const headers = ['發票編號', '供應商', '日期', '總金額', '稅額', '狀態'];
        const rows = [headers];
        
        invoices.forEach(invoice => {
            const data = invoice.processedData;
            const row = [
                data.invoiceNumber || '',
                data.vendorName || data.supplier || '',
                data.invoiceDate || data.date || '',
                data.totalAmount || data.total || '0',
                data.taxAmount || data.tax || '0',
                data.status || '已付款'
            ];
            rows.push(row);
        });
        
        return rows.map(row => row.map(escapeCSV).join(',')).join('\n');
    }
    
    /**
     * 生成發票詳細交易數據 CSV
     */
    function generateInvoiceDetailedCSV(invoices) {
        const headers = ['發票編號', '供應商', '日期', '項目名稱', '數量', '單價', '小計', '總金額'];
        const rows = [headers];
        
        invoices.forEach(invoice => {
            const data = invoice.processedData;
            const items = data.items || data.lineItems || [];
            
            items.forEach(item => {
                const row = [
                    data.invoiceNumber || '',
                    data.vendorName || data.supplier || '',
                    data.invoiceDate || data.date || '',
                    item.description || item.itemName || '',
                    item.quantity || '1',
                    item.unitPrice || item.price || '0',
                    item.subtotal || (item.quantity * item.unitPrice) || '0',
                    data.totalAmount || data.total || '0'
                ];
                rows.push(row);
            });
        });
        
        return rows.map(row => row.map(escapeCSV).join(',')).join('\n');
    }
    
    /**
     * Escape CSV 字段
     */
    function escapeCSV(value) {
        if (value === null || value === undefined) return '';
        const str = String(value);
        if (str.includes(',') || str.includes('"') || str.includes('\n')) {
            return `"${str.replace(/"/g, '""')}"`;
        }
        return str;
    }
    
    // 全局暴露
    window.InvoiceExport = {
        generateInvoiceSummaryCSV,
        generateInvoiceDetailedCSV
    };
    
    console.log('✅ InvoiceExport 模塊已載入');
})();
```

---

## 🧪 測試計劃

### 測試場景 1: 只選銀行對帳單

**步驟**:
1. 訪問項目頁面
2. 勾選 2 個銀行對帳單
3. 點擊 "Export 2"
4. 確認菜單只顯示銀行對帳單選項
5. 選擇 "標準 CSV"
6. 確認下載的 CSV 只包含這 2 個文檔

---

### 測試場景 2: 只選發票

**步驟**:
1. 訪問項目頁面
2. 勾選 2 個發票
3. 點擊 "Export 2"
4. 確認菜單只顯示發票選項
5. 選擇 "標準 CSV（總數）"
6. 確認下載的 CSV 格式正確

---

### 測試場景 3: 混合選擇

**步驟**:
1. 訪問項目頁面
2. 勾選 1 個銀行對帳單 + 2 個發票
3. 點擊 "Export 3"
4. 確認菜單顯示所有相關選項
5. 選擇 "CSV（通用）"
6. 確認下載 2 個 CSV:
   - `BankStatement_2025-11-21.csv`（1個）
   - `Invoice_2025-11-21.csv`（2個）

---

## 📊 工作量估算

| 任務 | 時間 | 說明 |
|------|------|------|
| 更新 Export 按鈕邏輯 | 30 分鐘 | 動態顯示選中數量 |
| 實施動態 Export 菜單 | 1 小時 | 根據類型生成菜單 |
| 按類型分組導出 | 1 小時 | 自動分組生成多個文件 |
| 新增發票 Export 函數 | 1 小時 | 總數 + 詳細數據 |
| 統一 document-detail.html | 30 分鐘 | 複製菜單邏輯 |
| 測試與調試 | 1 小時 | 全面測試 |
| **總計** | **5 小時** | |

---

## 🎯 下一步行動

### 立即執行（2 小時）

1. ✅ 更新 `firstproject.html` Export 按鈕邏輯
2. ✅ 實施動態 Export 菜單
3. ✅ 創建 `invoice-export.js`

### 今天完成（3 小時）

4. ✅ 按類型分組導出
5. ✅ 統一 `document-detail.html`
6. ✅ 測試所有場景

---

## 💡 關於 Google Drive/Email 整合

**建議時間表**:

| 階段 | 時間 | 優先級 |
|------|------|--------|
| MVP 核心功能 | 當前 | 🔥 高 |
| Export 優化 | 本週 | 🔥 高 |
| 語言切換完成 | 本週 | 🟡 中 |
| Google Drive 整合 | MVP 後 | 🟢 低 |
| Email 發送 | MVP 後 | 🟢 低 |
| API/Webhook | MVP 後 | 🟢 低 |

**原因**:
- ✅ Google Drive/Email 屬於增值功能
- ✅ MVP 應專注核心價值：AI 處理 + 基本導出
- ✅ 完成 MVP 後，根據用戶反饋決定是否需要

---

**更新日期**: 2025-11-21 下午 2:50

