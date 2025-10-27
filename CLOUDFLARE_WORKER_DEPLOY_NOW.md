# 🚀 立即部署 Cloudflare Worker

## ✅ Worker 已更新

Cloudflare Worker 已更新以支持 **DeepSeek Reasoner（思考模式）**。

---

## 📋 更新內容

### 1. 支持的模型

```javascript
const SUPPORTED_MODELS = [
  'deepseek-chat',      // DeepSeek-V3.2-Exp（非思考模式）
  'deepseek-reasoner'   // DeepSeek-V3.2-Exp（思考模式）- 推薦 ✅
];
```

### 2. 模型驗證

Worker 會自動驗證模型名稱，並在日誌中顯示警告。

### 3. Token 用量追蹤

Worker 會自動記錄並計算成本：

```javascript
{
  usage: {
    prompt_tokens: 1500,
    completion_tokens: 1000,
    total_tokens: 2500,
    estimated_cost_cny: "0.0110"  // ¥0.011
  }
}
```

**成本計算公式**：
- 輸入成本 = `prompt_tokens / 1,000,000 × ¥2`
- 輸出成本 = `completion_tokens / 1,000,000 × ¥8`

### 4. 圖片輸入警告

如果嘗試發送圖片，Worker 會顯示警告：
```
⚠️ 警告：DeepSeek API 不支持圖片輸入！請使用 Vision API OCR 先提取文本。
```

---

## 🔧 如何部署

### 方法 1：手動部署（推薦）

#### 步驟 1：打開 Cloudflare Dashboard

1. 訪問 https://dash.cloudflare.com/
2. 登入您的帳戶
3. 點擊 "Workers & Pages"
4. 找到 `deepseek-proxy`

#### 步驟 2：更新 Worker 代碼

1. 點擊 "Quick edit"
2. **刪除所有舊代碼**
3. 複製 `cloudflare-worker-deepseek.js` 的**全部內容**（第 1-188 行）
4. 粘貼到 Cloudflare 編輯器
5. 點擊 "Save and Deploy"

#### 步驟 3：驗證部署

等待 5-10 秒，然後測試：

```bash
curl https://deepseek-proxy.vaultcaddy.workers.dev
```

**預期結果**：
```json
{
  "error": "Method not allowed",
  "message": "只支持 POST 請求"
}
```

---

## 🧪 測試 DeepSeek Reasoner

### 測試 1：測試 Worker 端點

```bash
curl https://deepseek-proxy.vaultcaddy.workers.dev
```

**預期結果**：
```json
{
  "error": "Method not allowed",
  "message": "只支持 POST 請求"
}
```

✅ 如果看到這個，說明 Worker 正常運行。

### 測試 2：測試 deepseek-reasoner 模型

```bash
curl -X POST https://deepseek-proxy.vaultcaddy.workers.dev \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-reasoner",
    "messages": [
      {
        "role": "user",
        "content": "計算 123 + 456"
      }
    ]
  }'
```

**預期結果**：
```json
{
  "choices": [
    {
      "message": {
        "content": "123 + 456 = 579"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 20,
    "total_tokens": 35
  }
}
```

✅ 如果看到這個，說明 `deepseek-reasoner` 正常工作。

### 測試 3：在 VaultCaddy 中測試

1. 清除瀏覽器緩存（Ctrl+Shift+R）
2. 訪問 `https://vaultcaddy.com/firstproject.html`
3. 打開控制台（F12）
4. 上傳一個測試發票

**預期日誌**：
```
🔄 混合處理器初始化（DeepSeek Reasoner）
   ✅ Vision API OCR: 可用
   ✅ DeepSeek Model: deepseek-reasoner
   ✅ DeepSeek Worker: https://deepseek-proxy.vaultcaddy.workers.dev
   🧠 使用思考模式（Reasoning Mode）

🚀 混合處理器開始處理: invoice.jpg (invoice)
📸 步驟 1: 使用 Vision API 進行 OCR...
✅ OCR 完成

🤖 步驟 2: 使用 DeepSeek Reasoner 處理文本...
📥 收到 DeepSeek 請求: { model: "deepseek-reasoner", ... }
📤 DeepSeek 響應: {
  model: "deepseek-reasoner",
  status: 200,
  usage: {
    prompt_tokens: 1500,
    completion_tokens: 1000,
    estimated_cost_cny: "0.0110"
  }
}
✅ DeepSeek 處理完成

🎉 混合處理完成
```

---

## 📊 查看 Worker 日誌

### 方法 1：Cloudflare Dashboard

1. 打開 Cloudflare Dashboard
2. 進入 "Workers & Pages"
3. 點擊 `deepseek-proxy`
4. 點擊 "Logs" 標籤
5. 點擊 "Begin log stream"

**您會看到**：
```
📥 收到 DeepSeek 請求: {
  origin: "https://vaultcaddy.com",
  model: "deepseek-reasoner",
  hasMessages: true,
  messageCount: 2,
  hasImages: false
}

📤 DeepSeek 響應: {
  model: "deepseek-reasoner",
  status: 200,
  ok: true,
  usage: {
    prompt_tokens: 1500,
    completion_tokens: 1000,
    total_tokens: 2500,
    estimated_cost_cny: "0.0110"
  }
}
```

### 方法 2：瀏覽器控制台

打開瀏覽器開發者工具（F12），在 Console 中查看。

---

## 💰 成本追蹤

### Worker 自動追蹤成本

每次 API 調用，Worker 都會在日誌中顯示：

```javascript
usage: {
  prompt_tokens: 1500,        // 輸入 token
  completion_tokens: 1000,    // 輸出 token
  total_tokens: 2500,         // 總計
  estimated_cost_cny: "0.0110" // 估算成本（CNY）
}
```

### 手動計算成本

**DeepSeek Reasoner 定價**：
- 輸入：¥2 / 百萬 tokens
- 輸出：¥8 / 百萬 tokens

**計算公式**：
```
總成本 = (輸入 tokens / 1,000,000 × ¥2) + (輸出 tokens / 1,000,000 × ¥8)
```

**示例**：
```
輸入：1,500 tokens
輸出：1,000 tokens

成本 = (1,500 / 1,000,000 × 2) + (1,000 / 1,000,000 × 8)
     = 0.003 + 0.008
     = ¥0.011
     ≈ $0.00154 USD
```

---

## ⚠️ 常見問題

### Q1: Worker 返回 400 錯誤

**原因**：可能的原因包括：
1. API Key 無效
2. 請求格式錯誤
3. 模型名稱錯誤

**解決方案**：
1. 檢查 API Key 是否正確
2. 檢查請求格式是否符合 DeepSeek API 規範
3. 確認使用 `deepseek-reasoner` 或 `deepseek-chat`

### Q2: 如何知道 Worker 是否已更新？

**方法 1**：查看日誌
```bash
curl https://deepseek-proxy.vaultcaddy.workers.dev
```

如果返回 `{"error":"Method not allowed","message":"只支持 POST 請求"}`，說明 Worker 正常運行。

**方法 2**：檢查 Worker 代碼
在 Cloudflare Dashboard 中查看代碼，確認包含：
```javascript
const SUPPORTED_MODELS = ['deepseek-chat', 'deepseek-reasoner'];
```

### Q3: 成本估算準確嗎？

**準確度**：約 99% 準確

Worker 使用 DeepSeek API 返回的實際 token 用量計算成本。

### Q4: 可以使用其他模型嗎？

**目前支持的模型**：
- ✅ `deepseek-chat`
- ✅ `deepseek-reasoner`

**不支持的模型**：
- ❌ `deepseek-vl2`（API 不可用）
- ❌ `deepseek-ocr`（API 不可用）
- ❌ 其他模型

---

## ✅ 部署清單

- [ ] 打開 Cloudflare Dashboard
- [ ] 找到 `deepseek-proxy` Worker
- [ ] 點擊 "Quick edit"
- [ ] 刪除舊代碼
- [ ] 複製 `cloudflare-worker-deepseek.js` 全部內容
- [ ] 粘貼到編輯器
- [ ] 點擊 "Save and Deploy"
- [ ] 等待 5-10 秒
- [ ] 測試 Worker（curl 命令）
- [ ] 清除瀏覽器緩存
- [ ] 在 VaultCaddy 中上傳測試文件
- [ ] 查看 Worker 日誌
- [ ] 驗證 token 用量和成本

---

## 🎯 預期結果

部署完成後，您應該看到：

1. ✅ Worker 正常運行
2. ✅ 支持 `deepseek-reasoner` 模型
3. ✅ 顯示 token 用量
4. ✅ 估算成本（CNY）
5. ✅ 詳細的日誌輸出

---

**最後更新**: 2025-10-27  
**狀態**: ✅ 準備部署  
**預計時間**: 5-10 分鐘

