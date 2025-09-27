# 🔑 在 Google Cloud Console 中獲取 Google AI API Key

## 當前狀態
您已經在 VaultCaddy Production 專案中。現在需要獲取 Google AI API Key。

## 步驟 1: 啟用 Generative AI API

### 1.1 進入 API 庫
從當前頁面操作：
1. 點擊左上角的「☰」選單
2. 選擇「API 和服務」
3. 點擊「程式庫」

**或直接點擊這個連結**：
[API 程式庫](https://console.cloud.google.com/apis/library?project=vaultcaddy-production)

### 1.2 搜尋並啟用 Generative AI API
1. 在搜尋框中輸入「Generative Language API」
2. 點擊「Generative Language API」
3. 點擊「啟用」按鈕

**直接連結**：
[Generative Language API](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com?project=vaultcaddy-production)

## 步驟 2: 創建 API 金鑰

### 2.1 進入憑證頁面
1. 在左側選單選擇「API 和服務」→「憑證」
2. 或直接使用連結：[憑證頁面](https://console.cloud.google.com/apis/credentials?project=vaultcaddy-production)

### 2.2 創建 API 金鑰
1. 點擊「+ 建立憑證」
2. 選擇「API 金鑰」
3. 會彈出對話框顯示新的 API 金鑰
4. **立即複製並保存這個金鑰**（格式類似：AIzaSy...）

### 2.3 限制 API 金鑰（重要安全步驟）
1. 點擊「限制金鑰」或編輯剛創建的金鑰
2. 在「API 限制」部分：
   - 選擇「限制金鑰」
   - 勾選「Generative Language API」
3. 在「應用程式限制」部分：
   - 選擇「HTTP 引用者（網站）」
   - 添加以下網址：
     - `https://vaultcaddy.com/*`
     - `http://localhost:*`（用於開發測試）
4. 點擊「儲存」

## 步驟 3: 其他建議的 API（可選）

### Document AI API
用於更高級的文檔處理：
[Document AI API](https://console.cloud.google.com/apis/library/documentai.googleapis.com?project=vaultcaddy-production)

### Cloud Vision API
用於圖像識別：
[Cloud Vision API](https://console.cloud.google.com/apis/library/vision.googleapis.com?project=vaultcaddy-production)

## 步驟 4: 設置 OAuth 2.0（用於用戶登入）

### 4.1 配置 OAuth 同意畫面
1. 前往：[OAuth 同意畫面](https://console.cloud.google.com/apis/credentials/consent?project=vaultcaddy-production)
2. 選擇「外部」用戶類型
3. 填寫必要資訊：
   - 應用程式名稱：VaultCaddy
   - 用戶支援電子郵件：vaultcaddy@gmail.com
   - 應用程式標誌：（可選）
   - 應用程式首頁：https://vaultcaddy.com
   - 應用程式隱私權政策：https://vaultcaddy.com/privacy.html

### 4.2 創建 OAuth 2.0 客戶端 ID
1. 在憑證頁面點擊「+ 建立憑證」→「OAuth 客戶端 ID」
2. 選擇「網路應用程式」
3. 設置：
   - 名稱：VaultCaddy Web Client
   - 已授權的 JavaScript 來源：
     - `https://vaultcaddy.com`
     - `http://localhost:8000`
   - 已授權的重新導向 URI：
     - `https://vaultcaddy.com`
     - `https://vaultcaddy.com/auth.html`

## 步驟 5: 測試 API

獲取 API Key 後，您可以使用以下方式測試：

### 使用 curl 測試
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Hello, 請用中文回答這是什麼 API"
      }]
    }]
  }' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY"
```

### 使用我們的測試工具
訪問：`https://vaultcaddy.com/test-google-apis.html`

## 安全提醒 ⚠️

1. **絕對不要在前端代碼中硬編碼 API 金鑰**
2. **定期輪換 API 金鑰**
3. **監控 API 使用量**
4. **設置適當的配額限制**

## 完成後的下一步

1. 將 API Key 添加到生產配置
2. 測試所有功能
3. 部署到生產環境

---

**當您獲得 API Key 後，請告訴我，我會幫您更新配置並進行測試！**
