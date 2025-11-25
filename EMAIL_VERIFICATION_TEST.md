# Email 驗證功能測試指南

## ✅ 修復完成

**問題：** Gmail 應用程式密碼已失效  
**解決方案：** 已更新為新的應用程式密碼並重新部署 Firebase Functions

---

## 🧪 測試步驟

### 1. 測試註冊流程

1. 訪問：https://vaultcaddy.com/auth.html
2. 點擊「註冊」標籤
3. 填寫信息：
   - Email：使用你的測試郵箱
   - 密碼：至少 6 位
   - 顯示名稱：任意名稱
4. 點擊「註冊」按鈕

**預期結果：**
- ✅ 應該跳轉到 `verify-email.html?email=你的郵箱`
- ✅ 頁面顯示「驗證您的電子郵件」
- ✅ 顯示你的郵箱地址

### 2. 檢查郵件

1. 打開你的郵箱（可能需要等待 1-2 分鐘）
2. 查找來自 `VaultCaddy <vaultcaddy@gmail.com>` 的郵件
3. 主題：「歡迎註冊 VaultCaddy - 驗證您的電子郵件」

**如果沒有收到郵件：**
- 檢查垃圾郵件資料夾
- 檢查「促銷」或「社交」標籤（Gmail）
- 等待最多 5 分鐘

### 3. 輸入驗證碼

1. 從郵件中複製 6 位數驗證碼
2. 在 `verify-email.html` 頁面輸入驗證碼
3. 驗證碼會自動驗證（輸入最後一位時）

**預期結果：**
- ✅ 顯示「驗證成功！正在跳轉...」
- ✅ 自動跳轉到 `index.html`
- ✅ 用戶獲得 20 個免費 Credits

### 4. 測試重新發送驗證碼

1. 在 `verify-email.html` 頁面
2. 點擊「重新發送驗證碼」按鈕

**預期結果：**
- ✅ 按鈕顯示「發送中...」
- ✅ 顯示「驗證碼已重新發送到您的郵箱」
- ✅ 按鈕變為「60 秒後可重新發送」並開始倒計時
- ✅ 收到新的驗證碼郵件

---

## 🔍 檢查 Firebase Functions 日誌

如果遇到問題，可以檢查日誌：

```bash
# 檢查 sendVerificationCode 日誌
firebase functions:log --only sendVerificationCode

# 檢查 verifyCode 日誌
firebase functions:log --only verifyCode
```

**成功的日誌應該包含：**
- ✅ `📧 準備發送驗證碼到: [email]`
- ✅ `✅ 驗證碼已成功發送到 [email]`
- ✅ `✅ Email 驗證成功: [email]`
- ✅ `🎁 已贈送 20 Credits 給用戶: [email]`

**失敗的日誌會包含：**
- ❌ `❌ 發送驗證碼失敗: Error: Invalid login` （這個問題已修復）

---

## 📧 Email 配置信息

- **Email 地址：** vaultcaddy@gmail.com
- **應用程式名稱：** vaultcaddy
- **應用程式密碼：** ighfhhanoamudyiv
- **配置狀態：** ✅ 已更新並部署

---

## 🎁 驗證成功獎勵

用戶完成 email 驗證後會自動獲得：
- **20 個免費 Credits**
- 可處理 20 頁文檔
- Credits 會記錄在 Firestore 的 `users/{userId}/creditsHistory` 集合中

---

## 🐛 常見問題

### 問題 1：沒有收到驗證碼郵件

**可能原因：**
1. Gmail 應用程式密碼失效（已修復）
2. 郵件被標記為垃圾郵件
3. Firebase Functions 未正確部署

**解決方案：**
- 檢查垃圾郵件資料夾
- 檢查 Firebase Functions 日誌
- 確認 Functions 已部署：`firebase functions:list`

### 問題 2：驗證碼錯誤

**可能原因：**
1. 驗證碼已過期（10 分鐘）
2. 輸入錯誤
3. 驗證碼已被使用

**解決方案：**
- 點擊「重新發送驗證碼」
- 確保在 10 分鐘內輸入
- 仔細檢查每一位數字

### 問題 3：重新發送驗證碼失敗

**可能原因：**
1. 網絡問題
2. Firebase Functions 錯誤
3. Email 配置問題

**解決方案：**
- 檢查網絡連接
- 查看瀏覽器控制台錯誤
- 檢查 Firebase Functions 日誌

---

## 📝 測試清單

- [ ] 註冊新用戶
- [ ] 收到驗證碼郵件
- [ ] 輸入正確的驗證碼
- [ ] 驗證成功並跳轉
- [ ] 用戶獲得 20 Credits
- [ ] 測試重新發送驗證碼
- [ ] 測試錯誤驗證碼（應顯示錯誤）
- [ ] 測試過期驗證碼（等待 10 分鐘）

---

## 🎉 完成！

如果所有測試都通過，email 驗證功能已完全修復並正常工作！

**下一步建議：**
1. 測試完整的註冊流程
2. 確認 Credits 正確添加到用戶帳戶
3. 測試登入功能
4. 測試文檔上傳和處理功能

