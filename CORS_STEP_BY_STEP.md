# 🔧 Firebase Storage CORS 設置 - 詳細教學

## 📋 目標
讓 Vision API 能夠訪問 Firebase Storage 中的文件，解決銀行對帳單處理失敗問題。

---

## 🚀 步驟 1：檢查 Google Cloud SDK 是否已安裝

打開終端，執行：

```bash
gcloud --version
```

**預期輸出：**
```
Google Cloud SDK 456.0.0
bq 2.0.101
core 2024.01.12
gcloud-crc32c 1.0.0
gsutil 5.27
```

**如果顯示 "command not found"：**
```bash
# 使用 Homebrew 安裝
brew install --cask google-cloud-sdk

# 安裝後，重新載入 shell
source ~/.zshrc

# 再次檢查
gcloud --version
```

---

## 🚀 步驟 2：登入 Google Cloud

```bash
gcloud auth login
```

**會發生什麼：**
1. 瀏覽器會自動打開
2. 選擇您的 Google 帳戶（`vaultcaddy@gmail.com` 或 `osclin2002@gmail.com`）
3. 點擊「允許」
4. 看到「You are now authenticated」

**終端預期輸出：**
```
You are now logged in as [vaultcaddy@gmail.com].
Your current project is [vaultcaddy-production-cbbe2].
```

**如果瀏覽器無法打開：**
```bash
gcloud auth login --no-launch-browser
# 會給您一個 URL，手動複製到瀏覽器打開
```

---

## 🚀 步驟 3：設置項目

```bash
gcloud config set project vaultcaddy-production-cbbe2
```

**預期輸出：**
```
Updated property [core/project].
```

**驗證項目設置：**
```bash
gcloud config get-value project
```

**預期輸出：**
```
vaultcaddy-production-cbbe2
```

---

## 🚀 步驟 4：檢查 cors.json 文件

```bash
cd /Users/cavlinyeung/ai-bank-parser
cat cors.json
```

**預期輸出（應該看到完整的 JSON）：**
```json
[
  {
    "origin": ["https://vaultcaddy.com", "http://localhost:*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "maxAgeSeconds": 3600,
    "responseHeader": [
      "Content-Type",
      "Access-Control-Allow-Origin",
      "Access-Control-Allow-Methods",
      "Access-Control-Allow-Headers",
      "Access-Control-Max-Age",
      "x-goog-meta-*"
    ]
  }
]
```

**如果看不到內容或格式錯誤：**
```bash
# 重新創建 cors.json
echo '[
  {
    "origin": ["https://vaultcaddy.com", "http://localhost:*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "maxAgeSeconds": 3600,
    "responseHeader": [
      "Content-Type",
      "Access-Control-Allow-Origin",
      "Access-Control-Allow-Methods",
      "Access-Control-Allow-Headers",
      "Access-Control-Max-Age",
      "x-goog-meta-*"
    ]
  }
]' > cors.json
```

---

## 🚀 步驟 5：列出所有 Storage Buckets

**先確認 bucket 存在：**

```bash
gsutil ls
```

**預期輸出（應該看到您的 bucket）：**
```
gs://vaultcaddy-production-cbbe2.appspot.com/
gs://vaultcaddy-production-cbbe2.firebasestorage.app/
```

**如果只看到一個 bucket，記下它的名稱！**

---

## 🚀 步驟 6：設置 CORS（關鍵步驟）

### 方法 A：使用 .firebasestorage.app（推薦）

```bash
gsutil cors set cors.json gs://vaultcaddy-production-cbbe2.firebasestorage.app
```

### 方法 B：使用 .appspot.com（備用）

```bash
gsutil cors set cors.json gs://vaultcaddy-production-cbbe2.appspot.com
```

**預期輸出（可能沒有任何輸出，這是正常的！）：**
```
Setting CORS on gs://vaultcaddy-production-cbbe2.firebasestorage.app/...
```

**或者可能完全沒有輸出，直接回到命令提示符。這也是正常的！**

**如果看到錯誤：**
```
BucketNotFoundException: 404 gs://... bucket does not exist.
```

**解決方法：**
1. 回到步驟 5，確認正確的 bucket 名稱
2. 使用正確的 bucket 名稱重試

---

## 🚀 步驟 7：驗證 CORS 設置（最重要！）

```bash
gsutil cors get gs://vaultcaddy-production-cbbe2.firebasestorage.app
```

**預期輸出（應該看到您剛才設置的 CORS 規則）：**
```json
[
  {
    "origin": ["https://vaultcaddy.com", "http://localhost:*"],
    "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
    "maxAgeSeconds": 3600,
    "responseHeader": [
      "Content-Type",
      "Access-Control-Allow-Origin",
      "Access-Control-Allow-Methods",
      "Access-Control-Allow-Headers",
      "Access-Control-Max-Age",
      "x-goog-meta-*"
    ]
  }
]
```

**如果看到這個輸出，恭喜！CORS 設置成功！✅**

**如果看到 "No CORS configuration"：**
- 說明設置失敗，需要重試步驟 6

---

## 🚀 步驟 8：測試銀行對帳單上傳

1. 打開瀏覽器，前往 `https://vaultcaddy.com`
2. 登入您的帳戶
3. 刷新頁面（Ctrl+F5 或 Cmd+Shift+R）
4. 上傳銀行對帳單 PDF
5. 打開瀏覽器控制台（F12）
6. 查看是否有 CORS 錯誤

**成功的標誌：**
- ✅ 無 CORS 錯誤
- ✅ 看到 "Vision API 處理成功"
- ✅ 文件狀態變為 "completed"

---

## 🔍 故障排除

### 問題 1：gsutil 命令找不到

```bash
# 重新安裝
brew install --cask google-cloud-sdk

# 添加到 PATH
echo 'source /opt/homebrew/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/path.zsh.inc' >> ~/.zshrc
source ~/.zshrc
```

### 問題 2：權限錯誤

```bash
# 檢查當前用戶
gcloud auth list

# 切換到正確的帳戶
gcloud config set account vaultcaddy@gmail.com

# 重新授權
gcloud auth login
```

### 問題 3：項目不存在

```bash
# 列出所有項目
gcloud projects list

# 確認項目 ID
gcloud config set project <正確的項目ID>
```

### 問題 4：Bucket 不存在

```bash
# 列出所有 buckets
gsutil ls

# 使用正確的 bucket 名稱
gsutil cors set cors.json gs://<正確的bucket名稱>
```

---

## 📞 需要幫助？

如果遇到問題，請執行以下命令並告訴我輸出：

```bash
# 1. 檢查 gcloud 配置
gcloud config list

# 2. 檢查認證狀態
gcloud auth list

# 3. 列出所有 buckets
gsutil ls

# 4. 檢查當前 CORS 設置
gsutil cors get gs://vaultcaddy-production-cbbe2.firebasestorage.app

# 5. 詳細錯誤輸出
gsutil -D cors set cors.json gs://vaultcaddy-production-cbbe2.firebasestorage.app 2>&1
```

我會根據這些輸出幫您診斷問題！🚀

