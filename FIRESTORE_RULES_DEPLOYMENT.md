# Firestore 安全規則部署指南

## 🚨 問題：權限被拒絕錯誤

從圖1-3的錯誤可以看到：
```
FirebaseError: Missing or insufficient permissions
code: "permission-denied"
```

這是因為 Firestore 安全規則不正確或未部署。

---

## ✅ 解決方案

### 步驟 1：部署 Firestore 規則

1. **前往 Firebase Console**
   - 打開：https://console.firebase.google.com/
   - 選擇您的項目：`vaultcaddy-production-cbbe2`

2. **部署安全規則**
   ```bash
   # 方法 1：使用 Firebase CLI（推薦）
   firebase deploy --only firestore:rules
   
   # 方法 2：手動複製規則
   # 打開 Firebase Console → Firestore Database → Rules
   # 複製下方的規則並點擊「發布」
   ```

3. **正確的 Firestore 規則**（已創建在 `firestore.rules`）：

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 用戶文檔規則
    match /users/{userId} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if request.auth != null && request.auth.uid == userId;
      
      // Credits 歷史記錄
      match /creditsHistory/{historyId} {
        allow read: if request.auth != null && request.auth.uid == userId;
        allow write: if request.auth != null && request.auth.uid == userId;
      }
      
      // 用戶項目
      match /projects/{projectId} {
        allow read: if request.auth != null && request.auth.uid == userId;
        allow write: if request.auth != null && request.auth.uid == userId;
        
        // 項目文檔
        match /documents/{documentId} {
          allow read: if request.auth != null && request.auth.uid == userId;
          allow write: if request.auth != null && request.auth.uid == userId;
        }
      }
    }
    
    // 項目文檔規則（備用路徑）
    match /projects/{projectId}/documents/{documentId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    // 驗證碼規則
    match /verificationCodes/{email} {
      allow read: if request.auth != null;
      allow write: if true; // 允許註冊時寫入
    }
  }
}
```

### 步驟 2：部署 Storage 規則

1. **正確的 Storage 規則**（已存在於 `firebase-storage-rules.txt`）：

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /documents/{userId}/{projectId}/{fileName} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /users/{userId}/projects/{projectId}/{fileName} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /projects/{projectId}/documents/{fileName} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    match /{projectId}/{fileName} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    match /{fileName} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
  }
}
```

2. **部署 Storage 規則**：
   ```bash
   # 使用 Firebase CLI
   firebase deploy --only storage
   
   # 或手動部署：
   # Firebase Console → Storage → Rules → 複製並發布
   ```

---

## 📋 驗證規則是否生效

### 方法 1：使用 Firebase Console

1. 前往 Firestore Database → Rules
2. 檢查規則是否已更新
3. 查看「已發布」時間戳

### 方法 2：測試上傳

1. 刷新網頁：https://vaultcaddy.com/firstproject.html
2. 嘗試上傳文件
3. 打開開發者工具（F12）查看錯誤

**成功的標誌：**
```
✅ 文檔記錄已創建: [docId]
✅ 文件已上傳到 Storage
🤖 開始 AI 處理: eStatementFile_20250829143359.pdf
```

**失敗的標誌：**
```
❌ FirebaseError: Missing or insufficient permissions
```

---

## 🔧 其他可能的問題

### 問題 1：Firebase Storage CORS 錯誤

**錯誤信息：**
```
Access to fetch at 'https://firebasestorage.googleapis.com/...' 
has been blocked by CORS policy
```

**解決方案：**
這通常不是規則問題，而是 CORS 配置。Firebase Storage 默認允許來自同一項目的請求。

**檢查步驟：**
1. 確認使用正確的 Firebase 項目
2. 確認 `config.js` 中的配置正確
3. 嘗試清除瀏覽器緩存

### 問題 2：Vision API 錯誤

**錯誤信息：**
```
❌ 混合處理失敗: Error: Vision API 未能提取文本
```

**可能原因：**
1. API 密鑰無效
2. API 配額用完
3. 文件格式不支持

**解決方案：**
```javascript
// 檢查 hybrid-vision-deepseek.js 中的 API 密鑰
this.visionApiKey = 'AIzaSyCpH0qoL0wSEtHzutJzIqElbL_17cBuvug';
```

前往 [Google Cloud Console](https://console.cloud.google.com/) 驗證：
1. API 是否啟用
2. 配額是否充足
3. 密鑰是否有效

### 問題 3：DeepSeek API 錯誤

**錯誤信息：**
```
❌ AI 處理失敗: DeepSeek API 請求失敗
```

**檢查步驟：**
1. 檢查 Cloudflare Worker 是否正常運行
2. 訪問：https://deepseek-proxy.vaultcaddy.workers.dev
3. 應該看到：`{"status":"ok","message":"DeepSeek Proxy is running"}`

**如果 Worker 未運行：**
```bash
# 重新部署 Cloudflare Worker
cd cloudflare-worker-deepseek
wrangler publish
```

---

## 🎯 快速修復檢查清單

完成以下步驟以修復問題：

- [ ] **1. 部署 Firestore 規則**
  ```bash
  firebase deploy --only firestore:rules
  ```

- [ ] **2. 部署 Storage 規則**
  ```bash
  firebase deploy --only storage
  ```

- [ ] **3. 驗證 Vision API**
  - 檢查 API 密鑰
  - 確認配額充足

- [ ] **4. 驗證 DeepSeek Worker**
  - 訪問 Worker URL
  - 確認返回 `status: ok`

- [ ] **5. 測試上傳**
  - 刷新頁面
  - 上傳測試文件
  - 查看控制台無錯誤

- [ ] **6. 驗證 Credits 退款**
  - 如果處理失敗
  - 檢查 Credits 是否退回
  - 查看 creditsHistory

---

## 📞 如果問題仍未解決

1. **查看完整錯誤日誌**
   - 打開開發者工具（F12）
   - 切換到 Console 標籤
   - 複製完整錯誤信息

2. **檢查 Firestore 數據結構**
   - 前往 Firebase Console → Firestore
   - 確認數據路徑正確：
     ```
     users/{userId}/projects/{projectId}/documents/{documentId}
     ```

3. **驗證用戶身份**
   ```javascript
   // 在控制台執行
   const user = firebase.auth().currentUser;
   console.log('User:', user.uid, user.email);
   ```

---

## ✅ 預期結果

部署規則後，您應該能夠：

1. ✅ 成功上傳文件到 Firebase Storage
2. ✅ 創建 Firestore 文檔記錄
3. ✅ AI 處理文件並提取數據
4. ✅ 如果失敗，自動退回 Credits
5. ✅ 查看處理狀態和結果

**成功的控制台輸出：**
```
✅ 文檔記錄已創建: abc123
✅ 文件已上傳到 Storage
🤖 開始 AI 處理: eStatementFile_20250829143359.pdf (3 頁)
🔄 步驟 1: Google Vision API OCR
✅ Vision API 提取了 1234 個字符
🔄 步驟 2: DeepSeek 分析
✅ DeepSeek 分析完成
✅ 混合處理完成（耗時: 5.2 秒）
✅ 文檔狀態已更新
```

---

**現在請執行：`firebase deploy --only firestore:rules storage`** 🚀
