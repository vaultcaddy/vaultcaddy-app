# Dashboard 和用戶體驗改進狀態

## 📅 更新日期
2025-11-19

---

## ✅ 已完成的功能

### 1. **index.html 動態用戶狀態**
- ✅ 用戶登入後顯示 "U" 頭像
- ✅ 未登入時顯示「登入」按鈕
- ✅ 監聽 Firebase 和 Auth 事件自動更新
- ✅ 多次延遲檢查確保狀態正確

**實現方式**:
```javascript
// index.html
function updateUserMenu() {
    const isLoggedIn = window.simpleAuth && window.simpleAuth.isLoggedIn();
    
    if (isLoggedIn) {
        // 顯示 U 頭像
        userMenu.innerHTML = `<div onclick="window.location.href='account.html'">U</div>`;
    } else {
        // 顯示登入按鈕
        userMenu.innerHTML = `<button onclick="window.location.href='auth.html'">登入</button>`;
    }
}

// 監聽事件
window.addEventListener('firebase-ready', updateUserMenu);
window.addEventListener('user-logged-in', updateUserMenu);
window.addEventListener('user-logged-out', updateUserMenu);

// 延遲檢查（1秒和2秒）
setTimeout(updateUserMenu, 1000);
setTimeout(updateUserMenu, 2000);
```

---

### 2. **billing.html 導航欄動態更新**
- ✅ 使用 `load-static-navbar.js` 統一管理
- ✅ 根據登入狀態顯示 "U" 或「登入」按鈕
- ✅ 支援登入/登出事件自動更新

---

### 3. **側邊欄項目篩選功能**
- ✅ 搜尋框實時篩選項目列表
- ✅ 支援部分匹配（例如輸入 "2" 顯示 "222"）
- ✅ 輸入 "3" 時顯示空白（沒有匹配項目）
- ✅ 清空搜尋框顯示所有項目

**實現方式**:
```javascript
// sidebar-component.js
window.filterProjects = (searchTerm) => {
    const projectItems = document.querySelectorAll('.project-item');
    const lowerSearchTerm = searchTerm.toLowerCase().trim();
    
    projectItems.forEach(item => {
        const projectName = item.textContent.toLowerCase();
        if (lowerSearchTerm === '' || projectName.includes(lowerSearchTerm)) {
            item.style.display = 'flex';  // 顯示
        } else {
            item.style.display = 'none';   // 隱藏
        }
    });
};
```

**HTML**:
```html
<input 
    type="text" 
    id="project-search-input" 
    placeholder="篩選文檔名稱..." 
    oninput="window.filterProjects && window.filterProjects(this.value)">
```

---

## ⏳ 待完成的功能

### 4. **Dashboard 顯示 Last Modified 和 Created**

**需求**:
- 在 dashboard.html 的項目列表中顯示兩列：
  - `Last Modified` - 最後修改時間
  - `Created` - 創建時間

**當前狀態**:
- dashboard.html 目前只顯示 `NAME` 列
- 需要從 Firestore 獲取 `createdAt` 和 `updatedAt` 時間戳
- 需要格式化為可讀的日期時間

**實現計劃**:
1. 修改 `dashboard.html` 的表格結構：
   ```html
   <thead>
       <tr>
           <th>NAME</th>
           <th>LAST MODIFIED</th>
           <th>CREATED</th>
           <th style="text-align: right;">
               <button id="delete-all-btn" title="刪除所有項目">
                   <i class="fas fa-trash"></i>
               </button>
           </th>
       </tr>
   </thead>
   ```

2. 在 `simple-data-manager.js` 中返回時間戳：
   ```javascript
   async getProjects(userId) {
       const projects = [];
       snapshot.forEach(doc => {
           projects.push({
               id: doc.id,
               name: doc.data().name,
               createdAt: doc.data().createdAt,
               updatedAt: doc.data().updatedAt
           });
       });
       return projects;
   }
   ```

3. 格式化時間戳：
   ```javascript
   function formatDate(timestamp) {
       if (!timestamp) return '-';
       const date = timestamp.toDate();
       return date.toLocaleDateString('zh-TW', {
           year: 'numeric',
           month: '2-digit',
           day: '2-digit',
           hour: '2-digit',
           minute: '2-digit'
       });
   }
   ```

---

### 5. **Dashboard 項目刪除功能**

**需求**:
- 在 `Created` 列右方添加垃圾桶按鈕
- 點擊後彈出確認對話框
- 用戶需要輸入項目名稱才能刪除
- 刪除後無法恢復（包括項目內的所有文檔）

**確認對話框文案**:
```
是否刪除文件夾 '222'？
刪除後無法復原文件夾及當中內容。

請輸入文件夾名稱以確認刪除：
[__________________]

[取消]  [是的，刪除]
```

**實現計劃**:
1. 添加刪除按鈕到每一行：
   ```html
   <td style="text-align: right;">
       <button onclick="confirmDeleteProject('222', 'project-id-123')" class="delete-btn" title="刪除項目">
           <i class="fas fa-trash"></i>
       </button>
   </td>
   ```

2. 創建確認對話框函數：
   ```javascript
   function confirmDeleteProject(projectName, projectId) {
       const modal = document.createElement('div');
       modal.className = 'delete-modal';
       modal.innerHTML = `
           <div class="modal-overlay" onclick="closeDeleteModal()"></div>
           <div class="modal-content">
               <h3>是否刪除文件夾 '${projectName}'？</h3>
               <p style="color: #ef4444; margin: 1rem 0;">
                   刪除後無法復原文件夾及當中內容。
               </p>
               <label>請輸入文件夾名稱以確認刪除：</label>
               <input 
                   type="text" 
                   id="delete-confirm-input" 
                   placeholder="輸入 ${projectName}"
                   style="width: 100%; padding: 0.5rem; margin: 0.5rem 0;">
               <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                   <button onclick="closeDeleteModal()" class="btn-secondary">取消</button>
                   <button 
                       id="confirm-delete-btn" 
                       onclick="deleteProject('${projectId}', '${projectName}')" 
                       class="btn-danger" 
                       disabled>
                       是的，刪除
                   </button>
               </div>
           </div>
       `;
       
       document.body.appendChild(modal);
       
       // 監聽輸入框，只有名稱匹配才啟用刪除按鈕
       const input = document.getElementById('delete-confirm-input');
       const deleteBtn = document.getElementById('confirm-delete-btn');
       input.addEventListener('input', () => {
           deleteBtn.disabled = input.value !== projectName;
       });
   }
   ```

3. 實現刪除邏輯：
   ```javascript
   async function deleteProject(projectId, projectName) {
       try {
           // 1. 刪除項目內的所有文檔
           const documents = await window.simpleDataManager.getDocuments(projectId);
           for (const doc of documents) {
               await window.simpleDataManager.deleteDocument(doc.id);
           }
           
           // 2. 刪除項目本身
           await window.simpleDataManager.deleteProject(projectId);
           
           // 3. 關閉對話框
           closeDeleteModal();
           
           // 4. 觸發事件更新 UI
           window.dispatchEvent(new Event('projectDeleted'));
           
           alert(`項目 "${projectName}" 已成功刪除`);
           
       } catch (error) {
           console.error('刪除項目失敗:', error);
           alert('刪除失敗：' + error.message);
       }
   }
   ```

4. 添加 CSS 樣式：
   ```css
   .delete-modal {
       position: fixed;
       top: 0;
       left: 0;
       right: 0;
       bottom: 0;
       z-index: 9999;
   }
   
   .modal-overlay {
       position: absolute;
       top: 0;
       left: 0;
       right: 0;
       bottom: 0;
       background: rgba(0, 0, 0, 0.5);
   }
   
   .modal-content {
       position: relative;
       background: white;
       max-width: 500px;
       margin: 10% auto;
       padding: 2rem;
       border-radius: 12px;
       box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
   }
   
   .delete-btn {
       background: none;
       border: none;
       color: #ef4444;
       cursor: pointer;
       padding: 0.5rem;
       font-size: 1rem;
       transition: color 0.2s;
   }
   
   .delete-btn:hover {
       color: #dc2626;
   }
   
   .btn-danger {
       background: #ef4444;
       color: white;
       border: none;
       padding: 0.75rem 1.5rem;
       border-radius: 6px;
       font-weight: 600;
       cursor: pointer;
       transition: background 0.2s;
   }
   
   .btn-danger:hover:not(:disabled) {
       background: #dc2626;
   }
   
   .btn-danger:disabled {
       background: #9ca3af;
       cursor: not-allowed;
   }
   ```

---

## 📁 需要修改的文件

### 已修改：
1. ✅ `index.html` - 動態用戶狀態
2. ✅ `sidebar-component.js` - 項目篩選功能

### 待修改：
3. ⏳ `dashboard.html` - 顯示時間戳和刪除按鈕
4. ⏳ `simple-data-manager.js` - 返回時間戳數據
5. ⏳ `dashboard.css` 或 `styles.css` - 添加刪除對話框樣式

---

## 🧪 測試計劃

### 已完成測試：
1. ✅ index.html 用戶狀態切換
2. ✅ billing.html 用戶狀態切換
3. ✅ 側邊欄項目篩選

### 待測試：
1. ⏳ Dashboard 顯示時間戳
2. ⏳ 刪除對話框顯示
3. ⏳ 輸入驗證（名稱匹配）
4. ⏳ 刪除功能（刪除項目和文檔）
5. ⏳ UI 更新（刪除後自動刷新列表）

---

## 📝 下一步工作

1. **實現 Dashboard 時間戳顯示**（預計 30 分鐘）
   - 修改表格結構
   - 獲取並格式化時間戳
   - 測試顯示效果

2. **實現刪除功能**（預計 45 分鐘）
   - 添加刪除按鈕
   - 創建確認對話框
   - 實現刪除邏輯
   - 添加 CSS 樣式
   - 測試完整流程

3. **優化用戶體驗**（預計 15 分鐘）
   - 添加加載動畫
   - 優化錯誤提示
   - 改進確認對話框設計

---

**更新者**: AI Assistant  
**狀態**: 部分完成（3/5 功能已完成）

