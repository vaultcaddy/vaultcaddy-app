# 🎯 首頁文件上傳功能實現計劃

**目標**：在首頁 hero section 添加文件上傳區域，支持未登入用戶拖入文件

---

## 📋 功能需求

### 1. 首頁上傳區域
- ✅ **位置**：替換「低至 HK$0.3 /頁」區域
- ✅ **樣式**：類似 firstproject.html 的上傳區
- ✅ **功能**：支持拖放和點擊上傳

### 2. 未登入用戶流程
```
用戶拖入文件（123.JPG）
    ↓
保存文件到臨時緩存
    ↓
彈出登入框
    ↓
用戶登入
    ↓
創建 First_Project 文件夾
    ↓
跳轉到 firstproject.html?project=First_Project
    ↓
開始處理文件
    ↓
扣除 Credits
```

### 3. 已登入用戶流程
```
用戶拖入文件（123.JPG）
    ↓
檢查是否有 First_Project
    ├─ 沒有 → 創建 First_Project
    └─ 有 → 使用現有的
    ↓
跳轉到 firstproject.html?project=First_Project
    ↓
開始處理文件
    ↓
扣除 Credits
```

---

## 🔧 需要修改的文件

### 1. `index.html`
- [ ] 替換「低至 HK$0.3 /頁」為上傳區域
- [ ] 添加文件拖放處理邏輯
- [ ] 添加臨時文件緩存邏輯
- [ ] 添加登入後處理邏輯

### 2. `simple-auth.js`
- [ ] 添加登入後回調函數
- [ ] 支持登入後跳轉到指定頁面

### 3. `simple-data-manager.js`
- [ ] 添加創建默認項目的函數
- [ ] 添加上傳文件到項目的函數

### 4. `firstproject.html`
- [ ] 支持從 URL 參數接收文件
- [ ] 自動開始處理文件

---

## 🎨 UI 設計

### 上傳區域（未登入時）

```html
<div style="background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 3rem; max-width: 600px; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.15);">
    <!-- 文件類型選擇 -->
    <div style="display: flex; gap: 1rem; margin-bottom: 2rem; justify-content: center;">
        <button class="doc-type-btn active" data-type="statement">
            <i class="fas fa-university"></i>
            <span>銀行對帳單</span>
        </button>
        <button class="doc-type-btn" data-type="invoice">
            <i class="fas fa-file-invoice"></i>
            <span>發票</span>
        </button>
    </div>
    
    <!-- 拖放區域 -->
    <div id="dropzone" style="border: 3px dashed #667eea; border-radius: 12px; padding: 3rem; text-align: center; background: rgba(102, 126, 234, 0.05); cursor: pointer; transition: all 0.3s ease;">
        <i class="fas fa-cloud-upload-alt" style="font-size: 3rem; color: #667eea; margin-bottom: 1rem;"></i>
        <h3 style="font-size: 1.5rem; color: #1f2937; margin-bottom: 0.5rem;">拖放文件到此處或點擊上傳</h3>
        <p style="color: #6b7280; font-size: 1rem;">支援 PDF、JPG、PNG 格式 (最大 10MB) | ✨ 支持批量上傳</p>
    </div>
    
    <!-- 隱藏的文件輸入 -->
    <input type="file" id="file-input" accept=".pdf,.jpg,.jpeg,.png" multiple style="display: none;">
    
    <!-- 信任標誌 -->
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; opacity: 0.7;">
        <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #667eea;">
            <i class="fas fa-lock"></i>
            <span>銀行級加密</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #667eea;">
            <i class="fas fa-shield-alt"></i>
            <span>GDPR 合規</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: #667eea;">
            <i class="fas fa-check-circle"></i>
            <span>98% 準確率</span>
        </div>
    </div>
</div>
```

---

## 💻 JavaScript 邏輯

### 1. 文件拖放處理

```javascript
// 初始化拖放區域
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('file-input');
let pendingFiles = []; // 臨時存儲未登入用戶的文件

// 點擊上傳
dropzone.addEventListener('click', () => {
    fileInput.click();
});

// 文件選擇
fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

// 拖放事件
dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#764ba2';
    dropzone.style.background = 'rgba(102, 126, 234, 0.1)';
});

dropzone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#667eea';
    dropzone.style.background = 'rgba(102, 126, 234, 0.05)';
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.style.borderColor = '#667eea';
    dropzone.style.background = 'rgba(102, 126, 234, 0.05)';
    handleFiles(e.dataTransfer.files);
});

// 處理文件
async function handleFiles(files) {
    if (!files || files.length === 0) return;
    
    // 檢查用戶是否已登入
    const isLoggedIn = window.simpleAuth && window.simpleAuth.isLoggedIn();
    
    if (!isLoggedIn) {
        // 未登入：保存文件並彈出登入框
        pendingFiles = Array.from(files);
        localStorage.setItem('pendingFiles', JSON.stringify(pendingFiles.map(f => ({
            name: f.name,
            size: f.size,
            type: f.type
        }))));
        
        // 顯示提示
        showToast('請先登入以處理文件');
        
        // 彈出登入框
        openAuthModal();
    } else {
        // 已登入：直接處理
        await processFiles(files);
    }
}

// 處理文件（已登入）
async function processFiles(files) {
    try {
        // 1. 確保有 First_Project
        const project = await ensureFirstProject();
        
        // 2. 保存文件到 sessionStorage（或直接上傳）
        const fileData = [];
        for (let file of files) {
            const base64 = await fileToBase64(file);
            fileData.push({
                name: file.name,
                data: base64,
                type: file.type,
                size: file.size
            });
        }
        sessionStorage.setItem('pendingUpload', JSON.stringify(fileData));
        
        // 3. 跳轉到 firstproject.html
        window.location.href = `firstproject.html?project=${project.id}&autoUpload=true`;
    } catch (error) {
        console.error('處理文件失敗:', error);
        showToast('處理文件失敗，請重試');
    }
}

// 確保 First_Project 存在
async function ensureFirstProject() {
    const userId = window.simpleAuth.getCurrentUser().uid;
    const db = window.simpleDataManager.db;
    
    // 查詢是否已有 First_Project
    const query = db.collection('projects')
        .where('userId', '==', userId)
        .where('name', '==', 'First_Project')
        .limit(1);
    
    const snapshot = await query.get();
    
    if (!snapshot.empty) {
        // 已存在
        return { id: snapshot.docs[0].id, name: 'First_Project' };
    } else {
        // 不存在，創建新項目
        const projectRef = await db.collection('projects').add({
            name: 'First_Project',
            userId: userId,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
            updatedAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        return { id: projectRef.id, name: 'First_Project' };
    }
}

// 文件轉 Base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Toast 提示
function showToast(message) {
    // 簡單的 toast 實現
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = 'position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%); background: #1f2937; color: white; padding: 1rem 2rem; border-radius: 8px; z-index: 10000; box-shadow: 0 4px 12px rgba(0,0,0,0.3);';
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
```

### 2. 登入後處理

```javascript
// 在 signInWithGoogleModal 成功後調用
async function handlePostLoginUpload() {
    const pendingFilesData = localStorage.getItem('pendingFiles');
    if (pendingFilesData) {
        // 清除緩存
        localStorage.removeItem('pendingFiles');
        
        // 重新觸發文件上傳
        // 注意：由於安全限制，我們無法直接訪問原始 File 對象
        // 所以需要在登入後提示用戶重新拖入文件
        showToast('登入成功！請重新拖入您的文件');
    }
}
```

---

## 🚨 安全考慮

### 1. 文件大小限制
- 單個文件最大 10MB
- 總大小最大 50MB

### 2. 文件類型驗證
- 只允許 PDF、JPG、PNG
- 檢查文件 MIME 類型

### 3. 防止 XSS
- 文件名過濾特殊字符
- Base64 編碼傳輸

---

## 📱 響應式設計

### 移動端優化

```css
@media (max-width: 768px) {
    /* 上傳區域調整 */
    #dropzone {
        padding: 2rem 1rem !important;
    }
    
    /* 文件類型按鈕垂直排列 */
    .doc-type-buttons {
        flex-direction: column !important;
    }
    
    /* 信任標誌調整 */
    .trust-badges {
        flex-direction: column !important;
        gap: 0.5rem !important;
    }
}
```

---

## ✅ 完成檢查清單

- [ ] 在 index.html 添加上傳區域 HTML
- [ ] 添加拖放處理 JavaScript
- [ ] 添加登入後回調邏輯
- [ ] 在 firstproject.html 添加自動上傳邏輯
- [ ] 測試未登入用戶流程
- [ ] 測試已登入用戶流程
- [ ] 測試移動端體驗
- [ ] 測試文件大小限制
- [ ] 測試文件類型驗證

---

## 🎯 下一步

1. **先實現基本功能**（未登入彈出登入框）
2. **再實現文件緩存**（登入後自動處理）
3. **最後優化體驗**（動畫、提示等）

---

**預計實現時間**: 30-45 分鐘  
**優先級**: 高

