# Google Cloud API 完整設置教學

## 🚀 步驟概覽
你的Google Cloud項目：**My First Project** (ID: fifth-handbook-470515-n2)  
免費額度：$2,354.99，試用期限：91天

---

## 📋 **步驟 1：啟用必要的 API**

### 1.1 進入 API Library
```
Google Cloud Console → API 和服務 → 程式庫
或直接訪問：https://console.cloud.google.com/apis/library
```

### 1.2 需要啟用的 API：
搜尋並啟用以下API：

✅ **Cloud Vision API**
- 用途：文字識別 (OCR)
- 搜尋：`Cloud Vision API`
- 點擊 "啟用"

✅ **Cloud Document AI API** 
- 用途：結構化文檔處理
- 搜尋：`Cloud Document AI API`
- 點擊 "啟用"

✅ **Cloud Translation API** (可選)
- 用途：多語言支援
- 搜尋：`Cloud Translation API`
- 點擊 "啟用"

---

## 🔑 **步驟 2：建立 API 密鑰**

### 2.1 進入憑證頁面
```
Google Cloud Console → API 和服務 → 憑證
或直接訪問：https://console.cloud.google.com/apis/credentials
```

### 2.2 建立 API 密鑰
1. 點擊 **"+ 建立憑證"**
2. 選擇 **"API 金鑰"**
3. 複製產生的API密鑰
4. 點擊 **"限制金鑰"** 進行安全設定

### 2.3 限制 API 密鑰（重要！）
在金鑰限制頁面：

**應用程式限制：**
- 選擇 "HTTP 轉介程式 (網站)"
- 新增你的網域：
  ```
  https://yourdomain.com/*
  https://localhost:3000/*  (開發用)
  ```

**API 限制：**
- 選擇 "限制金鑰"
- 勾選：
  - Cloud Vision API
  - Cloud Document AI API
  - Cloud Translation API

---

## 🔐 **步驟 3：建立服務帳戶（推薦）**

### 3.1 建立服務帳戶
```
Google Cloud Console → IAM 與管理 → 服務帳戶
```

1. 點擊 **"+ 建立服務帳戶"**
2. 填寫：
   - **服務帳戶名稱**：`vaultcaddy-ai-service`
   - **描述**：`VaultCaddy AI 文檔處理服務`
3. 點擊 **"建立並繼續"**

### 3.2 指派角色
選擇以下角色：
- **Cloud Vision Client**
- **Document AI Editor**
- **AI Platform User**

### 3.3 下載憑證金鑰
1. 點擊建立的服務帳戶
2. 切換到 **"金鑰"** 標籤
3. 點擊 **"新增金鑰"** → **"建立新金鑰"**
4. 選擇 **JSON** 格式
5. 下載並**安全保存**這個 JSON 檔案

---

## 🤖 **步驟 4：設定 Document AI 處理器**

### 4.1 進入 Document AI
```
Google Cloud Console → 人工智慧 → Document AI
或直接訪問：https://console.cloud.google.com/ai/document-ai
```

### 4.2 建立處理器
為每種文檔類型建立專用處理器：

**4.2.1 銀行對帳單處理器**
1. 點擊 **"建立處理器"**
2. 選擇處理器類型：
   - **類型**：`Document OCR Processor`
   - **名稱**：`VaultCaddy-BankStatement`
   - **地區**：`us` 或 `asia-east1`
3. 記錄處理器ID（格式類似：`projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID`）

**4.2.2 發票處理器**
1. 建立新處理器
2. 選擇：
   - **類型**：`Invoice Processor`
   - **名稱**：`VaultCaddy-Invoice`

**4.2.3 收據處理器**
1. 建立新處理器
2. 選擇：
   - **類型**：`Receipt Processor`
   - **名稱**：`VaultCaddy-Receipt`

**4.2.4 通用處理器**
1. 建立新處理器
2. 選擇：
   - **類型**：`Form Parser Processor`
   - **名稱**：`VaultCaddy-General`

### 4.3 記錄處理器ID
每個處理器會有唯一的ID，格式如：
```
projects/fifth-handbook-470515-n2/locations/us/processors/abcd1234567890
```

---

## 💰 **步驟 5：了解計費和配額**

### 5.1 免費額度
你目前有 **$354.99** 免費額度，足夠進行大量測試：

**Cloud Vision API：**
- 前 1,000 次文字檢測/月：免費
- 超出部分：$1.50/1,000次

**Document AI：**
- 前 1,000 頁/月：免費
- 超出部分：$0.50-$1.50/頁（依處理器類型）

### 5.2 設定預算提醒
```
Google Cloud Console → 計費 → 預算和提醒
```
建議設定：
- **預算**：$100/月
- **提醒閾值**：50%, 80%, 100%

---

## 🔧 **步驟 6：配置你的專案**

### 6.1 建立 .env 檔案
在專案根目錄建立 `.env` 檔案：

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=fifth-handbook-470515-n2
GOOGLE_APPLICATION_CREDENTIALS=./credentials/vaultcaddy-service-account.json

# Document AI Processors (替換為你的實際ID)
BANK_STATEMENT_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_PROCESSOR_ID
INVOICE_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_INVOICE_PROCESSOR_ID
RECEIPT_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_RECEIPT_PROCESSOR_ID
GENERAL_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_GENERAL_PROCESSOR_ID
```

### 6.2 安全存放憑證
```bash
# 建立憑證目錄
mkdir credentials

# 將下載的JSON檔案放入此目錄
# 重新命名為：vaultcaddy-service-account.json
```

### 6.3 測試配置
使用我們提供的測試腳本驗證設定：

```javascript
const { getSecureConfig } = require('./config-secure');

// 測試配置
const config = getSecureConfig();
console.log('可用服務：', config.getAvailableServices());
```

---

## ✅ **設置檢查清單**

- [ ] 啟用 Cloud Vision API
- [ ] 啟用 Cloud Document AI API  
- [ ] 建立並限制 API 密鑰
- [ ] 建立服務帳戶
- [ ] 下載服務帳戶 JSON 憑證
- [ ] 建立 4 個 Document AI 處理器
- [ ] 記錄所有處理器ID
- [ ] 建立 .env 檔案
- [ ] 安全存放憑證檔案
- [ ] 設定預算提醒
- [ ] 測試 API 連接

---

## 🛡️ **安全最佳實踐**

### ❌ **絕對不要做：**
- 將API密鑰提交到Git倉庫
- 在前端JavaScript中暴露API密鑰
- 使用無限制的API密鑰

### ✅ **一定要做：**
- 使用環境變數存儲密鑰
- 限制API密鑰的使用範圍
- 定期輪換API密鑰
- 監控API使用量
- 設定預算提醒

---

## 🔄 **下一步**

完成上述設置後，你就可以：

1. **測試 API 連接**
2. **處理真實文檔**
3. **監控使用量和成本**
4. **根據需要調整配額**

需要幫助嗎？我可以協助你完成任何具體步驟！

