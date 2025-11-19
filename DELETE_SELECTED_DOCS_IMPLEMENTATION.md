# 刪除已選文檔功能實現指南

## 📅 日期
2025-11-19

---

## ✅ 已完成的部分

### 1. Delete 按鈕修改
```html
<!-- 原來：刪除整個項目 -->
<button onclick="confirmDeleteProject()">Delete</button>

<!-- 修改後：刪除已選文檔 -->
<button 
    onclick="deleteSelectedDocuments()" 
    id="delete-selected-btn" 
    disabled 
    style="opacity: 0.5;">
    <i class="fas fa-trash"></i>
    <span>Delete</span>
    <span id="delete-count" style="display: none;"></span>
</button>
```

### 2. JavaScript 功能實現

#### a) 全選/取消全選
```javascript
window.toggleSelectAll = function() {
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    const documentCheckboxes = document.querySelectorAll('.document-checkbox');
    
    documentCheckboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
    
    updateDeleteButton();
};
```

#### b) 更新刪除按鈕狀態
```javascript
function updateDeleteButton() {
    const selectedCheckboxes = document.querySelectorAll('.document-checkbox:checked');
    const deleteBtn = document.getElementById('delete-selected-btn');
    const deleteCount = document.getElementById('delete-count');
    
    if (selectedCheckboxes.length > 0) {
        // 啟用按鈕
        deleteBtn.disabled = false;
        deleteBtn.style.opacity = '1';
        deleteCount.style.display = 'inline-block';
        deleteCount.textContent = selectedCheckboxes.length;  // 顯示選中數量
    } else {
        // 禁用按鈕
        deleteBtn.disabled = true;
        deleteBtn.style.opacity = '0.5';
        deleteCount.style.display = 'none';
    }
}
```

#### c) 刪除已選文檔
```javascript
window.deleteSelectedDocuments = async function() {
    const selectedCheckboxes = document.querySelectorAll('.document-checkbox:checked');
    
    if (selectedCheckboxes.length === 0) {
        alert('請先選擇要刪除的文檔');
        return;
    }
    
    const count = selectedCheckboxes.length;
    if (!confirm(`確定要刪除 ${count} 個文檔嗎？此操作無法復原。`)) {
        return;
    }
    
    try {
        const deletePromises = [];
        selectedCheckboxes.forEach(checkbox => {
            const docId = checkbox.dataset.docId;
            deletePromises.push(window.simpleDataManager.deleteDocument(currentProjectId, docId));
        });
        
        await Promise.all(deletePromises);
        console.log(`✅ 已刪除 ${count} 個文檔`);
        alert(`成功刪除 ${count} 個文檔`);
        await loadDocuments();  // 重新加載文檔列表
    } catch (error) {
        console.error('❌ 刪除失敗:', error);
        alert('刪除失敗: ' + error.message);
    }
};
```

---

## ⏳ 待完成的部分

### 需要修改文檔渲染邏輯

在 `firstproject.html` 中找到渲染文檔列表的代碼（通常在 `loadDocuments()` 或類似函數中），並添加複選框到每一行：

#### 當前的表格行結構（推測）:
```html
<tr>
    <td><!-- 文檔名稱 --></td>
    <td><!-- 類型 --></td>
    <td><!-- 供應商 --></td>
    <!-- 其他列 -->
</tr>
```

#### 需要修改為:
```html
<tr>
    <td>
        <input 
            type="checkbox" 
            class="document-checkbox" 
            data-doc-id="${doc.id}"
            onchange="updateDeleteButton()">
    </td>
    <td><!-- 文檔名稱 --></td>
    <td><!-- 類型 --></td>
    <td><!-- 供應商 --></td>
    <!-- 其他列 -->
</tr>
```

#### 完整示例（JavaScript）:
```javascript
function loadDocuments() {
    // ... 獲取文檔數據 ...
    
    const tbody = document.querySelector('table tbody');
    tbody.innerHTML = documents.map(doc => `
        <tr>
            <!-- ✅ 添加複選框列 -->
            <td style="padding: 1rem;">
                <input 
                    type="checkbox" 
                    class="document-checkbox" 
                    data-doc-id="${doc.id}"
                    onchange="updateDeleteButton()">
            </td>
            
            <!-- 文檔名稱列 -->
            <td style="padding: 1rem;">
                ${doc.name}
            </td>
            
            <!-- 類型列 -->
            <td style="padding: 1rem;">
                ${doc.type}
            </td>
            
            <!-- 其他列... -->
        </tr>
    `).join('');
    
    // ✅ 重置全選複選框
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    if (selectAllCheckbox) {
        selectAllCheckbox.checked = false;
    }
    
    // ✅ 重置刪除按鈕狀態
    updateDeleteButton();
}
```

---

## 🔍 如何找到文檔渲染代碼

### 方法 1：搜尋關鍵字
```bash
# 搜尋 loadDocuments 函數
grep -n "function loadDocuments" firstproject.html

# 搜尋 tbody.innerHTML
grep -n "tbody.innerHTML" firstproject.html

# 搜尋文檔渲染相關的代碼
grep -n "documents.map" firstproject.html
```

### 方法 2：在瀏覽器開發者工具中
1. 打開 `firstproject.html`
2. 按 F12 開啟開發者工具
3. 在 Console 中輸入：
   ```javascript
   console.log(loadDocuments.toString());
   ```
4. 查看函數的完整代碼

### 方法 3：查看網絡請求
1. 打開開發者工具的 Network 標籤
2. 刷新頁面
3. 查找 Firestore 相關的請求
4. 在 Console 中查找相關的日誌

---

## 🎯 完整實現步驟

### 步驟 1：找到文檔渲染函數
在 `firstproject.html` 中搜尋以下關鍵字之一：
- `loadDocuments`
- `renderDocuments`
- `displayDocuments`
- `tbody.innerHTML`

### 步驟 2：添加複選框到表格行
在每個 `<tr>` 的開頭添加：
```html
<td>
    <input 
        type="checkbox" 
        class="document-checkbox" 
        data-doc-id="${doc.id}"
        onchange="updateDeleteButton()">
</td>
```

### 步驟 3：測試功能
1. 重新加載頁面
2. 檢查每個文檔行是否有複選框
3. 點擊複選框，檢查 Delete 按鈕是否啟用
4. 檢查選中數量是否正確顯示
5. 點擊全選複選框，檢查所有文檔是否被選中
6. 點擊 Delete 按鈕，確認刪除提示
7. 確認刪除後文檔列表自動刷新

---

## 🐛 AI 處理失敗問題診斷

根據圖2-3的錯誤信息：

### 錯誤 1: `AI 處理失敗: Error: AI 處理終止或超時`
**可能原因**:
1. DeepSeek API 超時（180秒）
2. 文檔太大或太複雜
3. 網絡連接問題
4. DeepSeek API 限流

**解決方案**:
1. 檢查 `hybrid-vision-deepseek.js` 中的超時設置
2. 增加超時時間或優化文檔分塊
3. 添加重試邏輯
4. 檢查 API 配額

### 錯誤 2: `文檔 XxqMQrFFfMwDMdT3yjYq 內 Credits 已經消耗，無需重新處理`
**這不是錯誤！** 這是正常的日誌信息，表示：
- 文檔已經處理過
- Credits 已經扣除
- 不需要重新處理

**如果需要重新處理**:
1. 在文檔詳情頁點擊「重新處理」按鈕
2. 或在數據庫中刪除 `processedData` 欄位
3. 重新上傳文檔

---

## 📝 測試檢查清單

- [ ] 每個文檔行都有複選框
- [ ] 複選框有 `class="document-checkbox"` 類名
- [ ] 複選框有 `data-doc-id` 屬性
- [ ] 複選框有 `onchange="updateDeleteButton()"` 事件
- [ ] 全選複選框可以選中/取消選中所有文檔
- [ ] Delete 按鈕在未選中時禁用（灰色）
- [ ] Delete 按鈕在選中時啟用（正常顏色）
- [ ] Delete 按鈕顯示選中數量
- [ ] 點擊 Delete 按鈕顯示確認對話框
- [ ] 確認後成功刪除文檔
- [ ] 刪除後自動刷新文檔列表
- [ ] 刪除後重置複選框和按鈕狀態

---

## 📁 相關文件
- `firstproject.html` - 項目文檔列表頁面
- `simple-data-manager.js` - 數據管理器（包含 `deleteDocument` 方法）
- `hybrid-vision-deepseek.js` - AI 處理邏輯

---

**狀態**: 功能已實現 90%，需要在文檔渲染時添加複選框  
**更新者**: AI Assistant  
**下一步**: 找到文檔渲染函數並添加複選框

