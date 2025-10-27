# 🔄 Cloudflare Worker 更新指南

## 📋 需要更新嗎？

### ✅ API Endpoint **不需要更改**

```javascript
const DEEPSEEK_API_ENDPOINT = 'https://api.deepseek.com/v1/chat/completions';
```

**原因**：
- 所有 DeepSeek 模型（deepseek-chat, deepseek-vl2, deepseek-ocr, janus-pro）都使用**同一個 endpoint**
- 只有 `model` 參數不同
- 這是 DeepSeek API 的標準設計

### ✅ 但我們改進了日誌記錄

我們添加了更詳細的日誌，幫助您了解：
- 使用了哪個模型
- 請求是否包含圖片
- API 返回了什麼錯誤

---

## 🚀 如何更新 Cloudflare Worker

### 方法 1：手動更新（推薦）

#### 步驟 1：打開 Cloudflare Dashboard
1. 訪問 https://dash.cloudflare.com/
2. 登入您的帳戶
3. 點擊左側 "Workers & Pages"
4. 找到並點擊 `deepseek-proxy`

#### 步驟 2：複製新代碼
1. 打開項目中的 `cloudflare-worker-deepseek.js` 文件
2. 複製**全部內容**（第 1-150 行）

#### 步驟 3：更新 Worker
1. 在 Cloudflare Dashboard 中，點擊 "Quick edit"
2. **刪除**舊代碼
3. **粘貼**新代碼
4. 點擊 "Save and Deploy"

#### 步驟 4：驗證部署
1. 等待 5-10 秒
2. 訪問 https://deepseek-proxy.vaultcaddy.workers.dev
3. 應該看到：`{"error":"Method not allowed","message":"只支持 POST 請求"}`

---

### 方法 2：使用 Wrangler CLI（進階）

如果您安裝了 Wrangler CLI：

```bash
# 1. 登入 Cloudflare
wrangler login

# 2. 部署 Worker
wrangler deploy cloudflare-worker-deepseek.js --name deepseek-proxy

# 3. 驗證部署
curl https://deepseek-proxy.vaultcaddy.workers.dev
```

---

## 📊 新日誌格式

### 請求日誌（更詳細）

**之前**：
```javascript
📥 收到 DeepSeek 請求: {
  origin: "https://vaultcaddy.com",
  timestamp: "2025-10-27T10:30:00.000Z",
  hasMessages: true
}
```

**現在**：
```javascript
📥 收到 DeepSeek 請求: {
  origin: "https://vaultcaddy.com",
  model: "deepseek-vl2",              // ✅ 新增：模型名稱
  hasMessages: true,
  hasImages: true,                     // ✅ 新增：是否包含圖片
  timestamp: "2025-10-27T10:30:00.000Z"
}
```

### 響應日誌（更詳細）

**之前**：
```javascript
📤 DeepSeek 響應: {
  status: 200,
  ok: true,
  timestamp: "2025-10-27T10:30:05.000Z"
}
```

**現在**：
```javascript
📤 DeepSeek 響應: {
  model: "deepseek-vl2",               // ✅ 新增：模型名稱
  status: 200,
  ok: true,
  hasChoices: true,                    // ✅ 新增：是否有響應內容
  timestamp: "2025-10-27T10:30:05.000Z"
}
```

### 錯誤日誌（更詳細）

**之前**：
```javascript
❌ DeepSeek API 錯誤: {
  error: { message: "Model not found" }
}
```

**現在**：
```javascript
❌ DeepSeek API 錯誤: {
  model: "deepseek-vl2",               // ✅ 新增：哪個模型失敗了
  status: 400,
  error: { message: "Model not found" }
}
```

---

## 🔍 如何查看 Worker 日誌

### 方法 1：Cloudflare Dashboard（實時日誌）

1. 打開 Cloudflare Dashboard
2. 進入 "Workers & Pages"
3. 點擊 `deepseek-proxy`
4. 點擊 "Logs" 標籤
5. 點擊 "Begin log stream"

您會看到：
```
📥 收到 DeepSeek 請求: { model: "deepseek-vl2", hasImages: true, ... }
📤 DeepSeek 響應: { model: "deepseek-vl2", status: 200, ... }
```

### 方法 2：Wrangler CLI（實時日誌）

```bash
wrangler tail deepseek-proxy
```

### 方法 3：瀏覽器控制台（客戶端）

打開瀏覽器開發者工具（F12），您會看到：
```
🤖 嘗試模型 1/5: deepseek-vl2
   📤 發送請求到 DeepSeek API...
   ✅ 模型 deepseek-vl2 成功返回響應
```

---

## 🧪 測試更新後的 Worker

### 測試 1：檢查 Worker 是否運行

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

### 測試 2：測試模型請求（使用 curl）

```bash
curl -X POST https://deepseek-proxy.vaultcaddy.workers.dev \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-vl2",
    "messages": [
      {
        "role": "user",
        "content": "Hello"
      }
    ]
  }'
```

**預期結果**（如果模型可用）：
```json
{
  "choices": [
    {
      "message": {
        "content": "Hello! How can I help you?"
      }
    }
  ]
}
```

**預期結果**（如果模型不可用）：
```json
{
  "error": "DeepSeek API 錯誤",
  "model": "deepseek-vl2",
  "status": 400,
  "details": {
    "error": {
      "message": "Model not found"
    }
  }
}
```

### 測試 3：在 VaultCaddy 中測試

1. 清除瀏覽器緩存（Ctrl+Shift+R）
2. 訪問 https://vaultcaddy.com/firstproject.html
3. 上傳一個測試文件
4. 打開控制台（F12）查看日誌

---

## 📝 更新清單

- [ ] 打開 Cloudflare Dashboard
- [ ] 找到 `deepseek-proxy` Worker
- [ ] 複製 `cloudflare-worker-deepseek.js` 的全部內容
- [ ] 在 Cloudflare 中更新代碼
- [ ] 點擊 "Save and Deploy"
- [ ] 等待 5-10 秒
- [ ] 測試 Worker（curl 或瀏覽器）
- [ ] 查看日誌（確認新日誌格式）
- [ ] 在 VaultCaddy 中上傳測試文件
- [ ] 驗證模型選擇是否正常工作

---

## ❓ 常見問題

### Q1: 更新後，舊的 API Key 會丟失嗎？

**A**: 不會！`DEEPSEEK_API_KEY` 已經在新代碼中：
```javascript
const DEEPSEEK_API_KEY = 'sk-4a43b49a13a840009052be65f599b7a4';
```

### Q2: 需要更改 Worker URL 嗎？

**A**: 不需要！Worker URL 保持不變：
```
https://deepseek-proxy.vaultcaddy.workers.dev
```

### Q3: 更新會影響現有功能嗎？

**A**: 不會！我們只是添加了更詳細的日誌，核心功能完全相同。

### Q4: 如果更新失敗怎麼辦？

**A**: 
1. 檢查是否複製了完整的代碼（第 1-150 行）
2. 確保沒有語法錯誤（Cloudflare 會顯示錯誤）
3. 如果有問題，可以回滾到舊版本（Cloudflare 保留歷史版本）

### Q5: 如何回滾到舊版本？

**A**: 
1. 在 Cloudflare Dashboard 中，點擊 "Deployments"
2. 找到之前的部署
3. 點擊 "Rollback"

---

## 🎯 更新後的優勢

### 1. 更好的調試能力
- 知道哪個模型被使用
- 知道哪個模型失敗了
- 更容易找到問題

### 2. 更好的監控
- 追蹤模型使用情況
- 監控 API 成功率
- 分析性能

### 3. 更好的錯誤處理
- 詳細的錯誤信息
- 包含模型名稱
- 便於排查問題

---

## 📞 需要幫助？

如果更新過程中遇到問題：

1. **檢查 Cloudflare 日誌**
   - 查看是否有錯誤信息
   - 確認 Worker 是否正常運行

2. **檢查瀏覽器控制台**
   - 查看客戶端日誌
   - 確認請求是否發送成功

3. **測試 Worker**
   - 使用 curl 測試
   - 確認返回正確的錯誤信息

4. **回滾**
   - 如果有問題，回滾到舊版本
   - 然後重新嘗試

---

**最後更新**: 2025-10-27  
**狀態**: ✅ 準備更新

**重要提醒**: 
- API Endpoint **不需要更改**
- 只需要更新 Worker 代碼
- 更新後立即測試

