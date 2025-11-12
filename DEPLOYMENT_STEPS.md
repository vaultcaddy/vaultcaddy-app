# 立即部署步驟

## ✅ 所有代碼已準備就緒

### 已完成的修改：
1. ✅ Firestore 規則（`firestore.rules`）
2. ✅ 文檔類型繁體中文化
3. ✅ 拖放上傳功能
4. ✅ 驗證邏輯（0 → 驗證 → 20 Credits）
5. ✅ 移除驗證阻擋，改為獎勵提示
6. ✅ 所有頁面顯示驗證提示

---

## 📋 需要執行的 3 個命令

### 步驟 1：部署 Firestore 規則
```bash
firebase deploy --only firestore:rules
```

**預期輸出：**
```
✔  Deploy complete!
```

---

### 步驟 2：設置 Email 配置

#### 2.1 創建 Gmail 應用專用密碼
1. 前往：https://myaccount.google.com/security
2. 啟用「兩步驗證」
3. 前往：https://myaccount.google.com/apppasswords
4. 創建應用專用密碼
5. 複製 16 位密碼

#### 2.2 設置 Firebase Functions 配置
```bash
# 設置 Gmail 用戶名（替換為您的實際值）
firebase functions:config:set email.user="your-email@gmail.com"

# 設置應用專用密碼（去掉空格）
firebase functions:config:set email.password="abcdefghijklmnop"
```

**驗證配置：**
```bash
firebase functions:config:get
```

---

### 步驟 3：部署 Cloud Functions
```bash
firebase deploy --only functions
```

**預期輸出：**
```
✔  functions: Finished running predeploy script.
✔  functions[sendVerificationCode]: Successful update operation.
✔  functions[verifyCode]: Successful update operation.
✔  Deploy complete!
```

---

## 🧪 測試步驟

### 1. 測試拖放上傳
- 前往：https://vaultcaddy.com/firstproject.html
- 拖放 PDF 文件
- 選擇「銀行對帳單」
- 確認上傳成功

### 2. 測試驗證流程
- 前往：https://vaultcaddy.com/auth.html
- 註冊新帳戶
- 確認初始 0 Credits
- 檢查郵箱收到驗證碼
- 輸入驗證碼
- 確認獲得 20 Credits

### 3. 測試驗證提示
- 前往：https://vaultcaddy.com/dashboard.html
- 確認顯示「立即驗證您的 email 即送 20 Credits 試用！」
- 確認可以正常使用功能（不被阻擋）

---

## 🔧 如果沒有 Firebase CLI

### 安裝 Firebase CLI
```bash
npm install -g firebase-tools
```

### 登入 Firebase
```bash
firebase login
```

### 選擇項目
```bash
firebase use vaultcaddy-production-cbbe2
```

---

## 📞 需要幫助？

如果遇到問題，請查看：
- `EMAIL_CONFIGURATION_GUIDE.md` - Email 配置詳細指南
- `FIRESTORE_RULES_DEPLOYMENT.md` - Firestore 規則部署指南
- `TROUBLESHOOTING_GUIDE.md` - 問題排查指南

---

**準備好了嗎？讓我們開始部署！** 🚀
