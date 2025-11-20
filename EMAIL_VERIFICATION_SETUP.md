# Email 驗證功能設置指南

## 📧 問題說明（圖1）
用戶註冊時，Email 驗證碼無法發送。這是因為 Firebase Functions 需要部署並配置 Email 服務。

## ✅ 代碼狀態
Email 驗證的所有代碼已經實現：
- **前端**: `verify-email.html` - 驗證頁面
- **前端**: `email-verification-check.js` - 驗證檢查模組
- **後端**: `firebase-functions/index.js` - Firebase Cloud Functions

## 🔧 需要完成的設置

### 1. 配置 Gmail SMTP (推薦)

Firebase Functions 使用 Gmail SMTP 發送驗證碼。需要：

#### a) 創建 Gmail App Password
1. 訪問 [Google Account Security](https://myaccount.google.com/security)
2. 開啟「2-Step Verification」（兩步驟驗證）
3. 在「App passwords」中創建新密碼
4. 選擇「Mail」和「Other (Custom name)」-> 輸入「VaultCaddy」
5. 複製生成的 16 位密碼（例如：`abcd efgh ijkl mnop`）

#### b) 配置 Firebase Functions
```bash
# 設置 Email 配置
firebase functions:config:set email.user="your-gmail@gmail.com" email.password="your-app-password"

# 查看當前配置
firebase functions:config:get
```

### 2. 部署 Firebase Functions

```bash
# 進入 functions 目錄
cd firebase-functions

# 安裝依賴（如果尚未安裝）
npm install

# 部署到 Firebase
firebase deploy --only functions:sendVerificationCode,functions:verifyCode,functions:checkEmailVerified

# 或部署所有 Functions
firebase deploy --only functions
```

### 3. 驗證部署

部署成功後，在 Firebase Console 中：
1. 前往 **Functions** 標籤
2. 確認以下 Functions 已部署：
   - `sendVerificationCode` - 發送驗證碼
   - `verifyCode` - 驗證驗證碼
   - `checkEmailVerified` - 檢查驗證狀態

### 4. 測試 Email 發送

```bash
# 使用 Firebase CLI 測試
firebase functions:shell

# 在 shell 中執行
sendVerificationCode({email: "test@example.com", displayName: "Test User"})
```

## 📋 完整的 Email 發送流程

### 1. 註冊時（`auth.html`）
```javascript
// 用戶註冊成功後自動發送驗證碼
const sendCodeFunc = functions.httpsCallable('sendVerificationCode');
const result = await sendCodeFunc({ 
    email: userEmail, 
    displayName: userName 
});
```

### 2. 驗證頁面（`verify-email.html`）
```javascript
// 用戶輸入驗證碼後
const verifyFunc = functions.httpsCallable('verifyCode');
const result = await verifyFunc({ 
    email: userEmail, 
    code: verificationCode 
});

// 驗證成功後發放 20 Credits
```

### 3. 檢查驗證狀態（`email-verification-check.js`）
```javascript
// 在 dashboard 等頁面檢查
const checkFunc = functions.httpsCallable('checkEmailVerified');
const result = await checkFunc({ email: userEmail });

if (!result.data.verified) {
    // 顯示「立即驗證您的 email 即送 20 Credits 試用！」橫幅
}
```

## 🎁 驗證獎勵

驗證成功後，用戶會自動獲得：
- ✅ **20 個免費 Credits**
- ✅ **可處理 20 頁文檔**
- ✅ **移除驗證提示橫幅**

## 🚨 故障排除

### 問題 1: Email 未發送
**症狀**: 用戶點擊「發送驗證碼」後沒有收到 Email

**檢查**:
1. 確認 Firebase Functions 已部署：`firebase functions:list`
2. 確認 Email 配置：`firebase functions:config:get`
3. 查看 Functions 日誌：`firebase functions:log`

### 問題 2: Gmail SMTP 錯誤
**症狀**: `Username and Password not accepted`

**解決**:
1. 確認已開啟 Gmail 兩步驟驗證
2. 使用 App Password，不是 Gmail 密碼
3. App Password 移除空格：`abcdefghijklmnop`

### 問題 3: Functions 配置丟失
**症狀**: 部署後 Email 配置消失

**解決**:
```bash
# 重新設置配置
firebase functions:config:set email.user="your-gmail@gmail.com" email.password="your-app-password"

# 部署
firebase deploy --only functions
```

## 📊 監控和日誌

### 查看 Functions 執行日誌
```bash
# 實時日誌
firebase functions:log

# 查看特定 Function
firebase functions:log sendVerificationCode
```

### Firebase Console
1. 前往 [Firebase Console](https://console.firebase.google.com)
2. 選擇項目
3. **Functions** -> 選擇 Function -> **Logs**

## 🔒 安全最佳實踐

1. **不要** 在代碼中硬編碼 Email 密碼
2. **使用** Firebase Functions Config 或 Secret Manager
3. **定期** 更換 Gmail App Password
4. **監控** Functions 執行次數，防止濫用
5. **設置** Firebase Functions 配額限制

## 📝 相關文件

- **前端代碼**: 
  - `verify-email.html` - 驗證頁面
  - `email-verification-check.js` - 驗證檢查
  - `auth.html` - 註冊頁面

- **後端代碼**:
  - `firebase-functions/index.js` (行 453-555) - `sendVerificationCode`
  - `firebase-functions/index.js` (行 557-600) - `verifyCode`
  - `firebase-functions/index.js` (行 602-650) - `checkEmailVerified`

## 🎯 快速開始命令

```bash
# 1. 配置 Email
firebase functions:config:set email.user="your-gmail@gmail.com" email.password="your-app-password"

# 2. 部署 Functions
cd firebase-functions
npm install
firebase deploy --only functions

# 3. 測試
# 訪問 https://vaultcaddy.com/auth.html
# 註冊新用戶
# 檢查 Email 收件箱
```

## ✅ 完成檢查清單

- [ ] Gmail App Password 已創建
- [ ] Firebase Functions Config 已設置
- [ ] Firebase Functions 已部署
- [ ] 測試發送驗證碼成功
- [ ] 測試驗證驗證碼成功
- [ ] 測試驗證獎勵（20 Credits）發放成功
- [ ] 驗證橫幅正確顯示/隱藏

---

## 📞 需要協助？

如果遇到問題，請：
1. 檢查 Firebase Functions 日誌：`firebase functions:log`
2. 查看 Browser Console 錯誤（F12）
3. 確認 Email 配置：`firebase functions:config:get`
4. 查閱 [Firebase Functions 文檔](https://firebase.google.com/docs/functions)
