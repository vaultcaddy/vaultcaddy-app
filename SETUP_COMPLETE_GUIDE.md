# 完整設置指南

## ✅ 已完成的步驟

1. ✅ **創建 Gmail 應用專用密碼**
   - Gmail: `osclin2002@gmail.com`
   - 應用專用密碼: `vjsl pwfv qaow yyza`（去掉空格：`vjslpwfvqaowyy za`）

2. ✅ **Firestore 規則已更新**
   - 規則內容正確
   - 待發布到 Firebase

---

## 🚀 方法 1：使用自動化腳本（推薦）

### 步驟 1：安裝 Firebase CLI

```bash
# 使用 npm 安裝 Firebase CLI
npm install -g firebase-tools

# 驗證安裝
firebase --version
```

### 步驟 2：登入 Firebase

```bash
firebase login
```

### 步驟 3：選擇項目

```bash
firebase use vaultcaddy-production-cbbe2
```

### 步驟 4：執行自動化腳本

```bash
cd /Users/cavlinyeung/ai-bank-parser
./configure-firebase.sh
```

這個腳本會自動完成：
- ✅ 部署 Firestore 規則
- ✅ 設置 Email 配置
- ✅ 部署 Cloud Functions

---

## 🔧 方法 2：手動執行命令

如果您已經安裝並登入 Firebase CLI：

```bash
# 1. 部署 Firestore 規則
firebase deploy --only firestore:rules

# 2. 設置 Email 配置
firebase functions:config:set email.user="osclin2002@gmail.com"
firebase functions:config:set email.password="vjslpwfvqaowyy za"

# 3. 驗證配置
firebase functions:config:get

# 4. 部署 Cloud Functions
firebase deploy --only functions
```

---

## 🖱️ 方法 3：使用 Firebase Console（手動）

### A. 部署 Firestore 規則

1. 打開：https://console.firebase.google.com/project/vaultcaddy-production-cbbe2/firestore/rules
2. 檢查規則內容是否正確（應該已經正確）
3. **點擊右上角的「發布」或「Publish」按鈕**
4. 等待幾秒讓規則生效

### B. 設置 Email 配置（需要 Firebase CLI）

⚠️ **注意：** Firebase Functions 配置只能通過 CLI 設置，無法通過 Console UI 設置。

**必須使用命令：**
```bash
firebase functions:config:set email.user="osclin2002@gmail.com"
firebase functions:config:set email.password="vjslpwfvqaowyy za"
```

### C. 部署 Cloud Functions

**選項 1：使用 CLI**
```bash
firebase deploy --only functions
```

**選項 2：重新上傳代碼**
- 如果沒有 CLI，需要通過 Firebase Console 重新上傳整個 `firebase-functions` 目錄

---

## 📋 快速安裝 Firebase CLI

```bash
# 安裝 Firebase CLI（使用 npm）
npm install -g firebase-tools

# 登入 Firebase
firebase login

# 選擇項目
firebase use vaultcaddy-production-cbbe2

# 執行自動化腳本
cd /Users/cavlinyeung/ai-bank-parser
./configure-firebase.sh
```

**估計時間：** 5-10 分鐘

---

## 🧪 測試步驟

### 測試 1：Dashboard 創建項目

1. 前往：https://vaultcaddy.com/dashboard.html
2. 點擊「Create」按鈕
3. 輸入項目名稱
4. 點擊「Create」
5. **預期結果：** 項目創建成功，不再出現權限錯誤

### 測試 2：驗證碼發送

1. 前往：https://vaultcaddy.com/auth.html
2. 點擊「創建帳戶」
3. 填寫註冊信息（使用測試郵箱）
4. 點擊「創建帳戶」
5. **預期結果：** 
   - 看到「驗證碼已發送到您的郵箱」
   - 收到郵件（標題：VaultCaddy - 驗證您的電子郵件）
   - 郵件包含 6 位驗證碼

### 測試 3：驗證獎勵

1. 在驗證頁面輸入驗證碼
2. 點擊「驗證」
3. **預期結果：**
   - 看到「驗證成功！已贈送 20 個 Credits」
   - 登入後查看 Credits：應該是 20

---

## ❓ 常見問題

### Q1：我沒有安裝 Firebase CLI，可以不用嗎？

**答：** Email 配置**必須**使用 Firebase CLI 設置，無法通過 Console UI 操作。

**建議：** 安裝 Firebase CLI，這是一次性的設置。

### Q2：安裝 Firebase CLI 需要多久？

**答：** 通常 1-2 分鐘。

```bash
npm install -g firebase-tools
```

### Q3：我可以在其他電腦上執行嗎？

**答：** 可以！只要那台電腦：
- 安裝了 Node.js 和 npm
- 可以訪問 Firebase 項目
- 有網絡連接

### Q4：如果腳本執行失敗怎麼辦？

**答：** 
1. 檢查錯誤信息
2. 確認已登入 Firebase：`firebase login`
3. 確認已選擇項目：`firebase use vaultcaddy-production-cbbe2`
4. 手動執行每個命令並查看錯誤

---

## 🎯 推薦執行順序

### 最快路徑（5-10 分鐘）：

```bash
# 1. 安裝 Firebase CLI
npm install -g firebase-tools

# 2. 登入
firebase login

# 3. 選擇項目
firebase use vaultcaddy-production-cbbe2

# 4. 執行自動化腳本
cd /Users/cavlinyeung/ai-bank-parser
./configure-firebase.sh

# 5. 測試
# 前往 dashboard.html 和 auth.html 測試
```

---

## 📞 需要幫助？

如果遇到問題：

1. **查看錯誤日誌**
   ```bash
   firebase functions:log
   ```

2. **驗證配置**
   ```bash
   firebase functions:config:get
   ```

3. **檢查部署狀態**
   ```bash
   firebase deploy:history
   ```

---

**準備好了嗎？讓我們開始吧！** 🚀

**建議：執行 `npm install -g firebase-tools` 並運行自動化腳本。**
