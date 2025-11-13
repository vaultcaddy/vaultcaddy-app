# 🔄 遷移舊數據到正確路徑

## 問題說明

**當前狀態：**
- "22222" 項目在：`projects/ITiDkYSplG8AWQG95TuP` ❌ 錯誤路徑
- "555" 項目可能在：`users/{userId}/projects/{projectId}` ✅ 正確路徑

**正確路徑：**
```
users/{userId}/projects/{projectId}/documents/{documentId}
```

---

## 🎯 為什麼只用一種路徑？

### 您的理解是完全正確的！

**1. 數據隔離**
```
用戶 A：users/userA/projects/projectA
用戶 B：users/userB/projects/projectB
```
- ✅ 用戶 A **絕對看不到**用戶 B 的項目
- ✅ Firestore Rules 自動驗證 `userId == request.auth.uid`

**2. 安全性**
```javascript
// Firestore Rules
match /users/{userId}/projects/{projectId} {
  // 只有當 userId === 登入用戶 ID 才允許
  allow read: if request.auth.uid == userId;
  allow write: if request.auth.uid == userId;
}
```

**3. 數據結構清晰**
```
users/
  {userId}/
    ├── email: "user@example.com"
    ├── credits: 10
    │
    └── projects/
        └── {projectId}/
            ├── name: "My Project"
            ├── createdAt: Timestamp
            │
            └── documents/
                └── {documentId}/
                    ├── fileName: "invoice.pdf"
                    └── fileUrl: "gs://..."
```

---

## 🔧 遷移步驟（5 分鐘）

### 方法 1：Firebase Console 手動遷移（推薦）

#### 步驟 1：打開 Firebase Console

前往：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/firestore

---

#### 步驟 2：找到舊項目 "22222"

1. 展開 `projects` collection
2. 找到 `ITiDkYSplG8AWQG95TuP`
3. 記下內容：
   ```
   name: "22222"
   userId: "AZ5Sk5FJBofAeKE09AYbGVlEoDy1"
   createdAt: 2025-11-07 16:58:09
   ```

---

#### 步驟 3：在正確路徑創建項目

1. **導航到：** `users` collection
2. **找到文檔：** `AZ5Sk5FJBofAeKE09AYbGVlEoDy1`
   - 如果不存在，創建它：
     ```
     文檔 ID: AZ5Sk5FJBofAeKE09AYbGVlEoDy1
     字段：
       email: "osclin2002@gmail.com"
       credits: 80000
       createdAt: [當前時間]
     ```

3. **在該文檔下創建子集合：** `projects`
4. **在 `projects` 子集合中創建文檔：**
   ```
   文檔 ID: ITiDkYSplG8AWQG95TuP（使用相同 ID）
   字段：
     name: "22222"
     createdAt: 2025-11-07T16:58:09Z
   ```

---

#### 步驟 4：驗證新路徑

1. 刷新 Dashboard（`Cmd + Shift + R`）
2. 應該看到 "22222" 項目
3. Console 應該顯示：
   ```
   ✅ 找到: 1 個項目
   ✅ 獲取 1 個項目
   ```

---

#### 步驟 5：刪除舊路徑數據

**⚠️ 只有確認新路徑正常後才執行！**

1. 返回 Firebase Console
2. 刪除 `projects/ITiDkYSplG8AWQG95TuP`
3. 檢查是否有 `documents` collection 中屬於這個項目的文檔，也一併刪除

---

## 🔍 檢查 "555" 項目

### 步驟 1：在 Firebase Console 中查找

**查找位置 1（正確路徑）：**
```
users/AZ5Sk5FJBofAeKE09AYbGVlEoDy1/projects/
```
- 如果在這裡，✅ 正確，無需遷移

**查找位置 2（錯誤路徑）：**
```
projects/
```
- 如果在這裡，❌ 需要遷移

---

### 步驟 2：如果 "555" 在錯誤路徑

重複上面的遷移步驟：
1. 複製項目數據
2. 在 `users/{userId}/projects/` 創建
3. 驗證後刪除舊數據

---

## 📊 驗證數據結構

### 正確的 Firestore 結構

```
✅ users/
   └── AZ5Sk5FJBofAeKE09AYbGVlEoDy1/
       ├── email: "osclin2002@gmail.com"
       ├── credits: 80000
       ├── currentCredits: 80000
       │
       ├── creditsHistory/
       │   └── {historyId}/
       │       ├── type: "usage"
       │       ├── amount: 3
       │       └── createdAt: Timestamp
       │
       └── projects/
           ├── ITiDkYSplG8AWQG95TuP/  ← "22222" 項目
           │   ├── name: "22222"
           │   ├── createdAt: Timestamp
           │   │
           │   └── documents/
           │       └── {documentId}/
           │           ├── fileName: "invoice.pdf"
           │           └── fileUrl: "gs://..."
           │
           └── {555ProjectId}/  ← "555" 項目
               ├── name: "555"
               └── createdAt: Timestamp

❌ projects/  ← 應該刪除
   └── ITiDkYSplG8AWQG95TuP/  ← 舊數據，應該刪除
```

---

## 🔐 安全性驗證

### 測試 1：用戶 A 看不到用戶 B 的數據

**場景：**
- 用戶 A (ID: userA) 登入
- 嘗試訪問 `users/userB/projects`

**預期結果：**
```
❌ Firestore 規則阻止（permission-denied）
```

**代碼驗證：**
```javascript
// 這會失敗（被 Firestore Rules 阻止）
const otherUserProjects = await db.collection('users')
    .doc('userB')  // ← 不是當前用戶
    .collection('projects')
    .get();  // ❌ Permission denied
```

---

### 測試 2：只能讀取自己的數據

**場景：**
- 用戶 A (ID: userA) 登入
- 訪問 `users/userA/projects`

**預期結果：**
```
✅ 成功讀取自己的項目
```

**代碼驗證：**
```javascript
// 這會成功
const myProjects = await db.collection('users')
    .doc(firebase.auth().currentUser.uid)  // ← 當前用戶
    .collection('projects')
    .get();  // ✅ Success
```

---

## 💡 關鍵理解

### Q1: 文件在用戶帳戶中建立的文件夾上載後只會是這個用戶帳戶中才可看到對嗎？

**A: 完全正確！** ✅

**原因：**

1. **路徑包含 userId：**
   ```
   users/{userId}/projects/{projectId}/documents/{documentId}
          ^^^^^^^
          這裡確保數據隔離
   ```

2. **Firestore Rules 驗證：**
   ```javascript
   match /users/{userId}/projects/{projectId} {
     // 只有當 userId === 登入用戶 ID 才允許
     allow read: if request.auth.uid == userId;
   }
   ```

3. **即使知道其他用戶的 projectId，也無法訪問：**
   ```javascript
   // 嘗試訪問其他用戶的項目
   await db.collection('users')
       .doc('otherUserId')  // ❌ 不是自己
       .collection('projects')
       .doc('knownProjectId')
       .get();
   
   // 結果：❌ Permission denied
   ```

---

### Q2: 為什麼要統一用 users/{userId} 路徑？

**A: 三大原因：**

**1. 自動權限驗證**
```javascript
// Firestore Rules 自動檢查
if (request.auth.uid == userId) {
    // ✅ 是自己的數據，允許訪問
} else {
    // ❌ 不是自己的數據，拒絕訪問
}
```

**2. 數據整合**
```
users/{userId}/
  ├── credits           ← 用戶 Credits
  ├── creditsHistory    ← Credits 歷史
  ├── projects          ← 用戶項目
  └── subscription      ← 訂閱信息
  
所有用戶數據在一個地方，易於管理！
```

**3. 簡化查詢**
```javascript
// 只需一個查詢，獲取用戶所有數據
const userData = await db.collection('users')
    .doc(userId)
    .get();

const projects = await db.collection('users')
    .doc(userId)
    .collection('projects')
    .get();
```

---

## 🚀 遷移後檢查清單

完成遷移後，確認以下內容：

- [ ] Dashboard 顯示所有項目（22222 和 555）
- [ ] 可以創建新項目
- [ ] 新項目顯示在列表中
- [ ] 可以上傳文件到項目
- [ ] 文件顯示在項目中
- [ ] Console 沒有權限錯誤
- [ ] 舊路徑 `projects/` collection 已刪除
- [ ] 只有一個正確路徑：`users/{userId}/projects/`

---

## 📝 遷移腳本（可選）

如果舊項目很多，可以使用腳本批量遷移：

```javascript
// 在 Firebase Console 的 Cloud Functions 中執行

async function migrateAllProjects() {
    const db = admin.firestore();
    
    // 獲取所有舊項目
    const oldProjects = await db.collection('projects').get();
    
    for (const projectDoc of oldProjects.docs) {
        const data = projectDoc.data();
        const userId = data.userId;
        
        if (!userId) {
            console.log('跳過項目（無 userId）:', projectDoc.id);
            continue;
        }
        
        // 創建新路徑
        await db.collection('users')
            .doc(userId)
            .collection('projects')
            .doc(projectDoc.id)
            .set({
                name: data.name,
                createdAt: data.createdAt
            });
        
        console.log('✅ 已遷移:', data.name);
    }
    
    console.log('🎉 遷移完成！');
}
```

---

**準備好開始遷移了嗎？** 🚀

**建議：先手動遷移 "22222" 項目（5 分鐘），確認無誤後再處理其他項目。**

