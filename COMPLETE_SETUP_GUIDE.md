# 🎯 完整設置指南：DeepSeek Reasoner + Vision API OCR

## 📋 系統架構

```
用戶上傳發票圖片
    ↓
Vision API OCR（提取文本）
    ↓
DeepSeek Reasoner（思考模式 - 結構化提取）
    ↓
返回結構化數據並顯示
```

---

## ✅ 第一步：驗證所有文件已更新

### 檢查清單

- [x] `hybrid-ocr-deepseek-processor.js` - 使用 `deepseek-reasoner`
- [x] `google-smart-processor.js` - 只使用混合處理器
- [x] `cloudflare-worker-deepseek.js` - 支持 `deepseek-reasoner`，正確的成本計算
- [x] `firstproject.html` - 加載混合處理器

### 驗證方法

```bash
# 檢查文件是否存在
ls -la hybrid-ocr-deepseek-processor.js
ls -la cloudflare-worker-deepseek.js
ls -la google-smart-processor.js
```

---

## 🚀 第二步：部署 Cloudflare Worker

### 2.1 打開 Cloudflare Dashboard

1. 訪問 https://dash.cloudflare.com/
2. 登入您的帳戶
3. 點擊左側 "Workers & Pages"
4. 找到 `deepseek-proxy`

### 2.2 更新 Worker 代碼

1. 點擊 "Quick edit"
2. **刪除所有舊代碼**
3. 打開項目中的 `cloudflare-worker-deepseek.js`
4. **複製全部內容**（第 1-201 行）
5. 粘貼到 Cloudflare 編輯器
6. 點擊 "Save and Deploy"
7. 等待 5-10 秒

### 2.3 驗證部署

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

✅ 如果看到這個，說明 Worker 已成功部署！

---

## 🧪 第三步：測試系統

### 3.1 清除瀏覽器緩存

**重要**：必須清除緩存以加載最新代碼！

```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

或者：
1. 打開開發者工具（F12）
2. 右鍵點擊刷新按鈕
3. 選擇 "清空緩存並硬性重新載入"

### 3.2 打開測試頁面

1. 訪問 `https://vaultcaddy.com/firstproject.html`
2. 打開瀏覽器控制台（F12）
3. 查看 Console 標籤

### 3.3 檢查初始化日誌

**預期日誌**：
```
🔄 混合處理器初始化（DeepSeek Reasoner）
   ✅ Vision API OCR: 可用
   ✅ DeepSeek Model: deepseek-reasoner
   ✅ DeepSeek Worker: https://deepseek-proxy.vaultcaddy.workers.dev
   🧠 使用思考模式（Reasoning Mode）
   📊 預期準確度: 90-95%
   💰 成本: Vision API $1.50/1K + DeepSeek ¥2/1M tokens

🧠 智能處理器初始化
   🔄 使用: Vision API OCR + DeepSeek Reasoner (思考模式)
   ❌ 已禁用: OpenAI, Gemini, 其他 AI
```

✅ 如果看到這些日誌，說明系統初始化成功！

### 3.4 上傳測試發票

1. 點擊 "Upload files" 按鈕
2. 選擇文檔類型（例如：Invoice）
3. 選擇一個測試發票圖片
4. 點擊 "確定"

### 3.5 查看處理日誌

**預期完整日誌**：

```
🚀 混合處理器開始處理: invoice.jpg (invoice)

📸 步驟 1/2: 使用 Vision API 進行 OCR...
✅ OCR 完成，耗時: 1500ms
📄 提取的文本長度: 1234 字符
📄 文本預覽: INVOICE
Invoice No: INV-2025-001
Date: 2025-01-15
...

🤖 步驟 2/2: 使用 DeepSeek 處理文本...
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
  hasChoices: true,
  usage: {
    prompt_tokens: 1500,
    completion_tokens: 1000,
    total_tokens: 2500,
    estimated_cost_cny: "0.0060"
  }
}

✅ DeepSeek 處理完成，耗時: 2000ms

🎉 混合處理完成，總耗時: 3500ms
```

### 3.6 驗證提取的數據

檢查表格中顯示的數據：

**應該包含**：
- ✅ 發票號碼（Invoice Number）
- ✅ 日期（Date）
- ✅ 供應商信息（Supplier）
- ✅ 客戶信息（Customer）
- ✅ 行項目（Line Items）
- ✅ 金額（Subtotal, Tax, Total）
- ✅ 幣種（Currency）

---

## 💰 第四步：驗證成本追蹤

### 4.1 查看 Cloudflare Worker 日誌

1. 打開 Cloudflare Dashboard
2. 進入 "Workers & Pages"
3. 點擊 `deepseek-proxy`
4. 點擊 "Logs" 標籤
5. 點擊 "Begin log stream"

### 4.2 預期日誌內容

```javascript
📥 收到 DeepSeek 請求: {
  origin: "https://vaultcaddy.com",
  model: "deepseek-reasoner",
  hasMessages: true,
  messageCount: 2,
  hasImages: false,
  timestamp: "2025-10-27T..."
}

📤 DeepSeek 響應: {
  model: "deepseek-reasoner",
  status: 200,
  ok: true,
  hasChoices: true,
  usage: {
    prompt_tokens: 1500,
    completion_tokens: 1000,
    total_tokens: 2500,
    estimated_cost_cny: "0.0060"  // ¥0.006 = $0.00084
  },
  timestamp: "2025-10-27T..."
}
```

### 4.3 計算實際成本

**每張發票的成本**：
```
Vision API: $0.0015（1 張）
DeepSeek:   $0.00084（根據實際 token 用量）
───────────────────────
總計:       $0.00234 ≈ $0.0024
```

**每 1,000 張**：
```
Vision API: $1.50
DeepSeek:   $0.84
───────────────────────
總計:       $2.34
```

---

## 🔍 第五步：故障排除

### 問題 1：Worker 返回 404

**症狀**：
```
Failed to load resource: the server responded with a status of 404
```

**原因**：Worker 未部署或 URL 錯誤

**解決方案**：
1. 檢查 Worker 名稱是否為 `deepseek-proxy`
2. 檢查 URL 是否為 `https://deepseek-proxy.vaultcaddy.workers.dev`
3. 重新部署 Worker

### 問題 2：Worker 返回 400

**症狀**：
```
DeepSeek API error: 400
```

**原因**：
1. API Key 無效
2. 請求格式錯誤
3. 模型名稱錯誤

**解決方案**：
1. 檢查 API Key：`sk-4a43b49a13a840009052be65f599b7a4`
2. 確認使用 `deepseek-reasoner` 模型
3. 確認請求格式符合 OpenAI 標準

### 問題 3：OCR 失敗

**症狀**：
```
Vision API 未能提取文本
```

**原因**：
1. 圖片質量太差
2. Google Vision API Key 無效
3. 圖片格式不支持

**解決方案**：
1. 使用高質量圖片（至少 300 DPI）
2. 檢查 Vision API Key
3. 使用支持的格式（JPG, PNG, PDF）

### 問題 4：提取的數據不完整

**症狀**：部分字段為空或錯誤

**原因**：
1. OCR 文本不完整
2. DeepSeek 理解錯誤
3. Prompt 不夠詳細

**解決方案**：
1. 提高圖片質量
2. 檢查 OCR 提取的文本
3. 優化 DeepSeek prompt

### 問題 5：處理速度慢

**症狀**：處理時間超過 10 秒

**原因**：
1. Vision API 響應慢
2. DeepSeek API 響應慢
3. 網絡問題

**解決方案**：
1. 檢查網絡連接
2. 查看 API 狀態頁面
3. 考慮使用緩存

---

## 📊 第六步：性能監控

### 6.1 追蹤指標

| 指標 | 目標值 | 如何測量 |
|------|--------|---------|
| **處理時間** | < 5 秒 | 控制台日誌 |
| **準確度** | > 90% | 手動驗證 |
| **成本** | $2.34 / 1K 張 | Worker 日誌 |
| **錯誤率** | < 5% | 錯誤日誌 |

### 6.2 建立監控儀表板

```javascript
// 成本追蹤器（建議實施）
class CostTracker {
    constructor() {
        this.stats = {
            visionAPICalls: 0,
            deepseekInputTokens: 0,
            deepseekOutputTokens: 0,
            totalCost: 0
        };
    }
    
    trackVisionAPI() {
        this.stats.visionAPICalls++;
        this.updateCost();
    }
    
    trackDeepSeek(inputTokens, outputTokens) {
        this.stats.deepseekInputTokens += inputTokens;
        this.stats.deepseekOutputTokens += outputTokens;
        this.updateCost();
    }
    
    updateCost() {
        // Vision API 成本（前 1,000 張免費）
        const visionCost = Math.max(0, this.stats.visionAPICalls - 1000) * 0.0015;
        
        // DeepSeek 成本
        const deepseekCost = (
            (this.stats.deepseekInputTokens / 1000000 * 2) + 
            (this.stats.deepseekOutputTokens / 1000000 * 3)
        ) * 0.14; // CNY to USD
        
        this.stats.totalCost = visionCost + deepseekCost;
    }
    
    getReport() {
        return {
            processed: this.stats.visionAPICalls,
            totalCost: this.stats.totalCost.toFixed(2),
            avgCostPerDoc: (this.stats.totalCost / this.stats.visionAPICalls).toFixed(4)
        };
    }
}

// 使用
const tracker = new CostTracker();
// 在處理後調用
tracker.trackVisionAPI();
tracker.trackDeepSeek(1500, 1000);
console.log('成本報告:', tracker.getReport());
```

---

## ✅ 第七步：驗證清單

### 部署驗證

- [ ] Cloudflare Worker 已部署
- [ ] Worker URL 可訪問
- [ ] Worker 返回正確的錯誤信息

### 功能驗證

- [ ] 瀏覽器緩存已清除
- [ ] 混合處理器初始化成功
- [ ] 可以上傳文件
- [ ] Vision API OCR 正常工作
- [ ] DeepSeek Reasoner 正常工作
- [ ] 提取的數據顯示在表格中

### 數據驗證

- [ ] 發票號碼正確
- [ ] 日期格式正確
- [ ] 供應商信息完整
- [ ] 客戶信息完整
- [ ] 行項目完整
- [ ] 金額計算正確
- [ ] 幣種正確

### 成本驗證

- [ ] Worker 日誌顯示 token 用量
- [ ] 成本計算正確
- [ ] 成本符合預期（$2.34 / 1K 張）

---

## 🎯 預期結果

### 成功標準

1. ✅ **處理時間** < 5 秒
2. ✅ **準確度** > 90%
3. ✅ **成本** ≈ $2.34 / 1,000 張
4. ✅ **錯誤率** < 5%

### 性能指標

| 指標 | 目標 | 實際 |
|------|------|------|
| OCR 時間 | < 2 秒 | _待測試_ |
| DeepSeek 時間 | < 3 秒 | _待測試_ |
| 總處理時間 | < 5 秒 | _待測試_ |
| 準確度 | > 90% | _待測試_ |

---

## 📝 測試報告模板

```
測試日期：2025-10-27
測試人員：[您的名字]

### 測試結果

1. Worker 部署狀態：[ ] 成功 [ ] 失敗
2. 系統初始化：[ ] 成功 [ ] 失敗
3. 文件上傳：[ ] 成功 [ ] 失敗
4. OCR 處理：[ ] 成功 [ ] 失敗
5. DeepSeek 處理：[ ] 成功 [ ] 失敗
6. 數據顯示：[ ] 成功 [ ] 失敗

### 性能數據

- OCR 時間：_____ ms
- DeepSeek 時間：_____ ms
- 總處理時間：_____ ms
- Token 用量：輸入 _____ / 輸出 _____
- 估算成本：¥_____ / $_____

### 準確度評估

- 發票號碼：[ ] 正確 [ ] 錯誤
- 日期：[ ] 正確 [ ] 錯誤
- 供應商：[ ] 正確 [ ] 錯誤
- 客戶：[ ] 正確 [ ] 錯誤
- 行項目：[ ] 完整 [ ] 不完整
- 金額：[ ] 正確 [ ] 錯誤

### 問題記錄

1. _______________
2. _______________
3. _______________

### 總體評價

[ ] 優秀 [ ] 良好 [ ] 需要改進 [ ] 失敗
```

---

## 🚀 完成後的下一步

### 短期（1 週內）

1. 監控系統穩定性
2. 收集用戶反饋
3. 優化 prompt 提高準確度
4. 實施成本追蹤

### 中期（1 個月內）

1. 添加批量處理功能
2. 實施緩存機制
3. 優化處理速度
4. 建立監控儀表板

### 長期（3 個月內）

1. 支持更多文檔類型
2. 實施自動分類
3. 添加數據驗證規則
4. 集成會計軟件

---

**最後更新**：2025-10-27  
**狀態**：✅ 準備測試  
**預計完成時間**：30-60 分鐘

