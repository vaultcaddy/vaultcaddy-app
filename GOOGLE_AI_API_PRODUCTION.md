# 🔗 VaultCaddy Google AI API 生產環境整合指南

## 📋 整合概覽

在 `vaultcaddy.com` 成功上線後，您需要整合真實的 Google AI API 來處理文檔。

## 🎯 前置要求

### 必須完成項目
- ✅ `vaultcaddy.com` 域名已設置
- ✅ GitHub Pages 部署成功
- ✅ HTTPS 已啟用
- ✅ 網站可正常訪問

## 🏗️ Google Cloud Platform 設置

### Step 1: 創建 Google Cloud 項目

1. 前往 [Google Cloud Console](https://console.cloud.google.com)
2. 點擊頂部的項目選擇器
3. 點擊 **NEW PROJECT**
4. 填寫項目信息：
   ```
   Project name: VaultCaddy Production
   Organization: (您的組織，可選)
   Location: (您的位置)
   ```
5. 點擊 **CREATE**

### Step 2: 啟用必要的 APIs

在新項目中啟用以下 API：

#### 2.1 Vision API (OCR 圖片文字識別)
```
API 名稱: Cloud Vision API
用途: 處理收據和發票圖片
價格: $1.50 per 1,000 units
```

#### 2.2 Document AI (結構化文檔處理)
```
API 名稱: Cloud Document AI API
用途: 處理 PDF 銀行對帳單和發票
價格: $0.005 per page
```

#### 2.3 Translation API (多語言支持)
```
API 名稱: Cloud Translation API
用途: 多語言文檔處理
價格: $20 per 1M characters
```

### Step 3: 創建 API 憑證

#### 3.1 創建 API Key
1. 前往 **APIs & Services > Credentials**
2. 點擊 **+ CREATE CREDENTIALS**
3. 選擇 **API key**
4. 複製生成的 API Key（保密！）

#### 3.2 限制 API Key 安全性
1. 點擊剛創建的 API Key 旁邊的編輯按鈕
2. 設置 **Application restrictions**：
   ```
   HTTP referrers (web sites)
   Add these referrers:
   - https://vaultcaddy.com/*
   - https://www.vaultcaddy.com/*
   ```
3. 設置 **API restrictions**：
   ```
   Restrict key
   Select APIs:
   ✓ Cloud Vision API
   ✓ Cloud Document AI API
   ✓ Cloud Translation API
   ```
4. 點擊 **SAVE**

## 💻 代碼更新

### 更新 ai-services.js

<function_calls>
<invoke name="search_replace">
<parameter name="file_path">/Users/cavlinyeung/ai-bank-parser/ai-services.js
