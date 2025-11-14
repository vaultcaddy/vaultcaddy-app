# 🚨 緊急修復指南

## 問題 1：Logo 未顯示 ✅

**原因：** Logo 代碼已存在，但可能被 CSS 隱藏或覆蓋

**解決方案：** 檢查 `navbar-component.js` 第139-160行，Logo 已經存在

---

## 問題 2：銀行對帳單處理失敗 ❌

### 錯誤分析（從圖1）：

```
❌ 第合處理失敗: Error: Vision API 未能提取文本
at HybridVisionDeepSeekProcessor.extractTextWithVision
```

### 可能原因：

1. **PDF 是多頁文檔（3頁）**
   - Vision API 一次只能處理一頁
   - 需要分頁處理

2. **Vision API 配額問題**
   - 免費配額：1000 次/月
   - 可能已用完

3. **PDF 格式問題**
   - 銀行對帳單可能是掃描件
   - 圖片質量不佳

### 解決方案：

#### 方案 A：使用 DOCUMENT_TEXT_DETECTION（推薦）

`hybrid-vision-deepseek.js` 已使用 `DOCUMENT_TEXT_DETECTION`（第93行），但 `hybrid-vision-deepseek-optimized.js` 使用的是 `TEXT_DETECTION`（第220行）。

**修復：** 統一使用 `DOCUMENT_TEXT_DETECTION`

#### 方案 B：處理多頁 PDF

當前代碼只處理第一頁。需要：
1. 將 PDF 分割成多頁
2. 對每頁進行 OCR
3. 合併所有頁面的文本

---

## 問題 3：Email 驗證失敗 ❌

### 錯誤分析（從圖2-3）：

```
發送失敗，請稍後重試
```

### 可能原因：

1. **Nodemailer 配置錯誤**
   - Gmail App Password 未設置
   - Email 配置未部署到 Cloud Functions

2. **Cloud Functions 未部署**
   - `sendVerificationCode` 函數未部署
   - 或部署失敗

3. **Firebase Functions Config 未設置**
   ```bash
   firebase functions:config:get
   ```
   應該看到：
   ```json
   {
     "email": {
       "user": "vaultcaddy@gmail.com",
       "password": "your-app-password"
     }
   }
   ```

### 解決方案：

#### 步驟 1：檢查 Cloud Functions 部署狀態

```bash
firebase functions:list
```

應該看到：
- ✅ sendVerificationCode
- ✅ verifyCode
- ✅ checkEmailVerified

#### 步驟 2：檢查 Email 配置

```bash
firebase functions:config:get
```

如果沒有 `email` 配置，執行：
```bash
firebase functions:config:set email.user="vaultcaddy@gmail.com" email.password="your-app-password"
firebase deploy --only functions
```

#### 步驟 3：檢查 Gmail App Password

1. 前往 https://myaccount.google.com/apppasswords
2. 使用 `vaultcaddy@gmail.com` 登入
3. 創建新的 App Password
4. 複製密碼並設置到 Firebase

---

## 🔧 立即執行的修復

### 修復 1：統一 Vision API 使用 DOCUMENT_TEXT_DETECTION

修改 `hybrid-vision-deepseek-optimized.js` 第220行：

```javascript
// 修改前
features: [{ type: 'TEXT_DETECTION', maxResults: 1 }]

// 修改後
features: [{ type: 'DOCUMENT_TEXT_DETECTION', maxResults: 1 }]
```

### 修復 2：增加錯誤詳情日誌

修改 `hybrid-vision-deepseek-optimized.js` 第236-238行：

```javascript
// 修改前
if (data.responses[0].error) {
    throw new Error(`Vision API 錯誤: ${data.responses[0].error.message}`);
}

// 修改後
if (data.responses[0].error) {
    console.error('❌ Vision API 詳細錯誤:', data.responses[0].error);
    throw new Error(`Vision API 錯誤: ${JSON.stringify(data.responses[0].error)}`);
}
```

### 修復 3：檢查 Email 配置

執行以下命令：

```bash
cd /Users/cavlinyeung/ai-bank-parser
firebase functions:config:get
```

如果沒有 `email` 配置，執行：

```bash
firebase functions:config:set email.user="vaultcaddy@gmail.com" email.password="YOUR_GMAIL_APP_PASSWORD"
firebase deploy --only functions:sendVerificationCode,functions:verifyCode
```

---

## 🎯 測試計劃

### 測試 1：Vision API

1. 上傳單頁 PDF（不是多頁）
2. 查看控制台錯誤
3. 如果成功，再測試多頁 PDF

### 測試 2：Email 驗證

1. 註冊新用戶
2. 查看控制台錯誤
3. 檢查 Firebase Functions 日誌：
   ```bash
   firebase functions:log
   ```

---

## 📋 檢查清單

- [ ] 修改 `hybrid-vision-deepseek-optimized.js` 使用 `DOCUMENT_TEXT_DETECTION`
- [ ] 增加 Vision API 錯誤詳情日誌
- [ ] 檢查 Firebase Functions Config（email.user, email.password）
- [ ] 重新部署 Cloud Functions
- [ ] 測試單頁 PDF 上傳
- [ ] 測試 Email 驗證
- [ ] 查看 Firebase Functions 日誌

---

## 💡 下一步

完成以上修復後，如果問題仍未解決：

1. **Vision API 問題：**
   - 檢查 API 配額
   - 嘗試使用不同的 PDF
   - 考慮使用 PDF.js 先將 PDF 轉換為圖片

2. **Email 問題：**
   - 檢查 Gmail 帳戶是否啟用 2-Step Verification
   - 檢查 App Password 是否正確
   - 查看 Firebase Functions 日誌獲取詳細錯誤

請告訴我執行結果！

