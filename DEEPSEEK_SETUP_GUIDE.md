# DeepSeek AI 設置指南

## 概述

本指南將幫助你完成 DeepSeek AI 的設置，包括：
1. 部署 Cloudflare Worker（保護 API Key）
2. 驗證 DeepSeek AI 功能

---

## 步驟 1：部署 Cloudflare Worker

### 1.1 登入 Cloudflare Workers

1. 訪問 [Cloudflare Workers](https://workers.cloudflare.com/)
2. 使用你的 Cloudflare 帳戶登入

### 1.2 創建新的 Worker

1. 點擊 **"Create a Service"** 或 **"Create Worker"**
2. 輸入 Worker 名稱：`deepseek-proxy`
3. 點擊 **"Create Service"**

### 1.3 編輯 Worker 代碼

1. 在 Worker 編輯頁面，點擊 **"Quick Edit"**
2. 刪除現有代碼
3. 複製 `cloudflare-worker-deepseek.js` 的完整內容並粘貼
4. **重要**：將第 8 行的 API Key 替換為你從 DeepSeek 平台複製的完整 API Key：
   ```javascript
   const DEEPSEEK_API_KEY = 'sk-4a43b8c2e7f54f4bb2c8e8f9e7b7a4'; // ⚠️ 請替換為完整的 API Key
   ```
5. 點擊 **"Save and Deploy"**

### 1.4 獲取 Worker URL

1. 部署成功後，你會看到 Worker URL，格式類似：
   ```
   https://deepseek-proxy.YOUR_SUBDOMAIN.workers.dev
   ```
2. 複製這個 URL

### 1.5 更新 VaultCaddy 配置

1. 打開 `firstproject.html`
2. 找到第 1925 行附近的 DeepSeek 初始化代碼
3. 將 `deepseekWorkerUrl` 更新為你的 Worker URL：
   ```javascript
   const deepseekWorkerUrl = 'https://deepseek-proxy.YOUR_SUBDOMAIN.workers.dev';
   ```

---

## 步驟 2：驗證設置

### 2.1 測試 Worker

使用以下 `curl` 命令測試 Worker 是否正常工作：

```bash
curl -X POST https://deepseek-proxy.YOUR_SUBDOMAIN.workers.dev \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {
        "role": "user",
        "content": "Hello, DeepSeek!"
      }
    ]
  }'
```

**預期響應**：你應該收到一個 JSON 響應，包含 DeepSeek AI 的回覆。

### 2.2 在 VaultCaddy 中測試

1. 打開 VaultCaddy 網站
2. 登入你的帳戶
3. 進入任何項目
4. 點擊 **"Upload files"** 按鈕
5. 上傳一張發票或收據圖片
6. 打開瀏覽器的開發者工具（F12）
7. 查看 Console 標籤，你應該看到：
   ```
   🤖 初始化 DeepSeek Vision Client...
   ✅ DeepSeek Vision Client 已初始化
   🚀 DeepSeek Vision Client 處理文檔: [文件名] (invoice)
   ✅ DeepSeek 原始響應: {...}
   ```

---

## DeepSeek API 定價

DeepSeek AI 的定價非常有競爭力：

| 模型 | 輸入 (每 1M tokens) | 輸出 (每 1M tokens) |
|------|---------------------|---------------------|
| deepseek-chat | $0.14 | $0.28 |

**對比 OpenAI GPT-4 Vision**：
- OpenAI GPT-4 Vision: $2.50 (輸入) / $10.00 (輸出)
- **DeepSeek 便宜約 17-35 倍！**

---

## 常見問題

### Q1: Worker 返回 405 錯誤
**A**: 這是正常的。Worker 只接受 POST 請求。如果你看到 `{"error":"Method not allowed","message":"只支持 POST 請求"}`，說明 Worker 已正確部署。

### Q2: Worker 返回 401 錯誤
**A**: 檢查 `cloudflare-worker-deepseek.js` 中的 `DEEPSEEK_API_KEY` 是否正確填寫。

### Q3: Worker 返回 CORS 錯誤
**A**: 確保 `ALLOWED_ORIGINS` 中包含你的網站域名（如 `https://vaultcaddy.com`）。

### Q4: 如何查看 DeepSeek 使用量？
**A**: 登入 [DeepSeek 平台](https://platform.deepseek.com/usage)，在 "Usage" 頁面查看你的 API 使用情況。

---

## 安全建議

1. **不要將 API Key 直接暴露在前端代碼中**
   - ✅ 正確：使用 Cloudflare Worker 作為代理
   - ❌ 錯誤：直接在 JavaScript 中使用 API Key

2. **定期更換 API Key**
   - 建議每 3-6 個月更換一次 API Key

3. **監控 API 使用量**
   - 定期檢查 DeepSeek 平台的使用情況
   - 設置使用量警報（如果可用）

---

## 支援

如果你在設置過程中遇到任何問題，請：
1. 檢查瀏覽器的開發者工具 Console 標籤
2. 查看 Cloudflare Worker 的日誌
3. 參考 DeepSeek 官方文檔：https://platform.deepseek.com/docs

---

## 下一步

設置完成後，你可以：
1. 上傳測試文檔，驗證 AI 提取功能
2. 查看提取的數據是否準確
3. 根據需要調整 AI 提示詞（在 `deepseek-vision-client.js` 中）

**祝你使用愉快！** 🎉

