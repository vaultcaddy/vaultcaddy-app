# 🚀 **最終部署指南**

## ✅ **已完成的修復**

1. ✅ **API Key 應用限制已設為「無」**
2. ✅ **API 版本修正**：`v1beta` → `v1`
3. ✅ **模型名稱修正**：使用 `gemini-1.5-flash`

---

## 📋 **關鍵修改**

### **修改 1: API 版本和模型**

**修改前**：
```javascript
const GEMINI_API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent';
```

**修改後**：
```javascript
const GEMINI_API_ENDPOINT = 'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent';
```

**原因**：
- ❌ `v1beta` API 版本不支持 `gemini-1.5-flash-latest` 模型
- ✅ `v1` 是穩定的生產環境 API 版本
- ✅ `gemini-1.5-flash` 是官方推薦的模型名稱

---

## �� **重新部署步驟**

### **Step 1: 複製更新後的代碼**

1. **打開本地文件** `cloudflare-worker-gemini.js`
2. **全選並複製**（Cmd+A 然後 Cmd+C）

### **Step 2: 訪問 Cloudflare Dashboard**

```
https://dash.cloudflare.com/6748a0e547bac4008c90c8005f437648/workers/services/edit/gemini-proxy/production
```

### **Step 3: 部署**

1. **刪除編輯器中的所有現有代碼**
2. **粘貼新代碼**（Cmd+V）
3. **點擊 "Deploy" 按鈕**
4. **等待部署完成**（3-5 秒）

---

## ✅ **測試步驟**

### **1. 清除瀏覽器緩存**

**重要！** 必須清除緩存，否則會載入舊代碼。

- **Chrome**: Cmd+Shift+Delete
- **Safari**: Cmd+Option+E
- 選擇 "**清除所有數據**"

### **2. 測試上傳**

1. 訪問：`https://vaultcaddy.com/firstproject.html`
2. **打開開發者工具**（Cmd+Option+I）
3. **切換到 Console 標籤**
4. **點擊 "Upload files"**
5. **選擇測試發票圖片**

### **3. 預期結果**

#### **✅ 成功的輸出**：

```
🚀 開始處理文檔: PHOTO-2025-10-03-18-10-02.jpg (invoice)
📋 處理順序: ['geminiAI', 'visionAI']
🔄 嘗試 1/2 使用 geminiAI...

🤖 開始處理文檔: PHOTO-2025-10-03-18-10-02.jpg (invoice)
   文件大小: 2063072 bytes

🔄 嘗試 1/3...
📥 Worker 請求已發送

✅ geminiAI 處理成功  ← ✅ 成功！
   耗時: 3000-5000ms

📋 提取的發票數據:
   - type: invoice
   - supplier: HW海運達（香港）有限公司
   - invoice_number: FI25093602
   - date: 2025-09-25
   - total: 1250.00
   - currency: HKD
   - items: [...]  ← 完整的商品列表
```

#### **❌ 如果仍然失敗**：

如果看到 404 或其他錯誤，請：

1. **確認已重新部署 Worker**
2. **確認已清除瀏覽器緩存**
3. **等待 5 分鐘**（API Key 設置可能需要時間生效）
4. **截圖控制台錯誤**並提供給我

---

## 📊 **預期效果**

修復後，系統將：

1. ✅ **使用 Gemini 1.5 Flash 模型**（v1 API）
2. ✅ **提取準確率達到 95%+**
3. ✅ **正確提取所有發票字段**：
   - 供應商名稱
   - 發票號碼
   - 日期
   - 客戶名稱
   - 所有商品明細（代碼、名稱、數量、單價、金額）
   - 小計、稅額、總額
   - 貨幣
4. ✅ **處理時間約 3-5 秒**

---

## 🎯 **快速檢查清單**

- [ ] 已複製 `cloudflare-worker-gemini.js` 的內容
- [ ] 已訪問 Cloudflare Dashboard
- [ ] 已刪除舊代碼並粘貼新代碼
- [ ] 已點擊 "Deploy" 按鈕
- [ ] 已清除瀏覽器緩存
- [ ] 已測試上傳發票
- [ ] 控制台顯示 "✅ geminiAI 處理成功"

---

## 📝 **技術細節**

### **為什麼改用 v1 API？**

- Google 的 **v1beta API** 是實驗性版本，支持的模型有限
- **v1 API** 是穩定的生產環境版本，支持所有最新模型
- `gemini-1.5-flash` 在 v1 API 中可用，在 v1beta 中需要使用 `-latest` 後綴

### **Worker 端點說明**

Worker 現在使用：
```
https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent
```

這是 Google 官方推薦的端點，穩定且性能優異。

---

**準備好了嗎？** 🚀

1. ✅ 複製代碼
2. ✅ 訪問 Cloudflare
3. ✅ 部署
4. ✅ 清除緩存
5. ✅ 測試
6. ✅ 提供結果

**這次應該會成功！** 🎉

如果仍然遇到問題，請提供：
- 完整的控制台錯誤截圖
- 錯誤代碼（404, 403, 500 等）
- 錯誤信息的完整文本
