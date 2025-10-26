# Firebase 設置指南

## 概述

本指南將幫助你完成 Firebase 的設置，實現數據持久化功能。

---

## 步驟 1：創建 Firebase 項目

### 1.1 訪問 Firebase Console

1. 訪問 [Firebase Console](https://console.firebase.google.com/)
2. 使用你的 Google 帳戶登入

### 1.2 創建新項目

1. 點擊 **"添加項目"** 或 **"Create a project"**
2. 輸入項目名稱：`vaultcaddy` 或你喜歡的名稱
3. （可選）啟用 Google Analytics
4. 點擊 **"創建項目"**
5. 等待項目創建完成（約 30 秒）

---

## 步驟 2：設置 Firestore 數據庫

### 2.1 創建 Firestore 數據庫

1. 在 Firebase Console 中，點擊左側菜單的 **"Firestore Database"**
2. 點擊 **"創建數據庫"** 或 **"Create database"**
3. 選擇模式：
   - **生產模式**（推薦）：需要設置安全規則
   - **測試模式**：30 天內允許所有讀寫（僅用於開發）
4. 選擇數據庫位置：
   - 推薦：`asia-east2`（香港）
   - 備選：`asia-northeast1`（東京）
5. 點擊 **"啟用"**

### 2.2 設置安全規則

在 Firestore 的 **"規則"** 標籤中，使用以下規則：

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 用戶只能訪問自己的數據
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
      
      // 允許匿名用戶訪問自己的數據
      allow read, write: if userId.matches('anonymous_.*');
      
      // 項目數據
      match /projects/{projectId} {
        allow read, write: if request.auth != null && request.auth.uid == userId
                           || userId.matches('anonymous_.*');
        
        // 文檔數據
        match /documents/{documentId} {
          allow read, write: if request.auth != null && request.auth.uid == userId
                             || userId.matches('anonymous_.*');
        }
      }
    }
  }
}
```

點擊 **"發布"** 保存規則。

---

## 步驟 3：設置 Authentication

### 3.1 啟用 Authentication

1. 在 Firebase Console 中，點擊左側菜單的 **"Authentication"**
2. 點擊 **"開始使用"** 或 **"Get started"**

### 3.2 啟用登入方式

1. 點擊 **"Sign-in method"** 標籤
2. 啟用以下登入方式：
   - **電子郵件/密碼**：點擊啟用
   - **Google**：點擊啟用（推薦）
   - **匿名**：點擊啟用（允許未登入用戶使用）

---

## 步驟 4：獲取 Firebase 配置

### 4.1 註冊 Web 應用

1. 在 Firebase Console 的項目概覽頁面
2. 點擊 **"添加應用"** 圖標（`</>`）
3. 輸入應用暱稱：`VaultCaddy Web`
4. （可選）啟用 Firebase Hosting
5. 點擊 **"註冊應用"**

### 4.2 複製配置

你會看到類似以下的配置代碼：

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "vaultcaddy.firebaseapp.com",
  projectId: "vaultcaddy",
  storageBucket: "vaultcaddy.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};
```

**複製這段配置代碼**，我們稍後會用到。

---

## 步驟 5：配置 VaultCaddy

### 5.1 更新 Firebase 配置

1. 打開 `firebase-config.js` 文件
2. 找到 `firebaseConfig` 對象
3. 將你複製的配置代碼替換進去：

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",              // 替換為你的 API Key
    authDomain: "YOUR_AUTH_DOMAIN",      // 替換為你的 Auth Domain
    projectId: "YOUR_PROJECT_ID",        // 替換為你的 Project ID
    storageBucket: "YOUR_STORAGE_BUCKET", // 替換為你的 Storage Bucket
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID", // 替換為你的 Messaging Sender ID
    appId: "YOUR_APP_ID"                 // 替換為你的 App ID
};
```

### 5.2 在 HTML 中加載 Firebase SDK

在 `firstproject.html` 的 `<head>` 標籤中添加以下代碼：

```html
<!-- Firebase SDK -->
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>

<!-- Firebase 配置和數據管理器 -->
<script src="firebase-config.js?v=1.0"></script>
<script src="firebase-data-manager.js?v=1.0"></script>
```

---

## 步驟 6：測試 Firebase 連接

### 6.1 打開瀏覽器開發者工具

1. 打開 VaultCaddy 網站
2. 按 `F12` 打開開發者工具
3. 切換到 **Console** 標籤

### 6.2 查看初始化日誌

你應該看到以下日誌：

```
✅ Firebase 配置模塊已載入
✅ Firebase App 已初始化
✅ Firestore 已初始化
✅ Firebase Authentication 已初始化
✅ Firestore 離線持久化已啟用
✅ Firebase 數據管理器初始化完成
```

### 6.3 測試數據寫入

在 Console 中執行以下代碼：

```javascript
// 測試創建項目
await window.firebaseDataManager.createProject({
    name: '測試項目',
    description: '這是一個測試項目'
});

// 測試獲取項目
const projects = await window.firebaseDataManager.getProjects();
console.log('項目列表:', projects);
```

如果成功，你會看到項目已創建並返回。

---

## 步驟 7：遷移現有數據

### 7.1 從 LocalStorage 遷移

如果你已經有 LocalStorage 中的數據，可以執行遷移：

```javascript
// 在瀏覽器 Console 中執行
await window.firebaseDataManager.migrateFromLocalStorage();
```

這會將所有項目和文檔從 LocalStorage 遷移到 Firebase。

### 7.2 驗證遷移結果

1. 在 Firebase Console 中打開 **Firestore Database**
2. 查看 `users` 集合
3. 你應該看到你的用戶 ID 和相關數據

---

## Firebase 定價和成本

### 免費額度（Spark 計劃）

| 資源 | 免費額度 |
|------|----------|
| **存儲空間** | 1 GB |
| **文檔讀取** | 50,000 次/天 |
| **文檔寫入** | 20,000 次/天 |
| **文檔刪除** | 20,000 次/天 |
| **網絡出站** | 10 GB/月 |

### 使用場景估算（Pro 方案：500 頁/月）

| 操作 | 次數/月 | 成本 (HKD) |
|------|---------|------------|
| 文檔寫入 | 500 | 0.007 |
| 文檔讀取 | 2,000 | 0.009 |
| 存儲空間 | 25 MB | 0.035 |
| **總計** | | **≈ HKD 0.05** |

**結論**：在 Pro 方案（500 頁/月）下，Firebase **完全免費**！

---

## 常見問題

### Q1: Firebase 初始化失敗
**A**: 檢查以下幾點：
1. Firebase SDK 是否正確加載？
2. `firebase-config.js` 中的配置是否正確？
3. 瀏覽器 Console 是否有錯誤訊息？

### Q2: 無法寫入數據
**A**: 檢查 Firestore 安全規則是否正確設置。在開發階段，可以暫時使用測試模式。

### Q3: 數據遷移失敗
**A**: 確保：
1. Firebase 已正確初始化
2. LocalStorage 中有數據
3. 網絡連接正常

### Q4: 如何查看 Firebase 使用量？
**A**: 在 Firebase Console 中：
1. 點擊左側菜單的 **"Usage and billing"**
2. 查看 Firestore 和 Authentication 的使用情況

---

## 數據結構

Firebase 中的數據結構如下：

```
users/
  {userId}/
    projects/
      {projectId}/
        - name
        - description
        - createdAt
        - updatedAt
        documents/
          {documentId}/
            - fileName
            - fileSize
            - fileType
            - documentType
            - uploadDate
            - status
            - processedData
            - createdAt
            - updatedAt
```

---

## 下一步

設置完成後，你可以：
1. 測試創建和讀取項目
2. 測試上傳文檔
3. 驗證數據同步
4. 遷移現有的 LocalStorage 數據

**祝你使用愉快！** 🎉

