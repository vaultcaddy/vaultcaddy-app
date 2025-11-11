# Email 驗證功能實施指南

## 已完成的工作

### 1. Firebase Cloud Functions
✅ 已添加 3 個 Cloud Functions：
- `sendVerificationCode` - 發送驗證碼到用戶 email
- `verifyCode` - 驗證用戶輸入的驗證碼
- `checkEmailVerified` - 檢查 email 是否已驗證

✅ 已添加 nodemailer 依賴到 package.json

### 2. 驗證碼功能特點
- 6 位數隨機驗證碼
- 10 分鐘過期時間
- 最多 5 次驗證嘗試
- 防止重複使用
- 精美的 HTML email 模板

### 3. Email 模板內容
- 歡迎訊息
- 驗證碼顯示
- VaultCaddy 功能介紹
- 立即驗證按鈕
- 專業的設計

## 待完成的工作

### 1. 創建驗證頁面
需要創建 `verify-email.html` 頁面：
- 輸入驗證碼的表單
- 倒計時顯示（10 分鐘）
- 重新發送驗證碼按鈕
- 驗證成功後跳轉

### 2. 修改註冊流程
需要修改 `register.html`：
- 註冊成功後不直接登入
- 調用 `sendVerificationCode` Cloud Function
- 跳轉到驗證頁面

### 3. 添加驗證檢查
需要在主要功能頁面添加檢查：
- `firstproject.html` - 上傳文件前檢查
- `account.html` - 進入頁面時檢查
- 未驗證用戶顯示提示訊息

### 4. 配置 Firebase
需要設置 Firebase Config：
```bash
firebase functions:config:set email.user="your-email@gmail.com"
firebase functions:config:set email.password="your-app-password"
```

### 5. 部署 Cloud Functions
```bash
cd firebase-functions
npm install
firebase deploy --only functions
```

## 使用流程

### 用戶註冊流程：
1. 用戶在 `register.html` 填寫資料
2. 點擊註冊按鈕
3. Firebase Auth 創建用戶
4. 調用 `sendVerificationCode` 發送驗證碼
5. 跳轉到 `verify-email.html`
6. 用戶輸入驗證碼
7. 調用 `verifyCode` 驗證
8. 驗證成功後跳轉到 dashboard

### 驗證檢查流程：
1. 用戶嘗試使用功能
2. 檢查 email 是否已驗證
3. 未驗證：顯示提示，跳轉到驗證頁面
4. 已驗證：正常使用功能

## 安全考慮

- ✅ 驗證碼 10 分鐘過期
- ✅ 最多 5 次驗證嘗試
- ✅ 防止驗證碼重複使用
- ✅ 使用 Firebase Auth 保護 API
- ✅ Email 使用 Gmail App Password

## 下一步

1. 創建 `verify-email.html` 頁面
2. 修改 `register.html` 註冊流程
3. 添加驗證檢查到主要頁面
4. 配置 Firebase email 設置
5. 部署和測試

## 注意事項

### Gmail App Password 設置：
1. 登入 Google 帳戶
2. 前往「安全性」設置
3. 啟用「兩步驟驗證」
4. 生成「應用程式密碼」
5. 使用該密碼配置 Firebase

### 測試建議：
1. 先在本地測試 Cloud Functions
2. 使用 Firebase Emulator
3. 測試各種錯誤情況
4. 確認 email 正確發送
5. 測試驗證碼過期和重試

## 預期效果

- ✅ 提升帳戶安全性
- ✅ 防止垃圾註冊
- ✅ 確保 email 有效性
- ✅ 專業的用戶體驗
- ✅ 符合行業標準
