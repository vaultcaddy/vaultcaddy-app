# 🔧 Export 功能修復與優化

## 問題列表

### 1. ✅ Export 只導出已勾選的文件
**當前問題：** 點擊 Export 導出所有文件，而非只導出已勾選的文件

**解決方案：** 修改導出邏輯，檢查 `selectedDocuments` 集合

---

### 2. ✅ 圖1（文檔詳情頁）添加更多標題欄位
**當前問題：** 圖1 只有基本欄位，缺少：發票號碼、發票日期、供應商名稱、項目描述、數量、單價等

**解決方案：** 根據文檔類型顯示相應欄位

---

### 3. ✅ 發票和收據是否需要分開？
**問題：** 圖2 中發票和收據看起來差不多，用戶是否需要分成兩個類型？

**分析：**

#### 發票（Invoice）特點：
- 供應商 → 客戶（B2B）
- 有客戶名稱、客戶地址
- 有付款條款（Net 30、Net 60）
- 有到期日
- 通常有發票號碼（INV-xxxx）
- 用於應收賬款管理

#### 收據（Receipt）特點：
- 商家 → 消費者（B2C）
- 沒有客戶名稱（只有消費者）
- 即時付款（現金、信用卡）
- 有付款方式、卡號後4位
- 有時間（不只日期）
- 用於費用報銷

**建議：** **合併為「發票/收據」一個類型**

**原因：**
1. ✅ 簡化用戶選擇（減少困惑）
2. ✅ 數據結構相似（都有項目明細）
3. ✅ AI 可以自動識別是發票還是收據
4. ✅ 導出時根據實際數據決定欄位

---

### 4. ✅ 銀行對帳單處理失敗
**問題：** 圖3 顯示銀行對帳單處理失敗

**可能原因：**
1. OCR 提取失敗（文字模糊）
2. AI 無法識別銀行對帳單格式
3. 提示詞不適合銀行對帳單

**解決方案：** 優化銀行對帳單提示詞

---

### 5. ✅ 收據顯示內容優化
**問題：** 圖4 收據的顯示內容需要優化

**解決方案：** 統一發票/收據的顯示格式

---

### 6. ✅ Email 驗證碼問題
**問題：** 圖5 無法重新發送驗證碼，也沒有收到 email

**可能原因：**
1. Cloud Functions 的 Nodemailer 配置問題
2. Gmail App Password 未正確設置
3. 驗證碼已過期但按鈕未啟用

---

## 🔧 修復代碼

### 修復 1：Export 只導出已勾選的文件

在 `firstproject.html` 中找到導出按鈕的事件處理，修改為：

```javascript
// 修改導出函數，只導出已勾選的文件
function exportDocuments(format) {
    // 獲取已勾選的文件
    const selectedDocs = Array.from(window.selectedDocuments || new Set());
    
    if (selectedDocs.length === 0) {
        // 如果沒有勾選，提示用戶
        alert('請先勾選要導出的文件');
        return;
    }
    
    // 過濾出已勾選的文檔
    const docsToExport = window.allDocuments.filter(doc => selectedDocs.includes(doc.id));
    
    console.log(`📤 導出 ${docsToExport.length} 個已勾選的文件`);
    
    // 根據格式導出
    switch(format) {
        case 'csv':
            const csv = generateCSV(docsToExport);
            downloadFile(csv, 'vaultcaddy_export.csv', 'text/csv');
            break;
        case 'iif':
            const iif = generateIIF(docsToExport);
            downloadFile(iif, 'vaultcaddy_export.iif', 'text/plain');
            break;
        case 'qbo':
            const qbo = generateQBO(docsToExport);
            downloadFile(qbo, 'vaultcaddy_export.qbo', 'application/xml');
            break;
    }
}

// 下載文件輔助函數
function downloadFile(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}
```

---

### 修復 2：合併發票和收據為一個類型

修改 `export-optimizer.js`：

```javascript
/**
 * 發票/收據專用 CSV 格式（合併版）
 */
static generateInvoiceReceiptCSV(docs) {
    const headers = [
        '文檔名稱',
        '編號',
        '日期',
        '時間',
        '供應商/商家',
        '供應商地址',
        '供應商電話',
        '供應商電郵',
        '客戶名稱',
        '客戶地址',
        '項目代碼',
        '項目描述',
        '項目類別',
        '數量',
        '單位',
        '單價',
        '項目金額',
        '小計',
        '服務費',
        '稅額',
        '稅率',
        '總金額',
        '幣別',
        '付款方式',
        '卡號後4位',
        '付款條款',
        '到期日',
        '備註',
        '上傳日期'
    ];
    
    const rows = [headers.join(',')];
    
    docs.forEach(doc => {
        const data = doc.processedData || {};
        const uploadDate = doc.uploadedAt ? new Date(doc.uploadedAt).toLocaleDateString('zh-TW') : '';
        
        // 如果有項目明細，每個項目一行
        if (data.items && Array.isArray(data.items) && data.items.length > 0) {
            data.items.forEach((item, index) => {
                const row = [
                    `"${this.escape(doc.fileName || doc.name)}"`,
                    // 編號（發票號或收據號）
                    data.invoice_number || data.invoiceNumber || data.receipt_number || data.receiptNumber || '',
                    // 日期
                    data.date || data.invoice_date || data.invoiceDate || '',
                    // 時間（收據才有）
                    data.time || '',
                    // 供應商/商家（統一欄位）
                    `"${this.escape(data.supplier || data.vendor || data.merchant_name || data.merchantName)}"`,
                    // 供應商地址
                    `"${this.escape(data.supplier_address || data.vendorAddress || data.merchant_address || data.merchantAddress)}"`,
                    // 供應商電話
                    data.supplier_phone || data.vendorPhone || data.merchant_phone || data.merchantPhone || '',
                    // 供應商電郵
                    data.supplier_email || data.vendorEmail || '',
                    // 客戶名稱（發票才有）
                    `"${this.escape(data.customer || data.customerName)}"`,
                    // 客戶地址（發票才有）
                    `"${this.escape(data.customer_address || data.customerAddress)}"`,
                    // 項目代碼
                    item.code || item.product_code || item.productCode || '',
                    // 項目描述
                    `"${this.escape(item.description || item.desc || item.name)}"`,
                    // 項目類別（收據才有）
                    item.category || '',
                    // 數量
                    item.quantity || item.qty || 1,
                    // 單位
                    item.unit || '件',
                    // 單價
                    item.unit_price || item.unitPrice || item.price || 0,
                    // 項目金額
                    item.amount || item.total || item.subtotal || 0,
                    // 小計（只在第一行顯示）
                    index === 0 ? (data.subtotal || data.subTotal || '') : '',
                    // 服務費（收據才有，只在第一行顯示）
                    index === 0 ? (data.service_charge || data.serviceCharge || '') : '',
                    // 稅額（只在第一行顯示）
                    index === 0 ? (data.tax || data.taxAmount || '') : '',
                    // 稅率（只在第一行顯示）
                    index === 0 ? (data.tax_rate || data.taxRate || '') : '',
                    // 總金額（只在第一行顯示）
                    index === 0 ? (data.total || data.totalAmount || '') : '',
                    // 幣別（只在第一行顯示）
                    index === 0 ? (data.currency || 'HKD') : '',
                    // 付款方式（只在第一行顯示）
                    index === 0 ? (data.payment_method || data.paymentMethod || '') : '',
                    // 卡號後4位（收據才有，只在第一行顯示）
                    index === 0 ? (data.card_last_4_digits || data.cardLast4 || '') : '',
                    // 付款條款（發票才有，只在第一行顯示）
                    index === 0 ? `"${this.escape(data.payment_terms || data.paymentTerms)}"` : '',
                    // 到期日（發票才有，只在第一行顯示）
                    index === 0 ? (data.due_date || data.dueDate || '') : '',
                    // 備註（只在第一行顯示）
                    index === 0 ? `"${this.escape(data.notes || data.memo)}"` : '',
                    // 上傳日期（只在第一行顯示）
                    index === 0 ? uploadDate : ''
                ];
                rows.push(row.join(','));
            });
        } else {
            // 沒有項目明細
            const row = [
                `"${this.escape(doc.fileName || doc.name)}"`,
                data.invoice_number || data.invoiceNumber || data.receipt_number || data.receiptNumber || '',
                data.date || data.invoice_date || data.invoiceDate || '',
                data.time || '',
                `"${this.escape(data.supplier || data.vendor || data.merchant_name || data.merchantName)}"`,
                `"${this.escape(data.supplier_address || data.vendorAddress || data.merchant_address || data.merchantAddress)}"`,
                data.supplier_phone || data.vendorPhone || data.merchant_phone || data.merchantPhone || '',
                data.supplier_email || data.vendorEmail || '',
                `"${this.escape(data.customer || data.customerName)}"`,
                `"${this.escape(data.customer_address || data.customerAddress)}"`,
                '', '', '', '', '', '', '',
                data.subtotal || data.subTotal || '',
                data.service_charge || data.serviceCharge || '',
                data.tax || data.taxAmount || '',
                data.tax_rate || data.taxRate || '',
                data.total || data.totalAmount || '',
                data.currency || 'HKD',
                data.payment_method || data.paymentMethod || '',
                data.card_last_4_digits || data.cardLast4 || '',
                `"${this.escape(data.payment_terms || data.paymentTerms)}"`,
                data.due_date || data.dueDate || '',
                `"${this.escape(data.notes || data.memo)}"`,
                uploadDate
            ];
            rows.push(row.join(','));
        }
    });
    
    return rows.join('\n');
}

// 更新 generateTypedCSV 函數
static generateTypedCSV(docs, type) {
    const normalizedType = (type || '').toLowerCase();
    
    // 發票和收據使用同一格式
    if (normalizedType.includes('receipt') || normalizedType.includes('invoice') || 
        normalizedType === 'receipts' || normalizedType === 'invoices') {
        return this.generateInvoiceReceiptCSV(docs);
    } else if (normalizedType.includes('statement') || normalizedType === 'bank_statements') {
        return this.generateStatementCSV(docs);
    } else if (normalizedType === 'general') {
        return this.generateGeneralCSV(docs);
    } else {
        return this.generateMixedCSV(docs);
    }
}
```

---

### 修復 3：優化銀行對帳單處理

修改 `hybrid-vision-deepseek-optimized.js`：

```javascript
generateOptimizedSystemPrompt(documentType) {
    const base = 'Extract data from OCR text. Return JSON only, no markdown.';
    
    const fields = {
        invoice: '{inv_no,date,supplier,customer,total,tax,items:[{desc,qty,price}]}',
        receipt: '{merchant,date,total,tax,items:[{desc,price}],payment}',
        // 優化銀行對帳單提示詞
        statement: '{bank,account,period,open_bal,close_bal,txs:[{date,desc,type,amt,bal}]}',
        general: '{type,title,date,entities,amounts,summary}'
    };
    
    // 銀行對帳單特殊處理
    if (documentType === 'statement' || documentType === 'bank_statements') {
        return `${base}\nExtract bank statement data.\nSchema: ${fields.statement}\nNote: txs = transactions array with date, description, type (debit/credit), amount, balance`;
    }
    
    return `${base}\nSchema: ${fields[documentType] || fields.general}`;
}
```

---

### 修復 4：Email 驗證碼問題

檢查 Cloud Functions 配置：

```bash
# 檢查 email 配置
firebase functions:config:get

# 如果沒有配置，重新設置
firebase functions:config:set email.user="vaultcaddy@gmail.com"
firebase functions:config:set email.password="你的Gmail App Password"

# 重新部署
firebase deploy --only functions
```

修改 `verify-email.html` 的重新發送邏輯：

```javascript
// 修復重新發送按鈕
async function resendCode() {
    const email = new URLSearchParams(window.location.search).get('email');
    
    if (!email) {
        showNotification('錯誤：找不到電子郵件地址', 'error');
        return;
    }
    
    // 禁用按鈕並顯示加載狀態
    const resendBtn = document.getElementById('resend-btn');
    resendBtn.disabled = true;
    resendBtn.textContent = '發送中...';
    
    try {
        // 調用 Cloud Function
        const sendCode = firebase.functions().httpsCallable('sendVerificationCode');
        const result = await sendCode({ email: email });
        
        if (result.data.success) {
            showNotification('驗證碼已重新發送！請檢查您的郵箱', 'success');
            startResendCountdown(); // 開始倒計時
        } else {
            throw new Error(result.data.error || '發送失敗');
        }
    } catch (error) {
        console.error('重新發送失敗:', error);
        showNotification('重新發送失敗：' + error.message, 'error');
        resendBtn.disabled = false;
        resendBtn.textContent = '重新發送驗證碼';
    }
}

// 倒計時函數（60秒）
function startResendCountdown() {
    const resendBtn = document.getElementById('resend-btn');
    let countdown = 60;
    
    resendBtn.disabled = true;
    
    const interval = setInterval(() => {
        countdown--;
        resendBtn.textContent = `重新發送驗證碼 (${countdown}s)`;
        
        if (countdown <= 0) {
            clearInterval(interval);
            resendBtn.disabled = false;
            resendBtn.textContent = '重新發送驗證碼';
        }
    }, 1000);
}
```

---

## 📋 實施清單

### 高優先級（今天）

- [ ] **修復 1：Export 只導出已勾選的文件**
  - 修改 `firstproject.html` 的導出函數
  - 添加勾選檢查邏輯
  - 測試導出功能

- [ ] **修復 2：合併發票和收據類型**
  - 更新 `export-optimizer.js`
  - 統一欄位名稱
  - 測試 CSV 導出

- [ ] **修復 6：Email 驗證碼問題**
  - 檢查 Firebase Functions 配置
  - 修改 `verify-email.html` 重新發送邏輯
  - 測試驗證碼發送

---

### 中優先級（本週）

- [ ] **修復 3：優化銀行對帳單處理**
  - 更新 AI 提示詞
  - 測試銀行對帳單提取
  - 優化錯誤處理

- [ ] **修復 4：優化文檔詳情頁顯示**
  - 根據文檔類型顯示相應欄位
  - 統一發票/收據顯示格式

---

## 🎯 下一步

**立即執行（30 分鐘）：**

1. **修復 Export 邏輯**
2. **合併發票/收據類型**
3. **檢查 Email 配置**

準備好開始了嗎？🚀

