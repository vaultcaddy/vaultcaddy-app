# ✅ 首頁文檔類型選擇功能 - 更新說明

**更新時間**: 2026-01-31 18:30 HKT  
**功能**: 在首頁上傳區域添加文檔類型選擇

---

## 🎯 新增功能

### 文檔類型選擇按鈕

**位置**: 拖放區域上方

**選項**：
1. **🏦 銀行對帳單**（默認選中）
2. **📄 發票**

---

## 📸 UI 設計

### 按鈕樣式

#### 激活狀態（選中）：
- 背景色：藍色（#667eea）
- 文字顏色：白色
- 邊框：2px 藍色

#### 未激活狀態：
- 背景色：白色
- 文字顏色：藍色（#667eea）
- 邊框：2px 藍色

### 佈局
```
┌─────────────────────────────────────┐
│  [🏦 銀行對帳單]  [📄 發票]         │  ← 文檔類型選擇
│                                     │
│  ┌─────────────────────────────┐   │
│  │  ☁️ 拖放文件到此處或點擊上傳  │   │  ← 上傳區域
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## 🔧 技術實現

### 1. HTML 結構

```html
<!-- 文檔類型選擇 -->
<div style="display: flex; gap: 0.75rem; margin-bottom: 1.5rem; justify-content: center;">
    <button id="doc-type-statement" class="doc-type-btn active" onclick="selectDocType('statement')">
        <i class="fas fa-university"></i>
        <span>銀行對帳單</span>
    </button>
    <button id="doc-type-invoice" class="doc-type-btn" onclick="selectDocType('invoice')">
        <i class="fas fa-file-invoice"></i>
        <span>發票</span>
    </button>
</div>
```

### 2. JavaScript 邏輯

```javascript
// 全局變量：當前選擇的文檔類型
let selectedDocType = 'statement'; // 默認為銀行對帳單

// 選擇文檔類型
window.selectDocType = function(type) {
    selectedDocType = type;
    console.log('✅ 選擇文檔類型:', type);
    
    // 更新按鈕樣式
    const statementBtn = document.getElementById('doc-type-statement');
    const invoiceBtn = document.getElementById('doc-type-invoice');
    
    if (type === 'statement') {
        statementBtn.style.background = '#667eea';
        statementBtn.style.color = 'white';
        invoiceBtn.style.background = 'white';
        invoiceBtn.style.color = '#667eea';
    } else {
        invoiceBtn.style.background = '#667eea';
        invoiceBtn.style.color = 'white';
        statementBtn.style.background = 'white';
        statementBtn.style.color = '#667eea';
    }
};
```

### 3. 數據保存

#### 未登入用戶：
```javascript
// 保存到 localStorage
localStorage.setItem('pendingDocType', selectedDocType);
```

#### 已登入用戶：
```javascript
// 保存到 sessionStorage
sessionStorage.setItem('selectedDocType', selectedDocType);
```

---

## 🔄 完整用戶流程

### 流程 A：未登入用戶

```
1. 用戶訪問 https://vaultcaddy.com
2. 選擇文檔類型（銀行對帳單 或 發票）
3. 拖入文件
4. 系統保存：
   - 文件數量 → localStorage.pendingFileCount
   - 文檔類型 → localStorage.pendingDocType
5. 彈出登入框
6. 用戶使用 Google 登入
7. 系統讀取保存的數據：
   - 從 localStorage 讀取 pendingDocType
   - 轉存到 sessionStorage.selectedDocType
8. 跳轉到 firstproject.html
9. firstproject.html 讀取 sessionStorage.selectedDocType
10. 根據文檔類型自動設置上傳類型
```

### 流程 B：已登入用戶

```
1. 用戶訪問 https://vaultcaddy.com（已登入）
2. 選擇文檔類型（銀行對帳單 或 發票）
3. 拖入文件
4. 系統保存：
   - 文檔類型 → sessionStorage.selectedDocType
5. 直接跳轉到 firstproject.html
6. firstproject.html 讀取 sessionStorage.selectedDocType
7. 根據文檔類型自動設置上傳類型
```

---

## 🎯 在 firstproject.html 中使用

### 讀取文檔類型

```javascript
// 在 firstproject.html 頁面加載時讀取
const selectedDocType = sessionStorage.getItem('selectedDocType');

if (selectedDocType) {
    console.log('📋 用戶從首頁選擇的文檔類型:', selectedDocType);
    
    // 自動選擇對應的文檔類型
    if (selectedDocType === 'statement') {
        // 選擇銀行對帳單
        selectBankStatement();
    } else if (selectedDocType === 'invoice') {
        // 選擇發票
        selectInvoice();
    }
    
    // 清除 sessionStorage（避免影響下次上傳）
    sessionStorage.removeItem('selectedDocType');
}
```

---

## ✅ 測試方法

### 測試 1：未登入 + 銀行對帳單

1. 訪問 https://vaultcaddy.com（登出狀態）
2. **確認"銀行對帳單"按鈕為藍色（默認選中）**
3. 拖入一個 PDF 文件
4. 應該看到提示：「已選擇 1 個銀行對帳單文件，請先登入以開始處理」
5. 彈出登入框
6. 使用 Google 登入
7. 應該跳轉到 firstproject.html
8. **打開瀏覽器控制台，應該看到：`📋 用戶從首頁選擇的文檔類型: statement`**

### 測試 2：未登入 + 發票

1. 訪問 https://vaultcaddy.com（登出狀態）
2. **點擊"發票"按鈕，應該變為藍色**
3. 拖入一個 PDF 文件
4. 應該看到提示：「已選擇 1 個發票文件，請先登入以開始處理」
5. 彈出登入框
6. 使用 Google 登入
7. 應該跳轉到 firstproject.html
8. **打開瀏覽器控制台，應該看到：`📋 用戶從首頁選擇的文檔類型: invoice`**

### 測試 3：已登入 + 銀行對帳單

1. 訪問 https://vaultcaddy.com（已登入）
2. **確認"銀行對帳單"按鈕為藍色（默認選中）**
3. 拖入一個 PDF 文件
4. 應該直接跳轉到 firstproject.html
5. **打開瀏覽器控制台，應該看到：`📋 用戶從首頁選擇的文檔類型: statement`**

### 測試 4：已登入 + 發票

1. 訪問 https://vaultcaddy.com（已登入）
2. **點擊"發票"按鈕，應該變為藍色**
3. 拖入一個 PDF 文件
4. 應該直接跳轉到 firstproject.html
5. **打開瀏覽器控制台，應該看到：`📋 用戶從首頁選擇的文檔類型: invoice`**

---

## 🔍 控制台日誌

### 預期日誌（按時間順序）

```
✅ 初始化首頁上傳功能
✅ 選擇文檔類型: statement  ← 用戶點擊按鈕時
📁 用戶拖入 1 個文件
📋 文檔類型: 銀行對帳單
ℹ️ 用戶未登入，保存文件信息和文檔類型  ← 未登入時
✅ 用戶已登入，保存文檔類型並跳轉到 firstproject.html  ← 已登入時
```

---

## 🎨 響應式設計

### 移動端（< 768px）

按鈕會自動調整：
- 保持並排顯示
- 縮小字體和間距
- 保持可點擊區域

---

## 📦 數據結構

### localStorage（未登入用戶）

```json
{
  "pendingFileCount": "1",
  "pendingFileNames": "[\"statement.pdf\"]",
  "pendingDocType": "statement"
}
```

### sessionStorage（已登入用戶）

```json
{
  "selectedDocType": "statement",
  "uploadHint": "您剛才選擇了 1 個銀行對帳單文件，請在此頁面上傳"
}
```

---

## 🚀 下一步（可選優化）

### 1. 在 firstproject.html 自動選擇文檔類型

需要在 `firstproject.html` 中添加邏輯：

```javascript
// 頁面加載時自動選擇文檔類型
window.addEventListener('DOMContentLoaded', () => {
    const selectedDocType = sessionStorage.getItem('selectedDocType');
    
    if (selectedDocType) {
        console.log('📋 自動選擇文檔類型:', selectedDocType);
        
        // 點擊對應的文檔類型按鈕
        const btn = selectedDocType === 'statement' 
            ? document.querySelector('[data-type="statement"]')
            : document.querySelector('[data-type="invoice"]');
        
        if (btn) {
            btn.click();
        }
        
        // 清除 sessionStorage
        sessionStorage.removeItem('selectedDocType');
    }
});
```

### 2. 添加文檔類型說明

可以在按鈕下方添加說明文字：

```html
<p style="text-align: center; color: #6b7280; font-size: 0.85rem; margin-top: -0.5rem; margin-bottom: 1rem;">
    選擇文檔類型以獲得最佳識別效果
</p>
```

---

## ✅ 完成檢查清單

- [x] 添加文檔類型選擇按鈕（HTML）
- [x] 實現按鈕切換邏輯（JavaScript）
- [x] 保存選擇到 localStorage/sessionStorage
- [x] 在提示信息中顯示文檔類型
- [x] 登入後攜帶文檔類型信息跳轉
- [x] 添加控制台日誌用於調試
- [x] 響應式設計（移動端友好）
- [ ] （可選）在 firstproject.html 自動選擇類型
- [ ] （可選）添加說明文字

---

## 🎉 完成！

**現在用戶可以在首頁選擇文檔類型，系統會記住選擇並在跳轉後自動應用！**

**Git 提交記錄**：
```
✨ Feature: 添加文檔類型選擇功能
```

---

**文檔版本**: 1.0.0  
**創建時間**: 2026-01-31 18:30 HKT  
**維護者**: VaultCaddy Development Team

