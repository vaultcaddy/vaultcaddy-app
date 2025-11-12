# 🚀 立即修復指南

## ✅ 已完成的修復

### 1. Firebase 配置錯誤修復
- **問題：** `Not in a Firebase app directory (could not locate firebase.json)`
- **修復：** ✅ 創建 `firebase.json` 和 `firestore.indexes.json`
- **狀態：** 已完成

### 2. 簡化帳戶管理
- **問題：** 需要兩個 Gmail 帳戶（`vaultcaddy@gmail.com` 和 `osclin2002@gmail.com`）
- **修復：** ✅ 改為只使用一個帳戶：`vaultcaddy@gmail.com`
- **狀態：** 已完成

---

## 📋 下一步操作（3 個步驟，預計 5 分鐘）

### 步驟 1：創建應用專用密碼（2 分鐘）

1. **打開應用專用密碼頁面**
   ```
   https://myaccount.google.com/apppasswords
   ```
   （已為您在瀏覽器中打開）

2. **登入 vaultcaddy@gmail.com**
   - 確認您已使用 `vaultcaddy@gmail.com` 登入

3. **創建應用專用密碼**
   - 點擊「選取應用程式」→ 選擇「郵件」
   - 點擊「選取裝置」→ 選擇「其他」
   - 輸入名稱：`VaultCaddy Functions`
   - 點擊「產生」

4. **複製密碼**
   - Google 會顯示一個 16 位密碼（例如：`abcd efgh ijkl mnop`）
   - **複製這個密碼**（去掉空格）
   - 保存到安全的地方

---

### 步驟 2：執行配置腳本（2 分鐘）

在終端機執行：

```bash
cd /Users/cavlinyeung/ai-bank-parser
./configure-firebase.sh
```

**腳本會要求輸入密碼時：**
- 貼上您剛才複製的應用專用密碼（去掉空格）
- 例如：`abcdefghijklmnop`

**腳本會自動執行：**
1. ✅ 部署 Firestore 規則
2. ✅ 設置 Email 配置（使用 `vaultcaddy@gmail.com`）
3. ✅ 部署 Cloud Functions

---

### 步驟 3：測試功能（1 分鐘）

**測試 1：Dashboard 項目創建**
1. 前往：https://vaultcaddy.com/dashboard.html
2. 嘗試創建新項目
3. **預期結果：** 項目創建成功，不再出現 "permission-denied" 錯誤

**測試 2：Email 驗證**
1. 前往：https://vaultcaddy.com/auth.html
2. 註冊新帳戶（例如：`test@example.com`）
3. **預期結果：** 收到驗證碼郵件（發件人：`vaultcaddy@gmail.com`）
4. 輸入驗證碼
5. **預期結果：** 驗證成功，獲得 20 個 Credits

---

## 📁 已創建/更新的文件

### 新增文件：
1. ✅ `firebase.json` - Firebase 項目配置
2. ✅ `firestore.indexes.json` - Firestore 索引配置

### 更新文件：
1. ✅ `configure-firebase.sh` - 改用 `vaultcaddy@gmail.com`
2. ✅ `firestore.rules` - Firestore 安全規則

---

## 🔑 關於「單一帳戶」設計

### 為什麼只需要 `vaultcaddy@gmail.com`？

**1. Firebase 管理**
- 登入 Firebase CLI
- 部署規則和 Functions
- 管理項目設置

**2. 發送郵件**
- 發送驗證碼
- 發送系統通知
- SMTP 發件人

### 優點：
- ✅ 管理簡單（只需一個應用專用密碼）
- ✅ 安全性高（使用 Firebase 項目擁有者帳戶）
- ✅ 統一品牌（所有郵件來自 vaultcaddy@gmail.com）

---

## ⚠️ 常見問題

### Q1: 為什麼需要應用專用密碼？
**A:** 因為 Gmail 開啟了「兩步驟驗證」，不能直接使用原始密碼。應用專用密碼是專為應用程式設計的安全密碼。

### Q2: 應用專用密碼會顯示給用戶嗎？
**A:** 不會。密碼只存儲在 Firebase Functions 配置中，不會顯示在前端，完全安全。

### Q3: 如果密碼洩漏怎麼辦？
**A:** 可以隨時在 Google 帳戶設置中撤銷該應用專用密碼，並生成新的密碼。

### Q4: 配置腳本執行失敗怎麼辦？
**A:** 查看終端錯誤訊息：
- 如果是 "permission-denied"：確認已用 `vaultcaddy@gmail.com` 登入 Firebase CLI
- 如果是 "invalid password"：重新創建應用專用密碼
- 如果是 "network error"：檢查網路連接

---

## 📞 需要幫助？

如果遇到任何問題，請提供：
1. 終端的完整錯誤訊息
2. 執行到哪個步驟失敗
3. Firebase Console 的截圖（如果有錯誤）

---

## 🎯 預期完成時間

- **步驟 1：** 創建應用專用密碼 - 2 分鐘
- **步驟 2：** 執行配置腳本 - 2 分鐘
- **步驟 3：** 測試功能 - 1 分鐘

**總計：約 5 分鐘** ⚡

---

## ✅ 完成後的狀態

所有功能將正常運行：
- ✅ Dashboard 項目創建
- ✅ Email 驗證系統
- ✅ Credits 管理
- ✅ 文檔處理
- ✅ 拖放上傳
- ✅ 繁體中文界面

---

**準備好開始了嗎？請先為 vaultcaddy@gmail.com 創建應用專用密碼！** 🔑
