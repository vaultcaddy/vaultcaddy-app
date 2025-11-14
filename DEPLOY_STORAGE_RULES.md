# 🔧 部署 Firebase Storage Rules

## 問題
Vision API 無法訪問 Firebase Storage 中的文件，導致銀行對帳單處理失敗。

---

## ✅ 解決方案：部署新的 Storage Rules

### 步驟 1：檢查 firebase-storage-rules.txt

```bash
cd /Users/cavlinyeung/ai-bank-parser
cat firebase-storage-rules.txt
```

**應該看到：**
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // 允許 Vision API 公開讀取（用於 AI 處理）
    match /{allPaths=**} {
      allow read: if request.auth != null || request.auth == null;
      allow write: if request.auth != null;
    }
  }
}
```

**說明：**
- ✅ `allow read: if request.auth != null || request.auth == null` - 允許所有讀取（包括 Vision API）
- ✅ `allow write: if request.auth != null` - 只有認證用戶可以寫入

---

### 步驟 2：部署 Storage Rules

**方法 A：使用 Firebase Console（推薦，最簡單）**

1. **打開 Firebase Console：**
   ```
   https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/storage/rules
   ```

2. **點擊「Rules」標籤**

3. **複製並貼上新規則：**
   ```
   rules_version = '2';
   service firebase.storage {
     match /b/{bucket}/o {
       match /{allPaths=**} {
         allow read: if request.auth != null || request.auth == null;
         allow write: if request.auth != null;
       }
     }
   }
   ```

4. **點擊「Publish」（發布）**

5. **等待 5-10 秒讓規則生效**

---

**方法 B：使用 Firebase CLI**

```bash
# 1. 確認已登入
firebase login

# 2. 切換到項目目錄
cd /Users/cavlinyeung/ai-bank-parser

# 3. 部署 Storage Rules
firebase deploy --only storage

# 預期輸出：
# === Deploying to 'vaultcaddy-production-cbbe2'...
# ✔  Deploy complete!
```

---

### 步驟 3：驗證 Storage Rules

**在 Firebase Console 中：**
1. 前往 Storage > Rules
2. 確認規則已更新
3. 查看「Last updated」時間戳

---

### 步驟 4：測試銀行對帳單上傳

1. **刷新網頁（Ctrl+F5）**

2. **登入帳戶**

3. **上傳銀行對帳單 PDF**

4. **打開瀏覽器控制台（F12）**

5. **查看是否有錯誤**

**成功的標誌：**
- ✅ 無 "Vision API 未返回文本" 錯誤
- ✅ 看到 "Vision API 處理成功"
- ✅ 文件狀態變為 "completed"（已完成）
- ✅ 可以看到提取的數據

---

## 🔍 故障排除

### 問題 1：Firebase CLI 找不到

```bash
# 安裝 Firebase CLI
npm install -g firebase-tools

# 驗證安裝
firebase --version
```

### 問題 2：部署權限錯誤

```bash
# 重新登入
firebase logout
firebase login

# 確認項目
firebase projects:list
firebase use vaultcaddy-production-cbbe2
```

### 問題 3：規則部署後仍然報錯

**解決方法：**
1. 等待 5-10 分鐘（Firebase 需要時間同步）
2. 清除瀏覽器緩存
3. 重新上傳文件測試

### 問題 4：擔心安全性

**說明：**
- ✅ 讀取權限：允許 Vision API 訪問文件進行 AI 處理
- ✅ 寫入權限：仍然需要認證，未授權用戶無法上傳
- ✅ 文件 URL：包含難以猜測的 token，不會被隨機訪問
- ✅ CORS：已設置，只允許 vaultcaddy.com 和 localhost

**如果需要更嚴格的規則：**
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /users/{userId}/projects/{projectId}/{fileName} {
      allow read: if request.auth != null && request.auth.uid == userId;
      allow write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

但這會導致 Vision API 無法訪問文件。**推薦使用當前規則。**

---

## 📞 需要幫助？

如果部署後仍然有問題，請告訴我：

1. Firebase Console Storage Rules 的截圖
2. `firebase deploy --only storage` 的完整輸出
3. 瀏覽器控制台（F12）的錯誤信息
4. 上傳文件後的文件狀態（pending/processing/completed/failed）

我會幫您進一步診斷！🚀

