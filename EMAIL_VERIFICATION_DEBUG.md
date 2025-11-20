# 🐛 Email 驗證失敗診斷

## 📊 錯誤分析

根據 Console 截圖，發現以下錯誤：

### 1️⃣ Firebase Storage 錯誤
```
firebase.storage is not a function
at initializeFirebase (firebase-config.js:108:20)
```

**原因**: `firebase-config.js` 嘗試初始化 `firebase.storage()`，但 Storage SDK 未正確載入。

---

### 2️⃣ Email 驗證 400 錯誤
```
Failed to load resource: verify-email.html?email=osclin2002%40gmail.com:367
the server responded with a status of 400 ()
```

**原因**: Firebase Functions 調用失敗，可能原因：
1. Functions 未部署
2. Email 配置未設置
3. CORS 問題

---

## 🔍 診斷步驟

### 步驟 1: 檢查 Firebase Functions 部署狀態

```bash
cd firebase-functions
firebase functions:list
```

**預期輸出**:
```
✔ functions: Loaded successfully

┌──────────────────────────────┬─────────┬────────┐
│ Name                         │ Status  │ Region │
├──────────────────────────────┼─────────┼────────┤
│ sendVerificationCode         │ ACTIVE  │ us-ce… │
│ verifyCode                   │ ACTIVE  │ us-ce… │
│ checkEmailVerified           │ ACTIVE  │ us-ce… │
└──────────────────────────────┴─────────┴────────┘
```

如果 Functions 不存在或狀態不是 ACTIVE，需要重新部署。

---

### 步驟 2: 檢查 Email 配置

```bash
cd firebase-functions
firebase functions:config:get
```

**預期輸出**:
```json
{
  "email": {
    "user": "your-email@gmail.com",
    "password": "your-app-password"
  }
}
```

如果沒有 `email` 配置，需要設置。

---

### 步驟 3: 檢查 Firebase Storage SDK

打開 `verify-email.html`，確認是否載入了 Storage SDK：

```html
<script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-storage-compat.js"></script>
```

如果缺少這行，需要添加。

---

## 🔧 修復方案

### 修復 1: 重新部署 Firebase Functions

```bash
cd firebase-functions

# 1. 安裝依賴
npm install

# 2. 設置 Email 配置（如果未設置）
firebase functions:config:set email.user="your-email@gmail.com" email.password="your-app-password"

# 3. 部署 Functions
firebase deploy --only functions
```

**注意**: 
- `your-email@gmail.com` 替換為您的 Gmail
- `your-app-password` 替換為 Gmail 應用專用密碼（不是普通密碼）

**如何生成 Gmail 應用專用密碼**:
1. 訪問 https://myaccount.google.com/apppasswords
2. 選擇「郵件」和「其他（自訂名稱）」
3. 輸入「VaultCaddy」
4. 複製生成的 16 位密碼

---

### 修復 2: 修復 Firebase Storage 錯誤

編輯 `firebase-config.js`，將 Storage 初始化改為可選：

```javascript
// 修改前
firebase.storage();

// 修改後
if (typeof firebase.storage === 'function') {
    firebase.storage();
} else {
    console.warn('⚠️ Firebase Storage SDK 未載入');
}
```

或者，在 `verify-email.html` 中添加 Storage SDK：

```html
<!-- 在 firebase-auth-compat.js 之後添加 -->
<script defer src="https://www.gstatic.com/firebasejs/10.7.0/firebase-storage-compat.js"></script>
```

---

### 修復 3: 檢查 Functions CORS

確保 Functions 允許跨域請求。在 `firebase-functions/index.js` 中：

```javascript
const cors = require('cors')({ origin: true });

exports.sendVerificationCode = functions.https.onRequest((req, res) => {
    cors(req, res, async () => {
        // ... 原有邏輯 ...
    });
});
```

**但是**，您使用的是 `onCall`，這已經自動處理 CORS，所以這個問題可能性較低。

---

## 🧪 測試步驟

### 1. 測試 Functions 是否可訪問

使用 `curl` 測試：

```bash
# 替換為您的 project ID
curl -X POST \
  https://us-central1-vaultcaddy-production-cbbe2.cloudfunctions.net/sendVerificationCode \
  -H "Content-Type: application/json" \
  -d '{"data": {"email": "test@example.com"}}'
```

**預期結果**: 返回 JSON，而非 400 錯誤。

---

### 2. 檢查 Console 日誌

訪問 Firebase Console:
1. 打開 https://console.firebase.google.com/
2. 選擇專案 `vaultcaddy-production-cbbe2`
3. 進入 Functions → Logs
4. 查看是否有錯誤日誌

---

### 3. 測試 Email 驗證流程

1. 註冊新用戶
2. 跳轉到 `verify-email.html?email=your-email@gmail.com`
3. 打開 Console (F12)
4. 查看是否有錯誤

**預期日誌**:
```
✅ Firebase 已初始化
📧 Email: your-email@gmail.com
✅ 初始化完成
```

---

## 📝 快速修復指令

如果您還沒有部署 Functions，執行以下指令：

```bash
# 1. 進入 Functions 目錄
cd /Users/cavlinyeung/ai-bank-parser/firebase-functions

# 2. 安裝依賴（如果未安裝）
npm install nodemailer

# 3. 設置 Email 配置
firebase functions:config:set \
  email.user="osclin2002@gmail.com" \
  email.password="YOUR_APP_PASSWORD_HERE"

# 4. 部署 Functions
firebase deploy --only functions:sendVerificationCode,functions:verifyCode,functions:checkEmailVerified

# 5. 查看部署結果
firebase functions:list
```

---

## 🎯 最可能的原因

根據 400 錯誤，**最可能的原因是 Firebase Functions 未部署或 Email 配置未設置**。

**建議**:
1. 先執行「快速修復指令」
2. 確認 Functions 部署成功
3. 重新測試 Email 驗證

---

## 📞 如果仍然失敗

如果執行上述步驟後仍然失敗，請提供：

1. **Functions 部署日誌**:
   ```bash
   firebase deploy --only functions 2>&1 | tee deploy.log
   ```

2. **Functions 列表**:
   ```bash
   firebase functions:list
   ```

3. **Email 配置**:
   ```bash
   firebase functions:config:get
   ```

4. **Console 完整錯誤**:
   - 打開 Chrome DevTools
   - 切換到 Console 標籤
   - 複製所有紅色錯誤

這樣我可以更準確地診斷問題。

---

**更新日期**: 2025-11-20  
**狀態**: 待修復

