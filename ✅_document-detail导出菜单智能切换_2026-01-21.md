# ✅ document-detail.html 导出菜单智能切换

## 📋 用户需求

用户指出 `document-detail.html` 和 `firstproject.html` 的导出内容不一样：
- `firstproject.html` 已经支持银行对账单和发票的完整导出功能
- `document-detail.html` 只支持银行对账单导出
- 需要更新 `document-detail.html`，使其根据文档类型自动显示对应的导出菜单

**重要**：银行对账单和发票的导出内容是不同的！

---

## ✅ 已完成的更改

### 修改文件
- `document-detail.html` - 更新导出菜单和导出逻辑

### 修改位置
1. **document-detail.html** (第 2870-2975 行) - `openVaultcaddyExportMenuInternal()` 函数
2. **document-detail.html** (第 3158-3312 行) - `vaultcaddyExportDocument()` 函数

---

## 🎯 核心功能：智能菜单切换

### 1️⃣ 自动检测文档类型

```javascript
function openVaultcaddyExportMenuInternal() {
    const menu = document.getElementById('vaultcaddyExportMenu');
    
    // 🔍 检测当前文档类型
    const doc = window.currentDocument;
    const docType = doc?.type || doc?.documentType || '';
    const isInvoice = docType.toLowerCase().includes('invoice');
    
    console.log('📋 文档类型:', docType, '是否发票:', isInvoice);
    
    let menuHTML = '<div style="padding: 0.5rem 0; background: #ffffff;">';
    
    if (isInvoice) {
        // 🧾 显示发票导出菜单
        menuHTML += generateInvoiceExportMenu();
    } else {
        // 🏦 显示银行对账单导出菜单
        menuHTML += generateBankStatementExportMenu();
    }
    
    menu.innerHTML = menuHTML;
    // ... 定位和显示菜单 ...
}
```

---

## 🏦 银行对账单导出菜单

### CSV 格式
1. **🌐 通用 CSV** (推荐，绿色高亮)
   - ✨ Xero, Wave, QuickBooks, MYOB

2. **📄 Sage CSV**
   - 🇬🇧 Sage 50, Sage Accounting

3. **📄 Zoho Books CSV**
   - 🇮🇳 Zoho Books 格式

### 其他格式
4. **☁️ QBO 文件**
   - QuickBooks Online 官方格式

5. **📊 Excel (.xlsx)**
   - Microsoft Excel 試算表

---

## 🧾 发票导出菜单

### CSV 格式
1. **🌐 通用 CSV** (推荐，绿色高亮)
   - ✨ Xero, Wave, QuickBooks, MYOB

2. **📄 Sage CSV**
   - 🇬🇧 Sage 50, Sage Accounting

3. **📄 Zoho Books CSV**
   - 🇮🇳 Zoho Books 格式

### Excel 格式 ✨
4. **標準 Excel（總數）**
   - 快速對帳

5. **完整交易數據 Excel**
   - 詳細記錄

### 其他格式
6. **☁️ QBO 文件**
   - QuickBooks Online 官方格式

---

## 🔧 导出功能实现

### 发票导出格式处理

#### A. 通用 CSV (`invoice_universal_csv`)
```javascript
case 'invoice_universal_csv':
    if (!window.InvoiceExport || !window.InvoiceExport.generateUniversalCSV) {
        alert('發票導出模塊未載入，請刷新頁面後重試');
        return;
    }
    exportContent = window.InvoiceExport.generateUniversalCSV([doc]);
    exportFileName = `Invoice_Universal_${dateStr}.csv`;
    mimeType = 'text/csv;charset=utf-8;';
    break;
```

#### B. Sage CSV (`invoice_sage_csv`)
```javascript
case 'invoice_sage_csv':
    if (!window.InvoiceExport || !window.InvoiceExport.generateSageCSV) {
        alert('發票導出模塊未載入，請刷新頁面後重試');
        return;
    }
    exportContent = window.InvoiceExport.generateSageCSV([doc]);
    exportFileName = `Invoice_Sage_${dateStr}.csv`;
    mimeType = 'text/csv;charset=utf-8;';
    break;
```

#### C. Zoho Books CSV (`invoice_zoho_csv`)
```javascript
case 'invoice_zoho_csv':
    if (!window.InvoiceExport || !window.InvoiceExport.generateZohoCSV) {
        alert('發票導出模塊未載入，請刷新頁面後重試');
        return;
    }
    exportContent = window.InvoiceExport.generateZohoCSV([doc]);
    exportFileName = `Invoice_ZohoBooks_${dateStr}.csv`;
    mimeType = 'text/csv;charset=utf-8;';
    break;
```

#### D. 標準 Excel（總數）(`invoice_summary_excel`)
```javascript
case 'invoice_summary_excel':
    const wb = XLSX.utils.book_new();
    const excelData = [['Invoice Number', 'Date', 'Supplier', 'Amount', 'Tax', 'Status']];
    
    excelData.push([
        data.invoiceNumber || '',
        data.invoiceDate || '',
        data.vendorName || data.supplier || '',
        parseFloat(data.totalAmount || 0).toFixed(2),
        parseFloat(data.taxAmount || 0).toFixed(2),
        data.status || '未付款'
    ]);
    
    const ws = XLSX.utils.aoa_to_sheet(excelData);
    ws['!cols'] = [{wch: 15}, {wch: 12}, {wch: 25}, {wch: 12}, {wch: 10}, {wch: 12}];
    XLSX.utils.book_append_sheet(wb, ws, "Invoice Summary");
    
    XLSX.writeFile(wb, `Invoice_Summary_${dateStr}.xlsx`);
    break;
```

#### E. 完整交易數據 Excel (`invoice_detailed_excel`)
```javascript
case 'invoice_detailed_excel':
    const wb = XLSX.utils.book_new();
    const excelData = [[
        'Invoice Number', 'Date', 'Supplier Name', 'Supplier Phone', 'Supplier Email',
        'Item Code', 'Item Description', 'Quantity', 'Unit', 'Unit Price',
        'Amount', 'Total Amount', 'Tax', 'Status'
    ]];
    
    // 处理每个项目
    const items = data.items || data.lineItems || [];
    
    if (items.length === 0) {
        excelData.push([
            invoiceNumber, invoiceDate, supplierName, supplierPhone, supplierEmail,
            '', '總計', 1, '', totalAmount,
            totalAmount, totalAmount, tax, status
        ]);
    } else {
        items.forEach(item => {
            excelData.push([
                invoiceNumber, invoiceDate, supplierName, supplierPhone, supplierEmail,
                item.code, item.description, item.quantity, item.unit, item.unitPrice,
                item.amount, totalAmount, tax, status
            ]);
        });
    }
    
    const ws = XLSX.utils.aoa_to_sheet(excelData);
    ws['!cols'] = [
        {wch: 15}, {wch: 12}, {wch: 25}, {wch: 15}, {wch: 25},
        {wch: 12}, {wch: 40}, {wch: 10}, {wch: 8}, {wch: 12},
        {wch: 12}, {wch: 12}, {wch: 10}, {wch: 10}
    ];
    XLSX.utils.book_append_sheet(wb, ws, "Invoice Details");
    
    XLSX.writeFile(wb, `Invoice_Detailed_${dateStr}.xlsx`);
    break;
```

---

## 📊 银行对账单 vs 发票导出对比

| 功能 | 银行对账单 | 发票 |
|-----|----------|-----|
| **通用 CSV** | ✅ | ✅ |
| **Sage CSV** | ✅ | ✅ |
| **Zoho Books CSV** | ✅ | ✅ |
| **Excel 汇总** | ❌ | ✅ (6列) |
| **Excel 详细** | ❌ | ✅ (14列) |
| **银行对账单 Excel** | ✅ (13列) | ❌ |
| **QBO 文件** | ✅ | ✅ |

---

## 🔍 关键区别

### 银行对账单
- **Excel格式**：13列，包含交易明细
  - CustomerName, AccountNumber, AccountType, BankName, BankAddress
  - OpeningBalance, EndingBalance
  - LineItems_Date, LineItems_Description, LineItems_Category, LineItems_Credits, LineItems_Debits, LineItems_Balance

### 发票
- **Excel汇总**：6列，每张发票一行
  - Invoice Number, Date, Supplier, Amount, Tax, Status

- **Excel详细**：14列，每个项目一行
  - Invoice Number, Date, Supplier Name, Supplier Phone, Supplier Email
  - Item Code, Item Description, Quantity, Unit, Unit Price
  - Amount, Total Amount, Tax, Status

---

## 🎨 菜单HTML示例

### 发票菜单
```html
<div style="padding: 0.5rem 0; background: #ffffff;">
    <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em;">CSV 格式</div>
    
    <button onclick="vaultcaddyExportDocument('invoice_universal_csv')" class="export-menu-item" style="...">
        <i class="fas fa-globe" style="color: #10b981; width: 20px;"></i>
        <div>
            <div style="font-weight: 600;">🌐 通用 CSV</div>
            <div style="font-size: 0.75rem; color: #059669; font-weight: 500;">✨ Xero, Wave, QuickBooks, MYOB</div>
        </div>
    </button>
    
    <!-- ... 其他CSV格式 ... -->
    
    <div style="padding: 0.5rem 1rem; font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.5rem;">Excel 格式</div>
    
    <button onclick="vaultcaddyExportDocument('invoice_summary_excel')" class="export-menu-item" style="...">
        <i class="fas fa-file-excel" style="color: #059669; width: 20px;"></i>
        <div>
            <div style="font-weight: 500;">標準 Excel（總數）</div>
            <div style="font-size: 0.75rem; color: #6b7280;">快速對帳</div>
        </div>
    </button>
    
    <!-- ... 其他格式 ... -->
</div>
```

---

## 🧪 测试步骤

### 测试银行对账单导出
1. **强制刷新**：`Cmd + Shift + R`
2. 打开银行对账单：`https://vaultcaddy.com/document-detail.html?project=SJJkhY7CFdqh8zyVAM6B&id=vPwfbEF32mLC72EsZsDW`
3. 点击 **Export** 按钮

**预期结果**：
- ✅ 看到 "CSV 格式" 分类
- ✅ 🌐 通用 CSV
- ✅ 📄 Sage CSV
- ✅ 📄 Zoho Books CSV
- ✅ 看到 "其他格式" 分类
- ✅ ☁️ QBO 文件
- ✅ 📊 Excel (.xlsx)
- ❌ **不显示** "Excel 格式" 分类
- ❌ **不显示** "標準 Excel（總數）"
- ❌ **不显示** "完整交易數據 Excel"

### 测试发票导出
1. **强制刷新**：`Cmd + Shift + R`
2. 打开发票：`https://vaultcaddy.com/document-detail.html?project=SJJkhY7CFdqh8zyVAM6B&id=IsaVCQfMCaDyolwDC6xS`
3. 点击 **Export** 按钮

**预期结果**：
- ✅ 看到 "CSV 格式" 分类
- ✅ 🌐 通用 CSV
- ✅ 📄 Sage CSV
- ✅ 📄 Zoho Books CSV
- ✅ 看到 "Excel 格式" 分类
- ✅ 標準 Excel（總數）
- ✅ 完整交易數據 Excel
- ✅ 看到 "其他格式" 分类
- ✅ ☁️ QBO 文件
- ❌ **不显示** "📊 Excel (.xlsx)"（银行对账单专用）

### 测试导出功能
1. 点击任意 CSV 格式
2. 等待下载

**预期结果**：
- ✅ 文件下载成功
- ✅ 文件名包含日期
- ✅ CSV 内容正确

3. 点击 "標準 Excel（總數）"（仅发票）
4. 等待下载

**预期结果**：
- ✅ 下载文件：`Invoice_Summary_2026-01-21.xlsx`
- ✅ 6列格式：Invoice Number, Date, Supplier, Amount, Tax, Status

4. 点击 "完整交易數據 Excel"（仅发票）
5. 等待下载

**预期结果**：
- ✅ 下载文件：`Invoice_Detailed_2026-01-21.xlsx`
- ✅ 14列格式（包含项目明细）

---

## 🎯 优点

### 1️⃣ **智能菜单切换**
- 自动检测文档类型
- 显示对应的导出选项
- 避免用户混淆

### 2️⃣ **完全对齐 firstproject.html**
- 银行对账单：与 firstproject.html 一致
- 发票：与 firstproject.html 一致

### 3️⃣ **专业的分类**
- CSV 格式：适合会计软件导入
- Excel 格式：适合人工审阅（仅发票）
- 其他格式：QBO、Excel（银行对账单）

### 4️⃣ **用户体验优化**
- 清晰的分类标题
- 醒目的图标
- 详细的格式说明
- 推荐提示

---

## 📂 依赖模块

### 发票导出
- `invoice-export.js` - 提供 `window.InvoiceExport`
  - `generateUniversalCSV()`
  - `generateSageCSV()`
  - `generateZohoCSV()`

### 银行对账单导出
- `bank-statement-export.js` - 提供 `window.BankStatementExport`
  - `generateUniversalCSV()`
  - `generateSageCSV()`
  - `generateZohoCSV()`

### Excel库
- SheetJS (XLSX) - 用于生成 `.xlsx` 文件

---

## 🔗 相关文档
- `✅_发票导出完全重构_2026-01-21.md` - 发票导出重构
- `✅_发票导出菜单增强_2026-01-21.md` - 菜单增强
- `invoice-export.js` - 发票导出模块
- `bank-statement-export.js` - 银行对账单导出模块

---

**创建时间**：2026-01-21  
**作者**：VaultCaddy AI Assistant  
**相关文件**：`document-detail.html`

