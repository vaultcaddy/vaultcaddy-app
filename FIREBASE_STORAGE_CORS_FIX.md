# 🔧 Firebase Storage CORS 修復指南

## 🚨 問題：CORS 錯誤

從圖3的錯誤日誌看到：

```
Access to fetch at 'https://firebasestorage.googleapis.com/v0/b/vaultcaddy-production-cbbe2.fire.le...' 
from origin 'https://vaultcaddy.com' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**原因：** Firebase Storage 默認的 CORS 配置不允許跨域請求。

---

## 📝 解決方案

### 步驟 1：創建 CORS 配置文件

創建文件 `cors.json`（已經為您準備好）：

\`\`\`json
[
  {
    "origin": ["https://vaultcaddy.com", "http://localhost:*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "maxAgeSeconds": 3600,
    "responseHeader": ["Content-Type", "Authorization", "Content-Length", "User-Agent", "X-Goog-Upload-Protocol", "X-Goog-Upload-Command"]
  }
]
\`\`\`

### 步驟 2：使用 gsutil 設置 CORS

#### 2.1 安裝 Google Cloud SDK

**macOS:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**或使用 Homebrew:**
```bash
brew install --cask google-cloud-sdk
```

#### 2.2 初始化 gcloud

```bash
gcloud init
```

選擇您的 Google 帳戶（`vaultcaddy@gmail.com` 或 `osclin2002@gmail.com`）

#### 2.3 設置 CORS

```bash
cd /Users/cavlinyeung/ai-bank-parser
gsutil cors set cors.json gs://vaultcaddy-production-cbbe2.appspot.com
```

**預期輸出：**
```
Setting CORS on gs://vaultcaddy-production-cbbe2.appspot.com/...
```

#### 2.4 驗證 CORS 設置

```bash
gsutil cors get gs://vaultcaddy-production-cbbe2.appspot.com
```

---

## 🔄 替代方案：使用 Firebase Console（更簡單）

如果您不想安裝 Google Cloud SDK，可以使用 Firebase Console：

### 步驟 1：前往 Firebase Console

1. 訪問：https://console.firebase.google.com/
2. 選擇項目：`vaultcaddy-production-cbbe2`
3. 點擊左側菜單「Storage」

### 步驟 2：在 Google Cloud Console 設置 CORS

1. 在 Storage 頁面，點擊「在 Google Cloud Console 中查看」
2. 或直接訪問：https://console.cloud.google.com/storage/browser?project=vaultcaddy-production-cbbe2
3. 點擊您的 bucket：`vaultcaddy-production-cbbe2.appspot.com`
4. 點擊「配置」標籤
5. 找到「CORS 配置」
6. 點擊「編輯」
7. 輸入以下配置：

```json
[
  {
    "origin": ["https://vaultcaddy.com", "http://localhost:*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "responseHeader": ["Content-Type", "Authorization", "Content-Length", "User-Agent"],
    "maxAgeSeconds": 3600
  }
]
```

8. 點擊「保存」

---

## 🧪 測試 CORS 修復

### 測試 1：上傳文件

1. 刷新頁面（Ctrl+F5）
2. 上傳銀行對帳單 PDF
3. 查看控制台，不應再看到 CORS 錯誤

### 測試 2：檢查文件訪問

在控制台輸入：

```javascript
fetch('https://firebasestorage.googleapis.com/v0/b/vaultcaddy-production-cbbe2.appspot.com/o/test.txt')
  .then(r => console.log('✅ CORS 正常:', r))
  .catch(e => console.error('❌ CORS 錯誤:', e))
```

---

## 📋 完整修復清單

### 立即執行

- [ ] **1. 設置 CORS（選擇一種方法）**
  - **方法 A：** 使用 gsutil（需要安裝 Google Cloud SDK）
  - **方法 B：** 使用 Google Cloud Console（推薦，更簡單）

- [ ] **2. 驗證 CORS 設置**
  ```bash
  gsutil cors get gs://vaultcaddy-production-cbbe2.appspot.com
  ```

- [ ] **3. 測試銀行對帳單上傳**
  - 刷新頁面
  - 上傳 PDF
  - 查看控制台無 CORS 錯誤

---

## 🎯 預期結果

### 成功的文件上傳（無 CORS 錯誤）

**控制台日誌：**
```
✅ 文件已上傳 Storage: eStatementFile_20250829143359.pdf
🤖 開始 AI 處理...
📊 Vision API 回應: { hasError: false, hasFullText: true, textLength: 2345 }
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

## 💡 如果問題仍未解決

### Vision API 問題

如果 CORS 修復後，Vision API 仍然失敗：

1. **檢查 API 配額**
   - 前往 [Google Cloud Console](https://console.cloud.google.com/)
   - 導航到「API 和服務」→「配額」
   - 搜索「Vision API」

2. **檢查 API 密鑰**
   - 確認 `hybrid-vision-deepseek-optimized.js` 中的 API 密鑰正確

3. **嘗試單頁 PDF**
   - 當前 PDF 是 3 頁，可能需要分頁處理
   - 嘗試上傳單頁 PDF 測試

---

## 📞 下一步

**請執行以下步驟並告訴我結果：**

1. **設置 CORS**（使用方法 A 或 B）
2. **測試銀行對帳單上傳**
3. **告訴我：**
   - CORS 錯誤是否消失？
   - Vision API 是否成功提取文本？
   - 還有其他錯誤嗎？

我會根據您的反饋提供進一步的解決方案！🚀

