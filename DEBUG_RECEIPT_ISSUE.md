# 🔧 收據顯示問題調試指南

## 🚨 **當前問題**
用戶上傳img_5268.JPG後，點擊文件仍然顯示舊的銀行對帳單數據，而不是收據數據。

## 🔍 **已實施的修復**

### **1. 修復了數據載入邏輯**
```javascript
// ledgerbox-integration.js - openDocumentDetail()
// 現在會按順序查找數據：
// 1. 內存中的processedDocuments
// 2. 統一存儲系統
// 3. 舊的存儲格式
```

### **2. 清理了硬編碼內容**
```html
<!-- dashboard.html -->
<!-- 移除了所有硬編碼的銀行交易數據 -->
<tbody id="transactions-tbody">
    <!-- 動態填充的交易數據將顯示在這裡 -->
</tbody>
```

### **3. 修復了標題更新**
```javascript
// 現在會更新多個標題元素
document.getElementById('document-title')
document.getElementById('document-title-header')
```

## 🧪 **調試步驟**

### **步驟1：檢查瀏覽器控制台**
打開瀏覽器開發者工具，查看控制台輸出：

1. **上傳文件時**：
   ```
   🎯 使用統一處理器處理文件...
   🔍 檢測到文檔類型: receipt
   🤖 使用AI提取數據...
   💾 文件已保存...
   ```

2. **點擊文件時**：
   ```
   🔍 查找文檔數據: [documentId]
   📂 從統一存儲載入文檔數據 (或其他來源)
   📄 打開文檔詳細視圖: img_5268.JPG
   ```

### **步驟2：檢查localStorage**
在控制台中運行：
```javascript
// 檢查統一存儲
Object.keys(localStorage).filter(key => key.includes('vaultcaddy_unified'))

// 檢查舊存儲
Object.keys(localStorage).filter(key => key.includes('vaultcaddy_files'))

// 查看收據存儲
JSON.parse(localStorage.getItem('vaultcaddy_unified_receipt') || '[]')
```

### **步驟3：手動觸發數據載入**
在控制台中運行：
```javascript
// 檢查統一處理器是否載入
console.log('UnifiedDocumentProcessor:', window.UnifiedDocumentProcessor);

// 檢查LedgerBox處理器
console.log('LedgerBoxProcessor:', window.ledgerBoxProcessor);

// 檢查處理後的文檔
console.log('Processed Documents:', window.ledgerBoxProcessor?.processedDocuments);
```

## 🎯 **可能的問題和解決方案**

### **問題1：數據沒有正確保存**
**症狀**：控制台顯示"找不到處理後的數據"
**解決**：
```javascript
// 檢查統一處理器是否正確保存數據
window.UnifiedDocumentProcessor.getAllProcessedDocuments('receipt')
```

### **問題2：文檔ID不匹配**
**症狀**：點擊文件時傳遞了錯誤的documentId
**解決**：
```javascript
// 檢查表格中的onclick事件
document.querySelectorAll('#documents-tbody tr').forEach(row => {
    console.log('Row onclick:', row.onclick.toString());
});
```

### **問題3：LedgerBox處理器沒有正確整合**
**症狀**：還是調用舊的處理邏輯
**解決**：
```javascript
// 強制重新載入頁面，確保新代碼生效
location.reload();
```

## 🔧 **緊急修復方案**

如果問題仍然存在，可以嘗試以下緊急修復：

### **方案1：清理所有存儲**
```javascript
// 清理所有相關的localStorage
Object.keys(localStorage).forEach(key => {
    if (key.includes('vaultcaddy')) {
        localStorage.removeItem(key);
    }
});
location.reload();
```

### **方案2：強制使用統一處理器**
在dashboard.html中添加調試代碼：
```javascript
// 在openDocumentDetail函數開始處添加
function openDocumentDetail(documentId) {
    console.log('🔧 DEBUG: 強制使用統一處理器');
    
    if (window.UnifiedDocumentProcessor) {
        const data = window.UnifiedDocumentProcessor.getProcessedDocument(documentId);
        if (data) {
            console.log('📄 找到統一數據:', data);
            // 直接更新視圖
            document.getElementById('document-title').textContent = data.fileName;
            document.getElementById('document-title-header').textContent = data.fileName;
            return;
        }
    }
    
    // 原有邏輯...
}
```

### **方案3：檢查文件上傳流程**
確保上傳時使用正確的處理器：
```javascript
// 檢查processSelectedFiles函數是否調用統一處理器
console.log('Upload processor:', window.UnifiedDocumentProcessor ? 'Unified' : 'Legacy');
```

## 📋 **檢查清單**

- [ ] 瀏覽器控制台沒有錯誤
- [ ] 統一處理器已載入 (`window.UnifiedDocumentProcessor`)
- [ ] LedgerBox處理器已載入 (`window.ledgerBoxProcessor`)
- [ ] 上傳時顯示"使用統一處理器處理文件"
- [ ] 點擊時顯示"查找文檔數據"和正確的文件名
- [ ] localStorage中有正確的收據數據
- [ ] 詳細視圖顯示收據信息而不是銀行數據

## 🎉 **預期結果**

修復成功後，用戶應該看到：
- **文檔標題**：img_5268.JPG
- **對帳狀態區域**：收據信息（收據號碼、總金額）
- **詳細信息區域**：收據詳細信息（商家、日期、付款方式）
- **交易表格**：商品列表（商品名稱、數量、單價、總價）
- **白色背景**：清晰的表格顯示

如果仍然看到銀行對帳單數據，說明還有其他問題需要進一步調試。
