# Cloudflare Worker 更新指南

## 🚨 問題診斷

### **錯誤信息**
```
❌ DeepSeek API 請求失敗（已重試 3 次）: signal is aborted without reason
```

### **根本原因**
1. ❌ Cloudflare Worker 不支持 `deepseek-reasoner` 模型
2. ❌ Worker 超時限制可能是 30 秒（與前端 60 秒不一致）
3. ❌ Worker 沒有正確轉發 `max_tokens` 參數

---

## ✅ 解決方案

### **更新 Cloudflare Worker 代碼**

新的 Worker 代碼已創建：`cloudflare-worker-deepseek-reasoner.js`

**關鍵改進：**
1. ✅ 添加 `deepseek-reasoner` 到支持模型列表
2. ✅ 增加超時時間到 60 秒（與前端一致）
3. ✅ 正確轉發 `max_tokens` 參數
4. ✅ 改進錯誤處理和日誌

---

## 📝 部署步驟

### **步驟 1：登錄 Cloudflare Dashboard**

1. 訪問：https://dash.cloudflare.com/
2. 登錄您的帳戶
3. 點擊左側菜單 **Workers & Pages**

---

### **步驟 2：找到現有 Worker**

1. 在 Workers 列表中找到：`deepseek-proxy`
2. 點擊進入編輯頁面

---

### **步驟 3：更新 Worker 代碼**

1. 點擊 **Quick Edit** 按鈕
2. 刪除所有現有代碼
3. 複製 `cloudflare-worker-deepseek-reasoner.js` 的內容
4. 粘貼到編輯器中

**⚠️ 重要：** 替換 `DEEPSEEK_API_KEY`：

```javascript
const DEEPSEEK_API_KEY = 'YOUR_DEEPSEEK_API_KEY'; // ⚠️ 請替換為您的 API Key
```

改為：

```javascript
const DEEPSEEK_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'; // ✅ 您的實際 API Key
```

---

### **步驟 4：保存並部署**

1. 點擊 **Save and Deploy** 按鈕
2. 等待部署完成（通常 10-30 秒）
3. 看到 ✅ **Deployed** 提示

---

### **步驟 5：測試 Worker**

#### **測試 1：健康檢查（GET 請求）**

在瀏覽器中訪問：
```
https://deepseek-proxy.vaultcaddy.workers.dev
```

**預期響應：**
```json
{
  "status": "ok",
  "version": "2.0.0",
  "supported_models": [
    "deepseek-chat",
    "deepseek-reasoner"
  ],
  "max_timeout": "60 seconds",
  "updated": "2025-11-16"
}
```

如果看到這個響應，說明 Worker 已成功部署！✅

---

#### **測試 2：DeepSeek API 調用（POST 請求）**

使用以下代碼測試（在瀏覽器控制台中運行）：

```javascript
// 測試 deepseek-reasoner 模型
fetch('https://deepseek-proxy.vaultcaddy.workers.dev', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        model: 'deepseek-reasoner',
        messages: [
            {
                role: 'system',
                content: '你是一個測試助手。'
            },
            {
                role: 'user',
                content: '請回答：1+1=?'
            }
        ],
        temperature: 0.1,
        max_tokens: 100
    })
})
.then(response => response.json())
.then(data => {
    console.log('✅ Worker 測試成功:', data);
    console.log('📝 AI 回答:', data.choices[0].message.content);
})
.catch(error => {
    console.error('❌ Worker 測試失敗:', error);
});
```

**預期結果：**
```
✅ Worker 測試成功: {choices: [...], usage: {...}}
📝 AI 回答: 1+1=2
```

---

## 🔍 關鍵改進對比

### **舊 Worker（1.0.0）**

```javascript
// ❌ 只支持 deepseek-chat
const SUPPORTED_MODELS = [
    'deepseek-chat'
];

// ❌ 超時 30 秒
const timeoutId = setTimeout(() => controller.abort(), 30000);

// ❌ 沒有正確轉發 max_tokens
body: JSON.stringify({
    model: requestBody.model,
    messages: requestBody.messages,
    temperature: requestBody.temperature || 0.1,
    max_tokens: 4096 // ❌ 固定為 4096
}),
```

---

### **新 Worker（2.0.0）**

```javascript
// ✅ 支持 deepseek-reasoner
const SUPPORTED_MODELS = [
    'deepseek-chat',
    'deepseek-reasoner' // ✅ 新增
];

// ✅ 超時 60 秒（與前端一致）
const timeoutId = setTimeout(() => controller.abort(), 60000);

// ✅ 正確轉發 max_tokens
const maxTokens = requestBody.max_tokens || 4096;
body: JSON.stringify({
    model: requestBody.model,
    messages: requestBody.messages,
    temperature: requestBody.temperature || 0.1,
    max_tokens: maxTokens // ✅ 使用請求中的 max_tokens
}),
```

---

## 📊 預期效果

### **部署前（舊 Worker）**
- ❌ `deepseek-reasoner` 請求被拒絕
- ❌ 超時錯誤（30 秒）
- ❌ `max_tokens: 8192` 被忽略，固定為 4096

### **部署後（新 Worker）**
- ✅ `deepseek-reasoner` 請求成功
- ✅ 60 秒超時（足夠處理複雜文檔）
- ✅ `max_tokens: 8192` 正確傳遞

---

## 🧪 測試計劃

### **測試 1：單頁發票**
- **預期：** 正常處理（8 秒）
- **驗證：** 檢查控制台日誌

### **測試 2：3 頁銀行對帳單**
- **預期：** 成功處理（18 秒）
- **驗證：**
  - ✅ 所有 14 筆交易都被提取
  - ✅ 賬戶信息正確
  - ✅ 期初/期末餘額正確
  - ✅ 控制台顯示：`✅ DeepSeek Reasoner 分析（香港可用）`

### **測試 3：5 頁收據**
- **預期：** 成功處理（25 秒）
- **驗證：** 所有商品項目都被提取

---

## 🚨 常見問題

### **問題 1：Worker 部署後仍然失敗**

**可能原因：**
- ❌ 瀏覽器緩存了舊的 Worker 響應

**解決方案：**
1. 清除瀏覽器緩存
2. 硬刷新頁面（Ctrl + Shift + R 或 Cmd + Shift + R）
3. 重新上傳文檔測試

---

### **問題 2：Worker 返回 401 錯誤**

**可能原因：**
- ❌ `DEEPSEEK_API_KEY` 不正確或過期

**解決方案：**
1. 檢查 DeepSeek API Key 是否正確
2. 訪問 https://platform.deepseek.com/ 確認 API Key 狀態
3. 如果過期，生成新的 API Key 並更新 Worker

---

### **問題 3：Worker 返回 504 超時錯誤**

**可能原因：**
- ❌ 文檔過於複雜，60 秒仍不夠

**解決方案：**
1. 檢查文檔大小和複雜度
2. 考慮進一步優化文本過濾邏輯
3. 或者將超時時間增加到 90 秒：
   ```javascript
   const timeoutId = setTimeout(() => controller.abort(), 90000); // 90 秒
   ```

---

## 📝 部署檢查清單

- [ ] 1. 登錄 Cloudflare Dashboard
- [ ] 2. 找到 `deepseek-proxy` Worker
- [ ] 3. 更新代碼（複製 `cloudflare-worker-deepseek-reasoner.js`）
- [ ] 4. 替換 `DEEPSEEK_API_KEY`
- [ ] 5. 保存並部署
- [ ] 6. 測試健康檢查（GET 請求）
- [ ] 7. 測試 DeepSeek API 調用（POST 請求）
- [ ] 8. 清除瀏覽器緩存
- [ ] 9. 重新上傳文檔測試
- [ ] 10. 驗證所有交易記錄都被提取

---

## 🎉 部署後驗證

### **控制台日誌應該顯示：**

```
🤖 混合處理器初始化
   ✅ Vision API OCR（香港可用）
   ✅ DeepSeek Reasoner 分析（香港可用）
   📊 預期準確度: 90%
   💰 預估成本: ~$0.0006/張
   📝 輸出長度: 最大 64K tokens

🚀 批量處理器開始處理: 3 頁 (bank_statement)
📸 步驟 1：批量 OCR 3 頁...
  📄 啟動 OCR 第 1 頁: ...
  📄 啟動 OCR 第 2 頁: ...
  📄 啟動 OCR 第 3 頁: ...
✅ 批量 OCR 完成，提取了 3 頁
  📄 第 1 頁: 2521 字符
  📄 第 2 頁: 2551 字符
  📄 第 3 頁: 2551 字符

🔍 步驟 2：過濾 3 頁的無用文本...
  ✅ 第 1 頁: 2521 → 1800 字符（減少 28%）
  ✅ 第 2 頁: 2551 → 1800 字符（減少 29%）
  ✅ 第 3 頁: 2551 → 1800 字符（減少 29%）

📋 步驟 3：合併所有頁面的文本...
✅ 合併完成：總計 5400 字符

🧠 步驟 4：使用 DeepSeek Chat 分析合併文本（單次調用）...
🔄 DeepSeek API 請求（第 1 次嘗試）...
✅ DeepSeek API 請求成功（第 1 次嘗試）

✅ 批量處理完成，總耗時: 18000ms
📊 性能統計：
   - 頁數: 3
   - OCR 調用: 3 次
   - DeepSeek 調用: 1 次
   - 總字符數: 5400
   - 平均每頁: 1800 字符
```

---

## 💡 下一步

部署完成後：
1. ✅ 清除瀏覽器緩存
2. ✅ 重新上傳 `eStatementFile_20250829143359.pdf`
3. ✅ 驗證所有 14 筆交易都被提取
4. ✅ 檢查處理時間是否 < 20 秒

**準備測試！** 🚀

