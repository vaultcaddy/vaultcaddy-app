# 📋 手動數據遷移指南

## 問題說明

**現象：** Dashboard 顯示 "No projects yet"，但 Firestore 中有 "22222" 項目

**原因：** 項目存儲在舊路徑

- **舊路徑（錯誤）：** `projects/ITiDkYSplG8AWQG95TuP`
- **新路徑（正確）：** `users/AZ5Sk5FJBofAeKE09AYbGVlEoDy1/projects/ITiDkYSplG8AWQG95TuP`

---

## 🔧 方法 1：Firebase Console 手動遷移（推薦）

### 步驟 1：打開 Firestore

1. 前往：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/firestore
2. 點擊左側「Firestore Database」

---

### 步驟 2：檢查舊數據

1. 展開 `projects` collection
2. 找到項目：`ITiDkYSplG8AWQG95TuP`
3. 查看字段：
   ```
   name: "22222"
   userId: "AZ5Sk5FJBofAeKE09AYbGVlEoDy1"
   createdAt: 2025-11-07 16:58:09
   ```
4. **記下 `userId`：** `AZ5Sk5FJBofAeKE09AYbGVlEoDy1`

---

### 步驟 3：創建新路徑

1. 在 Firestore 左側，找到或創建 `users` collection
2. 點擊 `users`
3. 找到或創建文檔：`AZ5Sk5FJBofAeKE09AYbGVlEoDy1`
4. 在該文檔下，創建子集合：`projects`
5. 在 `projects` 子集合中，創建文檔：`ITiDkYSplG8AWQG95TuP`
6. 添加字段：
   ```
   name: "22222"
   createdAt: 2025-11-07 16:58:09 (Timestamp)
   ```
   **注意：** 不需要 `userId` 字段（因為已在路徑中）

---

### 步驟 4：遷移文檔（如果有）

1. 檢查 `documents` collection
2. 查找 `projectId == "ITiDkYSplG8AWQG95TuP"` 的文檔
3. 對每個文檔：
   - 在 `users/AZ5Sk5FJBofAeKE09AYbGVlEoDy1/projects/ITiDkYSplG8AWQG95TuP/documents` 創建新文檔
   - 複製所有字段（除了 `projectId`）

---

### 步驟 5：驗證

1. 刷新 https://vaultcaddy.com/dashboard.html
2. 清除瀏覽器緩存（Cmd/Ctrl + Shift + R）
3. **預期結果：** 應該看到 "22222" 項目

---

### 步驟 6：清理舊數據（確認後）

**⚠️  只有在確認新數據正確顯示後才執行！**

1. 刪除 `projects/ITiDkYSplG8AWQG95TuP`
2. 刪除 `documents` collection 中該項目的文檔

---

## 🚀 方法 2：使用 Cloud Functions（自動化）

### 創建臨時遷移 Function

在 `firebase-functions/index.js` 中添加：

```javascript
/**
 * 手動觸發的數據遷移 Function
 * 只需執行一次
 */
exports.migrateOldProjects = functions.https.onRequest(async (req, res) => {
    // 安全檢查：只允許管理員執行
    const authHeader = req.headers.authorization;
    if (!authHeader || authHeader !== 'Bearer YOUR_SECRET_KEY') {
        return res.status(403).send('Unauthorized');
    }
    
    try {
        const db = admin.firestore();
        let migratedCount = 0;
        
        // 獲取所有舊項目
        const oldProjects = await db.collection('projects').get();
        
        for (const projectDoc of oldProjects.docs) {
            const projectId = projectDoc.id;
            const projectData = projectDoc.data();
            
            if (!projectData.userId) {
                console.log(`跳過項目 ${projectId}：缺少 userId`);
                continue;
            }
            
            // 創建新路徑
            const newProjectRef = db.collection('users')
                .doc(projectData.userId)
                .collection('projects')
                .doc(projectId);
            
            // 複製數據（移除 userId）
            const { userId, ...newData } = projectData;
            await newProjectRef.set(newData);
            
            // 遷移文檔
            const oldDocs = await db.collection('documents')
                .where('projectId', '==', projectId)
                .get();
            
            for (const docDoc of oldDocs.docs) {
                const docData = docDoc.data();
                const { projectId: _, ...newDocData } = docData;
                
                await db.collection('users')
                    .doc(projectData.userId)
                    .collection('projects')
                    .doc(projectId)
                    .collection('documents')
                    .doc(docDoc.id)
                    .set(newDocData);
            }
            
            migratedCount++;
            console.log(`✅ 已遷移項目: ${projectData.name}`);
        }
        
        res.json({
            success: true,
            message: `成功遷移 ${migratedCount} 個項目`
        });
        
    } catch (error) {
        console.error('遷移失敗:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});
```

### 執行遷移

```bash
# 部署 Function
firebase deploy --only functions:migrateOldProjects

# 執行遷移（在瀏覽器或 curl）
curl -X POST https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/migrateOldProjects \
  -H "Authorization: Bearer YOUR_SECRET_KEY"
```

---

## 📊 驗證清單

遷移完成後，檢查以下內容：

- [ ] Firestore 中 `users/AZ5Sk5FJBofAeKE09AYbGVlEoDy1/projects` 有數據
- [ ] Dashboard 顯示 "22222" 項目
- [ ] 可以點擊項目並查看文檔
- [ ] Console 沒有權限錯誤
- [ ] 可以上傳新文件

---

## 🔍 故障排查

### 問題 1：遷移後還是看不到項目

**解決方案：**
1. 清除瀏覽器緩存（重要！）
2. 硬重新整理（Cmd/Ctrl + Shift + R）
3. 檢查 Console 是否有新的 `users/{userId}/projects` 查詢日誌

### 問題 2：userId 不匹配

**檢查：**
```javascript
// 在 Dashboard Console 輸入：
firebase.auth().currentUser.uid
// 應該等於 "AZ5Sk5FJBofAeKE09AYbGVlEoDy1"
```

### 問題 3：遷移後出現權限錯誤

**檢查 Firestore 規則：**
```
users/{userId}/projects/{projectId}
  - userId 必須等於 request.auth.uid
```

---

## 💡 預防未來問題

### 確保新項目使用正確路徑

已修復的代碼（`simple-data-manager.js`）：

```javascript
// ✅ 正確：使用 users/{userId}/projects
const docRef = await this.db.collection('users')
    .doc(userId)
    .collection('projects')
    .add(projectData);

// ❌ 錯誤：直接使用 projects
const docRef = await this.db.collection('projects').add(projectData);
```

---

## 📞 需要幫助？

如果遇到問題：

1. 提供 Console 的完整錯誤訊息
2. 提供 Firestore 的截圖
3. 確認是否已清除瀏覽器緩存

---

**建議：先使用方法 1（手動遷移），因為只有 1 個項目，5 分鐘即可完成！** 🚀

