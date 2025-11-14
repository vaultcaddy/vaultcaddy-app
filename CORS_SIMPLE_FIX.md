# 🔧 Firebase Storage CORS 簡易修復指南

## 問題：找不到「配置」選項

從圖1看到，Google Cloud Storage Console 的界面可能沒有「配置」標籤。

---

## ✅ 解決方案：使用 gsutil 命令（最簡單）

### 步驟 1：安裝 Google Cloud SDK

**方法 A：使用 Homebrew（推薦）**
```bash
brew install --cask google-cloud-sdk
```

**方法 B：使用安裝腳本**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 步驟 2：初始化 gcloud

```bash
gcloud init
```

**選擇：**
1. 登入帳戶：選擇 `vaultcaddy@gmail.com` 或 `osclin2002@gmail.com`
2. 選擇項目：`vaultcaddy-production-cbbe2`

### 步驟 3：設置 CORS

```bash
cd /Users/cavlinyeung/ai-bank-parser
gsutil cors set cors.json gs://vaultcaddy-production-cbbe2.appspot.com
```

**預期輸出：**
```
Setting CORS on gs://vaultcaddy-production-cbbe2.appspot.com/...
```

### 步驟 4：驗證 CORS 設置

```bash
gsutil cors get gs://vaultcaddy-production-cbbe2.appspot.com
```

**預期輸出：**
```json
[
  {
    "origin": ["https://vaultcaddy.com", "http://localhost:*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "maxAgeSeconds": 3600,
    "responseHeader": [...]
  }
]
```

---

## 🎯 完整執行流程

打開終端，依次執行：

```bash
# 1. 安裝 Google Cloud SDK（如果未安裝）
brew install --cask google-cloud-sdk

# 2. 初始化（首次使用）
gcloud init
# 選擇帳戶和項目

# 3. 切換到項目目錄
cd /Users/cavlinyeung/ai-bank-parser

# 4. 設置 CORS
gsutil cors set cors.json gs://vaultcaddy-production-cbbe2.appspot.com

# 5. 驗證設置
gsutil cors get gs://vaultcaddy-production-cbbe2.appspot.com

echo "✅ CORS 設置完成！"
```

---

## 🧪 測試 CORS

### 測試 1：重新上傳銀行對帳單

1. 刷新頁面（Ctrl+F5）
2. 上傳銀行對帳單 PDF
3. 查看控制台：
   - ✅ 無 CORS 錯誤
   - ✅ Vision API 成功

### 測試 2：檢查控制台

在瀏覽器控制台輸入：

```javascript
fetch('https://firebasestorage.googleapis.com/v0/b/vaultcaddy-production-cbbe2.appspot.com/o/')
  .then(r => console.log('✅ CORS 正常'))
  .catch(e => console.error('❌ CORS 錯誤:', e))
```

---

## ❓ 常見問題

### Q: 找不到 gsutil 命令

**A:** 重新執行安裝：
```bash
brew install --cask google-cloud-sdk
source ~/.zshrc
```

### Q: gcloud init 失敗

**A:** 使用無瀏覽器模式：
```bash
gcloud init --console-only
```

### Q: 權限錯誤

**A:** 確認您使用的帳戶是項目擁有者：
```bash
gcloud projects get-iam-policy vaultcaddy-production-cbbe2
```

---

## 📞 如果仍有問題

請執行以下命令並告訴我輸出：

```bash
# 檢查 gcloud 配置
gcloud config list

# 檢查項目權限
gcloud projects get-iam-policy vaultcaddy-production-cbbe2

# 嘗試設置 CORS（詳細輸出）
gsutil -D cors set cors.json gs://vaultcaddy-production-cbbe2.appspot.com
```

我會根據錯誤信息提供解決方案！🚀

