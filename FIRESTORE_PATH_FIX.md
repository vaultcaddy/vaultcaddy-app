# 🔧 Firestore 路徑修復完成

## ✅ 問題已解決

### 原始問題（圖3）
```
FirebaseError: Missing or insufficient permissions
獲取項目失敗
```

### 根本原因
**Firestore 規則** 要求項目存儲在：
```
users/{userId}/projects/{projectId}
```

但 **simple-data-manager.js** 查詢的是：
```
projects (錯誤的路徑)
```

---

## 🛠️ 已修復的函數

### 項目管理（Projects）

| 函數 | 原路徑 | 新路徑 | 狀態 |
|------|--------|--------|------|
| `getProjects()` | `projects` | `users/{userId}/projects` | ✅ |
| `createProject()` | `projects` | `users/{userId}/projects` | ✅ |
| `updateProject()` | `projects/{projectId}` | `users/{userId}/projects/{projectId}` | ✅ |
| `deleteProject()` | `projects/{projectId}` | `users/{userId}/projects/{projectId}` | ✅ |

### 文檔管理（Documents）

| 函數 | 原路徑 | 新路徑 | 狀態 |
|------|--------|--------|------|
| `getDocuments()` | `documents?projectId==X` | `users/{userId}/projects/{projectId}/documents` | ✅ |
| `getDocument()` | `documents/{documentId}` | `users/{userId}/projects/{projectId}/documents/{documentId}` | ✅ |
| `createDocument()` | `documents` | `users/{userId}/projects/{projectId}/documents` | ✅ |
| `updateDocument()` | `documents/{documentId}` | `users/{userId}/projects/{projectId}/documents/{documentId}` | ✅ |
| `deleteDocument()` | `documents/{documentId}` | `users/{userId}/projects/{projectId}/documents/{documentId}` | ✅ |

---

## 📋 Firestore 數據結構

### 正確的結構（已實現）

```
users/
  {userId}/
    ├── credits: 10
    ├── currentCredits: 10
    ├── email: "user@example.com"
    ├── emailVerified: true
    ├── plan: "free"
    ├── createdAt: Timestamp
    │
    ├── creditsHistory/
    │   └── {historyId}/
    │       ├── type: "usage" | "purchase" | "refund" | "bonus"
    │       ├── amount: 3
    │       ├── reason: "document_processing"
    │       ├── createdAt: Timestamp
    │       └── balanceAfter: 7
    │
    └── projects/
        └── {projectId}/
            ├── name: "My Project"
            ├── createdAt: Timestamp
            │
            └── documents/
                └── {documentId}/
                    ├── fileName: "invoice.pdf"
                    ├── fileUrl: "gs://..."
                    ├── type: "invoice"
                    ├── status: "completed"
                    ├── processedData: {...}
                    └── createdAt: Timestamp
```

---

## 🧪 測試步驟

### 1. 清除瀏覽器緩存

**重要！** 必須清除緩存以加載新的 JavaScript 代碼：

**Chrome：**
1. 按 `Cmd + Shift + Delete`（Mac）或 `Ctrl + Shift + Delete`（Windows）
2. 選擇「快取的圖片和檔案」
3. 點擊「清除資料」

**或者使用硬重新整理：**
1. 打開 DevTools（F12）
2. 右鍵點擊重新整理按鈕
3. 選擇「清空快取並強制重新整理」

---

### 2. 測試 Dashboard

**步驟：**
1. 前往：https://vaultcaddy.com/dashboard.html
2. 打開 Console（F12）
3. 觀察日誌

**預期結果：**
```
✅ Firebase 加載 0 個項目
✅ 從 Firebase 加載 0 個項目
```

**不應該出現：**
```
❌ FirebaseError: Missing or insufficient permissions
```

---

### 3. 測試創建項目

**步驟：**
1. 點擊「+ Create」按鈕
2. 輸入項目名稱（例如：「Test Project」）
3. 點擊「創建」

**預期結果：**
```
📂 getProjects() 開始執行...
   userId: AZ5Sk5FJBofAeKE09AYbGVlEoDy1
   準備查詢 Firestore collection: users/{userId}/projects
   ✅ Firestore 查詢完成
   snapshot.empty: false
   snapshot.size: 1
   查詢結果: 1 個項目
✅ 獲取 1 個項目
✅ 項目已創建: abc123
```

**頁面應該顯示：**
- 左側邊欄出現「Test Project」
- 不再顯示「No projects yet」

---

### 4. 測試文件上傳

**步驟：**
1. 選擇剛創建的項目
2. 點擊「Upload」或拖放文件
3. 選擇文檔類型（Invoice/Receipt/等）
4. 上傳 PDF 文件

**預期結果：**
```
📄 開始處理文件: invoice.pdf
✅ 文件上傳成功
✅ 文檔已創建: xyz789
🤖 開始 AI 處理...
✅ AI 處理完成
```

**頁面應該顯示：**
- 文件出現在文檔列表中
- 狀態從「Processing」變為「Completed」
- Credits 正確扣除

---

## 🔍 故障排查

### 問題 1：還是出現權限錯誤

**解決方案：**
1. **清除瀏覽器緩存**（最重要！）
2. 硬重新整理（Cmd/Ctrl + Shift + R）
3. 檢查 Console 是否加載了新的 `simple-data-manager.js`

**驗證方法：**
```javascript
// 在 Console 輸入：
console.log(window.dataManager.getProjects.toString())
// 應該看到 "users/{userId}/projects" 而不是 "projects"
```

---

### 問題 2：項目創建成功但看不到

**可能原因：**
- 舊數據存儲在錯誤的路徑（`projects` collection）

**解決方案：**
1. 前往 Firebase Console
2. 檢查 Firestore 數據庫
3. 確認數據在 `users/{userId}/projects` 路徑下
4. 如果有舊數據在 `projects` collection，可以手動刪除

---

### 問題 3：文件上傳失敗

**檢查：**
1. Credits 是否足夠
2. Storage 規則是否正確
3. Console 是否有詳細錯誤訊息

**Storage 規則應該是：**
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

## 📊 數據遷移（如果需要）

如果您之前在 `projects` collection 中有數據，需要遷移：

### 選項 1：手動遷移（Firebase Console）

1. 前往 Firebase Console → Firestore
2. 找到 `projects` collection
3. 對每個項目：
   - 複製項目數據
   - 在 `users/{userId}/projects` 創建新文檔
   - 刪除舊項目

### 選項 2：使用腳本遷移

```javascript
// 在 Firebase Console 或 Cloud Functions 中執行
const admin = require('firebase-admin');
const db = admin.firestore();

async function migrateProjects() {
  const oldProjects = await db.collection('projects').get();
  
  for (const doc of oldProjects.docs) {
    const data = doc.data();
    const userId = data.userId;
    
    if (userId) {
      // 創建新路徑
      await db.collection('users')
        .doc(userId)
        .collection('projects')
        .doc(doc.id)
        .set(data);
      
      // 刪除舊數據
      await doc.ref.delete();
      
      console.log(`✅ 遷移項目: ${doc.id}`);
    }
  }
  
  console.log('🎉 遷移完成！');
}

migrateProjects();
```

---

## ✅ 驗證清單

完成以下檢查以確認修復成功：

- [ ] 清除瀏覽器緩存
- [ ] Dashboard 加載不出現權限錯誤
- [ ] 可以成功創建項目
- [ ] 項目顯示在左側邊欄
- [ ] 可以上傳文件
- [ ] 文件處理成功
- [ ] Credits 正確扣除和退回
- [ ] Console 不再出現 "Missing or insufficient permissions"

---

## 🎉 預期結果

### Dashboard（圖3）應該顯示：

**左側邊欄：**
```
project
  + [創建按鈕]
  
  📁 Test Project
  📁 My Invoices
  📁 Receipts 2025
```

**主區域：**
```
NAME          LAST MODIFIED    CREATED
invoice.pdf   2 hours ago      2025-01-12
receipt.jpg   1 day ago        2025-01-11
```

**Console 日誌：**
```
✅ Firebase 加載 3 個項目
✅ Sidebar: SimpleDataManager 已載入
✅ 用戶已登入: osclin2002@gmail.com
✅ 從 Firebase 加載 3 個項目
```

---

**準備好測試了嗎？請清除瀏覽器緩存後刷新 Dashboard！** 🚀

