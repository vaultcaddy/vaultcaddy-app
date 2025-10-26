# 🔧 VaultCaddy 新功能整合指南

## 📋 **已完成的新功能**

### 1. **可編輯表格功能** ✅
- 文件：`editable-table.js`
- 功能：讓用戶可以直接在表格中編輯 AI 提取的數據
- 特性：
  - 可編輯的單元格（inline editing）
  - 自動保存到 LocalStorage
  - 數據驗證（日期、金額格式）
  - 保存狀態指示器
  - 鍵盤導航（Tab, Enter, Escape）

### 2. **可編輯表格樣式** ✅
- 文件：`editable-table.css`
- 特性：
  - 白色主題（參考 LedgerBox 圖3）
  - 編輯中狀態高亮
  - 已修改標記
  - 無效輸入提示
  - 保存指示器動畫

### 3. **導出功能增強** ✅
- 文件：`export-manager.js`（已更新）
- 新增格式：
  - JSON 導出（參考 LedgerBox 圖1）
  - QuickBooks 導出（參考 LedgerBox 圖2）
  - CSV 導出（已有）

---

## 🚀 **如何整合到 document-detail.html**

### **Step 1: 載入新的 JavaScript 和 CSS 文件**

在 `document-detail.html` 的 `<head>` 部分添加：

```html
<!-- 在現有的 CSS 之後添加 -->
<link rel="stylesheet" href="editable-table.css">

<!-- 在現有的 JavaScript 之後添加 -->
<script src="editable-table.js"></script>
<script src="export-manager.js"></script>
```

完整的 `<head>` 部分應該是：

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文檔詳情 - VaultCaddy</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="dashboard.css">
    <link rel="stylesheet" href="pages.css">
    <link rel="stylesheet" href="editable-table.css">  <!-- 新增 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="config.js"></script>
    <script src="translations.js"></script>
    <script src="unified-auth.js"></script>
    <script src="global-auth-sync.js?v=4.0"></script>
    <script src="navbar-component.js?v=4.0"></script>
    <script src="sidebar-component.js?v=4.0"></script>
    <script src="editable-table.js"></script>  <!-- 新增 -->
    <script src="export-manager.js"></script>  <!-- 新增 -->
</head>
```

---

### **Step 2: 更新表格 HTML，添加可編輯屬性**

找到 `displayTransactions()` 函數（約第 1081 行），更新表格行生成代碼：

**原始代碼**：
```javascript
tbody.innerHTML = transactions.map((tx, index) => {
    return `
        <tr>
            <td class="checkbox-cell">
                <input type="checkbox">
            </td>
            <td>${tx.date || '—'}</td>
            <td>${tx.description || '—'}</td>
            <td class="amount-cell">${netAmount >= 0 ? '+' : ''}${netAmount.toFixed(2)}</td>
            <td class="amount-cell">${tx.balance || '—'}</td>
            <td class="action-cell">
                <button class="action-btn delete" onclick="deleteTransaction(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `;
}).join('');
```

**更新為**：
```javascript
tbody.innerHTML = transactions.map((tx, index) => {
    const netAmount = (tx.credit || 0) - (tx.debit || 0);
    
    return `
        <tr data-row-index="${index}">
            <td class="checkbox-cell">
                <input type="checkbox" onchange="updateReconciliationStatus()">
            </td>
            <td data-editable="true" 
                data-field-name="date" 
                data-field-type="date"
                class="editable-cell">
                ${tx.date || '—'}
            </td>
            <td data-editable="true" 
                data-field-name="description" 
                data-field-type="text"
                class="editable-cell">
                ${tx.description || '—'}
            </td>
            <td data-editable="true" 
                data-field-name="amount" 
                data-field-type="amount"
                class="amount-cell editable-cell">
                ${netAmount >= 0 ? '+' : ''}${netAmount.toFixed(2)}
            </td>
            <td data-editable="true" 
                data-field-name="balance" 
                data-field-type="amount"
                class="amount-cell editable-cell">
                ${tx.balance || '—'}
            </td>
            <td class="action-cell">
                <button class="action-btn delete" onclick="deleteTransaction(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `;
}).join('');

// 初始化可編輯表格
if (window.EditableTable) {
    const editableTable = new EditableTable('transactionsBody');
    editableTable.init();
}
```

---

### **Step 3: 添加對帳狀態顯示**

在 `<div class="transactions-section">` 的開頭添加對帳狀態頭部：

**找到**（約第 588 行）：
```html
<div class="transactions-section">
    <div class="transactions-header">
        <h3 class="transactions-title">Transactions</h3>
        <div class="transaction-controls">
            <button class="control-btn">Show Unreconciled</button>
            <button class="control-btn">Toggle All</button>
            <button class="control-btn add">Add Item</button>
        </div>
    </div>
```

**更新為**：
```html
<div class="transactions-section">
    <!-- 對帳狀態頭部（參考 LedgerBox 圖3） -->
    <div class="reconciliation-header">
        <div class="reconciliation-status">
            <span id="reconciliationStatus">0 of 0 transactions reconciled</span>
            <span class="percentage-badge" id="progressBadge">0% Complete</span>
        </div>
    </div>
    
    <div class="transactions-header">
        <h3 class="transactions-title">Transactions</h3>
        <div class="transaction-controls">
            <button class="control-btn" onclick="showUnreconciled()">Show Unreconciled</button>
            <button class="control-btn" onclick="toggleAllTransactions()">Toggle All</button>
            <button class="control-btn add" onclick="addTransaction()">Add Item</button>
        </div>
    </div>
```

---

### **Step 4: 添加導出按鈕和下拉菜單**

在 `<div class="top-actions">` 中添加導出按鈕（約第 129 行）：

**找到**：
```html
<div class="top-actions">
    <div class="saved-indicator" style="display: none;">
        <i class="fas fa-check-circle"></i>
        <span>已保存</span>
    </div>
</div>
```

**更新為**：
```html
<div class="top-actions">
    <!-- 導出按鈕（參考 LedgerBox 圖2） -->
    <div class="export-section">
        <button class="export-btn" onclick="toggleExportMenu()">
            <i class="fas fa-download"></i>
            Export
        </button>
        
        <div class="export-menu" id="exportMenu">
            <h3>Export method</h3>
            <select class="export-method-select" id="exportMethod">
                <option value="">Select method</option>
                <option value="download">Download to computer</option>
                <option value="quickbooks">QuickBooks</option>
            </select>
            
            <div class="export-buttons">
                <button class="export-format-btn" onclick="exportDocument('csv')">
                    <span>CSV</span>
                    <i class="fas fa-file-csv"></i>
                </button>
                <button class="export-format-btn" onclick="exportDocument('quickbooks')">
                    <span>QuickBooks</span>
                    <i class="fas fa-file-invoice"></i>
                </button>
                <button class="export-format-btn" onclick="exportDocument('json')">
                    <span>JSON</span>
                    <i class="fas fa-file-code"></i>
                </button>
            </div>
        </div>
    </div>
    
    <div class="saved-indicator" style="display: none;">
        <i class="fas fa-check-circle"></i>
        <span>已保存</span>
    </div>
</div>
```

---

### **Step 5: 添加 JavaScript 函數**

在 `<script>` 部分的末尾（約第 1370 行之前）添加以下函數：

```javascript
// ========== 導出功能 ==========

function toggleExportMenu() {
    const menu = document.getElementById('exportMenu');
    menu.classList.toggle('show');
}

function exportDocument(format) {
    console.log(`📤 導出文檔為 ${format} 格式...`);
    
    if (!currentDocument) {
        alert('沒有文檔可以導出');
        return;
    }
    
    const exportManager = window.exportManager;
    if (!exportManager) {
        alert('導出功能未載入');
        return;
    }
    
    try {
        let blob;
        let filename;
        
        const documentType = currentDocument.documentType || 'bank-statement';
        const timestamp = new Date().toISOString().split('T')[0];
        
        if (format === 'csv') {
            blob = exportManager.exportBankStatementsToCSV([currentDocument]);
            filename = `${currentDocument.name || 'document'}_${timestamp}.csv`;
        } else if (format === 'quickbooks' || format === 'qbo') {
            blob = exportManager.exportToQBO([currentDocument]);
            filename = `${currentDocument.name || 'document'}_${timestamp}.qbo`;
        } else if (format === 'json') {
            blob = exportManager.exportToJSON([currentDocument], { documentType });
            filename = `${currentDocument.name || 'document'}_${timestamp}.json`;
        }
        
        if (blob) {
            exportManager.downloadFile(blob, filename);
            
            // 關閉導出菜單
            document.getElementById('exportMenu').classList.remove('show');
            
            // 顯示成功消息
            alert(`✅ 文檔已成功導出為 ${format.toUpperCase()} 格式`);
        }
    } catch (error) {
        console.error('❌ 導出失敗:', error);
        alert(`❌ 導出失敗: ${error.message}`);
    }
}

// 點擊外部關閉導出菜單
document.addEventListener('click', function(event) {
    const exportSection = document.querySelector('.export-section');
    if (exportSection && !exportSection.contains(event.target)) {
        document.getElementById('exportMenu').classList.remove('show');
    }
});

// ========== 對帳狀態功能 ==========

function updateReconciliationStatus() {
    if (!currentDocument) return;
    
    const checkboxes = document.querySelectorAll('.transactions-table tbody input[type="checkbox"]');
    const total = checkboxes.length;
    const reconciled = Array.from(checkboxes).filter(cb => cb.checked).length;
    const percentage = total > 0 ? Math.round((reconciled / total) * 100) : 0;
    
    // 更新顯示
    document.getElementById('reconciliationStatus').textContent = 
        `${reconciled} of ${total} transactions reconciled`;
    
    const progressBadge = document.getElementById('progressBadge');
    progressBadge.textContent = `${percentage}% Complete`;
    
    // 更新樣式
    if (percentage === 100) {
        progressBadge.classList.add('complete');
    } else {
        progressBadge.classList.remove('complete');
    }
    
    // 保存對帳狀態到 LocalStorage
    saveReconciliationStatus(reconciled, total, percentage);
}

function saveReconciliationStatus(reconciled, total, percentage) {
    const params = new URLSearchParams(window.location.search);
    const documentId = params.get('id');
    const projectId = params.get('project');
    
    if (!documentId || !projectId) return;
    
    const storageKey = `vaultcaddy_project_${projectId}_files`;
    const filesData = localStorage.getItem(storageKey);
    
    if (!filesData) return;
    
    const files = JSON.parse(filesData);
    const fileIndex = files.findIndex(f => f.id === documentId);
    
    if (fileIndex === -1) return;
    
    files[fileIndex].reconciledTransactions = reconciled;
    files[fileIndex].totalTransactions = total;
    files[fileIndex].reconciliationPercentage = percentage;
    
    localStorage.setItem(storageKey, JSON.stringify(files));
}

function showUnreconciled() {
    const rows = document.querySelectorAll('.transactions-table tbody tr');
    rows.forEach(row => {
        const checkbox = row.querySelector('input[type="checkbox"]');
        if (checkbox && checkbox.checked) {
            row.style.display = 'none';
        } else {
            row.style.display = '';
        }
    });
}

function toggleAllTransactions() {
    const checkboxes = document.querySelectorAll('.transactions-table tbody input[type="checkbox"]');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    
    checkboxes.forEach(cb => {
        cb.checked = !allChecked;
    });
    
    updateReconciliationStatus();
}

function addTransaction() {
    alert('添加交易功能即將推出！');
    // TODO: 實現添加交易功能
}

// 使函數全局可用
window.toggleExportMenu = toggleExportMenu;
window.exportDocument = exportDocument;
window.updateReconciliationStatus = updateReconciliationStatus;
window.showUnreconciled = showUnreconciled;
window.toggleAllTransactions = toggleAllTransactions;
window.addTransaction = addTransaction;
```

---

## ✅ **完成檢查清單**

整合完成後，請檢查以下功能是否正常工作：

### **可編輯表格**
- [ ] 點擊單元格可以編輯
- [ ] Tab 鍵可以移動到下一個單元格
- [ ] Enter 鍵可以移動到下一行
- [ ] Escape 鍵可以取消編輯
- [ ] 編輯後自動保存（1 秒後）
- [ ] 顯示保存指示器
- [ ] 日期格式驗證
- [ ] 金額格式驗證

### **對帳狀態**
- [ ] 顯示對帳狀態（X of Y transactions reconciled）
- [ ] 顯示進度百分比（X% Complete）
- [ ] 勾選框可以更新對帳狀態
- [ ] "Show Unreconciled" 按鈕可以篩選未對帳交易
- [ ] "Toggle All" 按鈕可以全選/取消全選

### **導出功能**
- [ ] 點擊 "Export" 按鈕顯示下拉菜單
- [ ] 可以選擇導出方法（Download to computer / QuickBooks）
- [ ] 可以導出 CSV 格式
- [ ] 可以導出 QuickBooks 格式
- [ ] 可以導出 JSON 格式
- [ ] 導出後自動下載文件
- [ ] 點擊外部關閉下拉菜單

---

## 🎨 **樣式預覽**

### **可編輯單元格**
- **正常狀態**：白色背景
- **懸停狀態**：淺灰色背景 (#f9fafb)
- **編輯中**：藍色邊框 (#3b82f6)
- **已修改**：黃色背景 (#fef3c7) + 橙色圓點
- **無效輸入**：紅色背景 (#fee2e2) + 紅色邊框

### **保存指示器**
- **保存中**：藍色 + 旋轉圖標
- **已保存**：綠色 + 勾選圖標

### **對帳狀態**
- **未完成**：灰色背景 (#f3f4f6)
- **已完成**：綠色背景 (#d1fae5)

---

## 📝 **測試步驟**

1. **測試可編輯功能**：
   - 打開 `document-detail.html?id=xxx&project=yyy`
   - 點擊任意單元格
   - 輸入新值
   - 按 Tab 或 Enter
   - 檢查是否顯示保存指示器
   - 刷新頁面，檢查數據是否保存

2. **測試對帳狀態**：
   - 勾選幾個交易的勾選框
   - 檢查對帳狀態是否更新
   - 點擊 "Show Unreconciled"
   - 檢查是否只顯示未對帳的交易

3. **測試導出功能**：
   - 點擊 "Export" 按鈕
   - 選擇 "Download to computer"
   - 點擊 "CSV" 按鈕
   - 檢查是否下載 CSV 文件
   - 用 Excel 打開 CSV 文件，檢查數據是否正確

---

## 🐛 **常見問題**

### **Q1: 點擊單元格無法編輯**
**A**: 檢查是否正確載入 `editable-table.js` 和初始化 `EditableTable`

### **Q2: 保存指示器不顯示**
**A**: 檢查是否正確載入 `editable-table.css`

### **Q3: 導出功能不工作**
**A**: 檢查是否正確載入 `export-manager.js` 和 `window.exportManager` 是否存在

### **Q4: 對帳狀態不更新**
**A**: 檢查 `updateReconciliationStatus()` 函數是否正確綁定到勾選框的 `onchange` 事件

---

## 🚀 **下一步**

完成整合後，你可以：

1. **測試所有功能**
2. **收集用戶反饋**
3. **優化 UI/UX**
4. **添加更多導出格式**（Excel, Xero, etc.）
5. **實現批量編輯功能**
6. **添加撤銷/重做功能**

---

**祝你整合順利！** 🎉

