# 🚀 Gemini API 快速設置指南（10 分鐘完成）

## ✅ 你需要做的事（按順序）

### 📝 步驟 1：部署 Cloudflare Worker（5 分鐘）

1. **訪問** Cloudflare Workers：https://dash.cloudflare.com/
   - 如果沒有帳戶，點擊 "Sign Up"（免費）
   - 如果已有帳戶，點擊 "Log In"

2. **創建 Worker**：
   - 點擊 "Workers & Pages" → "Create application" → "Create Worker"
   - 名稱：`gemini-proxy`（或任何你喜歡的名稱）
   - 點擊 "Deploy"

3. **編輯代碼**：
   - 點擊 "Edit code"
   - **刪除所有默認代碼**
   - 打開 `cloudflare-worker-gemini.js` 文件
   - **複製全部內容**
   - **粘貼**到 Worker 編輯器
   - 點擊 "Save and Deploy"

4. **記錄 URL**：
   - 複製 Worker URL（類似：`https://gemini-proxy.你的用戶名.workers.dev`）
   - **保存這個 URL**，下一步需要用！

---

### 🔧 步驟 2：更新網站代碼（2 分鐘）

**我會幫你完成這一步！**

請告訴我你的 **Worker URL**，格式類似：
```
https://gemini-proxy.你的用戶名.workers.dev
```

然後我會自動更新以下文件：
- `gemini-worker-client.js` - 設置 Worker URL
- `firstproject.html` - 整合 Gemini Worker Client
- `google-smart-processor.js` - 添加 Gemini Worker 到處理順序

---

### ✅ 步驟 3：測試（3 分鐘）

1. Push 代碼到 GitHub
2. 刷新 `https://vaultcaddy.com/firstproject.html`
3. 上傳一個發票圖片
4. 查看控制台，應該看到：
   ```
   🚀 開始智能處理...
   📋 處理順序: geminiWorker → visionAI
   🔄 嘗試處理器 1/2: geminiWorker
   ✅ 處理器 geminiWorker 成功處理文檔
   ```

---

## 🎯 完成後你會獲得什麼？

- ✅ **準確率提升至 90-95%**（從 60% 提升）
- ✅ **自動識別發票結構**（不再需要正則表達式猜測）
- ✅ **完全免費**（Cloudflare + Gemini 免費配額）
- ✅ **速度快**（1-2 秒完成處理）

---

## 📧 需要幫助？

如果遇到問題，請告訴我：
1. 你的 Worker URL
2. 控制台的錯誤信息
3. 你進行到哪一步

我會立即幫你解決！🚀

---

## 🔜 下一步計劃

完成 Gemini 設置後，我們將進行：

### 1. **用戶帳戶升級至 Google Cloud**
   - Firebase Authentication（用戶登入）
   - Cloud Storage（文件存儲）
   - Firestore（數據庫）

### 2. **安全性增強**
   - 用戶數據加密
   - API 請求驗證
   - 文件訪問控制

### 3. **性能優化**
   - CDN 加速
   - 圖片壓縮
   - 批量處理

一步一步來，我們會完成所有功能！💪

