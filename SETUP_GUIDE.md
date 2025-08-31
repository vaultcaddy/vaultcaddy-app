# 🚀 VaultCaddy 完整設置指南

## 📋 快速開始檢查清單

- [ ] **步驟 1**: 安裝依賴
- [ ] **步驟 2**: 設置 Google Cloud API
- [ ] **步驟 3**: 配置環境變數
- [ ] **步驟 4**: 測試 API 連接
- [ ] **步驟 5**: 啟動應用

---

## 🔧 步驟 1: 安裝依賴

```bash
# 確保你在專案目錄中
cd /Users/cavlinyeung/ai-bank-parser

# 安裝 Node.js 依賴
npm install

# 或使用 yarn
yarn install
```

**需要的依賴：**
- `dotenv`: 環境變數管理
- `@google-cloud/documentai`: Google Document AI
- `@google-cloud/vision`: Google Vision API
- `@azure/ai-form-recognizer`: Azure Form Recognizer
- `aws-sdk`: AWS Textract

---

## ☁️ 步驟 2: 設置 Google Cloud API

### 2.1 按照詳細指南
請參考 `GOOGLE_CLOUD_SETUP.md` 完成以下設置：

1. ✅ 啟用必要的 API
2. ✅ 建立 API 密鑰
3. ✅ 建立服務帳戶
4. ✅ 設置 Document AI 處理器
5. ✅ 下載服務帳戶 JSON 檔案

### 2.2 你的專案信息
- **專案ID**: `fifth-handbook-470515-n2`
- **專案名稱**: `My First Project`
- **免費額度**: $354.99 (91天)

---

## 🔐 步驟 3: 配置環境變數

### 3.1 建立 .env 檔案
```bash
# 複製範例檔案
cp .env.example .env

# 編輯 .env 檔案
nano .env  # 或使用你喜歡的編輯器
```

### 3.2 填入你的實際配置
```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=fifth-handbook-470515-n2
GOOGLE_APPLICATION_CREDENTIALS=./credentials/vaultcaddy-service-account.json

# Document AI Processors (替換為你的實際處理器ID)
BANK_STATEMENT_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_PROCESSOR_ID
INVOICE_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_INVOICE_PROCESSOR_ID
RECEIPT_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_RECEIPT_PROCESSOR_ID
GENERAL_PROCESSOR_ID=projects/fifth-handbook-470515-n2/locations/us/processors/YOUR_GENERAL_PROCESSOR_ID

# Azure Form Recognizer (可選)
AZURE_FORM_RECOGNIZER_ENDPOINT=https://your-region.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=your-azure-key

# Application Settings
NODE_ENV=development
PORT=3000
```

### 3.3 安全存放憑證
```bash
# 建立憑證目錄
mkdir -p credentials

# 將下載的 Google Cloud 服務帳戶 JSON 檔案放入此目錄
# 重新命名為: vaultcaddy-service-account.json
```

---

## 🧪 步驟 4: 測試 API 連接

### 4.1 測試配置
```bash
npm run test-config
```

**預期輸出：**
```
🔍 開始測試 API 配置...

🔧 服務可用性檢查：
✅ googleCloud: 已配置
❌ azure: 未配置
❌ aws: 未配置

📊 總計：1/3 個服務已配置

🔍 Google Cloud 詳細配置：
   項目ID: fifth-handbook-470515-n2
   認證方式: Service Account JSON
   處理器配置:
     ✅ bankStatement: 已配置
     ✅ invoice: 已配置
     ✅ receipt: 已配置
     ✅ general: 已配置

💡 下一步建議：
✅ Google Cloud 已配置，可以開始處理文檔
```

### 4.2 如果測試失敗
檢查以下項目：

**常見問題：**
1. **找不到 .env 檔案**
   ```bash
   # 確認檔案存在
   ls -la .env
   ```

2. **服務帳戶 JSON 檔案路徑錯誤**
   ```bash
   # 確認檔案存在
   ls -la credentials/vaultcaddy-service-account.json
   ```

3. **處理器ID格式錯誤**
   - 應該是完整路徑：`projects/PROJECT_ID/locations/LOCATION/processors/PROCESSOR_ID`

---

## 🚀 步驟 5: 啟動應用

### 5.1 開發模式
```bash
# 啟動開發服務器
npm run dev

# 或直接用瀏覽器打開
open index.html
```

### 5.2 生產模式
```bash
# 啟動生產服務器
npm start
```

### 5.3 訪問應用
- **主頁**: `http://localhost:3000` 或直接打開 `index.html`
- **儀表板**: 點擊 "登入" 按鈕進入
- **處理文檔**: 在儀表板中選擇文檔類型並上傳

---

## 🔍 驗證功能

### 測試文檔處理流程：

1. **打開主頁** (`index.html`)
2. **點擊登入** → 進入儀表板
3. **選擇文檔類型** → 例如 "銀行對帳單"
4. **上傳PDF檔案** → 測試AI處理
5. **查看結果** → 驗證數據提取準確性

### 預期結果：
- ✅ 文檔成功上傳
- ✅ AI 正確識別文檔類型
- ✅ 準確提取交易數據
- ✅ 可下載多種格式 (CSV, Excel, JSON)

---

## 🛠️ 故障排除

### 問題 1: "Google Cloud service not properly configured"
**解決方案：**
1. 檢查 `.env` 檔案中的 `GOOGLE_CLOUD_PROJECT_ID`
2. 確認服務帳戶 JSON 檔案路徑正確
3. 驗證 Google Cloud API 已啟用

### 問題 2: "處理器未找到"
**解決方案：**
1. 確認在 Google Cloud Console 中建立了處理器
2. 檢查處理器ID格式是否正確
3. 確認處理器所在地區與配置一致

### 問題 3: "API 配額超限"
**解決方案：**
1. 檢查 Google Cloud Console 中的配額使用情況
2. 確認免費額度未用完
3. 考慮升級到付費方案

### 問題 4: "CORS 錯誤"
**解決方案：**
1. 使用本地服務器而非直接打開 HTML 檔案
2. 確認 API 密鑰限制設置正確
3. 添加正確的域名到允許清單

---

## 📞 獲得幫助

如果遇到問題：

1. **檢查日誌**: 打開瀏覽器開發者工具查看錯誤信息
2. **運行測試**: `npm run test-config` 診斷配置問題
3. **參考文檔**: 
   - `GOOGLE_CLOUD_SETUP.md` - Google Cloud 詳細設置
   - `config-secure.js` - 配置管理邏輯
4. **聯繫支援**: 提供錯誤日誌和配置信息

---

## 🎉 成功！

如果所有步驟都完成且測試通過，恭喜！你現在擁有一個功能完整的 AI 文檔處理平台：

- ✅ **多文檔類型支援**: 銀行對帳單、發票、收據、通用文檔
- ✅ **多平台 AI 整合**: Google Cloud + Azure + AWS
- ✅ **安全配置管理**: 環境變數 + 服務帳戶
- ✅ **專業用戶界面**: 對標 LedgerBox 的現代化設計
- ✅ **多格式輸出**: CSV、Excel、JSON、QBO

**開始處理你的第一個文檔吧！** 🚀

