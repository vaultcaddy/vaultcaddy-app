# 🔧 完整修復指南

## 📊 問題診斷總結

### 問題 1：Logo 未顯示 ✅
**狀態：** Logo 代碼已存在（`navbar-component.js` 第139-160行）

**可能原因：** CSS 被覆蓋或瀏覽器緩存

**解決方案：** 刷新頁面（Ctrl+F5 或 Cmd+Shift+R）

---

### 問題 2：銀行對帳單處理失敗 ❌
**狀態：** 已修復代碼，需要測試

**錯誤信息：**
```
❌ 第合處理失敗: Error: Vision API 未能提取文本
```

**已完成的修復：**
1. ✅ 統一使用 `DOCUMENT_TEXT_DETECTION`（更適合文檔）
2. ✅ 增加詳細錯誤日誌
3. ✅ 增加 Vision API 回應調試信息

**可能的原因：**
1. **PDF 是多頁文檔（3頁）** - Vision API 一次只能處理一頁
2. **Vision API 配額問題** - 免費配額：1000 次/月
3. **PDF 格式問題** - 掃描件質量不佳

**測試步驟：**
1. 刷新頁面（清除緩存）
2. 重新上傳銀行對帳單
3. 查看控制台的新日誌：
   ```
   📊 Vision API 回應: { hasError: false, hasFullText: true, textLength: 1234 }
   ```
4. 如果仍然失敗，查看詳細錯誤信息

---

### 問題 3：Email 驗證失敗 ❌
**狀態：** 發現問題 - `verifyCode` 函數未部署

**錯誤信息：**
```
發送失敗，請稍後重試
```

**診斷結果：**
- ✅ Email 配置已設置（`vaultcaddy@gmail.com`）
- ✅ `sendVerificationCode` 函數已部署
- ❌ **`verifyCode` 函數未部署**（這是問題所在！）

**解決方案：**

#### 步驟 1：重新部署 `verifyCode` 函數

```bash
cd /Users/cavlinyeung/ai-bank-parser
firebase deploy --only functions:verifyCode
```

#### 步驟 2：驗證部署成功

```bash
firebase functions:list | grep verifyCode
```

應該看到：
```
verifyCode  │ v1  │ callable  │ us-central1  │ 256  │ nodejs20
```

#### 步驟 3：測試 Email 驗證

1. 刷新頁面
2. 註冊新用戶
3. 輸入驗證碼
4. 查看控制台是否有錯誤

---

## 🚀 立即執行的命令

### 命令 1：重新部署 verifyCode 函數（必須）

```bash
cd /Users/cavlinyeung/ai-bank-parser
firebase deploy --only functions:verifyCode
```

**預期輸出：**
```
✔  functions[verifyCode(us-central1)] Successful update operation.
✔  Deploy complete!
```

### 命令 2：驗證部署（可選）

```bash
firebase functions:list | grep -E "(sendVerificationCode|verifyCode|checkEmailVerified)"
```

**預期輸出：**
```
sendVerificationCode  │ v1  │ callable  │ us-central1  │ 256  │ nodejs20
verifyCode            │ v1  │ callable  │ us-central1  │ 256  │ nodejs20
checkEmailVerified    │ v1  │ callable  │ us-central1  │ 256  │ nodejs20
```

### 命令 3：查看 Functions 日誌（如果仍失敗）

```bash
firebase functions:log --only sendVerificationCode,verifyCode
```

---

## 🧪 測試計劃

### 測試 1：銀行對帳單上傳

1. **刷新頁面**（Ctrl+F5 或 Cmd+Shift+R）
2. **上傳銀行對帳單 PDF**
3. **查看控制台日誌**：
   ```
   📊 Vision API 回應: { hasError: false, hasFullText: true, textLength: 1234 }
   🧠 DeepSeek 分析中...
   ✅ 處理完成
   ```
4. **如果失敗，查看詳細錯誤**：
   ```
   ❌ Vision API 詳細錯誤: {...}
   ```

### 測試 2：Email 驗證

1. **執行命令 1**（部署 `verifyCode`）
2. **刷新頁面**
3. **註冊新用戶**（使用新 email）
4. **檢查 email 是否收到驗證碼**
5. **輸入驗證碼並提交**
6. **查看控制台日誌**：
   ```
   ✅ 驗證成功
   ✅ 已發放 20 Credits
   ```

---

## 📋 完整檢查清單

### 立即執行（必須）
- [ ] **1. 部署 `verifyCode` 函數**
  ```bash
  firebase deploy --only functions:verifyCode
  ```

### 測試（必須）
- [ ] **2. 測試銀行對帳單上傳**
  - 刷新頁面
  - 上傳 PDF
  - 查看控制台日誌

- [ ] **3. 測試 Email 驗證**
  - 註冊新用戶
  - 檢查 email
  - 輸入驗證碼
  - 確認 20 Credits 發放

### 如果仍失敗（可選）
- [ ] **4. 查看 Functions 日誌**
  ```bash
  firebase functions:log
  ```

- [ ] **5. 檢查 Vision API 配額**
  - 前往 [Google Cloud Console](https://console.cloud.google.com/)
  - 檢查 Vision API 配額使用情況

- [ ] **6. 檢查 Gmail App Password**
  - 前往 https://myaccount.google.com/apppasswords
  - 使用 `vaultcaddy@gmail.com` 登入
  - 確認 App Password 正確

---

## 💡 預期結果

### 成功的銀行對帳單處理

**控制台日誌：**
```
🤖 開始 AI 處理: eStatementFile_20250829143359.pdf (3 頁)
📸 步驟 1：Vision API OCR...
📊 Vision API 回應: { hasError: false, hasFullText: true, textLength: 2345 }
✅ OCR 完成，提取了 2345 字符
🧠 步驟 2：DeepSeek 分析...
✅ 處理完成
```

**UI 顯示：**
```
文檔名稱: eStatementFile_20250829143359.pdf
類型: 銀行對帳單
供應商/來源/銀行: 恆生銀行
金額: $30,188.66
日期: 02/01/2025 to 03/22/2025
狀態: 已完成 ✅
```

---

### 成功的 Email 驗證

**控制台日誌：**
```
📧 發送驗證碼到: user@example.com
✅ 驗證碼已發送
✅ 驗證成功
✅ 已發放 20 Credits
```

**UI 顯示：**
```
✅ 驗證成功！
您已獲得 20 Credits
```

---

## 🆘 如果問題仍未解決

### Vision API 問題

1. **檢查 API 配額**
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 導航到「API 和服務」→「配額」
   - 搜索「Vision API」
   - 確認配額未用完

2. **嘗試不同的 PDF**
   - 使用單頁 PDF 測試
   - 使用較小的 PDF（< 5MB）
   - 確保 PDF 不是掃描件

3. **查看詳細錯誤**
   - 控制台會顯示完整的 Vision API 錯誤
   - 複製錯誤信息並告訴我

### Email 驗證問題

1. **檢查 Functions 日誌**
   ```bash
   firebase functions:log --only sendVerificationCode,verifyCode
   ```

2. **檢查 Gmail 設置**
   - 確認 2-Step Verification 已啟用
   - 確認 App Password 正確
   - 嘗試重新生成 App Password

3. **檢查 Firestore 規則**
   - 確認 `verificationCodes` 集合可寫入
   - 檢查 `firestore.rules`

---

## 📞 下一步

**請執行以下步驟並告訴我結果：**

1. **執行命令 1**（部署 `verifyCode`）
2. **測試銀行對帳單上傳**
3. **測試 Email 驗證**
4. **告訴我：**
   - 哪個測試成功了？
   - 哪個測試失敗了？
   - 控制台顯示什麼錯誤？

我會根據您的反饋提供進一步的解決方案！🚀

