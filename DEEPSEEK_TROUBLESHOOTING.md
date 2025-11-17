# DeepSeek API 故障排除完整指南

## 🚨 當前問題

**症狀：** 上傳發票/銀行對帳單後，無法成功調用 DeepSeek AI

**錯誤信息：**
```
❌ DeepSeek API 請求失敗（已重試 3 次）: signal is aborted without reason
```

---

## ✅ 已完成的修復

1. ✅ 前端已切換到 `deepseek-reasoner` 模型
2. ✅ 前端已增加 `max_tokens` 到 8192
3. ✅ 前端已增加超時時間到 60 秒
4. ✅ Cloudflare Worker 已更新代碼
5. ✅ 創建了新的 API Key：`sk-d0edd459796441c1905439794123867`

---

## 🔍 需要檢查的問題

### **問題 1：Cloudflare Worker API Key 是否正確更新？**

**檢查步驟：**

1. 訪問：https://dash.cloudflare.com/
2. 進入 **Workers & Pages** → **deepseek-proxy**
3. 點擊 **Quick Edit**
4. 檢查第 22 行：

```javascript
// ❌ 如果還是舊的 Key
const DEEPSEEK_API_KEY = 'sk-258e49c87c4d47d88e62cd18d4bbfc8c';

// ✅ 應該改為新的 Key
const DEEPSEEK_API_KEY = 'sk-d0edd459796441c1905439794123867';
```

5. 如果不是新 Key，請更新並點擊 **Save and Deploy**

---

### **問題 2：Cloudflare Worker 是否真的部署成功？**

**測試步驟：**

在瀏覽器訪問：
```
https://deepseek-proxy.vaultcaddy.workers.dev
```

**預期響應：**
```json
{
  "status": "ok",
  "version": "2.0.0",
  "supported_models": ["deepseek-chat", "deepseek-reasoner"],
  "max_timeout": "60 seconds",
  "updated": "2025-11-16"
}
```

**如果看不到這個響應：**
- ❌ Worker 沒有正確部署
- ❌ 需要重新保存並部署

---

### **問題 3：新的 API Key 是否有效？**

**測試步驟：**

在瀏覽器控制台運行：

```javascript
// 直接測試 DeepSeek API
fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-d0edd459796441c1905439794123867'
    },
    body: JSON.stringify({
        model: 'deepseek-reasoner',
        messages: [
            {role: 'system', content: '你是測試助手'},
            {role: 'user', content: '回答：1+1=?'}
        ],
        max_tokens: 100
    })
})
.then(r => r.json())
.then(data => {
    if (data.error) {
        console.error('❌ API Key 無效:', data);
    } else {
        console.log('✅ API Key 有效:', data);
        console.log('📝 回答:', data.choices[0].message.content);
    }
});
```

**預期結果：**
- ✅ 返回 AI 回答（1+1=2）
- ❌ 如果返回 401 錯誤，API Key 無效

---

### **問題 4：是否有瀏覽器緩存問題？**

**清除緩存步驟：**

1. **清除瀏覽器緩存**
   - Chrome：設置 → 隱私和安全性 → 清除瀏覽數據
   - 選擇：緩存的圖片和文件
   - 時間範圍：全部時間

2. **硬刷新頁面**
   - Windows/Linux：Ctrl + Shift + R
   - Mac：Cmd + Shift + R

3. **重啟瀏覽器**
   - 完全關閉瀏覽器
   - 重新打開

---

### **問題 5：Cloudflare Worker 是否支持 `deepseek-reasoner`？**

**檢查步驟：**

在 Cloudflare Worker 代碼中，確認第 25-28 行：

```javascript
// ✅ 正確：支持兩個模型
const SUPPORTED_MODELS = [
    'deepseek-chat',
    'deepseek-reasoner' // ✅ 必須包含
];
```

**如果沒有 `deepseek-reasoner`：**
- 添加這一行
- 保存並部署

---

## 📝 完整修復檢查清單

### **步驟 1：更新 Cloudflare Worker API Key**

- [ ] 訪問 Cloudflare Dashboard
- [ ] 編輯 `deepseek-proxy` Worker
- [ ] 將第 22 行改為：`const DEEPSEEK_API_KEY = 'sk-d0edd459796441c1905439794123867';`
- [ ] 點擊 **Save and Deploy**
- [ ] 等待 10-30 秒

---

### **步驟 2：測試 Worker 健康檢查**

- [ ] 訪問：https://deepseek-proxy.vaultcaddy.workers.dev
- [ ] 確認返回 JSON（包含 `"deepseek-reasoner"`）
- [ ] 如果返回錯誤，重新部署 Worker

---

### **步驟 3：測試 DeepSeek API Key**

- [ ] 在控制台運行測試代碼（見上面）
- [ ] 確認 API Key 有效
- [ ] 如果無效，在 DeepSeek 平台重新生成

---

### **步驟 4：清除瀏覽器緩存**

- [ ] 清除所有緩存的圖片和文件
- [ ] 硬刷新頁面（Ctrl + Shift + R）
- [ ] 重啟瀏覽器

---

### **步驟 5：測試上傳**

- [ ] 上傳一個簡單的發票
- [ ] 打開瀏覽器開發者工具（F12）
- [ ] 檢查 Console 標籤的日誌
- [ ] 檢查 Network 標籤的請求

---

## 🔍 診斷日誌分析

### **成功的日誌應該是：**

```
🤖 混合處理器初始化
   ✅ Vision API OCR（香港可用）
   ✅ DeepSeek Reasoner 分析（香港可用）
   📊 預期準確度: 90%
   💰 預估成本: ~$0.0006/張
   📝 輸出長度: 最大 64K tokens

🚀 批量處理器開始處理: 3 頁 (bank_statement)
📸 步驟 1：批量 OCR 3 頁...
✅ 批量 OCR 完成，提取了 3 頁

🔍 步驟 2：過濾 3 頁的無用文本...
✅ 過濾完成

📋 步驟 3：合併所有頁面的文本...
✅ 合併完成：總計 5400 字符

🧠 步驟 4：使用 DeepSeek Chat 分析合併文本（單次調用）...
🔄 DeepSeek API 請求（第 1 次嘗試）...
✅ DeepSeek API 請求成功（第 1 次嘗試）  // ✅ 這一行很重要！

✅ 批量處理完成，總耗時: 18000ms
```

### **失敗的日誌：**

```
🔄 DeepSeek API 請求（第 1 次嘗試）...
❌ DeepSeek API 請求失敗（第 1 次嘗試）: signal is aborted without reason
⏳ 等待 2 秒後重試...
🔄 DeepSeek API 請求（第 2 次嘗試）...
❌ DeepSeek API 請求失敗（第 2 次嘗試）: signal is aborted without reason
⏳ 等待 4 秒後重試...
🔄 DeepSeek API 請求（第 3 次嘗試）...
❌ DeepSeek API 請求失敗（第 3 次嘗試）: signal is aborted without reason
❌ DeepSeek API 請求失敗（已重試 3 次）: signal is aborted without reason
```

---

## 🐛 可能的錯誤原因

### **錯誤 1：401 Unauthorized**

**原因：** API Key 無效

**解決方案：**
1. 重新生成 API Key
2. 更新 Cloudflare Worker
3. 保存並部署

---

### **錯誤 2：signal is aborted without reason**

**可能原因：**
1. ❌ Worker 沒有正確部署
2. ❌ Worker 超時（30 秒）
3. ❌ DeepSeek API 響應慢
4. ❌ 網絡連接問題

**解決方案：**
1. 確認 Worker 已部署
2. 確認 Worker 超時設置為 60 秒
3. 測試 DeepSeek API 直接調用
4. 檢查網絡連接

---

### **錯誤 3：模型不支持**

**原因：** Worker 不支持 `deepseek-reasoner`

**解決方案：**
1. 在 Worker 的 `SUPPORTED_MODELS` 數組中添加 `'deepseek-reasoner'`
2. 保存並部署

---

## 💡 臨時解決方案

如果以上方法都無法解決，可以嘗試：

### **方案 1：回退到 `deepseek-chat`**

暫時改回 `deepseek-chat` 模型：

1. 在 `hybrid-vision-deepseek.js` 第 26 行：
   ```javascript
   this.deepseekModel = 'deepseek-chat'; // 暫時回退
   ```

2. 在 `hybrid-vision-deepseek.js` 第 392 行：
   ```javascript
   max_tokens: 4096 // 改回 4096
   ```

3. 重新測試

---

### **方案 2：直接調用 DeepSeek API（不通過 Worker）**

修改 `hybrid-vision-deepseek.js`，直接調用 DeepSeek API：

```javascript
// 在 analyzeTextWithDeepSeek 方法中
const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-d0edd459796441c1905439794123867'
    },
    body: JSON.stringify({
        model: 'deepseek-reasoner',
        messages: [
            {role: 'system', content: systemPrompt},
            {role: 'user', content: userPrompt}
        ],
        temperature: 0.1,
        max_tokens: 8192
    })
});
```

**注意：** 這會暴露 API Key 在前端，不推薦長期使用！

---

## 🎯 下一步行動

1. **立即執行：** 完成上面的 5 個檢查步驟
2. **測試：** 上傳一個簡單的發票
3. **反饋：** 告訴我控制台的完整日誌輸出

我需要看到：
- ✅ Worker 健康檢查的響應
- ✅ API Key 測試的結果
- ✅ 上傳文檔的完整控制台日誌

這樣我才能準確診斷問題！🚀

