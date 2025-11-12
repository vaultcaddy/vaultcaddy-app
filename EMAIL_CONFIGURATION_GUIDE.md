# Email 驗證配置指南

## 🚨 問題：無法發送驗證碼

從圖5可以看到：
- ❌ 發送失敗，請稍後重試
- ❌ 沒有收到 email

**原因：** Firebase Functions 的 email 配置變量未設置。

---

## ✅ 解決方案

### 步驟 1：設置 Firebase Functions 配置

Firebase Functions 使用環境變量來存儲敏感信息（如 Gmail 密碼）。

#### 1.1 創建 Gmail 應用專用密碼

1. **前往 Google 帳戶設置**
   - 打開：https://myaccount.google.com/security
   - 確保已啟用「兩步驗證」

2. **創建應用專用密碼**
   - 前往：https://myaccount.google.com/apppasswords
   - 選擇「應用」：郵件
   - 選擇「設備」：其他（自訂名稱）
   - 輸入名稱：`VaultCaddy Email Verification`
   - 點擊「產生」
   - **複製生成的 16 位密碼**（例如：`abcd efgh ijkl mnop`）

#### 1.2 設置 Firebase Functions 配置

```bash
# 設置 Gmail 用戶名（您的 Gmail 地址）
firebase functions:config:set email.user="your-email@gmail.com"

# 設置 Gmail 應用專用密碼（去掉空格）
firebase functions:config:set email.password="abcdefghijklmnop"

# 示例（使用實際的值）
firebase functions:config:set email.user="vaultcaddy@gmail.com"
firebase functions:config:set email.password="abcd efgh ijkl mnop"
```

#### 1.3 驗證配置

```bash
# 查看當前配置
firebase functions:config:get

# 應該看到：
# {
#   "email": {
#     "user": "your-email@gmail.com",
#     "password": "abcdefghijklmnop"
#   },
#   "stripe": {
#     ...
#   }
# }
```

### 步驟 2：重新部署 Cloud Functions

```bash
# 部署所有 Functions
firebase deploy --only functions

# 或只部署 email 相關的 Functions
firebase deploy --only functions:sendVerificationCode,functions:verifyCode
```

### 步驟 3：測試驗證碼發送

1. **前往註冊頁面**
   - 打開：https://vaultcaddy.com/auth.html
   - 點擊「創建帳戶」

2. **填寫註冊信息**
   - 名字：測試
   - 姓氏：用戶
   - 郵箱：your-test-email@gmail.com
   - 密碼：Test123456

3. **檢查郵箱**
   - 應該收到一封標題為「VaultCaddy - 驗證您的電子郵件」的郵件
   - 郵件包含 6 位驗證碼

4. **輸入驗證碼**
   - 在驗證頁面輸入 6 位驗證碼
   - 點擊「驗證」
   - 應該看到「驗證成功！已贈送 20 個 Credits」

---

## 🔧 替代方案：使用其他 Email 服務

如果不想使用 Gmail，可以使用其他 SMTP 服務：

### 選項 1：SendGrid（推薦）

```javascript
// firebase-functions/index.js
const nodemailer = require('nodemailer');
const sgTransport = require('nodemailer-sendgrid-transport');

const transporter = nodemailer.createTransport(sgTransport({
    auth: {
        api_key: functions.config().sendgrid.api_key
    }
}));
```

```bash
# 設置 SendGrid API 密鑰
firebase functions:config:set sendgrid.api_key="SG.xxxxx"
```

### 選項 2：Mailgun

```javascript
const transporter = nodemailer.createTransport({
    host: 'smtp.mailgun.org',
    port: 587,
    auth: {
        user: functions.config().mailgun.user,
        pass: functions.config().mailgun.password
    }
});
```

```bash
firebase functions:config:set mailgun.user="postmaster@your-domain.mailgun.org"
firebase functions:config:set mailgun.password="your-mailgun-password"
```

### 選項 3：自訂 SMTP

```javascript
const transporter = nodemailer.createTransport({
    host: functions.config().smtp.host,
    port: functions.config().smtp.port,
    secure: true,
    auth: {
        user: functions.config().smtp.user,
        pass: functions.config().smtp.password
    }
});
```

```bash
firebase functions:config:set smtp.host="smtp.example.com"
firebase functions:config:set smtp.port="465"
firebase functions:config:set smtp.user="your-email@example.com"
firebase functions:config:set smtp.password="your-password"
```

---

## 📋 驗證流程

### 完整流程

1. **用戶註冊**
   - 用戶在 `auth.html` 填寫註冊信息
   - 點擊「創建帳戶」
   - Firebase Auth 創建用戶（初始 0 Credits）

2. **發送驗證碼**
   - 調用 `sendVerificationCode` Cloud Function
   - 生成 6 位隨機驗證碼
   - 保存到 Firestore `verificationCodes` 集合
   - 通過 Gmail 發送驗證碼郵件

3. **用戶驗證**
   - 用戶在 `verify-email.html` 輸入驗證碼
   - 調用 `verifyCode` Cloud Function
   - 驗證碼正確後：
     - 標記為已驗證
     - 贈送 20 個 Credits
     - 記錄到 `creditsHistory`

4. **登入使用**
   - 用戶登入後可以使用功能
   - 所有頁面顯示未驗證提示（如果未驗證）

---

## 🐛 常見問題排查

### 問題 1：「發送失敗，請稍後重試」

**可能原因：**
1. ❌ Firebase Functions 配置未設置
2. ❌ Gmail 應用專用密碼錯誤
3. ❌ Gmail 帳戶未啟用「兩步驗證」
4. ❌ Gmail 帳戶被鎖定或限制

**解決方案：**
```bash
# 檢查配置
firebase functions:config:get

# 重新設置配置
firebase functions:config:set email.user="your-email@gmail.com"
firebase functions:config:set email.password="your-app-password"

# 重新部署
firebase deploy --only functions
```

### 問題 2：沒有收到 email

**檢查步驟：**
1. **檢查垃圾郵件文件夾**
2. **檢查 Gmail 發送限制**
   - Gmail 每天限制發送 500 封郵件
   - 前往：https://mail.google.com/mail/u/0/#sent
   - 確認郵件已發送

3. **檢查 Cloud Functions 日誌**
   ```bash
   # 查看 Functions 日誌
   firebase functions:log
   
   # 應該看到：
   # ✅ 驗證碼已發送到 user@example.com
   # 或
   # ❌ 發送驗證碼失敗: [錯誤信息]
   ```

4. **測試 SMTP 連接**
   ```javascript
   // 在本地測試
   transporter.verify(function(error, success) {
       if (error) {
           console.log('❌ SMTP 連接失敗:', error);
       } else {
           console.log('✅ SMTP 連接成功');
       }
   });
   ```

### 問題 3：驗證碼過期

**默認設置：**
- 驗證碼有效期：10 分鐘
- 重發冷卻時間：1 分鐘
- 最大嘗試次數：5 次

**修改設置：**
```javascript
// firebase-functions/index.js
// 修改驗證碼有效期（例如改為 30 分鐘）
expiresAt: admin.firestore.Timestamp.fromDate(
    new Date(Date.now() + 30 * 60 * 1000)
)
```

---

## ✅ 驗證成功後的變化

### 1. 用戶獲得 20 個 Credits
```javascript
// Firestore: users/{userId}
{
    credits: 20,
    currentCredits: 20,
    emailVerified: true,
    emailVerifiedAt: Timestamp
}
```

### 2. Credits 歷史記錄
```javascript
// Firestore: users/{userId}/creditsHistory/{historyId}
{
    type: 'bonus',
    amount: 20,
    reason: 'email_verification',
    description: '完成 Email 驗證獎勵',
    createdAt: Timestamp,
    balanceAfter: 20
}
```

### 3. 未驗證提示消失
- 橙色橫幅消失
- 用戶可以正常使用所有功能

---

## 🎯 快速修復檢查清單

完成以下步驟以修復 email 發送問題：

- [ ] **1. 啟用 Gmail 兩步驗證**
  - 前往：https://myaccount.google.com/security
  - 啟用「兩步驗證」

- [ ] **2. 創建應用專用密碼**
  - 前往：https://myaccount.google.com/apppasswords
  - 創建密碼並複製

- [ ] **3. 設置 Firebase Functions 配置**
  ```bash
  firebase functions:config:set email.user="your-email@gmail.com"
  firebase functions:config:set email.password="your-app-password"
  ```

- [ ] **4. 驗證配置**
  ```bash
  firebase functions:config:get
  ```

- [ ] **5. 重新部署 Functions**
  ```bash
  firebase deploy --only functions
  ```

- [ ] **6. 測試註冊和驗證**
  - 註冊新帳戶
  - 檢查郵箱
  - 輸入驗證碼
  - 確認獲得 20 Credits

---

**現在請按照上述步驟設置 Gmail 配置並重新部署 Functions！** ✅🚀
