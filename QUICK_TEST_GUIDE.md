# 🚀 快速測試指南（5 分鐘）

## ✅ 系統已準備就緒

```
✅ Cloudflare Worker 已部署並測試通過
✅ DeepSeek Reasoner (思考模式) 正常運行
✅ Vision API OCR 已配置
✅ 混合處理器已實施
✅ 成本追蹤已啟用
```

---

## 🎯 立即測試（3 個步驟）

### 步驟 1：清除瀏覽器緩存（30 秒）

**Windows**：
```
Ctrl + Shift + R
```

**Mac**：
```
Cmd + Shift + R
```

**或者**：
1. 按 F12 打開開發者工具
2. 右鍵點擊刷新按鈕
3. 選擇 "清空緩存並硬性重新載入"

---

### 步驟 2：打開測試頁面（10 秒）

訪問：
```
https://vaultcaddy.com/firstproject.html
```

打開控制台（F12），應該看到：

```
🔄 混合處理器初始化（DeepSeek Reasoner）
   ✅ Vision API OCR: 可用
   ✅ DeepSeek Model: deepseek-reasoner
   ✅ DeepSeek Worker: https://deepseek-proxy.vaultcaddy.workers.dev
   🧠 使用思考模式（Reasoning Mode）

🧠 智能處理器初始化
   🔄 使用: Vision API OCR + DeepSeek Reasoner (思考模式)
   ❌ 已禁用: OpenAI, Gemini, 其他 AI
```

✅ **如果看到這些日誌，說明系統已準備就緒！**

---

### 步驟 3：上傳測試發票（2 分鐘）

1. 點擊 **"Upload files"** 按鈕
2. 選擇文檔類型（例如：**Invoice**）
3. 選擇一個測試發票圖片
4. 點擊 **"確定"**

**預期處理日誌**：

```
🚀 混合處理器開始處理: invoice.jpg (invoice)

📸 步驟 1/2: 使用 Vision API 進行 OCR...
✅ OCR 完成，耗時: 1500ms
📄 提取的文本長度: 1234 字符

🤖 步驟 2/2: 使用 DeepSeek 處理文本...
✅ DeepSeek 處理完成，耗時: 2000ms

🎉 混合處理完成，總耗時: 3500ms
```

**預期結果**：

表格中應該顯示：
- ✅ 發票號碼
- ✅ 日期
- ✅ 供應商信息
- ✅ 客戶信息
- ✅ 行項目
- ✅ 金額（Subtotal, Tax, Total）
- ✅ 幣種

---

## 💰 成本驗證（可選）

### 查看 Worker 日誌

1. 訪問 https://dash.cloudflare.com/
2. 進入 "Workers & Pages"
3. 點擊 `deepseek-proxy`
4. 點擊 "Logs" 標籤
5. 點擊 "Begin log stream"

**預期日誌**：

```javascript
📥 收到 DeepSeek 請求: {
  model: "deepseek-reasoner",
  hasMessages: true,
  messageCount: 2
}

📤 DeepSeek 響應: {
  model: "deepseek-reasoner",
  status: 200,
  usage: {
    prompt_tokens: 1500,
    completion_tokens: 1000,
    total_tokens: 2500,
    estimated_cost_cny: "0.0060"  // ¥0.006 = $0.00084
  }
}
```

**成本計算**：
```
Vision API: $0.0015
DeepSeek:   $0.00084
───────────────────
總計:       $0.00234 / 張
```

---

## 🔍 快速故障排除

### ❌ 控制台沒有初始化日誌

**原因**：瀏覽器緩存未清除

**解決方案**：
1. 強制刷新（Ctrl+Shift+R）
2. 或使用無痕模式

---

### ❌ Worker 返回 404

**原因**：Worker 未部署

**解決方案**：
```bash
./test-deepseek-worker.sh
```

如果測試失敗，請重新部署 Worker。

---

### ❌ OCR 失敗

**原因**：圖片質量太差

**解決方案**：
1. 使用高質量圖片（至少 300 DPI）
2. 使用支持的格式（JPG, PNG, PDF）

---

### ❌ 提取的數據不完整

**原因**：OCR 文本不完整或 DeepSeek 理解錯誤

**解決方案**：
1. 查看控制台中的 OCR 文本
2. 檢查圖片質量
3. 嘗試不同的發票

---

## 📊 性能目標

| 指標 | 目標 | 實際 |
|------|------|------|
| **處理時間** | < 5 秒 | _待測試_ |
| **準確度** | > 90% | _待測試_ |
| **成本** | $2.34 / 1K 張 | _待測試_ |

---

## ✅ 測試清單

- [ ] 瀏覽器緩存已清除
- [ ] 控制台顯示初始化日誌
- [ ] 可以上傳文件
- [ ] OCR 正常工作（顯示提取的文本）
- [ ] DeepSeek 正常工作（顯示處理完成）
- [ ] 數據顯示在表格中
- [ ] 數據準確度 > 90%

---

## 📝 測試結果報告

```
測試日期：2025-10-27
測試人員：___________

系統狀態：[ ] 成功 [ ] 失敗

處理時間：_____ 秒
準確度：_____ %
成本：$_____ / 張

問題：
1. _______________
2. _______________

總體評價：[ ] 優秀 [ ] 良好 [ ] 需要改進
```

---

## 🎯 下一步

### 如果測試成功 ✅

1. 測試更多發票類型
2. 驗證批量上傳功能
3. 測試導出功能（CSV, QuickBooks）
4. 開始實際使用

### 如果測試失敗 ❌

1. 查看控制台錯誤日誌
2. 運行 `./test-deepseek-worker.sh`
3. 查看 `COMPLETE_SETUP_GUIDE.md`
4. 查看 `DEPLOYMENT_CHECKLIST.md`

---

## 📚 相關文件

- **COMPLETE_SETUP_GUIDE.md** - 完整設置指南（30 分鐘）
- **DEPLOYMENT_CHECKLIST.md** - 部署清單（60 分鐘）
- **test-deepseek-worker.sh** - 自動化測試腳本（2 分鐘）
- **DEEPSEEK_REASONER_COST_ANALYSIS.md** - 成本分析

---

**最後更新**：2025-10-27  
**狀態**：✅ 準備測試  
**預計時間**：5 分鐘

